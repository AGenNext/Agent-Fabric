# Fabric Intent Protocol

Fabric Intent Protocol defines why a fabric action exists.

Without intent, Fabric can describe relationships, authority, time, validation, and reconciliation, but it cannot explain purpose.

Intent makes the fabric accountable to objectives and constraints.

## Definition

Fabric Intent Protocol is the purpose model for Agent-Fabric.

It answers:

```text
Why does this exist?
What objective does it serve?
Who expressed the intent?
What constraints apply?
What outcome is expected?
How is success measured?
When does the intent expire?
What must not happen?
```

## Core rule

```text
No autonomous action without explicit intent.
```

## Intent primitive

An Intent is a declared purpose that can produce objectives, constraints, proposals, actions, and outcomes.

```json
{
  "id": "intent:onboarding:reduce-manual-work",
  "type": "Intent",
  "expressedBy": "human:operator",
  "scope": "workspace:customer-success",
  "purpose": "Reduce manual onboarding effort while preserving approval and audit requirements.",
  "objectives": ["objective:onboarding:automate-draft-replies"],
  "constraints": ["constraint:no-sensitive-data-without-approval"],
  "successCriteria": ["criterion:reduce-response-time", "criterion:no-policy-violations"],
  "risk": "medium",
  "status": "active",
  "temporal": {
    "validFrom": "2026-06-07T00:00:00Z",
    "expiresAt": "2026-07-07T00:00:00Z"
  }
}
```

## Intent components

```text
Intent
  -> Objective
  -> Constraint
  -> Action Boundary
  -> Success Criteria
  -> Outcome
```

## Objective

An Objective is a measurable target derived from intent.

```json
{
  "id": "objective:onboarding:automate-draft-replies",
  "type": "Objective",
  "intent": "intent:onboarding:reduce-manual-work",
  "description": "Draft onboarding replies for human review.",
  "measure": "percentage of onboarding replies drafted before human review",
  "target": 0.8,
  "status": "active"
}
```

Rule:

```text
No objective without intent.
```

## Constraint

A Constraint limits how an objective may be pursued.

```json
{
  "id": "constraint:no-sensitive-data-without-approval",
  "type": "Constraint",
  "description": "The agent must not access sensitive customer data unless approval exists.",
  "enforcedBy": ["policy:customer-data-access"],
  "severity": "critical"
}
```

Rule:

```text
Constraints override objectives.
```

## Action boundary

An Action Boundary defines what is allowed, forbidden, and approval-gated.

```json
{
  "id": "boundary:onboarding:draft-only",
  "type": "ActionBoundary",
  "intent": "intent:onboarding:reduce-manual-work",
  "allowedActions": ["read-approved-context", "draft-response", "request-review"],
  "forbiddenActions": ["send-email-without-human-approval", "access-payment-data"],
  "approvalRequiredFor": ["send-email", "access-sensitive-record"]
}
```

## Success criteria

Success criteria define how outcomes are judged.

```json
{
  "id": "criterion:reduce-response-time",
  "type": "SuccessCriterion",
  "description": "Reduce average onboarding response preparation time by 40%.",
  "measurementSource": "agent-traces",
  "target": "40_percent_reduction"
}
```

## Outcome

An Outcome is the observed result of pursuing intent.

```json
{
  "id": "outcome:onboarding:week-1",
  "type": "Outcome",
  "intent": "intent:onboarding:reduce-manual-work",
  "status": "partiallyAchieved",
  "evidence": ["trace:onboarding:week-1"],
  "metrics": {
    "draftCoverage": 0.72,
    "policyViolations": 0
  }
}
```

## Intent sources

Intent may be expressed by:

- human
- team
- organization
- contract
- policy
- agent
- system
- platform

Agent-expressed intent is always subordinate to human, contract, policy, and platform authority.

## Intent hierarchy

```text
Human Intent
  -> Organizational Intent
  -> Contract Intent
  -> Policy Intent
  -> Agent Intent
  -> Action Intent
```

When intents conflict:

```text
Safety > Law/Compliance > Contract > Human Approval > Policy > Objective > Optimization
```

## Intent-to-action chain

Every autonomous action must be traceable back to intent.

```text
Intent
  -> Objective
  -> Constraint
  -> Proposal
  -> Validation
  -> Authority
  -> Reconciliation
  -> Action
  -> Outcome
```

## Intent validation

An intent is invalid when:

- expressedBy is missing,
- scope is missing,
- purpose is missing,
- no objective exists,
- constraints are missing for medium or higher risk,
- success criteria are missing,
- temporal validity is missing for delegated or autonomous intent,
- intent conflicts with policy, contract, or authority,
- intent cannot be traced to an accountable authority.

## Intent risk

| Risk | Meaning |
|---|---|
| low | Informational or assistive intent |
| medium | Operational intent affecting work routing or output |
| high | Intent affecting access, identity, runtime, external systems, or contracts |
| critical | Intent affecting money, tenant boundaries, sensitive data, legal obligations, or autonomous authority |

Rule:

```text
High and critical intent requires explicit authority before execution.
```

## Intent expiry

Intent must expire or be renewed when it grants ongoing autonomy.

```text
Intent expires
  -> DriftDetected
  -> ReconciliationRequired
  -> Renew, retire, or quarantine related actions
```

## Relationship to Fabric primitives

| Primitive | Intent relationship |
|---|---|
| Node | May be created to satisfy intent |
| Relationship | Must serve or evidence intent |
| Contract | May bind intent into obligation |
| Identity | Identifies who expressed or owns intent |
| Event | Records intent-related change |
| Trace | Evidences intent execution |
| Proposal | Suggests a way to satisfy intent |
| Reconciliation | Decides whether intent-aligned change becomes state |
| State | Projects accepted intent outcomes |

## One-line definition

Fabric Intent Protocol is the purpose layer that binds every autonomous fabric action to an accountable objective, constraint, and measurable outcome.
