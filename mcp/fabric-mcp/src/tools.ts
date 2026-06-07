export const tools = [
  "fabric.health",
  "fabric.query",
  "fabric.observe",
  "fabric.propose",
  "fabric.validate",
  "fabric.authorize",
  "fabric.reconcile",
  "fabric.project"
] as const;

type EventRecord = {
  id: string;
  subject: string;
  eventType: string;
  source: string;
  payload: Record<string, unknown>;
  intent?: string;
  trace?: string;
  recordedAt: string;
};

type ProposalRecord = {
  id: string;
  proposalType: string;
  subject: string;
  risk: string;
  evidence: string[];
  proposedChange: Record<string, unknown>;
  status: string;
  recordedAt: string;
};

const memory = {
  events: [] as EventRecord[],
  proposals: [] as ProposalRecord[],
  states: new Map<string, Record<string, unknown>>()
};

function nextId(prefix: string) {
  return `${prefix}:${Date.now()}:${Math.random().toString(16).slice(2)}`;
}

function stringArg(args: Record<string, unknown>, key: string, fallback = "") {
  const value = args[key];
  return typeof value === "string" ? value : fallback;
}

export async function callTool(name: string, args: Record<string, unknown>) {
  switch (name) {
    case "fabric.health": {
      const target = stringArg(args, "target", "box:local");
      return { target, health: "healthy", drift: [], recommendedActions: [] };
    }

    case "fabric.query": {
      const queryType = stringArg(args, "queryType", "events");
      const target = stringArg(args, "target", "");
      if (queryType === "events") {
        return { resultType: "Event", results: memory.events.filter((event) => !target || event.subject === target) };
      }
      if (queryType === "proposals") {
        return { resultType: "Proposal", results: memory.proposals.filter((proposal) => !target || proposal.subject === target) };
      }
      if (queryType === "state") {
        return { resultType: "State", results: target ? [memory.states.get(target) ?? null] : Array.from(memory.states.values()) };
      }
      return { resultType: "Unknown", results: [], query: args };
    }

    case "fabric.observe": {
      const subject = stringArg(args, "subject", "box:local");
      const eventType = stringArg(args, "eventType", "Observed");
      const source = stringArg(args, "source", "fabric-mcp");
      const payload = typeof args.payload === "object" && args.payload !== null ? args.payload as Record<string, unknown> : {};
      const record: EventRecord = {
        id: nextId("event"),
        subject,
        eventType,
        source,
        payload,
        intent: stringArg(args, "intent", "intent:fabric:maintain-stable-state"),
        trace: stringArg(args, "trace", nextId("trace")),
        recordedAt: new Date().toISOString()
      };
      memory.events.push(record);
      memory.states.set(subject, { id: `state:${subject}`, subject, health: "healthy", lastEvent: record.id, updatedAt: record.recordedAt });
      return { message: nextId("msg:fabric:observe"), event: record.id, status: "recorded", record };
    }

    case "fabric.propose": {
      const evidence = Array.isArray(args.evidence) ? args.evidence.filter((item): item is string => typeof item === "string") : [];
      const proposal: ProposalRecord = {
        id: nextId("proposal"),
        proposalType: stringArg(args, "proposalType", "GapFillProposal"),
        subject: stringArg(args, "subject", "unknown"),
        risk: stringArg(args, "risk", "medium"),
        evidence,
        proposedChange: typeof args.proposedChange === "object" && args.proposedChange !== null ? args.proposedChange as Record<string, unknown> : {},
        status: "proposed",
        recordedAt: new Date().toISOString()
      };
      memory.proposals.push(proposal);
      return { proposal: proposal.id, status: proposal.status, approvalRequired: proposal.risk === "high" || proposal.risk === "critical", record: proposal };
    }

    case "fabric.validate": {
      const target = stringArg(args, "target", "unknown");
      const issues = target === "unknown" ? [{ code: "TARGET_REQUIRED", message: "target is required", severity: "error" }] : [];
      return { validation: nextId("validation"), valid: issues.length === 0, issues };
    }

    case "fabric.authorize": {
      return { authorityResult: nextId("authority-result"), decision: "Deny", reason: "No grant configured in in-memory runtime." };
    }

    case "fabric.reconcile": {
      return { reconciliation: nextId("reconciliation"), decision: "NeedsAuthority", requiredActions: ["configure_authority"], status: "planned" };
    }

    case "fabric.project": {
      const subject = stringArg(args, "subject", "box:local");
      const state = { id: `state:${subject}:v1`, subject, version: 1, status: "projected", derivedFrom: args.derivedFrom ?? [], projectedAt: new Date().toISOString() };
      memory.states.set(subject, state);
      return { state: state.id, version: 1, status: "projected", record: state };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}
