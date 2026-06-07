# Fabric Runtime Contract

Fabric Runtime Contract defines what every Fabric participant must implement to safely participate in Agent-Fabric.

A Fabric participant may be a human, agent, tool, runtime, workspace, controller, registry, identity service, policy service, or platform.

The Runtime Contract does not require every participant to implement every operation.
It requires every participant to declare what it can do, prove identity, emit traces, respect authority, and exchange Fabric Protocol Messages correctly.

## Definition

Fabric Runtime Contract is the participant interface for Agent-Fabric.

It answers:

```text
Who are you?
What capabilities do you expose?
What messages can you send or receive?
What authority do you require?
What evidence do you emit?
How do you validate, reconcile, and project state?
How do others query or challenge you?
```

## Core rule

```text
No participant joins the active fabric without identity, capability declaration, trace support, and authority boundary.
```

## Participant types

```text
Human
Agent
Tool
Runtime
Workspace
Controller
Registry
PolicyService
IdentityService
TraceService
Platform
```

## Required baseline

Every participant must support:

```text
identify()
describeCapabilities()
receiveMessage()
emitTrace()
reportHealth()
```

Every active operational participant should also support:

```text
query()
notify()
challenge()
```

Only authorized participants may support:

```text
approve()
reject()
commit()
reconcile()
project()
```

## Runtime interface

```text
identify()
describeCapabilities()
observe()
propose()
validate()
approve()
reject()
commit()
challenge()
reconcile()
project()
query()
notify()
emitTrace()
reportHealth()
```

---

## identify()

Returns the participant identity.

```json
{
  "participant": "agent:gap-filler",
  "type": "Agent",
  "identity": "identity:agent:gap-filler",
  "issuer": "identity:org:agennext",
  "status": "verified",
  "lifecycle": "active"
}
```

Rule:

```text
No actor without identity.
```

---

## describeCapabilities()

Returns the participant capability declaration.

```json
{
  "participant": "agent:gap-filler",
  "capabilities": [
    "observe",
    "propose",
    "query",
    "notify",
    "emitTrace",
    "reportHealth"
  ],
  "acceptedMessages": ["Observe", "Query", "Notify"],
  "emittedMessages": ["Observe", "Propose", "Notify"],
  "authorityBoundary": {
    "mayPropose": true,
    "mayApprove": false,
    "mayReconcile": false,
    "maxRiskWithoutApproval": "low"
  }
}
```

Rule:

```text
No hidden capability.
```

---

## receiveMessage()

Receives a Fabric Protocol Message.

Validation requirements:

```text
message envelope valid
sender identity valid
message type accepted
intent present
trace present
risk allowed
policy allowed
```

---

## observe()

Emits an observation about current or historical reality.

May produce:

```text
Observe message
Event
Trace
ObservedState
GapDetected
DriftDetected
```

Rule:

```text
Observation does not equal truth.
```

---

## propose()

Creates a proposal for change.

May produce:

```text
GapFillProposal
RepairProposal
VocabularyGapProposal
CommitmentProposal
StateChangeProposal
```

Rule:

```text
Proposal does not equal activation.
```

---

## validate()

Checks a record or message against Fabric validation rules.

May validate:

```text
JSON Schema
JSON-LD context
SHACL shapes
Vocabulary
References
Evidence
Authority
Temporal rules
Cycle rules
Reachability
```

---

## approve()

Grants authority for a proposal or change.

Allowed only when participant has approval authority.

Rule:

```text
Approval must match risk, scope, time, and accountability.
```

---

## reject()

Rejects a proposal or change with reason and trace.

Rule:

```text
Rejected proposals remain auditable.
```

---

## commit()

Creates or accepts a CommitmentRecord.

Rule:

```text
Commitments create obligations. Obligations require evidence and lifecycle.
```

---

## challenge()

Challenges a record, relationship, commitment, authority decision, or state projection.

May produce:

```text
Challenge message
Validation request
Reconciliation request
Quarantine request
```

---

## reconcile()

Compares desired state, observed state, evidence, validation, authority, and risk to produce a ReconciliationRecord.

Allowed only for authorized controllers or platform services.

Rule:

```text
No reconciliation without authority.
```

---

## project()

Publishes projected state according to a StateProjectionContract.

Rule:

```text
State is projected from accepted source records. It is not manually written.
```

---

## query()

Queries Fabric state, history, relationships, evidence, authority, commitments, or projections.

Common query types:

```text
stateAsOf
relationshipsFor
commitmentsFor
authorityFor
evidenceFor
traceFor
openProposals
activeDrift
reachableFrom
```

---

## notify()

Sends a notification to interested participants.

Common notifications:

```text
GapDetected
DriftDetected
ProposalCreated
ValidationFailed
ApprovalRequired
ReconciliationCompleted
StateProjected
CommitmentViolated
AuthorityExpired
```

---

## emitTrace()

Emits trace evidence for operations.

Every operation that affects Fabric must emit or reference a trace.

Rule:

```text
No claim without trace.
```

---

## reportHealth()

Reports participant health.

```json
{
  "participant": "agent:gap-filler",
  "status": "healthy",
  "lastSeenAt": "2026-06-07T00:00:00Z",
  "capabilitiesAvailable": ["observe", "propose", "query"],
  "degradedCapabilities": []
}
```

## Capability levels

| Level | Meaning |
|---|---|
| observer | Can observe and emit evidence |
| proposer | Can propose changes |
| validator | Can validate records |
| approver | Can approve or reject within scope |
| reconciler | Can reconcile accepted changes |
| projector | Can publish state projections |
| authority | Can be accountable for stable state |

## Minimum contracts by participant

| Participant | Required capabilities |
|---|---|
| Human | identify, approve/reject when authorized, challenge, query |
| Agent | identify, describeCapabilities, observe/propose/query/notify, emitTrace, reportHealth |
| Tool | identify, describeCapabilities, receiveMessage, emitTrace, reportHealth |
| Runtime | identify, observe, emitTrace, reportHealth, query |
| Controller | observe, validate, reconcile, project, notify |
| Registry | identify, query, notify, validate references |
| PolicyService | validate, approve/reject policy decisions |
| IdentityService | identify, validate identity, notify lifecycle changes |
| Platform | approve, reject, reconcile, project, query, notify |

## Runtime safety boundaries

A participant must not:

- advertise false capabilities,
- act outside its authority boundary,
- activate high-risk state without approval,
- suppress trace emission,
- rewrite history,
- skip validation,
- bypass reconciliation,
- hide failed operations,
- ignore challenges,
- retain expired delegated authority.

## Runtime registration record

```json
{
  "id": "participant:agent:gap-filler",
  "type": "FabricParticipant",
  "participantType": "Agent",
  "identity": "identity:agent:gap-filler",
  "capabilities": ["observe", "propose", "query", "notify", "emitTrace", "reportHealth"],
  "acceptedMessages": ["Observe", "Query", "Notify"],
  "emittedMessages": ["Observe", "Propose", "Notify"],
  "authorityBoundary": {
    "mayPropose": true,
    "mayApprove": false,
    "mayReconcile": false,
    "maxRiskWithoutApproval": "low"
  },
  "status": "active"
}
```

## One-line definition

Fabric Runtime Contract is the minimum participant interface that lets humans, agents, tools, runtimes, controllers, and platforms safely join, communicate, validate, reconcile, and project state inside Agent-Fabric.
