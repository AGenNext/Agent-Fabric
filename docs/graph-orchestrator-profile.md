# Graph Orchestrator Profile

Graph is the orchestration model for Agent-Fabric.

It is not the Fabric Kernel.
It is not the source of truth.
It is the execution planner that orders participants, dependencies, commitments, policies, topology, and reconciliation steps.

## Definition

The Fabric Graph Orchestrator is a dependency-aware execution planner that turns Fabric topology, relationships, commitments, state, and drift into ordered work.

```text
Fabric Graph
  -> plan execution
  -> order dependencies
  -> route messages
  -> detect impact
  -> schedule reconciliation
  -> call Rust Fabric Runtime
  -> update projected state
```

## Core rule

```text
Graph orchestrates work. Kernel governs truth.
```

The graph may decide what should run next.
The Rust Fabric Kernel decides whether the change is valid, authorized, reconcilable, and projectable.

---

## Placement

```text
Fabric Protocol
    ↓
Rust Fabric Kernel / Runtime
    ↓
Graph Orchestrator
    ↓
Adapters
├── MCP
├── Kubernetes Operator
├── Go Orchestrator
├── Horizon
└── Landscape Adapter
```

The graph sits above adapters and below the kernel contract.

---

## What the graph owns

```text
dependency ordering
impact analysis
execution planning
participant routing
workflow graph
reconciliation scheduling
rollback path planning
failure propagation
blast-radius analysis
parallelization boundaries
```

## What the graph must not own

```text
canonical type invariants
authority truth
validation truth
commitment truth
projected state truth
lifecycle truth
policy enforcement truth
identity truth
```

---

## Graph inputs

The graph consumes projected and observed Fabric records:

```text
Nodes
Relationships
Topology
Commitments
AuthorityChains
Events
Traces
DriftRecords
ValidationReports
ReconciliationRecords
StateProjections
```

## Graph outputs

The graph produces plans, not truth.

```text
ExecutionPlan
ReconciliationPlanRequest
ImpactReport
DependencyOrder
RollbackPlan
RoutingPlan
```

These outputs are submitted to the Fabric Runtime for validation, authority, reconciliation, and projection.

---

## Canonical graph flow

```text
Observe drift
  -> load topology graph
  -> load dependency graph
  -> calculate affected nodes
  -> generate execution plan
  -> validate plan
  -> authorize plan
  -> reconcile plan
  -> project resulting state
  -> notify participants
```

---

## Graph entities

```text
GraphNode
GraphEdge
ExecutionStep
ExecutionPlan
ImpactReport
DependencyOrder
RollbackPlan
RoutingPlan
```

## Graph edge types

Use Fabric canonical predicates:

```text
dependsOn
runsOn
ownedBy
governedBy
authorizedBy
boundBy
contains
belongsTo
tracedBy
evidencedBy
reconciles
supersedes
managedBy
participatesIn
```

Rule:

```text
No hidden orchestration edge. Every graph edge must map to a Fabric predicate.
```

---

## ExecutionPlan

An ExecutionPlan is an ordered proposal for work.

```json
{
  "id": "plan:reconcile:box:factory-gateway-001",
  "type": "ExecutionPlan",
  "target": "box:factory-gateway-001",
  "reason": "Health drift detected",
  "steps": [
    {
      "id": "step:validate-box",
      "action": "fabric.validate",
      "target": "box:factory-gateway-001",
      "dependsOn": []
    },
    {
      "id": "step:authorize-reconcile",
      "action": "fabric.authorize",
      "target": "box:factory-gateway-001",
      "dependsOn": ["step:validate-box"]
    },
    {
      "id": "step:reconcile-box",
      "action": "fabric.reconcile",
      "target": "box:factory-gateway-001",
      "dependsOn": ["step:authorize-reconcile"]
    }
  ]
}
```

Rule:

```text
ExecutionPlan is proposal. Reconciliation decides whether it becomes action.
```

---

## Dependency ordering

The graph must order work so dependent objects do not activate before dependencies.

Example:

```text
Identity
  -> AuthorityGrant
  -> Participant
  -> Relationship
  -> Commitment
  -> Reconciliation
  -> Projection
```

Rule:

```text
No participant activation before identity and authority are active.
```

---

## Impact analysis

When a node changes, the graph must calculate impact.

Examples:

```text
Runtime degraded
  -> affected participants
  -> affected commitments
  -> affected state projections
  -> affected domains

Authority expired
  -> affected approvals
  -> affected reconciliations
  -> affected participants

Policy changed
  -> affected commitments
  -> affected relationships
  -> affected boxes
```

---

## Graph and Kubernetes

Kubernetes executes workloads.
The graph orders Fabric work.
The Fabric Runtime governs state.

```text
Graph Plan
  -> Kubernetes Operator Step
  -> Runtime Validate/Reconcile/Project
  -> Kubernetes Status
```

Kubernetes controller loops may use graph plans, but must not replace Fabric reconciliation.

---

## Graph and MCP

MCP tools can request graph actions:

```text
fabric.explain impact
fabric.query graph
fabric.reconcile plan
fabric.health blast-radius
```

But MCP remains an adapter.

---

## Graph and Horizon

Horizon should visualize:

```text
dependency graph
impact graph
execution plan
rollback path
active drift graph
authority graph
commitment graph
state projection graph
```

Horizon must not mutate graph truth directly. It sends commands through Fabric tools.

---

## Graph and runtime

The runtime boundary remains:

```text
GraphOrchestrator
  -> validate(plan)
  -> authorize(plan)
  -> reconcile(plan)
  -> project(state)
```

The graph never bypasses runtime.

---

## One-line definition

Graph is the Agent-Fabric orchestration brain: it orders dependencies, plans execution, analyzes impact, and routes work while the Rust Fabric Kernel remains the authority for validation, reconciliation, and projected truth.
