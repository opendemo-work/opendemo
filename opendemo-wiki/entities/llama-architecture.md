---
title: LLaMA Architecture
summary: LLaMA uses RMSNorm, SwiGLU activation, and RoPE positional encoding for efficient decoder-only performance.
updated: 2026-06-05
tags:
  - llm
  - architecture
  - llama-architecture
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/architecture/llama-architecture/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# LLaMA Architecture

LLaMA architecture introduces RMSNorm, SwiGLU activation, and RoPE rotary positional encoding for efficient decoder-only inference.

## Architecture

```
Input Tokens
  ▼
Token Embedding (with RMSNorm Pre-norm)
  ▼
[N × LLaMA Blocks]
  ▼
Final RMSNorm → Linear (LM Head) → Output Distribution

LLaMA Block:
  Input (Pre-Norm) → RMSNorm → Casual Self-Attention + RoPE → RMSNorm → SwiGLU FFN (W1,W2,W3) → Output
```

## Core Optimizations

### RMSNorm

More efficient than LayerNorm by using root mean square:

```python
class RMSNorm(nn.Module):
    def forward(self, x):
        rms = torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * rms * self.weight
```

### SwiGLU Activation

```
SwiGLU(x) = Swish(W_1, x) ⊙ Sigmoid(W_2, x)
```

### RoPE (Rotary Position Embedding)

Rotary embeddings applied to queries and keys instead of additive positional embeddings.

## Key Implementation

```python
def precompute_freqs_cis(dim, end, theta=10000.0):
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2).float() / dim))
    t = torch.arange(end)
    freqs = torch.outer(t, freqs)
    return torch.polar(torch.ones_like(freqs), freqs)

def apply_rotary_emb(x, freqs_cis):
    x_complex = torch.view_as_complex(x.float().reshape(*x.shape[:-1], -1, 2))
    x_rotated = x_complex * freqs_cis
    return torch.view_as_real(x_rotated).flatten(-2).type_as(x)
```

## LLaMA Series Comparison

| Model | Params | Layers | Heads | Context |
|-------|--------|--------|-------|---------|
| LLaMA 7B | 7B | 32 | 32 | 2048 |
| LLaMA 13B | 13B | 40 | 40 | 2048 |
| LLaMA 70B | 70B | 80 | 80 | 2048 |
| LLaMA 2 70B | 70B | 80 | 80 | 4096 |

## Key Insights

- [[entities/decoder-only-architecture]] for base decoder concepts
- Pre-norm provides better training stability than post-norm
- [[entities/gpt-architecture]] for GPT series evolution
- [[entities/state-space-models]] for alternative efficient architectures
- [[entities/tech-stacks]] for LLM technology stacks overview
- KV Cache enables efficient autoregressive inference
