#!/usr/bin/env python3
"""sim — fold a GraphEvent stream onto a base graph to project ("rehearse") state.

The fabric is event-sourced: a graph is the left-fold of an ordered event
stream (meta-model spec, §3.4 / §7). `sim` applies that fold in memory so you
can preview the outcome of a proposed change set *before* committing it for
real — a model of the world, like a storyboard before the shot.

    sim.py BASE.json EVENTS.json [--at SEQ] [-o out.json] [--summary]

Nothing is mutated on disk except an explicit -o output. `--at SEQ` folds only
events up to sequence SEQ (time-travel / partial rehearsal).
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabriclib import read_json


def merge(existing, payload):
    """Apply an upsert payload onto an existing element (attributes merge)."""
    for k, v in payload.items():
        if k == "attributes" and isinstance(existing.get("attributes"), dict) \
                and isinstance(v, dict):
            existing["attributes"] = {**existing["attributes"], **v}
        else:
            existing[k] = v


def fold(base, events, until=None):
    """Return (projected_graph, change_summary) from folding events onto base."""
    nodes = {n["id"]: dict(n) for n in base.get("nodes", [])}
    edges = {e["id"]: dict(e) for e in base.get("edges", [])}
    applied, last_seq, last_at, stream = 0, None, None, None

    for ev in sorted(events, key=lambda e: e.get("sequence", 0)):
        seq = ev.get("sequence", 0)
        if until is not None and seq > until:
            break
        store = nodes if ev["target"] == "node" else edges
        pid = ev["payload"]["id"]
        op = ev["op"]
        if op == "upsert":
            if pid in store:
                merge(store[pid], ev["payload"])
            else:
                store[pid] = dict(ev["payload"])
        elif op == "delete":
            store.pop(pid, None)
        elif op == "invalidate":
            if pid in store:
                store[pid]["validTo"] = ev["payload"].get("validTo", ev.get("occurredAt"))
        applied += 1
        last_seq, last_at = seq, ev.get("occurredAt", last_at)
        stream = ev.get("stream", stream)

    projected = {
        "@context": base.get("@context", "https://schema.agennext.dev/agent-fabric/context.jsonld"),
        "id": base.get("id", "af:graph/projected"),
        "kind": "Graph",
        "nodes": list(nodes.values()),
        "edges": list(edges.values()),
        "watermark": {"asOf": last_at or "1970-01-01T00:00:00Z"},
    }
    if last_seq is not None:
        projected["watermark"]["sequence"] = last_seq
    if stream:
        projected["watermark"]["stream"] = stream
    if "tenant" in base:
        projected["tenant"] = base["tenant"]

    summary = {
        "events_applied": applied,
        "nodes": (len(base.get("nodes", [])), len(nodes)),
        "edges": (len(base.get("edges", [])), len(edges)),
    }
    return projected, summary


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

    projected, summary = fold(base, events, until=args.at)

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
