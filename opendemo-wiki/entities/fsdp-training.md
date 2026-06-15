---
title: FSDP Training
summary: Fully Sharded Data Parallel shards model parameters across GPUs, using dynamic AllGather for computation with communication-for-memory tradeoff.
updated: 2026-06-05
tags:
  - llm
  - training
  - fsdp-training
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/training/fsdp-training/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# FSDP Training

Fully Sharded Data Parallel (FSDP) shards model parameters across GPUs, fetching only needed parameters via AllGather during computation.

## FSDP vs DDP

| Feature | DDP | FSDP |
|---------|-----|------|
| Model Storage | Full replica | Sharded |
| Gradient Sync | AllReduce | AllGather + local backward |
| Communication | O(model_size) | O(shard_size × num_layers) |
| Memory | O(model_size) | O(model_size / world_size) |

### Memory Example (7B Model)

| Strategy | Memory |
|----------|--------|
| DDP | ~28GB/GPU |
| FSDP (8 GPUs) | ~3.5GB/GPU |

## PyTorch FSDP Implementation

```python
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP,
    ShardingStrategy,
    MixedPrecision,
    BackwardPrefetch,
    CPUOffload
)
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy

mixed_precision_policy = MixedPrecision(
    param_dtype=torch.float16,
    reduce_dtype=torch.float16,
    buffer_dtype=torch.float16,
    keep_low_precision_grads=True
)

def create_fsdp_model(model):
    fsdp_model = FSDP(
        model,
        sharding_strategy=ShardingStrategy.FULL_SHARD,
        auto_wrap_policy=transformer_auto_wrap_policy,
        mixed_precision=mixed_precision_policy,
        cpu_offload=CPUOffload(offload_params=True),
        backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
        use_orig_params=True
    )
    return fsdp_model
```

### Training Loop

```python
def train_fsdp():
    dist.init_process_group(backend="nccl")
    rank = int(os.environ["LOCAL_RANK"])
    
    model = build_transformer_model()
    model = FSDP(
        model,
        sharding_strategy=ShardingStrategy.FULL_SHARD,
        auto_wrap_policy=transformer_auto_wrap_policy,
        mixed_precision=MixedPrecision(param_dtype=torch.bfloat16),
        device_id=torch.cuda.current_device()
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    for batch in dataloader:
        optimizer.zero_grad()
        output = model(batch.cuda())
        loss = compute_loss(output, labels.cuda())
        loss.backward()
        optimizer.step()
```

## Training Commands

```bash
# Basic FSDP
torchrun --nproc_per_node=8 train_fsdp.py

# With CPU Offload
torchrun --nproc_per_node=4 train_fsdp.py --cpu_offload

# With Mixed Precision
torchrun --nproc_per_node=4 train_fsdp.py --mixed_precision
```

## Key Takeaways

1. **Model Sharding**: Each GPU stores only portion of parameters
2. **Dynamic AllGather**: Fetch parameters only when needed
3. **Communication-Memory Tradeoff**: Exchange communication for memory
4. **CPU Offload**: Further reduce GPU memory

## Related

- [[entities/data-parallel-training]] — DDP with full model replicas
- [[entities/zero-redundancy-optimizer]] — Memory optimization via state sharding
- [[entities/mixed-precision-training]] — FP16/BF16 memory savings
- [[entities/gradient-checkpointing]] — Activation memory optimization
