# OpenDemo × Vibe Coding 发展方案

> 沉淀时间：2026-05-31

## 一、现状诊断

OpenDemo 目前本质是一个**静态知识库**——518+ demo 案例以文件形式存储，人工编写，AI 仅用于生成新 demo 的辅助手段。

现有 `vibe-coding/` 目录内容较空——4 个高度模板化的 K8s YAML 部署清单（local-demo、qoder-cli、gemini-cli、other-cli），没有真正的代码，没有教学价值。

需要重新定位：**不是教部署 AI 工具，而是教 vibe coding 的手艺。**

## 二、核心洞察

OpenDemo 的真正资产是 **518 个跨栈 demo 的完整代码+文档**。和 vibe coding 教学结合的唯一正确切入点是：

> **用这 518 个 demo 作为"题目"，教用户用 AI 编码工具从零复现它们。**

## 三、教学体系设计

### 三个层次

| 层次 | 给什么 | 学什么 | 难度 |
|------|--------|--------|------|
| **Level 1: 跟练** | 给 prompt + 录屏 + AI 工具配置 | 学会写有效 prompt，复现已知 demo | 入门 |
| **Level 2: 挑战** | 只给需求描述（从 README 提取）+ 测试用例 | 学会用 AI 从需求到完整实现 | 进阶 |
| **Level 3: 造题** | 只给目标效果截图/描述 | 学会拆解问题、多轮对话、debug | 高级 |

### 目录结构

```
vibe-coding/
├── README.md                          # Vibe Coding 学习路径总览
├── getting-started/                   # 工具入门
│   ├── cursor/                        # Cursor IDE 配置和基本用法
│   ├── claude-code/                   # Claude Code (CLI) 用法
│   ├── copilot/                       # GitHub Copilot 用法
│   ├── cline/                         # Cline (VS Code 插件) 用法
│   └── windsurf/                      # Windsurf 用法
│
├── fundamentals/                      # Vibe Coding 基础技法
│   ├── prompt-engineering/            # 如何写好 prompt
│   ├── iterative-refinement/          # 多轮对话迭代技巧
│   ├── debugging-with-ai/             # 用 AI debug 的方法
│   ├── testing-with-ai/              # 让 AI 写测试
│   └── code-review-with-ai/          # 用 AI 做代码审查
│
├── practices/                         # 实战练习（对应已有 demo）
│   ├── go/
│   │   ├── go-concurrency-demo/
│   │   │   ├── CHALLENGE.md           # 只给需求，不给代码
│   │   │   ├── SOLUTION.md            # 完整的 vibe coding 过程
│   │   │   ├── prompts/               # 实际使用的 prompt 序列
│   │   │   │   ├── 01-initial.md
│   │   │   │   ├── 02-refine.md
│   │   │   │   └── 03-debug.md
│   │   │   └── tests/                 # 验证用测试
│   │   └── ...
│   ├── python/
│   ├── nodejs/
│   └── kubernetes/
│
└── advanced/                          # 高级主题
    ├── mcp-integration/               # 用 MCP 扩展 AI 编码能力
    ├── multi-file-refactoring/        # 大规模重构
    ├── cross-stack-project/           # 跨栈项目
    └── legacy-migration/              # 用 AI 迁移老代码
```

### CHALLENGE.md 格式

```markdown
# 挑战：Go 并发模式 — Worker Pool

## 难度：intermediate
## 预计用时：20 分钟
## 推荐工具：Cursor / Claude Code

## 目标
实现一个可配置的 Worker Pool，支持：
- N 个 worker 并发处理任务
- 优雅关闭（处理完进行中的任务再退出）
- 结果收集和错误处理

## 约束
- 只使用 Go 标准库
- 必须通过以下测试（tests/worker_pool_test.go）

## 提示（卡住时再看）
<details>
<summary>提示 1：数据结构</summary>
需要定义 Task struct、Result struct、以及 channel 来连接它们
</details>

## 验证
go test ./tests/ -v
```

### SOLUTION.md 格式（核心差异化）

记录完整的 vibe coding 过程，不是最终代码：

```markdown
# 解决过程：Go Worker Pool

## 使用的工具：Claude Code

### 第 1 轮对话
**Prompt：** "创建一个 Go worker pool，5 个 worker 处理 20 个任务"
**AI 生成：** [代码片段]
**问题：** 没有优雅关闭，直接 os.Exit
**学习点：** 初始 prompt 太笼统，需要明确"优雅关闭"需求

### 第 2 轮对话
**Prompt：** "加上 graceful shutdown，用 context.Context 控制"
**AI 生成：** [改进代码]
**问题：** 测试失败 — results channel 没关闭导致死锁
**学习点：** 用 WaitGroup + close(results) 配合

### 第 3 轮对话
**Prompt：** "修复死锁：worker 完成后关闭 results channel"
**AI 生成：** [最终代码] ✅ 测试通过

## 总结
- 3 轮对话，约 8 分钟
- 关键技巧：先让 AI 写基本框架，再逐步补充边界条件
- 常见坑：channel 关闭时机、context 传播
```

## 四、为什么这个方向有价值

1. **零内容成本启动** — 518 个 demo 已有完整代码和测试，直接提取 CHALLENGE.md
2. **解决真实痛点** — 很多人买了 Cursor/Claude Code 但不会用，缺的不是工具教程，而是**带答案的实战练习题**
3. **数据飞轮** — 用户提交的 prompt 序列和解决过程本身又是新的教学内容
4. **和现有体系天然衔接** — `opendemo search go concurrency` → 找到 demo → 点进去就是对应的 vibe coding 挑战

## 五、落地步骤

1. 从 10 个高质量 demo 提取 CHALLENGE.md（选 Go/Python/Node 各几个，覆盖不同难度）
2. 为这 10 个 demo 录制 SOLUTION.md（实际用 Cursor 或 Claude Code 走一遍，记录 prompt 序列）
3. 写一篇 vibe coding 入门教程放在 `fundamentals/`，用这些案例当教材

## 六、备选方向（记录但非首选）

- RAG 知识库：将 demo 向量化，支持自然语言搜索
- Benchmark 生成器：用 demo 做模型编码能力评测
- 微调数据集：将 demo 转为 instruction-following 训练数据
- 可交互 Playground：零门槛运行环境
- 企业知识管理平台：将 opendemo-cli 改造为通用 SDK
