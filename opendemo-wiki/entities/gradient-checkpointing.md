---
title: Gradient Checkpointing
summary: Gradient checkpointing trades compute for memory by recomputing activations during backward pass instead of storing all forward pass activations.
updated: 2026-06-05
tags:
  - llm
  - training
  - gradient-checkpointing
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/training/gradient-checkpointing/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Gradient Checkpointing

Gradient checkpointing reduces activation memory by recomputing intermediate activations during backward pass instead of storing them during forward pass.

## Memory vs Compute Tradeoff

| Approach | Memory | Compute |
|----------|--------|---------|
| Standard | O(N) activations | O(1) recompute |
| Checkpointing | O(√N) checkpoints | O(N) recompute |

### 7B Model Example

| Strategy | Activation Memory | Time Overhead |
|----------|-----------------|---------------|
| Standard (30 layers) | ~28GB | 0% |
| Checkpointing (6 checkpoints) | ~4GB | 20-30% |

## PyTorch Implementation

```python
from torch.utils.checkpoint import checkpoint, checkpoint_sequential
import torch.nn as nn

# Method 1: checkpoint wrapper
class ModelWithCheckpoint(nn.Module):
    def forward(self, x):
        x = checkpoint(self.layer1, x)
        x = checkpoint(self.layer2, x)
        x = checkpoint(self.layer3, x)
        return x

# Method 2: checkpoint_sequential
def forward_with_checkpoint(model, input):
    modules = [model.layer1, model.layer2, model.layer3, model.layer4]
    return checkpoint_sequential(modules, 2, input)  # 2 layers per checkpoint
```

### Transformer with Checkpointing

```python
class LMWithCheckpoint(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers, num_heads):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.blocks = nn.ModuleList([
            TransformerBlock(hidden_size, num_heads) 
            for _ in range(num_layers)
        ])
        self.lm_head = nn.Linear(hidden_size, vocab_size)
    
    def forward(self, input_ids):
        x = self.embedding(input_ids)
        for block in self.blocks:
            x = checkpoint(block, x, use_reentrant=True)
        return self.lm_head(x)
```

## Training Commands

```bash
# PyTorch native checkpoint
python train.py --use_checkpoint --checkpoint_ratio 2

# FasterTransformer checkpoint
python train.py --gradient_checkpointing

# DeepSpeed activation checkpointing
deepspeed train.py --deepspeed_config ds_config.json
```

## Key Takeaways

1. **Time-Memory Tradeoff**: Exchange computation for lower memory
2. **Checkpoint Strategy**: Balance checkpoint count and recompute overhead
3. **use_reentrant**: Controls backward pass behavior
4. **Combined Strategies**: Works with mixed precision and parallel strategies

## Related

- [[entities/mixed-precision-training]] — FP16/BF16 memory savings
- [[entities/fsdp-training]] — FSDP with checkpointing
- [[entities/zero-redundancy-optimizer]] — ZeRO combined with checkpointing
