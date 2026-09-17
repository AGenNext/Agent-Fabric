#!/usr/bin/env python3
"""migrate — promote a model's proposals to active, once correctness is enforced.

Everything starts as a proposal (the default lifecycle state). Migration is the
supported promotion path: it gates on correctness (the graph must validate) and,
optionally, on a minimum quality score, then promotes every `proposed` (or
unset) element to `active`. Nothing is promoted unless the gate passes.

    migrate.py GRAPH.json [-o out.json] [--min-quality N] [--summary]

Pure standard library.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabriclib import read_json
import afc
import grade as grade_mod


def migrate(graph, min_quality=0):
    """Return (migrated_graph, report). Raises ValueError if a gate fails."""
    errs, _ = afc.validate_graph(graph)
    if errs:
        raise ValueError(f"correctness gate failed ({len(errs)} error(s)); "
                         "fix the model before migrating")
    score, _ = grade_mod.grade(graph)
    if score < min_quality:
        raise ValueError(f"quality gate failed: {score} < {min_quality}")

    promoted = 0
    out = {k: v for k, v in graph.items() if k not in ("nodes", "edges")}
    for key in ("nodes", "edges"):
        items = []
        for el in graph.get(key, []):
            el = dict(el)
            if el.get("state", "proposed") == "proposed":
                el["state"] = "active"
                promoted += 1
            items.append(el)
        out[key] = items
    total = len(graph.get("nodes", [])) + len(graph.get("edges", []))
    return out, {"promoted": promoted, "total": total, "quality": score}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Promote a model's proposals to active.")
    ap.add_argument("graph", help="graph JSON file")
    ap.add_argument("--min-quality", type=float, default=0,
                    help="also require grade >= N before promoting (default 0)")
    ap.add_argument("-o", "--out", help="write the migrated graph here (default: stdout)")
    ap.add_argument("--summary", action="store_true", help="print only the summary")
    args = ap.parse_args(argv)

    graph = read_json(args.graph)
    try:
        migrated, report = migrate(graph, args.min_quality)
    except ValueError as e:
        print(f"migrate: {e}", file=sys.stderr)
        return 1

    print(f"migrate: promoted {report['promoted']}/{report['total']} elements to "
          f"active (quality {report['quality']}/100)", file=sys.stderr)
    if args.summary:
        return 0
    out = json.dumps(migrated, indent=2)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(out + "\n")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
