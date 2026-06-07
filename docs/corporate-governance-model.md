# Corporate Governance Model

Agent-Fabric governance is organization-owned, platform-led, evidence-backed, and community-contributed.

The platform owns accountability.
The kernel preserves truth.
The graph plans work.
Operators execute.
Edge participants observe and act.
Partners and providers fulfill scoped commitments.
The community contributes under maintained boundaries.

## Definition

Corporate governance for Agent-Fabric is the system of authority, accountability, controls, evidence, decision rights, risk boundaries, partner commitments, community contribution rules, and release practices that keep the platform trustworthy and sustainable.

```text
Organization Governance
  -> Platform Governance
  -> Protocol Governance
  -> Runtime Governance
  -> Community Governance
  -> Partner Governance
  -> Release Governance
```

## Core rule

```text
The organization owns accountability. The platform operationalizes governance. The kernel protects truth.
```

---

## Governance layers

| Layer | Responsibility |
|---|---|
| Corporate governance | purpose, accountability, risk appetite, oversight |
| Platform governance | service model, contract model, partner model, delivery controls |
| Protocol governance | vocabulary, schemas, MCP/OpenAPI, compatibility |
| Kernel governance | invariants, validation, authority, reconciliation, projection |
| Runtime governance | execution, observability, safety, reliability |
| Community governance | issues, PRs, discussions, reviews, contribution boundaries |
| Partner governance | capability admission, commitments, SLAs, evidence, escalation |
| Release governance | CI/CD, versioning, release notes, provenance, rollback |

---

## Board and stewardship principles

Agent-Fabric governance should follow these principles:

```text
clear purpose
clear accountability
transparent decisions
risk-aware authority
separation of duties
evidence-based control
stakeholder respect
responsible disclosure
regular review
continuous improvement
```

## Decision rights

| Decision | Owner |
|---|---|
| Platform direction | AGenNext |
| Customer-facing contract model | AGenNext |
| Kernel invariant changes | Maintainers / platform authority |
| Protocol compatibility changes | Maintainers after proposal review |
| Community contribution acceptance | Maintainers |
| Partner admission | Platform authority |
| Provider capability certification | Platform authority / delegated reviewers |
| Release approval | Maintainers |
| High-risk runtime action | Authorized accountable authority |

---

## Risk appetite

Risk must be classified and governed.

```text
low      = informational or low-impact change
medium   = operational change with bounded impact
high     = identity, access, runtime, policy, contract, or production impact
critical = safety, money, tenant boundary, legal, sensitive data, or autonomous authority impact
```

Rules:

```text
High-risk changes require explicit authority.
Critical-risk changes require escalation and final review.
No high-risk adapter may bypass kernel-native validation, authority, reconciliation, or projection.
```

---

## Internal control model

Agent-Fabric controls should cover:

```text
control environment
risk assessment
control activities
information and communication
monitoring
```

Fabric mapping:

| Control area | Fabric implementation |
|---|---|
| Control environment | organizational autonomy, platform-owned contracts, governance docs |
| Risk assessment | risk levels, authority gates, issue triage, release gates |
| Control activities | CI, reviews, validation, reconciliation, approval workflow |
| Information and communication | GitHub issues, discussions, wiki, roadmap, release notes |
| Monitoring | CI status, stale workflow, community loop, health reports, audit evidence |

---

## Community governance

GitHub-native community loop:

```text
Discussion
  -> Issue
  -> Project
  -> Pull Request
  -> CI
  -> Review
  -> Merge
  -> Release
  -> Wiki/docs update
```

Rule:

```text
Community contributes. AGenNext curates. Kernel invariants stay stable.
```

Community may contribute:

```text
docs
examples
SDKs
MCP tools/resources/prompts
Kubernetes operator work
Horizon UI
Fabric Box packaging
integration proposals
vocabulary proposals
```

Strict review required for:

```text
fabric-core
fabric-runtime
authority semantics
reconciliation semantics
projection semantics
lifecycle changes
protocol compatibility changes
```

---

## Partner and provider governance

Partners and providers participate through scoped commitments.

They may supply:

```text
capability
software
infrastructure
support
integration
delivery capacity
compliance evidence
```

They must have:

```text
identity
scope
contract or agreement
commitments
evidence obligations
support path
risk classification
lifecycle status
```

Rule:

```text
Providers fulfill commitments. Partners co-deliver outcomes. The platform owns the customer-facing contract unless explicitly shared.
```

---

## Release governance

Release rules:

```text
CI must pass.
Protocol changes must be documented.
Kernel changes require strict review.
Release notes must describe compatibility impact.
Artifacts should be traceable to commit SHA.
Manual release is required until automated release governance is mature.
```

Release stages:

```text
proposal
candidate
validated
released
monitored
superseded
archived
```

---

## Audit and evidence

Every important governance action should produce evidence.

Examples:

```text
issue
pull request
review
CI run
release artifact
commit SHA
approval comment
reconciliation record
incident report
partner evidence
compliance report
```

Rule:

```text
No claim without evidence. No outcome without trace.
```

---

## Incident and escalation governance

Incidents should be classified by impact:

```text
security
availability
data integrity
tenant boundary
protocol integrity
kernel correctness
partner/provider failure
community conduct
```

Escalation should include:

```text
owner
severity
affected scope
evidence
mitigation
reconciliation requirement
communication plan
post-incident review
```

---

## One-line definition

AGenNext corporate governance for Agent-Fabric is an organization-owned, platform-led, evidence-backed control model where community contribution, partner delivery, runtime execution, and release automation operate under clear authority, risk, reconciliation, and audit boundaries.
