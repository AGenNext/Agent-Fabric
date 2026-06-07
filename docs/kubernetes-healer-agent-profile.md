# Kubernetes as the Healer Agent

Kubernetes is the healer agent for infrastructure and workload execution in Agent-Fabric deployments.

It is not the Fabric Kernel.
It is not the source of truth.
It is the infrastructure-level healer that continuously reconciles pods, services, deployments, jobs, volumes, probes, and controllers toward desired state.

## Core rule

```text
Kubernetes heals infrastructure.
Fabric governs truth.
Human remains accountable.
```

Kubernetes is a healer because it runs reconciliation loops.

Fabric is the governance layer because it validates, authorizes, reconciles, and projects operational truth.

---

## Placement

```text
Foundation
  -> Fabric Protocol
  -> Fabric Runtime
  -> Graph Orchestrator
  -> Kubernetes Healer Agent
  -> Workloads / Services / Edge Participants
  -> Reality
```

## What Kubernetes heals

Kubernetes may heal:

```text
failed pods
crashed containers
unhealthy services
node placement
replica count drift
rollout drift
configuration rollout
job execution
controller state
resource scheduling
```

Kubernetes must not decide:

```text
contract truth
authority truth
partner/provider accountability
customer-facing outcome truth
high-risk business action
Fabric projected state
foundation contract meaning
```

---

## Healing loop

```text
Observe cluster state
  -> compare to Kubernetes spec
  -> detect drift
  -> take infrastructure action
  -> update status
  -> emit event
  -> Fabric observes evidence
  -> Fabric reconciles operational truth
```

## Fabric + Kubernetes reconciliation

There are two reconciliation loops:

```text
Kubernetes Reconciliation
  = workload health and scheduling

Fabric Reconciliation
  = authority, contracts, commitments, state, outcomes
```

Rule:

```text
Do not confuse healthy pods with fulfilled outcomes.
```

A pod can be healthy while a service commitment is violated.

A workload can restart successfully while a customer outcome remains degraded.

---

## Kubernetes as healer, not owner

Kubernetes may restart the service.

Fabric must decide whether:

```text
the service is still trusted
the outcome is fulfilled
a commitment was violated
a partner/provider failed
a human approval is required
a state projection should change
```

## Healer signals

Kubernetes should emit evidence into Fabric:

```text
PodRestarted
DeploymentRolledOut
ReadinessFailed
LivenessFailed
NodeNotReady
JobFailed
ReplicaDriftDetected
ServiceUnavailable
ConfigRolledOut
```

## Critical path

```text
Cortex observes metrics
Kubernetes heals workloads
Mesh routes traffic
Graph plans recovery
Fabric reconciles truth
Human approves high-risk action
```

---

## Freeze integration

When the freeze switch is active:

Kubernetes may continue safe infrastructure healing such as:

```text
restart failed pods
maintain replicas
preserve logs
keep read-only observability alive
```

Kubernetes must freeze governed transitions such as:

```text
promote release
change contract-bound runtime
run high-risk operator command
publish artifact
activate new partner/provider capability
```

Rule:

```text
Heal runtime safety. Freeze trusted-state transition.
```

---

## One-line definition

Kubernetes is the Agent-Fabric healer agent for infrastructure: it repairs workload drift through reconciliation loops, while Fabric governs truth, Cortex watches the critical path, mesh carries traffic, and accountable humans reopen gates when trust is uncertain.
