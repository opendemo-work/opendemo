---
title: Self-Ask Agent
summary: Guide-based question decomposition architecture for breaking down complex problems into simpler sub-questions.
updated: 2026-06-05
tags:
  - llm
  - agentic
  - self-ask-agent
sources:
  - /ai-ml/llm/agentic/self-ask-agent/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Self-Ask Agent

Guide-based question decomposition architecture for breaking down complex problems into simpler sub-questions.

## Architecture

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

## Key Implementation

### Self-Ask Mechanism

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

## Related Cases

- [[entities/reflexion-agent]] - Reflexion Agent
- [[entities/multi-agent-competition]] - Multi-Agent Competition
