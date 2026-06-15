---
title: State Space Models (Mamba)
summary: Mamba SSM offers O(n) inference complexity vs O(n²) for transformers, with selective state scanning.
updated: 2026-06-05
tags:
  - llm
  - architecture
  - state-space-models
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/architecture/state-space-models/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# State Space Models (Mamba)

Mamba introduces selective scanning SSM achieving O(n) inference vs O(n²) for transformers.

## Architecture Comparison

```
Transformer                    Mamba (SSM)
O(n²) Attention                O(n) Linear Scan
Q,K,V projections              Selective SSM
Softmax(QK^T)V                 x' = Ax + Bu, y = Cx + Du
                             
Strengths: Expressive          Strengths: Linear inference, selective memory
Weaknesses: O(n²) complexity   Weaknesses: Slightly less expressive
```

## Core Concepts

### State Space Model Equations

```
Continuous:
  x'(t) = A · x(t) + B · u(t)
  y(t) = C · x(t) + D · u(t)

Discrete:
  x_k = A_k · x_{k-1} + B_k · u_k
  y_k = C_k · x_k + D_k · u_k
```

### Mamba Selective Mechanism

```python
def selective_scan(u, A, B, C, D):
    # Dynamically compute B, C based on input selection
    B = nn.Parameter(torch.sigmoid(project_input(u, dim_b)) @ B_bar)
    C = nn.Parameter(torch.sigmoid(project_input(u, dim_c)) @ C_bar)
    
    y = causal_conv1d(u)  # Preprocessing
    y = torch.einsum('bld,dn,bld->bln', y, A, u)  # SSM computation
    return y
```

## Key Implementation

```python
class MambaBlock(nn.Module):
    def __init__(self, d_model, d_state=16, d_conv=4, expand=2):
        self.in_proj = nn.Linear(d_model, self.d_inner * 2, bias=False)
        self.conv1d = nn.Conv1d(self.d_inner, self.d_inner, kernel_size=d_conv, padding=d_conv - 1, groups=self.d_inner)
        self.x_proj = nn.Linear(self.d_inner, d_state * 2 + 1, bias=False)
        self.A_log = nn.Parameter(torch.log(torch.arange(1, d_state + 1).repeat(self.d_inner, 1)))

    def selective_scan(self, x, dt, A, B, C, D):
        # Discretize
        dA = torch.exp(dt.unsqueeze(-1) * A)
        dB = dt.unsqueeze(-1) * B.unsqueeze(2)
        
        # Scan computation
        h = torch.zeros(batch, d_inner, d_state, device=x.device)
        for i in range(seq_len):
            h = dA[:, i] * h + dB[:, i] * x[:, i:i+1].transpose(-1, -2)
            y = torch.einsum('bdn,dn->bd', h, C[:, i])
        return y
```

## Efficiency Comparison

| Model | Inference Complexity | 100K Context Time |
|-------|---------------------|-------------------|
| Transformer | O(n²) | ~30 minutes |
| Mamba | O(n) | ~1 minute |
| FlashAttention | O(n²) but efficient | ~5 minutes |

## Transformer vs Mamba

| Feature | Transformer | Mamba |
|---------|-------------|-------|
| Complexity | O(n²) | O(n) |
| Inference Speed | Slow | Fast |
| Context Length | Limited | Scalable |
| Selective Memory | Weak | Strong |
| Parallel Training | Supported | Supported |

## Key Insights

- [[entities/decoder-only-architecture]] for transformer-based decoder
- [[entities/gpt-architecture]] for GPT series evolution
- [[entities/llama-architecture]] for LLaMA optimizations
- [[entities/tech-stacks]] for LLM technology stacks overview
- A matrix acts like LSTM forget gate controlling information retention
- SSM enables parallel training with RNN-like inference efficiency
