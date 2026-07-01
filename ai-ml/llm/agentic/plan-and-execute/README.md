<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Plan-and-Execute 规划执行模式

> 本案例详解 Plan-and-Execute Agent 范式，先规划后执行

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Plan-and-Execute 流程                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Task: "帮我写一篇关于 AI 的博客，并发布到博客平台"          │
│                                                                 │
│  Phase 1: Planning (规划)                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  LLM 生成执行计划                                        │   │
│  │                                                          │   │
│  │  Plan:                                                   │   │
│  │  1. Research AI topic and outline structure             │   │
│  │  2. Write blog content with examples                    │   │
│  │  3. Review and edit content                            │   │
│  │  4. Format for blog platform                           │   │
│  │  5. Publish to blog                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  Phase 2: Execution (执行)                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  逐个执行计划中的步骤                                    │   │
│  │                                                          │   │
│  │  Step 1 → Step 2 → Step 3 → Step 4 → Step 5            │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  Phase 3: Recovery (可选 - 失败恢复)                           │
│       │                                                         │
│       ▼                                                         │
│  Final Output                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 核心实现

### Plan-and-Execute Agent

```python
class PlanAndExecuteAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    async def plan(self, task: str) -> List[str]:
        """生成执行计划"""
        prompt = f"""Given the task: {task}
        
Break it down into clear, ordered steps.
Output as a numbered list."""
        
        response = self.llm.generate(prompt)
        steps = self.parse_steps(response)
        return steps
    
    async def execute(self, plan: List[str]) -> Any:
        """执行计划"""
        results = []
        for step in plan:
            result = await self.execute_step(step, results)
            results.append(result)
        return results
    
    async def run(self, task: str) -> Dict:
        """完整流程"""
        plan = await self.plan(task)
        results = await self.execute(plan)
        return {"plan": plan, "results": results}
```

## 🔗 相关案例

- `react-agent` - ReAct Agent
- `multi-agent-collaboration` - Multi-Agent
- `langchain-agent` - LangChain Agent

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 AI/ML 核心概念。

### 2. 适用场景

- 场景 1：学术研究
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
python code/main.py
```
