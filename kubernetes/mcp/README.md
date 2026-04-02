# Model Context Protocol

MCP模型上下文协议演示，AI应用与外部工具集成标准。

## 什么是MCP

MCP是Anthropic推出的开放协议，用于AI模型与外部数据源/工具集成：

```
MCP架构:
┌─────────────────────────────────────────────────────────┐
│                  AI Model (Claude/LLM)                  │
├─────────────────────────────────────────────────────────┤
│                  MCP Host                               │
│              (Claude Desktop/IDE)                       │
├────────────────────────┬────────────────────────────────┤
│      MCP Client        │       MCP Client               │
│   (Built-in Tools)     │    (External Tools)            │
└────────┬───────────────┴───────────────┬────────────────┘
         │                               │
    ┌────┴────┐                    ┌────┴────┐
    │  MCP    │                    │  MCP    │
    │ Server  │                    │ Server  │
    │(Filesystem)                  │(Database)
    └─────────┘                    └─────────┘
```

## MCP Server开发

```typescript
// TypeScript示例
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-mcp-server",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {}
  }
});

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [{
      name: "search_database",
      description: "Search the company database",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string" }
        }
      }
    }]
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## 配置MCP

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/user/data"]
    },
    "postgres": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

## 学习要点

1. MCP协议规范
2. Server开发模式
3. 工具暴露与调用
4. 安全与权限控制
