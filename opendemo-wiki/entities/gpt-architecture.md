---
title: GPT Architecture
summary: GPT series evolved from 117M to 175B+ parameters, pioneering scaling laws and in-context learning capabilities.
updated: 2026-06-05
tags:
  - llm
  - architecture
  - gpt-architecture
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/architecture/gpt-architecture/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# GPT Architecture

GPT series (GPT-1/2/3/4) pioneered decoder-only architecture with scaling laws and emergent in-context learning capabilities.

## Evolution

```
GPT-1 (2018)          GPT-2 (2019)        GPT-3 (2020)
117M, 12 layers       1.5B, 48 layers     175B, 96 layers
768 dim               1600 dim            12288 dim

GPT-4 (2023)
???B (proprietary)
MoE?, 128K context, multimodal
```

## Key Innovations

### Scaling Law (Kaplan et al., 2020)

```
L(N) = (N_c / N)^α + (N_min / N)^β + const

- N: model parameters
- L: cross-entropy loss
- α ≈ 0.076, β ≈ 0.095
```

Model scale matters more than data scale.

### In-Context Learning

```python
prompt = """
Translate to French:
English: Hello
French: Bonjour

English: Good morning
French:"""

# Model learns pattern without parameter updates
output = gpt3.generate(prompt)
```

## Key Implementation

```python
class GPTBlock(nn.Module):
    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x

class GPT(nn.Module):
    def forward(self, idx):
        tok_emb = self.wte(idx)
        pos_emb = self.wpe(pos)
        x = self.drop(tok_emb + pos_emb)
        
        for block in self.h:
            x = block(x)
        
        return self.lm_head(self.ln_f(x))
```

## Scaling Laws Data

| Parameters | Training Tokens | Optimal Batch | Optimal LR |
|------------|-----------------|---------------|------------|
| 117M | 1M-100M | ~0.5M | 3e-4 |
| 1.5B | 1B | ~1M | 2.5e-4 |
| 175B | 300B | ~4M | 1.2e-4 |

## GPT-2 vs GPT-3 vs GPT-4

| Feature | GPT-2 | GPT-3 | GPT-4 |
|---------|-------|-------|-------|
| Parameters | 1.5B | 175B | proprietary |
| Context | 1K | 2K→8K | 128K |
| Multimodal | No | No | Yes |
| Reasoning | Basic | Medium | Strong |

## Key Insights

- [[entities/decoder-only-architecture]] for base architecture concepts
- [[entities/llama-architecture]] for optimized open-source implementation
- [[entities/state-space-models]] for linear-complexity alternatives
- [[entities/tech-stacks]] for LLM technology stacks overview
- Emergent abilities appear at critical model scales
