# Agent-Fabric Meta-Model

**The multi-model, real-time graph meta-model for autonomous agents.**

Version: 1.0.0 · Status: Draft · Owner: Agent-Fabric

---

## 1. Purpose

Agent-Fabric is the topology and relationship layer of the AGenNext ecosystem.
This document defines its **meta-model**: the model that describes the graph of
agents, humans, teams, tools, skills, runtimes, resources, policies, traces,
identities, and workspaces — and the rules by which that graph stays live,
queryable, and versioned.

Three properties give the meta-model its name:

| Property | Meaning |
|---|---|
| **Multi-model** | One heterogeneous graph carries many node kinds and many relation types. The schema is not specialized to a single entity; it is a labeled, typed property graph over the whole ecosystem. |
| **Real-time** | The graph is the left-fold of an ordered stream of change events. Snapshots carry a watermark so consumers can detect staleness and resume. |
| **Meta-model** | The node kinds and relation predicates are themselves first-class, versioned data (the *type registry*). The graph describes both the ecosystem *and* its own schema. |

---

## 2. Layered architecture

```
 ┌─────────────────────────────────────────────────────────────┐
 │  M2  Meta layer        type-registry.schema.json             │
 │      (schema of schemas)  → declares node kinds & relations  │
 ├─────────────────────────────────────────────────────────────┤
 │  M1  Model layer       entity / relation / graph / event     │
 │      (the fabric schema)  + 11 concrete node-kind schemas    │
 ├─────────────────────────────────────────────────────────────┤
 │  M0  Instance layer    actual agents, edges, snapshots,      │
 │      (live data)          and the GraphEvent stream          │
 └─────────────────────────────────────────────────────────────┘
```

- **M2 — Meta layer.** `meta/type-registry.schema.json` plus the populated
  `registry/registry.json`. This is where "what kinds and predicates may exist"
  is declared, with domain/range, cardinality, symmetry, transitivity, and
  inverses. New kinds/predicates are added here, versioned, not hard-coded.
- **M1 — Model layer.** The base meta-classes `Entity` and `Relation`, the
  `Graph` snapshot envelope, the `GraphEvent` change unit, and the eleven
  concrete node schemas that refine `Entity`.
- **M0 — Instance layer.** Live nodes and edges, materialized snapshots, and
  the append-only event stream (see `examples/`).

---

## 3. Core meta-classes (M1)

### 3.1 Entity (node)

Every node extends [`Entity`](../schema/meta/entity.schema.json). Required:
`id` (a stable IRI) and `kind` (a registered node kind). Cross-cutting fields:

- **Identity & typing** — `id`, `kind`, `label`, `description`, `tags`.
- **Classification** — `state` (`proposed → active → degraded → suspended →
  retired → deleted`), kind-specific `attributes`.
- **Partitioning** — `scope` (the owning `Workspace`), `tenant`.
- **Versioning (bitemporal)** — `version`, `revision`, valid-time
  (`validFrom`/`validTo`), transaction-time (`createdAt`/`updatedAt`), and the
  real-time `observedAt`.
- **Provenance** — `source`, `assertedBy`, `evidence` (trace IRIs),
  `confidence ∈ [0,1]`.

### 3.2 Relation (edge)

Every edge extends [`Relation`](../schema/meta/relation.schema.json). Required:
`id`, `relation` (a registered predicate), `from`, `to`. Edges carry the same
bitemporal, scoping, and provenance fields as entities, plus `directed` and
`weight`. Edges are addressable by `id`, so an edge can itself be the `to`
endpoint of an `EVIDENCED_BY` relation (edge reification — see example
`af:rel/11`).

### 3.3 Graph (snapshot)

A [`Graph`](../schema/meta/graph.schema.json) is a materialized set of `nodes`
and `edges` with a **watermark** (`asOf`, `sequence`, `stream`). The watermark
is the contract for real-time correctness: it states exactly which event the
snapshot reflects.

### 3.4 GraphEvent (change unit)

The fabric is event-sourced. A [`GraphEvent`](../schema/meta/event.schema.json)
upserts, deletes, or invalidates a single node or edge:

- `op`: `upsert` (create/update) · `delete` (tombstone) · `invalidate` (close
  valid-time without removing history).
- `sequence`: monotonic per `stream`, defining total order.
- `occurredAt` (valid-time) vs `recordedAt` (transaction-time).
- `correlationId` / `causationId` for grouping and lineage.

**Folding rule:** `Graph(n) = fold(apply, Graph₀, events[0..n])`, where `apply`
upserts by `payload.id`, tombstones on `delete`, and sets `validTo` on
`invalidate`. Replaying a stream up to sequence *n* reproduces the snapshot
whose watermark is *n* — deterministically.

---

## 4. The meta layer (M2): type registry

[`registry/registry.json`](../schema/registry/registry.json) is an instance of
[`type-registry.schema.json`](../schema/meta/type-registry.schema.json). It is
the authoritative, versioned list of what may exist in the graph.

### 4.1 Node kinds (12)

`Agent`, `Human`, `Team`, `Tool`, `Skill`, `Runtime`, `Resource`, `Policy`,
`Trace`, `Identity`, `Workspace`, `Channel`. Each entry links to the JSON Schema
that validates that kind's instances.

### 4.2 Relation types (predicates)

Each predicate declares `domain` (allowed `from` kinds), `range` (allowed `to`
kinds), `cardinality`, and optional `symmetric` / `transitive` / `inverseOf`.

| Predicate | Domain → Range | Notes |
|---|---|---|
| `MEMBER_OF` | Agent, Human → Team | team topology |
| `OWNS` | Identity, Human, Team → Agent, Resource, Tool, Skill, Workspace | ownership |
| `HAS_IDENTITY` / `ASSUMES_IDENTITY` | Agent, Human → Identity | inverses |
| `USES` | Agent, Skill → Tool, Skill | capability use |
| `INVOKES` | Agent → Tool | observed call (weighted) |
| `DEPENDS_ON` | Tool, Skill, Agent → Tool, Skill, Agent | transitive |
| `PROVIDES` | Tool, Runtime, Agent → Skill, Resource | provisioning |
| `RUNS_ON` / `DEPLOYED_IN` | Agent → Runtime → Workspace | runtime topology |
| `SCOPED_TO` | any → Workspace | workspace topology |
| `GOVERNED_BY` | subject → Policy | governance map |
| `GRANTS` | Policy → Resource, Tool | entitlement |
| `ACCESSES` | Agent → Resource | access edge |
| `TRUSTS` | Agent, Identity, Human → same | trust graph |
| `DELEGATES_TO` | Agent, Human → Agent | delegation |
| `COMMUNICATES_WITH` | Agent, Human, Team ↔ same | symmetric, any parties |
| `COLLABORATES_WITH` | Team ↔ Team | symmetric |
| `PARTICIPATES_IN` | Agent, Human, Team → Channel | one node connecting any parties |
| `PRODUCED` | Agent, Team → Trace | evidence production |
| `EVIDENCED_BY` | any → Trace | assertion ↔ evidence |
| `DERIVED_FROM` | any → any | inference lineage, transitive |

A relation instance is **valid** iff its `relation` is registered and its
`from`/`to` kinds satisfy that predicate's `domain`/`range` (empty = any).

---

## 5. How the scope maps to the model

The Agent-Fabric scope (from the project README) maps directly onto views over
this one graph:

| Scope item | Realized as |
|---|---|
| agent relationship graphs | `Agent` nodes + `DELEGATES_TO`/`COMMUNICATES_WITH`/`TRUSTS` |
| team topology | `Team` + `MEMBER_OF`/`COLLABORATES_WITH` |
| runtime topology | `Runtime` + `RUNS_ON`/`DEPLOYED_IN` |
| workspace topology | `Workspace` + `SCOPED_TO` |
| tool/skill dependency maps | `Tool`/`Skill` + `DEPENDS_ON`/`USES`/`PROVIDES` |
| policy relationship graphs | `Policy` + `GOVERNED_BY`/`GRANTS` |
| trust & interaction graphs | `TRUSTS`/`COMMUNICATES_WITH` |
| trace relationship mapping | `Trace` + `PRODUCED`/`EVIDENCED_BY` |
| organizational graph views | filtered projections by `tenant`/`scope` |
| cross-agent dependency mapping | `DEPENDS_ON` closure over `Agent` |

---

## 6. Boundary discipline

Agent-Fabric maps relationships; it is not the system of record for the things
it points at. `Trace`, `Identity`, `Policy` nodes are **references** —
authoritative data lives in Agent-Traces, Agent-Identity, and Agent-IGA
respectively (each node carries a `*Ref` attribute). The fabric's job is the
topology between them, kept traceable, queryable, and versioned.

---

## 7. Real-time & versioning guarantees

1. **Append-only.** History is never mutated; corrections are new events.
2. **Deterministic replay.** Same stream prefix → same snapshot watermark.
3. **Bitemporal queries.** "What did the graph assert about X at valid-time T,
   as known at transaction-time T'?" is answerable from `validFrom/validTo` +
   `createdAt/updatedAt`.
4. **Resumability.** A consumer holding watermark `sequence=n` resumes by
   requesting events `> n` on the same `stream`.
5. **Provenance everywhere.** Every node and edge can name its source,
   asserter, supporting traces, and confidence.

---

## 8. Files

| File | Layer | Purpose |
|---|---|---|
| `schema/context.jsonld` | — | JSON-LD context (semantic linking) |
| `schema/meta/entity.schema.json` | M1 | base node |
| `schema/meta/relation.schema.json` | M1 | base edge |
| `schema/meta/graph.schema.json` | M1 | snapshot envelope |
| `schema/meta/event.schema.json` | M1 | real-time change unit |
| `schema/meta/type-registry.schema.json` | M2 | meta-model definition |
| `schema/nodes/*.schema.json` | M1 | 11 concrete node kinds |
| `schema/registry/registry.json` | M2 | populated kind/predicate registry |
| `schema/examples/graph.example.json` | M0 | sample snapshot |
| `schema/examples/event-stream.example.json` | M0 | sample event stream |
