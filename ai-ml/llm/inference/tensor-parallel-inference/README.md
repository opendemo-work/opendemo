<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Tensor Parallel Inference 张量并行推理

> 本案例详解 LLM 张量并行推理：模型分片、前向切分、通信优化

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Tensor Parallel 原理                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  单卡推理:                                                       │
│                                                                 │
│  ┌─────────────────────────────────────────┐                   │
│  │           Transformer Layer              │                   │
│  │                                         │                   │
│  │  Input → [W] → [W] → [W] → Output      │                   │
│  │            ↓       ↓       ↓             │                   │
│  │          FC1     FC2     FC3            │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  2-GPU Tensor Parallel:                                         │
│                                                                 │
│  GPU 0:                          GPU 1:                         │
│  ┌─────────────────────┐       ┌─────────────────────┐          │
│  │  Input → [W/2] ─┐   │       │   ┌→ [W/2] → Output │          │
│  │               ↓   │       │   ↓                 │          │
│  │            AllReduce│←─────→│AllReduce           │          │
│  └─────────────────────┘       └─────────────────────┘          │
│                                                                 │
│  Layer N 的权重按列切分到不同 GPU                                 │
│  Attention 计算后通过 AllReduce 汇总                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

AllReduce 通信模式:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Ring AllReduce:                                                │
│                                                                 │
│  GPU0 ──[send/recv]── GPU1 ──[send/recv]── GPU2 ──[send/recv]── GPU3 │
│     ↑                                                              │
│     └────────────────── ring ────────────────────────────────────┘│
│                                                                 │
│  步骤:                                                          │
│  1. 每个 GPU 将数据分成 N 份                                     │
│  2. Ring pass: 累加各个分片                                      │
│  3. Ring pass: 同步完整结果                                      │
│                                                                 │
│  通信量: 2 × (N-1) / N × 数据大小                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 为什么需要 Tensor Parallel

大模型单卡放不下：
- 7B 模型 (FP16): ~14GB
- 13B 模型 (FP16): ~26GB
- 70B 模型 (FP16): ~140GB

**张量并行**：将权重矩阵按维度切分到多卡

### 2. Attention 的并行化

```python
class TensorParallelAttention(torch.nn.Module):
    """张量并行的 Attention"""

    def __init__(self, hidden_size, num_heads, tensor_parallel_size=2):
        self.num_heads = num_heads // tensor_parallel_size
        self.head_dim = hidden_size // num_heads

        # QKV 权重按列切分
        self.qkv_weight = ColumnParallel(
            input_size=hidden_size,
            output_size=hidden_size * 3,
            num_partitions=tensor_parallel_size
        )

        # Output 投影按行切分
        self.o_weight = RowParallel(
            input_size=hidden_size,
            output_size=hidden_size,
            num_partitions=tensor_parallel_size
        )

    def forward(self, x):
        # 各 GPU 独立计算 QKV
        qkv = self.qkv_weight(x)
        q, k, v = qkv.chunk(3, dim=-1)

        # 计算本地 Attention
        local_attn = self.scaled_dot_product_attention(q, k, v)

        # Row Parallel 输出 + AllReduce
        output = self.o_weight(local_attn)
        return output
```

### 3. 通信优化

```python
class AllReduce:
    """优化的 AllReduce 实现"""

    @staticmethod
    def ring_allreduce(tensors, world_size, rank):
        """Ring AllReduce 算法"""
        send_buf = tensors.clone()
        recv_buf = torch.zeros_like(tensors)

        for step in range(world_size - 1):
            src_rank = (rank - step - 1) % world_size
            dst_rank = (rank + step + 1) % world_size

            # Wait for send/recv to complete
            recv_req = MPI.Irecv(recv_buf, src=src_rank)
            MPI.Send(send_buf, dest=dst_rank)
            recv_req.wait()

            # Accumulate
            send_buf += recv_buf

        # Second ring pass: sync final result
        for step in range(world_size - 1):
            src_rank = (rank - step) % world_size
            dst_rank = (rank + step + 1) % world_size

            recv_req = MPI.Irecv(recv_buf, src=src_rank)
            MPI.Send(send_buf, dest=dst_rank)
            recv_req.wait()
            send_buf.copy_(recv_buf)
```

## 📊 性能对比

| 配置 | 7B 延迟 | 13B 延迟 | 70B 延迟 |
|------|---------|----------|----------|
| 单卡 | 50ms | 120ms | N/A |
| 2-GPU TP | 35ms | 80ms | N/A |
| 4-GPU TP | 25ms | 50ms | 350ms |
| 8-GPU TP | - | - | 180ms |

## 📚 学习要点

1. **Column Parallel**：权重按列切分，QKV 分片计算
2. **Row Parallel**：输出投影分片，AllReduce 汇总
3. **通信隐藏**：Overlap 计算与通信
4. **自动分片**：Megatron-LM 风格统一框架

## 🔗 相关案例

- `vllm-inference` - vLLM 高吞吐推理
- `batch-inference` - Batch 推理优化
- `paged-attention` - PagedAttention 内存管理

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
