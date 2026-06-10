#!/usr/bin/env python3
"""sim — project graph state by folding a GraphEvent stream over a base graph.

Thin CLI over the GraphKernel: storage (the base graph + event delta) plus
calculation (the overlay). It previews the outcome of a proposed change set
before it is committed for real — a model of the world, like a storyboard
before the shot. Nothing is mutated except an explicit -o output.

    sim.py BASE.json EVENTS.json [--at SEQ] [-o out.json] [--summary]

`--at SEQ` folds only events up to sequence SEQ (time-travel / partial rehearsal).
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabriclib import read_json
from kernel import GraphKernel


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fold a GraphEvent stream onto a base graph (dry-run).")
    ap.add_argument("base", help="base graph JSON")
    ap.add_argument("events", help="event stream JSON (array of GraphEvent)")
    ap.add_argument("--at", type=int, help="fold only events with sequence <= AT")
    ap.add_argument("-o", "--out", help="write projected graph JSON here (default: stdout)")
    ap.add_argument("--summary", action="store_true", help="print a change summary to stderr only")
    args = ap.parse_args(argv)

    base = read_json(args.base)
    events = read_json(args.events)
    if isinstance(events, dict):
        events = events.get("events", [events])

    projected, summary = GraphKernel(base, events, until=args.at).view()

    n0, n1 = summary["nodes"]
    e0, e1 = summary["edges"]
    print(f"sim: applied {summary['events_applied']} event(s); "
          f"nodes {n0}->{n1}, edges {e0}->{e1}", file=sys.stderr)

    if args.summary:
        return 0
    out = json.dumps(projected, indent=2)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(out + "\n")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
