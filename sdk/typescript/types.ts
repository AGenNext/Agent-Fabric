// Agent-Fabric meta-model types (TypeScript). Mirrors schema/meta/*.schema.json.
import { NodeKind, RelationPredicate, LifecycleState } from "./vocabulary";

export interface Provenance {
  source?: string;
  assertedBy?: string;
  evidence?: string[];
  confidence?: number;
}

export interface Entity {
  id: string;
  kind: NodeKind;
  label?: string;
  description?: string;
  state?: LifecycleState;
  tags?: string[];
  attributes?: Record<string, unknown>;
  scope?: string;
  tenant?: string;
  version?: string;
  revision?: number;
  validFrom?: string;
  validTo?: string;
  observedAt?: string;
  createdAt?: string;
  updatedAt?: string;
  provenance?: Provenance;
}

export interface Relation {
  id: string;
  relation: RelationPredicate;
  from: string;
  to: string;
  directed?: boolean;
  weight?: number;
  attributes?: Record<string, unknown>;
  state?: LifecycleState;
  validFrom?: string;
  validTo?: string;
  observedAt?: string;
  provenance?: Provenance;
}

export interface Watermark {
  asOf: string;
  sequence?: number;
  stream?: string;
}

export interface Graph {
  "@context"?: unknown;
  id?: string;
  kind?: "Graph";
  tenant?: string;
  nodes: Entity[];
  edges: Relation[];
  watermark?: Watermark;
}

export type Op = "upsert" | "delete" | "invalidate";

export interface GraphEvent {
  id: string;
  kind: "GraphEvent";
  stream?: string;
  sequence: number;
  op: Op;
  target: "node" | "edge";
  occurredAt: string;
  recordedAt?: string;
  source?: string;
  correlationId?: string;
  causationId?: string;
  payload: Partial<Entity & Relation> & { id: string };
}
