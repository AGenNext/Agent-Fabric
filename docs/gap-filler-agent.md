# Gap Filler Agent

A Gap Filler Agent is an agent that identifies missing, weak, stale, conflicting, or unresolved relationships in the Agent-Fabric and proposes the smallest safe completion needed to restore a usable fabric state.

It does not invent reality.
It does not become the source of truth.
It does not bypass governance.

It fills gaps by producing traceable proposals that can be accepted, rejected, tested, or reconciled by the platform authority.

## Definition

A Gap Filler Agent observes the fabric, detects incomplete relationships, and emits completion proposals.

A gap exists when a fabric node, relationship, contract, event, policy, identity, trace, dependency, or workspace cannot be resolved into a complete operational state.

The agent fills the gap only by:

1. locating existing evidence,
2. deriving the minimum missing relation,
3. marking uncertainty,
4. attaching provenance,
5. submitting the proposal for reconciliation.

## Why it exists

Agent-Fabric is the relationship layer of the autonomous ecosystem.

Real systems drift. Humans forget to link things. Tools emit partial state. Policies evolve. Agents produce traces that may not map cleanly to identities, contracts, skills, runtimes, or workspaces.

The Gap Filler Agent exists so the fabric does not silently break when reality is incomplete.

## What it fills

| Gap type | Example | Output |
|---|---|---|
| Identity gap | Agent has trace but no owner | Proposed `ownedBy` relation |
| Runtime gap | Agent exists but runtime is missing | Proposed `runsOn` relation |
| Policy gap | Tool is callable but no policy is linked | Proposed `guardedBy` relation |
| Skill gap | Work requires capability but no skill is mapped | Proposed `requiresSkill` relation |
| Trace gap | Event exists but no decision record is linked | Proposed `evidencedBy` relation |
| Contract gap | Provider exists but no service contract is linked | Proposed `boundBy` relation |
| Workspace gap | Work item exists but workspace is unresolved | Proposed `belongsToWorkspace` relation |
| Trust gap | Relation exists but provenance is weak | Proposed review or trust downgrade |
| Drift gap | Desired and observed state diverge | Proposed reconciliation action |

## Operating rule

The Gap Filler Agent may propose.
The Fabric records.
The Platform decides.
The Human or policy authority approves when required.

## Inputs

- Fabric graph snapshots
- JSON-LD entity records
- schema.org typed objects
- identity records
- policy records
- traces and event streams
- tool and skill registries
- workspace topology
- runtime topology
- decision logs
- external system observations

## Outputs

Every output is a proposal, never an unverified fact.

```json
{
  "@type": "GapFillProposal",
  "gapId": "gap:agent:runtime:missing",
  "subject": "agent:onboarding-assistant",
  "predicate": "runsOn",
  "object": "runtime:agent-runtime-default",
  "confidence": 0.82,
  "evidence": [
    "trace:2026-06-07:onboarding-assistant:run-17",
    "workspace:customer-success"
  ],
  "risk": "medium",
  "approvalRequired": true,
  "status": "proposed"
}
```

## Lifecycle

```text
Observe
  -> Detect Gap
  -> Classify Gap
  -> Search Evidence
  -> Propose Minimal Completion
  -> Validate Against Schema
  -> Validate Against Policy
  -> Submit For Reconciliation
  -> Record Decision
  -> Monitor Drift
```

## Safety boundaries

The Gap Filler Agent must not:

- create identities without authority,
- grant access without policy approval,
- overwrite source records,
- hide uncertainty,
- collapse conflicting evidence into a false fact,
- create circular dependencies,
- create relationships without provenance,
- mutate runtime state directly,
- bypass Agent-Platform authority.

## Fabric contract

A valid gap-fill proposal must include:

- stable subject identifier,
- relationship predicate,
- proposed object identifier,
- evidence list,
- confidence score,
- risk level,
- approval requirement,
- schema validation result,
- policy validation result,
- trace identifier,
- decision state.

## Relationship to other components

| Component | Relationship |
|---|---|
| Agent-Fabric | Stores topology and relationship proposals |
| Agent-Platform | Holds operational authority and reconciliation decision |
| Agent-Identity | Verifies actors, owners, issuers, and subjects |
| Agent-Policy / Agent-IGA | Validates entitlement and governance constraints |
| Agent-Traces | Provides execution evidence |
| Agent-Control | Detects and reconciles drift |
| Agent-Registry | Resolves agents, tools, skills, and runtimes |
| Agent-Bench / Agent-Eval | Tests quality of proposed completions |

## First principle

The agent fills gaps only so the fabric can remain complete enough to reason over.

Completion is not truth.
Completion is a governed proposal until reconciled.
