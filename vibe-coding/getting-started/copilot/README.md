# GitHub Copilot 快速上手

## 什么是 GitHub Copilot

GitHub 和 OpenAI 联合推出的 AI 编码助手，集成在 VS Code、JetBrains 等 IDE 中，提供实时代码补全和对话功能。

## 安装

1. 在 VS Code 扩展商店搜索 "GitHub Copilot" 安装
2. 登录 GitHub 账号授权
3. Copilot Chat 需要单独安装（免费版有额度限制）

## 核心 Vibe Coding 功能

### 行内补全（Ghost Text）
写注释或函数签名后，Copilot 自动灰色提示补全代码。按 `Tab` 接受。

### Copilot Chat
侧边栏对话，支持：
- `/explain` — 解释选中代码
- `/tests` — 生成测试用例
- `/fix` — 修复错误
- `/doc` — 生成文档注释

### Copilot Edits（多文件编辑）
类似 Cursor 的 Composer，一次修改多个文件。

### Copilot Agent（最新）
给 Copilot 一个 issue 描述，它自动分析代码库、规划方案、创建 PR。

## Vibe Coding 最佳实践

1. **用注释驱动开发** — 先写清晰的注释描述意图，让 Copilot 补全实现
2. **提供示例** — 在 prompt 中给一个输入输出示例，Copilot 的理解会准确很多
3. **迭代修正** — 不满意时不要反复按 Tab，而是写更具体的注释
4. **用 Chat 而非盲猜** — 遇到复杂逻辑时，先在 Chat 中讨论方案，再写代码

## 对应 OpenDemo 练习

- 入门：[Go Gin Web 框架](../practices/go/go-ginwebdemo-web-framework-intro/CHALLENGE.md)
- 进阶：[Python 异步编程](../practices/python/async-programming/CHALLENGE.md)
- 高级：[Node.js 熔断器](../practices/nodejs/nodejs-circuit-breaker-demo/CHALLENGE.md)
