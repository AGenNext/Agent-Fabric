# Agent-Fabric — The Complete Specification

*The kernel-native, real-time, structured metabase for enterprise autonomous agents.*

Version 1.0.0 · Status: Draft

This document is the authoritative, self-contained specification. The companion
files ([meta-model](meta-model.md), [FAL](dsl.md), [BQL](bql.md),
[simulation](simulation.md)) are narrative introductions; where they differ,
this book governs.

---

## Contents

- [0. Overview & principles](#0-overview--principles)
- [1. Architecture](#1-architecture)
- [2. Identifiers](#2-identifiers)
- [3. Entity (node)](#3-entity-node)
- [4. Relation (edge)](#4-relation-edge)
- [5. Node kinds](#5-node-kinds)
- [6. Relation predicates](#6-relation-predicates)
- [7. The type registry](#7-the-type-registry)
- [8. Storage & the kernel](#8-storage--the-kernel)
- [9. Real-time events](#9-real-time-events)
- [10. Emulation & rebuild](#10-emulation--rebuild)
- [11. FAL — the authoring language](#11-fal--the-authoring-language)
- [12. BQL — the query language](#12-bql--the-query-language)
- [13. The toolchain](#13-the-toolchain)
- [14. Validation & conformance](#14-validation--conformance)
- [15. Appendix: file map](#15-appendix-file-map)

---

## 0. Overview & principles

Agent-Fabric is the topology and relationship layer of the AGenNext ecosystem:
one graph connecting agents, humans, teams, tools, skills, runtimes, resources,
policies, traces, identities, workspaces, and channels. It is **multi-model**
(one heterogeneous graph, many kinds), **real-time** (the graph is the fold of
an event stream), and a **meta-model** (kinds and predicates are first-class,
versioned data).

Non-negotiable principles, enforced throughout:

| Principle | Meaning |
|---|---|
| **Storage + calculation** | Data is stored as-is; every view is calculated on read. No ORM, no middleware, no compute service. |
| **Store as-is** | No tokenization, normalization, or transformation on write. |
| **Just a key** | The store is a key (`id`) → value map. |
| **A chain, not a tree** | The event log is an append-only linear chain; history is never mutated. |
| **No merge, just concat** | Upserts are keyed last-write-wins; the only "merge" is inserting a new key. |
| **No materialized subgraph** | Emulation and ego-views are computed transiently through the kernel. |
| **Single binary, zero install** | One entry point on a stock Python interpreter — no packages, no services, no GPU. |
| **Traceable, queryable, versioned** | Every element is bitemporal and provenance-bearing. |

## 1. Architecture

Three modelling layers (after the OMG meta-object pattern) plus one runtime
component:

```
 M2  meta      type registry — declares the kinds & predicates (schema of schemas)
 M1  model     Entity, Relation, Graph, GraphEvent + 12 concrete node schemas
 M0  instance  live nodes, edges, snapshots, and the append-only event chain
```

The **kernel** is the only runtime component: a pure function
`base graph + event delta → emulated state`, computed on read. Authoring writes
graphs, querying reads them, the kernel folds events over them. No server sits
between storage and calculation.

## 2. Identifiers

Every element has a stable identifier (`id`), an IRI. The canonical scheme:

```
af:<kind>/<name>                     e.g. af:agent/orchestrator-7
af:<domain>/<kind>/<name>            e.g. af:acme/agent/invoice-agent   (namespaced)
af:rel/<n>                           edge ids
af:event/<n>                         event ids
```

`af:` abbreviates the namespace `https://schema.agennext.dev/agent-fabric/ns#`
(see `schema/context.jsonld`). Any resolvable IRI/URN is acceptable; the `af:`
form is the default the tools emit. The **domain is the namespace**: when a
graph is authored under a domain, ids are prefixed `af:<domain>/…`. Names are
slugs — internal whitespace collapses to hyphens — and must match
`[A-Za-z][A-Za-z0-9._-]*` after slugging.

## 3. Entity (node)

Base meta-class for every node. Schema: `schema/meta/entity.schema.json`.
Required: `id`, `kind`. `additionalProperties` is permitted (open for forward
compatibility); concrete kinds constrain `attributes`.

| Field | Type | Semantics |
|---|---|---|
| `id` | IRI | globally unique, stable identifier |
| `kind` | enum | one of the 12 node kinds |
| `label` | string | human-readable display name |
| `description` | string | free text |
| `state` | enum | `proposed` → `active` → `degraded` → `suspended` → `retired` → `deleted` (default `active`) |
| `tags` | string[] | free-form classification (unique) |
| `attributes` | object | kind-specific key/values (constrained per kind) |
| `scope` | IRI | owning `Workspace` (workspace topology partition) |
| `tenant` | string | tenant / organization boundary |
| `version` | string | version of the definition (default `"1"`) |
| `revision` | integer ≥ 0 | monotonic transaction revision |
| `validFrom` | date-time | valid-time start (when true in the world) |
| `validTo` | date-time | valid-time end (open-ended if absent) |
| `observedAt` | date-time | real-time: last observed/refreshed |
| `createdAt` | date-time | transaction-time: first written |
| `updatedAt` | date-time | transaction-time: last written |
| `provenance` | object | `source`, `assertedBy` (IRI), `evidence` (Trace IRIs), `confidence` ∈ [0,1] |

**Bitemporality.** *Valid-time* (`validFrom`/`validTo`) models when a fact is
true in the world; *transaction-time* (`createdAt`/`updatedAt`) models when the
fabric knew it. Together they answer "what did the graph assert about X at
valid-time T, as known at transaction-time T'?". `observedAt` is the live
refresh signal.

## 4. Relation (edge)

Base meta-class for every edge. Schema: `schema/meta/relation.schema.json`.
Required: `id`, `relation`, `from`, `to`. `additionalProperties: false`.

| Field | Type | Semantics |
|---|---|---|
| `id` | IRI | unique identifier (edges are addressable → reifiable) |
| `relation` | enum | one of the 22 predicates |
| `from` | IRI | tail (subject / source vertex) |
| `to` | IRI | head (object / target vertex) |
| `directed` | boolean | default `true`; symmetric predicates set `false` |
| `weight` | number | strength / cost / frequency for ranking & algorithms |
| `attributes` | object | predicate-specific key/values |
| `state`, `scope`, `tenant`, `version`, `revision`, `validFrom`, `validTo`, `observedAt`, `createdAt`, `updatedAt`, `provenance` | — | as for Entity |

An edge can be the `to` endpoint of an `EVIDENCED_BY` relation, attaching a
`Trace` to an assertion (edge reification).

## 5. Node kinds

12 kinds. Each extends `Entity`, pins `kind` to a constant, and constrains
`attributes` (open beyond the listed keys). Schemas: `schema/nodes/*.schema.json`.

| Kind | Purpose | Attributes (enums in parentheses) |
|---|---|---|
| **Agent** | autonomous software agent | `role`, `model`, `autonomyLevel` (supervised\|semi-autonomous\|autonomous), `capabilities[]`, `status` (idle\|busy\|blocked\|offline) |
| **Human** | human participant | `role`, `email`, `timezone` |
| **Team** | group of agents/humans | `mission`, `topology` (flat\|hierarchical\|hub-and-spoke\|mesh), `size` |
| **Tool** | invocable capability | `protocol` (mcp\|http\|grpc\|function\|cli), `endpoint`, `sideEffects` (read-only\|write\|destructive), `schemaRef` |
| **Skill** | reusable competency | `category`, `inputs[]`, `outputs[]`, `maturity` (experimental\|beta\|stable\|deprecated) |
| **Runtime** | execution environment | `platform`, `region`, `capacity`, `health` (healthy\|degraded\|down) |
| **Resource** | protected asset | `resourceType`, `uri`, `sensitivity` (public\|internal\|confidential\|restricted) |
| **Policy** | governance rule (ref) | `policyType` (access\|rate-limit\|data-governance\|safety\|budget), `effect` (allow\|deny\|require-approval), `ruleRef` |
| **Trace** | execution evidence (ref) | `traceRef`, `outcome` (success\|failure\|partial\|aborted), `startedAt`, `endedAt` |
| **Identity** | credentialed principal (ref) | `principalType` (service-account\|user\|workload\|role), `issuer`, `subject` |
| **Workspace** | bounded context / partition | `environment` (dev\|staging\|prod), `purpose`, `parent` |
| **Channel** | communication channel | `medium` (chat\|event-bus\|rpc\|email\|topic), `topic`, `visibility` (private\|team\|public) |

`Trace`, `Identity`, `Policy` are **reference** nodes: a `*Ref` attribute points
at the system of record (Agent-Traces / Agent-Identity / Agent-IGA). The fabric
owns the topology, not the authoritative payload — **boundary discipline**.

The node union `schema/nodes/node.schema.json` is the discriminated `oneOf` of
all 12; a value is a valid node iff it matches exactly one kind (each pins a
distinct `kind` const), so kind-specific rules are enforced wherever a node is
expected.

## 6. Relation predicates

22 predicates. A relation is valid iff its `relation` is registered and its
`from`/`to` kinds satisfy the predicate's `domain`/`range` (empty = any).

| Predicate | Domain → Range | Card. | Flags |
|---|---|---|---|
| `MEMBER_OF` | Agent, Human → Team | M:N | |
| `OWNS` | Identity, Human, Team → Agent, Resource, Tool, Skill, Workspace | 1:N | |
| `HAS_IDENTITY` | Agent, Human → Identity | M:N | inverse of ASSUMES_IDENTITY |
| `ASSUMES_IDENTITY` | Agent → Identity | M:N | inverse of HAS_IDENTITY |
| `USES` | Agent, Skill → Tool, Skill | M:N | |
| `INVOKES` | Agent → Tool | M:N | (weighted observation) |
| `DEPENDS_ON` | Tool, Skill, Agent → Tool, Skill, Agent | M:N | transitive |
| `PROVIDES` | Tool, Runtime, Agent → Skill, Resource | 1:N | |
| `RUNS_ON` | Agent → Runtime | M:1 | inverse of DEPLOYED_IN |
| `DEPLOYED_IN` | Runtime, Agent → Workspace | M:1 | |
| `SCOPED_TO` | any → Workspace | M:1 | |
| `GOVERNED_BY` | Agent, Human, Team, Tool, Resource, Workspace → Policy | M:N | |
| `GRANTS` | Policy → Resource, Tool | M:N | |
| `ACCESSES` | Agent → Resource | M:N | |
| `TRUSTS` | Agent, Identity, Human → Agent, Identity, Human | M:N | |
| `DELEGATES_TO` | Agent, Human → Agent | M:N | |
| `COMMUNICATES_WITH` | Agent, Human, Team ↔ same | M:N | symmetric |
| `COLLABORATES_WITH` | Team ↔ Team | M:N | symmetric |
| `PARTICIPATES_IN` | Agent, Human, Team → Channel | M:N | one node, any parties |
| `PRODUCED` | Agent, Team → Trace | 1:N | |
| `EVIDENCED_BY` | any → Trace | M:N | |
| `DERIVED_FROM` | any → any | M:N | transitive |

**Scope → view mapping.** Team topology = `Team` + `MEMBER_OF`/`COLLABORATES_WITH`;
runtime topology = `RUNS_ON`/`DEPLOYED_IN`; workspace topology = `SCOPED_TO`;
tool/skill dependency = `DEPENDS_ON`/`USES`/`PROVIDES`; governance =
`GOVERNED_BY`/`GRANTS`; trust/interaction = `TRUSTS`/`COMMUNICATES_WITH`;
communication = `Channel` + `PARTICIPATES_IN`; evidence = `PRODUCED`/`EVIDENCED_BY`.

## 7. The type registry

`schema/registry/registry.json` (instance of
`schema/meta/type-registry.schema.json`) is the authoritative, versioned
declaration of what may exist:

- `nodeKinds[]`: `{ name, schema, abstract?, description? }`.
- `relationTypes[]`: `{ name, description?, domain[], range[], cardinality,
  symmetric?, transitive?, inverseOf? }`.

The tools read their entire vocabulary from this file, so meta-model, compiler,
and query engine never drift. Adding a kind or predicate here (plus, for a node,
a `nodes/<kind>.schema.json` and a union entry) extends the system; bump the
registry `version`. **Never hard-code kinds or predicates outside the registry.**

## 8. Storage & the kernel

The substrate is a **key → value store** and an **append-only chain of events**.

- **Identity is the key.** The store is `id → element`.
- **The log is a chain.** Events are totally ordered by `sequence` within a
  `stream`, linkable via `causationId`; append-only, never rewritten.
- **State is the fold:** `Graph(n) = fold(apply, base, events[0..n])`.

```
apply(store, event):
    key = event.payload.id
    s   = store[node|edge]               # selected by event.target
    if event.op == "upsert":     s[key] = event.payload      # store as-is (LWW)
    elif event.op == "delete":   s.pop(key)                  # tombstone
    elif event.op == "invalidate": s[key].validTo = event.payload.validTo or event.occurredAt
```

| `op` | Effect on the keyed store |
|---|---|
| `upsert` | set by key, stored **as-is** — insert if absent, overwrite if present (last-write-wins); no deep merge |
| `delete` | remove by key (tombstone) |
| `invalidate` | set `validTo` (close valid-time) without removing |

The fold is **deterministic**: identical base + stream prefix → identical
projection. The projection's `watermark` records the last applied `sequence`,
its `occurredAt` (as `asOf`), and the `stream`.

## 9. Real-time events

`GraphEvent` (schema `schema/meta/event.schema.json`) is the unit of change.

| Field | Type | Semantics |
|---|---|---|
| `id` | IRI | unique event id |
| `kind` | const `GraphEvent` | |
| `stream` | string | logical stream/partition |
| `sequence` | integer ≥ 0 | monotonic per stream — total order |
| `op` | enum | `upsert` \| `delete` \| `invalidate` |
| `target` | enum | `node` \| `edge` |
| `occurredAt` | date-time | valid-time (when it happened) |
| `recordedAt` | date-time | transaction-time (when ingested) |
| `source` | string | producer |
| `correlationId` | string | groups events of one logical operation |
| `causationId` | string | the event/command that caused this one (chain lineage) |
| `payload` | object | the element body |

For `op = upsert` the `payload` must be a full element (validated against the
node union for `target = node`, or `Relation` for `target = edge`); for
`delete`/`invalidate` an id-only stub suffices. A consumer holding
`watermark.sequence = n` resumes from events `> n` on the same stream —
resumable, replayable.

## 10. Emulation & rebuild

The same fold, run in memory, is a **simulator**. `GraphKernel(base, events,
until)` overlays the event delta on the base and presents emulated state on read
— **no subgraph is materialized**. `until` bounds the overlay to events with
`sequence ≤ until` (time-travel).

```
GraphKernel(base, events=None, until=None)
  .view()  -> (graph, summary)     # the emulated Graph + change counts
  .nodes() -> [node, …]            # emulated nodes
  .edges() -> [edge, …]            # emulated edges
explode(graph, stream="genesis") -> [GraphEvent, …]
```

- **`sim`** prints/saves the projection; **`bql --events`** queries the emulated
  state directly.
- **Rebuild / sustainability.** `explode(graph)` decomposes a graph into a
  genesis log (one `upsert` per element); folding it onto an empty graph
  reproduces the original **byte-identically**. Graph and log are
  interconvertible — lose the snapshot, replay the log, restore the model.

## 11. FAL — the authoring language

Indentation-style `.af` → graph JSON. Full narrative: [dsl.md](dsl.md).

```ebnf
file        = { directive | declaration } ;
directive   = "@" , key , [ ws , value ] ;            (* column 0 *)
declaration = kind , ws , name , NEWLINE , { INDENT , property } ;
property    = key , ":" , value ;
```

**Header directives:** `@id <slug>` (graph id), `@domain <ns>` (id namespace),
`@tenant <name>`, `@asOf <iso-8601>` (watermark), `@scope <workspace>`.

**Property classification** (in order): (1) if `KEY.upper()` is a registered
predicate → emit edge(s); (2) reserved entity field (derived from the entity
schema: `label`, `description`, `scope`, `tenant`, `state`, `version`, `tags`,
`validFrom`, …) → set on node, `scope` resolves a workspace name to its id,
`tags` is a comma list; (3) otherwise → `attributes`, with coercion
(`true`/`false` → bool, integer/decimal → number, else string).

**Relation values:** comma-separated targets, each `name (k=v, …)`; `weight=` →
edge `weight`, other `k=v` → edge `attributes`; symmetric predicates emit
`directed:false`. Names may contain spaces (slugged on resolve).

**Guarantees:** schema-valid output; only registered kinds/predicates;
domain/range enforced; referential integrity (every target declared); unique
names; deterministic id assignment (`af:rel/N` in order).

Example (`examples/comms.af`): one `channel ops-room` with `participates_in:
ops-room` on an agent, a human, and a team → one node connecting any parties.

## 12. BQL — the query language

Path traversal using `>` (forward) and `<` (reverse). Full narrative:
[bql.md](bql.md).

```ebnf
query    = selector , { hop } ;
hop      = ( ">" | "<" ) , predicate , ( ">" | "<" ) , selector ;
selector = ( "*" | kind | kind , ":" , name ) , { filter } ;
filter   = "[" , cond , { "," , cond } , "]" ;
cond     = key , ( "=" | "!=" ) , value ;
```

- **Selectors:** `*` (any), `agent` (by kind), `agent:orchestrator-7` (by id),
  `runtime[platform=kubernetes]` (filters; keys resolve node fields then
  attributes; values coerced, string fallback).
- **Predicates:** a registered name (lowercased) or `*` (any).
- **Evaluation:** edges are indexed once by endpoint (`from`/`to`); each hop is a
  dict lookup, never a scan. Results are the de-duplicated end nodes,
  first-discovery order.
- **Ego-view:** `--ego NODE [--radius N]` returns the center plus all nodes
  within `N` hops in any direction — each party is the centre of its own view.
- **Emulated queries:** `--events EV [--at SEQ]` runs the query through the
  kernel over the emulated state (no subgraph materialized).

## 13. The toolchain

One entry point, `tools/fab.py`, pure standard library.

| Command | Module | Role |
|---|---|---|
| `fab compile x.af [--validate] [-o out]` | `afc` | author: FAL → graph JSON |
| `fab query g.json "Q" [--ego N] [--radius R] [--events EV] [--at S] [--json]` | `bql` | query / ego / emulated query |
| `fab sim base.json ev.json [--at S] [--explode] [-o out]` | `sim` | emulate / rebuild |
| `fab test` | `tests/e2e.py` | conformance suite |

`kernel.py` is the shared overlay engine; `fabriclib.py` holds shared helpers —
registry vocabulary (`load_registry`), schema-derived reserved fields
(`reserved_fields`), scalar `coerce`, and `read_json` — all `lru_cache`d. Each
subcommand is also runnable as its own script.

## 14. Validation & conformance

**Validation modes.** `afc --validate` uses JSON Schema (draft 2020-12) with a
cross-file `$ref` registry when `jsonschema` is installed, and otherwise falls
back automatically to a built-in zero-dependency structural check (registered
kinds/predicates, required fields, edge referential integrity). The active mode
is reported.

**The five guarantees.** (1) schema-valid output; (2) registry-bound with
domain/range; (3) deterministic replay; (4) lossless graph↔log round-trip;
(5) bitemporal + provenance on every element.

**Conformance suite** (`tests/e2e.py`, run via `fab test`) asserts, end to end:

- *authoring* — `research.af` compiles to the committed graph; it validates;
  expected size; `@domain` namespacing.
- *querying* — forward hop, multi-hop with filters, reverse hop, wildcard
  predicate; ego radius 1 and radius 2.
- *emulation* — delete removes a node; upsert adds an edge; invalidate sets
  `validTo`; watermark records the last sequence; `--at` time-travel; BQL over
  emulated state.
- *rebuild* — graph rebuilds byte-identically from its genesis log; the rebuilt
  graph validates.
- *conformance* — every example graph validates.

All checks must pass (currently 21/21).

## 15. Appendix: file map

```
spec/
  SPECIFICATION.md   this book
  meta-model.md      kinds, relations, registry, bitemporal, provenance
  dsl.md             FAL grammar
  bql.md             BQL grammar + ego
  simulation.md      kernel, emulation, rebuild
schema/
  context.jsonld     JSON-LD context
  meta/              entity, relation, graph, event, type-registry schemas
  nodes/             12 node-kind schemas + the node union
  registry/          populated kind & predicate registry
  examples/          sample snapshot + event stream
tools/
  fab.py             single entry point
  afc.py             FAL compiler
  bql.py             query engine + ego
  sim.py             simulator CLI
  kernel.py          GraphKernel overlay + explode
  fabriclib.py       shared helpers
examples/            .af sources + compiled graphs (research, namespaced, comms)
tests/e2e.py         conformance suite
```
