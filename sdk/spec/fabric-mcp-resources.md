# Fabric MCP Resources

Fabric MCP Resources define the readable `fabric://` namespace for Agent-Fabric.

Tools perform governed operations.
Resources expose readable Fabric records, topology, evidence, history, and projected state.

## Definition

A Fabric MCP Resource is a stable URI-addressed view of Fabric state or history exposed through an MCP server.

```text
fabric://<collection>/<id>
```

## Core rule

```text
Resources are read surfaces. Tools request change. Reconciliation decides state.
```

MCP resources must not mutate Fabric state.

---

## Topology resources

```text
fabric://federations/{id}
fabric://domains/{id}
fabric://clusters/{id}
fabric://boxes/{id}
fabric://participants/{id}
```

Examples:

```text
fabric://federations/federation:agennext
fabric://domains/domain:customer-a
fabric://clusters/cluster:customer-a:edge
fabric://boxes/box:factory-gateway-001
fabric://participants/participant:fabric-kernel:factory-gateway-001
```

## Core record resources

```text
fabric://nodes/{id}
fabric://relationships/{id}
fabric://intents/{id}
fabric://commitments/{id}
fabric://events/{id}
fabric://traces/{id}
fabric://proposals/{id}
fabric://validations/{id}
fabric://authority/{id}
fabric://reconciliations/{id}
fabric://states/{id}
fabric://projection-contracts/{id}
fabric://vocabulary/{id}
fabric://lifecycle/{id}
```

## Derived view resources

```text
fabric://views/state/{subject}
fabric://views/state/{subject}/as-of/{timestamp}
fabric://views/topology/{id}
fabric://views/relationships/{node}
fabric://views/evidence/{target}
fabric://views/authority/{target}
fabric://views/commitments/{node}
fabric://views/drift/active
fabric://views/proposals/open
fabric://views/reconciliations/pending
fabric://views/health/federation/{id}
fabric://views/health/domain/{id}
fabric://views/health/cluster/{id}
fabric://views/health/box/{id}
```

## Ubuntu resources

```text
fabric://ubuntu/landscape/computers/{id}
fabric://ubuntu/landscape/groups/{id}
fabric://ubuntu/core/boxes/{id}
fabric://ubuntu/core/assertions/{box}
fabric://ubuntu/core/snaps/{box}
fabric://ubuntu/core/validation-sets/{box}
fabric://ubuntu/realtime/{box}
fabric://ubuntu/horizon/views/{id}
```

These are Fabric views of Ubuntu estate data, not replacements for Landscape, Ubuntu Core, or Horizon.

---

## Resource response envelope

All resource reads should return a common envelope.

```json
{
  "uri": "fabric://states/state:fabric:agent:onboarding-assistant:v2",
  "type": "State",
  "version": 2,
  "readAt": "2026-06-07T00:00:00Z",
  "source": "fabric-mcp-server",
  "data": {},
  "links": []
}
```

## Links

Resources should expose related resource links.

```json
{
  "links": [
    {
      "rel": "evidence",
      "href": "fabric://traces/trace:runtime:001"
    },
    {
      "rel": "authority",
      "href": "fabric://authority/authority:proposal:runtime:001"
    },
    {
      "rel": "reconciliation",
      "href": "fabric://reconciliations/reconciliation:runtime-gap:001"
    }
  ]
}
```

## Read modes

MCP resources should support these logical read modes:

```text
current
asOf
history
explain
related
```

Examples:

```text
fabric://views/state/agent:onboarding-assistant
fabric://views/state/agent:onboarding-assistant/as-of/2026-06-07T00:10:00Z
fabric://views/evidence/proposal:gapfill:runtime:001
fabric://views/authority/proposal:gapfill:runtime:001
```

## Access control

Resource reads are not automatically public.

Every read must evaluate:

```text
reader identity
requested resource
scope
risk
purpose
policy
relationship to target
```

Rule:

```text
Readable does not mean globally visible.
```

## Resource safety rules

MCP resources must not:

```text
mutate state
activate proposals
approve authority
hide lifecycle state
hide trace requirements
collapse projected state and event history
expose cross-domain records without authority
serve stale state without timestamp
```

## Resource-to-tool pattern

Resources show state.
Tools request change.

Example:

```text
Read:
  fabric://views/drift/active

Then act:
  fabric.challenge
  fabric.reconcile
  fabric.project
```

## One-line definition

Fabric MCP Resources are the URI-addressed read model for topology, records, evidence, authority, reconciliation, lifecycle, Ubuntu estate state, and projected Fabric reality.
