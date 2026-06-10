#!/usr/bin/env python3
"""fab — single entry point for the Agent-Fabric toolchain.

One command, subcommands for each stage. Thin dispatcher over the same module
mains, so `fab compile` == `afc`, `fab query` == `bql`, `fab sim` == `sim`.

    fab compile EXAMPLE.af [--validate] [-o out.json]   # author  (afc)
    fab query   GRAPH.json "QUERY" [--events ...]        # query   (bql)
    fab sim     BASE.json EVENTS.json [--explode] ...    # emulate (sim)
    fab vocab                                            # print the shipped vocabulary
    fab grade   GRAPH.json [--json]                      # score model quality
    fab migrate GRAPH.json [--min-quality N]             # promote proposals -> active
    fab test                                             # run the e2e suite

Pure standard library; no install.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

USAGE = __doc__


def _emit_python(kinds, preds, states, version):
    return ('"""Agent-Fabric vocabulary — generated from the registry; do not edit."""\n'
            f'REGISTRY_VERSION = "{version}"\n'
            f"NODE_KINDS = {kinds!r}\n"
            f"RELATION_PREDICATES = {preds!r}\n"
            f"LIFECYCLE_STATES = {states!r}\n")


def _emit_typescript(kinds, preds, states, version):
    union = lambda xs: " | ".join(f'"{x}"' for x in xs)
    arr = lambda xs: "[" + ", ".join(f'"{x}"' for x in xs) + "]"
    return ("// Agent-Fabric vocabulary — generated from the registry; do not edit.\n"
            f'export const REGISTRY_VERSION = "{version}";\n'
            f"export type NodeKind = {union(kinds)};\n"
            f"export type RelationPredicate = {union(preds)};\n"
            f"export type LifecycleState = {union(states)};\n"
            f"export const NODE_KINDS: NodeKind[] = {arr(kinds)};\n"
            f"export const RELATION_PREDICATES: RelationPredicate[] = {arr(preds)};\n"
            f"export const LIFECYCLE_STATES: LifecycleState[] = {arr(states)};\n")


def _emit_go(kinds, preds, states, version):
    arr = lambda xs: "{" + ", ".join(f'"{x}"' for x in xs) + "}"
    return ("// Agent-Fabric vocabulary — generated from the registry; DO NOT EDIT.\n"
            "package fabric\n\n"
            f'const RegistryVersion = "{version}"\n\n'
            f"var NodeKinds = []string{arr(kinds)}\n\n"
            f"var RelationPredicates = []string{arr(preds)}\n\n"
            f"var LifecycleStates = []string{arr(states)}\n")


def _emit_json(kinds, preds, states, version):
    import json
    return json.dumps({"registryVersion": version, "nodeKinds": kinds,
                       "relationPredicates": preds, "lifecycleStates": states},
                      indent=2) + "\n"


_EMITTERS = {"python": _emit_python, "typescript": _emit_typescript,
             "ts": _emit_typescript, "go": _emit_go, "json": _emit_json}


def _vocab(argv):
    """Print or export the vocabulary the product ships with — the registered
    node kinds and relation predicates, the single source of truth.

    fab vocab                      human-readable listing
    fab vocab --lang python|ts|go|json [-o FILE]   generated language bindings
    """
    import fabriclib
    lang = out = None
    i = 0
    while i < len(argv):
        if argv[i] == "--lang":
            lang = argv[i + 1]; i += 2
        elif argv[i] in ("-o", "--out"):
            out = argv[i + 1]; i += 2
        else:
            i += 1
    reg = fabriclib.read_json(os.path.join(ROOT, "schema", "registry", "registry.json"))
    state_reg = fabriclib.read_json(os.path.join(ROOT, "schema", "registry", "states.json"))
    version = reg.get("version", "?")
    kinds = [k["name"] for k in reg["nodeKinds"]]
    preds = [p["name"] for p in reg["relationTypes"]]
    states = [s["name"] for s in state_reg["states"]]

    if lang:
        emit = _EMITTERS.get(lang)
        if not emit:
            print(f"fab: unknown --lang {lang!r}; choose from {', '.join(sorted(_EMITTERS))}",
                  file=sys.stderr)
            return 2
        text = emit(kinds, preds, states, version)
        if out:
            with open(out, "w") as fh:
                fh.write(text)
        else:
            sys.stdout.write(text)
        return 0

    print(f"Agent-Fabric vocabulary (registry {version})\n")
    print(f"NODE KINDS ({len(kinds)}):")
    for k in reg["nodeKinds"]:
        print(f"  {k['name']:<11} {k.get('description', '')}")
    print(f"\nRELATION PREDICATES ({len(preds)}):")
    for p in reg["relationTypes"]:
        dom = ", ".join(p.get("domain") or ["any"])
        rng = ", ".join(p.get("range") or ["any"])
        flags = [f for f in ("symmetric", "transitive") if p.get(f)]
        tail = f"  [{', '.join(flags)}]" if flags else ""
        print(f"  {p['name']:<18} {dom} -> {rng}{tail}")
    print(f"\nLIFECYCLE STATES ({len(states)}):")
    for s in state_reg["states"]:
        print(f"  {s['name']:<11} {s.get('description', '')}")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    cmd, rest = argv[0], argv[1:]

    if cmd in ("compile", "afc", "author"):
        import afc
        return afc.main(rest)
    if cmd in ("query", "bql"):
        import bql
        return bql.main(rest)
    if cmd in ("sim", "emulate", "rebuild"):
        import sim
        return sim.main(rest)
    if cmd in ("vocab", "vocabulary", "registry"):
        return _vocab(rest)
    if cmd in ("grade", "quality", "lint"):
        import grade
        return grade.main(rest)
    if cmd in ("migrate", "promote"):
        import migrate
        return migrate.main(rest)
    if cmd in ("test", "e2e"):
        import runpy
        try:
            runpy.run_path(os.path.join(ROOT, "tests", "e2e.py"), run_name="__main__")
        except SystemExit as exc:
            return exc.code or 0
        return 0

    print(f"fab: unknown command {cmd!r}\n", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
