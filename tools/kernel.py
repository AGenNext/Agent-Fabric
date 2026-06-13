"""GraphKernel — the emulation kernel for Agent-Fabric.

Emulation is modelled by the kernel, not by materializing a separate subgraph.
A `GraphKernel` overlays an ordered `GraphEvent` delta on a base graph and
presents the emulated state on demand. Change the kernel (append events, move
the `until` watermark) and every read reflects it — no projected subgraph needs
to be built or stored. `sim` and `bql --events` both read through this one
kernel, so the fold semantics live in a single place. Pure standard library.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabriclib import load_registry


class KernelError(ValueError):
    """An event violated correctness at ingestion."""


def _enforce(ev):
    """Enforce intrinsic correctness on an event before it touches the store:
    a payload id, and — for upserts — a registered kind (nodes) or registered
    predicate with from/to (edges). Order-dependent checks (referential
    integrity) are left to graph-level validation, since events may arrive
    out of order. Raises KernelError on violation."""
    kinds, preds = load_registry()
    p = ev.get("payload") or {}
    eid = ev.get("id", "?")
    if "id" not in p:
        raise KernelError(f"event {eid}: payload has no id")
    if ev.get("op") == "upsert":
        if ev.get("target") == "node":
            if p.get("kind") not in set(kinds.values()):
                raise KernelError(f"event {eid}: unregistered node kind {p.get('kind')!r}")
        else:
            for k in ("relation", "from", "to"):
                if k not in p:
                    raise KernelError(f"event {eid}: edge payload missing {k!r}")
            if p["relation"].lower() not in preds:
                raise KernelError(f"event {eid}: unregistered relation {p['relation']!r}")


def _seq(ev):
    return ev.get("sequence", 0)


def explode(graph, stream="genesis"):
    """Decompose a graph into a genesis GraphEvent log that rebuilds it from
    empty. Folding the result onto an empty graph reproduces the input — the
    sustainability guarantee: the world model is reconstructable from its log.
    """
    occurred = graph.get("watermark", {}).get("asOf", "1970-01-01T00:00:00Z")
    events, seq = [], 0
    for target, elements in (("node", graph.get("nodes", [])),
                             ("edge", graph.get("edges", []))):
        for element in elements:
            seq += 1
            events.append({
                "id": f"af:event/genesis-{seq}",
                "kind": "GraphEvent",
                "stream": stream,
                "sequence": seq,
                "op": "upsert",
                "target": target,
                "occurredAt": occurred,
                "payload": element,
            })
    return events


class GraphKernel:
    """Overlay of a base graph and an event delta.

    The store is just a key (id) -> value map; the log is an append-only chain,
    not a tree. Upserts are keyed last-write-wins, stored as-is — the only
    "merge" is inserting a new key. The base is never mutated; the overlay is
    computed transiently on read, so there is no persisted subgraph. `until`
    bounds the overlay to events with sequence <= until."""

    def __init__(self, base, events=None, until=None, strict=True):
        self.base = base
        self.events = sorted(events or [], key=_seq)
        self.until = until
        self.strict = strict

    def _overlay(self):
        nodes = {n["id"]: dict(n) for n in self.base.get("nodes", [])}
        edges = {e["id"]: dict(e) for e in self.base.get("edges", [])}
        applied, last_seq, last_at, stream = 0, None, None, None
        for ev in self.events:
            seq = _seq(ev)
            if self.until is not None and seq > self.until:
                break
            if self.strict:
                _enforce(ev)
            store = nodes if ev["target"] == "node" else edges
            pid = ev["payload"]["id"]
            op = ev["op"]
            if op == "upsert":
                # Keyed, last-write-wins, stored as-is: an upsert inserts when the
                # key is absent and overwrites when present. The only "merge" is
                # inserting a new key — existing values are never deep-merged.
                store[pid] = dict(ev["payload"])
            elif op == "delete":
                store.pop(pid, None)
            elif op == "invalidate":
                if pid in store:
                    store[pid]["validTo"] = ev["payload"].get("validTo", ev.get("occurredAt"))
            applied += 1
            last_seq, last_at = seq, ev.get("occurredAt", last_at)
            stream = ev.get("stream", stream)
        meta = {"applied": applied, "last_seq": last_seq, "last_at": last_at, "stream": stream}
        return nodes, edges, meta

    def nodes(self):
        return list(self._overlay()[0].values())

    def edges(self):
        return list(self._overlay()[1].values())

    def view(self):
        """Return (graph_dict, summary) for the emulated state."""
        nodes, edges, meta = self._overlay()
        graph = {
            "@context": self.base.get(
                "@context", "https://schema.agennext.dev/agent-fabric/context.jsonld"),
            "id": self.base.get("id", "af:graph/emulated"),
            "kind": "Graph",
            "nodes": list(nodes.values()),
            "edges": list(edges.values()),
            "watermark": {"asOf": meta["last_at"] or "1970-01-01T00:00:00Z"},
        }
        if meta["last_seq"] is not None:
            graph["watermark"]["sequence"] = meta["last_seq"]
        if meta["stream"]:
            graph["watermark"]["stream"] = meta["stream"]
        if "tenant" in self.base:
            graph["tenant"] = self.base["tenant"]
        summary = {
            "events_applied": meta["applied"],
            "nodes": (len(self.base.get("nodes", [])), len(nodes)),
            "edges": (len(self.base.get("edges", [])), len(edges)),
        }
        return graph, summary
