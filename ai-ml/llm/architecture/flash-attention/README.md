# Flash Attention 原理与实现

> 本案例深入解析 Flash Attention 算法原理，理解如何通过 IO-Aware 优化减少显存访问，提升注意力计算效率

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      Flash Attention 流程                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: Q, K, V Tensors                                         │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Block-wise 计算                        │   │
│  │                                                          │   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │   │
│  │   │ Block 1 │  │ Block 2 │  │ Block 3 │  │ Block 4 │  │   │
│  │   │ (T1)   │  │ (T2)    │  │ (T3)    │  │ (T4)    │  │   │
│  │   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  │   │
│  │        │            │            │            │        │   │
│  │        └────────────┼────────────┼────────────┘        │   │
│  │                     │            │                       │   │
│  │                     ▼            ▼                       │   │
│  │              Online Softmax                             │   │
│  │                     │                                    │   │
│  │                     ▼                                    │   │
│  │              Attn Block 1│2|3|4                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│                      Output: Attention Matrix                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

标准 Attention vs Flash Attention 对比:

标准 Attention (O(n²) 显存):
┌─────────────────────────────────┐
│  Q × K^T  →  n×n Matrix        │
│       ↓                         │
│  softmax →  n×n Matrix          │
│       ↓                         │
│  × V    →  n×d Matrix          │
│       ↓                         │
│  需要完整 n×n 中间结果          │
└─────────────────────────────────┘

Flash Attention (O(n) 显存):
┌─────────────────────────────────┐
│  分块处理: 每次只处理 block     │
│       ↓                         │
│  Online Softmax 增量计算        │
│       ↓                         │
│  累积统计量 (m, l) 替代完整矩阵 │
│       ↓                         │
│  最终一次性得到正确结果         │
└─────────────────────────────────┘
```

## 🎯 核心概念

### 1. 标准 Attention 的问题

标准 Attention 实现需要计算并存储完整的注意力矩阵：

```
S = QK^T ∈ R^{n×n}  (n = 序列长度)
P = softmax(S) ∈ R^{n×n}
O = PV ∈ R^{n×d}
```

**问题：**
- 显存复杂度：O(n²)
- 对于 LLM，n 可达 4096+，显存爆炸

### 2. Flash Attention 核心思想

**IO-Aware 优化**：利用 GPU 内存层级，减少 HBM 和 SRAM 之间的数据移动

```
GPU 内存层级:
┌─────────────────────────────────────┐
│        HBM (High Bandwidth)         │  ← 慢但容量大 (80GB)
│                                     │
│   ┌─────────────────────────────┐  │
│   │      SRAM (Shared Memory)    │  │  ← 快但容量小 (192KB/block)
│   │         ~192 KB              │  │
│   └─────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘

策略: 分块加载 K, V 到 SRAM，计算后释放
```

### 3. Online Softmax 算法

Flash Attention 使用在线 softmax 避免完整矩阵：

```
传统 softmax:
exp(x_i) / Σ exp(x_j)

在线版本:
m_i = max(x_i, m_{i-1})           # 局部最大值
M_i = max(M_{i-1}, m_i)          # 全局最大值
f_i = exp(x_i - M_i)             # 归一化指数
l_i = l_{i-1} + f_i              # 累积和
softmax = f_i / l_i              # 最终结果
```

## 💻 完整实现

### Flash Attention CUDA 实现

```cuda
// flash_attention.cu
#include <cuda_runtime.h>
#include <stdio.h>

#define BLOCK_SIZE 128
#define HEAD_DIM 64

__global__ void flash_attention_kernel(
    const float* Q,      // [batch, heads, seq_len, dim]
    const float* K,
    const float* V,
    float* Output,
    int seq_len,
    int batch_size,
    int num_heads
) {
    int batch_idx = blockIdx.z;
    int head_idx = blockIdx.y;
    int block_row = blockIdx.x;

    int row_start = block_row * BLOCK_SIZE;
    int row_end = min(row_start + BLOCK_SIZE, seq_len);

    // 共享内存暂存
    __shared__ float k_cache[BLOCK_SIZE][HEAD_DIM];
    __shared__ float v_cache[BLOCK_SIZE][HEAD_DIM];

    float q[HEAD_DIM];
    float acc[HEAD_DIM] = {0.0f};
    float m_prev = -INFINITY;
    float l_prev = 0.0f;

    // 加载 Q
    int q_idx = (batch_idx * num_heads + head_idx) * seq_len * HEAD_DIM
                + row_start * HEAD_DIM;
    for (int i = 0; i < HEAD_DIM; i++) {
        q[i] = Q[q_idx + i];
    }

    // 逐块计算
    for (int block_col = 0; block_col < seq_len; block_col += BLOCK_SIZE) {
        // 加载 K, V 到共享内存
        int k_idx = (batch_idx * num_heads + head_idx) * seq_len * HEAD_DIM
                    + block_col * HEAD_DIM;

        for (int i = threadIdx.x; i < BLOCK_SIZE * HEAD_DIM; i += blockDim.x) {
            int row = i / HEAD_DIM;
            int col = i % HEAD_DIM;
            if (row < BLOCK_SIZE && (block_col + row) < seq_len) {
                k_cache[row][col] = K[k_idx + row * HEAD_DIM + col];
                v_cache[row][col] = V[k_idx + row * HEAD_DIM + col];
            }
        }
        __syncthreads();

        // 计算注意力分数
        for (int k = 0; k < BLOCK_SIZE && (block_col + k) < seq_len; k++) {
            // S_ij = Q_i · K_j / √d
            float s = 0.0f;
            for (int d = 0; d < HEAD_DIM; d++) {
                s += q[d] * k_cache[k][d];
            }
            s /= sqrtf((float)HEAD_DIM);

            // Online softmax
            float m = fmaxf(s, m_prev);
            float l = expf(m_prev - m) * l_prev + expf(s - m);
            float alpha = expf(s - m);
            float l_new = expf(m_prev - m) * l_prev + expf(s - m);

            // 更新输出
            for (int d = 0; d < HEAD_DIM; d++) {
                acc[d] = (expf(m_prev - m) * l_prev * acc[d] 
                         + alpha * v_cache[k][d]) / l_new;
            }

            m_prev = m;
            l_prev = l_new;
        }
        __syncthreads();
    }

    // 写入输出
    int out_idx = (batch_idx * num_heads + head_idx) * seq_len * HEAD_DIM
                  + row_start * HEAD_DIM;
    for (int i = threadIdx.x; i < (row_end - row_start) * HEAD_DIM; i += blockDim.x) {
        Output[out_idx + i] = acc[i % HEAD_DIM];
    }
}
```

### PyTorch 实现 (可运行版本)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

def flash_attention_pytorch(Q, K, V, block_size=64, dropout_p=0.0):
    """
    Flash Attention 的 PyTorch 参考实现
    Q, K, V: [batch, num_heads, seq_len, head_dim]
    """
    batch_size, num_heads, seq_len, head_dim = Q.shape

    # 初始化输出和累积统计量
    output = torch.zeros_like(Q)
    l = torch.zeros(batch_size, num_heads, seq_len, 1, device=Q.device)
    m = torch.full((batch_size, num_heads, seq_len, 1), -float('inf'), device=Q.device)

    # 按行分块
    for j in range(0, seq_len, block_size):
        # 加载当前块的 K, V
        K_block = K[:, :, j:j+block_size, :]
        V_block = V[:, :, j:j+block_size, :]

        # 计算注意力分数
        # Q: [batch, heads, seq_len, head_dim]
        # K_block: [batch, heads, block_size, head_dim]
        # scores: [batch, heads, seq_len, block_size]
        scores = torch.matmul(Q, K_block.transpose(-2, -1)) / math.sqrt(head_dim)

        # 更新 m 和 l (online softmax)
        m_block = torch.max(scores, dim=-1, keepdim=True)[0]
        m_new = torch.maximum(m[:, :, j:j+block_size, :], m_block)

        # 防止指数溢出
        scores = torch.exp(scores - m_new)

        l_block = torch.sum(scores, dim=-1, keepdim=True)
        l_update = torch.exp(m[:, :, j:j+block_size, :] - m_new) * l[:, :, j:j+block_size, :] + l_block

        # 更新输出
        output[:, :, j:j+block_size, :] = (
            (torch.exp(m[:, :, j:j+block_size, :] - m_new) * l[:, :, j:j+block_size, :] * output[:, :, j:j+block_size, :]
             + torch.matmul(scores, V_block)) / l_update
        )

        m[:, :, j:j+block_size, :] = m_new
        l[:, :, j:j+block_size, :] = l_update

    return output


class FlashAttention(nn.Module):
    """Flash Attention 层"""
    def __init__(self, d_model, num_heads, dropout=0.0):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads

        assert d_model % num_heads == 0

        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, Q, K, V, mask=None, use_flash=True):
        batch_size = Q.size(0)

        # 线性投影
        Q = self.W_Q(Q)
        K = self.W_K(K)
        V = self.W_V(V)

        # reshape to [batch, num_heads, seq_len, head_dim]
        Q = Q.view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)

        if use_flash and hasattr(torch.nn.functional, 'scaled_dot_product_attention'):
            # 使用 PyTorch 原生 flash attention (F.scaled_dot_product_attention)
            output = F.scaled_dot_product_attention(Q, K, V, dropout_p=self.dropout.p)
        else:
            output = flash_attention_pytorch(Q, K, V, block_size=64)

        # 合并头
        output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        output = self.W_O(output)

        return output
```

## 📊 性能对比

### 显存复杂度

| 实现 | 显存复杂度 | 相对显存 (n=4096, d=128) |
|------|------------|--------------------------|
| 标准 Attention | O(n²) | 1x (约 8GB) |
| Flash Attention v1 | O(n) | ~0.1x |
| Flash Attention v2 | O(n) | ~0.05x |

### Benchmark 示例

```python
def benchmark_attention():
    import time

    batch_size = 4
    num_heads = 32
    seq_len = 4096
    head_dim = 128

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    Q = torch.randn(batch_size, num_heads, seq_len, head_dim, device=device)
    K = torch.randn(batch_size, num_heads, seq_len, head_dim, device=device)
    V = torch.randn(batch_size, num_heads, seq_len, head_dim, device=device)

    # 标准 attention
    start = time.time()
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(head_dim)
    attn = F.softmax(scores, dim=-1)
    output = torch.matmul(attn, V)
    standard_time = time.time() - start

    # Flash attention
    start = time.time()
    flash_output = flash_attention_pytorch(Q, K, V)
    flash_time = time.time() - start

    print(f"Standard Attention: {standard_time*1000:.2f} ms")
    print(f"Flash Attention: {flash_time*1000:.2f} ms")
    print(f"Speedup: {standard_time/flash_time:.2f}x")
```

## 📋 命令速查

```bash
# 运行基准测试
python flash_attention/benchmark.py

# 运行 CUDA 实现测试
python flash_attention/cuda_test.py

# 可视化注意力权重
python flash_attention/visualize.py
```

## 📚 学习要点

1. **IO-Aware 核心**：理解 GPU 内存层级对性能的影响
2. **Online Softmax**：通过增量计算避免完整矩阵存储
3. **分块矩阵乘法**：Tile-based 计算提高数据局部性
4. **数值稳定性**：处理指数溢出问题

## 🔗 相关案例

- `multi-head-attention` - Multi-Head Attention 详解
- `transformer-scratch` - Transformer 从零实现
- `rotary-embedding` - RoPE 位置编码
- `vllm-inference` - vLLM 中的 Flash Attention 应用
