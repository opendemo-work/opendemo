# 数据并行训练

> 本案例详解数据并行 (Data Parallelism) 原理，演示如何利用多 GPU 加速大模型训练

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    数据并行训练原理                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GPU 0                    GPU 1                    GPU 2       │
│  ┌─────────┐              ┌─────────┐              ┌─────────┐  │
│  │ Model   │              │ Model   │              │ Model   │  │
│  │ Copy    │              │ Copy    │              │ Copy    │  │
│  │ W₀      │              │ W₀      │              │ W₀      │  │
│  └────┬────┘              └────┬────┘              └────┬────┘  │
│       │                        │                        │       │
│       ▼                        ▼                        ▼       │
│  ┌─────────┐              ┌─────────┐              ┌─────────┐  │
│  │ Batch 0 │              │ Batch 1 │              │ Batch 2 │  │
│  │ x₀      │              │ x₁      │              │ x₂      │  │
│  └────┬────┘              └────┬────┘              └────┬────┘  │
│       │                        │                        │       │
│       ▼                        ▼                        ▼       │
│  ┌─────────┐              ┌─────────┐              ┌─────────┐  │
│  │ Forward │              │ Forward │              │ Forward │  │
│  │ Loss 0  │              │ Loss 1  │              │ Loss 2  │  │
│  └────┬────┘              └────┬────┘              └────┬────┘  │
│       │                        │                        │       │
│       └────────────────────────┼────────────────────────┘       │
│                                ▼                                 │
│                    ┌─────────────────────┐                       │
│                    │  Gradient AllReduce │                       │
│                    │  (求平均)           │                       │
│                    └──────────┬──────────┘                       │
│                               ▼                                   │
│                    ┌─────────────────────┐                       │
│                    │  Optimizer Step    │                       │
│                    │  (同步更新)         │                       │
│                    └─────────────────────┘                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心概念

### 1. 数据并行原理

数据并行将训练数据划分为多个 micro-batch，每个 GPU 持有完整模型副本：

- 每个 GPU 计算本地梯度
- 所有 GPU 通信聚合梯度 (AllReduce)
- 聚合后同步更新模型参数

### 2. PyTorch DDP 实现

```python
import torch
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.distributed as dist

def setup_ddp():
    """初始化分布式训练环境"""
    dist.init_process_group(backend="nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    return local_rank

def train_ddp(model, train_loader):
    """DDP 训练循环"""
    local_rank = setup_ddp()
    
    # 包装模型
    model = model.cuda()
    model = DDP(model, device_ids=[local_rank])
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    model.train()
    for batch in train_loader:
        inputs, labels = batch.cuda(), batch.cuda()
        
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        
        # DDP 自动处理梯度同步
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
```

### 3. 通信策略

| 策略 | 通信量 | 适用场景 |
|------|--------|----------|
| AllReduce | O(N) | 通用 |
| ReduceScatter | O(N) | 优化器状态分区 |
| Bucket AllReduce | 批量通信 | 减少通信开销 |

## 完整训练脚本

```python
import os
import torch
import torch.nn as nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler

def main():
    # 初始化
    dist.init_process_group(backend="nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    
    # 模型
    model = build_model().cuda()
    model = DDP(model, device_ids=[local_rank])
    
    # 数据
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    loader = DataLoader(dataset, batch_size=32, sampler=sampler)
    
    # 训练
    for epoch in range(num_epochs):
        sampler.set_epoch(epoch)
        for batch in loader:
            outputs = model(batch.cuda())
            loss = compute_loss(outputs, batch.labels.cuda())
            
            loss.backward()
            
            # Optimizer step 和梯度同步由 DDP 自动处理
            optimizer.step()
            optimizer.zero_grad()
    
    dist.destroy_process_group()

if __name__ == "__main__":
    # 启动命令: torchrun --nproc_per_node=4 train.py
    main()
```

## 命令速查

```bash
# 单机多卡 (DDP)
torchrun --nproc_per_node=4 train.py

# 多机多卡
torchrun --nnodes=2 --nproc_per_node=4 --rdzv_id=123 --rdzv_backend=c10d train.py

# 查看 NCCL 调试信息
NCCL_DEBUG=INFO python train.py
```

## 学习要点

1. **数据并行**：每个 GPU 持有完整模型，数据分片
2. **梯度同步**：AllReduce 聚合所有 GPU 的梯度
3. **同步更新**：所有 GPU 使用相同的聚合梯度更新
4. **通信效率**：选择合适的通信后端和策略
