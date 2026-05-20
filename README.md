# Agent-Fabric

Agent-Fabric maps and manages the relationship graph of the AGenNext autonomous ecosystem.

## Decision

Agent-Fabric is the graph/fabric layer connecting agents, humans, teams, tools, skills, runtimes, resources, policies, traces, identities, and workspaces.

It is the ecosystem topology and relationship layer for AGenNext.

## Scope

Agent-Fabric owns:

- agent relationship graphs
- team topology
- runtime topology
- workspace topology
- tool/skill dependency maps
- policy relationship graphs
- trust and interaction graphs
- trace relationship mapping
- organizational graph views
- cross-agent dependency mapping

## Boundary

| Component | Responsibility |
|---|---|
| Agent-Fabric | Ecosystem relationship graph and topology |
| Agent-Team | Agent team definitions |
| Agent-Graph | Workflow/agent execution graph |
| Agent-Traces | Timeline and execution evidence |
| Agent-Identity | Identity and ownership relationships |
| Agent-IGA | Governance and entitlement relationships |
| Agent-Platform | Final operational authority |

## Rule

The ecosystem graph should remain traceable, queryable, and versioned.
