export const tools = ["fabric.health","fabric.query","fabric.observe","fabric.propose","fabric.validate","fabric.authorize","fabric.reconcile","fabric.project"] as const;

export async function callTool(name: string, args: Record<string, unknown>) {
  switch (name) {
    case "fabric.health": return { target: args.target ?? "fabric://local", health: "healthy", drift: [], recommendedActions: [] };
    case "fabric.query": return { resultType: "Stub", results: [], query: args };
    case "fabric.observe": return { message: "msg:fabric:observe:stub", event: "event:stub", status: "recorded" };
    case "fabric.propose": return { proposal: "proposal:stub", status: "proposed", approvalRequired: true };
    case "fabric.validate": return { validation: "validation:stub", valid: true, issues: [] };
    case "fabric.authorize": return { authorityResult: "authority-result:stub", decision: "Deny", reason: "No grant configured in stub server." };
    case "fabric.reconcile": return { reconciliation: "reconciliation:stub", decision: "NeedsAuthority", requiredActions: ["configure_authority"], status: "planned" };
    case "fabric.project": return { state: "state:stub", version: 1, status: "projected" };
    default: throw new Error(`Unknown tool: ${name}`);
  }
}
