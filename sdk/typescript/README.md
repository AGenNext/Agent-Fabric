# @agennext/agent-fabric — TypeScript + NestJS SDK

The TypeScript SDK targets Horizon, dashboards, browser surfaces, and
MCP/OpenAPI clients. It is a typed, dependency-light SDK for the Agent-Fabric
meta-model: graphs and events are plain JSON, and this package adds the
**vocabulary**, **types**, the **GraphKernel** (emulation/rebuild), **query**
helpers (ego, hop, byKind), and a **NestJS module/service**. Pure TypeScript —
NestJS is an optional peer dependency, so the core works in any Node/TS project.

## Install

```bash
npm install @agennext/agent-fabric
# NestJS integration (optional):
npm install @nestjs/common
```

## Core usage (framework-agnostic)

```ts
import { GraphKernel, ego, explode, NODE_KINDS, Graph, GraphEvent } from "@agennext/agent-fabric";

// Emulate: project the state after an event delta — no subgraph materialized.
const { graph } = new GraphKernel(base, events).view();

// Ego-view: a party at the centre of its world.
ego(graph, "af:agent/researcher-3", 2);

// Rebuild: a graph is reconstructable from its genesis log (byte-identical).
const genesis = explode(base);
new GraphKernel({ nodes: [], edges: [] }, genesis).view();
```

The kernel mirrors `tools/kernel.py` exactly: keyed last-write-wins, append-only
fold, `--at`-style `until` time-travel, and correctness enforced at ingestion
(`KernelError`). Same inputs produce the same projection as the Python tools.

## NestJS usage

```ts
import { Module } from "@nestjs/common";
import { AgentFabricModule, AgentFabricService } from "@agennext/agent-fabric";

@Module({ imports: [AgentFabricModule] })
export class AppModule {}

@Injectable()
export class MyService {
  constructor(private readonly fabric: AgentFabricService) {}

  whoDelegates(graph: Graph) {
    return this.fabric.hop(graph, ["af:agent/orchestrator-7"], "DELEGATES_TO");
  }

  projected(base: Graph, events: GraphEvent[]) {
    return this.fabric.emulate(base, events); // emulated state, on demand
  }
}
```

## Vocabulary

`vocabulary.ts` is **generated from the registry** (`fab vocab --lang ts`), so
`NodeKind`, `RelationPredicate`, and `LifecycleState` never drift from the source
of truth. Regenerate after any registry change.

## Build

```bash
npm run typecheck   # tsc --noEmit
npm run build       # emits dist/
```
