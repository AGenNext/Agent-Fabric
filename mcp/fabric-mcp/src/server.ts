import { callTool, tools } from "./tools.js";

async function main() {
  console.log("Agent-Fabric MCP server scaffold");
  console.log("Registered tools:", tools.join(", "));
  console.log(await callTool("fabric.health", { target: "fabric://local" }));
}

main().catch((error) => { console.error(error); process.exit(1); });
