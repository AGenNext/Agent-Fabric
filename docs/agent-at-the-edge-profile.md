# Agent at the Edge Profile

Agent at the edge is the deployment model where a Fabric participant runs closest to the real-world signal, device, workload, human workflow, or operational boundary.

The edge agent observes and proposes.
The kernel validates, authorizes, reconciles, and projects.

## Definition

An Edge Agent is a Fabric Participant deployed at or near the execution boundary so it can observe local reality, emit traces, detect drift, propose repairs, and request reconciliation without becoming the source of truth.

```text
Reality / Device / Workload / Human Workflow
  -> Edge Agent
  -> Fabric Protocol Message
  -> Rust Fabric Runtime
  -> Validation / Authority / Reconciliation / Projection
  -> Projected Fabric State
```

## Core rule

```text
Agent at the edge observes and proposes. The Fabric Kernel decides.
```

The edge agent must not silently activate state, bypass authority, bypass reconciliation, or invent local truth.

---

## Placement

```text
Fabric Protocol
    ↓
Rust Fabric Kernel / Runtime
    ↓
Graph Orchestrator
    ↓
Edge Agent
    ↓
Reality
```

Execution substrates:

```text
Ubuntu Core Fabric Box
Kubernetes / k3s node
Landscape-managed Ubuntu machine
PREEMPT_RT realtime box
local workstation
industrial gateway
```

---

## Edge agent responsibilities

Edge agents should own:

```text
local observation
local health checks
local trace emission
local drift detection
local proposal creation
local command execution when authorized
local rollback request
local offline buffering
local reconnection sync
```

Edge agents must not own:

```text
Fabric authority truth
Fabric validation truth
Fabric projected state truth
vocabulary governance
cross-domain reconciliation
final approval for high-risk changes
identity root of trust
```

---

## Edge agent lifecycle

```text
proposed
  -> validating
  -> approved
  -> active
  -> degraded
  -> quarantined
  -> recovered
  -> retired
  -> archived
```

Activation requires:

```text
identity
capability declaration
authority boundary
trace behavior
health endpoint
runtime contract
update channel
```

---

## Edge agent capabilities

Minimum capabilities:

```text
identify
observe
emitTrace
reportHealth
queryLocal
notify
```

Optional capabilities:

```text
propose
challenge
executeApprovedCommand
bufferOfflineEvents
syncBufferedEvents
requestReconciliation
```

High-risk capabilities require explicit authority:

```text
approve
reconcile
project
modifyRuntime
accessSensitiveData
executeExternalAction
```

---

## Edge agent message flow

```text
Observe local signal
  -> emit trace
  -> create Observe message
  -> detect drift if needed
  -> create Proposal or Challenge
  -> send to Runtime / MCP / Operator
  -> wait for reconciliation decision
  -> execute only approved command
  -> report result
```

---

## Edge agent and graph orchestration

The graph orchestrator decides ordering and impact.

Edge agent executes local steps only after the graph plan is validated and reconciled.

```text
Graph ExecutionPlan
  -> Runtime validate/authorize/reconcile
  -> Edge Agent receives approved step
  -> Edge Agent executes
  -> Edge Agent emits trace
  -> Runtime projects state
```

Rule:

```text
No graph edge becomes execution without kernel approval.
```

---

## Edge agent and Kubernetes

On Kubernetes, the edge agent may run as:

```text
DaemonSet
Deployment
sidecar-like participant only when explicitly declared
operator-managed participant
node-local agent
```

Preferred model:

```text
FabricParticipant CRD
  -> Fabric Operator
  -> Edge Agent workload
  -> Runtime status
```

Rule:

```text
Kubernetes schedules the edge agent. Fabric governs the edge agent.
```

---

## Edge agent and Ubuntu Core

On Ubuntu Core, the edge agent should be packaged as a snap.

```text
Snapcraft
  -> fabric-agent-edge snap
  -> snapd confinement
  -> Ubuntu Core Fabric Box
```

Required snap metadata:

```text
identity
capabilities
interfaces
health command
trace behavior
channel
validation set
```

Rule:

```text
No unmanaged edge agent on a Fabric Box.
```

---

## Edge agent and PREEMPT_RT

For real-time boxes, edge agents may observe deadline-sensitive signals.

Real-time priority requires authority.

```text
identity verified
risk classified
authority chain active
time window bounded
trace emitted
```

Rule:

```text
Reasoning is not real-time by default. Safety and evidence loops outrank reasoning loops.
```

---

## Edge agent offline behavior

Edge agents may buffer observations when disconnected.

Offline buffer rules:

```text
append-only
signed or hashed where possible
timestamped
ordered
replayable
synced when connection returns
marked as delayed evidence
```

Rule:

```text
Offline observations are evidence, not automatically accepted state.
```

---

## Edge agent safety rules

1. No autonomous activation of stable state.
2. No high-risk action without authority.
3. No hidden local state mutation.
4. No trace suppression.
5. No vocabulary invention.
6. No cross-domain action without permission.
7. No real-time priority without authority.
8. No offline replay without delayed-evidence marking.
9. No unmanaged agent on Fabric Box.
10. Fail closed for safety, security, identity, policy, or tenant-boundary uncertainty.

---

## One-line definition

Agent at the edge means Fabric intelligence is placed close to reality for observation and action, while validation, authority, reconciliation, and projected truth remain kernel-native and governed.
