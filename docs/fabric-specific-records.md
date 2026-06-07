# Fabric-Specific Records

These records are the parts Agent-Fabric must define itself because existing standards do not compose them end-to-end.

Agent-Fabric reuses JSON-LD, schema.org, SKOS, PROV-O, CloudEvents, OpenTelemetry, DID, VC, JSON Schema, SHACL, OPA, OpenFGA, AuthZEN, RFC3339, Kubernetes-style reconciliation, Contract Net, and commitment-based multi-agent literature.

The Fabric-specific layer defines how those pieces become one operational model.

## Canonical Fabric-specific records

```text
GapFillProposal
AuthorityChain
ReconciliationRecord
CommitmentRecord
StateProjectionContract
VocabularyGovernance
```

## 1. GapFillProposal

A GapFillProposal is a proposed completion for missing, weak, stale, or conflicting fabric state.

It is not a fact.
It is a candidate repair.

Required fields:

```text
id
type
gapType
subject
proposedChange
confidence
risk
evidence
proposedBy
approvalRequired
status
temporal
```

Allowed statuses:

```text
proposed
validating
needsEvidence
needsAuthority
accepted
rejected
quarantined
superseded
```

Rule:

```text
Gap filler agents propose. They do not activate state.
```

## 2. AuthorityChain

An AuthorityChain records who observed, proposed, validated, reviewed, approved, reconciled, projected, and remains accountable.

Required fields:

```text
id
target
observer
proposer
validator
reviewers
approvers
reconciler
stateProjector
accountableAuthority
risk
status
trace
temporal
```

Rule:

```text
No stable change without an authority chain.
```

## 3. ReconciliationRecord

A ReconciliationRecord records the decision that turns proposal, observation, validation, authority, and evidence into projected state.

Required fields:

```text
id
target
desiredState
observedState
currentState
decision
reason
risk
validatorResult
authorityChain
appliedChanges
resultingState
trace
status
temporal
```

Rule:

```text
No stable state without reconciliation.
```

## 4. CommitmentRecord

A CommitmentRecord represents what was promised, by whom, to whom, under what conditions, by when, and with what fulfillment state.

It is grounded in commitment-based multi-agent systems but adapted for operational work.

Required fields:

```text
id
debtor
creditor
scope
condition
obligations
constraints
dueAt
status
evidence
authorityChain
temporal
```

Lifecycle:

```text
offered
accepted
active
fulfilled
violated
released
cancelled
expired
superseded
```

Rule:

```text
A contract records a commitment. A commitment is the operational promise.
```

## 5. StateProjectionContract

A StateProjectionContract defines how stable state is projected from events, traces, proposals, validations, authority chains, reconciliations, commitments, and temporal rules.

Required fields:

```text
id
projectionName
sourceStreams
projectionRules
orderingRules
conflictRules
replayRules
outputStateType
version
status
temporal
```

Rule:

```text
State is projected. It is not hand-written.
```

## 6. VocabularyGovernance

VocabularyGovernance defines how new predicates, node types, risk classes, and status values are proposed, reviewed, accepted, deprecated, or rejected.

Required fields:

```text
id
term
termType
definition
proposedBy
reason
impact
status
reviewers
approvers
supersedes
effectiveAt
temporal
```

Lifecycle:

```text
proposed
reviewing
accepted
rejected
deprecated
superseded
retired
```

Rule:

```text
If no predicate exists, emit VocabularyGapProposal instead of inventing an edge.
```

## Composition loop

```text
Intent
  -> Commitment
  -> Proposal
  -> Validation
  -> AuthorityChain
  -> ReconciliationRecord
  -> StateProjectionContract
  -> Projected State
  -> Outcome
```

## One-line definition

Fabric-specific records are the minimal operational records that compose identity, provenance, policy, authority, commitments, validation, and reconciliation into stable fabric state.
