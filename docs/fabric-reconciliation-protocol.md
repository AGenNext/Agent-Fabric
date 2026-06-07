# Fabric Reconciliation Protocol

Fabric Reconciliation Protocol defines how Agent-Fabric turns drift, gaps, conflicts, and incomplete observations into stable governed state.

Validation answers whether a record is structurally valid.
Authority answers who is allowed to decide.
Reconciliation answers what the accepted state is now.

## Definition

Fabric Reconciliation Protocol is the control loop that compares desired state, observed state, evidence, policy, authority, and risk, then produces the next stable fabric state.

```text
Desired State
  + Observed State
  + Evidence
  + Policy
  + Authority
  + Risk
  -> Reconciliation Decision
  -> Projected State
```

## Core rule

```text
No stable state without reconciliation.
```

## Reconciliation loop

```text
Observe
  -> Compare
  -> Detect Gap or Drift
  -> Classify
  -> Propose Repair
  -> Validate
  -> Authorize
  -> Decide
  -> Apply
  -> Project State
  -> Monitor
```

## Inputs

A reconciliation process may consume:

- desired state
- observed state
- current projected state
- fabric nodes
- fabric relationships
- contracts
- identities
- events
- traces
- proposals
- validation results
- authority records
- policy decisions
- human approvals
- runtime observations
- external system observations

## Outputs

A reconciliation process may emit:

- accepted relationship
- rejected relationship
- updated state projection
- rejected proposal
- remediation task
- escalation request
- authority request
- evidence request
- contract request
- identity request
- drift record
- incident record
- audit trace

## Reconciliation record

```json
{
  "id": "reconciliation:runtime-gap:001",
  "type": "FabricReconciliation",
  "target": "proposal:gapfill:runtime:001",
  "desiredState": "state:desired:agent:onboarding-assistant",
  "observedState": "state:observed:agent:onboarding-assistant",
  "currentState": "state:fabric:agent:onboarding-assistant:v1",
  "decision": "accepted",
  "reason": "Runtime relationship is required, validated, authorized, and supported by trace evidence.",
  "risk": "high",
  "validatorResult": "validation:relationship:001",
  "authorityRecord": "authority:proposal:gapfill:runtime:001",
  "appliedChanges": [
    "rel:agent:onboarding-assistant:runsOn:runtime-default"
  ],
  "resultingState": "state:fabric:agent:onboarding-assistant:v2",
  "trace": "trace:reconciliation:001",
  "status": "completed",
  "recordedAt": "2026-06-07T00:00:00Z"
}
```

## Decision types

| Decision | Meaning |
|---|---|
| `accepted` | Proposal becomes part of projected fabric state |
| `rejected` | Proposal is denied and recorded |
| `needsEvidence` | More trace or source evidence is required |
| `needsAuthority` | Approval or authority chain is incomplete |
| `needsContract` | Contract is required before activation |
| `needsIdentity` | Identity is missing or unverifiable |
| `needsPolicy` | Policy decision is missing |
| `defer` | Decision is postponed with reason |
| `quarantine` | Node or relation is isolated from active state |
| `escalate` | Human or platform intervention required |
| `rollback` | Prior state is restored |
| `supersede` | Existing state is replaced by newer valid state |

## Drift classes

| Drift | Meaning | Typical action |
|---|---|---|
| `missingNode` | Relationship points to absent node | create proposal or reject relation |
| `missingRelationship` | Required edge is absent | gap-fill proposal |
| `missingIdentity` | Actor has no verified identity | identity request |
| `missingEvidence` | Claim has no trace | evidence request |
| `missingContract` | Governed relationship lacks contract | contract request |
| `policyDrift` | Current state violates policy | suspend, repair, or escalate |
| `runtimeDrift` | Runtime differs from desired binding | reconcile runtime edge |
| `authorityDrift` | Decision chain is stale or invalid | re-approve or revoke |
| `trustDrift` | Trust score or provenance weakened | downgrade or review |
| `schemaDrift` | Record no longer matches schema | migrate or quarantine |
| `conflictDrift` | Two valid records conflict | escalate or supersede |
| `orphanDrift` | Active node has no reachable root | attach, archive, or quarantine |

## Desired state

Desired state is the expected governed configuration.

It may come from:

- contract
- policy
- platform configuration
- workspace configuration
- tenant configuration
- operator declaration
- registry declaration
- deployment manifest

Desired state is not always correct. It must still be validated and authorized.

## Observed state

Observed state is what systems report as current reality.

It may come from:

- runtime events
- traces
- logs
- tool adapters
- identity providers
- registries
- databases
- external systems
- human observations

Observed state is not always trusted. It must carry evidence.

## Projected state

Projected state is the accepted current fabric view after reconciliation.

```text
Projected State = accepted events + valid evidence + authority + reconciliation decision
```

Projected state is versioned and replayable.

## Repair proposal

A repair proposal is a proposed change that restores fabric integrity.

```json
{
  "id": "proposal:repair:runtime-drift:001",
  "type": "RepairProposal",
  "drift": "runtimeDrift",
  "action": "UpdateRelationship",
  "target": "rel:agent:x:runsOn:runtime-old",
  "replacement": "rel:agent:x:runsOn:runtime-new",
  "confidence": 0.91,
  "risk": "high",
  "approvalRequired": true,
  "evidence": ["trace:runtime:heartbeat:123"]
}
```

## Reconciliation safety rules

1. Reconciliation must be idempotent.
2. Reconciliation must be replayable.
3. Reconciliation must not erase evidence.
4. Reconciliation must not hide rejected proposals.
5. Reconciliation must not activate invalid relationships.
6. Reconciliation must not bypass authority.
7. Reconciliation must not collapse uncertainty into fact.
8. Reconciliation must emit a trace.
9. Reconciliation must produce a versioned state projection.
10. Reconciliation must support rollback or supersession.

## Idempotency

The same reconciliation input must produce the same result unless evidence, policy, authority, or desired state changes.

```text
same input -> same decision -> same projected state
```

## Replayability

A fabric state must be reconstructable from:

```text
Events
Traces
Proposals
Validation Results
Authority Records
Reconciliations
```

If state cannot be replayed, it is not stable fabric state.

## Quarantine

Quarantine isolates unsafe or unresolved records from active fabric state.

Use quarantine when:

- identity is missing,
- evidence is missing,
- authority is disputed,
- policy conflict exists,
- contract expired,
- relationship is critical and unapproved,
- state cannot be safely projected.

Quarantined records remain visible for audit and repair.

## Rollback and supersession

Rollback restores a previously valid state.

Supersession replaces an old state with a newer valid state.

Rule:

```text
Prefer supersession for normal evolution.
Use rollback for unsafe or invalid state.
```

## Relationship to Gap Filler Agent

Gap Filler Agent proposes missing completions.

Reconciliation decides whether those completions become stable state.

```text
Gap
  -> GapFillProposal
  -> Validation
  -> Authority
  -> Reconciliation
  -> Projected State
```

## Relationship to Agent-Control

Agent-Control detects drift and drives reconciliation loops.

Agent-Fabric records the relationship and state model.

Agent-Platform holds final operational authority.

```text
Agent-Control detects drift.
Agent-Fabric models drift.
Agent-Platform authorizes reconciliation.
```

## One-line definition

Fabric Reconciliation Protocol is the governed control loop that converts drift and incomplete reality into stable, traceable, versioned fabric state.
