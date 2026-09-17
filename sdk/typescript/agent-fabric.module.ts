// NestJS module exposing the Agent-Fabric service. Import into any Nest app:
//   @Module({ imports: [AgentFabricModule] }) export class AppModule {}
import { Module } from "@nestjs/common";
import { AgentFabricService } from "./agent-fabric.service";

@Module({
  providers: [AgentFabricService],
  exports: [AgentFabricService],
})
export class AgentFabricModule {}
