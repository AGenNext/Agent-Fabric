# Node Kinds

Agent Fabric models the ecosystem as one heterogeneous graph over **12 node kinds** and **22 relation predicates**, defined in the versioned [registry](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/registry/registry.json) (v1.0.0) — the single source of truth from which the tools and SDKs read their vocabulary.

| Kind | Description |
|---|---|
| [`Agent`](#agent) | Autonomous software agent. |
| [`Human`](#human) | Human participant. |
| [`Team`](#team) | Group of agents/humans. |
| [`Tool`](#tool) | Invocable capability. |
| [`Skill`](#skill) | Reusable competency. |
| [`Runtime`](#runtime) | Execution environment. |
| [`Resource`](#resource) | Protected asset. |
| [`Policy`](#policy) | Governance rule. |
| [`Trace`](#trace) | Execution evidence pointer. |
| [`Identity`](#identity) | Credentialed principal. |
| [`Workspace`](#workspace) | Bounded context / partition. |
| [`Channel`](#channel) | Communication channel mediating any parties. |

## Agent

Autonomous software agent.

_Schema: [`nodes/agent.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/agent.schema.json)_

## Human

Human participant.

_Schema: [`nodes/human.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/human.schema.json)_

## Team

Group of agents/humans.

_Schema: [`nodes/team.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/team.schema.json)_

## Tool

Invocable capability.

_Schema: [`nodes/tool.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/tool.schema.json)_

## Skill

Reusable competency.

_Schema: [`nodes/skill.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/skill.schema.json)_

## Runtime

Execution environment.

_Schema: [`nodes/runtime.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/runtime.schema.json)_

## Resource

Protected asset.

_Schema: [`nodes/resource.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/resource.schema.json)_

## Policy

Governance rule.

_Schema: [`nodes/policy.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/policy.schema.json)_

## Trace

Execution evidence pointer.

_Schema: [`nodes/trace.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/trace.schema.json)_

## Identity

Credentialed principal.

_Schema: [`nodes/identity.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/identity.schema.json)_

## Workspace

Bounded context / partition.

_Schema: [`nodes/workspace.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/workspace.schema.json)_

## Channel

Communication channel mediating any parties.

_Schema: [`nodes/channel.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/channel.schema.json)_

## Relation Predicates

The 22 directed predicates that connect node kinds:

| Predicate | Description |
|---|---|
| `MEMBER_OF` | Agent/Human is a member of a Team. |
| `OWNS` | Identity/Human owns an entity. |
| `HAS_IDENTITY` | Agent/Human is bound to an Identity. |
| `ASSUMES_IDENTITY` | Agent assumes/impersonates an Identity at runtime. |
| `USES` | Agent uses a Tool or Skill. |
| `INVOKES` | Runtime-observed invocation of a Tool by an Agent. |
| `DEPENDS_ON` | Dependency between tools/skills/agents. |
| `PROVIDES` | Tool/Runtime provides a Skill or Resource. |
| `RUNS_ON` | Agent runs on a Runtime. |
| `DEPLOYED_IN` | Runtime is deployed in a Workspace. |
| `SCOPED_TO` | Entity is scoped to a Workspace. |
| `GOVERNED_BY` | Subject is governed by a Policy. |
| `GRANTS` | Policy grants access to a Resource. |
| `ACCESSES` | Agent accesses a Resource. |
| `TRUSTS` | Trust edge between agents/identities. |
| `DELEGATES_TO` | Agent delegates a task/authority to another agent. |
| `COMMUNICATES_WITH` | Direct interaction between any two parties. |
| `COLLABORATES_WITH` | Team-to-team collaboration. |
| `PARTICIPATES_IN` | A party participates in a communication Channel — one node connecting any parties. |
| `PRODUCED` | Agent produced a Trace. |
| `EVIDENCED_BY` | An assertion is evidenced by a Trace. |
| `DERIVED_FROM` | Entity/relation derived/inferred from another. |
