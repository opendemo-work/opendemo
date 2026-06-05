# Reflexion 自我反思 Agent

> 本案例详解 Reflexion 架构：通过自我反思实现 Agent 能力提升

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Reflexion Self-Reflection 架构                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │    Action    │───▶│   Reflexion  │───▶│   Memory     │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                  │                   │               │
│         ▼                  ▼                   ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Observe    │◀───│   Evaluate   │◀───│    Learn     │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心实现

### 自我反思机制

```python
class ReflexionAgent:
    def __init__(self, llm):
        self.llm = llm
        self.memory = []
        
    def reflect(self, trajectory, feedback):
        prompt = f"""回顾以下执行轨迹：{trajectory}
给予的反馈：{feedback}
进行自我反思并总结改进策略："""
        reflection = self.llm.generate(prompt)
        self.memory.append(reflection)
        return reflection
    
    def act(self, state):
        context = "\n".join(self.memory[-3:])
        action = self.llm.generate(f"{state}\n近期反思：{context}")
        return action
```

## 相关案例

- `react-agent` - ReAct Agent
- `self-ask-agent` - Self-Ask Agent
