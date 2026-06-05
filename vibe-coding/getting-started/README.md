# 工具入门

选一个你顺手的工具开始。工具之间没有绝对优劣，核心差异在于工作流偏好。

## 快速选择

| 你的情况 | 推荐工具 | 理由 |
|----------|----------|------|
| 用 VS Code，想要无缝体验 | [Cursor](cursor/) | 基于 VS Code，零迁移成本 |
| 习惯终端，喜欢 CLI | [Claude Code](claude-code/) | 终端内完成所有编码 |
| 已有 Copilot 订阅 | [Copilot](copilot/) | 不用额外装工具 |
| 想要 AI 自主完成复杂任务 | [Cline](cline/) | 自主 Agent，自动执行命令 |
| 想要多步推理自动执行 | [Windsurf](windsurf/) | Cascade 功能最强 |

## 共通原则

无论选哪个工具，以下原则通用：

1. **小步迭代** — 不要一次让 AI 写 500 行，拆成 3-4 步
2. **每步验证** — AI 写完立即运行测试或手动验证
3. **给上下文** — 项目约定、代码风格、已有代码结构都要告诉 AI
4. **Review 每次 AI 改动** — 不要盲目接受，用 diff 视图检查
5. **错了就说** — AI 不会因为你指出错误而"生气"，直接说"这里不对"

## 下一步

选好工具后，先做一个简单的练习热手：
- 新手推荐：[Python OOP](../practices/python/oop-classes/CHALLENGE.md)
- 有经验者：[Go Cobra CLI](../practices/go/go-cobra-cli-cli-tool-demo/CHALLENGE.md)
