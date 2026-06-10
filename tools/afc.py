#!/usr/bin/env python3
"""afc — the Fabric Agent Language (FAL) compiler.

Compiles an indentation-style `.af` source file into an Agent-Fabric `Graph`
JSON document that validates against schema/meta/graph.schema.json.

Usage:
    python tools/afc.py path/to/file.af [-o out.json] [--validate]

Language (see spec/dsl.md):

    @id research-snapshot          # optional header directives (column 0, '@')
    @tenant agennext
    @asOf 2026-06-07T12:00:00Z

    workspace research             # <kind> <name>  -> a node
      environment: prod            #   attribute (unknown key -> attributes{})
      purpose: Autonomous squad

    agent researcher-3
      scope: research              #   reserved entity field
      role: executor               #   attribute
      uses: web-search             #   relation predicate -> an edge
      invokes: web-search (weight=17, callCount=17)
      member_of: research-squad

Keys whose UPPER_CASE form is a registered relation predicate emit edges; the
reserved keys (label, description, scope, tenant, state, version, tags) set
entity fields; everything else goes into the node's `attributes`.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabriclib import ROOT, coerce, load_registry, read_json, reserved_fields

CONTEXT = "https://schema.agennext.dev/agent-fabric/context.jsonld"
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")


class FALError(Exception):
    pass


def slug(name):
    """Collapse internal whitespace to single hyphens so names form valid ids."""
    return re.sub(r"\s+", "-", name.strip())


def split_top_level(s, sep=","):
    """Split on `sep` only outside parentheses."""
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def parse_targets(value):
    """'a, b (weight=2, k=v)' -> [('a', {}), ('b', {'weight':2,'k':'v'})]

    A target name may contain spaces (collapsed to a slug on resolution); the
    optional trailing parenthesised group holds k=v modifiers.
    """
    targets = []
    for token in split_top_level(value):
        if "(" in token:
            name, rest = token.split("(", 1)
            mods = rest.rsplit(")", 1)[0]
        else:
            name, mods = token, ""
        name = name.strip()
        if not name:
            raise FALError(f"invalid relation target: {token!r}")
        modmap = {}
        if mods.strip():
            for part in split_top_level(mods):
                if "=" not in part:
                    raise FALError(f"invalid modifier {part!r} (expected k=v)")
                k, v = part.split("=", 1)
                modmap[k.strip()] = coerce(v.strip())
        targets.append((name, modmap))
    return targets


def parse(text):
    """Return (header dict, list of declaration dicts)."""
    header, decls, cur = {}, [], None
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line[0] in " \t"
        body = line.strip()
        if not indented:
            if body.startswith("@"):
                parts = body[1:].split(None, 1)
                header[parts[0]] = parts[1].strip() if len(parts) > 1 else ""
                continue
            parts = body.split(None, 1)
            if len(parts) != 2:
                raise FALError(f"line {lineno}: expected '<kind> <name>', got {body!r}")
            kind, name = parts[0], slug(parts[1])
            if not NAME_RE.match(name):
                raise FALError(f"line {lineno}: invalid node name {name!r}")
            cur = {"kind": kind, "name": name, "props": [], "lineno": lineno}
            decls.append(cur)
        else:
            if cur is None:
                raise FALError(f"line {lineno}: property before any declaration")
            if ":" not in body:
                raise FALError(f"line {lineno}: expected 'key: value', got {body!r}")
            key, value = body.split(":", 1)
            cur["props"].append((key.strip(), value.strip(), lineno))
    return header, decls


def compile_source(text):
    kinds, predicates = load_registry()
    reserved = reserved_fields()
    header, decls = parse(text)

    # The domain (if given) is the identifier namespace: af:<domain>/<kind>/<name>.
    domain = slug(header["domain"]) if header.get("domain") else None
    prefix = f"af:{domain}/" if domain else "af:"

    # First pass: build nodes and a name -> node index.
    by_name, nodes = {}, []
    for d in decls:
        kind = kinds.get(d["kind"].lower())
        if not kind:
            raise FALError(f"line {d['lineno']}: unknown node kind {d['kind']!r}")
        if d["name"] in by_name:
            raise FALError(f"line {d['lineno']}: duplicate node name {d['name']!r}")
        node = {"id": f"{prefix}{kind.lower()}/{d['name']}", "kind": kind}
        by_name[d["name"]] = node
        nodes.append((node, d))

    def resolve(name, lineno):
        name = slug(name)
        if name not in by_name:
            raise FALError(f"line {lineno}: reference to undeclared node {name!r}")
        return by_name[name]

    # Second pass: fill attributes/fields and emit edges.
    edges, seq = [], 0
    for node, d in nodes:
        attrs = {}
        for key, value, lineno in d["props"]:
            pred = predicates.get(key.lower())
            if pred:
                for tname, mods in parse_targets(value):
                    seq += 1
                    target = resolve(tname, lineno)
                    if pred.get("domain") and node["kind"] not in pred["domain"]:
                        raise FALError(
                            f"line {lineno}: {pred['name']} not allowed from {node['kind']}")
                    if pred.get("range") and target["kind"] not in pred["range"]:
                        raise FALError(
                            f"line {lineno}: {pred['name']} not allowed to {target['kind']}")
                    edge = {
                        "id": f"af:rel/{seq}",
                        "relation": pred["name"],
                        "from": node["id"],
                        "to": target["id"],
                    }
                    if pred.get("symmetric"):
                        edge["directed"] = False
                    if "weight" in mods:
                        edge["weight"] = mods.pop("weight")
                    if mods:
                        edge["attributes"] = mods
                    edges.append(edge)
            elif key == "tags":
                node["tags"] = [t.strip() for t in value.split(",") if t.strip()]
            elif key == "scope":
                node["scope"] = resolve(value, lineno)["id"]
            elif key in reserved:
                node[key] = value
            else:
                attrs[key] = coerce(value)
        if attrs:
            node["attributes"] = attrs

    graph = {
        "@context": CONTEXT,
        "id": f"af:graph/{header.get('id', 'compiled')}",
        "kind": "Graph",
        "nodes": [n for n, _ in nodes],
        "edges": edges,
    }
    if "tenant" in header:
        graph["tenant"] = header["tenant"]
    if "scope" in header:
        graph["scope"] = resolve(header["scope"], 0)["id"]
    graph["watermark"] = {"asOf": header.get("asOf", "1970-01-01T00:00:00Z")}
    return graph


def builtin_check(graph):
    """Zero-dependency structural validation of a compiled graph.

    Used as a fallback when the `jsonschema` package isn't installed, so the
    toolchain needs nothing beyond a stock Python interpreter. Checks the
    invariants the meta-model relies on: required fields, registered kinds and
    predicates, and referential integrity of edge endpoints.
    """
    kinds, predicates = load_registry()
    valid_kinds = set(kinds.values())
    errs, ids = [], set()
    for n in graph.get("nodes", []):
        if "id" not in n or "kind" not in n:
            errs.append(f"node missing id/kind: {n.get('id', n)}")
        if n.get("kind") not in valid_kinds:
            errs.append(f"unregistered node kind: {n.get('kind')!r} ({n.get('id')})")
        ids.add(n.get("id"))
    for e in graph.get("edges", []):
        for k in ("id", "relation", "from", "to"):
            if k not in e:
                errs.append(f"edge missing {k}: {e.get('id', e)}")
        if e.get("relation", "").lower() not in predicates:
            errs.append(f"unregistered relation: {e.get('relation')!r} ({e.get('id')})")
        if e.get("from") not in ids:
            errs.append(f"dangling 'from': {e.get('id')} -> {e.get('from')}")
        if e.get("to") not in ids:
            errs.append(f"dangling 'to': {e.get('id')} -> {e.get('to')}")
    return errs


def validate_graph(graph):
    """Validate a graph, preferring full JSON Schema but falling back to the
    built-in check. Returns (errors, mode)."""
    import glob
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError:
        return builtin_check(graph), "builtin (zero-dependency)"
    res = []
    for f in glob.glob(os.path.join(ROOT, "schema", "**", "*.json"), recursive=True):
        d = read_json(f)
        if "$id" in d:
            res.append((d["$id"], Resource.from_contents(d)))
    reg = Registry().with_resources(res)
    schema = read_json(os.path.join(ROOT, "schema", "meta", "graph.schema.json"))
    errs = [f"{list(e.path)} {e.message}"
            for e in Draft202012Validator(schema, registry=reg).iter_errors(graph)]
    return errs, "jsonschema"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compile FAL (.af) to Agent-Fabric graph JSON.")
    ap.add_argument("source")
    ap.add_argument("-o", "--out", help="write JSON here (default: stdout)")
    ap.add_argument("--validate", action="store_true",
                    help="validate output against graph.schema.json (needs jsonschema)")
    args = ap.parse_args(argv)

    try:
        with open(args.source) as fh:
            graph = compile_source(fh.read())
    except FALError as e:
        print(f"afc: {e}", file=sys.stderr)
        return 2

    out = json.dumps(graph, indent=2)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(out + "\n")
    else:
        print(out)

    if args.validate:
        errs, mode = validate_graph(graph)
        if errs:
            for e in errs[:10]:
                print(f"afc: INVALID {e}", file=sys.stderr)
            return 1
        print(f"afc: valid [{mode}] — {len(graph['nodes'])} nodes, "
              f"{len(graph['edges'])} edges", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
