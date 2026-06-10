// NestJS injectable service over the Agent-Fabric kernel and query helpers.
import { Injectable } from "@nestjs/common";
import { Entity, Graph, GraphEvent } from "./types";
import { GraphKernel, explode, FoldSummary } from "./kernel";
import { byKind, ego, hop } from "./query";
import { NodeKind, RelationPredicate } from "./vocabulary";

@Injectable()
export class AgentFabricService {
  /** Project the emulated state of a base graph after an event delta (no subgraph materialized). */
  emulate(base: Graph, events: GraphEvent[], until?: number): Graph {
    return new GraphKernel(base, events, until).view().graph;
  }

  /** Emulate and also return the change summary. */
  emulateWithSummary(base: Graph, events: GraphEvent[], until?: number): { graph: Graph; summary: FoldSummary } {
    return new GraphKernel(base, events, until).view();
  }

  /** Decompose a graph into a genesis event log that rebuilds it from empty. */
  explode(graph: Graph): GraphEvent[] {
    return explode(graph);
  }

  /** Ego-network around a node: the centre plus everything within `radius` hops. */
  ego(graph: Graph, center: string, radius = 1): Entity[] {
    return ego(graph, center, radius);
  }

  /** All nodes of a kind. */
  byKind(graph: Graph, kind: NodeKind): Entity[] {
    return byKind(graph, kind);
  }

  /** One hop from a set of node ids along a predicate ("*" for any); reverse follows incoming edges. */
  hop(graph: Graph, fromIds: string[], predicate: RelationPredicate | "*", reverse = false): Entity[] {
    return hop(graph, fromIds, predicate, reverse);
  }
}
