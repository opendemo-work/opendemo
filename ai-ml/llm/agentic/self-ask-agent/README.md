# Self-Ask 自我提问 Agent

> 本案例详解 Self-Ask 架构：通过引导式提问分解复杂问题

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Self-Ask Agent 架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Question   │───▶│    Self-Ask   │───▶│   Answer    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                  │                   │               │
│         ▼                  ▼                   ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Sub-Question│◀───│   Follow-up   │◀───│   Combine   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心实现

### 自我提问机制

```python
class SelfAskAgent:
    def __init__(self, llm):
        self.llm = llm
        
    def decompose(self, question):
        prompt = f"""将问题分解为更简单的子问题：
问题：{question}
逐步提问并回答："""
        result = self.llm.generate(prompt)
        return self.parse_steps(result)
    
    def answer(self, question):
        steps = self.decompose(question)
        answers = []
        for step in steps:
            ans = self.llm.generate(f"Q: {step}\nA:")
            answers.append(ans)
        return self.combine(answers)
```

## 相关案例

- `react-agent` - ReAct Agent
- `reflexion-agent` - Reflexion Agent
