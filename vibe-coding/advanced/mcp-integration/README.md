# MCP 集成：用 AI 编码工具连接一切

## 什么是 MCP

Model Context Protocol（MCP）是 Anthropic 提出的开放协议，让 AI 编码工具（如 Claude Desktop、Cursor）可以连接外部数据源和工具。类似于 AI 世界的 USB 接口。

## MCP 对 Vibe Coding 的意义

没有 MCP：AI 只能看到你粘贴给它的代码
有了 MCP：AI 可以读取数据库、调用 API、访问内部文档、操作文件系统

## 常用 MCP Server

| MCP Server | 功能 | 安装方式 |
|------------|------|----------|
| `@modelcontextprotocol/server-filesystem` | 文件系统读写 | npx 直接运行 |
| `@modelcontextprotocol/server-postgres` | PostgreSQL 查询 | npx + 连接字符串 |
| `@modelcontextprotocol/server-github` | GitHub API | npx + GitHub Token |
| `@modelcontextprotocol/server-brave-search` | 网络搜索 | npx + API Key |

## 配置示例（Claude Desktop）

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost:5432/mydb"]
    }
  }
}
```

## Vibe Coding 场景

### 场景一：数据库感知编码
连接 PostgreSQL MCP Server 后：
```
> 看一下 users 表的结构，然后帮我写一个用户注册 API
```
AI 会直接查询数据库 schema，生成匹配的 Pydantic 模型和 SQL。

### 场景二：文件系统操作
连接 Filesystem MCP Server 后：
```
> 读取 src/ 下所有 Go 文件，找出缺少 error handling 的函数
```
AI 可以遍历文件系统，批量分析代码。

### 场景三：GitHub 集成
连接 GitHub MCP Server 后：
```
> 创建一个 PR，把 feature/auth 分支合并到 main，描述今天的改动
```
AI 可以直接操作 GitHub API。

## 对应 OpenDemo 资源

- K8s 中的 MCP 部署案例：`kubernetes/mcp/`
- Cursor 中的 MCP 配置：创建 `.cursor/mcp.json`
