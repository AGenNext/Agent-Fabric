#!/usr/bin/env python3
"""bql — Blockquote Query Language for the Agent-Fabric graph.

A path-traversal query language that uses `>` (markdown's blockquote marker) as
the hop operator over a compiled `Graph` JSON document. `<` traverses edges in
reverse. See spec/bql.md.

    bql.py GRAPH.json "agent:orchestrator-7 > delegates_to > agent[status=busy]"
    bql.py GRAPH.json -f query.bql --json

Grammar (whitespace/newlines insignificant; `#` starts a comment):

    query    := selector hop*
    hop      := ('>' forward | '<' reverse) predicate ('>'|'<') selector
    selector := ('*' | kind | kind ':' name) filter*
    filter   := '[' key ('='|'!=') value (',' key op value)* ']'

`predicate` is a lowercased relation name (e.g. delegates_to) or `*` (any).
A selector with no kind is `*`. Filters match node fields then attributes.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabriclib import coerce, read_json


# ---------------------------------------------------------------- tokenizer ---
def tokenize(text):
    # strip per-line comments
    text = "\n".join(line.split("#", 1)[0] for line in text.splitlines())
    tokens, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
        elif c in "><":
            tokens.append(c)
            i += 1
        else:
            # read an atom, keeping bracketed filters (which may contain spaces) intact
            start, depth = i, 0
            while i < n:
                c = text[i]
                if c == "[":
                    depth += 1
                elif c == "]":
                    depth -= 1
                elif depth == 0 and (c.isspace() or c in "><"):
                    break
                i += 1
            tokens.append(text[start:i])
    return tokens


# ----------------------------------------------------------------- selector ---
class Selector:
    def __init__(self, atom):
        self.kind = None
        self.name = None
        self.filters = []
        # peel off filter groups [ ... ]
        head = atom
        for grp in re.findall(r"\[(.*?)\]", atom):
            for cond in grp.split(","):
                cond = cond.strip()
                if not cond:
                    continue
                m = re.match(r"^(.+?)\s*(!=|=)\s*(.+)$", cond)
                if not m:
                    raise ValueError(f"bad filter condition: {cond!r}")
                self.filters.append((m.group(1).strip(), m.group(2), m.group(3).strip()))
        head = re.sub(r"\[.*?\]", "", head).strip()
        if head and head != "*":
            if ":" in head:
                self.kind, self.name = head.split(":", 1)
            else:
                self.kind = head

    def _field(self, node, key):
        if key in node:
            return node[key]
        return node.get("attributes", {}).get(key)

    def match(self, node):
        if self.kind and node.get("kind", "").lower() != self.kind.lower():
            return False
        if self.name and node.get("id") != f"af:{self.kind.lower()}/{self.name}":
            return False
        for key, op, val in self.filters:
            actual = self._field(node, key)
            if actual is None:
                return False
            eq = coerce(actual) == coerce(val) or str(actual) == val
            if (op == "=" and not eq) or (op == "!=" and eq):
                return False
        return True


# -------------------------------------------------------------------- parser ---
def parse(tokens):
    if not tokens:
        raise ValueError("empty query")
    start = Selector(tokens[0])
    hops, i = [], 1
    while i < len(tokens):
        direction = tokens[i]
        if direction not in "><":
            raise ValueError(f"expected '>' or '<', got {tokens[i]!r}")
        if i + 2 >= len(tokens):
            raise ValueError("incomplete hop: expected `DIR predicate DIR selector`")
        predicate = tokens[i + 1]
        # tokens[i+2] is the trailing direction marker; tokens[i+3] the selector
        sel = Selector(tokens[i + 3])
        hops.append(("reverse" if direction == "<" else "forward", predicate.lower(), sel))
        i += 4
    return start, hops


# ------------------------------------------------------------------ evaluate ---
def evaluate(graph, query):
    nodes = {n["id"]: n for n in graph["nodes"]}
    # Index every edge once by its endpoints; hops are then dict lookups, not
    # scans of the whole edge list. out_index[from] / in_index[to] -> edges.
    out_index, in_index = defaultdict(list), defaultdict(list)
    for e in graph["edges"]:
        out_index[e["from"]].append(e)
        in_index[e["to"]].append(e)
    start, hops = parse(tokenize(query))

    current = [n["id"] for n in graph["nodes"] if start.match(n)]
    for direction, predicate, sel in hops:
        forward = direction == "forward"
        index = out_index if forward else in_index
        endpoint = "to" if forward else "from"
        nxt, seen = [], set()
        for nid in current:
            for e in index[nid]:
                if predicate != "*" and e["relation"].lower() != predicate:
                    continue
                neigh = e[endpoint]
                node = nodes.get(neigh)
                if node and neigh not in seen and sel.match(node):
                    seen.add(neigh)
                    nxt.append(neigh)
        current = nxt
    return [nodes[nid] for nid in current]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Query an Agent-Fabric graph with BQL.")
    ap.add_argument("graph", help="compiled graph JSON file")
    ap.add_argument("query", nargs="?", help="BQL query string")
    ap.add_argument("-f", "--file", help="read the query from a file")
    ap.add_argument("--events", help="overlay this GraphEvent stream and query the "
                                     "emulated state (no subgraph materialized)")
    ap.add_argument("--at", type=int, help="with --events: overlay only up to sequence AT")
    ap.add_argument("--json", action="store_true", help="emit full node objects as JSON")
    args = ap.parse_args(argv)

    if args.file:
        with open(args.file) as fh:
            q = fh.read()
    else:
        q = args.query
    if not q:
        ap.error("provide a query string or -f FILE")

    graph = read_json(args.graph)
    if args.events:
        from kernel import GraphKernel
        events = read_json(args.events)
        if isinstance(events, dict):
            events = events.get("events", [events])
        graph, _ = GraphKernel(graph, events, until=args.at).view()
    try:
        results = evaluate(graph, q)
    except ValueError as e:
        print(f"bql: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for n in results:
            label = n.get("label") or n.get("attributes", {}).get("role") or ""
            print(f"{n['id']}\t{n['kind']}\t{label}".rstrip())
        print(f"# {len(results)} result(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
