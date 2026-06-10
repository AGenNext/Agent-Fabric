# Simulation — rehearse before real

**A model of the world you can run before committing it for real.**

Because the fabric is event-sourced, a graph is the deterministic left-fold of
an ordered `GraphEvent` stream (meta-model spec §3.4, §7). That same fold,
applied in memory, is a **simulator**: take a base snapshot and a *proposed*
change set, and project the resulting graph without touching anything live —
a storyboard before the shot. The evaluator is [`tools/sim.py`](../tools/sim.py).

Status: Draft · Version 1.0.0

---

## 1. Idea

Authoring (`afc`) builds a graph; querying (`bql`) reads it; **simulation
(`sim`) folds events onto it to preview a future or hypothetical state.** The
result is a normal `Graph`, so it can be queried with `bql`, validated, or
diffed against the base — all before any of it is made real.

```bash
# Project the outcome of an event stream onto a base graph (nothing is committed)
python tools/sim.py schema/examples/graph.example.json \
                    schema/examples/event-stream.example.json -o projected.json

# Then rehearse a query against the projection
python tools/bql.py projected.json "agent"
```

## 2. Fold semantics

Events are applied in `sequence` order. Each event targets one node or edge:

| `op` | Effect on the in-memory store |
|---|---|
| `upsert` | create the element, or merge the payload into the existing one (top-level fields replaced; `attributes` shallow-merged) |
| `delete` | remove the element (tombstone) |
| `invalidate` | set the element's `validTo` (close valid-time) without removing it |

The projection's `watermark` records the last applied `sequence`, its
`occurredAt`, and the `stream` — so it states exactly how far the rehearsal ran.

## 3. Time-travel

`--at SEQ` folds only events with `sequence <= SEQ`, reproducing the graph as of
that point in the stream. Because the fold is deterministic, the same base plus
the same stream prefix always yields the same projection.

```bash
# the graph as it would stand after sequence 44
python tools/sim.py base.json events.json --at 44 -o at-44.json
```

## 4. Guarantees & scope

- **Non-destructive.** Only an explicit `-o` writes anything; the base and
  stream are read-only.
- **Deterministic.** Same inputs → same projection (the spec's replay rule).
- **Composable.** The output is a `Graph`; pipe it into `bql`, validation, or a
  diff.

Out of scope for v1: branching/what-if trees, conflict resolution between
concurrent streams, and probabilistic ("Monte-Carlo") rollouts. The fold is the
primitive those would build on.
