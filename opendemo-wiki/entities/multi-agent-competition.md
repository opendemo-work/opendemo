---
title: Multi-Agent Competition
summary: Multiple agents competing and collaborating to optimize solutions through adversarial evaluation.
updated: 2026-06-05
tags:
  - llm
  - agentic
  - multi-agent-competition
sources:
  - /ai-ml/llm/agentic/multi-agent-competition/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Multi-Agent Competition

Multiple agents competing and collaborating to optimize solutions through adversarial evaluation.

## Architecture

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

## Key Implementation

### Competitive Agent Implementation

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

## Related Cases

- [[entities/self-ask-agent]] - Self-Ask Agent
- [[entities/reflexion-agent]] - Reflexion Agent
