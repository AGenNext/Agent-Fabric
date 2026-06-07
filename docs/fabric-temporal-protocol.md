# Fabric Temporal Protocol

Fabric Temporal Protocol defines how time is represented in Agent-Fabric.

Without time, Fabric can say what is related.
With time, Fabric can say when it was observed, when it became effective, when it was valid, when it was superseded, and how state can be replayed.

## Definition

Fabric Temporal Protocol is the time model for replayable operational reality.

It answers:

```text
When was it observed?
When was it recorded?
When did it become effective?
When was it valid?
When did it expire?
When was it reconciled?
When was it projected?
What did the fabric know at that time?
```

## Core rule

```text
No stable fabric state without temporal context.
```

## Temporal fields

| Field | Meaning |
|---|---|
| `observedAt` | When reality was observed by an actor or system |
| `recordedAt` | When the observation entered the fabric record |
| `effectiveAt` | When the record becomes operationally effective |
| `validFrom` | Start of the validity window |
| `validTo` | End of the validity window |
| `expiresAt` | When the record naturally expires |
| `supersededAt` | When the record was replaced by another version |
| `reconciledAt` | When reconciliation accepted or rejected the record |
| `projectedAt` | When the state projection was generated |
| `challengedAt` | When the record was challenged |
| `retiredAt` | When the record was retired from active use |

## Time types

Fabric uses different time concepts because operational systems do not observe, record, decide, and apply things at the same moment.

### Observed time

Observed time is when something happened in reality or was seen by a system.

```json
{
  "observedAt": "2026-06-07T00:00:00Z"
}
```

### Recorded time

Recorded time is when Fabric stored the record.

```json
{
  "recordedAt": "2026-06-07T00:00:03Z"
}
```

### Effective time

Effective time is when the record becomes operationally active.

```json
{
  "effectiveAt": "2026-06-07T00:05:00Z"
}
```

### Valid time

Valid time is the business or governance validity window.

```json
{
  "validFrom": "2026-06-07T00:00:00Z",
  "validTo": "2026-07-07T00:00:00Z"
}
```

### Reconciled time

Reconciled time is when the system accepted, rejected, quarantined, or superseded the record.

```json
{
  "reconciledAt": "2026-06-07T00:10:00Z"
}
```

### Projected time

Projected time is when the current fabric state view was produced.

```json
{
  "projectedAt": "2026-06-07T00:10:02Z"
}
```

## Temporal record

Every fabric record may carry a temporal block.

```json
{
  "temporal": {
    "observedAt": "2026-06-07T00:00:00Z",
    "recordedAt": "2026-06-07T00:00:03Z",
    "effectiveAt": "2026-06-07T00:05:00Z",
    "validFrom": "2026-06-07T00:00:00Z",
    "validTo": null,
    "expiresAt": null,
    "supersededAt": null,
    "reconciledAt": "2026-06-07T00:10:00Z",
    "projectedAt": "2026-06-07T00:10:02Z"
  }
}
```

## Temporal states

A record may be:

```text
future
pending
active
expired
superseded
challenged
retired
archived
```

## Temporal rules

1. `observedAt` must not be after `recordedAt` unless explicitly marked as delayed reporting.
2. `effectiveAt` must not be before approval for high or critical relationships.
3. `validFrom` must be before `validTo` when `validTo` exists.
4. `expiresAt` must not be after `validTo` when both exist.
5. `supersededAt` requires a superseding record.
6. `reconciledAt` requires a reconciliation record.
7. `projectedAt` requires a state projection.
8. Active state must be inside its validity window.
9. Expired records must not remain active unless renewed.
10. Backdated records require authority and trace evidence.

## Bitemporal model

Fabric separates what happened from when Fabric knew it.

```text
Observed Time  = when reality happened
Recorded Time  = when Fabric learned it
```

This allows Fabric to answer:

```text
What was true on June 1?
What did Fabric know on June 1?
When did Fabric learn the missing fact?
Which state projection changed after late evidence arrived?
```

## As-of queries

Fabric should support temporal questions:

```text
state as of time T
relationship active at time T
contract valid at time T
identity status at time T
proposal pending at time T
reconciliation completed before time T
trace recorded after time T
```

Example:

```text
Show all active relationships for agent:onboarding-assistant as of 2026-06-07T00:10:00Z.
```

## Temporal reconciliation

Reconciliation must respect time.

A reconciliation decision must specify:

- what evidence existed,
- when evidence was observed,
- when evidence was recorded,
- when the decision was made,
- when the decision became effective,
- what state version resulted.

## Late evidence

Late evidence is evidence observed earlier but recorded later.

Late evidence may:

- update projected state,
- supersede prior state,
- challenge a decision,
- trigger rollback,
- require audit review.

Late evidence must never silently rewrite history.

Rule:

```text
Append new evidence. Supersede projections. Do not erase history.
```

## Expiry and renewal

Contracts, identities, delegations, approvals, and trust relationships may expire.

Expiry must trigger drift detection.

```text
expiresAt reached
  -> ExpiryEvent
  -> DriftDetected
  -> ReconciliationRequired
```

Renewal is a new authority decision, not a silent extension.

## Temporal authority

Authority can also expire.

Delegated authority must include:

```text
validFrom
validTo or expiresAt
scope
revocation path
```

Rule:

```text
No permanent delegated authority by default.
```

## Versioning

Every projected state must be versioned.

```json
{
  "id": "state:fabric:agent:onboarding-assistant:v2",
  "version": 2,
  "supersedes": "state:fabric:agent:onboarding-assistant:v1",
  "projectedAt": "2026-06-07T00:10:02Z"
}
```

## Replay

A fabric state must be replayable from:

```text
Events ordered by recordedAt
Traces ordered by recordedAt
Proposals ordered by recordedAt
Validation results ordered by recordedAt
Authority records ordered by recordedAt
Reconciliations ordered by reconciledAt
State projections ordered by projectedAt
```

## One-line definition

Fabric Temporal Protocol is the time model that makes Agent-Fabric replayable, auditable, explainable, and safe to reconcile over changing reality.
