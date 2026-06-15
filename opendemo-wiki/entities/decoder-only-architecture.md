---
title: Decoder-Only Architecture
summary: GPT series models use causal attention and autoregressive generation for text synthesis.
updated: 2026-06-05
tags:
  - llm
  - architecture
  - decoder-only-architecture
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/architecture/decoder-only-architecture/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Decoder-Only Architecture

Decoder-Only architecture powers GPT-series models with causal (masked) self-attention and autoregressive token generation.

## Architecture

```
Input: "今天天气"
  ▼
Token Embedding + Positional Encoding
  ▼
Causal (Masked) Self-Attention (Q,K,V projections + lower-triangular mask)
  ▼
Feed Forward Network
  ▼
[N × Decoder Layers]
  ▼
Language Model Head → Output Token
```

## Core Concepts

### Causal Attention

Position i can only attend to positions 0 to i-1, enforced via lower-triangular attention mask.

### Autoregressive Generation

```python
def generate(model, input_ids, max_new_tokens):
    for _ in range(max_new_tokens):
        logits = model(input_ids)
        next_token_logits = logits[:, -1, :]
        next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
        input_ids = torch.cat([input_ids, next_token], dim=1)
    return input_ids
```

### Training Objective

```
Loss = -Σ log P(x_{t+1} | x_1, ..., x_t)
```

## Key Implementation

```python
class CausalSelfAttention(nn.Module):
    def __init__(self, d_model, num_heads, max_seq_len, dropout=0.1):
        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)
        self.register_buffer(
            "causal_mask",
            torch.tril(torch.ones(max_seq_len, max_seq_len))
        )

    def forward(self, x):
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        scores = scores.masked_fill(causal_mask == 0, float('-inf'))
        attention_weights = F.softmax(scores, dim=-1)
```

## Comparison: Decoder vs Encoder

| Feature | Decoder-Only | Encoder-Only |
|---------|--------------|--------------|
| Attention | Unidirectional (causal) | Bidirectional |
| Generation | Strong | Weak |
| Context | Unidirectional | Bidirectional |
| Typical Tasks | Text generation | Understanding, classification |
| Training Efficiency | Low (autoregressive) | High (parallel) |

## Key Insights

- [[entities/tech-stacks]] for LLM technology stacks overview
- Causal mask prevents seeing future information
- KV Cache is critical for inference acceleration
- [[entities/gpt-architecture]] for GPT series evolution
- [[entities/llama-architecture]] for LLaMA optimizations
