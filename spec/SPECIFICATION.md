# Agent-Fabric — The Complete Specification

*The kernel-native, real-time, structured metabase for enterprise autonomous agents.*

Version 1.0.0 · Status: Draft · This document is the consolidated specification.
Detailed grammars live in the companion specs ([meta-model](meta-model.md),
[FAL](dsl.md), [BQL](bql.md), [simulation](simulation.md)); this book is the
authoritative whole.

---

## Contents

0. [Overview & principles](#0-overview--principles)
1. [Architecture](#1-architecture)
2. [The meta-model](#2-the-meta-model)
3. [Storage & the kernel](#3-storage--the-kernel)
4. [Real-time events](#4-real-time-events)
5. [Emulation & rebuild](#5-emulation--rebuild)
6. [Authoring — FAL](#6-authoring--fal)
7. [Querying — BQL](#7-querying--bql)
8. [The toolchain](#8-the-toolchain)
9. [Guarantees & conformance](#9-guarantees--conformance)
10. [Appendix: file map](#10-appendix-file-map)

---

## 0. Overview & principles

Agent-Fabric is the topology and relationship layer of the AGenNext ecosystem:
one graph connecting agents, humans, teams, tools, skills, runtimes, resources,
policies, traces, identities, workspaces, and channels. It is **multi-model**
(one heterogeneous graph, many kinds), **real-time** (the graph is the fold of
an event stream), and a **meta-model** (kinds and predicates are first-class,
versioned data).

The system is built on a small set of non-negotiable principles, each stated
once here and enforced throughout:

- **Storage + calculation, nothing else.** Data is stored as-is (raw JSON);
  every view is calculated on read. No ORM, no middleware, no compute service.
- **Store as-is.** No tokenization, normalization, or transformation on write.
- **Just a key.** The store is a key (`id`) → value map.
- **A chain, not a tree.** The event log is an append-only linear chain;
  history is never mutated. Corrections are new events.
- **No merge, just concat.** Upserts are keyed last-write-wins; the only "merge"
  is inserting a new key. Existing values are never deep-merged.
- **No materialized subgraph.** Emulation and ego-views are computed transiently
  through the kernel; nothing is persisted as a derived copy.
- **Single binary, zero install.** The whole toolchain is one entry point on a
  stock Python interpreter — no packages, no services, no GPU.
- **Traceable, queryable, versioned.** Every element is bitemporal and
  provenance-bearing; nothing hides in space or time.

## 1. Architecture

Three modelling layers, plus a single runtime kernel:

```
 M2  meta      type registry — declares the kinds & predicates (schema of schemas)
 M1  model     Entity, Relation, Graph, GraphEvent + 12 concrete node schemas
 M0  instance  live nodes, edges, snapshots, and the append-only event chain
```

The **kernel** is the only runtime component. It is a pure function over
storage: `base graph + event delta → emulated state`, computed on read. Authoring
(`afc`) writes graphs; querying (`bql`) reads them; the kernel (`sim`,
`bql --events`) folds events over them. There is no server in between.

## 2. The meta-model

Full detail: [meta-model.md](meta-model.md).

**Entity (node).** Every node extends `Entity`: required `id` (IRI) and `kind`;
plus `label`, `description`, `state`, kind-specific `attributes`, partitioning
(`scope`, `tenant`), bitemporal time (`validFrom`/`validTo`,
`createdAt`/`updatedAt`, real-time `observedAt`), and `provenance`
(`source`, `assertedBy`, `evidence`, `confidence`).

**Relation (edge).** Every edge extends `Relation`: `id`, `relation`
(predicate), `from`, `to`, plus `directed`, `weight`, and the same temporal and
provenance fields. Edges are addressable, so an edge can itself be the target of
an `EVIDENCED_BY` relation (reification).

**12 node kinds.** Agent, Human, Team, Tool, Skill, Runtime, Resource, Policy,
Trace, Identity, Workspace, Channel.

**22 relation predicates,** each with `domain`/`range`, `cardinality`, and
optional `symmetric`/`transitive`/`inverseOf`. Highlights: `MEMBER_OF`, `OWNS`,
`HAS_IDENTITY`/`ASSUMES_IDENTITY`, `USES`, `INVOKES`, `DEPENDS_ON`, `PROVIDES`,
`RUNS_ON`/`DEPLOYED_IN`, `SCOPED_TO`, `GOVERNED_BY`, `GRANTS`, `ACCESSES`,
`TRUSTS`, `DELEGATES_TO`, `COMMUNICATES_WITH`, `COLLABORATES_WITH`,
`PARTICIPATES_IN` (any party → Channel), `PRODUCED`, `EVIDENCED_BY`,
`DERIVED_FROM`.

**The registry** (`schema/registry/registry.json`) is the authoritative,
versioned declaration of kinds and predicates. The tools read their vocabulary
from it, so the meta-model and the languages never drift.

**Boundary discipline.** `Trace`, `Identity`, `Policy` are *reference* nodes;
authoritative data lives in Agent-Traces / Agent-Identity / Agent-IGA. The
fabric owns only the topology between them.

## 3. Storage & the kernel

The substrate is the simplest thing that works: **a key → value store and an
append-only chain of events.**

- **Identity is the key.** Each node/edge has a stable IRI `id`; the store is
  `id → element`. Ids may be namespaced by domain: `af:<domain>/<kind>/<name>`.
- **The log is a chain.** Events are totally ordered by `sequence` within a
  `stream`, linkable by `causationId`. It is append-only — never rewritten.
- **State is the fold.** `Graph(n) = fold(apply, base, events[0..n])`.

`apply` is keyed and minimal:

| `op` | Effect on the keyed store |
|---|---|
| `upsert` | set by key, stored **as-is** — insert if absent, overwrite if present (last-write-wins). No deep merge |
| `delete` | remove by key (tombstone) |
| `invalidate` | set `validTo` (close valid-time) without removing |

The fold is **deterministic**: the same base and stream prefix always yield the
same projection, whose `watermark` records the last applied `sequence`,
`occurredAt`, and `stream`.

## 4. Real-time events

Full detail: [meta-model.md §3.4](meta-model.md).

A `GraphEvent` is the unit of change: `op` (`upsert`/`delete`/`invalidate`),
`target` (`node`/`edge`), `sequence` (monotonic per stream), `occurredAt`
(valid-time) vs `recordedAt` (transaction-time), `correlationId`/`causationId`
for grouping and lineage, and the `payload`. For `upsert` the payload is the
full element (validated against its concrete kind); for `delete`/`invalidate` an
id-only stub suffices.

A consumer holding `watermark.sequence = n` resumes by requesting events `> n` on
the same stream — resumable, replayable, real-time.

## 5. Emulation & rebuild

Full detail: [simulation.md](simulation.md).

Because the graph is the fold of its log, the same fold run in memory is a
**simulator**. The `GraphKernel` overlays a proposed event delta on a base graph
and presents the emulated state on read — *no subgraph is materialized*. `sim`
prints/saves the projection; `bql --events` queries the emulated state directly;
`--at SEQ` time-travels to a point in the stream.

**Rebuild / sustainability.** `explode(graph)` decomposes a graph into a genesis
event log (one `upsert` per element); folding it onto an empty graph reproduces
the original **byte-identically**. Graph and log are interconvertible — lose the
snapshot, replay the log, get the model back.

## 6. Authoring — FAL

Full grammar: [dsl.md](dsl.md).

The Fabric Agent Language is an indentation-style `.af` format that compiles to
schema-valid graph JSON. A declaration `<kind> <name>` becomes a node; indented
`key: value` lines are relations (registered predicates → edges), reserved
entity fields, or attributes. `@domain` namespaces ids; names with spaces are
collapsed to slugs. The compiler enforces registered kinds/predicates,
domain/range, and referential integrity.

## 7. Querying — BQL

Full grammar: [bql.md](bql.md).

The Blockquote Query Language traverses the graph using `>` as the hop operator
(`<` for reverse): `agent:a > delegates_to > agent[status=busy] > runs_on >
runtime`. Selectors choose by kind, id, and attribute filters; predicates may be
`*`. Evaluation is index-driven (edges indexed by endpoint). `--ego NODE
[--radius N]` returns a party's ego-network — each party is the centre of its own
view. Queries compose with `--events` to run over the emulated state.

## 8. The toolchain

One entry point, `tools/fab.py`, pure standard library:

| Command | Module | Role |
|---|---|---|
| `fab compile x.af [--validate]` | `afc` | author: FAL → graph JSON |
| `fab query g.json "Q" [--ego N] [--events EV]` | `bql` | query / ego / emulated query |
| `fab sim base.json ev.json [--at] [--explode]` | `sim` | emulate / rebuild |
| `fab test` | `tests/e2e.py` | run the conformance suite |

`kernel.py` is the shared overlay engine; `fabriclib.py` holds shared helpers
(registry vocabulary, schema-derived reserved fields, coercion, JSON I/O).
Validation uses JSON Schema when available, with a zero-dependency built-in
fallback — no extra software required.

## 9. Guarantees & conformance

1. **Schema-valid.** Every compiled graph validates against the meta-model.
2. **Registry-bound.** Only registered kinds and predicates exist; domain/range
   enforced.
3. **Deterministic replay.** Same base + stream prefix → same projection.
4. **Lossless round-trip.** Graph → genesis log → graph is byte-identical.
5. **Bitemporal + provenance.** Every element is pinned in valid-time,
   transaction-time, and origin.

`python tools/fab.py test` runs the end-to-end suite (author → query → ego →
emulate → rebuild → validate); all checks must pass.

## 10. Appendix: file map

```
spec/
  SPECIFICATION.md   this book
  meta-model.md      kinds, relations, registry, bitemporal, provenance
  dsl.md             FAL grammar
  bql.md             BQL grammar + ego
  simulation.md      kernel, emulation, rebuild
schema/
  context.jsonld     JSON-LD context
  meta/              Entity, Relation, Graph, GraphEvent, TypeRegistry
  nodes/             12 node-kind schemas + the node union
  registry/          populated kind & predicate registry
  examples/          sample snapshot + event stream
tools/
  fab.py             single entry point
  afc.py bql.py sim.py kernel.py fabriclib.py
examples/            .af sources + compiled graphs (research, namespaced, comms)
tests/e2e.py         conformance suite
```
