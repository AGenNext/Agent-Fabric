# Cortex Monitoring Profile

Cortex keeps an eye on the critical path.

In Agent-Fabric, Cortex is the long-term metrics and alerting layer for service delivery, mesh health, runtime health, support paths, and operational drift signals.

## Core rule

```text
Cortex observes. Fabric reconciles. Human remains accountable.
```

Cortex does not own truth.
Cortex does not approve action.
Cortex does not reconcile state.

Cortex emits evidence that Fabric can use.

---

## Placement

```text
Service Mesh / Kubernetes / Runtime / Edge Agents
  -> metrics and alerts
  -> Cortex
  -> Alertmanager / Webhook
  -> Fabric observe
  -> Graph impact analysis
  -> Runtime reconciliation
  -> Human accountability gate when required
```

## What Cortex watches

```text
service availability
latency and error rates
mesh traffic health
mTLS failures
policy denials
timeouts and retries
runtime health
operator health
edge-agent heartbeat
critical path SLOs
release/artifact pipeline health
```

## Critical path signals

Every critical path should have metrics for:

```text
request count
error count
latency
saturation
policy denial
retry count
timeout count
queue depth
reconciliation delay
human approval delay
```

## Evidence flow

```text
Metric breach
  -> Cortex alert
  -> Fabric event
  -> Drift classification
  -> Graph impact report
  -> Reconciliation issue or runtime action
  -> Evidence preserved
```

## Mesh integration

Cortex should ingest metrics from:

```text
Prometheus
Service mesh telemetry
Kubernetes metrics
Runtime metrics
Operator metrics
Edge-agent metrics
GitHub workflow metrics where available
```

## Freeze integration

When freeze/kill-switch is active:

```text
Cortex keeps observing.
State-changing actions freeze.
Evidence collection remains open.
Incident and recovery paths remain open.
```

## One-line definition

Cortex is the observability watcher for Agent-Fabric critical paths: it monitors mesh, runtime, operator, and edge signals, emits evidence, and feeds Fabric reconciliation without replacing kernel authority or human accountability.
