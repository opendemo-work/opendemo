# Multi-Agent 竞争系统

> 本案例详解多 Agent 竞争架构：多个 Agent 对抗协作优化解决方案

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Multi-Agent 竞争架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Agent A    │◀───▶│   Judge      │◀───▶│   Agent B    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                  │                   │               │
│         └──────────────────┴───────────────────┘               │
│                          │                                     │
│                    ┌──────────────┐                            │
│                    │   Best       │                            │
│                    │   Response   │                            │
│                    └──────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心实现

### 竞争 Agent 实现

```python
class CompetitiveAgent:
    def __init__(self, llm, name):
        self.llm = llm
        self.name = name
        self.score = 0
        
    def propose(self, task):
        prompt = f"Agent {self.name} 提出解决方案：{task}"
        return self.llm.generate(prompt)
    
class JudgeAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def evaluate(self, response_a, response_b):
        prompt = f"评估方案A：{response_a}\n方案B：{response_b}"
        winner = self.llm.generate(prompt + "\n选择更优方案：")
        return winner
```

## 相关案例

- `multi-agent-collaboration` - 多 Agent 协作
