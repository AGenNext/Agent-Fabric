# Fabric MCP API

Fabric MCP API is the first developer-facing API surface for Agent-Fabric.

Instead of starting with generic REST, Agent-Fabric exposes Fabric operations as MCP tools, resources, and prompts so agents, IDEs, assistants, operators, and automation runtimes can safely interact with the Fabric.

## Decision

```text
MCP first.
REST later.
SDKs wrap MCP where appropriate.
```

MCP is the right first API surface because Agent-Fabric is built for agent and tool participation.

## Definition

Fabric MCP Server exposes governed Fabric operations as tools while preserving identity, intent, trace, validation, authority, reconciliation, projection, and lifecycle.

```text
Agent / IDE / Assistant / Operator
  -> MCP Client
  -> Fabric MCP Server
  -> Fabric Orchestrator
  -> Rust Fabric Kernel
  -> Fabric State
```

## Core rule

```text
MCP tools may request or propose change. They must not bypass validation, authority, reconciliation, traceability, or lifecycle.
```

## MCP capabilities

Fabric MCP Server exposes:

```text
Tools      -> active operations
Resources  -> readable Fabric records and projections
Prompts    -> guided operational workflows
```

---

# Tools

## fabric.observe

Records an observation as a Fabric event/message.

Input:

```json
{
  "subject": "agent:onboarding-assistant",
  "eventType": "RuntimeObserved",
  "source": "agent:gap-filler",
  "payload": {},
  "intent": "intent:fabric:maintain-stable-state",
  "trace": "trace:runtime:001"
}
```

Output:

```json
{
  "message": "msg:fabric:observe:001",
  "event": "event:runtime-observed:001",
  "status": "recorded"
}
```

## fabric.propose

Creates a proposal such as GapFillProposal, RepairProposal, VocabularyGapProposal, or StateChangeProposal.

Input:

```json
{
  "proposalType": "GapFillProposal",
  "subject": "agent:onboarding-assistant",
  "risk": "high",
  "evidence": ["trace:runtime:001"],
  "proposedChange": {
    "predicate": "runsOn",
    "object": "runtime:default"
  }
}
```

Output:

```json
{
  "proposal": "proposal:gapfill:runtime:001",
  "status": "proposed",
  "approvalRequired": true
}
```

## fabric.validate

Validates a Fabric record or message.

Input:

```json
{
  "target": "proposal:gapfill:runtime:001",
  "validationTypes": ["schema", "semantic", "authority", "temporal", "topology"]
}
```

Output:

```json
{
  "validation": "validation:proposal:001",
  "valid": true,
  "issues": []
}
```

## fabric.authorize

Checks whether an actor may perform an action on a resource within scope.

Input:

```json
{
  "actor": "agent:gap-filler",
  "action": "proposeRelationship",
  "resource": "agent:onboarding-assistant",
  "scope": "domain:customer-a",
  "risk": "high",
  "validation": "validation:proposal:001"
}
```

Output:

```json
{
  "authorityResult": "authority-result:001",
  "decision": "Deny",
  "reason": "No active authority grant matched request."
}
```

## fabric.approve

Approves a proposal when the caller has authority.

Input:

```json
{
  "target": "proposal:gapfill:runtime:001",
  "scope": "runtime-binding",
  "authorityChain": "authority:proposal:runtime:001"
}
```

Output:

```json
{
  "message": "msg:fabric:approve:001",
  "status": "approved"
}
```

## fabric.reject

Rejects a proposal with a reason.

Input:

```json
{
  "target": "proposal:gapfill:runtime:001",
  "reason": "Runtime evidence is insufficient."
}
```

Output:

```json
{
  "message": "msg:fabric:reject:001",
  "status": "rejected"
}
```

## fabric.commit

Creates or accepts an operational commitment.

Input:

```json
{
  "debtor": "runtime:default",
  "creditor": "agent:onboarding-assistant",
  "scope": "runtime execution",
  "condition": "Agent is active and authorized",
  "obligations": ["execute", "emit-trace", "enforce-policy"],
  "evidence": ["trace:contract:001"]
}
```

Output:

```json
{
  "commitment": "commitment:runtime:001",
  "status": "active"
}
```

## fabric.challenge

Challenges a record, relationship, authority decision, commitment, or state projection.

Input:

```json
{
  "target": "rel:agent:onboarding-assistant:runsOn:runtime-default",
  "reason": "Evidence is stale.",
  "requestedAction": "revalidate"
}
```

Output:

```json
{
  "challenge": "challenge:001",
  "status": "recorded",
  "reconciliationRequired": true
}
```

## fabric.reconcile

Produces a reconciliation plan or outcome.

Input:

```json
{
  "target": "proposal:gapfill:runtime:001",
  "desiredState": "state:desired:agent:onboarding-assistant",
  "observedState": "state:observed:agent:onboarding-assistant",
  "currentState": "state:fabric:agent:onboarding-assistant:v1",
  "validation": "validation:proposal:001",
  "authorityResult": "authority-result:001",
  "evidence": ["trace:runtime:001"],
  "risk": "high"
}
```

Output:

```json
{
  "reconciliation": "reconciliation:runtime-gap:001",
  "decision": "Accepted",
  "requiredActions": [],
  "status": "planned"
}
```

## fabric.project

Projects stable Fabric state from accepted source records.

Input:

```json
{
  "subject": "agent:onboarding-assistant",
  "projectionContract": "projection:agent-state:v1",
  "derivedFrom": ["reconciliation:runtime-gap:001"]
}
```

Output:

```json
{
  "state": "state:fabric:agent:onboarding-assistant:v2",
  "version": 2,
  "status": "projected"
}
```

## fabric.query

Queries Fabric state, topology, evidence, commitments, authority, or lifecycle.

Input:

```json
{
  "queryType": "stateAsOf",
  "target": "agent:onboarding-assistant",
  "asOf": "2026-06-07T00:10:00Z"
}
```

Output:

```json
{
  "resultType": "State",
  "results": []
}
```

## fabric.notify

Emits a notification to interested Fabric participants.

Input:

```json
{
  "notificationType": "ReconciliationCompleted",
  "target": "reconciliation:runtime-gap:001",
  "state": "state:fabric:agent:onboarding-assistant:v2"
}
```

Output:

```json
{
  "message": "msg:fabric:notify:001",
  "status": "sent"
}
```

---

# Resources

Fabric MCP resources expose readable state.

```text
fabric://nodes/{id}
fabric://relationships/{id}
fabric://events/{id}
fabric://traces/{id}
fabric://proposals/{id}
fabric://validations/{id}
fabric://authority/{id}
fabric://commitments/{id}
fabric://reconciliations/{id}
fabric://state/{id}
fabric://topology/{id}
fabric://lifecycle/{id}
```

Examples:

```text
fabric://state/agent:onboarding-assistant
fabric://topology/box:factory-gateway-001
fabric://authority/proposal:gapfill:runtime:001
```

---

# Prompts

Fabric MCP prompts provide guided workflows.

## fabric.diagnose_drift

Guides an operator or agent through drift diagnosis.

## fabric.review_proposal

Guides approval or rejection of a proposal.

## fabric.reconcile_box

Guides reconciliation of a Fabric Box.

## fabric.explain_state

Explains how a state projection was derived.

## fabric.audit_authority

Explains who approved what and under which authority.

---

# Safety boundaries

Fabric MCP tools must not:

```text
activate state directly
skip validation
skip authority
skip reconciliation
hide traces
invent predicates
ignore lifecycle
silently update high-risk state
silently cross topology boundaries
```

## One-line definition

Fabric MCP API exposes Agent-Fabric as governed tools, resources, and prompts so agents and operators can interact with Fabric state without bypassing validation, authority, reconciliation, or traceability.
