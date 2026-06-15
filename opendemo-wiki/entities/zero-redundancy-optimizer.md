---
title: Zero Redundancy Optimizer (ZeRO)
summary: ZeRO eliminates training redundancy by sharding optimizer states, gradients, and parameters across GPUs to reduce memory footprint.
updated: 2026-06-05
tags:
  - llm
  - training
  - zero-redundancy-optimizer
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/training/zero-redundancy-optimizer/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Zero Redundancy Optimizer (ZeRO)

ZeRO eliminates memory redundancy in data parallelism by partitioning optimizer states, gradients, and parameters across GPUs.

## ZeRO Stages

| Stage | Partition | Memory Savings |
|-------|-----------|----------------|
| ZeRO-1 | Optimizer states only | ~4x |
| ZeRO-2 | Optimizer states + gradients | ~8x |
| ZeRO-3 | All states + parameters | ~8x per rank |

### ZeRO-1: Optimizer State Sharding
Each GPU stores only a partition of optimizer states (Adam moments).

### ZeRO-2: Gradient Sharding
Adds gradient partitioning to optimizer state partitioning.

### ZeRO-3: Parameter Sharding
Full partitioning including model parameters, enabling true single-GPU large model loading.

### Memory Comparison (7B Model, 8 GPUs)

| Strategy | Memory |
|----------|--------|
| DDP | 28GB × 8 = 224GB total |
| ZeRO-1 | 28GB × 1 + partitioned optimizer |
| ZeRO-2 | ~16GB/GPU |
| ZeRO-3 | ~2GB/GPU |

## DeepSpeed Implementation

```json
{
    "zero_optimization": {
        "stage": 3,
        "offload_optimizer": {"device": "cpu", "pin_memory": true},
        "offload_param": {"device": "cpu", "pin_memory": true},
        "overlap_comm": true,
        "contiguous_gradients": true
    },
    "fp16": {"enabled": true, "loss_scale": 0}
}
```

```python
import deepspeed

deepspeed.init_distributed()
ds_config = {
    "train_batch_size": 32,
    "gradient_accumulation_steps": 4,
    "zero_optimization": {"stage": 3, "offload_optimizer": {"device": "cpu"}},
    "fp16": {"enabled": True}
}
model, optimizer, _, _ = deepspeed.initialize(model=model, optimizer=optimizer, config=ds_config)
```

## Communication Overhead

| Stage | Communication | Overhead |
|-------|--------------|----------|
| ZeRO-1 | 1.5x AllReduce | ~4x memory |
| ZeRO-2 | 1.5x AllReduce | ~8x memory |
| ZeRO-3 | 2x AllReduce + P2P | ~8x memory per rank |

## Key Takeaways

1. **State Sharding**: Eliminate optimizer state redundancy
2. **Gradient Sharding**: Reduce gradient memory footprint
3. **Parameter Sharding**: Enable true single-GPU large model loading
4. **Communication Optimization**: Overlap communication with computation

## Related

- [[entities/data-parallel-training]] — Basic data parallelism
- [[entities/tensor-parallel-training]] — Model weight partitioning
- [[entities/fsdp-training]] — PyTorch native full sharding
- [[entities/mixed-precision-training]] — FP16/BF16 for memory efficiency
