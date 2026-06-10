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

- **[`spec/SPECIFICATION.md`](spec/SPECIFICATION.md) — the complete specification** (principles, architecture, meta-model, storage/kernel, events, emulation/rebuild, languages, toolchain). Start here.
- [`spec/meta-model.md`](spec/meta-model.md) · [`spec/dsl.md`](spec/dsl.md) · [`spec/bql.md`](spec/bql.md) · [`spec/simulation.md`](spec/simulation.md) — detailed companion specs.
- [`schema/`](schema/) — machine-readable JSON Schema (draft 2020-12) + JSON-LD, plus the populated type registry and worked examples.

It is **multi-model** (one heterogeneous graph over 12 node kinds and 22 relation types), **real-time** (the graph is the left-fold of an ordered `GraphEvent` stream, with watermarked snapshots), and a **meta-model** (node kinds and predicates are first-class, versioned data in the type registry).

### Quickstart (60-second tour)

No install — pure Python standard library (a stock interpreter, no packages, no services). One entry point, `tools/fab.py`, with a subcommand per stage. Author → query → emulate → rebuild:

```bash
# 1. author: compile the human-writable .af model to a validated graph
python tools/fab.py compile examples/research.af --validate

# 2. query: traverse the graph (> is a hop, < is reverse)
python tools/fab.py query examples/research.graph.json "agent:orchestrator-7 > delegates_to > agent"

# 3. emulate: query the state AFTER a proposed event delta — no subgraph built
python tools/fab.py query schema/examples/graph.example.json "agent" \
  --events schema/examples/event-stream.example.json

# 4. rebuild: reconstruct the whole model from its event log alone
python tools/fab.py sim examples/research.graph.json --explode -o /tmp/genesis.json
echo '{"nodes":[],"edges":[]}' > /tmp/empty.json
python tools/fab.py sim /tmp/empty.json /tmp/genesis.json -o /tmp/rebuilt.json  # == research.graph.json

# verify everything end-to-end
python tools/fab.py test
```

Each subcommand is also runnable as its own script (`tools/afc.py`, `tools/bql.py`, `tools/sim.py`).

### Authoring (Fabric Agent Language)

For human-friendly authoring, [`spec/dsl.md`](spec/dsl.md) defines **FAL** — an indentation-style `.af` language that compiles to schema-valid graph JSON via [`tools/afc.py`](tools/afc.py):

```bash
python tools/afc.py examples/research.af --validate
```

### Querying (Blockquote Query Language)

[`spec/bql.md`](spec/bql.md) defines **BQL** — a path-traversal query language that uses `>` as the hop operator (`<` for reverse), evaluated by [`tools/bql.py`](tools/bql.py):

```bash
python tools/bql.py examples/research.graph.json \
  "agent:orchestrator-7 > delegates_to > agent > runs_on > runtime"
```

### Simulating (rehearse before real)

[`spec/simulation.md`](spec/simulation.md) describes **`sim`** — fold a proposed `GraphEvent` stream onto a base graph to project the outcome without committing it, via [`tools/sim.py`](tools/sim.py):

```bash
python tools/sim.py schema/examples/graph.example.json \
                    schema/examples/event-stream.example.json -o projected.json
```
