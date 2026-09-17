// Agent-Fabric vocabulary — generated from the registry; do not edit.
export const REGISTRY_VERSION = "1.0.0";
export type NodeKind = "Agent" | "Human" | "Team" | "Tool" | "Skill" | "Runtime" | "Resource" | "Policy" | "Trace" | "Identity" | "Workspace" | "Channel";
export type RelationPredicate = "MEMBER_OF" | "OWNS" | "HAS_IDENTITY" | "ASSUMES_IDENTITY" | "USES" | "INVOKES" | "DEPENDS_ON" | "PROVIDES" | "RUNS_ON" | "DEPLOYED_IN" | "SCOPED_TO" | "GOVERNED_BY" | "GRANTS" | "ACCESSES" | "TRUSTS" | "DELEGATES_TO" | "COMMUNICATES_WITH" | "COLLABORATES_WITH" | "PARTICIPATES_IN" | "PRODUCED" | "EVIDENCED_BY" | "DERIVED_FROM";
export type LifecycleState = "proposed" | "active" | "degraded" | "suspended" | "retired" | "deleted";
export const NODE_KINDS: NodeKind[] = ["Agent", "Human", "Team", "Tool", "Skill", "Runtime", "Resource", "Policy", "Trace", "Identity", "Workspace", "Channel"];
export const RELATION_PREDICATES: RelationPredicate[] = ["MEMBER_OF", "OWNS", "HAS_IDENTITY", "ASSUMES_IDENTITY", "USES", "INVOKES", "DEPENDS_ON", "PROVIDES", "RUNS_ON", "DEPLOYED_IN", "SCOPED_TO", "GOVERNED_BY", "GRANTS", "ACCESSES", "TRUSTS", "DELEGATES_TO", "COMMUNICATES_WITH", "COLLABORATES_WITH", "PARTICIPATES_IN", "PRODUCED", "EVIDENCED_BY", "DERIVED_FROM"];
export const LIFECYCLE_STATES: LifecycleState[] = ["proposed", "active", "degraded", "suspended", "retired", "deleted"];
