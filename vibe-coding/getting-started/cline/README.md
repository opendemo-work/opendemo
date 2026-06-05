# Cline 快速上手

## 什么是 Cline

Cline 是 VS Code 中的自主编码 Agent 插件，可以独立完成创建文件、运行命令、浏览终端输出等操作。比 Copilot 更"自主"，适合较复杂的任务。

## 安装

1. VS Code 扩展商店搜索 "Cline" 安装
2. 配置 API Key（支持 OpenAI、Anthropic、OpenRouter 等）

## 核心 Vibe Coding 功能

### 自主编码
描述任务后，Cline 会自动：
- 分析项目结构
- 创建/编辑多个文件
- 运行命令并查看输出
- 根据报错自动修正

### 终端集成
Cline 可以直接在你的终端中执行命令并读取结果，形成反馈循环。

### 浏览器工具
支持用 Puppeteer 访问网页，获取最新文档信息。

## Vibe Coding 最佳实践

1. **明确验收标准** — "完成后运行 `go test ./...` 确保全部通过"
2. **分阶段给任务** — 不要一次让 Cline 做太多，每步确认后再继续
3. **利用终端反馈** — 让 Cline 自己跑测试、看报错、自动修复
4. **限制范围** — "只修改 main.go，不要动其他文件"

## 对应 OpenDemo 练习

- 入门：[Python OOP](../practices/python/oop-classes/CHALLENGE.md)
- 进阶：[Go Cobra CLI](../practices/go/go-cobra-cli-cli-tool-demo/CHALLENGE.md)
- 高级：[Go gRPC](../practices/go/go-grpc-protobuf-go-demo/CHALLENGE.md)
