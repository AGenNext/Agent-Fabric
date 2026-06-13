// GraphKernel — TypeScript port of tools/kernel.py. Overlays an event delta on a
// base graph and presents emulated state on read. Storage + calculation: keyed
// last-write-wins, no materialized subgraph.
import { Entity, Graph, GraphEvent, Relation, Watermark } from "./types";
import { NODE_KINDS, RELATION_PREDICATES } from "./vocabulary";

export class KernelError extends Error {}

const NODE_KIND_SET = new Set<string>(NODE_KINDS);
const PREDICATE_SET = new Set<string>(RELATION_PREDICATES);

function enforce(ev: GraphEvent): void {
  const p = ev.payload ?? ({} as GraphEvent["payload"]);
  if (p.id === undefined) throw new KernelError(`event ${ev.id}: payload has no id`);
  if (ev.op === "upsert") {
    if (ev.target === "node") {
      if (!NODE_KIND_SET.has(String(p.kind)))
        throw new KernelError(`event ${ev.id}: unregistered node kind ${String(p.kind)}`);
    } else {
      for (const k of ["relation", "from", "to"] as const) {
        if (p[k] === undefined) throw new KernelError(`event ${ev.id}: edge payload missing ${k}`);
      }
      if (!PREDICATE_SET.has(String(p.relation)))
        throw new KernelError(`event ${ev.id}: unregistered relation ${String(p.relation)}`);
    }
  }
}

export interface FoldSummary {
  eventsApplied: number;
  nodes: [number, number];
  edges: [number, number];
}

export class GraphKernel {
  constructor(
    private readonly base: Graph,
    private readonly events: GraphEvent[] = [],
    private readonly until?: number,
    private readonly strict: boolean = true,
  ) {}

  view(): { graph: Graph; summary: FoldSummary } {
    const nodes = new Map<string, Entity>(this.base.nodes.map((n) => [n.id, { ...n }]));
    const edges = new Map<string, Relation>((this.base.edges ?? []).map((e) => [e.id, { ...e }]));
    let applied = 0;
    let lastSeq: number | undefined;
    let lastAt: string | undefined;
    let stream: string | undefined;

    for (const ev of [...this.events].sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))) {
      const seq = ev.sequence ?? 0;
      if (this.until !== undefined && seq > this.until) break;
      if (this.strict) enforce(ev);
      const store = ev.target === "node" ? (nodes as Map<string, any>) : (edges as Map<string, any>);
      const pid = ev.payload.id;
      if (ev.op === "upsert") store.set(pid, { ...ev.payload });
      else if (ev.op === "delete") store.delete(pid);
      else if (ev.op === "invalidate") {
        const cur = store.get(pid);
        if (cur) cur.validTo = ev.payload.validTo ?? ev.occurredAt;
      }
      applied++;
      lastSeq = seq;
      lastAt = ev.occurredAt ?? lastAt;
      stream = ev.stream ?? stream;
    }

    const watermark: Watermark = { asOf: lastAt ?? "1970-01-01T00:00:00Z" };
    if (lastSeq !== undefined) watermark.sequence = lastSeq;
    if (stream !== undefined) watermark.stream = stream;

    const graph: Graph = {
      "@context": this.base["@context"] ?? "https://schema.agennext.dev/agent-fabric/context.jsonld",
      id: this.base.id ?? "af:graph/emulated",
      kind: "Graph",
      nodes: [...nodes.values()],
      edges: [...edges.values()],
      watermark,
    };
    if (this.base.tenant !== undefined) graph.tenant = this.base.tenant;

    return {
      graph,
      summary: {
        eventsApplied: applied,
        nodes: [this.base.nodes.length, nodes.size],
        edges: [(this.base.edges ?? []).length, edges.size],
      },
    };
  }
}

// Decompose a graph into a genesis event log that rebuilds it from empty.
export function explode(graph: Graph, stream = "genesis"): GraphEvent[] {
  const occurred = graph.watermark?.asOf ?? "1970-01-01T00:00:00Z";
  const events: GraphEvent[] = [];
  let seq = 0;
  for (const n of graph.nodes) {
    events.push({ id: `af:event/genesis-${++seq}`, kind: "GraphEvent", stream, sequence: seq,
      op: "upsert", target: "node", occurredAt: occurred, payload: n });
  }
  for (const e of graph.edges ?? []) {
    events.push({ id: `af:event/genesis-${++seq}`, kind: "GraphEvent", stream, sequence: seq,
      op: "upsert", target: "edge", occurredAt: occurred, payload: e });
  }
  return events;
}
