# Agent Fabric

**The kernel-native, real-time, structured metabase for enterprise autonomous agents.**

Agent Fabric represents the ecosystem as one heterogeneous graph over **12 node
kinds** and **22 relation predicates**. It is:

- **Multi-model** — one graph for agents, humans, teams, tools, skills, runtimes,
  resources, policies, traces, identities, workspaces, and channels.
- **Real-time** — the graph is the deterministic fold of an append-only
  `GraphEvent` chain; idempotent keyed last-write-wins, so at-least-once /
  out-of-order delivery is enough (no event bus needed).
- **A meta-model** — kinds, predicates, and lifecycle states are first-class,
  versioned **registries**: the single source of truth the tools and SDKs read
  their vocabulary from, so nothing drifts.

The guiding principle is **storage + calculation, nothing else**: data is stored
as-is (raw JSON, keyed by `id`, an append-only chain) and every view is
calculated on read — no ORM, no middleware, no materialized subgraphs.

## How to read this book

- **[Specification](./specification.md)** — the complete normative book.
- **[Meta-Model](./meta-model.md)** — the graph, events, bitemporality, provenance.
- **[Node Kinds](./node-kinds.md)** — the 12 node kinds and 22 predicates, generated
  from the registry.
- **[FAL](./dsl.md)** — the human-writable authoring DSL.
- **[BQL](./bql.md)** — the traversal / query language.
- **[Simulation & Kernel](./simulation.md)** — emulation, time-travel, and rebuild.
- **[Quality](./quality.md)** — grading a model beyond mere correctness.

> This book is built with [mdBook](https://rust-lang.github.io/mdBook/). The
> chapters are included directly from `spec/` and the Node Kinds chapter is
> generated from `schema/registry/registry.json`, so the book never drifts from
> the source of truth. Rebuild with `mdbook build book`.
