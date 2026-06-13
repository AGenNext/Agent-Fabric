# Platform as the Agent

Agent-Fabric treats the platform itself as the accountable agent.

Individual agents are participants at the edge.
The platform is the governing agent that observes the whole fabric, coordinates graph execution, enforces kernel-native rules, and projects operational truth.

## Definition

The Platform Agent is the composite Fabric actor that coordinates humans, edge agents, tools, runtimes, boxes, Kubernetes operators, graph plans, policies, commitments, authority, reconciliation, and projected state.

```text
Platform Agent
  -> observes through edge agents and adapters
  -> plans through graph orchestration
  -> validates through the Rust Kernel
  -> authorizes through authority chains
  -> reconciles through Fabric Runtime
  -> projects stable state
  -> coordinates execution through operators
```

## Core rule

```text
The platform is the agent. Edge agents are participants.
```

This prevents every local agent from becoming an independent source of truth.

---

## Role separation

```text
Kernel
  = truth and invariants

Runtime
  = execution of kernel decisions

Graph
  = orchestration and planning

Platform Agent
  = accountable coordination

Edge Agent
  = local observation and action

Kubernetes
  = operator substrate

Ubuntu Core
  = sealed box substrate

MCP
  = interaction surface

Horizon
  = command surface

Landscape
  = fleet operations surface
```

---

## Platform Agent responsibilities

The Platform Agent owns:

```text
cross-fabric observation
intent routing
graph planning
authority-aware coordination
commitment tracking
drift classification
reconciliation scheduling
state projection requests
operator coordination
edge-agent supervision
health posture
explanation and audit trail
```

The Platform Agent must not bypass:

```text
kernel validation
kernel authority checks
kernel reconciliation
kernel projection
identity lifecycle
trace requirements
policy boundaries
human approval where required
```

---

## Edge agents vs Platform Agent

| Layer | Role |
|---|---|
| Edge Agent | sees local reality and proposes action |
| Platform Agent | coordinates the fabric and requests governed action |
| Kernel | decides validity and reconciliation truth |
| Graph | plans execution order |
| Operator | executes infrastructure changes |

Rule:

```text
Edge agent proposes. Platform agent coordinates. Kernel decides.
```

---

## Platform Agent loop

```text
Observe fabric signals
  -> classify drift
  -> build graph impact map
  -> create execution plan
  -> validate plan
  -> authorize plan
  -> reconcile plan
  -> project state
  -> dispatch approved work
  -> collect traces
  -> explain outcome
```

---

## Why platform-as-agent matters

Without platform-as-agent, the system becomes many independent agents competing for truth.

With platform-as-agent:

```text
agents become participants
platform becomes accountable coordinator
kernel remains stable truth boundary
```

This gives:

```text
one accountability model
one reconciliation model
one authority model
one projected state model
many local agents
many adapters
many execution substrates
```

---

## Platform Agent interfaces

The Platform Agent exposes:

```text
MCP tools
OpenAPI endpoints
Horizon views
Kubernetes CRDs
Landscape observations
SDK clients
```

All interfaces flow through the same kernel-native runtime boundary.

```text
MCP / OpenAPI / Horizon / K8s / Landscape
  -> Platform Agent
  -> Fabric Runtime
  -> Rust Kernel
```

---

## One-line definition

Platform-as-agent means Agent-Fabric is not a collection of rogue agents; it is one accountable platform agent coordinating many edge participants through kernel-native validation, authority, reconciliation, and projected state.
