---
title: SparseGPT Pruning
summary: One-shot pruning using Hessian information for global error correction, achieving 50% sparsity with minimal accuracy loss.
updated: 2026-06-05
tags:
  - llm
  - optimization
  - pruning
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/optimization/sparsegpt-pruning/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# SparseGPT Pruning

SparseGPT (Sparse Generative Pre-training) enables one-shot pruning with error correction using Hessian information.

## Core Principle

```
Traditional pruning: Layer-by-layer independent, error accumulates
SparseGPT: Uses Hessian information for global error correction

Key Insight:
- Pruning error can be compensated by adjusting other weights
- Need Hessian matrix inverse to determine compensation amount
- Direct Hessian inverse is impractical, uses approximation
```

## Pruning Formula

```python
def sparsegpt_update(W, hessian, mask, pruned_indices):
    error = W[:, pruned_indices] @ hessian[pruned_indices]
    h_inv = torch.linalg.inv(hessian + 1e-6 * torch.eye(hessian.size(0)))
    compensation = -h_inv @ error
    W_new = W + compensation * mask
    return W_new
```

## Implementation

```python
class SparseGPTPruner:
    def __init__(self, model, sparsity=0.5):
        self.model = model
        self.sparsity = sparsity
        self.masks = {}
        
    def compute_hessian_approximation(self, layer, x, y):
        proj = torch.randn(x.shape[-1], 512, device=x.device)
        x_proj = x @ proj
        hessian_approx = x_proj.t() @ x_proj / x.shape[0]
        return hessian_approx
    
    def prune_layer(self, layer, x, y):
        W = layer.weight.data.clone()
        n, m = W.shape
        n_pruned = int(m * self.sparsity)
        
        importance = (W ** 2).mean(dim=0)
        prune_indices = torch.argsort(importance)[:n_pruned]
        
        mask = torch.ones_like(W)
        mask[:, prune_indices] = 0
        
        hessian = self.compute_hessian_approximation(layer, x, y)
        W_corrected = self.sparsegpt_error_correction(W, hessian, mask, prune_indices)
        
        layer.weight.data = W_corrected
        self.masks[layer] = mask
        
    def sparsegpt_error_correction(self, W, hessian, mask, pruned_indices):
        W_compensated = W.clone()
        h_diag = hessian.diagonal()
        for idx in pruned_indices:
            error = (W[:, idx] * h_diag).sum()
            correction = -error / (h_diag.sum() + 1e-6)
            W_compensated[:, idx] = 0
            W_compensated[:, :len(correction)] += correction * mask[:, :len(correction)]
        return W_compensated
```

## Sparsity Comparison

| Sparsity | SparseGPT PPL | Magnitude PPL | Memory Reduction |
|----------|---------------|---------------|------------------|
| 0% | 12.5 | 12.5 | 1.0x |
| 50% | 13.2 | 15.8 | 1.5x |
| 70% | 14.5 | 18.2 | 2.0x |
| 90% | 18.3 | 25.6 | 3.0x |

## Usage

```bash
pip install git+https://github.com/IST-DASLab/sparsegpt.git
python -m sparsegpt.prune \
    --model meta-llama/Llama-2-7b \
    --sparsity 0.5 \
    --nsamples 128
python evaluate.py --model pruned_model --task mmlu
```

## Key Takeaways

1. **One-shot pruning**: Complete in one pass, no iterative training
2. **Error correction**: Uses Hessian information to compensate pruning error
3. **Sparsity control**: Target sparsity determines pruning ratio
4. **vs Magnitude**: SparseGPT significantly outperforms simple magnitude pruning

## Related

- [[entities/awq-quantization]] - Weight quantization methods
- [[entities/self-distillation]] - Knowledge distillation techniques
- [[entities/tensorrt-inference]] - Inference optimization
- [[entities/tech-stacks]] - LLM optimization stack
