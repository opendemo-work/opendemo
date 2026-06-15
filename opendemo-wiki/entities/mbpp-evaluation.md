---
title: MBPP Evaluation
summary: Python programming benchmark (Mostly Basic Python Problems) evaluating code generation with Pass@K metrics.
updated: 2026-06-05
tags:
  - llm
  - evaluation
  - mbpp
sources:
  - /ai-ml/llm/evaluation/mbpp-evaluation/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# MBPP Evaluation

Python programming benchmark evaluating code generation using Pass@K metrics.

## Dataset Structure

| Stat | Value |
|------|-------|
| Total Problems | 974 |
| Training Set | 500 |
| Test Set | 500 |
| Avg Code Length | ~15 lines |
| Avg Test Cases | 3-5 per problem |

## Pass@K Metric

```python
MBPP_CONFIG = {
    "num_prompt_examples": 3,   # 3-shot
    "metric": "pass_at_k",      # Pass@K metric
    "k_values": [1, 10, 100],
    "timeout": 5,               # seconds
}
```

## Implementation

```python
from datasets import load_dataset

def load_mbpp():
    return {
        "full": load_dataset("mbpp", split="full"),
        "test": load_dataset("mbpp", split="test"),
        "train": load_dataset("mbpp", split="train")
    }

def format_prompt(problem: dict, fewshot_examples: list):
    prompt = "Solve the following Python problem:\n\n"
    for ex in fewshot_examples:
        prompt += f"Problem: {ex['text']}\n"
        prompt += f"Code: {ex['code']}\n\n"
    prompt += f"Problem: {problem['text']}\nCode: "
    return prompt

def calculate_pass_at_k(results: dict, k_values: list) -> dict:
    pass_at_k = {}
    for k in k_values:
        total = len(results)
        passed = sum(1 for r in results.values() if r.get(f"passed_at_{k}"))
        pass_at_k[f"pass@{k}"] = passed / total if total > 0 else 0
    return pass_at_k
```

## Typical Results

| Model | Pass@1 | Pass@10 | Pass@100 |
|-------|--------|---------|----------|
| GPT-3 | 45% | 62% | 71% |
| Codex | 72% | 86% | 94% |
| CodeGen | 48% | 67% | 78% |
| StarCoder | 52% | 69% | 80% |

## Related

- [[entities/gsm8k-evaluation]] - GSM8K Math Evaluation
- [[entities/mmlu-pro-evaluation]] - MMLU-Pro Evaluation
