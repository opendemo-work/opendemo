# Claude Code 快速上手

## 什么是 Claude Code

Anthropic 官方的 CLI 编码工具，直接在终端中与 Claude 对话，支持读取文件、执行命令、编辑代码。适合习惯终端工作流的开发者。

## 安装

```bash
npm install -g @anthropic-ai/claude-code
```

## 启动

在项目根目录运行：
```bash
claude
```

## 核心 Vibe Coding 功能

### 自然语言指令
直接描述你想做什么：
```
> 帮我创建一个 Go 的 REST API 项目，使用 Gin 框架，包含用户 CRUD 接口
```

### 文件读取与编辑
Claude Code 会自动读取相关文件，也可以明确指定：
```
> 读取 main.go 并添加 graceful shutdown 支持
```

### 命令执行
Claude Code 可以运行 shell 命令：
```
> 运行 go test ./... 并分析失败的测试
```

### 上下文管理
- `/add <file>` — 将文件加入上下文
- `/compact` — 压缩对话历史，保留关键信息
- `/clear` — 清除对话，重新开始

## Vibe Coding 最佳实践

1. **CLAUDE.md 文件** — 在项目根目录创建 `CLAUDE.md`，写明项目约定、常用命令、代码风格。Claude Code 每次启动都会读取
2. **渐进式构建** — 先让 Claude 生成骨架，确认后再逐步补充细节
3. **善用 /compact** — 长对话后压缩历史，避免超出上下文窗口
4. **明确约束** — 告诉 Claude "只用标准库"、"必须兼容 Go 1.19" 等限制条件

## CLAUDE.md 示例

```markdown
# 项目约定
- 中文注释，英文变量名
- Go 项目：go mod init <module-name>
- Python 项目：使用 Black 格式化，行宽 100
- 所有 demo 必须有 README.md 和 metadata.json
```

## 对应 OpenDemo 练习

- 入门：[Python OOP](../practices/python/oop-classes/CHALLENGE.md)
- 进阶：[FastAPI 完整教程](../practices/python/fastapi-complete-tutorial/CHALLENGE.md)
- 高级：[Docker SDK 容器管理](../practices/go/go-dockersdkgo-container-management/CHALLENGE.md)
