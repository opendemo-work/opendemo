# GPT 架构演进 (GPT-2/3/4)

> 本案例深入解析 GPT-2/3/4 架构演进，理解从 GPT 到 GPT-4 的关键技术突破和 Scaling Laws

## 📐 GPT 系列演进

```
┌─────────────────────────────────────────────────────────────────┐
│                         GPT 系列演进                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GPT-1 (2018)          GPT-2 (2019)        GPT-3 (2020)        │
│  ┌─────────┐           ┌─────────┐          ┌─────────┐         │
│  │ 117M    │           │ 1.5B    │          │ 175B    │         │
│  │ 12 layers│          │ 48 layers│          │ 96 layers│         │
│  │ 768 dim  │          │ 1600 dim │          │ 12288   │         │
│  └─────────┘           └─────────┘          └─────────┘         │
│                                                                 │
│  GPT-4 (2023)                                                   │
│  ┌─────────┐                                                    │
│  │ ???B    │  ← 未公开详细架构                                   │
│  │ MoE?    │                                                    │
│  │ 长上下文│                                                    │
│  └─────────┘                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. GPT-1 → GPT-2 的关键改进

**GPT-2 核心设计**：
- 更深的网络 (48 layers vs 12)
- 更大的隐藏维度 (1600 vs 768)
- 去除下一句预测任务，专注语言建模
- 引入"涌现能力"概念

### 2. GPT-3 的突破

**Scaling Law** (Kaplan et al., 2020)：

```
L(N) = (N_c / N)^α + (N_min / N)^β + const

其中：
- N: 模型参数量
- L: 交叉熵损失
- α ≈ 0.076, β ≈ 0.095
```

**In-Context Learning**：

```python
# GPT-3 的 In-Context Learning
prompt = """
Translate to French:
English: Hello
French: Bonjour

English: Good morning
French:"""

# 模型直接"理解"示例模式，无需参数更新
output = gpt3.generate(prompt)
```

### 3. GPT-4 的进化

- **长上下文**：支持 128K tokens
- **多模态**：支持图像输入
- **对齐改进**：更安全的输出
- **推理能力**：更强的逻辑推理

## 💻 核心实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class GPTConfig:
    """GPT 配置"""
    def __init__(self, vocab_size, block_size, n_layer, n_head, n_embd, dropout=0.1):
        self.vocab_size = vocab_size
        self.block_size = block_size
        self.n_layer = n_layer
        self.n_head = n_head
        self.n_embd = n_embd
        self.dropout = dropout


class GPTBlock(nn.Module):
    """GPT Transformer Block"""
    def __init__(self, config):
        super().__init__()
        self.ln1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln2 = nn.LayerNorm(config.n_embd)
        self.mlp = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd),
            nn.GELU(),
            nn.Linear(4 * config.n_embd, config.n_embd),
            nn.Dropout(config.dropout)
        )
        
    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x


class GPT(nn.Module):
    """GPT 模型"""
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        self.wte = nn.Embedding(config.vocab_size, config.n_embd)
        self.wpe = nn.Embedding(config.block_size, config.n_embd)
        self.drop = nn.Dropout(config.dropout)
        self.h = nn.ModuleList([GPTBlock(config) for _ in range(config.n_layer)])
        self.ln_f = nn.LayerNorm(config.n_embd)
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        
        self.apply(self._init_weights)
        
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            
    def forward(self, idx):
        b, t = idx.size()
        pos = torch.arange(0, t, dtype=torch.long, device=idx.device)
        
        tok_emb = self.wte(idx)
        pos_emb = self.wpe(pos)
        x = self.drop(tok_emb + pos_emb)
        
        for block in self.h:
            x = block(x)
            
        x = self.ln_f(x)
        logits = self.lm_head(x)
        
        return logits


class CausalSelfAttention(nn.Module):
    """因果自注意力"""
    def __init__(self, config):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        self.dropout = config.dropout
        
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(config.block_size, config.block_size)).view(1, 1, config.block_size, config.block_size)
        )
        
    def forward(self, x):
        b, t, c = x.size()
        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)
        
        k = k.view(b, t, self.n_head, c // self.n_head).transpose(1, 2)
        q = q.view(b, t, self.n_head, c // self.n_head).transpose(1, 2)
        v = v.view(b, t, self.n_head, c // self.n_head).transpose(1, 2)
        
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
        att = att.masked_fill(self.bias[:, :, :t, :t] == 0, float('-inf'))
        att = F.softmax(att, dim=-1)
        att = F.dropout(att, p=self.dropout, training=self.training)
        
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(b, t, c)
        
        return self.c_proj(y)
```

## 📊 Scaling Laws 实验

| 参数量 | 训练 Tokens | 最优 Batch Size | 最优 LR |
|--------|-------------|-----------------|---------|
| 117M | 1M-100M | ~0.5M | 3e-4 |
| 1.5B | 1B | ~1M | 2.5e-4 |
| 175B | 300B | ~4M | 1.2e-4 |

## 📊 GPT-2 vs GPT-3 vs GPT-4

| 特性 | GPT-2 | GPT-3 | GPT-4 |
|------|-------|-------|-------|
| 参数量 | 1.5B | 175B | 私有 |
| 上下文 | 1K | 2K→8K | 128K |
| 多模态 | No | No | Yes |
| 推理能力 | 基础 | 中等 | 强 |

## 🧪 实践练习

### 练习：实现 In-Context Learning Demo

```python
def in_context_learning_demo():
    """演示 GPT 的 In-Context Learning 能力"""
    
    examples = [
        ("猫", "cat"),
        ("狗", "dog"),
        ("鸟", "bird"),
    ]
    
    prompt = "根据示例翻译：\n"
    for eng, chn in examples:
        prompt += f"{eng} → {chn}\n"
    prompt += "鱼 → "
    
    # 模型无需任何参数更新就能"学会"翻译模式
    result = gpt.generate(prompt)
    return result
```

## 📚 学习要点

1. **Scaling Law 的启示**：模型规模比数据规模更重要
2. **In-Context Learning**：通过上下文示例学习新任务
3. **涌现能力**：大模型突然出现小模型没有的能力
4. **GPT-4 的多模态**：统一处理文本和图像
