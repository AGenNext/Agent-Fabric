# Fabric Kernel Architecture

Fabric Kernel is the executable core of Agent-Fabric.

The protocol defines the language.
The schemas define record shape.
The ontology defines meaning.
The runtime contract defines participant behavior.
The kernel defines how Fabric actually runs.

## Definition

Fabric Kernel is the minimal runtime core that stores, validates, reconciles, projects, queries, and audits Fabric state.

It is not an agent.
It is not an application server.
It is not a workflow engine.
It is the governed state kernel for the Fabric.

## Core rule

```text
The kernel owns stable Fabric state.
Agents may observe and propose. The kernel validates, reconciles, projects, and records.
```

## Kernel responsibilities

```text
Store records
Validate records
Resolve relationships
Evaluate authority
Track commitments
Process events
Attach traces
Detect gaps and drift
Run reconciliation loops
Project stable state
Serve queries
Emit notifications
Preserve replayability
```

## Kernel modules

```text
Fabric Kernel
├── Identity Store
├── Node Store
├── Relationship Store
├── Commitment Store
├── Event Store
├── Trace Store
├── Proposal Store
├── Authority Store
├── Validation Engine
├── Policy Adapter
├── Graph Resolver
├── Drift Detector
├── Reconciliation Engine
├── Projection Engine
├── Query Engine
├── Notification Bus
└── Audit Log
```

---

## 1. Identity Store

Stores Fabric identities and lifecycle state.

Owned records:

```text
Identity
Issuer
Subject
Credential reference
Verification status
Lifecycle state
```

External grounding:

```text
DID Core
Verifiable Credentials
SCIM
OIDC/SAML
```

Rule:

```text
No actor enters active Fabric state without identity.
```

---

## 2. Node Store

Stores canonical Fabric nodes.

Owned records:

```text
Human
Agent
Tool
Skill
Runtime
Workspace
Policy
Team
Organization
Contract
Service
Resource
State
```

Rule:

```text
Every active thing must be a node.
```

---

## 3. Relationship Store

Stores typed relationships between nodes.

Owned records:

```text
subject
predicate
object
evidence
risk
authority
status
temporal lifecycle
```

Rule:

```text
No relationship without canonical predicate and evidence.
```

---

## 4. Commitment Store

Stores operational promises and obligations.

Owned records:

```text
CommitmentRecord
Offer
Acceptance
Obligation
Fulfillment
Violation
Release
Expiry
```

Rule:

```text
Contracts record commitments. Commitments define what remains owed.
```

---

## 5. Event Store

Stores immutable Fabric events.

Event sources:

```text
runtime
agent
tool
human
policy
identity
registry
controller
external system
```

Rule:

```text
Append events. Do not rewrite events.
```

---

## 6. Trace Store

Stores execution, observation, decision, and reconciliation evidence.

External grounding:

```text
OpenTelemetry
W3C PROV
Audit logs
```

Rule:

```text
No claim without trace.
```

---

## 7. Proposal Store

Stores candidate changes.

Proposal types:

```text
GapFillProposal
RepairProposal
VocabularyGapProposal
CommitmentProposal
StateChangeProposal
```

Rule:

```text
Proposal is candidate state, not active state.
```

---

## 8. Authority Store

Stores authority chains and approval state.

Owned records:

```text
observer
proposer
validator
reviewer
approver
reconciler
projector
accountable authority
```

Rule:

```text
No stable state without accountability.
```

---

## 9. Validation Engine

Runs structural and semantic checks.

Validation layers:

```text
JSON Schema
JSON-LD context
SKOS vocabulary
SHACL graph constraints
Reference checks
Evidence checks
Temporal checks
Authority checks
Cycle checks
Reachability checks
```

Rule:

```text
Invalid records cannot become active Fabric state.
```

---

## 10. Policy Adapter

Connects Fabric decisions to policy and authorization systems.

External grounding:

```text
OPA/Rego
OpenFGA
AuthZEN
XACML
```

Policy questions:

```text
Can subject perform action on object in context?
Can this relationship become active?
Can this authority approve this risk?
Can this commitment be accepted?
Can this state be projected?
```

---

## 11. Graph Resolver

Resolves relationships, paths, ownership, authority, dependency, and reachability.

Core queries:

```text
relationshipsFor(node)
reachableFrom(root)
ownersOf(node)
authorityFor(target)
commitmentsFor(node)
evidenceFor(claim)
stateAsOf(node, time)
openGaps()
activeDrift()
```

---

## 12. Drift Detector

Compares desired, observed, and projected state.

Drift classes:

```text
missingNode
missingRelationship
missingIdentity
missingEvidence
missingContract
policyDrift
runtimeDrift
authorityDrift
trustDrift
schemaDrift
conflictDrift
orphanDrift
```

Rule:

```text
Drift creates proposal or reconciliation demand. It does not silently mutate state.
```

---

## 13. Reconciliation Engine

Decides accepted state transitions.

Inputs:

```text
desired state
observed state
projected state
evidence
validation results
authority chain
policy decision
risk
commitments
```

Outputs:

```text
ReconciliationRecord
accepted change
rejected change
quarantine
rollback
supersession
state projection request
notification
```

Rule:

```text
Reconciliation must be idempotent and replayable.
```

---

## 14. Projection Engine

Builds stable Fabric state from accepted records.

Inputs:

```text
events
traces
relationships
commitments
proposals
validations
authority chains
reconciliations
projection contracts
```

Output:

```text
versioned projected state
```

Rule:

```text
State is projected. It is not hand-written.
```

---

## 15. Query Engine

Serves Fabric state and history.

Query types:

```text
current state
state as of time
relationship graph
commitment status
authority chain
evidence trail
reconciliation history
open proposals
active drift
orphan nodes
policy violations
```

---

## 16. Notification Bus

Emits Fabric messages.

Messages:

```text
Observe
Propose
Validate
Approve
Reject
Commit
Challenge
Reconcile
Project
Query
Notify
```

Transport options:

```text
HTTP
WebSocket
message queue
event stream
Git
MCP
A2A
file/inbox-outbox
```

---

## 17. Audit Log

Records all critical operations.

Must record:

```text
who
what
when
why
under which authority
with what evidence
resulting state
```

Rule:

```text
Audit log is append-only.
```

---

## Canonical kernel loop

```text
Receive Message
  -> Verify Identity
  -> Validate Envelope
  -> Store Event/Trace
  -> Validate Record
  -> Resolve Graph
  -> Evaluate Policy
  -> Check Authority
  -> Detect Gap or Drift
  -> Reconcile
  -> Project State
  -> Emit Notification
  -> Audit
```

## Real component mapping

| Kernel module | First implementation |
|---|---|
| Identity Store | SurrealDB records + DID/VC references |
| Node Store | SurrealDB tables |
| Relationship Store | SurrealDB graph relations |
| Commitment Store | SurrealDB tables + relations |
| Event Store | SurrealDB append-only event table, CloudEvents envelope |
| Trace Store | OpenTelemetry IDs + SurrealDB trace index |
| Proposal Store | SurrealDB proposal tables |
| Authority Store | SurrealDB authority_chain records |
| Validation Engine | JSON Schema + SHACL + custom rules |
| Policy Adapter | OPA/Rego + OpenFGA/AuthZEN adapter |
| Graph Resolver | SurrealQL graph queries |
| Drift Detector | SurrealQL checks + controller loop |
| Reconciliation Engine | deterministic controller service |
| Projection Engine | SurrealQL projections + versioned state records |
| Query Engine | HTTP/API + SurrealQL |
| Notification Bus | CloudEvents-compatible messages |
| Audit Log | append-only SurrealDB audit events |

## Kernel data flow

```text
Fabric Participant
  -> Fabric Message
  -> Kernel Ingress
  -> Identity Check
  -> Validation Engine
  -> Event Store
  -> Trace Store
  -> Proposal / Relationship / Commitment Store
  -> Authority Store
  -> Reconciliation Engine
  -> Projection Engine
  -> Query Engine
  -> Notification Bus
```

## Kernel boundaries

Fabric Kernel must not:

- become an agent runtime,
- execute arbitrary tool calls,
- replace identity provider,
- replace policy engine,
- replace observability stack,
- hide failed reconciliation,
- overwrite event history,
- activate invalid relationships,
- grant authority without record,
- project state without replayable evidence.

## Minimal implementation profile

The smallest useful kernel must implement:

```text
Node Store
Relationship Store
Event Store
Trace Store
Proposal Store
Authority Store
Validation Engine
Reconciliation Engine
Projection Engine
Query Engine
Audit Log
```

Optional first pass:

```text
Commitment Store
Policy Adapter
SHACL Engine
Notification Bus
DID/VC verification
```

## One-line definition

Fabric Kernel is the executable state core that validates, reconciles, projects, queries, and audits Agent-Fabric reality from identity, events, traces, relationships, commitments, authority, and time.
