<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# FSDP 完全分片数据并行

> 本案例详解 FSDP (Fully Sharded Data Parallel) 原理，演示 PyTorch 原生大模型训练方案

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    FSDP 原理                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FSDP 分片策略:                                                  │
│                                                                 │
│  GPU 0                    GPU 1                    GPU 2          │
│  ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
│  │ Sharded Model  │      │ Sharded Model  │      │ Sharded Model  │
│  │                │      │                │      │                │
│  │ Layer 0: P0    │      │ Layer 0: P1    │      │ Layer 0: P2    │
│  │ Layer 1: P2    │      │ Layer 1: P0    │      │ Layer 1: P1    │
│  │ Layer 2: P1    │      │ Layer 2: P2    │      │ Layer 2: P0    │
│  └────────────────┘      └────────────────┘      └────────────────┘
│                                                                 │
│  Forward Pass:                                                  │
│                                                                 │
│  Step 1: all_gather(Layer 0) → 计算 → discard                  │
│  Step 2: all_gather(Layer 1) → 计算 → discard                   │
│  Step 3: all_gather(Layer 2) → 计算 → discard                   │
│                                                                 │
│  Backward Pass:                                                 │
│                                                                 │
│  Step 1: all_gather(Grad Layer 2) → backward → scatter        │
│  Step 2: all_gather(Grad Layer 1) → backward → scatter           │
│  Step 3: all_gather(Grad Layer 0) → backward → scatter          │
│                                                                 │
│  vs DDP:                                                        │
│  ┌─────────────────────────────────────────────────────────────┐
│  │ DDP: 每个 GPU 存储完整 FP32 模型副本                         │
│  │ 7B 模型: ~28GB/GPU (仅参数)                                  │
│  │                                                             │
│  │ FSDP: 8 GPU 分片，每个只存 1/8 参数                           │
│  │ 7B 模型: ~3.5GB/GPU (仅参数)                                │
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心概念

### 1. FSDP vs DDP

| 特性 | DDP | FSDP |
|------|-----|------|
| 模型存储 | 完整副本 | 分片副本 |
| 梯度同步 | AllReduce | AllGather + 本地反向 |
| 通信量 | O(model_size) | O(shard_size × num_layers) |
| 内存效率 | O(model_size) | O(model_size / world_size) |

### 2. PyTorch FSDP 实现

```python
import torch
import torch.nn as nn
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP,
    ShardingStrategy,
    MixedPrecision,
    BackwardPrefetch,
    CPUOffload
)
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy

def setup_fsdp():
    """初始化 FSDP"""
    torch.distributed.init_process_group(backend="nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    return local_rank

# 混合精度策略
mixed_precision_policy = MixedPrecision(
    param_dtype=torch.float16,
    reduce_dtype=torch.float16,
    buffer_dtype=torch.float16,
    keep_low_precision_grads=True
)

# CPU Offload
cpu_offload = CPUOffload(offload_params=True)

def create_fsdp_model(model):
    """创建 FSDP 模型"""
    fsdp_model = FSDP(
        model,
        sharding_strategy=ShardingStrategy.FULL_SHARD,
        auto_wrap_policy=transformer_auto_wrap_policy,
        mixed_precision=mixed_precision_policy,
        cpu_offload=cpu_offload,
        backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
        use_orig_params=True
    )
    return fsdp_model
```

### 3. 完整训练脚本

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import ShardingStrategy
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
import torch.nn as nn

def train_fsdp():
    dist.init_process_group(backend="nccl")
    rank = int(os.environ["LOCAL_RANK"])
    world_size = dist.get_world_size()
    
    # 创建模型
    model = build_transformer_model()
    
    # FSDP 包装
    model = FSDP(
        model,
        sharding_strategy=ShardingStrategy.FULL_SHARD,
        auto_wrap_policy=transformer_auto_wrap_policy,
        mixed_precision=MixedPrecision(
            param_dtype=torch.bfloat16,
            reduce_dtype=torch.bfloat16,
        ),
        device_id=torch.cuda.current_device(),
        use_orig_params=True
    )
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    for batch in dataloader:
        optimizer.zero_grad()
        
        # FSDP 自动处理 all_gather 和分片
        output = model(batch.cuda())
        loss = compute_loss(output, labels.cuda())
        
        # 异步 reduce 梯度
        loss.backward()
        
        # FSDP 自动处理梯度分片
        optimizer.step()
    
    return model
```

## 命令速查

```bash
# 启动 FSDP 训练
torchrun --nproc_per_node=8 train_fsdp.py

# CPU Offload
torchrun --nproc_per_node=4 train_fsdp.py --cpu_offload

# 混合精度
torchrun --nproc_per_node=4 train_fsdp.py --mixed_precision
```

## 学习要点

1. **模型分片**：每个 GPU 只存储部分参数
2. **动态 AllGather**：需要参数时才拉取
3. **内存通信 trade-off**：用通信换内存
4. **CPU Offload**：进一步降低 GPU 内存

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 AI/ML 核心概念。

### 2. 适用场景

- 场景 1：学术研究
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
python code/main.py
```
