# Fabric MCP Prompts

Fabric MCP Prompts define guided workflows for operators, agents, IDEs, assistants, and automation runtimes.

Tools act.
Resources read.
Prompts guide.

## Definition

A Fabric MCP Prompt is a governed operational workflow that helps a user or agent inspect, explain, approve, challenge, reconcile, or audit Fabric state without bypassing validation, authority, lifecycle, or traceability.

## Core rule

```text
Prompts guide decisions. They do not silently mutate Fabric state.
```

Every prompt should route any state-changing action through Fabric MCP tools.

---

## Prompt catalog

```text
fabric.diagnose_drift
fabric.review_proposal
fabric.audit_authority
fabric.explain_state
fabric.reconcile_box
fabric.reconcile_cluster
fabric.reconcile_domain
fabric.trace_commitment
fabric.explain_decision
fabric.health_report
```

---

## fabric.diagnose_drift

Guides diagnosis of active drift.

Inputs:

```json
{
  "target": "box:factory-gateway-001",
  "scope": "cluster:customer-a:edge"
}
```

Workflow:

```text
Read active drift
Read target topology
Read evidence
Read validation report
Classify drift
Recommend challenge, evidence request, quarantine, or reconciliation
```

May call:

```text
fabric.query
fabric.challenge
fabric.reconcile
fabric.notify
```

Must not directly activate state.

---

## fabric.review_proposal

Guides approval or rejection of a proposal.

Inputs:

```json
{
  "proposal": "proposal:gapfill:runtime:001"
}
```

Workflow:

```text
Read proposal
Read evidence
Read validation result
Read authority chain
Read risk
Explain impact
Ask for approve, reject, request evidence, or escalate
```

May call:

```text
fabric.approve
fabric.reject
fabric.challenge
fabric.notify
```

---

## fabric.audit_authority

Explains who approved what and under which authority.

Inputs:

```json
{
  "target": "proposal:gapfill:runtime:001"
}
```

Workflow:

```text
Read authority chain
Read approvers
Read scope
Read risk
Read expiration
Read trace
Detect missing or expired authority
Explain accountability
```

May call:

```text
fabric.query
fabric.challenge
fabric.notify
```

---

## fabric.explain_state

Explains how a projected state was derived.

Inputs:

```json
{
  "state": "state:fabric:agent:onboarding-assistant:v2"
}
```

Workflow:

```text
Read state
Read derivedFrom records
Read events
Read traces
Read proposals
Read validations
Read authority chains
Read reconciliations
Produce replay explanation
```

May call:

```text
fabric.query
```

---

## fabric.reconcile_box

Guides reconciliation of a Fabric Box.

Inputs:

```json
{
  "box": "box:factory-gateway-001"
}
```

Workflow:

```text
Read box topology
Read Ubuntu Core profile
Read Landscape status
Read snap revisions
Read validation set status
Read participant health
Read active drift
Prepare reconciliation input
Request authority if needed
Call reconciliation
Project state
```

May call:

```text
fabric.query
fabric.validate
fabric.authorize
fabric.reconcile
fabric.project
fabric.notify
```

---

## fabric.reconcile_cluster

Guides reconciliation of a Fabric Cluster.

Inputs:

```json
{
  "cluster": "cluster:customer-a:edge"
}
```

Workflow:

```text
Read cluster topology
Read boxes
Read update domain
Read failure domain
Read validation set compliance
Aggregate drift
Classify risk
Plan staged reconciliation
```

May call:

```text
fabric.query
fabric.validate
fabric.authorize
fabric.reconcile
fabric.project
fabric.notify
```

---

## fabric.reconcile_domain

Guides reconciliation of a Fabric Domain.

Inputs:

```json
{
  "domain": "domain:customer-a"
}
```

Workflow:

```text
Read domain topology
Read policies
Read authority boundaries
Read commitments
Read compliance state
Read cluster health
Classify domain drift
Recommend repair, escalation, or quarantine
```

May call:

```text
fabric.query
fabric.challenge
fabric.reconcile
fabric.notify
```

---

## fabric.trace_commitment

Explains a commitment lifecycle.

Inputs:

```json
{
  "commitment": "commitment:runtime:001"
}
```

Workflow:

```text
Read commitment
Read debtor
Read creditor
Read obligations
Read evidence
Read due time
Read fulfillment or violation
Explain what remains owed
```

May call:

```text
fabric.query
fabric.challenge
fabric.notify
```

---

## fabric.explain_decision

Explains why a reconciliation decision happened.

Inputs:

```json
{
  "reconciliation": "reconciliation:runtime-gap:001"
}
```

Workflow:

```text
Read reconciliation record
Read validation result
Read authority result
Read evidence
Read risk
Read applied changes
Explain decision path
```

May call:

```text
fabric.query
```

---

## fabric.health_report

Generates a health report for a federation, domain, cluster, box, or participant.

Inputs:

```json
{
  "target": "cluster:customer-a:edge",
  "depth": "box"
}
```

Workflow:

```text
Read topology
Read health views
Read drift
Read failed validations
Read pending reconciliations
Read timing violations
Read Landscape signals
Summarize status and recommended actions
```

May call:

```text
fabric.query
fabric.notify
```

---

## Prompt safety rules

Prompts must not:

```text
approve without authority
reject without reason
reconcile without validation
project without accepted reconciliation
hide uncertainty
collapse evidence into unsupported fact
skip lifecycle
cross domains without permission
```

## One-line definition

Fabric MCP Prompts are guided operational workflows that help humans and agents inspect, explain, approve, challenge, reconcile, and audit Fabric state through governed MCP tools and resources.
