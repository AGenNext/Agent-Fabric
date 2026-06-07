# Fabric MCP Server

`fabric-mcp` is the first executable API surface for Agent-Fabric.

It exposes Fabric operations as MCP tools, resources, and prompts.

## Purpose

```text
MCP Client
  -> Fabric MCP Server
  -> Fabric Kernel / SDK
  -> Fabric State
```

## Tools

```text
fabric.create_node
fabric.create_relationship
fabric.observe
fabric.propose
fabric.validate
fabric.authorize
fabric.approve
fabric.reject
fabric.commit
fabric.challenge
fabric.reconcile
fabric.project
fabric.query
fabric.notify
fabric.explain
fabric.health
```

## Resources

```text
fabric://federations/{id}
fabric://domains/{id}
fabric://clusters/{id}
fabric://boxes/{id}
fabric://participants/{id}
fabric://states/{id}
fabric://authority/{id}
fabric://commitments/{id}
fabric://reconciliations/{id}
fabric://traces/{id}
```

## Prompts

```text
fabric.diagnose_drift
fabric.review_proposal
fabric.audit_authority
fabric.explain_state
fabric.reconcile_box
fabric.health_report
```

## Rule

```text
MCP tools may request change.
Fabric validation, authority, reconciliation, and projection decide state.
```

## First implementation target

Build a minimal server that supports:

```text
fabric.health
fabric.query
fabric.observe
fabric.propose
fabric.validate
```

Then add:

```text
fabric.authorize
fabric.reconcile
fabric.project
```

## One-line definition

Fabric MCP Server is the agent-facing gateway that turns Agent-Fabric protocol operations into governed MCP tools, resources, and prompts.
