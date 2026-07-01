<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 张量并行训练

> 本案例详解张量并行 (Tensor Parallelism) 原理，演示如何将大模型权重分片到多 GPU

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    张量并行训练原理                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  单层 transformer: Y = LayerNorm(Attention(X))                  │
│                                                                 │
│  矩阵乘法分片示例 (Column Parallel):                              │
│                                                                 │
│  X (batch, seq, hidden)                                         │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                               │
│  │  Column     │                                               │
│  │  Parallel   │                                               │
│  │  Linear     │                                               │
│  │  W: [h, h/n]│  W: [h, h/n]  W: [h, h/n]                     │
│  └──────┬──────┘                                               │
│         │ Y0           Y1           Y2                           │
│         ▼                                                         │
│  ┌─────────────────────────────────────────────┐               │
│  │           All-Gather / Reduce-Scatter        │               │
│  └─────────────────────────────────────────────┘               │
│                                                                 │
│  Attention 张量并行:                                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │   Q = X @ W_Q     K = X @ W_K     V = X @ W_V            │  │
│  │      │                │                │                   │  │
│  │      ▼                ▼                ▼                   │  │
│  │   [h/n]            [h/n]            [h/n]                  │  │
│  │                                                           │  │
│  │   Q @ K^T → Softmax → Attention @ V                      │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心概念

### 1. 张量并行原理

张量并行将模型权重矩阵沿某个维度切分到不同 GPU：

- **Column Parallel**: 权重按列切分，输出拼接
- **Row Parallel**: 权重按行切分，输出聚合

### 2. Megatron-LM 分片策略

```python
class ColumnParallelLinear(nn.Module):
    """列并行线性层"""
    def __init__(self, in_features, out_features, world_size):
        super().__init__()
        self.in_features = in_features
        self.out_features_per_rank = out_features // world_size
        
        # 权重按列切分
        self.weight = nn.Parameter(
            torch.randn(self.out_features_per_rank, in_features)
        )
    
    def forward(self, x):
        # 本地计算
        local_output = F.linear(x, self.weight)
        
        # All-Gather 收集所有输出
        world_size = dist.get_world_size()
        outputs = [torch.zeros_like(local_output) for _ in range(world_size)]
        dist.all_gather(outputs, local_output)
        return torch.cat(outputs, dim=-1)
```

### 3. 3D 并行组合

| 并行方式 | 分片维度 | 通信模式 |
|----------|----------|----------|
| Tensor Parallel | 模型权重 | AllReduce/AllGather |
| Pipeline Parallel | 层间 | P2P Send/Recv |
| Data Parallel | 数据批次 | AllReduce |

## 完整实现

```python
import torch
import torch.nn as nn
import torch.distributed as dist
import torch.nn.functional as F

class TensorParallelModel(nn.Module):
    """简化的张量并行模型"""
    def __init__(self, vocab_size, hidden_size, num_heads, world_size):
        super().__init__()
        self.world_size = world_size
        
        # 词嵌入分片
        self.embed = VocabEmbedding(vocab_size, hidden_size, world_size)
        
        # Transformer 层
        self.layers = nn.ModuleList([
            TransformerLayer(hidden_size, num_heads, world_size)
            for _ in range(num_layers)
        ])
        
        # 输出层
        self.lm_head = ColumnParallelLinear(
            hidden_size, vocab_size, world_size
        )
    
    def forward(self, input_ids):
        # 词嵌入
        x = self.embed(input_ids)
        
        # Transformer 层
        for layer in self.layers:
            x = layer(x)
        
        # 预测
        logits = self.lm_head(x)
        return logits

def train_tensor_parallel():
    """张量并行训练"""
    dist.init_process_group(backend="nccl")
    rank = dist.get_rank()
    world_size = dist.get_world_size()
    
    model = TensorParallelModel(vocab_size, hidden_size, num_heads, world_size)
    model = model.cuda()
    
    # 使用 timer 切分权重
    partition_model(model, world_size, rank)
    
    for batch in dataloader:
        outputs = model(batch.cuda())
        loss = compute_loss(outputs, labels.cuda())
        loss.backward()
        optimizer.step()
```

## 命令速查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用 Megatron-LM
python pretrain_gpt.py \
    --tensor-model-parallel-size 8 \
    --num-layers 32 \
    --hidden-size 4096

# 使用 DeepSpeed
deepspeed train.py \
    --deepspeed_config ds_config.json \
    --tensor_parallel_size 4
```

## 学习要点

1. **张量分片**：沿权重维度切分模型参数
2. **通信模式**：AllReduce/AllGather 实现跨 GPU 协同
3. **通信 overlap**：与计算重叠隐藏延迟
4. **3D 并行**：结合多种并行策略最大化效率

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
python code/main.py
```
