# LLaMA 模型架构

> 本案例深入解析 LLaMA 模型架构，理解 RMSNorm、SwiGLU、RoPE 等关键优化技术的工程实现

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         LLaMA Model                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input Tokens                                                    │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Token Embedding (with RMSNorm Pre-norm)      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│       ┌───────────────────┼───────────────────┐                 │
│       ▼                   ▼                   ▼                 │
│  ┌─────────┐         ┌─────────┐         ┌─────────┐          │
│  │ LLaMA   │         │ LLaMA   │   ...   │ LLaMA   │          │
│  │ Block 1 │         │ Block 2 │         │ Block N │          │
│  └─────────┘         └─────────┘         └─────────┘          │
│       │                   │                   │                 │
│       └───────────────────┼───────────────────┘                 │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Final RMSNorm                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Linear (LM Head)                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│                    Output Distribution                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

LLaMA Block 内部结构：
┌─────────────────────────────────────────────────────────┐
│  Input (Pre-Norm)                                        │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │            RMSNorm (Pre-Normalization)            │   │
│  └──────────────────────────────────────────────────┘   │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │     Casual Self-Attention + RoPE                 │   │
│  │     (with Q, K, V projections + Rotary Embed)    │   │
│  └──────────────────────────────────────────────────┘   │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │                  RMSNorm                          │   │
│  └──────────────────────────────────────────────────┘   │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │         SwiGLU Feed Forward (W1, W2, W3)         │   │
│  │         FFN = Swish(W1,x) * (W2,x)               │   │
│  └──────────────────────────────────────────────────┘   │
│       │                                                  │
│       ▼                                                  │
│      Output                                               │
└─────────────────────────────────────────────────────────┘
```

## 🎯 核心优化

### 1. RMSNorm

比 LayerNorm 更高效的归一化：

```python
class RMSNorm(nn.Module):
    """RMSNorm 实现"""
    def __init__(self, d_model, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(d_model))
        
    def forward(self, x):
        rms = torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * rms * self.weight
```

### 2. SwiGLU 激活函数

LLaMA 使用的改进激活：

```
SwiGLU(x) = Swish(W_1, x) ⊙ Sigmoid(W_2, x)
```

### 3. RoPE 旋转位置编码

所有 LLaMA 模型使用 RoPE 而非绝对位置编码。

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


class SwiGLU(nn.Module):
    """SwiGLU 激活"""
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff, bias=False)
        self.w2 = nn.Linear(d_model, d_ff, bias=False)
        self.w3 = nn.Linear(d_model, d_ff, bias=False)
        
    def forward(self, x):
        return F.silu(self.w1(x)) * self.w2(x)


def precompute_freqs_cis(dim, end, theta=10000.0):
    """预计算旋转编码的复数频率"""
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2).float() / dim))
    t = torch.arange(end)
    freqs = torch.outer(t, freqs)
    return torch.polar(torch.ones_like(freqs), freqs)


def apply_rotary_emb(x, freqs_cis):
    """应用旋转位置编码"""
    x_complex = torch.view_as_complex(x.float().reshape(*x.shape[:-1], -1, 2))
    freqs_cis = freqs_cis[:, :x_complex.size(1)]
    x_rotated = x_complex * freqs_cis
    return torch.view_as_real(x_rotated).flatten(-2).type_as(x)


class Attention(nn.Module):
    def __init__(self, d_model, num_heads, max_seq_len):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, d_model, bias=False)
        self.W_V = nn.Linear(d_model, d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)
        
        self.freqs_cis = precompute_freqs_cis(self.d_k, max_seq_len * 2)
        
    def forward(self, x, start_pos=0):
        b, seq_len, d_model = x.shape
        
        q = self.W_Q(x).view(b, seq_len, self.num_heads, self.d_k)
        k = self.W_K(x).view(b, seq_len, self.num_heads, self.d_k)
        v = self.W_V(x).view(b, seq_len, self.num_heads, self.d_k)
        
        q = apply_rotary_emb(q, self.freqs_cis[start_pos:start_pos+seq_len])
        k = apply_rotary_emb(k, self.freqs_cis[start_pos:start_pos+seq_len])
        
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        causal_mask = torch.triu(torch.ones(seq_len, seq_len, device=x.device), diagonal=1).bool()
        scores = scores.masked_fill(causal_mask, float('-inf'))
        
        attn = F.softmax(scores, dim=-1)
        attn = torch.matmul(attn, v)
        
        return self.W_O(attn.transpose(1, 2).contiguous().view(b, seq_len, d_model))


class LLaMABlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, max_seq_len):
        super().__init__()
        self.attention = Attention(d_model, num_heads, max_seq_len)
        self.ffn = SwiGLU(d_model, d_ff)
        self.attention_norm = RMSNorm(d_model)
        self.ffn_norm = RMSNorm(d_model)
        
    def forward(self, x, start_pos=0):
        x = x + self.attention(self.attention_norm(x), start_pos)
        x = x + self.ffn(self.ffn_norm(x))
        return x


class LLaMA(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff, max_seq_len):
        super().__init__()
        self.layers = nn.ModuleList([
            LLaMABlock(d_model, num_heads, d_ff, max_seq_len)
            for _ in range(num_layers)
        ])
        self.norm = RMSNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)
        
    def forward(self, input_ids, start_pos=0):
        x = self.lm_head.weight[input_ids]
        for layer in self.layers:
            x = layer(x, start_pos)
        return self.norm(x) @ self.lm_head.weight.T
```

## 📊 LLaMA 系列对比

| Model | Params | Layers | Heads | Context |
|-------|--------|--------|-------|---------|
| LLaMA 7B | 7B | 32 | 32 | 2048 |
| LLaMA 13B | 13B | 40 | 40 | 2048 |
| LLaMA 70B | 70B | 80 | 80 | 2048 |
| LLaMA 2 70B | 70B | 80 | 80 | 4096 |

## 🧪 实践练习

### 练习：实现 KV Cache

```python
def forward_with_kv_cache(self, x, start_pos, prev_k, prev_v):
    """带 KV Cache 的前向传播"""
    b, seq_len = x.shape[0], x.shape[1]
    cur_len = prev_k.shape[2] + seq_len
    
    x = self.attention_norm(x)
    q = self.W_Q(x)
    k = self.W_K(x)
    v = self.W_V(x)
    
    k = torch.cat([prev_k, k], dim=2)
    v = torch.cat([prev_v, v], dim=2)
    
    return q, k, v, cur_len
```

## 📚 学习要点

1. **Pre-Norm 的稳定性**：比 Post-Norm 更稳定
2. **SwiGLU 的效果**：显著提升模型表达能力
3. **KV Cache 的价值**：大幅加速推理
4. **RoPE 的优势**：无需学习的位置编码，支持长上下文
