---
title: Tensor Parallel Training
summary: Tensor parallelism splits model weight matrices across GPU dimensions using Column/Row parallel strategies with AllReduce communication.
updated: 2026-06-05
tags:
  - llm
  - training
  - tensor-parallel-training
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/training/tensor-parallel-training/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Tensor Parallel Training

Tensor parallelism partitions model weight matrices along certain dimensions across different GPUs. Column parallel splits weights by columns with output concatenation; Row parallel splits by rows with output aggregation.

## Core Concepts

### Tensor Parallel Principle

- **Column Parallel**: Weight split by columns, outputs concatenated
- **Row Parallel**: Weight split by rows, outputs aggregated

### Megatron-LM Sharding Strategy

```python
class ColumnParallelLinear(nn.Module):
    def __init__(self, in_features, out_features, world_size):
        super().__init__()
        self.out_features_per_rank = out_features // world_size
        self.weight = nn.Parameter(
            torch.randn(self.out_features_per_rank, in_features)
        )
    
    def forward(self, x):
        local_output = F.linear(x, self.weight)
        world_size = dist.get_world_size()
        outputs = [torch.zeros_like(local_output) for _ in range(world_size)]
        dist.all_gather(outputs, local_output)
        return torch.cat(outputs, dim=-1)
```

### 3D Parallel Composition

| Parallel Type | Sharding Dimension | Communication |
|---------------|-------------------|---------------|
| Tensor Parallel | Model weights | AllReduce/AllGather |
| Pipeline Parallel | Inter-layer | P2P Send/Recv |
| Data Parallel | Data batch | AllReduce |

## Training Commands

```bash
# Using Megatron-LM
python pretrain_gpt.py \
    --tensor-model-parallel-size 8 \
    --num-layers 32 \
    --hidden-size 4096

# Using DeepSpeed
deepspeed train.py \
    --deepspeed_config ds_config.json \
    --tensor_parallel_size 4
```

## Key Takeaways

1. **Tensor Sharding**: Split model parameters along weight dimensions
2. **Communication**: AllReduce/AllGather for cross-GPU coordination
3. **Communication Overlap**: Hide latency with computation overlap
4. **3D Parallel**: Combine strategies for maximum efficiency

## Related

- [[entities/data-parallel-training]] — Data sharding with complete model copies
- [[entities/zero-redundancy-optimizer]] — Memory optimization via state sharding
- [[entities/fsdp-training]] — Full model parameter sharding
