---
title: MMLU-Pro Evaluation
summary: Advanced multi-task language understanding evaluation with 10-way multiple choice questions at graduate level difficulty.
updated: 2026-06-05
tags:
  - llm
  - evaluation
  - mmlu-pro
sources:
  - /ai-ml/llm/evaluation/mmlu-pro-evaluation/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# MMLU-Pro Evaluation

Advanced benchmark evaluation with higher difficulty than standard MMLU through 10-way multiple choice questions.

## Key Differences from MMLU

| Feature | MMLU | MMLU-Pro |
|---------|------|----------|
| Questions | ~15,000 | ~12,000 |
| Options | 4 | 10 |
| Difficulty | Medium | High |
| Reasoning | Single-step | Multi-step |
| Random Baseline | 25% | 10% |

## Evaluation Setup

```python
MMLU_PRO_CONFIG = {
    "num_fewshot": 5,
    "num_choices": 10,
    "metric": "multiple_choice_grade",
    "include_reasoning": True,  # CoT prompting
}
```

## Implementation

```python
from datasets import load_dataset

def load_mmlu_pro():
    dataset = load_dataset("cais/mmlu", "mmlu_pro", split="test")
    return dataset

def format_prompt_pro(question: dict, fewshot_examples: list):
    prompt = "Solve the following problem step by step.\n\n"
    for ex in fewshot_examples:
        prompt += f"Question: {ex['question']}\n"
        for i, choice in enumerate(ex['options']):
            prompt += f"  {i}. {choice}\n"
        prompt += f"Reasoning: {ex['reasoning']}\n"
        prompt += f"Answer: {ex['answer']}\n\n"
    return prompt

def extract_answer_pro(generated: str) -> int:
    import re
    patterns = [r"Answer:\s*(\d+)", r"The answer is\s*(\d+)", r"^\s*(\d+)"]
    for pattern in patterns:
        match = re.search(pattern, generated)
        if match:
            return int(match.group(1))
    return -1
```

## Typical Results

| Model | MMLU | MMLU-Pro | Decline |
|-------|------|----------|---------|
| GPT-4 | 86% | 72% | -14% |
| Claude-3 | 88% | 70% | -18% |
| LLaMA-65B | 68% | 45% | -23% |

## Related

- [[entities/gsm8k-evaluation]] - GSM8K Math Evaluation
- [[entities/truthfulqa-evaluation]] - TruthfulQA Evaluation
- [[entities/mbpp-evaluation]] - MBPP Programming Evaluation
