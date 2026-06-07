# Fabric Protocol Messages

Fabric Protocol Messages define how Fabric nodes communicate.

The data model defines what exists.
The semantic model defines what it means.
The message model defines how Fabric records move between humans, agents, tools, runtimes, controllers, and platforms.

## Definition

A Fabric Protocol Message is a typed, traceable, temporally scoped message exchanged between Fabric participants.

It may carry an observation, proposal, validation result, authority decision, commitment, challenge, reconciliation request, state projection, query, or notification.

## Core rule

```text
No Fabric message without identity, intent, trace, time, and type.
```

## Message envelope

All Fabric messages use the same envelope.

```json
{
  "id": "msg:fabric:observe:001",
  "type": "Observe",
  "specversion": "1.0",
  "source": "agent:gap-filler",
  "subject": "agent:onboarding-assistant",
  "time": "2026-06-07T00:00:00Z",
  "trace": "trace:message:001",
  "intent": "intent:fabric:maintain-stable-state",
  "identity": "identity:agent:gap-filler",
  "payload": {}
}
```

The envelope is intentionally compatible with CloudEvents-style fields while preserving Fabric-specific requirements.

## Required envelope fields

| Field | Meaning |
|---|---|
| `id` | Stable message identifier |
| `type` | Fabric message type |
| `specversion` | Message contract version |
| `source` | Sender node |
| `subject` | Primary target node or record |
| `time` | Message creation time |
| `trace` | Trace or correlation evidence |
| `intent` | Intent that justifies the message |
| `identity` | Identity of the sender |
| `payload` | Message-specific body |

## Message types

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

---

## 1. Observe

Observe reports something seen in reality.

```json
{
  "type": "Observe",
  "payload": {
    "event": "event:runtime-gap-detected",
    "observedState": "state:observed:agent:onboarding-assistant",
    "evidence": ["trace:runtime:heartbeat:123"]
  }
}
```

Rule:

```text
Observe emits evidence. It does not decide truth.
```

---

## 2. Propose

Propose suggests a change to Fabric.

```json
{
  "type": "Propose",
  "payload": {
    "proposal": "proposal:gapfill:runtime:001",
    "proposalType": "GapFillProposal",
    "risk": "high",
    "approvalRequired": true
  }
}
```

Rule:

```text
Propose creates candidate state, not active state.
```

---

## 3. Validate

Validate reports whether a record satisfies schema, vocabulary, reference, evidence, authority, and reachability rules.

```json
{
  "type": "Validate",
  "payload": {
    "target": "proposal:gapfill:runtime:001",
    "validationResult": "validation:proposal:001",
    "valid": false,
    "errors": ["AUTHORITY_REQUIRED"]
  }
}
```

---

## 4. Approve

Approve grants authority for a proposal or change.

```json
{
  "type": "Approve",
  "payload": {
    "target": "proposal:gapfill:runtime:001",
    "authorityChain": "authority:proposal:gapfill:runtime:001",
    "scope": "runtime-binding",
    "expiresAt": "2026-07-07T00:00:00Z"
  }
}
```

Rule:

```text
Approval must match risk and scope.
```

---

## 5. Reject

Reject denies a proposal or change.

```json
{
  "type": "Reject",
  "payload": {
    "target": "proposal:gapfill:runtime:001",
    "reason": "Insufficient authority for production runtime binding.",
    "authorityChain": "authority:proposal:gapfill:runtime:001"
  }
}
```

---

## 6. Commit

Commit records an accepted obligation between parties.

```json
{
  "type": "Commit",
  "payload": {
    "commitment": "commitment:runtime-provider:001",
    "debtor": "runtime:agent-runtime-default",
    "creditor": "agent:onboarding-assistant",
    "obligations": ["execute", "emit-trace", "enforce-policy"]
  }
}
```

Rule:

```text
Commitment represents what is owed, by whom, to whom, under which conditions.
```

---

## 7. Challenge

Challenge disputes active or proposed Fabric state.

```json
{
  "type": "Challenge",
  "payload": {
    "target": "rel:agent:onboarding-assistant:runsOn:runtime-default",
    "reason": "Runtime evidence is stale.",
    "requestedAction": "revalidate"
  }
}
```

---

## 8. Reconcile

Reconcile requests or reports a reconciliation decision.

```json
{
  "type": "Reconcile",
  "payload": {
    "target": "proposal:gapfill:runtime:001",
    "desiredState": "state:desired:agent:onboarding-assistant",
    "observedState": "state:observed:agent:onboarding-assistant",
    "reconciliationRecord": "reconciliation:runtime-gap:001"
  }
}
```

---

## 9. Project

Project publishes a state projection.

```json
{
  "type": "Project",
  "payload": {
    "projectionContract": "projection:fabric:agent-state:v1",
    "state": "state:fabric:agent:onboarding-assistant:v2",
    "version": 2,
    "derivedFrom": ["reconciliation:runtime-gap:001"]
  }
}
```

Rule:

```text
Projected state must be replayable from source records.
```

---

## 10. Query

Query asks Fabric for state, relationships, evidence, authority, or history.

```json
{
  "type": "Query",
  "payload": {
    "queryType": "stateAsOf",
    "target": "agent:onboarding-assistant",
    "asOf": "2026-06-07T00:10:00Z"
  }
}
```

---

## 11. Notify

Notify informs participants of a Fabric event or state change.

```json
{
  "type": "Notify",
  "payload": {
    "notificationType": "ReconciliationCompleted",
    "target": "reconciliation:runtime-gap:001",
    "state": "state:fabric:agent:onboarding-assistant:v2"
  }
}
```

## Message flow examples

### Gap fill flow

```text
Observe
  -> Propose
  -> Validate
  -> Approve
  -> Reconcile
  -> Project
  -> Notify
```

### Commitment flow

```text
Propose
  -> Approve
  -> Commit
  -> Reconcile
  -> Project
```

### Challenge flow

```text
Challenge
  -> Validate
  -> Reconcile
  -> Project
  -> Notify
```

## Transport neutrality

Fabric Protocol Messages are transport-neutral.

They may move over:

- HTTP
- WebSocket
- message queues
- event streams
- files
- Git commits
- inbox/outbox endpoints
- MCP tools
- A2A channels

The message contract is stable even when transport changes.

## Interop mapping

| Fabric message | Existing protocol inspiration |
|---|---|
| Observe | CloudEvents, OpenTelemetry |
| Propose | Contract Net, FIPA ACL propose |
| Validate | JSON Schema, SHACL reports |
| Approve | workflow approvals, policy decisions |
| Reject | workflow rejection, FIPA reject-proposal |
| Commit | commitment-based MAS, contracts |
| Challenge | audit disputes, governance challenge |
| Reconcile | Kubernetes controllers, GitOps |
| Project | event-sourced projections, CQRS |
| Query | graph query, state API |
| Notify | CloudEvents, ActivityPub notifications |

## One-line definition

Fabric Protocol Messages are the transport-neutral communication contracts that let Fabric participants exchange observations, proposals, commitments, authority decisions, reconciliation requests, and projected state.
