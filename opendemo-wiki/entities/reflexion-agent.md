---
title: Reflexion Agent
summary: Self-reflection architecture enabling agents to improve through self-evaluation and learning from feedback.
updated: 2026-06-05
tags:
  - llm
  - agentic
  - reflexion-agent
sources:
  - /ai-ml/llm/agentic/reflexion-agent/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Reflexion Agent

Self-reflection architecture enabling agents to improve through self-evaluation and learning from feedback.

## Architecture

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

## Key Implementation

### Self-Reflection Mechanism

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

## Related Cases

- [[entities/self-ask-agent]] - Self-Ask Agent
- [[entities/long-term-memory]] - Long-Term Memory
