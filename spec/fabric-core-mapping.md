# Fabric Core ↔ Meta-Model Crosswalk

Agent Fabric has one model, described at two altitudes:

- **[Fabric Core](../specs/fabric-core-v1.md)** is the *normative skeleton* — seven
  canonical records, six mandatory verbs, and the kernel-boundary services every
  Fabric-compliant implementation must provide.
- **The [meta-model](meta-model.md)** (12 node kinds, 22 relation predicates, the
  `GraphEvent` chain, and the `fab` toolchain) is the *concrete realization* of
  that skeleton.

They are not two competing designs: the meta-model **is** Fabric Core, specialized.
This crosswalk pins the correspondence so neither drifts from the other.

## Canonical records → meta-model

| Fabric Core record | Realized in the meta-model as |
|---|---|
| **Entity** | The 12 **node kinds** (Agent, Human, Team, Tool, Skill, Runtime, Resource, Policy, Trace, Identity, Workspace, Channel). Each kind is a typed Entity; `Identity`, `Trace`, and `Policy` are the reference-node boundary. |
| **Relationship** | The 22 **relation predicates** (edges). Each edge is a directed Relationship; edges may themselves be the subject of a Relationship (edge-level provenance). |
| **Assertion** | A `GraphEvent` with `op: upsert`, carried on the append-only chain. Everything enters as a **proposal** (`state: proposed`) — an assertion awaiting reconciliation. |
| **Observation** | The bitemporal + provenance stamps on every element (`observedAt`, `occurredAt`, `recordedAt`, `provenance`) and the `Trace` reference nodes that evidence them. |
| **Projection** | The deterministic **kernel fold** — every read is a calculated view of the base graph plus its event delta (`fab sim`, `fab query --events`). No subgraph is materialized. |
| **Drift** | What `VERIFY`/`COMPARE` surface: schema/kernel **validation errors** (correctness drift) and `fab grade` **quality findings** (readiness drift) — the gap between what was asserted and what is valid or good. |
| **Reconciliation** | `fab migrate`: the gated promotion of proposals to `active`, optionally behind a minimum quality score. |

## Mandatory verbs → toolchain

| Verb | Toolchain |
|---|---|
| **ASSERT** | Author proposals (`fab compile`) and emit `GraphEvent` upserts onto the chain. |
| **OBSERVE** | Record bitemporal/provenance stamps and `Trace` evidence on events and elements. |
| **VERIFY** | `validate_graph` (JSON Schema, with a zero-dependency built-in fallback) and the kernel rejecting bad events at ingestion (`KernelError`). |
| **PROJECT** | The kernel fold presenting emulated state on read (`fab sim`, `fab query`). |
| **COMPARE** | `fab grade` (quality rubric) and validation (correctness) — drift detection. |
| **RECONCILE** | `fab migrate` promoting proposals → active. |

## Kernel-boundary services → where they live

| Fabric Core service | Provided by |
|---|---|
| Identity Service | The `Identity` reference-node kind + the registry vocabulary. |
| Assertion Service | The append-only `GraphEvent` chain + `kernel.py`. |
| Verification Service | `validate_graph` + kernel enforcement. |
| Projection Service | The kernel fold (`kernel.py`, `fab sim`). |
| Drift Service | `fab grade`. |
| Reconciliation Service | `fab migrate`. |

"Everything else is an extension" (Fabric Core §Kernel Boundary): the node kinds,
predicates, DSL (FAL), query language (BQL), and SDKs are all extensions layered on
these records and services — they add vocabulary and ergonomics, never new
primitives.
