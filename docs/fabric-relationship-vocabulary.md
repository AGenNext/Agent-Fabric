# Fabric Relationship Vocabulary

The Fabric Relationship Vocabulary defines the canonical predicates used by Agent-Fabric.

A predicate is the typed relationship between two fabric nodes.

Without a shared vocabulary, every repo invents its own edge language and the fabric fragments.

This vocabulary is intentionally small, stable, and composable.

## Rule

```text
No relationship enters the fabric without a canonical predicate.
```

Every relationship must include:

```json
{
  "subject": "node:id",
  "predicate": "canonicalPredicate",
  "object": "node:id",
  "evidence": ["trace:id"],
  "status": "proposed | active | rejected | retired",
  "authority": "platform | policy | human | system",
  "risk": "low | medium | high | critical"
}
```

---

## Canonical predicates

| Predicate | Meaning | Example |
|---|---|---|
| `isA` | Subject is typed as object | `agent:x isA Agent` |
| `ownedBy` | Subject is owned by object | `agent:x ownedBy human:y` |
| `operatedBy` | Subject is operated by object | `runtime:x operatedBy team:y` |
| `controlledBy` | Subject is controlled by object | `tool:x controlledBy policy:y` |
| `governedBy` | Subject is governed by object | `workspace:x governedBy policy:y` |
| `authorizedBy` | Subject action is authorized by object | `access:x authorizedBy approval:y` |
| `uses` | Subject uses object | `agent:x uses tool:y` |
| `dependsOn` | Subject depends on object | `agent:x dependsOn model:y` |
| `runsOn` | Subject executes on object | `agent:x runsOn runtime:y` |
| `belongsTo` | Subject belongs to object | `agent:x belongsTo workspace:y` |
| `contains` | Subject contains object | `workspace:x contains agent:y` |
| `produces` | Subject produces object | `agent:x produces document:y` |
| `consumes` | Subject consumes object | `agent:x consumes event:y` |
| `observes` | Subject observes object | `monitor:x observes runtime:y` |
| `emits` | Subject emits object | `runtime:x emits event:y` |
| `tracedBy` | Subject is evidenced by trace | `event:x tracedBy trace:y` |
| `evidencedBy` | Subject is supported by evidence | `claim:x evidencedBy trace:y` |
| `trusts` | Subject trusts object within scope | `agent:x trusts tool:y` |
| `delegatesTo` | Subject delegates work to object | `human:x delegatesTo agent:y` |
| `reportsTo` | Subject reports to object | `agent:x reportsTo team:y` |
| `contractsWith` | Subject is contractually bound to object | `provider:x contractsWith org:y` |
| `boundBy` | Subject is bound by contract | `agent:x boundBy contract:y` |
| `reconciles` | Subject reconciles object | `controller:x reconciles state:y` |
| `approves` | Subject approves object | `human:x approves proposal:y` |
| `rejects` | Subject rejects object | `policy:x rejects proposal:y` |
| `proposes` | Subject proposes object | `agent:x proposes proposal:y` |
| `requires` | Subject requires object | `task:x requires skill:y` |
| `satisfies` | Subject satisfies requirement | `skill:x satisfies requirement:y` |
| `violates` | Subject violates object | `event:x violates policy:y` |
| `conflictsWith` | Subject conflicts with object | `policy:x conflictsWith policy:y` |
| `supersedes` | Subject replaces object | `contract:v2 supersedes contract:v1` |
| `derivedFrom` | Subject is derived from object | `state:x derivedFrom event:y` |
| `mirrors` | Subject mirrors object | `repo:x mirrors workspace:y` |
| `represents` | Subject represents object | `digitalTwin:x represents system:y` |

---

## Predicate groups

### Identity predicates

```text
isA
ownedBy
operatedBy
represents
```

Owned primarily by:

```text
Agent-Identity
Agent-Fabric
Agent-Platform
```

### Governance predicates

```text
governedBy
controlledBy
authorizedBy
boundBy
approves
rejects
violates
conflictsWith
```

Owned primarily by:

```text
Agent-Policy
Agent-IGA
Agent-Compliance
Agent-Platform
```

### Runtime predicates

```text
runsOn
uses
dependsOn
requires
satisfies
```

Owned primarily by:

```text
Agent-Runtime
Agent-Kernel
Agent-Registry
Agent-Skills
```

### Topology predicates

```text
belongsTo
contains
reportsTo
contractsWith
mirrors
```

Owned primarily by:

```text
Agent-Fabric
Agent-Team
Agent-Space
Agent-Registry
```

### Evidence predicates

```text
emits
observes
tracedBy
evidencedBy
derivedFrom
produces
consumes
```

Owned primarily by:

```text
Agent-Traces
Agent-Control
Agent-Analytics
Agent-Fabric
```

### Decision predicates

```text
proposes
reconciles
approves
rejects
supersedes
```

Owned primarily by:

```text
Agent-Platform
Agent-Control
Agent-Fabric
```

---

## Predicate authority levels

| Authority | Meaning |
|---|---|
| `system` | Recorded by trusted system observation |
| `agent` | Proposed by an agent and requires reconciliation |
| `policy` | Decided by policy engine |
| `human` | Approved or rejected by accountable human |
| `platform` | Final operational authority |

Rule:

```text
Agents may propose relationships. They do not grant final authority.
```

---

## Risk levels

| Risk | Use |
|---|---|
| `low` | Informational topology relation |
| `medium` | Operational relation that can affect routing or work |
| `high` | Access, identity, runtime, governance, or contract relation |
| `critical` | Relation that can grant authority, execute money movement, expose sensitive data, or alter tenant boundaries |

Rule:

```text
High and critical relationships require explicit reconciliation before activation.
```

---

## Relationship lifecycle

```text
proposed
  -> validating
  -> active
  -> challenged
  -> superseded
  -> retired
```

A relationship can be rejected at any stage before activation.

A relationship can be challenged after activation if evidence weakens or drift is detected.

---

## Minimal relationship record

```json
{
  "id": "rel:agent:onboarding-assistant:runsOn:runtime-default",
  "subject": "agent:onboarding-assistant",
  "predicate": "runsOn",
  "object": "runtime:agent-runtime-default",
  "status": "proposed",
  "authority": "agent",
  "risk": "high",
  "evidence": ["trace:run-17"],
  "proposedBy": "agent:gap-filler",
  "createdAt": "2026-06-07T00:00:00Z"
}
```

---

## Validation rules

A relationship is invalid when:

- predicate is not canonical,
- subject is missing,
- object is missing,
- evidence is missing,
- risk is missing,
- authority is missing,
- subject and object create a forbidden cycle,
- predicate violates allowed type pairs,
- relationship bypasses identity, policy, or platform authority.

---

## Allowed type-pair direction

Examples:

| Predicate | Subject type | Object type |
|---|---|---|
| `ownedBy` | Agent, Tool, Workspace, Runtime, Resource | Human, Team, Organization |
| `runsOn` | Agent, Service, Workflow | Runtime, Kernel, Cluster |
| `governedBy` | Agent, Workspace, Tool, Runtime, Contract | Policy, Constitution, RuleSet |
| `boundBy` | Agent, Human, Team, Organization, Service | Contract |
| `tracedBy` | Event, Decision, Proposal, Reconciliation | Trace |
| `reconciles` | Controller, Platform, Agent-Control | State, Proposal, Drift |
| `delegatesTo` | Human, Team, Agent | Agent, Team, Tool, Service |

The full type-pair matrix should be machine-enforced in schema files.

---

## Gap filler behavior

When the Gap Filler Agent detects a missing relation, it must select from this vocabulary.

Example:

```text
Missing runtime edge
  -> candidate predicate: runsOn
  -> risk: high
  -> authority: agent proposal only
  -> requires reconciliation: yes
```

It must not create a new predicate casually.

If no predicate exists, the output must be:

```text
VocabularyGapProposal
```

not an invented relationship.

---

## One-line definition

The Fabric Relationship Vocabulary is the stable edge language that keeps the operational fabric coherent across all AGenNext repositories.
