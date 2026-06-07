# Fabric MCP Tools

Fabric MCP Tools are the governed action surface of Agent-Fabric.

Resources read.
Prompts guide.
Tools act.

## Definition

A Fabric MCP Tool is a state-aware operation exposed by the Fabric MCP Server. Tools may create messages, proposals, validations, authority requests, commitments, challenges, reconciliations, projections, queries, or notifications.

Tools must never bypass validation, authority, lifecycle, reconciliation, or traceability.

## Core rule

```text
Every state-changing tool produces a Fabric message, event, trace, and lifecycle-aware record.
```

## Canonical tool catalog

```text
fabric.create_node
fabric.create_relationship
fabric.observe
fabric.propose
fabric.validate
fabric.authorize
fabric.approve
fabric.reject
fabric.commit
fabric.challenge
fabric.reconcile
fabric.project
fabric.query
fabric.notify
fabric.explain
fabric.health
```

---

## fabric.create_node

Creates a Fabric node record in draft or proposed state.

Touches:

```text
Node
Lifecycle
Event
Trace
```

Safety gate:

```text
Identity required.
Activation still requires validation and reconciliation.
```

Input:

```json
{
  "id": "agent:onboarding-assistant",
  "nodeType": "Agent",
  "name": "Onboarding Assistant",
  "status": "proposed",
  "metadata": {}
}
```

Output:

```json
{
  "node": "agent:onboarding-assistant",
  "status": "proposed",
  "message": "msg:fabric:create-node:001"
}
```

---

## fabric.create_relationship

Creates a proposed relationship between two Fabric nodes.

Touches:

```text
Relationship
Vocabulary
Evidence
Lifecycle
```

Safety gate:

```text
Predicate must be canonical. Evidence required before activation.
```

Input:

```json
{
  "subject": "agent:onboarding-assistant",
  "predicate": "runsOn",
  "object": "runtime:default",
  "risk": "high",
  "evidence": ["trace:runtime:001"]
}
```

Output:

```json
{
  "relationship": "rel:agent:onboarding-assistant:runsOn:runtime:default",
  "status": "proposed",
  "approvalRequired": true
}
```

---

## fabric.observe

Records an observation as a Fabric event/message.

Touches:

```text
Event
Trace
ObservedState
```

Safety gate:

```text
Observation does not equal truth.
```

Input:

```json
{
  "subject": "box:factory-gateway-001",
  "eventType": "HealthHeartbeatMissed",
  "source": "participant:fabric-health-agent",
  "payload": {},
  "intent": "intent:fabric:maintain-stable-state",
  "trace": "trace:health:001"
}
```

Output:

```json
{
  "message": "msg:fabric:observe:001",
  "event": "event:health-heartbeat-missed:001",
  "status": "recorded"
}
```

---

## fabric.propose

Creates a candidate Fabric change.

Touches:

```text
GapFillProposal
RepairProposal
VocabularyGapProposal
StateChangeProposal
Lifecycle
```

Safety gate:

```text
Proposal does not activate state.
```

Input:

```json
{
  "proposalType": "GapFillProposal",
  "subject": "agent:onboarding-assistant",
  "risk": "high",
  "evidence": ["trace:runtime:001"],
  "proposedChange": {
    "predicate": "runsOn",
    "object": "runtime:default"
  }
}
```

Output:

```json
{
  "proposal": "proposal:gapfill:runtime:001",
  "status": "proposed",
  "approvalRequired": true
}
```

---

## fabric.validate

Validates a Fabric record, message, relationship, topology object, or proposed state.

Touches:

```text
ValidationReport
Schema
SHACL
Vocabulary
Topology
Temporal
Evidence
```

Safety gate:

```text
Validation produces evidence. It does not grant permission.
```

Input:

```json
{
  "target": "proposal:gapfill:runtime:001",
  "validationTypes": ["schema", "semantic", "temporal", "topology", "evidence"]
}
```

Output:

```json
{
  "validation": "validation:proposal:001",
  "valid": true,
  "issues": []
}
```

---

## fabric.authorize

Evaluates whether an actor may perform an action on a resource within scope.

Touches:

```text
AuthorityRequest
AuthorityResult
Grant
Delegation
Scope
Risk
```

Safety gate:

```text
Deny by default. Permission does not equal reconciliation.
```

Input:

```json
{
  "actor": "agent:gap-filler",
  "action": "proposeRelationship",
  "resource": "agent:onboarding-assistant",
  "scope": "domain:customer-a",
  "risk": "high",
  "validation": "validation:proposal:001"
}
```

Output:

```json
{
  "authorityResult": "authority-result:001",
  "decision": "Deny",
  "reason": "No active authority grant matched request."
}
```

---

## fabric.approve

Approves a proposal when the actor has authority.

Touches:

```text
AuthorityChain
Approval
Lifecycle
Trace
```

Safety gate:

```text
Approval must match risk, scope, authority, and time.
```

Input:

```json
{
  "target": "proposal:gapfill:runtime:001",
  "scope": "runtime-binding",
  "authorityChain": "authority:proposal:runtime:001"
}
```

Output:

```json
{
  "message": "msg:fabric:approve:001",
  "status": "approved"
}
```

---

## fabric.reject

Rejects a proposal or requested change.

Touches:

```text
Proposal
Lifecycle
Trace
```

Safety gate:

```text
Rejection requires a reason and remains auditable.
```

Input:

```json
{
  "target": "proposal:gapfill:runtime:001",
  "reason": "Runtime evidence is insufficient."
}
```

Output:

```json
{
  "message": "msg:fabric:reject:001",
  "status": "rejected"
}
```

---

## fabric.commit

Creates or accepts an operational commitment.

Touches:

```text
CommitmentRecord
Obligation
Evidence
Authority
Lifecycle
```

Safety gate:

```text
Commitments create obligations and must be traceable.
```

Input:

```json
{
  "debtor": "runtime:default",
  "creditor": "agent:onboarding-assistant",
  "scope": "runtime execution",
  "condition": "Agent is active and authorized",
  "obligations": ["execute", "emit-trace", "enforce-policy"],
  "evidence": ["trace:contract:001"]
}
```

Output:

```json
{
  "commitment": "commitment:runtime:001",
  "status": "active"
}
```

---

## fabric.challenge

Challenges a record, relationship, state, commitment, authority decision, or reconciliation.

Touches:

```text
Challenge
Lifecycle
Validation
Reconciliation
```

Safety gate:

```text
Challenge must preserve the disputed record and request revalidation or reconciliation.
```

Input:

```json
{
  "target": "rel:agent:onboarding-assistant:runsOn:runtime-default",
  "reason": "Evidence is stale.",
  "requestedAction": "revalidate"
}
```

Output:

```json
{
  "challenge": "challenge:001",
  "status": "recorded",
  "reconciliationRequired": true
}
```

---

## fabric.reconcile

Produces a reconciliation plan or outcome from desired state, observed state, validation, authority, evidence, and risk.

Touches:

```text
ReconciliationRecord
ReconciliationPlan
ReconciliationOutcome
StateTransition
```

Safety gate:

```text
No reconciliation without validation, authority result, evidence, and trace.
```

Input:

```json
{
  "target": "proposal:gapfill:runtime:001",
  "desiredState": "state:desired:agent:onboarding-assistant",
  "observedState": "state:observed:agent:onboarding-assistant",
  "currentState": "state:fabric:agent:onboarding-assistant:v1",
  "validation": "validation:proposal:001",
  "authorityResult": "authority-result:001",
  "evidence": ["trace:runtime:001"],
  "risk": "high"
}
```

Output:

```json
{
  "reconciliation": "reconciliation:runtime-gap:001",
  "decision": "Accepted",
  "requiredActions": [],
  "status": "planned"
}
```

---

## fabric.project

Projects stable Fabric state from accepted source records.

Touches:

```text
ProjectedState
StateProjectionContract
Version
Replay
```

Safety gate:

```text
Projection requires accepted reconciliation or accepted source record.
```

Input:

```json
{
  "subject": "agent:onboarding-assistant",
  "projectionContract": "projection:agent-state:v1",
  "derivedFrom": ["reconciliation:runtime-gap:001"]
}
```

Output:

```json
{
  "state": "state:fabric:agent:onboarding-assistant:v2",
  "version": 2,
  "status": "projected"
}
```

---

## fabric.query

Queries Fabric topology, records, evidence, history, authority, commitments, lifecycle, or projected state.

Touches:

```text
Resource
View
Projection
History
```

Safety gate:

```text
Readable does not mean globally visible. Query must check read authority.
```

Input:

```json
{
  "queryType": "stateAsOf",
  "target": "agent:onboarding-assistant",
  "asOf": "2026-06-07T00:10:00Z"
}
```

Output:

```json
{
  "resultType": "State",
  "results": []
}
```

---

## fabric.notify

Emits a Fabric notification.

Touches:

```text
Notification
Message
Trace
```

Safety gate:

```text
Notification must not mutate state.
```

Input:

```json
{
  "notificationType": "ReconciliationCompleted",
  "target": "reconciliation:runtime-gap:001",
  "state": "state:fabric:agent:onboarding-assistant:v2"
}
```

Output:

```json
{
  "message": "msg:fabric:notify:001",
  "status": "sent"
}
```

---

## fabric.explain

Explains state, authority, commitment, reconciliation, lifecycle, or topology.

Touches:

```text
Evidence
Trace
State
Authority
Reconciliation
```

Safety gate:

```text
Explanation must cite evidence and uncertainty.
```

Input:

```json
{
  "target": "state:fabric:agent:onboarding-assistant:v2",
  "explainType": "state"
}
```

Output:

```json
{
  "target": "state:fabric:agent:onboarding-assistant:v2",
  "summary": "State was projected from accepted reconciliation.",
  "evidence": ["trace:runtime:001"],
  "uncertainty": []
}
```

---

## fabric.health

Returns health posture for a federation, domain, cluster, box, participant, or Fabric service.

Touches:

```text
Health
Drift
Lifecycle
Ubuntu Estate
```

Safety gate:

```text
Health report is observational unless followed by a governed tool action.
```

Input:

```json
{
  "target": "cluster:customer-a:edge",
  "depth": "box"
}
```

Output:

```json
{
  "target": "cluster:customer-a:edge",
  "health": "degraded",
  "drift": ["box:factory-gateway-001"],
  "recommendedActions": ["fabric.reconcile"]
}
```

## Tool safety matrix

| Tool | Can mutate? | Requires validation? | Requires authority? | Requires reconciliation? |
|---|---:|---:|---:|---:|
| create_node | yes | yes before activation | sometimes | yes before active state |
| create_relationship | yes | yes | yes for medium+ risk | yes |
| observe | append-only | envelope validation | identity required | no |
| propose | yes | yes before approval | yes for medium+ risk | yes before state |
| validate | no | n/a | no | no |
| authorize | no | consumes validation | n/a | no |
| approve | yes | yes | yes | yes before state |
| reject | yes | no | yes | no |
| commit | yes | yes | yes | yes for active state |
| challenge | yes | no | identity required | maybe |
| reconcile | yes | yes | yes | n/a |
| project | yes | source must be accepted | yes for protected state | consumes reconciliation |
| query | no | no | read authority | no |
| notify | no | envelope validation | no | no |
| explain | no | no | read authority | no |
| health | no | no | read authority | no |

## One-line definition

Fabric MCP Tools are the governed action surface for creating, observing, validating, authorizing, committing, challenging, reconciling, projecting, querying, and explaining Agent-Fabric state.
