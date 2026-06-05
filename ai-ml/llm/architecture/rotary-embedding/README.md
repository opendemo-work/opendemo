# RoPE 旋转位置编码详解

> 本案例详解 Rotary Position Embedding (RoPE) 的原理与实现，理解其如何在 LLM 中替代绝对/相对位置编码

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    RoPE 核心思想                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  绝对位置编码的问题:                                              │
│  ❌ 不具备相对位置感知能力                                        │
│  ❌ 位置编码是加性的，对旋转不友好                                │
│                                                                 │
│  RoPE 解决方案:                                                  │
│  ✅ 通过旋转操作实现位置编码                                      │
│  ✅ Query 和 Key 旋转后，内积天然包含相对位置信息                  │
│  ✅ 可以处理任意长度的序列                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

RoPE 旋转矩阵:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  对第 m 个位置，Query 向量 q_m 需要旋转 θ_m:                       │
│                                                                 │
│         ┌ cos(mθ)  -sin(mθ) ┐                                  │
│  R_m =  │                       │                                 │
│         └ sin(mθ)   cos(mθ) ┘                                  │
│                                                                 │
│  旋转后的 Query:                                                 │
│  q'_m = R_m · q_m                                              │
│                                                                 │
│  旋转后的 Key:                                                   │
│  k'_n = R_n · k_n                                              │
│                                                                 │
│  内积 (包含相对位置):                                            │
│  q'_m · k'_n = (R_m q_m) · (R_n k_n)                          │
│               = q_m · R_{m-n} · k_n                            │
│               = q_m · k'_n-m  ← 相对位置 m-n                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

多维 RoPE 实现:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  对于 d_model 维向量，分为 d/2 个 2D 子向量:                      │
│                                                                 │
│  q_m = [q_{m,0}, q_{m,1}, ..., q_{m,d-2}, q_{m,d-1}]         │
│        ─────────  ─────────              ─────────              │
│           2D       2D                     2D                    │
│           pair     pair                   pair                   │
│                                                                 │
│  第 i 个 pair 的旋转角度:                                        │
│  θ_i = BASE^{-2i/d}  (通常 BASE = 10000)                      │
│                                                                 │
│  第 i 个 pair 的旋转:                                            │
│  ┌ cos(mθ_i)  -sin(mθ_i) ┐ ┌ q_{m,2i}     ┐                 │
│  │                       │ │               │                     │
│  └ sin(mθ_i)   cos(mθ_i) ┘ └ q_{m,2i+1}   ┘                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 旋转位置编码 vs 其他编码

| 特性 | Sinusoidal | Relative (Shaw) | RoPE |
|------|------------|-----------------|------|
| 绝对位置 | ✅ | ❌ | ✅ |
| 相对位置 | ✅ | ✅ | ✅ |
| 可扩展长度 | ❌ | ✅ | ✅ |
| 计算效率 | 高 | 中 | 高 |
| LLM 采用 | BERT | - | LLaMA, Qwen, GLM |

### 2. RoPE 核心公式

```python
# 旋转角度
θ_i = BASE^{-2i/d} = 10000^{-2i/d}

# 旋转矩阵
R(θ, m) = cos(mθ) + sin(mθ) * [[0, -1], [1, 0]]

# 旋转操作
RoPE(q_m, i) = q_{m,2i} * cos(mθ_i) - q_{m,2i+1} * sin(mθ_i)
               q_{m,2i+1} * cos(mθ_i) + q_{m,2i} * sin(mθ_i)
```

### 3. 远程衰减特性

```python
# RoPE 内积随相对距离衰减
# 有利于注意力自然地关注近距离 token

<q_m, k_n> ∝ cos((m-n)θ)
```

## 💻 完整实现

### RoPE 实现

```python
import math
import torch
import torch.nn as nn
import torch.nn.functional as F

def precompute_freqs_cis(dim: int, end: int, theta: float = 10000.0) -> torch.Tensor:
    """
    预计算旋转角度
    
    Args:
        dim: 嵌入维度
        end: 最大序列长度
        theta: 基础角度
    
    Returns:
        freqs_cis: 复数形式的旋转因子 [seq_len, dim//2]
    """
    # 计算每个维度的频率
    # θ_i = theta^{-2i/dim}
    freqs = theta ** (-2.0 * torch.arange(0, dim, 2).float() / dim)
    
    # 计算位置角度
    # m * θ_i
    positions = torch.arange(end).float()
    angles = positions[:, None] * freqs[None, :]
    
    # 转换为复数形式: cos(mθ) + i*sin(mθ)
    freqs_cis = torch.polar(torch.ones_like(angles), angles)
    
    return freqs_cis


def rotate_half(x: torch.Tensor) -> torch.Tensor:
    """
    旋转半个隐藏维度
    
    Input: [batch, seq_len, num_heads, head_dim]
    Output: [batch, seq_len, num_heads, head_dim]
    """
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat([-x2, x1], dim=-1)


def apply_rotary_pos_emb(
    q: torch.Tensor,
    k: torch.Tensor,
    freqs_cis: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    应用 RoPE 到 Q 和 K
    
    Args:
        q: Query [batch, seq_len, num_heads, head_dim]
        k: Key [batch, seq_len, num_heads, head_dim]
        freqs_cis: 旋转因子 [seq_len, head_dim//2]
    
    Returns:
        q_rot, k_rot: 旋转后的 Q 和 K
    """
    # reshape freqs_cis 以匹配 q 的形状
    # freqs_cis: [seq_len, head_dim//2] -> [1, seq_len, 1, head_dim//2]
    freqs_cis = freqs_cis.unsqueeze(0).unsqueeze(2)  # [1, seq_len, 1, head_dim//2]
    
    # 将实数复数转换为复数张量
    # q: [batch, seq_len, num_heads, head_dim] -> [batch, seq_len, num_heads, head_dim//2, 2]
    q_float = q.float().reshape(q.shape[:-1] + (-1, 2))
    k_float = k.float().reshape(k.shape[:-1] + (-1, 2))
    
    # 复数乘法
    # q_complex: [batch, seq_len, num_heads, head_dim//2]
    q_complex = torch.view_as_complex(q_float)
    k_complex = torch.view_as_complex(k_float)
    
    # 应用旋转 (复数乘法)
    q_rot = torch.view_as_real(q_complex * freqs_cis)
    k_rot = torch.view_as_real(k_complex * freqs_cis)
    
    # reshape 回原始格式
    q_rot = q_rot.flatten(-2).type_as(q)
    k_rot = k_rot.flatten(-2).type_as(k)
    
    return q_rot, k_rot


class RotaryEmbedding(nn.Module):
    """RoPE 嵌入层"""
    
    def __init__(
        self,
        dim: int,
        max_seq_len: int = 4096,
        theta: float = 10000.0
    ):
        super().__init__()
        self.dim = dim
        self.max_seq_len = max_seq_len
        self.theta = theta
        
        # 预计算旋转因子
        self.freqs_cis = precompute_freqs_cis(dim, max_seq_len * 2, theta)
        
    def forward(self, seq_len: int) -> torch.Tensor:
        """返回旋转因子"""
        # 动态扩展如果需要
        if seq_len > self.max_seq_len:
            self._extend_freqs(seq_len)
        return self.freqs_cis[:seq_len]
    
    def _extend_freqs(self, new_len: int):
        """扩展预计算的频率"""
        if new_len <= self.max_seq_len:
            return
        new_freqs = precompute_freqs_cis(self.dim, new_len * 2, self.theta)
        self.freqs_cis = torch.cat([self.freqs_cis, new_freqs[self.max_seq_len:]], dim=0)
        self.max_seq_len = new_len
```

### Transformer 中的 RoPE

```python
class RoPEAttention(nn.Module):
    """使用 RoPE 的注意力层"""
    
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads
        
        # QKV 投影
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.o_proj = nn.Linear(d_model, d_model)
        
        # RoPE
        self.rotary_emb = RotaryEmbedding(self.head_dim)
        
    def forward(
        self,
        x: torch.Tensor,
        mask: torch.Tensor = None
    ) -> torch.Tensor:
        batch_size, seq_len, _ = x.shape
        
        # QKV 投影
        q = self.q_proj(x).view(batch_size, seq_len, self.num_heads, self.head_dim)
        k = self.k_proj(x).view(batch_size, seq_len, self.num_heads, self.head_dim)
        v = self.v_proj(x).view(batch_size, seq_len, self.num_heads, self.head_dim)
        
        # 应用 RoPE
        freqs_cis = self.rotary_emb(seq_len)
        q, k = apply_rotary_pos_emb(q, k, freqs_cis)
        
        # 注意力计算
        attn_output = F.scaled_dot_product_attention(q, k, v, mask)
        
        # 输出投影
        attn_output = attn_output.flatten(-2)
        output = self.o_proj(attn_output)
        
        return output
```

### Llama 中的完整实现

```python
# 参考 transformers/src/transformers/models/llama/modeling_llama.py

def rotate_half(x):
    """RoPE 旋转 half"""
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat([-x2, x1], dim=-1)


def apply_rotary_pos_emb(q, k, cos, sin, position_ids):
    """应用 RoPE"""
    # cos, sin: [batch_size, seq_len, num_heads, head_dim]
    # position_ids: [batch_size, seq_len]
    
    cos = cos[position_ids].unsqueeze(2)  # [batch, seq, 1, dim]
    sin = sin[position_ids].unsqueeze(2)
    
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    
    return q_embed, k_embed


class LlamaAttention(nn.Module):
    """Llama 的注意力实现"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        self.num_heads = config.num_attention_heads
        self.head_dim = self.hidden_size // self.num_heads
        
        self.q_proj = nn.Linear(self.hidden_size, self.num_heads * self.head_dim)
        self.k_proj = nn.Linear(self.hidden_size, self.num_heads * self.head_dim)
        self.v_proj = nn.Linear(self.hidden_size, self.num_heads * self.head_dim)
        self.o_proj = nn.Linear(self.num_heads * self.head_dim, self.hidden_size)
        
        # RoPE 嵌入
        self.rotary_emb = LlamaRotaryEmbedding(
            dim=self.head_dim,
            max_position_embeddings=config.max_position_embeddings
        )
    
    def forward(self, hidden_states, position_ids, attention_mask=None):
        batch_size = hidden_states.shape[0]
        
        # QKV
        q = self.q_proj(hidden_states)
        k = self.k_proj(hidden_states)
        v = self.v_proj(hidden_states)
        
        q = q.view(batch_size, -1, self.num_heads, self.head_dim)
        k = k.view(batch_size, -1, self.num_heads, self.head_dim)
        v = v.view(batch_size, -1, self.num_heads, self.head_dim)
        
        # RoPE
        cos, sin = self.rotary_emb(v, position_ids)
        q, k = apply_rotary_pos_emb(q, k, cos, sin, position_ids)
        
        # 注意力
        attn_output = F.scaled_dot_product_attention(q, k, v, attention_mask)
        
        # 输出
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(batch_size, -1, self.hidden_size)
        return self.o_proj(attn_output)
```

## 📊 RoPE vs 其他位置编码

| 特性 | Sinusoidal | RoPE | ALiBi |
|------|------------|------|-------|
| 外推能力 | ❌ 差 | ✅ 好 | ✅ 最好 |
| 远程衰减 | ✅ | ✅ | ❌ |
| 计算效率 | 高 | 高 | 高 |
| 实现复杂度 | 低 | 中 | 低 |
| GPT-3 | ✅ | ❌ | ❌ |
| LLaMA | ❌ | ✅ | ❌ |
| BLOOM | ❌ | ❌ | ✅ |

## 📋 命令速查

```bash
# 测试 RoPE 实现
python rotary_embedding/test_rope.py

# 对比不同位置编码
python rotary_embedding/compare_encodings.py

# 可视化注意力模式
python rotary_embedding/visualize_attention.py
```

## 📚 学习要点

1. **旋转本质**：通过旋转 QK 内积实现相对位置感知
2. **远程衰减**：内积随距离自然衰减，有利长序列
3. **长度外推**：通过位置插值处理超长序列
4. **复数形式**：用复数乘法简化旋转操作

## 🔗 相关案例

- `transformer-scratch` - Transformer 从零实现
- `flash-attention` - Flash Attention
- `mixture-of-experts` - MoE 混合专家
- `llama-architecture` - LLaMA 架构解读
