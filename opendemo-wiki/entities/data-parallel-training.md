---
title: Data Parallel Training
summary: Data parallelism training distributes data across GPUs while keeping complete model copies, using AllReduce to synchronize gradients.
updated: 2026-06-05
tags:
  - llm
  - training
  - data-parallel-training
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/training/data-parallel-training/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Data Parallel Training

Data parallelism splits training data into micro-batches while each GPU holds a complete model copy. After local gradient computation, all GPUs communicate via AllReduce to aggregate gradients and synchronously update parameters.

## Core Concepts

### Data Parallel Principle

- Each GPU computes local gradients
- All GPUs communicate to aggregate gradients (AllReduce)
- After aggregation, all GPUs update model parameters synchronously

### PyTorch DDP Implementation

```python
import torch
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.distributed as dist

def setup_ddp():
    dist.init_process_group(backend="nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    return local_rank

def train_ddp(model, train_loader):
    local_rank = setup_ddp()
    model = model.cuda()
    model = DDP(model, device_ids=[local_rank])
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    model.train()
    for batch in train_loader:
        inputs, labels = batch.cuda(), batch.cuda()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
```

### Communication Strategies

| Strategy | Communication | Use Case |
|----------|---------------|----------|
| AllReduce | O(N) | General |
| ReduceScatter | O(N) | Optimizer state partitioning |
| Bucket AllReduce | Batch | Reduce communication overhead |

## Training Commands

```bash
# Single-node multi-GPU (DDP)
torchrun --nproc_per_node=4 train.py

# Multi-node multi-GPU
torchrun --nnodes=2 --nproc_per_node=4 --rdzv_id=123 --rdzv_backend=c10d train.py
```

## Key Takeaways

1. **Data Parallel**: Each GPU holds complete model, data sharded
2. **Gradient Sync**: AllReduce aggregates gradients from all GPUs
3. **Synchronous Update**: All GPUs use same aggregated gradients
4. **Communication Efficiency**: Choose appropriate backend and strategy

## Related

- [[entities/tensor-parallel-training]] — Model weight sharding across GPUs
- [[entities/zero-redundancy-optimizer]] — Memory optimization via state sharding
- [[entities/fsdp-training]] — PyTorch native full model sharding
