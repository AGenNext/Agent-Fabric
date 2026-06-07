# Kubernetes Operator Profile

Kubernetes is the operator and orchestration layer for Agent-Fabric in cluster deployments.

It is not the Fabric Kernel.
It is not the source of governed truth.
It is the reconciliation host that runs controllers, adapters, and Fabric participants at cluster scale.

## Definition

Agent-Fabric uses Kubernetes as an operator substrate where Custom Resources declare desired Fabric objects and controllers call the Rust Fabric Runtime to validate, authorize, reconcile, project, and report status.

```text
Kubernetes CRD
  -> Fabric Controller
  -> Rust Fabric Runtime
  -> Fabric Reconciliation
  -> Fabric Projected State
  -> Kubernetes Status
```

## Core rule

```text
Kubernetes operates the Fabric. The Fabric Kernel governs the state.
```

Kubernetes desired state is an input.
Fabric projected state is the governed output.

---

## Correct placement

```text
Fabric Protocol
    ↓
Rust Fabric Kernel / Runtime
    ↓
Kubernetes Operator
    ↓
Kubernetes Cluster
    ↓
Pods / Services / Config / Secrets
```

Kubernetes is below the kernel boundary.

It schedules and runs.
It does not decide Fabric truth.

---

## Kubernetes responsibilities

Kubernetes should own:

```text
workload scheduling
controller execution
service discovery
config distribution
secret mounting
health probes
scaling
rolling updates
namespace isolation
operator lifecycle
status reporting
```

Kubernetes should not own:

```text
Fabric authority
Fabric commitment truth
Fabric reconciliation rules
Fabric vocabulary governance
Fabric projected state truth
Fabric identity semantics
Fabric lifecycle model
```

---

## Fabric Operator

The Fabric Operator is a Kubernetes controller that watches Fabric CRDs and calls the Fabric Runtime.

```text
Watch CRD
  -> build Fabric message
  -> validate
  -> authorize
  -> reconcile
  -> project
  -> update CRD status
  -> emit event
```

## Minimal CRDs

```text
FabricFederation
FabricDomain
FabricCluster
FabricBox
FabricParticipant
FabricIntent
FabricCommitment
FabricProposal
FabricReconciliation
FabricStateProjection
```

## CRD mapping

| Kubernetes CRD | Fabric model |
|---|---|
| FabricFederation | Federation topology boundary |
| FabricDomain | Domain authority boundary |
| FabricCluster | Cluster update/failure boundary |
| FabricBox | Execution node boundary |
| FabricParticipant | Agent/tool/runtime/controller participant |
| FabricIntent | Purpose and objective declaration |
| FabricCommitment | Operational obligation |
| FabricProposal | Candidate state change |
| FabricReconciliation | Reconciliation request/status |
| FabricStateProjection | Projected state view |

---

## Desired vs projected state

Kubernetes `.spec` expresses desired state.

Fabric `.status.fabric` records projected governed state.

```yaml
apiVersion: fabric.agennext.com/v1alpha1
kind: FabricParticipant
metadata:
  name: gap-filler
spec:
  type: Agent
  capabilities:
    - observe
    - propose
  runtime: fabric-runtime
status:
  fabric:
    lifecycle: active
    projectedState: state:participant:gap-filler:v1
    lastReconciliation: reconciliation:participant:gap-filler:001
```

Rule:

```text
spec is request. status is evidence. Fabric state is truth.
```

---

## Controller loop

```text
Observe Kubernetes object
  -> convert to Fabric record
  -> validate envelope and record
  -> evaluate authority
  -> detect drift
  -> reconcile
  -> project state
  -> update Kubernetes status
  -> emit Kubernetes event
```

## Controller safety rules

1. Controller must not directly activate high-risk Fabric state.
2. Controller must call Fabric Runtime for validation.
3. Controller must call Fabric Runtime for reconciliation.
4. Controller must write status, not mutate spec silently.
5. Controller must preserve events and traces.
6. Controller must fail closed on missing authority.
7. Controller must quarantine unsafe participants.
8. Controller must never become the authority source.

---

## Operator profiles

### Local profile

```text
kind / k3d / minikube
memory runtime
no external policy engine
no external identity provider
```

### Edge profile

```text
k3s
single-node or small cluster
local runtime
offline-capable
snap/Ubuntu Core optional
```

### Enterprise profile

```text
managed Kubernetes
OPA/OpenFGA/AuthZEN adapters
OpenTelemetry
GitOps
Landscape integration
Horizon UI
```

### Fabric Box profile

```text
Ubuntu Core 26
snap-confined Fabric operator
optional k3s
Landscape managed
PREEMPT_RT optional
```

---

## Relationship to GitOps

GitOps declares desired state.
Fabric reconciles governed state.

```text
Git commit
  -> Kubernetes apply
  -> Fabric CRD spec
  -> Fabric Operator
  -> Fabric Runtime
  -> Fabric projected state
```

GitOps must not bypass Fabric authority.

Rule:

```text
GitOps is delivery. Fabric is governance.
```

---

## Relationship to Ubuntu Core

On Fabric Boxes, Kubernetes can run as a snap-confined participant, commonly k3s.

```text
Ubuntu Core
  -> snapd
  -> k3s snap / operator snap
  -> Fabric Operator
  -> Fabric Runtime
```

Ubuntu Core seals the box.
Kubernetes operates workloads.
Fabric governs state.

---

## Relationship to MCP

MCP is the agent-facing API.
Kubernetes Operator is the cluster-facing API.
Both call the same Fabric Runtime.

```text
MCP Tool Call       -> Fabric Runtime
Kubernetes CRD      -> Fabric Runtime
Go Orchestrator     -> Fabric Runtime
Horizon Command     -> Fabric Runtime
```

Rule:

```text
One runtime. Many adapters.
```

---

## One-line definition

Kubernetes is the Agent-Fabric operator substrate: it hosts controllers and desired-state CRDs, while the Rust Fabric Runtime remains the kernel-native authority for validation, reconciliation, projection, and lifecycle truth.
