# OpenDemo Vibe Coding 实战教程

> 用 AI 编码工具从零复现 518+ 技术案例 — 学工具、练手艺、做项目

## 这是什么

OpenDemo 有 518 个跨 11 个技术栈的可运行 demo。这个目录将这些 demo 转化为 **Vibe Coding 实战练习题**：

- **CHALLENGE.md** — 只给需求和验证标准，不给代码
- **SOLUTION.md** — 记录完整的 AI 编码过程：每轮 prompt、AI 的错误、人工修正、最终方案

不是教你怎么部署 Cursor，而是教你怎么**用好 AI 编码工具**。

## 学习路径

```
入门 → fundamentals/（学技法） → practices/（做练习） → advanced/（做项目）
  ↑                                                              ↓
  └──────────── getting-started/（选工具）←───────────────────────┘
```

### 第一步：选工具（getting-started/）

| 工具 | 特色 | 适合场景 |
|------|------|----------|
| [Cursor](getting-started/cursor/) | Cmd+K 行内编辑，Composer 多文件 | 日常开发首选 |
| [Claude Code](getting-started/claude-code/) | 终端 Agent，自动读写文件 | 终端用户 |
| [Copilot](getting-started/copilot/) | 行内补全 + Chat | VS Code 用户 |
| [Cline](getting-started/cline/) | 自主 Agent，自动执行命令 | 复杂任务 |
| [Windsurf](getting-started/windsurf/) | Cascade 多步推理 | 大型任务 |

### 第二步：学技法（fundamentals/）

| 技法 | 学什么 |
|------|--------|
| [Prompt Engineering](fundamentals/prompt-engineering/) | 五种高效 Prompt 模式 + 反面模式 |
| [迭代技巧](fundamentals/iterative-refinement/) | 骨架→填充、测试驱动、模仿→创造 |
| [AI Debug](fundamentals/debugging-with-ai/) | 五种 Debug 模式 + 元技巧 |
| [AI 写测试](fundamentals/testing-with-ai/) | 四种测试生成方法 + 常见坑 |
| [AI Code Review](fundamentals/code-review-with-ai/) | 三种 Review 模式 + 重点检查清单 |

### 第三步：做练习（practices/）

#### Go（4 个挑战）

| 挑战 | 难度 | 时间 | 核心技能 |
|------|------|------|----------|
| [Cobra CLI](practices/go/go-cobra-cli-cli-tool-demo/CHALLENGE.md) | intermediate | 20min | 分步构建 CLI |
| [Gin Web](practices/go/go-ginwebdemo-web-framework-intro/CHALLENGE.md) | intermediate | 25min | REST API |
| [gRPC + Protobuf](practices/go/go-grpc-protobuf-go-demo/CHALLENGE.md) | advanced | 40min | 微服务通信 |
| [Docker SDK](practices/go/go-dockersdkgo-container-management/CHALLENGE.md) | advanced | 35min | DevOps 自动化 |

#### Python（3 个挑战）

| 挑战 | 难度 | 时间 | 核心技能 |
|------|------|------|----------|
| [OOP](practices/python/oop-classes/CHALLENGE.md) | beginner | 25min | 面向对象基础 |
| [Async](practices/python/async-programming/CHALLENGE.md) | intermediate | 30min | 异步编程 |
| [FastAPI](practices/python/fastapi-complete-tutorial/CHALLENGE.md) | intermediate | 45min | 全栈 Web 开发 |

#### Node.js（2 个挑战）

| 挑战 | 难度 | 时间 | 核心技能 |
|------|------|------|----------|
| [闭包](practices/nodejs/nodejs-closures-demo/CHALLENGE.md) | intermediate | 20min | 函数式编程 |
| [熔断器](practices/nodejs/nodejs-circuit-breaker-demo/CHALLENGE.md) | advanced | 30min | 容错模式 |

#### Kubernetes（1 个挑战）

| 挑战 | 难度 | 时间 | 核心技能 |
|------|------|------|----------|
| [n8n 部署](practices/kubernetes/n8n/CHALLENGE.md) | intermediate | 35min | K8s 生产部署 |

### 第四步：做项目（advanced/）

| 主题 | 内容 |
|------|------|
| [MCP 集成](advanced/mcp-integration/) | 让 AI 连接数据库、GitHub、文件系统 |
| [多文件重构](advanced/multi-file-refactoring/) | 一次 prompt 修改 5+ 文件 |
| [跨栈项目](advanced/cross-stack-project/) | 前端 + 后端 + 部署一体化 |
| [代码迁移](advanced/legacy-migration/) | 用 AI 把老代码迁移到新技术栈 |

## 怎么用

### 跟练模式（推荐新手）
1. 打开 CHALLENGE.md
2. 用 AI 编码工具按需求写代码
3. 卡住时看提示
4. 完成后对比 SOLUTION.md 的 prompt 序列

### 挑战模式（有经验者）
1. 只看 CHALLENGE.md 的目标和约束
2. 不看提示，独立完成
3. 完成后对比 SOLUTION.md，看你的 prompt 策略和参考方案的差异

### 造题模式（高级）
1. 从 OpenDemo 的其他 508 个 demo 中选一个
2. 自己提取 CHALLENGE.md
3. 用 AI 工具完成，记录 prompt 序列
4. 提交到本项目（欢迎 PR）

## 目录结构

```
vibe-coding/
├── README.md                          # 本文件
├── VIBE-CODING-PLAN.md                # 发展规划文档
├── getting-started/                   # 工具入门（5 个工具）
├── fundamentals/                      # 基础技法（5 个主题）
├── practices/                         # 实战练习（10 个挑战）
│   ├── go/                            # Go 挑战 ×4
│   ├── python/                        # Python 挑战 ×3
│   ├── nodejs/                        # Node.js 挑战 ×2
│   └── kubernetes/                    # K8s 挑战 ×1
├── advanced/                          # 高级主题（4 个方向）
├── local-demo/                        # 原 K8s 部署案例（保留）
├── qoder-cli/                         # 原 K8s 部署案例（保留）
├── gemini-cli/                        # 原 K8s 部署案例（保留）
└── other-cli/                         # 原 K8s 部署案例（保留）
```

## 贡献

欢迎贡献新的 Vibe Coding 挑战：
1. 从 OpenDemo 的 518 个 demo 中选择一个
2. 创建 CHALLENGE.md（需求 + 约束 + 验证 + 提示）
3. 用 AI 工具完成，记录 SOLUTION.md（每轮 prompt + 分析）
4. 提交 PR

命名规范：与原 demo 目录名一致，放在 `practices/<stack>/` 下。

## 相关资源

- OpenDemo 主项目：`../` （518+ 技术案例）
- opendemo-cli：`../opendemo-cli/` （搜索和管理 demo 的 CLI 工具）
- 项目规划：`VIBE-CODING-PLAN.md`
