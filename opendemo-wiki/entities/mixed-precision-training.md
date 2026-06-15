---
title: Mixed Precision Training
summary: Mixed precision training uses FP16/BF16 for forward/backward computation while keeping FP32 for optimizer states and master weights.
updated: 2026-06-05
tags:
  - llm
  - training
  - mixed-precision-training
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/training/mixed-precision-training/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Mixed Precision Training

Mixed precision training accelerates computation using FP16/BF16 while maintaining FP32 for optimizer states and master weights to preserve accuracy.

## Precision Formats

| Format | Bits | Range | Stability |
|--------|------|-------|-----------|
| FP32 | 32 | Standard | Highest |
| FP16 | 16 | 5.96e-8 ~ 65504 | Needs loss scale |
| BF16 | 16 | 6.10e-5 ~ 3.40e+38 | Most stable |

BF16 has same exponent bits as FP32 (8 bits) vs FP16 (5 bits), making it much more stable with similar memory savings to FP16.

## Training Flow

1. **Forward Pass**: FP16/BF16 computation, cache activations in FP16
2. **Backward Pass**: FP16 gradients with loss scaling
3. **Optimizer Step**: FP32 master weights and optimizer states

## PyTorch AMP Implementation

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
model = model.cuda()

for batch in dataloader:
    optimizer.zero_grad()
    
    with autocast(dtype=torch.bfloat16):
        outputs = model(batch.cuda())
        loss = compute_loss(outputs, labels.cuda())
    
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    scaler.step(optimizer)
    scaler.update()
```

## Dynamic Loss Scaling

```python
class DynamicLossScaler:
    def __init__(self, init_scale=2**16, scale_factor=2.0, scale_window=1000):
        self.scale = init_scale
        self.scale_factor = scale_factor
        self.scale_window = scale_window
    
    def update_scale(self, overflow):
        if overflow:
            self.scale /= self.scale_factor
            self.unskipped_iterations = 0
        else:
            self.unskipped_iterations += 1
            if self.unskipped_iterations >= self.scale_window:
                self.scale *= self.scale_factor
```

## FP16 vs BF16

| Feature | FP16 | BF16 |
|---------|------|------|
| Overflow Risk | High | Minimal |
| Loss Scale | Required | Not needed |
| Training Stability | Requires tuning | Very stable |
| Speed | Faster | Slightly slower |

## Training Commands

```bash
# PyTorch AMP
python train.py --use_amp --amp_dtype bf16

# NVIDIA Apex
python train.py --fp16 --loss_scale dynamic

# DeepSpeed
deepspeed train.py --deepspeed_config ds_config_fp16.json
```

## Key Takeaways

1. **Precision Selection**: BF16 more stable, FP16 faster
2. **Loss Scale**: Prevent gradient underflow
3. **Mixed Precision**: Compute in low precision, store in high precision
4. **Dynamic Scaling**: Auto-adjust scaling factor

## Related

- [[entities/fsdp-training]] — FSDP with mixed precision
- [[entities/zero-redundancy-optimizer]] — ZeRO with FP16
- [[entities/gradient-checkpointing]] — Combined with activation checkpointing
