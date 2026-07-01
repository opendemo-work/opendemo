<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Transformer 从零实现

> 本案例从零实现 Transformer 架构，深入理解注意力机制、位置编码、前馈网络等核心组件

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      Transformer Encoder                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input Embedding                                                │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                                │
│  │ Positional  │                                                │
│  │  Encoding   │                                                │
│  └─────────────┘                                                │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Multi-Head Attention                   │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │   │
│  │  │  Head 1 │  │  Head 2 │  │  Head h │                  │   │
│  │  └─────────┘  └─────────┘  └─────────┘                  │   │
│  │        │            │            │                       │   │
│  │        └────────────┼────────────┘                       │   │
│  │                     ▼                                    │   │
│  │              Linear Projection                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         │                                      │
│                         ▼                                      │
│                  ┌────────────┐                                │
│                  │   Add &    │                                │
│                  │   Norm     │                                │
│                  └────────────┘                                │
│                         │                                      │
│                         ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Feed Forward                          │   │
│  │              (Linear → ReLU → Linear)                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         │                                      │
│                         ▼                                      │
│                  ┌────────────┐                                │
│                  │   Add &    │                                │
│                  │   Norm     │                                │
│                  └────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. Self-Attention 机制

Self-Attention 允许序列中的每个位置关注序列中的所有其他位置：

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

**关键特性：**
- 并行计算，无 RNN 依赖
- 捕捉长距离依赖关系
- 可学习的注意力权重

### 2. Multi-Head Attention

将注意力分成多个头，分别学习不同的表示子空间：

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) × W_O

where head_i = Attention(QW_Q^i, KW_K^i, VW_V^i)
```

### 3. 位置编码

Transformer 本身不包含位置信息，需要通过位置编码注入：

- **Sinusoidal 编码**：基于正弦余弦函数
- **Rotary 编码 (RoPE)**：旋转矩阵形式
- **ALiBi 编码**：无需学习的偏置

### 4. Feed Forward Network

每个 Transformer 层包含前馈网络：

```
FFN(x) = max(0, xW_1 + b_1) × W_2 + b_2
```

## 💻 完整实现

### 核心代码结构

```python
import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    """Multi-Head Attention 实现"""
    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)

        self.dropout = nn.Dropout(dropout)

    def split_heads(self, x):
        """将隐藏维度分割成多个头"""
        batch_size, seq_len, _ = x.size()
        x = x.view(batch_size, seq_len, self.num_heads, self.d_k)
        return x.permute(0, 2, 1, 3)

    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)

        # 线性投影并分割头
        Q = self.split_heads(self.W_Q(Q))
        K = self.split_heads(self.W_K(K))
        V = self.split_heads(self.W_V(V))

        # 注意力计算
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)

        # 注意力加权求和
        context = torch.matmul(attention_weights, V)

        # 合并多头
        context = context.permute(0, 2, 1, 3).contiguous()
        context = context.view(batch_size, -1, self.d_model)

        return self.W_O(context)


class PositionwiseFeedForward(nn.Module):
    """Position-wise Feed Forward Network"""
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.w_2(self.dropout(F.relu(self.w_1(x))))


class TransformerEncoderLayer(nn.Module):
    """Transformer Encoder 单层"""
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = PositionwiseFeedForward(d_model, d_ff, dropout)

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # Self-Attention + 残差连接
        attn_output = self.self_attn(x, x, x, mask)
        x = self.norm1(x + self.dropout1(attn_output))

        # Feed Forward + 残差连接
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout2(ff_output))

        return x


class TransformerEncoder(nn.Module):
    """完整的 Transformer Encoder"""
    def __init__(self, num_layers, d_model, num_heads, d_ff, vocab_size, dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_embedding = PositionalEncoding(d_model, dropout)

        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])

        self.output_projection = nn.Linear(d_model, vocab_size)

    def forward(self, x, mask=None):
        x = self.embedding(x) * math.sqrt(self.d_model)
        x = self.pos_embedding(x)

        for layer in self.layers:
            x = layer(x, mask)

        return self.output_projection(x)


class PositionalEncoding(nn.Module):
    """位置编码"""
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)

        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)
```

### 完整训练示例

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

def train_transformer():
    """训练 Transformer 示例"""
    # 超参数
    VOCAB_SIZE = 10000
    D_MODEL = 512
    NUM_HEADS = 8
    D_FF = 2048
    NUM_LAYERS = 6
    DROPOUT = 0.1

    # 模型初始化
    model = TransformerEncoder(
        num_layers=NUM_LAYERS,
        d_model=D_MODEL,
        num_heads=NUM_HEADS,
        d_ff=D_FF,
        vocab_size=VOCAB_SIZE,
        dropout=DROPOUT
    )

    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    # 训练循环
    model.train()
    for epoch in range(10):
        total_loss = 0
        for batch in train_dataloader:
            inputs, targets = batch

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs.view(-1, VOCAB_SIZE), targets.view(-1))
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_dataloader):.4f}")

    return model


def inference_example(model, input_sequence):
    """推理示例"""
    model.eval()
    with torch.no_grad():
        input_tensor = torch.tensor([input_sequence])
        output = model(input_tensor)
        predictions = output.argmax(dim=-1)
    return predictions
```

## 📊 复杂度分析

### 时间复杂度

| 组件 | 复杂度 | 说明 |
|------|--------|------|
| Self-Attention | O(n² × d) | 序列长度 n 的二次方 |
| Multi-Head | O(n² × d × h) | h 为头数 |
| Feed Forward | O(n × d × d_ff) | 线性扩展 |

### 空间复杂度

| 组件 | 复杂度 | 说明 |
|------|--------|------|
| Attention Weights | O(n² × h) | 注意力矩阵存储 |
| KV Cache | O(n × d × L) | L 为层数 |
| 模型参数 | O(d²) | 权重矩阵 |

## 🧪 实践练习

### 练习 1: 实现因果注意力 (Causal Attention)

```python
def create_causal_mask(seq_len):
    """创建下三角注意力掩码"""
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)
    return mask.masked_fill(mask == 1, float('-inf'))
```

### 练习 2: 实现 Flash Attention 简化版

```python
def flash_attention_simplified(Q, K, V, block_size=64):
    """Flash Attention 简化实现"""
    batch_size, num_heads, seq_len, d_k = Q.shape

    output = torch.zeros_like(Q)

    for i in range(0, seq_len, block_size):
        Q_block = Q[:, :, i:i+block_size, :]
        scores_block = torch.matmul(Q_block, K.transpose(-2, -1)) / math.sqrt(d_k)
        scores_block = F.softmax(scores_block, dim=-1)
        output[:, :, i:i+block_size, :] = torch.matmul(scores_block, V)

    return output
```

## 📋 命令速查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 运行训练示例
python transformer_scratch/train.py

# 运行单元测试
python -m pytest transformer_scratch/tests/

# 导出 ONNX 模型
python transformer_scratch/export_onnx.py

# Benchmark 性能测试
python transformer_scratch/benchmark.py
```

## 📚 学习要点

1. **注意力机制本质**：通过 QKV 变换实现序列内信息的全局交互
2. **多头注意力作用**：让模型在不同的表示子空间学习关注不同类型的关系
3. **残差连接关键**：缓解深层网络的梯度消失问题
4. **LayerNorm vs BatchNorm**：LayerNorm 更适合序列模型
5. **位置编码选择**：RoPE 在 LLM 中广泛使用（如 LLaMA、Qwen）

## 🔗 相关案例

- `flash-attention` - Flash Attention 原理与 CUDA 实现
- `rotary-embedding` - RoPE 旋转位置编码详解
- `mixture-of-experts` - MoE 混合专家架构
- `llama-architecture` - LLaMA 模型架构解读

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
