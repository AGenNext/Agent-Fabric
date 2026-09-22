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
def _split_condition(cond):
    """Split 'key OP value' on the leftmost '!=' or '=', returning
    (key, op, value) or None if there's no valid split.

    Equivalent to `re.match(r"^(.+?)\s*(!=|=)\s*(.+)$", cond)` but scans
    linearly instead of backtracking: with query strings coming straight off
    an untrusted API request (api/server.py's /v1/graphs/query), the lazy
    `.+?` next to `\s*` next to `(.+)$` is an unbounded-backtracking pattern
    over attacker-controlled input (flagged by CodeQL as a polynomial ReDoS).
    A key must be non-empty and a value must be non-empty (pre-strip), same
    as the original pattern required.
    """
    n = len(cond)
    i = 0
    while i < n:
        if cond[i:i + 2] == "!=":
            op, oplen = "!=", 2
        elif cond[i] == "=":
            op, oplen = "=", 1
        else:
            i += 1
            continue
        value = cond[i + oplen:]
        if i == 0 or not value:
            i += 1  # key or value would be empty; keep looking, as the
            continue  # original pattern's non-empty quantifiers would too
        return cond[:i].strip(), op, value.strip()
    return None


class Selector:
    def __init__(self, atom):
        self.kind = None
        self.name = None
        self.filters = []
        # peel off filter groups [ ... ]; a negated character class instead
        # of '.*?' keeps this linear regardless of input shape (unlike '.',
        # '[^\[\]]' can't overlap with the terminator, so there's no
        # backtracking ambiguity for CodeQL's polynomial-ReDoS check to flag).
        head = atom
        for grp in re.findall(r"\[([^\[\]]*)\]", atom):
            for cond in grp.split(","):
                cond = cond.strip()
                if not cond:
                    continue
                split = _split_condition(cond)
                if not split:
                    raise ValueError(f"bad filter condition: {cond!r}")
                self.filters.append(split)
        head = re.sub(r"\[[^\[\]]*\]", "", head).strip()
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


def ego(graph, center, radius=1):
    """Return the ego-network: the center node and every node within `radius`
    hops, in any edge direction. Each party is the centre of its own view."""
    nodes = {n["id"]: n for n in graph["nodes"]}
    if center not in nodes:
        raise ValueError(f"unknown center node: {center}")
    adj = defaultdict(set)
    for e in graph["edges"]:
        adj[e["from"]].add(e["to"])
        adj[e["to"]].add(e["from"])
    order, seen, frontier = [center], {center}, [center]
    for _ in range(max(0, radius)):
        nxt = []
        for nid in frontier:
            for neigh in adj.get(nid, ()):
                if neigh not in seen and neigh in nodes:
                    seen.add(neigh)
                    order.append(neigh)
                    nxt.append(neigh)
        frontier = nxt
        if not frontier:
            break
    return [nodes[nid] for nid in order]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Query an Agent-Fabric graph with BQL.")
    ap.add_argument("graph", help="compiled graph JSON file")
    ap.add_argument("query", nargs="?", help="BQL query string")
    ap.add_argument("-f", "--file", help="read the query from a file")
    ap.add_argument("--events", help="overlay this GraphEvent stream and query the "
                                     "emulated state (no subgraph materialized)")
    ap.add_argument("--at", type=int, help="with --events: overlay only up to sequence AT")
    ap.add_argument("--ego", help="return the ego-network centered on this node id (no QUERY needed)")
    ap.add_argument("--radius", type=int, default=1, help="ego radius in hops (default 1)")
    ap.add_argument("--json", action="store_true", help="emit full node objects as JSON")
    args = ap.parse_args(argv)

    if args.file:
        with open(args.file) as fh:
            q = fh.read()
    else:
        q = args.query
    if not q and not args.ego:
        ap.error("provide a query string, -f FILE, or --ego NODE")

    graph = read_json(args.graph)
    if args.events:
        from kernel import GraphKernel
        events = read_json(args.events)
        if isinstance(events, dict):
            events = events.get("events", [events])
        graph, _ = GraphKernel(graph, events, until=args.at).view()
    try:
        results = ego(graph, args.ego, args.radius) if args.ego else evaluate(graph, q)
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
