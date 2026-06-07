# Fabric Validator

Fabric Validator is the enforcement layer for Agent-Fabric.

It checks whether nodes, relationships, contracts, identities, events, traces, proposals, reconciliations, and states are valid before they can participate in stable fabric state.

The validator does not decide business truth.
It enforces fabric integrity.

## Definition

Fabric Validator is a deterministic validation layer that rejects incomplete, unsafe, orphaned, circular, untraced, ungoverned, or unresolved fabric records.

It turns a raw fabric graph into a valid fabric graph.

```text
Raw Fabric
  -> Schema Validation
  -> Vocabulary Validation
  -> Reference Validation
  -> Evidence Validation
  -> Authority Validation
  -> Cycle Validation
  -> State Reachability Validation
  -> Valid Fabric
```

## Core rule

```text
Nothing becomes stable state until it passes validation and reconciliation.
```

## Validator responsibilities

| Check | Meaning |
|---|---|
| Schema validation | Record matches its JSON Schema |
| Vocabulary validation | Relationship predicate is canonical |
| Reference validation | Subject and object nodes exist |
| Identity validation | Actors have valid identity records |
| Evidence validation | Relationship or claim has trace evidence |
| Authority validation | Authority is allowed for risk level |
| Contract validation | Governed relationship has a contract when required |
| Cycle validation | Forbidden dependency loops are rejected |
| Orphan validation | Active nodes must be reachable from a workspace, org, team, or platform root |
| State validation | Stable state must derive from events, traces, proposals, and reconciliation |

## Validation phases

### 1. Schema validation

Each record must conform to its schema.

```text
schemas/node.schema.json
schemas/relationship.schema.json
schemas/state.schema.json
```

Failure examples:

- missing `id`
- missing `status`
- invalid `risk`
- empty evidence list
- invalid node type

### 2. Vocabulary validation

Every relationship predicate must exist in the canonical vocabulary.

Invalid:

```text
agent:x magicallyControls tool:y
```

Valid:

```text
agent:x controlledBy policy:y
```

If a new predicate is needed, emit a `VocabularyGapProposal`.

### 3. Reference validation

Every relationship must resolve both ends.

```text
subject exists
object exists
```

Invalid:

```text
agent:x runsOn runtime:missing
```

unless it is explicitly marked as a gap proposal.

### 4. Evidence validation

Every active relationship must have evidence.

Evidence must resolve to at least one trace, event, decision, or source record.

```text
No evidence, no active relation.
```

### 5. Identity validation

Every actor must have identity.

Actors include:

- humans
- agents
- tools
- runtimes
- services
- teams
- organizations
- issuers
- approvers

```text
No actor without identity.
```

### 6. Authority validation

Authority must match risk.

| Risk | Minimum authority before activation |
|---|---|
| low | system |
| medium | policy or platform |
| high | policy plus platform |
| critical | human plus policy plus platform |

Agents may propose high or critical relationships, but cannot activate them.

### 7. Contract validation

Some relationships require contracts.

| Predicate | Contract required |
|---|---|
| `boundBy` | yes |
| `contractsWith` | yes |
| `authorizedBy` | yes |
| `controlledBy` | yes |
| `governedBy` | yes |
| `runsOn` | yes for production runtime |
| `uses` | yes for sensitive tools |
| `delegatesTo` | yes for privileged work |

### 8. Cycle validation

Some cycles are allowed. Some are forbidden.

Allowed:

```text
workspace contains agent
agent belongsTo workspace
```

Forbidden:

```text
policy:a governedBy policy:b
a policy:b governedBy policy:a
```

```text
agent:a dependsOn agent:b
agent:b dependsOn agent:a
```

unless an explicit coordination contract allows the cycle.

### 9. Orphan validation

Active nodes must be reachable from at least one root.

Valid roots:

- platform
- organization
- tenant
- workspace
- team

Orphan nodes may exist only in `proposed`, `archived`, or `quarantined` state.

### 10. State reachability validation

Stable state must be derived from:

```text
Event
Trace
Proposal or Direct Observation
Reconciliation
```

A state projection with no derivation is invalid.

## Validation result

The validator emits a validation result.

```json
{
  "id": "validation:relationship:001",
  "target": "rel:agent:onboarding-assistant:runsOn:runtime-default",
  "valid": false,
  "severity": "error",
  "errors": [
    {
      "code": "AUTHORITY_TOO_LOW",
      "message": "High-risk relationship requires policy plus platform authority before activation."
    }
  ],
  "warnings": [],
  "checkedAt": "2026-06-07T00:00:00Z"
}
```

## Error levels

| Level | Meaning |
|---|---|
| info | Useful diagnostic only |
| warning | Allowed but should be reviewed |
| error | Cannot become active |
| critical | Must be blocked and escalated |

## Validator outputs

The validator may emit:

- `ValidationPassed`
- `ValidationFailed`
- `GapDetected`
- `VocabularyGapProposal`
- `ContractRequired`
- `IdentityRequired`
- `EvidenceRequired`
- `AuthorityRequired`
- `CycleDetected`
- `OrphanDetected`
- `ReconciliationRequired`

## Relationship with Gap Filler Agent

The Gap Filler Agent detects incompleteness.

The Validator decides whether the proposed completion is structurally valid.

The Platform decides whether the proposed completion becomes operational state.

```text
Gap Filler Agent
  -> Proposal
  -> Fabric Validator
  -> Reconciliation
  -> Stable State
```

## One-line definition

Fabric Validator is the deterministic integrity gate that prevents incomplete or unsafe relationships from becoming stable fabric state.
