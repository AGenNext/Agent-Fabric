# Ubuntu Real-Time PREEMPT_RT Fabric Profile

Ubuntu Real-Time / PREEMPT_RT is the deterministic scheduling profile for time-sensitive Fabric Boxes.

It is not the default for every Fabric node.
It is the profile for edge, industrial, robotic, telemetry, and control nodes where bounded latency matters.

## Definition

A Fabric Real-Time Box is an Ubuntu Core based Fabric Box running a real-time Linux kernel profile so Fabric participants can execute with more predictable scheduling and lower jitter.

```text
Ubuntu Core 26
  -> Real-Time Kernel / PREEMPT_RT
  -> snapd
  -> Snapcraft-built Fabric snaps
  -> Rust Fabric Kernel
  -> Go Fabric Orchestrator
  -> priority-aware Fabric loops
```

## Core rule

```text
Real-time is for deadlines, not throughput.
```

PREEMPT_RT improves timing determinism.
It does not make agents correct.
It does not replace validation, authority, reconciliation, or traceability.

## Layer meaning

| Layer | Fabric meaning |
|---|---|
| Ubuntu Core | sealed node substrate |
| Real-time kernel | bounded-latency scheduling substrate |
| Snapcraft | packaging compiler for Fabric participants |
| snap confinement | OS capability boundary |
| Rust Fabric Kernel | correctness boundary |
| Go Orchestrator | control loop and adapter boundary |
| Fabric Reconciliation | operational determinism |
| Fabric Projection | stable state output |

## What PREEMPT_RT gives Fabric

```text
bounded scheduling latency
reduced jitter
priority-aware execution
more predictable control loops
safer edge behavior under load
better timing isolation for critical participants
```

## What PREEMPT_RT does not give Fabric

```text
semantic correctness
authority correctness
agent reliability
policy compliance
state reconciliation
identity verification
traceability
rollback
security by itself
```

Those remain Fabric responsibilities.

## Fabric Box profiles

```text
standard
  Ubuntu Core + normal kernel
  general Fabric nodes

edge
  Ubuntu Core + strict confinement + offline recovery
  local/field Fabric nodes

realtime
  Ubuntu Core + PREEMPT_RT kernel profile
  deadline-sensitive Fabric nodes
```

## Use real-time profile for

```text
industrial edge
robotics
factory controllers
IoT gateways
telemetry gateways
real-time monitoring
field devices
medical/clinical device gateways
vehicle/transport gateways
local safety controllers
```

## Do not use real-time profile just for

```text
normal SaaS APIs
web dashboards
batch processing
non-deadline background agents
general enterprise control planes
```

## Fabric loop priority model

Fabric loops should be classified by timing criticality.

| Loop | Priority | Notes |
|---|---|---|
| safety event ingestion | critical | must not be delayed by non-critical agents |
| health heartbeat | high | needed for failover and rollback |
| trace emission | high | evidence must survive failures |
| reconciliation of safety state | high | bounded drift repair |
| policy adapter call | medium | important but can fail closed |
| gap filler proposal | medium | useful but not urgent |
| state projection | medium | bounded but not hard real-time by default |
| analytics/export | low | never block critical loops |
| model/agent reasoning | low by default | not a real-time primitive |

## Scheduling rule

```text
Safety and evidence loops outrank reasoning loops.
```

Agent reasoning must never starve:

```text
health
trace
authority
reconciliation
rollback
```

## Snap service model

Real-time Fabric snaps should declare clear services.

Example service classes:

```text
fabric-kernel.daemon
fabric-orchestrator.daemon
fabric-trace-agent.daemon
fabric-health-agent.daemon
fabric-reconciler.daemon
fabric-gap-filler.daemon
```

The orchestrator owns priority policy and must not let arbitrary agents claim real-time priority.

## Priority authority

Real-time priority is an authority decision.

A snap or participant may request elevated scheduling only when:

```text
identity is verified
authority chain exists
risk is classified
purpose is declared
scope is bounded
time window is bounded
trace is emitted
```

Rule:

```text
No participant gets elevated scheduling without authority.
```

## Real-time drift

Timing violations are Fabric drift.

Examples:

```text
heartbeat missed
trace delayed
reconciliation loop exceeded deadline
rollback health check exceeded window
safety event queue delayed
critical service starved
```

These emit:

```text
TimingDriftDetected
DeadlineMissed
PriorityViolation
RealtimeHealthDegraded
```

and must enter reconciliation.

## Reconciliation under real-time profile

The real-time profile adds deadline context to reconciliation.

```json
{
  "deadline": "PT100MS",
  "priority": "high",
  "missPolicy": "failClosed",
  "onMiss": "quarantine"
}
```

## Failure behavior

Real-time Fabric nodes should prefer safe failure.

```text
deadline missed
  -> emit trace
  -> fail closed if safety/security related
  -> quarantine affected participant
  -> reconcile state
  -> notify accountable authority
```

## Snapcraft role

Snapcraft packages real-time participants exactly like standard participants, but their manifests must declare timing intent.

```text
snapcraft.yaml
  -> service
  -> confinement
  -> plugs/slots
  -> health command
  -> timing class metadata
```

Timing metadata is Fabric-level metadata even if snapd does not natively enforce all of it.
The Go orchestrator and Rust kernel must enforce the Fabric timing policy.

## Kernel boundary

PREEMPT_RT is an OS scheduling feature.

Rust Fabric Kernel remains the correctness kernel.
Go Orchestrator remains the scheduling and control-loop coordinator.
Ubuntu Core remains the sealed substrate.
Snapcraft remains the packaging compiler.

## One-line definition

Ubuntu Real-Time PREEMPT_RT gives Fabric Boxes bounded-latency scheduling; Agent-Fabric turns that timing substrate into governed, traceable, reconciled operational state.
