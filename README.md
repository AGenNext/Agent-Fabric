# Agent-Fabric

Agent-Fabric maps and manages the relationship graph of the AGenNext autonomous ecosystem.

## Decision

Agent-Fabric is the graph/fabric layer connecting agents, humans, teams, tools, skills, runtimes, resources, policies, traces, identities, and workspaces.

It is the ecosystem topology and relationship layer for AGenNext.

## Scope

Agent-Fabric owns:

- agent relationship graphs
- team topology
- runtime topology
- workspace topology
- tool/skill dependency maps
- policy relationship graphs
- trust and interaction graphs
- trace relationship mapping
- organizational graph views
- cross-agent dependency mapping

## Boundary

| Component | Responsibility |
|---|---|
| Agent-Fabric | Ecosystem relationship graph and topology |
| Agent-Team | Agent team definitions |
| Agent-Graph | Workflow/agent execution graph |
| Agent-Traces | Timeline and execution evidence |
| Agent-Identity | Identity and ownership relationships |
| Agent-IGA | Governance and entitlement relationships |
| Agent-Platform | Final operational authority |

## Rule

The ecosystem graph should remain traceable, queryable, and versioned.

## Meta-Model

The multi-model, real-time graph meta-model for autonomous agents is defined in:

- [`spec/meta-model.md`](spec/meta-model.md) — the specification (concepts, layers, real-time/versioning rules, relation taxonomy).
- [`schema/`](schema/) — machine-readable JSON Schema (draft 2020-12) + JSON-LD, plus the populated type registry and worked examples.

It is **multi-model** (one heterogeneous graph over 11 node kinds and 21 relation types), **real-time** (the graph is the left-fold of an ordered `GraphEvent` stream, with watermarked snapshots), and a **meta-model** (node kinds and predicates are first-class, versioned data in the type registry).
