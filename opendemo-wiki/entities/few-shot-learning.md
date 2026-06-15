---
title: Few-Shot Learning
summary: In-context learning techniques including example selection strategies and format design for LLM prompting.
updated: 2026-06-05
tags:
  - llm
  - application
  - few-shot-learning
sources:
  - /ai-ml/llm/application/few-shot-learning/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Few-Shot Learning

In-context learning techniques including example selection strategies and format design for LLM prompting.

## Few-Shot Classification

```
┌──────────────────────────────────────────────────────┐
│                   Few-Shot Learning                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Zero-Shot ─────── No examples, instructions only    │
│       │                                               │
│       ▼                                               │
│  One-Shot ─────── 1 example                          │
│       │                                               │
│       ▼                                               │
│  Few-Shot ─────── K examples (typically 3-10)       │
│       │                                               │
│       ▼                                               │
│  Multi-Shot ───── Many examples, near fine-tuning   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Core Strategies

### Example Selection

| Strategy | Method | Pros/Cons |
|----------|--------|-----------|
| Random | Random selection | Simple, may be suboptimal |
| Similarity | Find similar samples | Requires sample library |
| Coverage | Diversity coverage | More comprehensive |
| LLM-based | LLM selection | Best but slower |

### Example Formats

```python
# QA format
qa_template = """Q: {question}
A: {answer}

Q: {new_question}
A:"""

# Chain format
cot_template = """Problem: {problem}
Step 1: {step1}
Step 2: {step2}
Conclusion: {conclusion}

Problem: {new_problem}
Step 1:"""
```

## Key Implementations

### Semantic Similarity Example Selection

```python
from langchain.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticExampleSelector:
    def __init__(self, examples: list, embeddings_model):
        self.examples = examples
        self.embeddings_model = embeddings_model
        self.example_embeddings = embeddings_model.embed_documents(
            [ex["text"] for ex in examples]
        )
    
    def select(self, query: str, k=5):
        query_embedding = self.embeddings_model.embed_query(query)
        
        similarities = cosine_similarity(
            [query_embedding],
            self.example_embeddings
        )[0]
        
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        return [self.examples[i] for i in top_k_indices]
```

### Diverse Example Selection

```python
class DiverseExampleSelector:
    def __init__(self, examples: list, embeddings_model, max_examples=10):
        self.examples = examples
        self.embeddings_model = embeddings_model
        self.max_examples = max_examples
    
    def select(self, query: str, k=5):
        query_embedding = self.embeddings_model.embed_query(query)
        
        selected = []
        remaining = self.examples.copy()
        query_emb = query_embedding
        
        while len(selected) < min(k, len(remaining)):
            best_idx = 0
            best_score = -float('inf')
            
            for i, ex in enumerate(remaining):
                ex_emb = self.embeddings_model.embed_query(ex["text"])
                relevance = cosine_similarity([query_emb], [ex_emb])[0][0]
                diversity = min(
                    cosine_similarity([ex_emb], [self.embeddings_model.embed_query(s["text"])])[0][0]
                    for s in selected
                ) if selected else 1
                
                score = 0.5 * relevance + 0.5 * diversity
                
                if score > best_score:
                    best_score = score
                    best_idx = i
            
            selected.append(remaining.pop(best_idx))
        
        return selected
```

### Dynamic Few-Shot Prompt

```python
class DynamicFewShotPrompter:
    def __init__(self, example_selector, template):
        self.example_selector = example_selector
        self.template = template
    
    def build_prompt(self, query: str, k=5):
        examples = self.example_selector.select(query, k=k)
        
        example_texts = []
        for ex in examples:
            example_texts.append(self.template.format(**ex))
        
        return "\n\n".join(example_texts) + f"\n\nQuery: {query}\nAnswer:"
    
    def invoke(self, query: str, llm, k=5):
        prompt = self.build_prompt(query, k=k)
        return llm.invoke(prompt)
```

## Best Practices

| Scenario | Recommended Examples | Format |
|----------|---------------------|--------|
| Classification | 3-5 | Input-Output |
| QA | 2-3 | Q-A |
| Reasoning | 1-2 | CoT format |
| Code Generation | 1 | Complete function |

## Related Cases

- [[entities/tree-of-thought]] - Tree of Thought
