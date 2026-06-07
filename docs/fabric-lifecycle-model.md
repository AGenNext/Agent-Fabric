# Fabric Lifecycle Model

Fabric Lifecycle Model defines the universal state machine for Agent-Fabric objects.

It applies to topology objects, protocol records, participants, commitments, proposals, authority chains, reconciliations, state projections, and Fabric Boxes.

## Definition

A Fabric lifecycle is the governed transition model that controls how a Fabric object is proposed, validated, approved, activated, degraded, challenged, suspended, retired, and archived.

```text
Proposed
  -> Validating
  -> Approved
  -> Active
  -> Degraded
  -> Challenged
  -> Suspended
  -> Retired
  -> Archived
```

Not every object uses every state, but every object must use the same lifecycle vocabulary.

## Core rule

```text
No state transition without event, trace, authority, and reconciliation.
```

A lifecycle transition is not just a field update.
It is a Fabric event that must be traceable and, when required, authorized.

---

## Universal lifecycle states

| State | Meaning |
|---|---|
| `draft` | Locally created but not yet submitted to Fabric |
| `proposed` | Submitted as candidate Fabric state |
| `validating` | Under schema, semantic, policy, reference, and authority validation |
| `needsEvidence` | Cannot proceed until evidence exists |
| `needsAuthority` | Cannot proceed until authority chain is complete |
| `needsContract` | Cannot proceed until required contract or commitment exists |
| `approved` | Authorized to become active or to be reconciled |
| `active` | Participates in current projected Fabric state |
| `degraded` | Active but impaired or partially invalid |
| `challenged` | Disputed and awaiting revalidation or reconciliation |
| `quarantined` | Isolated from active state for safety |
| `suspended` | Temporarily disabled by authority or policy |
| `superseded` | Replaced by a newer accepted version |
| `retired` | Intentionally removed from active operation |
| `archived` | Preserved for history, replay, audit, or compliance |
| `rejected` | Denied before activation |
| `failed` | Transition, validation, reconciliation, or health check failed |
| `expired` | Time validity ended |
| `violated` | Commitment, policy, deadline, or authority boundary was breached |
| `fulfilled` | Commitment or objective completed successfully |

---

## Canonical transition flow

```text
draft
  -> proposed
  -> validating
  -> approved
  -> active
```

Exceptional flows:

```text
validating -> needsEvidence -> validating
validating -> needsAuthority -> validating
validating -> rejected
active -> degraded -> active
active -> challenged -> validating
active -> quarantined -> validating
active -> suspended -> active
active -> superseded -> archived
active -> retired -> archived
active -> expired -> archived
active -> violated -> challenged
```

## Transition record

Every lifecycle change must produce a transition record.

```json
{
  "id": "transition:box:factory-gateway-001:active-to-degraded",
  "target": "box:factory-gateway-001",
  "from": "active",
  "to": "degraded",
  "reason": "Health heartbeat missed deadline.",
  "event": "event:deadline-missed:001",
  "trace": "trace:health-loop:001",
  "authorityChain": "authority:box-health:001",
  "reconciliation": "reconciliation:box-health:001",
  "recordedAt": "2026-06-07T00:00:00Z"
}
```

## Lifecycle authority matrix

| Transition | Authority required |
|---|---|
| draft -> proposed | proposer identity |
| proposed -> validating | validator or kernel |
| validating -> approved | policy, human, or platform depending on risk |
| approved -> active | reconciler/platform |
| active -> degraded | system observation or health controller |
| degraded -> active | reconciliation |
| active -> challenged | any authorized challenger or policy signal |
| challenged -> active | revalidation plus reconciliation |
| active -> quarantined | policy, platform, or safety controller |
| quarantined -> active | explicit authority plus reconciliation |
| active -> suspended | accountable authority or policy |
| suspended -> active | accountable authority plus reconciliation |
| active -> retired | owner or accountable authority |
| retired -> archived | archival policy |
| active -> superseded | reconciliation with replacement record |
| active -> expired | temporal rule |
| active -> violated | evidence, deadline, policy, or commitment breach |

## Lifecycle by object type

### Federation

```text
proposed -> validating -> approved -> active -> suspended -> retired -> archived
```

Federation lifecycle changes require root authority.

### Domain

```text
proposed -> validating -> approved -> active -> degraded -> suspended -> retired -> archived
```

Domain lifecycle changes require domain authority and federation admission rules.

### Cluster

```text
proposed -> validating -> active -> degraded -> suspended -> retired -> archived
```

Cluster lifecycle changes are update and failure-domain sensitive.

### Box

```text
proposed -> validating -> active -> degraded -> quarantined -> recovered -> active
active -> retired -> archived
```

Box lifecycle is driven by Ubuntu Core health, Landscape status, snap validation sets, recovery state, and Fabric reconciliation.

### Participant

```text
proposed -> validating -> active -> degraded -> suspended -> retired -> archived
```

Participant lifecycle is driven by snap state, health, identity, capability declaration, and authority boundary.

### Proposal

```text
draft -> proposed -> validating -> needsEvidence | needsAuthority | approved | rejected
approved -> reconciled -> archived
```

Proposals do not become active state directly.

### Commitment

```text
offered -> accepted -> active -> fulfilled -> archived
active -> violated -> challenged
active -> released -> archived
active -> expired -> archived
active -> cancelled -> archived
```

Commitments track promises, obligations, fulfillment, violation, and release.

### AuthorityChain

```text
proposed -> validating -> approved -> active -> expired | challenged | retired -> archived
```

Authority chains expire unless explicitly renewed.

### ReconciliationRecord

```text
proposed -> validating -> completed -> archived
proposed -> failed -> challenged
```

Reconciliation records are append-only and replayable.

### StateProjection

```text
projected -> active -> superseded -> archived
projected -> challenged -> superseded | archived
```

State is projected, versioned, and superseded. It is not overwritten.

---

## Lifecycle events

Canonical lifecycle events:

```text
LifecycleProposed
LifecycleValidationStarted
LifecycleValidationFailed
LifecycleEvidenceRequired
LifecycleAuthorityRequired
LifecycleApproved
LifecycleActivated
LifecycleDegraded
LifecycleChallenged
LifecycleQuarantined
LifecycleSuspended
LifecycleRecovered
LifecycleSuperseded
LifecycleRetired
LifecycleArchived
LifecycleRejected
LifecycleExpired
LifecycleViolated
LifecycleFulfilled
```

## Lifecycle and time

Every lifecycle transition must record:

```text
observedAt
recordedAt
effectiveAt when applicable
validFrom when applicable
validTo when applicable
expiredAt when applicable
supersededAt when applicable
```

Rule:

```text
Lifecycle is temporal. Current status is only the latest projection.
```

## Lifecycle and reconciliation

Lifecycle changes that affect active state require reconciliation.

Examples:

```text
activate participant
quarantine box
retire cluster
supersede state
accept commitment
release authority
```

Rule:

```text
Lifecycle transition changes projected state only through reconciliation.
```

## Lifecycle and Ubuntu Core

Ubuntu Core events map into Box and Participant lifecycle events.

```text
snap installed        -> participant proposed/active
snap refresh started  -> participant validating
snap refresh failed   -> participant degraded
snap rollback applied -> participant recovered
device recovery mode  -> box degraded/quarantined
validation set mismatch -> box challenged/quarantined
```

## Lifecycle and Landscape

Landscape observations map into lifecycle drift.

```text
machine offline       -> box degraded
compliance failed     -> box challenged
update required       -> box needsReconciliation
script executed       -> operator action event
reboot required       -> box degraded or pending maintenance
```

## Lifecycle and Horizon

Horizon displays lifecycle and sends governed commands.

Allowed Horizon commands:

```text
Challenge
Approve
Reject
Suspend
Retire
RequestEvidence
RequestReconciliation
RequestRollback
RequestSupersession
```

Horizon must not mutate lifecycle state directly.

## Lifecycle safety rules

1. No active object without identity.
2. No activation without validation.
3. No high-risk activation without authority.
4. No lifecycle transition without event and trace.
5. No active state change without reconciliation.
6. No history rewrite.
7. Supersede instead of overwrite.
8. Archive instead of delete.
9. Quarantine unsafe uncertainty.
10. Expire delegated authority by default.

## One-line definition

Fabric Lifecycle Model is the universal governed state machine that makes every Fabric object traceable from proposal to activation, degradation, reconciliation, retirement, and archive.
