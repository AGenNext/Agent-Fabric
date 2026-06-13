# External Consensus Quorum Model

Some Fabric constraints are too important to be changed by a single actor, repository, agent, operator, vendor, or runtime.

For those constraints, Agent-Fabric uses an external consensus quorum model.

## Core rule

```text
Hard constraints require quorum consensus before change.
```

No one directly alters the Fabric.
No one silently changes the hard constraints.
No one bypasses the review gate.

## Scope

This model applies to foundational Fabric constraints such as:

```text
no direct Fabric alteration
human accountability gate
freeze-not-destroy emergency control
trusted artifact publishing
kernel-native truth boundary
reconciliation-before-projection
no hidden side channels
no unmanaged authority escalation
no artifact without provenance
```

## Quorum participants

A hard-constraint change proposal should be reviewed against the principles, practices, or working models of relevant external communities and standards bodies, such as:

```text
Linux Foundation
Cloud Native Computing Foundation
Kubernetes working groups / SIGs
Canonical / Ubuntu ecosystem
AutonomyX / AGenNext platform authority
Cloud Security Alliance
schema.org working group
Google Open Source community practices
```

This document does not claim endorsement, approval, membership, or formal ratification by those organizations.

It defines a desired external-review quorum model for changes that affect Fabric trust boundaries.

## Quorum meaning

Quorum means a proposed change has been reviewed for alignment with:

```text
open governance
cloud-native practice
Kubernetes operator/reconciliation principles
Ubuntu/Core operational practice
security assurance
semantic interoperability
open-source community health
platform autonomy and accountability
```

## Change path

```text
Proposal
  -> issue opened
  -> evidence attached
  -> risk classified
  -> affected hard constraints listed
  -> external consensus checklist completed
  -> maintainer review
  -> human accountability approval
  -> implementation PR
  -> CI validation
  -> release gate
  -> published decision record
```

## Consensus checklist

Every hard-constraint change must answer:

```text
Which hard constraint changes?
Why is change necessary?
What evidence supports the change?
What breaks if it is accepted?
What breaks if it is rejected?
Which external practices does it align with?
Which communities should review it?
How is compatibility preserved?
How is rollback handled?
How is human accountability preserved?
```

## Minimum quorum evidence

A proposal should include at least:

```text
public issue
written rationale
risk assessment
compatibility assessment
security assessment
implementation plan
rollback plan
maintainer review
human approval
```

For high-impact constraints, it should also include:

```text
external review notes
community discussion link
standards alignment notes
partner/provider impact notes
release notes
migration guidance
```

## Non-negotiables

```text
No direct Fabric alteration.
No hard-constraint change without issue.
No hard-constraint change without evidence.
No hard-constraint change without human accountability.
No hard-constraint change without compatibility notes.
No hard-constraint change through hidden implementation drift.
```

## One-line definition

External consensus quorum means Fabric hard constraints can change only through visible proposal, evidence, risk review, community/standards alignment, maintainer review, and accountable human approval before they become trusted Fabric truth.
