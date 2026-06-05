# ZeRO 优化器

> 本案例详解 ZeRO (Zero Redundancy Optimizer) 原理，演示如何通过分片消除训练冗余

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    ZeRO 优化器原理                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  传统 DDP: 每个 GPU 存储完整副本                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │ Optimizer│  │ Optimizer│  │ Optimizer│                       │
│  │ States   │  │ States   │  │ States   │                       │
│  │ Gradients│  │ Gradients│  │ Gradients│                       │
│  │ Parameters│ │ Parameters│ │ Parameters│                       │
│  └──────────┘  └──────────┘  └──────────┘                       │
│                                                                 │
│  ZeRO Stage 1: 优化器状态分片                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │ Optimizer│  │ Optimizer│  │ Optimizer│                       │
│  │ States 0 │  │ States 1 │  │ States 2 │                       │
│  ├──────────┤  ├──────────┤  ├──────────┤                       │
│  │ Gradients│  │ Gradients│  │ Gradients│                       │
│  │ Parameters│ │ Parameters│ │ Parameters│                       │
│  └──────────┘  └──────────┘  └──────────┘                       │
│                                                                 │
│  ZeRO Stage 2: 梯度分片                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │ Optimizer│  │ Optimizer│  │ Optimizer│                       │
│  │ States   │  │ States   │  │ States   │                       │
│  ├──────────┤  ├──────────┤  ├──────────┤                       │
│  │ Grad 0   │  │ Grad 1   │  │ Grad 2   │                       │
│  │ Parameters│ │ Parameters│ │ Parameters│                       │
│  └──────────┘  └──────────┘  └──────────┘                       │
│                                                                 │
│  ZeRO Stage 3: 参数分片                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │ Optimizer│  │ Optimizer│  │ Optimizer│                       │
│  │ States   │  │ States   │  │ States   │                       │
│  ├──────────┤  ├──────────┤  ├──────────┤                       │
│  │ Gradients│  │ Gradients│  │ Gradients│                       │
│  ├──────────┤  ├──────────┤  ├──────────┤                       │
│  │ Params 0 │  │ Params 1 │  │ Params 2 │                       │
│  └──────────┘  └──────────┘  └──────────┘                       │
│                                                                 │
│  内存对比 (7B 模型, 8 GPUs):                                      │
│                                                                 │
│  DDP:  28GB × 8 = 224GB (总)                                    │
│  ZeRO-1: 28GB × 1 + 优化器分片                                   │
│  ZeRO-2: ~16GB/GPU                                               │
│  ZeRO-3: ~2GB/GPU                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心概念

### 1. ZeRO 原理

ZeRO 通过划分优化器状态、梯度、参数来消除数据并行中的内存冗余：

- **ZeRO-1**: 分片优化器状态 (Adam moments)
- **ZeRO-2**: 分片优化器状态 + 梯度
- **ZeRO-3**: 分片所有状态 + 参数

### 2. DeepSpeed 实现

```python
# ds_config.json
{
    "zero_optimization": {
        "stage": 3,
        "offload_optimizer": {
            "device": "cpu",
            "pin_memory": true
        },
        "offload_param": {
            "device": "cpu",
            "pin_memory": true
        },
        "overlap_comm": true,
        "contiguous_gradients": true,
        "sub_group_size": 1e9
    },
    "fp16": {
        "enabled": true,
        "loss_scale": 0,
        "loss_scale_window": 1000
    }
}
```

### 3. ZeRO 通信量

| Stage | 通信量 | 内存节省 |
|-------|--------|----------|
| ZeRO-1 | 1.5x AllReduce | ~4x |
| ZeRO-2 | 1.5x AllReduce | ~8x |
| ZeRO-3 | 2x AllReduce + P2P | ~8x per rank |

## 完整训练脚本

```python
import deepspeed

deepspeed.init_distributed()

model, optimizer, train_loader, _ = setup_model()

# DeepSpeed 配置
ds_config = {
    "train_batch_size": 32,
    "gradient_accumulation_steps": 4,
    "zero_optimization": {
        "stage": 3,
        "offload_optimizer": {"device": "cpu"},
        "offload_param": {"device": "cpu"},
        "overlap_comm": True,
        "contiguous_gradients": True
    },
    "fp16": {"enabled": True}
}

# 包装模型
model, optimizer, _, _ = deepspeed.initialize(
    model=model,
    optimizer=optimizer,
    config=ds_config,
    training_data=train_loader
)

for batch in train_loader:
    model.zero_grad()
    loss = model(batch)
    model.step(loss)
```

## 命令速查

```bash
# 启动 DeepSpeed ZeRO-3
deepspeed train.py \
    --deepspeed_config ds_config.json \
    --local_rank 0

# 监控 ZeRO 内存
deepspeed --monitor memory train.py
```

## 学习要点

1. **状态分片**：消除优化器状态冗余
2. **梯度分片**：减少梯度内存占用
3. **参数分片**：实现真正单 GPU 可加载大模型
4. **通信优化**：Overlap 通信与计算
