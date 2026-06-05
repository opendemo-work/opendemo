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
