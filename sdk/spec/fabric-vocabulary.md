# Fabric Vocabulary

Fabric Vocabulary is the authoritative dictionary for Agent-Fabric SDKs, MCP tools, resources, prompts, runtime contracts, and implementations.

Every SDK must use these concepts consistently.

## Core rule

```text
No SDK invents local vocabulary for canonical Fabric concepts.
```

If a term is missing, create a VocabularyGapProposal.

---

# 1. Topology Vocabulary

## Federation

The highest interoperability and trust boundary.

Contains domains.

```text
Federation -> Domain -> Cluster -> Box -> Participant
```

## Domain

The first real authority boundary.

Usually maps to a tenant, organization, site, environment, or regulated boundary.

## Cluster

A group of boxes managed together.

Usually maps to an update domain, failure domain, site group, or Landscape computer group.

## Box

A physical or virtual execution node.

Usually maps to an Ubuntu Core device, Ubuntu Server machine, or Landscape computer.

## Participant

An active Fabric actor or component.

Examples:

```text
fabric-kernel
fabric-orchestrator
agent
tool
validator
reconciler
projector
policy adapter
identity adapter
trace adapter
store adapter
human operator identity
```

---

# 2. Governance Vocabulary

## Intent

The purpose behind a Fabric action.

Answers:

```text
Why does this exist?
```

## Objective

A measurable target derived from intent.

## Constraint

A boundary that limits how an objective may be pursued.

## Commitment

An operational promise between debtor and creditor.

Answers:

```text
Who owes what to whom under which condition?
```

## Obligation

A specific duty inside a commitment.

## Authority

The accountable ability to approve, reject, reconcile, project, or govern state.

## Grant

A permission issued by an authority.

## Delegation

A scoped and time-bounded transfer of authority.

## Approval

A positive authority decision.

## Rejection

A negative authority decision with reason.

## Challenge

A dispute against a record, relationship, authority decision, commitment, reconciliation, or state.

---

# 3. Runtime Vocabulary

## Observe

Record something seen in reality.

Observation is not truth.

## Propose

Suggest a candidate change.

Proposal is not activation.

## Validate

Check structural, semantic, temporal, authority, topology, evidence, or policy validity.

Validation is evidence, not permission.

## Authorize

Check whether an actor may perform an action on a resource within scope.

Authorization is permission, not state.

## Approve

Grant authority to proceed.

## Reject

Deny a proposal or requested action.

## Commit

Create or accept an operational commitment.

## Challenge

Dispute a Fabric record or state.

## Reconcile

Decide how desired state, observed state, evidence, validation, authority, and risk produce accepted state change.

## Project

Produce versioned current state from accepted source records.

## Query

Read Fabric state, history, topology, evidence, or authority.

## Notify

Emit a Fabric notification.

---

# 4. Evidence Vocabulary

## Event

An observed change.

Events are append-only.

## Trace

Evidence of observation, execution, decision, validation, reconciliation, or projection.

## Evidence

A reference supporting a claim, proposal, relationship, decision, or state.

## Provenance

The origin and derivation path of a record or state.

## ValidationReport

A record of validation issues and pass/fail status.

## Decision

A recorded choice made by authority, policy, reconciliation, or human approval.

---

# 5. State Vocabulary

## DesiredState

The expected governed configuration.

## ObservedState

The state reported by systems, humans, tools, agents, or external sources.

## CurrentState

The latest accepted projected state.

## ProjectedState

A versioned state derived from events, traces, proposals, validations, authority chains, reconciliations, commitments, and projection contracts.

## StateProjectionContract

The contract that defines how state is projected.

## Outcome

The observed result of an intent, objective, commitment, or reconciliation.

---

# 6. Lifecycle Vocabulary

Canonical lifecycle states:

```text
draft
proposed
validating
needsEvidence
needsAuthority
needsContract
approved
active
degraded
challenged
quarantined
suspended
superseded
retired
archived
rejected
failed
expired
violated
fulfilled
```

## Draft

Created locally but not submitted to Fabric.

## Proposed

Submitted as candidate Fabric state.

## Validating

Under validation.

## NeedsEvidence

Cannot proceed until evidence exists.

## NeedsAuthority

Cannot proceed until authority exists.

## NeedsContract

Cannot proceed until contract or commitment exists.

## Approved

Authorized to proceed.

## Active

Participates in current projected Fabric state.

## Degraded

Active but impaired.

## Challenged

Disputed.

## Quarantined

Isolated from active state for safety.

## Suspended

Temporarily disabled.

## Superseded

Replaced by a newer accepted version.

## Retired

Intentionally removed from active operation.

## Archived

Preserved for audit, replay, or compliance.

## Rejected

Denied before activation.

## Failed

Transition or operation failed.

## Expired

Validity period ended.

## Violated

Commitment, policy, deadline, or authority boundary breached.

## Fulfilled

Commitment or objective completed.

---

# 7. Risk Vocabulary

```text
low
medium
high
critical
```

## Low

Informational or low-impact operation.

## Medium

Operational change affecting routing, work, or non-sensitive state.

## High

Change affecting identity, access, runtime, policy, contract, or production state.

## Critical

Change affecting money, tenant boundaries, sensitive data, legal obligations, safety, or autonomous authority.

---

# 8. Relationship Predicate Vocabulary

Canonical predicates:

```text
isA
ownedBy
operatedBy
controlledBy
governedBy
authorizedBy
uses
dependsOn
runsOn
belongsTo
contains
produces
consumes
observes
emits
tracedBy
evidencedBy
trusts
delegatesTo
reportsTo
contractsWith
boundBy
reconciles
approves
rejects
proposes
requires
satisfies
violates
conflictsWith
supersedes
derivedFrom
mirrors
represents
managedBy
participatesIn
federatesWith
```

Rule:

```text
No relationship enters active state without a canonical predicate.
```

---

# 9. Ubuntu Fabric Vocabulary

## Landscape

Fleet operations panel for Ubuntu machines and Fabric Boxes.

## Horizon

Fabric command surface for topology, drift, authority, reconciliation, and projected state.

## Ubuntu Core

Sealed execution substrate for Fabric Boxes.

## PREEMPT_RT

Real-time Linux kernel profile for bounded-latency Fabric Boxes.

## Snapcraft

Packaging compiler that turns Fabric participants into snaps.

## Snap

Packaged Fabric participant artifact.

## Assertion

Signed trust statement used by Ubuntu Core and snapd.

## ValidationSet

Approved combination of snaps.

## Channel

Release ring such as edge, beta, candidate, stable.

## FabricBox

A sealed physical or virtual execution boundary.

---

# 10. Separation Vocabulary

## Validation

Evidence.

## Authority

Permission.

## Reconciliation

Judgment.

## Projection

Reality.

Canonical separation:

```text
Validation  = Is it valid?
Authority   = Are you allowed?
Reconcile   = What should happen?
Project     = What is current state?
```

## One-line definition

Fabric Vocabulary is the controlled language that keeps SDKs, MCP tools, resources, prompts, runtime contracts, topology, Ubuntu profiles, and kernel implementations interoperable.
