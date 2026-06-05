# Decoder-Only 架构 (GPT 系列)

> 本案例深入解析 Decoder-Only 架构，聚焦 GPT 系列模型的自回归生成和因果注意力机制

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Decoder-Only (GPT)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: "今天天气"                                               │
│                                                                 │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Token Embedding + Positional Encoding       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Causal (Masked) Self-Attention              │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │   │
│  │  │ Head 1  │  │ Head 2  │  │ Head h  │                  │   │
│  │  │ ▓▓▓░░░  │  │ ▓▓▓▓░░  │  │ ▓▓▓▓▓░  │ ← 因果掩码        │   │
│  │  └─────────┘  └─────────┘  └─────────┘                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Feed Forward Network                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│       ┌───────────────────┼───────────────────┐                 │
│       ▼                   ▼                   ▼                 │
│  ┌─────────┐         ┌─────────┐         ┌─────────┐          │
│  │Decoder  │         │Decoder  │   ...   │Decoder  │          │
│  │ Layer 1 │         │ Layer 2 │         │ Layer N │          │
│  └─────────┘         └─────────┘         └─────────┘          │
│                           │                                      │
│                           ▼                                      │
│                  ┌────────────────┐                             │
│                  │   Language     │                             │
│                  │   Model Head   │                             │
│                  └────────────────┘                             │
│                           │                                      │
│                           ▼                                      │
│                    "真好，适合户外"                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 因果注意力 (Causal Attention)

Decoder-Only 的关键机制：

```
位置 i 只能关注位置 0 到 i-1 的 tokens
通过下三角注意力掩码实现
```

### 2. 自回归生成 (Autoregressive)

逐 token 生成下一个 token：

```python
def generate(model, input_ids, max_new_tokens):
    for _ in range(max_new_tokens):
        logits = model(input_ids)
        next_token_logits = logits[:, -1, :]
        next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
        input_ids = torch.cat([input_ids, next_token], dim=1)
    return input_ids
```

### 3. Next Token Prediction

训练目标最大化似然：

```
Loss = -Σ log P(x_{t+1} | x_1, ..., x_t)
```

## 💻 核心实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class CausalSelfAttention(nn.Module):
    """因果自注意力"""
    def __init__(self, d_model, num_heads, max_seq_len, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)
        
        self.register_buffer(
            "causal_mask",
            torch.tril(torch.ones(max_seq_len, max_seq_len)).view(1, 1, max_seq_len, max_seq_len)
        )
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        batch_size, seq_len, d_model = x.size()
        
        Q = self.W_Q(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_K(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_V(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        causal_mask = self.causal_mask[:, :, :seq_len, :seq_len]
        scores = scores.masked_fill(causal_mask == 0, float('-inf'))
        
        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        context = torch.matmul(attention_weights, V)
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
        
        return self.W_O(context)


class DecoderLayer(nn.Module):
    """Decoder 层"""
    def __init__(self, d_model, num_heads, d_ff, max_seq_len, dropout=0.1):
        super().__init__()
        self.self_attn = CausalSelfAttention(d_model, num_heads, max_seq_len, dropout)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model)
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        x = self.norm1(x + self.dropout(self.self_attn(x)))
        x = self.norm2(x + self.dropout(self.ffn(x)))
        return x


class GPTDecoder(nn.Module):
    """GPT Decoder-Only 模型"""
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff, max_seq_len, dropout=0.1):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_seq_len, d_model)
        
        self.layers = nn.ModuleList([
            DecoderLayer(d_model, num_heads, d_ff, max_seq_len, dropout)
            for _ in range(num_layers)
        ])
        
        self.norm = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)
        
    def forward(self, input_ids):
        batch_size, seq_len = input_ids.size()
        
        token_embeds = self.token_embedding(input_ids)
        position_ids = torch.arange(seq_len, device=input_ids.device)
        position_embeds = self.position_embedding(position_ids)
        
        hidden_states = token_embeds + position_embeds
        
        for layer in self.layers:
            hidden_states = layer(hidden_states)
        
        hidden_states = self.norm(hidden_states)
        logits = self.lm_head(hidden_states)
        
        return logits
```

## 📊 Decoder-Only vs Encoder-Only

| 特性 | Decoder-Only | Encoder-Only |
|------|--------------|--------------|
| 注意力 | 单向（因果） | 双向 |
| 生成能力 | 强 | 弱 |
| 上下文利用 | 单向 | 双向 |
| 典型任务 | 文本生成 | 理解、分类 |
| 训练效率 | 低（自回归） | 高（并行） |

## 🧪 实践练习

### 练习：实现 Greedy Decoding

```python
def greedy_decode(model, input_ids, max_new_tokens, eos_token_id):
    """贪心解码"""
    for _ in range(max_new_tokens):
        logits = model(input_ids)
        next_token_logits = logits[:, -1, :]
        next_token = torch.argmax(next_token_logits, dim=-1)
        
        if next_token == eos_token_id:
            break
        input_ids = torch.cat([input_ids, next_token.unsqueeze(0)], dim=1)
    return input_ids
```

## 📚 学习要点

1. **因果掩码的本质**：防止看到未来信息
2. **KV Cache**：推理加速的关键技术
3. **自回归的挑战**：训练效率低，推理成本高
4. **Scaling Law**：模型规模与性能的幂律关系
