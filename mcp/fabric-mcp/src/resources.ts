export async function readResource(uri: string) {
  return { uri, type: "FabricResource", readAt: new Date().toISOString(), source: "fabric-mcp", data: {}, links: [] };
}
