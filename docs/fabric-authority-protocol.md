# Fabric Authority Protocol

Fabric Authority Protocol defines who is allowed to observe, propose, validate, approve, reject, reconcile, and project state inside Agent-Fabric.

Fabric without authority becomes an unmanaged graph.
Fabric with authority becomes a governed operational system.

## Definition

Fabric Authority Protocol is the decision and permission chain for changing fabric state.

It answers:

```text
Who observed this?
Who proposed this?
Who validated this?
Who approved this?
Who reconciled this?
Who is accountable?
```

## Core rule

```text
No fabric change becomes stable state without an authority chain.
```

## Authority chain

```text
Observer
  -> Proposer
  -> Validator
  -> Reviewer
  -> Approver
  -> Reconciler
  -> State Projector
  -> Accountable Authority
```

Each step may be performed by a different actor, but every step must be traceable.

---

## Authority roles

## 1. Observer

An Observer records something that happened or exists.

Examples:

- runtime monitor
- trace collector
- human operator
- tool adapter
- registry watcher
- policy watcher
- gap filler agent

Rule:

```text
Observers emit events. Observers do not decide truth.
```

## 2. Proposer

A Proposer suggests a change to the fabric.

Examples:

- Gap Filler Agent
- Agent-Control
- Agent-Registry
- human operator
- migration tool

Rule:

```text
Proposers create proposals. Proposers do not activate high-risk state.
```

## 3. Validator

A Validator checks whether a proposal is structurally valid.

Examples:

- Fabric Validator
- schema validator
- vocabulary validator
- reference validator
- cycle detector

Rule:

```text
Validators enforce integrity. Validators do not grant authority.
```

## 4. Reviewer

A Reviewer evaluates risk, context, and impact.

Examples:

- team owner
- security reviewer
- compliance reviewer
- runtime owner
- workspace owner
- policy agent

Rule:

```text
Reviewers may recommend. Reviewers do not always approve.
```

## 5. Approver

An Approver grants permission for a change to proceed.

Examples:

- accountable human
- policy authority
- platform authority
- tenant admin
- organization admin

Rule:

```text
Approval must match risk level.
```

## 6. Reconciler

A Reconciler applies the accepted change into fabric state.

Examples:

- Agent-Platform
- Agent-Control
- fabric controller

Rule:

```text
Reconcilers change state only after validation and authority checks pass.
```

## 7. State Projector

A State Projector produces the current stable view from accepted events and reconciliations.

Examples:

- Agent-Fabric projection service
- query engine
- state snapshotter

Rule:

```text
State is projected. It is not hand-written.
```

## 8. Accountable Authority

The Accountable Authority is the final owner of the decision.

Examples:

- platform owner
- tenant owner
- workspace owner
- organization owner
- contract owner

Rule:

```text
Every stable state must have accountability.
```

---

## Risk-to-authority matrix

| Risk | Observer | Proposer | Validator | Approval required | Reconciler |
|---|---|---|---|---|---|
| low | system or agent | system or agent | validator | optional | platform or controller |
| medium | system or agent | agent or human | validator + policy | policy or owner | platform or controller |
| high | trusted system or human | agent or human | validator + policy + identity | owner + platform | platform |
| critical | trusted system or human | human or controlled agent | validator + policy + identity + contract | human + policy + platform | platform only |

## Critical relationship examples

Critical changes include:

- granting access to sensitive data,
- crossing tenant boundaries,
- activating payment authority,
- changing identity issuer,
- changing ownership,
- production runtime binding,
- disabling policy,
- overriding reconciliation,
- creating autonomous delegation chains.

Rule:

```text
Critical changes require explicit human, policy, and platform authority.
```

---

## Authority record

Every proposal and reconciliation must carry an authority record.

```json
{
  "id": "authority:proposal:gapfill:runtime:001",
  "target": "proposal:gapfill:runtime:001",
  "observer": "agent:gap-filler",
  "proposer": "agent:gap-filler",
  "validator": "service:fabric-validator",
  "reviewers": ["team:platform-ops"],
  "approvers": ["human:operator", "policy:runtime-binding"],
  "reconciler": "platform:agennext",
  "accountableAuthority": "organization:tenant-owner",
  "risk": "high",
  "status": "approved",
  "trace": "trace:authority:001"
}
```

## Authority states

```text
observed
proposed
validated
reviewed
approved
rejected
reconciled
projected
challenged
retired
```

## Separation of duties

For high and critical changes:

```text
Proposer must not be the sole approver.
Validator must not be the accountable authority.
Reconciler must not bypass approval.
Human approval must be traceable.
Policy approval must be reproducible.
```

## Delegation

Authority may be delegated only through explicit relationships and contracts.

Required predicates:

```text
delegatesTo
boundBy
authorizedBy
governedBy
```

Delegation must include:

- scope,
- duration,
- risk limit,
- revocation path,
- accountable authority,
- trace.

Rule:

```text
Delegated authority expires unless renewed.
```

## Challenge path

Any active authority decision may be challenged when:

- evidence weakens,
- source system changes,
- identity changes,
- policy changes,
- contract expires,
- drift is detected,
- conflict is found,
- human disputes the decision.

Challenge flow:

```text
Challenge
  -> Freeze or mark challenged
  -> Gather evidence
  -> Revalidate
  -> Re-approve or reject
  -> Reconcile
  -> Project new state
```

## Relationship to Validator

Validator answers:

```text
Is this structurally valid?
```

Authority Protocol answers:

```text
Who is allowed to decide this?
```

Reconciliation answers:

```text
What is the accepted state now?
```

## One-line definition

Fabric Authority Protocol is the governed decision chain that prevents valid-looking fabric changes from becoming unauthorized reality.
