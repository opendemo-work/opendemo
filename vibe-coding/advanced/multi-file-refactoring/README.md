# 多文件重构

## 什么是多文件重构

Vibe Coding 中最具挑战性的任务——一次 prompt 修改 5+ 个文件，保持逻辑一致性。

## 适合 AI 的重构类型

| 重构类型 | AI 擅长程度 | 建议 |
|----------|------------|------|
| 重命名变量/函数 | ⭐⭐⭐⭐⭐ | 直接让 AI 做，但要求它检查所有引用 |
| 提取函数/模块 | ⭐⭐⭐⭐ | 明确告诉 AI 新函数的签名和职责 |
| 接口抽取 | ⭐⭐⭐ | 给 AI 一个接口定义示例 |
| 架构级重构 | ⭐⭐ | 风险高，建议分步进行 |
| 跨语言迁移 | ⭐⭐ | AI 能做但容易出错，需要大量测试 |

## Prompt 技巧

### 技巧一：列出所有需要修改的文件

```
将 User 模型从 models.py 拆分到独立的 user.py 模块。
需要修改的文件：
1. models/user.py — 新建，包含 User 类
2. models/__init__.py — 重新导出 User
3. services/user_service.py — 更新 import 路径
4. api/user_handler.py — 更新 import 路径
5. tests/test_user.py — 更新 import 路径

保持所有 public API 不变，只改内部组织。
```

### 技巧二：先规划后执行

```
第一步：分析当前代码结构，列出所有受影响的文件和 import。
不要修改代码，只输出分析结果。

[AI 输出分析后]

第二步：基于分析结果，逐文件修改。每修改一个文件后确认 import 正确。
```

### 技巧三：用 Cursor Composer / Claude Code

这些工具天然支持多文件编辑：
- Cursor Composer：Cmd+I 打开，一次修改多个文件，实时预览 diff
- Claude Code：直接描述任务，AI 自动读取和修改相关文件

## 风险控制

1. **重构前先 commit** — 出问题可以 `git checkout .`
2. **跑测试** — 每改完一批文件立即 `go test ./...` 或 `pytest`
3. **检查 import** — 多文件重构最常见的遗漏是忘记更新 import
4. **不要同时重构 + 加功能** — 一次只做一件事

## 实战练习

- [Go Cobra CLI](../../practices/go/go-cobra-cli-cli-tool-demo/CHALLENGE.md) — 添加第三个子命令（重构 cmd/ 目录）
- [FastAPI](../../practices/python/fastapi-complete-tutorial/CHALLENGE.md) — 拆分 main.py 为多个模块
