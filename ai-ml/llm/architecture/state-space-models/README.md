# 状态空间模型 (State Space Models / Mamba)

> 本案例深入解析状态空间模型 (SSM)，理解 Mamba 的选择性扫描机制和线性复杂度推理优势

## 📐 架构对比

```
┌─────────────────────────────────────────────────────────────────┐
│              Transformer vs Mamba 架构对比                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Transformer                    Mamba (SSM)                      │
│  ┌──────────────────┐          ┌──────────────────┐            │
│  │ O(n²) Attention  │          │ O(n) Linear Scan  │            │
│  │                  │          │                  │            │
│  │ Q,K,V projections│          │ Selective SSM     │            │
│  │ Softmax(QK^T)V  │          │ x' = Ax + Bu     │            │
│  │                  │          │ y = Cx + Du       │            │
│  └──────────────────┘          └──────────────────┘            │
│                                                                 │
│  优势：表达力强                优势：线性推理、选择性遗忘       │
│  劣势：O(n²) 复杂度            劣势：表达能力略逊                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 状态空间模型基础

SSM 将序列建模为连续状态系统：

```
连续形式：
  x'(t) = A · x(t) + B · u(t)
  y(t) = C · x(t) + D · u(t)

离散形式：
  x_k = A_k · x_{k-1} + B_k · u_k
  y_k = C_k · x_k + D_k · u_k
```

### 2. Mamba 的选择性机制

Mamba 的核心创新是选择性状态扫描：

```python
def selective_scan(u, A, B, C, D):
    """Mamba 选择性扫描"""
    b, l, d_inner = u.shape
    
    # 动态计算 B, C (基于输入选择)
    B = nn.Parameter(torch.sigmoid(project_input(u, dim_b)) @ B_bar)
    C = nn.Parameter(torch.sigmoid(project_input(u, dim_c)) @ C_bar)
    
    # 选择性扫描替代 full attention
    y = causal_conv1d(u)  # 预处理
    y = torch.einsum('bld,dn,bld->bln', y, A, u)  # SSM 计算
    
    return y
```

### 3. 与 Transformer 对比

| 特性 | Transformer | Mamba |
|------|-------------|-------|
| 复杂度 | O(n²) | O(n) |
| 推理速度 | 慢 | 快 |
| 上下文长度 | 受限 | 可扩展 |
| 选择性记忆 | 弱 | 强 |
| 并行训练 | 支持 | 支持 |

## 💻 核心实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class RMSNorm(nn.Module):
    def __init__(self, d_model, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(d_model))
    
    def forward(self, x):
        rms = torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * rms * self.weight


class MambaBlock(nn.Module):
    """Mamba Block 实现"""
    def __init__(self, d_model, d_state=16, d_conv=4, expand=2):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.d_inner = int(expand * d_model)
        
        # 输入投影
        self.in_proj = nn.Linear(d_model, self.d_inner * 2, bias=False)
        
        # 卷积
        self.conv1d = nn.Conv1d(
            self.d_inner, self.d_inner,
            kernel_size=d_conv,
            padding=d_conv - 1,
            groups=self.d_inner
        )
        
        # SSM 参数
        self.x_proj = nn.Linear(self.d_inner, d_state * 2 + 1, bias=False)
        self.dt_proj = nn.Linear(1, self.d_inner, bias=True)
        
        # A, B, C 矩阵
        A = torch.arange(1, d_state + 1, dtype=torch.float).repeat(self.d_inner, 1)
        self.A_log = nn.Parameter(torch.log(A))
        self.D = nn.Parameter(torch.ones(self.d_inner))
        
        self.out_proj = nn.Linear(self.d_inner, d_model, bias=False)
        self.norm = RMSNorm(d_model)
        
    def selective_scan(self, x, dt, A, B, C, D):
        """选择性扫描核心"""
        batch, seq_len, d_inner = x.shape
        d_state = B.shape[-1]
        
        # 离散化
        dA = torch.exp(dt.unsqueeze(-1) * A)  # (batch, seq, d_inner, d_state)
        dB = dt.unsqueeze(-1) * B.unsqueeze(2)  # (batch, seq, d_inner, d_state)
        
        # 扫描计算
        h = torch.zeros(batch, d_inner, d_state, device=x.device)
        ys = []
        
        for i in range(seq_len):
            h = dA[:, i] * h + dB[:, i] * x[:, i:i+1].transpose(-1, -2)
            y = torch.einsum('bdn,dn->bd', h, C[:, i])
            ys.append(y)
        
        y = torch.stack(ys, dim=1)
        return y
    
    def forward(self, x):
        batch, seq_len, d_model = x.shape
        
        # 输入投影 + 分割
        xz = self.in_proj(x)
        x_inner, z = xz.chunk(2, dim=-1)
        
        # 卷积 + 激活
        x_conv = self.conv1d(x_inner.transpose(1, 2))[:, :, :seq_len].transpose(1, 2)
        x_conv = F.silu(x_conv)
        
        # SSM 参数
        x_flat = x_conv.reshape(batch * seq_len, self.d_inner)
        x_proj = self.x_proj(x_flat)
        dt, B, C = x_proj.split([1, self.d_state, self.d_state], dim=-1)
        
        dt = F.softplus(self.dt_proj(dt))
        A = -torch.exp(self.A_log.float())
        B = B.float().reshape(batch, seq_len, self.d_state)
        C = C.float().reshape(batch, seq_len, self.d_state)
        D = self.D.float()
        
        # 选择性扫描
        y = self.selective_scan(x_conv, dt, A, B, C, D)
        
        # GEGLU 门控
        y = y * F.gelu(z)
        
        # 输出投影
        output = self.out_proj(y)
        
        return output + x


class MambaModel(nn.Module):
    """完整的 Mamba 模型"""
    def __init__(self, vocab_size, d_model, n_layers, d_state=16):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.layers = nn.ModuleList([
            MambaBlock(d_model, d_state)
            for _ in range(n_layers)
        ])
        self.norm = RMSNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)
        
    def forward(self, input_ids):
        x = self.embedding(input_ids)
        for layer in self.layers:
            x = layer(x) + x  # 残差连接
        x = self.norm(x)
        return self.lm_head(x)
```

## 📊 效率对比

| 模型 | 推理复杂度 | 100K 上下文推理时间 |
|------|------------|---------------------|
| Transformer | O(n²) | ~30分钟 |
| Mamba | O(n) | ~1分钟 |
| FlashAttention | O(n²) 但高效 | ~5分钟 |

## 🧪 实践练习

### 练习：实现 SSM 的并行扫描

```python
def parallel_scan(x, A, B):
    """并行扫描算法（简化为演示）"""
    # Mamba 使用并行扫描算法实现高效计算
    # 实际实现需要自定义 CUDA kernel
    seq_len = x.shape[1]
    h = torch.zeros_like(x)
    
    for i in range(seq_len):
        if i == 0:
            h[:, i] = B[:, i] * x[:, i]
        else:
            h[:, i] = A[:, i] * h[:, i-1] + B[:, i] * x[:, i]
    
    return h
```

## 📚 学习要点

1. **SSM 的线性复杂度**：选择性地扫描输入，而非全注意力
2. **A 矩阵的作用**：类似 LSTM 的遗忘门，控制信息保留
3. **与 RNN 的区别**：SSM 可以并行训练，同时保持 RNN 的推理效率
4. **Mamba 的优势**：在长上下文任务上效率显著高于 Transformer
