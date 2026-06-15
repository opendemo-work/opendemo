---
title: Tree of Thought (ToT)
summary: Multi-path exploration and self-evaluation framework to enhance LLM complex problem solving capabilities.
updated: 2026-06-05
tags:
  - llm
  - application
  - tree-of-thought
sources:
  - /ai-ml/llm/application/tree-of-thought/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Tree of Thought (ToT)

Multi-path exploration and self-evaluation framework to enhance LLM complex problem solving capabilities.

## Architecture

```
                    Problem Input
                         │
                         ▼
               ┌─────────────────┐
               │   Thought 1     │ ← Initial Thought
               └────────┬────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     ┌─────────┐  ┌─────────┐  ┌─────────┐
     │ Thought │  │ Thought │  │ Thought │
     │   1.1   │  │   1.2   │  │   1.3   │
     └────┬────┘  └────┬────┘  └────┬────┘
          │            │            │
          ▼            ▼            ▼
     ┌─────────┐  ┌─────────┐  ┌─────────┐
     │ Evaluate│  │ Evaluate│  │ Evaluate│
     │   BAD   │  │  GOOD   │  │   BAD   │
     └─────────┘  └────┬────┘  └─────────┘
                       │ GOOD path continues
                       ▼
                  Continue expansion...
```

## Comparison with CoT

| Feature | Chain of Thought | Tree of Thought |
|---------|------------------|-----------------|
| Structure | Linear chain | Tree branches |
| Exploration | Single path | Multiple paths |
| Evaluation | None | Self-evaluation |
| Use Case | Simple reasoning | Complex planning |

## Key Implementation

### ToT Controller

```python
from typing import List, Callable
from langchain.llms import OpenAI

class ToTController:
    def __init__(self, llm, k=3, max_depth=3):
        self.llm = llm
        self.k = k  # Keep k branches per node
        self.max_depth = max_depth
    
    def generate_thoughts(self, state, prompt_template):
        prompt = prompt_template.format(state=state)
        response = self.llm.invoke(prompt)
        thoughts = response.split('\n')
        return [t.strip() for t in thoughts if t.strip()]
    
    def evaluate_states(self, states: List[str]) -> List[float]:
        eval_prompt = """Rate each state from 0-10 for likely to solve the problem:
        States:
        {states}
        
        Ratings (one per line):"""
        
        prompt = eval_prompt.format(states='\n'.join(
            [f"{i+1}. {s}" for i, s in enumerate(states)]
        ))
        response = self.llm.invoke(prompt)
        return [float(x.strip()) for x in response.split('\n') if x.strip()]
    
    def select_top_k(self, states, scores, k=None):
        k = k or self.k
        paired = sorted(zip(states, scores), key=lambda x: x[1], reverse=True)
        return [state for state, _ in paired[:k]]
    
    def search(self, initial_state, thought_prompt, max_iterations=10):
        current_states = [initial_state]
        
        for depth in range(self.max_depth):
            all_thoughts = []
            
            for state in current_states:
                thoughts = self.generate_thoughts(state, thought_prompt)
                all_thoughts.extend(thoughts)
            
            if not all_thoughts:
                break
            
            scored = self.evaluate_states(all_thoughts)
            current_states = self.select_top_k(all_thoughts, scored)
            
            if depth >= max_iterations:
                break
        
        return current_states
```

### Math Problem Application

```python
class MathToT(ToTController):
    def solve_math_problem(self, problem: str):
        thought_prompt = """Given the math problem: {state}
        
        Think step by step and propose the next calculation or transformation:
        """
        
        final_states = self.search(problem, thought_prompt, max_iterations=5)
        
        answer_prompt = """Based on these solution paths, determine the answer:
        Problem: {problem}
        Paths: {states}
        
        Final answer:"""
        
        answer = self.llm.invoke(answer_prompt.format(
            problem=problem,
            states='\n'.join(final_states)
        ))
        return answer
```

## Related Cases

- [[entities/few-shot-learning]] - Few-Shot Learning
