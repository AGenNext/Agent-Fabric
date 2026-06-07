# Fabric Protocol

Fabric Protocol is the canonical relationship protocol for Agent-Fabric.

It defines how agents, humans, tools, skills, runtimes, identities, policies, traces, contracts, workspaces, and events become part of one governed operational fabric.

Fabric Protocol does not replace systems.
It connects systems through typed, traceable, versioned relationships.

## Definition

Fabric Protocol is a minimal, governed protocol for representing operational reality as resolvable state.

A fabric is complete enough when every active thing can answer:

```text
What is it?
Who owns it?
What is it connected to?
What is it allowed to do?
What evidence supports it?
What state is expected?
What state is observed?
What must reconcile next?
```

## First principle

A fabric is not a graph for visualization.

A fabric is a governed state surface where every relationship can be resolved, traced, challenged, approved, and reconciled.

## Core primitives

Fabric Protocol has nine primitives.

```text
Node
Relationship
Contract
Identity
Event
Trace
Proposal
Reconciliation
State
```

These primitives are intentionally small. Everything else is composed from them.

---

## 1. Node

A Node is any addressable thing in the fabric.

Examples:

- human
- agent
- tool
- skill
- model
- runtime
- workspace
- policy
- organization
- team
- document
- decision
- contract
- service
- system
- resource

A node must have:

```json
{
  "id": "agent:onboarding-assistant",
  "type": "Agent",
  "name": "Onboarding Assistant",
  "status": "active",
  "createdAt": "2026-06-07T00:00:00Z"
}
```

Rule:

```text
No node without stable identity.
```

---

## 2. Relationship

A Relationship connects two nodes with a typed predicate.

Examples:

```text
agent:onboarding-assistant runsOn runtime:agent-runtime-default
agent:onboarding-assistant ownedBy human:operator
agent:onboarding-assistant guardedBy policy:customer-data-access
workspace:customer-success contains agent:onboarding-assistant
```

A relationship must have:

```json
{
  "id": "rel:agent:onboarding-assistant:runsOn:runtime-default",
  "subject": "agent:onboarding-assistant",
  "predicate": "runsOn",
  "object": "runtime:agent-runtime-default",
  "evidence": ["trace:run-17"],
  "status": "active"
}
```

Rule:

```text
No relationship without subject, predicate, object, evidence, and status.
```

---

## 3. Contract

A Contract defines the binding obligation between nodes.

Contracts convert loose relationships into governed relationships.

Examples:

- service contract
- policy contract
- runtime contract
- data access contract
- agent behavior contract
- payment contract
- approval contract
- tenant contract

A contract must define:

```json
{
  "id": "contract:agent:onboarding-assistant:runtime",
  "parties": [
    "agent:onboarding-assistant",
    "runtime:agent-runtime-default",
    "platform:agennext"
  ],
  "scope": "runtime execution",
  "obligations": ["trace execution", "enforce policy", "emit events"],
  "authority": "platform:agennext",
  "status": "active"
}
```

Rule:

```text
No authority without contract.
No contract without parties, scope, obligations, and authority.
```

---

## 4. Identity

Identity defines who or what a node is allowed to be in the fabric.

Identity may represent:

- person
- organization
- agent
- service
- runtime
- tool
- workspace
- issuer
- verifier
- tenant

Identity must support verification and lifecycle.

```json
{
  "id": "identity:agent:onboarding-assistant",
  "subject": "agent:onboarding-assistant",
  "issuer": "identity:org:agennext",
  "method": "did",
  "status": "verified",
  "lifecycle": "active"
}
```

Rule:

```text
No actor without identity.
No identity without issuer, subject, status, and lifecycle.
```

---

## 5. Event

An Event is an observed change in the fabric.

Events do not decide truth.
They report what happened.

Examples:

- node created
- relation proposed
- policy changed
- runtime failed
- trace emitted
- contract expired
- drift detected
- approval granted
- reconciliation completed

```json
{
  "id": "event:2026-06-07:runtime-gap-detected",
  "type": "GapDetected",
  "subject": "agent:onboarding-assistant",
  "observedAt": "2026-06-07T00:00:00Z",
  "source": "agent:gap-filler",
  "payload": {
    "missingRelationship": "runsOn"
  }
}
```

Rule:

```text
No state change without event.
```

---

## 6. Trace

A Trace is evidence of execution, decision, observation, or reconciliation.

Trace makes the fabric auditable.

```json
{
  "id": "trace:run-17",
  "subject": "agent:onboarding-assistant",
  "event": "event:2026-06-07:runtime-gap-detected",
  "source": "agent:gap-filler",
  "evidenceType": "execution",
  "hash": "sha256:example",
  "recordedAt": "2026-06-07T00:00:00Z"
}
```

Rule:

```text
No claim without trace.
```

---

## 7. Proposal

A Proposal is a suggested change to the fabric.

Proposals are not facts until reconciled.

Examples:

- add relationship
- remove relationship
- downgrade trust
- request approval
- bind contract
- suspend node
- repair state
- escalate conflict

```json
{
  "id": "proposal:gapfill:runtime:001",
  "type": "GapFillProposal",
  "subject": "agent:onboarding-assistant",
  "action": "AddRelationship",
  "proposedRelationship": {
    "subject": "agent:onboarding-assistant",
    "predicate": "runsOn",
    "object": "runtime:agent-runtime-default"
  },
  "confidence": 0.82,
  "risk": "medium",
  "approvalRequired": true,
  "status": "proposed"
}
```

Rule:

```text
No uncertain completion becomes fact directly.
```

---

## 8. Reconciliation

Reconciliation is the process that compares desired state, observed state, policy, evidence, and authority, then decides what changes.

A reconciliation may:

- accept proposal
- reject proposal
- request more evidence
- require human approval
- trigger remediation
- open incident
- update fabric state

```json
{
  "id": "reconciliation:gapfill:runtime:001",
  "proposal": "proposal:gapfill:runtime:001",
  "decision": "accepted",
  "authority": "platform:agennext",
  "approvedBy": "human:operator",
  "resultingState": "state:fabric:stable:001",
  "recordedAt": "2026-06-07T00:00:00Z"
}
```

Rule:

```text
No stable state without reconciliation.
```

---

## 9. State

State is the current projection of the fabric after reconciliation.

State is not raw event history.
State is the resolved operational view.

```json
{
  "id": "state:fabric:stable:001",
  "subject": "agent:onboarding-assistant",
  "relationships": [
    "rel:agent:onboarding-assistant:runsOn:runtime-default"
  ],
  "health": "stable",
  "version": 1,
  "derivedFrom": [
    "event:2026-06-07:runtime-gap-detected",
    "proposal:gapfill:runtime:001",
    "reconciliation:gapfill:runtime:001"
  ]
}
```

Rule:

```text
State is a projection. Evidence is the source. Reconciliation is the gate.
```

---

## Protocol loop

```text
Observe
  -> Event
  -> Trace
  -> Detect Gap or Drift
  -> Proposal
  -> Validate Schema
  -> Validate Policy
  -> Reconcile
  -> Project State
  -> Monitor
```

## Gap loop

```text
Missing relation
  -> Gap detected
  -> Evidence searched
  -> Minimal relationship proposed
  -> Authority checks
  -> Reconciliation
  -> Stable fabric state
```

## Stability rules

1. Every node has identity.
2. Every relationship has evidence.
3. Every contract has authority.
4. Every change emits an event.
5. Every claim has a trace.
6. Every uncertain completion is a proposal.
7. Every proposal is reconciled.
8. Every stable state is versioned.
9. Every version is replayable.

## Non-goals

Fabric Protocol is not:

- a workflow engine,
- a database replacement,
- a blockchain,
- a sidecar mesh,
- a proxy layer,
- a visualization graph,
- an agent runtime,
- a policy engine,
- an identity provider.

It is the relationship protocol that lets those systems become one coherent operational fabric.

## One-line definition

Fabric Protocol is the governed relationship protocol that turns partial operational reality into traceable, reconcilable, stable state.
