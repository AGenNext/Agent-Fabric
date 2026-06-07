# Platform as the Service Delivery Model

Agent-Fabric uses platform-as-agent as the service delivery model.

The customer does not buy isolated agents.
The customer consumes an accountable platform agent that delivers governed operational outcomes through participants, graph orchestration, kernel-native rules, operators, and edge execution.

## Definition

Platform-as-service-delivery means the platform is the accountable service agent that observes, plans, validates, authorizes, reconciles, executes, explains, and improves work across a governed fabric.

```text
Customer Outcome
  -> Platform Agent
  -> Fabric Kernel
  -> Fabric Runtime
  -> Graph Orchestrator
  -> Kubernetes / Ubuntu / Landscape Operators
  -> Edge Participants
  -> Delivered Service
```

## Core rule

```text
Sell the governed outcome, not the individual agent.
```

Agents are participants.
The platform is the accountable delivery model.

---

## What the customer experiences

The customer experiences:

```text
service onboarding
managed operations
continuous observation
governed automation
human approval where required
reconciled state
traceable decisions
health and compliance posture
explainable outcomes
```

The customer should not need to manage:

```text
agent sprawl
tool sprawl
policy wiring
graph complexity
runtime complexity
Kubernetes internals
Ubuntu Core internals
Snapcraft packaging
reconciliation mechanics
```

---

## Service delivery layers

```text
Service Catalog
  -> Outcome Contract
  -> Platform Agent
  -> Fabric Runtime
  -> Graph Plan
  -> Operator Execution
  -> Edge Participant Action
  -> Evidence
  -> Reconciled State
  -> Report / SLA / Invoice
```

## Service catalog

The platform exposes services, not raw agents.

Examples:

```text
Agentic Operations Management
Fabric Box Management
Kubernetes Operator Management
Ubuntu Fleet Management
Drift Detection and Reconciliation
Compliance Evidence Management
Runtime Health Management
Edge Agent Management
Authority and Approval Management
State Projection and Audit
```

Each service has:

```text
scope
outcome
SLO/SLA
risk class
authority model
commitments
approval gates
evidence requirements
reporting
pricing unit
```

---

## Outcome contract

A service must be bound to an outcome contract.

```json
{
  "service": "Drift Detection and Reconciliation",
  "customer": "domain:customer-a",
  "outcome": "Detect and reconcile runtime drift for Fabric Boxes",
  "scope": "cluster:customer-a:edge",
  "risk": "high",
  "approvalRequired": true,
  "evidenceRequired": true,
  "commitments": [
    "observe",
    "classify",
    "propose",
    "reconcile",
    "report"
  ]
}
```

Rule:

```text
No service without outcome, scope, authority, evidence, and commitment.
```

---

## Platform agent delivery loop

```text
Receive service intent
  -> bind outcome contract
  -> discover topology
  -> observe state
  -> build graph plan
  -> validate plan
  -> authorize actions
  -> execute through operators and edge participants
  -> collect traces
  -> reconcile state
  -> project service status
  -> report outcome
```

---

## Relationship to managed services

Agent-Fabric can be delivered as:

```text
self-hosted platform
managed platform
hybrid managed service
edge appliance service
compliance/audit service
operator-as-a-service
platform operations service
```

But the invariant remains:

```text
The platform agent is accountable.
The kernel governs truth.
The graph plans work.
The operator executes infrastructure.
The edge participants observe and act locally.
```

---

## Delivery roles

| Role | Responsibility |
|---|---|
| Platform Agent | accountable service delivery actor |
| Human Operator | approval, exception handling, accountability |
| Edge Participant | local observation/action |
| Graph Orchestrator | execution planning and impact analysis |
| Fabric Kernel | validation, authority, reconciliation, projection |
| Kubernetes Operator | cluster execution |
| Landscape | fleet operations |
| Horizon | command and visibility surface |
| Ubuntu Core | sealed execution box |
| Snapcraft | packaging and release channel |

---

## Pricing and packaging units

Possible service units:

```text
per Fabric Domain
per Fabric Cluster
per Fabric Box
per Fabric Participant
per managed workload
per reconciliation
per evidence trail
per compliance report
per approved automation
per managed outcome
```

Preferred model:

```text
Outcome-based service package
  + usage-based operational units
  + premium governance/compliance tier
```

---

## Customer value proposition

```text
We operate the fabric, not just deploy agents.
We deliver governed outcomes, not automation scripts.
We reconcile operational truth, not dashboard noise.
We provide accountable platform intelligence, not rogue agents.
```

---

## One-line definition

Platform-as-service-delivery means Agent-Fabric is sold and operated as an accountable platform agent that delivers governed, traceable, reconciled outcomes through kernel-native rules, graph orchestration, operators, and edge participants.
