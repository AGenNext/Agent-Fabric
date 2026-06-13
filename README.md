# Agent Fabric

Agent Fabric is the assertion-native operating model for AGenNext.

This repository defines the canonical primitives required to represent, verify, project, and reconcile governed reality across agents, services, devices, workspaces, organizations, and digital twins.

## Fabric Core

Fabric reduces governed systems to seven canonical records:

1. `Entity`
2. `Relationship`
3. `Assertion`
4. `Observation`
5. `Projection`
6. `Drift`
7. `Reconciliation`

Everything else is an extension of these records.

## Core Principle

```text
Identity establishes existence.
Relationships establish context.
Assertions establish truth.
Observations establish reality.
Projections establish visibility.
Drift establishes difference.
Reconciliation establishes order.
```

## Repository Layout

```text
specs/fabric-core-v1.md        Normative Fabric Core specification
schemas/v1/*.schema.json       JSON Schemas for canonical records
examples/v1/*.json             Valid example records
.github/workflows/validate.yml Schema validation workflow
```

## Fabric Core Conformance

A Fabric-compliant implementation MUST support:

- identity resolution
- assertion storage
- signature verification
- schema validation
- projection generation
- drift detection
- reconciliation recording

## Status

Draft v1.0.

---

## Meta-Model & Toolchain

The reference implementation of Fabric as a multi-model, real-time graph
meta-model for autonomous agents. It is
**multi-model** (one heterogeneous graph over **12 node kinds** and **22 relation
predicates**), **real-time** (the graph is the deterministic fold of an
append-only `GraphEvent` chain), and a **meta-model** (kinds, predicates, and
lifecycle states are first-class, versioned **registries**). The ecosystem
graph stays traceable, queryable, and versioned.

**Read the spec:** **[`spec/SPECIFICATION.md`](spec/SPECIFICATION.md)** is the
complete book; [`meta-model`](spec/meta-model.md) · [`dsl`](spec/dsl.md) ·
[`bql`](spec/bql.md) · [`simulation`](spec/simulation.md) ·
[`quality`](spec/quality.md) are detailed companions.
[`schema/`](schema/) holds the JSON Schema (draft 2020-12) + JSON-LD and the
registries.

### Principles

Built on a few non-negotiables — **storage + calculation, nothing else**: data
is stored as-is (raw JSON, keyed by `id`, an append-only chain), and every view
is calculated on read. No ORM, no middleware, no compute service, no event bus
(the idempotent keyed fold makes at-least-once/out-of-order delivery enough), no
materialized subgraphs, single binary, zero install.

### Lifecycle: proposal → enforce → migrate → active

Everything starts as a **proposal** (`state` defaults to `proposed`).
**Correctness is enforced**, not optional — the compiler never emits an invalid
graph and the kernel rejects bad events at ingestion. **Migration** is the gated
promotion path: `fab migrate` validates (and optionally requires a minimum
quality score), then promotes proposals to `active`.

### Quickstart

No install — pure Python standard library. One entry point, `tools/fab.py`:

```bash
# author: compile the human-writable .af model (correctness is enforced)
python tools/fab.py compile examples/research.af --validate

# query: traverse the graph (> is a hop, < is reverse)
python tools/fab.py query examples/research.graph.json "agent:orchestrator-7 > delegates_to > agent"

# ego-view: each party is the centre of its own world
python tools/fab.py query examples/research.graph.json --ego af:agent/researcher-3 --radius 2

# emulate: query the state AFTER a proposed event delta — no subgraph built
python tools/fab.py query schema/examples/graph.example.json "agent" \
  --events schema/examples/event-stream.example.json

# rebuild: reconstruct the whole model from its event log alone
python tools/fab.py sim examples/research.graph.json --explode -o /tmp/genesis.json
echo '{"nodes":[],"edges":[]}' > /tmp/empty.json
python tools/fab.py sim /tmp/empty.json /tmp/genesis.json -o /tmp/rebuilt.json  # == research.graph.json

# grade: score model quality, not just correctness
python tools/fab.py grade examples/research.graph.json

# migrate: promote proposals -> active, gated on correctness
python tools/fab.py migrate examples/research.graph.json --min-quality 60 -o active.json

# verify everything end-to-end (32/32)
python tools/fab.py test
```

### Commands

| Command | Stage | Does |
|---|---|---|
| `fab compile x.af` | author | FAL → schema-valid graph JSON (domain-namespaced, slugged) |
| `fab query g.json "Q"` | query | indexed `>`/`<` traversal; `--ego N`; `--events EV` for emulated state |
| `fab sim base ev` | emulate / rebuild | kernel overlay (no subgraph); `--at` time-travel; `--explode` genesis log |
| `fab grade g.json` | quality | weighted rubric of verifiers → 0–100 + verdict |
| `fab migrate g.json` | lifecycle | promote proposals → active, gated on correctness/quality |
| `fab vocab [--lang …]` | vocabulary | print / export the registry vocabulary |
| `fab test` | conformance | the 32-check e2e suite |

Each subcommand is also a standalone script under [`tools/`](tools/).

### Ships with its vocabulary, in every language

The [registries](schema/registry/) (types + states) are the single source of
truth; [`sdk/`](sdk/) carries generated bindings for **Python, TypeScript, Go,
and JSON**, drift-guarded by the e2e suite. Regenerate with
`fab vocab --lang …`.

### Correctness vs. quality

Validation proves a model is *correct*; `fab grade` asks whether it is *good*
(after the FrontierCode shift from correctness to quality). The valid research
model scores ~64/100 — "not ready" — flagging agents without identity/runtime,
ungoverned resources, and missing provenance. See [`spec/quality.md`](spec/quality.md).

### Layout

```
spec/     SPECIFICATION.md (the book) + meta-model, dsl, bql, simulation, quality
schema/   meta schemas · 12 node kinds · registries (types, states) · JSON-LD · examples
tools/    fab · afc · bql · sim · kernel · grade · migrate · fabriclib
sdk/      generated vocabulary: python · typescript · go · json
examples/ .af sources + compiled graphs (research, namespaced, comms)
tests/    e2e.py — 32 conformance checks
```
