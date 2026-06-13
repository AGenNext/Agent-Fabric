import { callTool, tools } from "./tools.js";

async function smoke() {
  const health = await callTool("fabric.health", { target: "box:local" });
  const observed = await callTool("fabric.observe", {
    subject: "box:local",
    eventType: "Started",
    source: "fabric-mcp",
    payload: { profile: "local-memory" },
    intent: "intent:fabric:maintain-stable-state"
  });
  const events = await callTool("fabric.query", { queryType: "events", target: "box:local" });
  const state = await callTool("fabric.query", { queryType: "state", target: "box:local" });

  return { health, observed, events, state };
}

async function main() {
  console.log("Agent-Fabric MCP runtime scaffold");
  console.log("Registered tools:", tools.join(", "));
  console.log(JSON.stringify(await smoke(), null, 2));
}

main().catch((error) => { console.error(error); process.exit(1); });
