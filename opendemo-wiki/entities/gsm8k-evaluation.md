---
title: GSM8K Evaluation
summary: Grade School Math 8K benchmark for evaluating multi-step mathematical reasoning with Chain-of-Thought prompting.
updated: 2026-06-05
tags:
  - llm
  - evaluation
  - gsm8k
sources:
  - /ai-ml/llm/evaluation/gsm8k-evaluation/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# GSM8K Evaluation

Mathematical reasoning benchmark with 8,592 grade school math problems requiring multi-step Chain-of-Thought reasoning.

## Dataset Structure

| Stat | Value |
|------|-------|
| Total Problems | 8,592 |
| Training Set | 7,473 |
| Test Set | 1,319 |
| Avg Solution Steps | 2-5 |
| Multi-step Required | 100% |

## Evaluation Setup

```python
GSM8K_CONFIG = {
    "num_fewshot": 5,
    "metric": "exact_match",
    "max_new_tokens": 512,
    "chain_of_thought": True,
}
```

## Implementation

```python
from datasets import load_dataset

def load_gsm8k():
    return {
        "train": load_dataset("openai/gsm8k", "main", split="train"),
        "test": load_dataset("openai/gsm8k", "main", split="test")
    }

def format_prompt(question: str, fewshot_examples: list):
    prompt = "Solve the following math problem step by step.\n\n"
    for ex in fewshot_examples:
        prompt += f"Problem: {ex['question']}\n"
        prompt += f"Solution:\n{ex['answer']}\n\n"
    prompt += f"Problem: {question}\nSolution:\n"
    return prompt

def extract_final_number(answer: str) -> float:
    import re
    numbers = re.findall(r'-?\d+\.?\d*', answer.strip())
    return float(numbers[-1]) if numbers else None
```

## Typical Results

| Model | GSM8K (5-shot) | GSM8K (CoT) |
|-------|----------------|-------------|
| GPT-3 | 46% | 55% |
| GPT-3.5 | 68% | 76% |
| GPT-4 | 87% | 92% |
| LLaMA-65B | 58% | 67% |

## Related

- [[entities/mmlu-pro-evaluation]] - MMLU-Pro Evaluation
- [[entities/mbpp-evaluation]] - MBPP Programming Evaluation
