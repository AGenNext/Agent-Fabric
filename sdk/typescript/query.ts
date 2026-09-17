// Query helpers — TypeScript port of the core of tools/bql.py (ego + traversal).
import { Entity, Graph, Relation } from "./types";
import { NodeKind, RelationPredicate } from "./vocabulary";

export function byKind(graph: Graph, kind: NodeKind): Entity[] {
  return graph.nodes.filter((n) => n.kind === kind);
}

// Follow edges of `predicate` ("*" for any) from a set of node ids; returns the
// de-duplicated neighbour nodes. `reverse` follows incoming edges.
export function hop(
  graph: Graph,
  fromIds: string[],
  predicate: RelationPredicate | "*",
  reverse = false,
): Entity[] {
  const nodes = new Map(graph.nodes.map((n) => [n.id, n]));
  const from = new Set(fromIds);
  const out: Entity[] = [];
  const seen = new Set<string>();
  for (const e of graph.edges ?? []) {
    const matchPred = predicate === "*" || e.relation === predicate;
    if (!matchPred) continue;
    const here = reverse ? e.to : e.from;
    const there = reverse ? e.from : e.to;
    if (!from.has(here)) continue;
    const node = nodes.get(there);
    if (node && !seen.has(there)) {
      seen.add(there);
      out.push(node);
    }
  }
  return out;
}

// Ego-network: the centre node plus every node within `radius` hops, any
// direction. Each party is the centre of its own view.
export function ego(graph: Graph, center: string, radius = 1): Entity[] {
  const nodes = new Map(graph.nodes.map((n) => [n.id, n]));
  if (!nodes.has(center)) throw new Error(`unknown center node: ${center}`);
  const adj = new Map<string, Set<string>>();
  const link = (a: string, b: string) => {
    let s = adj.get(a);
    if (!s) adj.set(a, (s = new Set()));
    s.add(b);
  };
  for (const e of graph.edges ?? []) {
    link(e.from, e.to);
    link(e.to, e.from);
  }
  const order: string[] = [center];
  const seen = new Set<string>([center]);
  let frontier: string[] = [center];
  for (let i = 0; i < Math.max(0, radius); i++) {
    const next: string[] = [];
    for (const id of frontier) {
      for (const m of adj.get(id) ?? []) {
        if (!seen.has(m) && nodes.has(m)) {
          seen.add(m);
          order.push(m);
          next.push(m);
        }
      }
    }
    frontier = next;
    if (frontier.length === 0) break;
  }
  return order.map((id) => nodes.get(id)!) as Entity[];
}
