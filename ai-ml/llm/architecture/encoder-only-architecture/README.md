<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Encoder-Only 架构 (BERT 系列)

> 本案例深入解析 Encoder-Only 架构，聚焦 BERT 系列模型的掩码语言建模和双向上下文理解机制

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Encoder-Only (BERT)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: [CLS] 今天 [MASK] 很好 [SEP]                            │
│                                                                 │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Token Embedding + Positional Encoding       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                      │
│       ┌───────────────────┼───────────────────┐                 │
│       ▼                   ▼                   ▼                 │
│  ┌─────────┐         ┌─────────┐         ┌─────────┐          │
│  │Encoder  │         │Encoder  │   ...   │Encoder  │          │
│  │ Layer 1 │         │ Layer 2 │         │ Layer N │          │
│  └─────────┘         └─────────┘         └─────────┘          │
│       │                   │                   │                 │
│       └───────────────────┼───────────────────┘                 │
│                           ▼                                      │
│              ┌─────────────────────────┐                        │
│              │   [CLS] Classification  │                        │
│              │       Output            │                        │
│              └─────────────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 掩码语言建模 (MLM)

BERT 采用随机掩码策略训练：

- **掩码比例**：15% 的 tokens 被掩码
- **掩码策略**：80% 替换为 [MASK]，10% 替换为随机词，10% 保持不变
- **训练目标**：预测被掩码位置的原始 token

### 2. 双向上下文

Encoder-Only 架构的核心优势：

- 每个位置可以关注序列中的所有其他位置
- 同时捕捉左侧和右侧的上下文信息
- 适用于理解任务（分类、序列标注、问答）

### 3. [CLS] Token

特殊分类 token 用于聚合全文表示：

```
[CLS] token 的输出hidden_states 用于下游分类任务
```

## 💻 核心实现

```python
import torch
import torch.nn as nn
from transformers import BertConfig

class BertEncoder(nn.Module):
    """BERT Encoder 实现"""
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff, max_seq_len):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_seq_len, d_model)
        self.segment_embedding = nn.Embedding(2, d_model)
        
        self.encoder_layers = nn.ModuleList([
            EncoderLayer(d_model, num_heads, d_ff)
            for _ in range(num_layers)
        ])
        
        self.pooler = nn.Linear(d_model, d_model)
        
    def forward(self, input_ids, segment_ids=None, attention_mask=None):
        seq_len = input_ids.size(1)
        position_ids = torch.arange(seq_len, device=input_ids.device)
        
        token_embeds = self.embedding(input_ids)
        position_embeds = self.position_embedding(position_ids)
        segment_embeds = self.segment_embedding(segment_ids) if segment_ids is not None else 0
        
        hidden_states = token_embeds + position_embeds + segment_embeds
        
        for layer in self.encoder_layers:
            hidden_states = layer(hidden_states, attention_mask)
        
        pooled_output = torch.tanh(self.pooler(hidden_states[:, 0]))
        return hidden_states, pooled_output


class EncoderLayer(nn.Module):
    """Transformer Encoder 层"""
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(d_model, num_heads, dropout, batch_first=True)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model)
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x, mask=None):
        attn_output, _ = self.self_attn(x, x, x, key_padding_mask=mask)
        x = self.norm1(x + self.dropout(attn_output))
        ffn_output = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_output))
        return x
```

## 📊 BERT vs GPT 对比

| 特性 | BERT (Encoder) | GPT (Decoder) |
|------|----------------|---------------|
| 注意力 | 双向 | 单向 |
| 训练目标 | MLM + NSP | Next Token Prediction |
| 适用任务 | 理解为主 | 生成为主 |
| 代表模型 | BERT, RoBERTa, DeBERTa | GPT-2/3/4, LLaMA |

## 🧪 实践练习

### 练习：实现 BERT 预训练损失

```python
def bert_pretraining_loss(mlm_logits, nsp_logits, mlm_labels, nsp_labels):
    """BERT 预训练损失计算"""
    mlm_loss = nn.CrossEntropyLoss()(mlm_logits.view(-1, vocab_size), mlm_labels.view(-1))
    nsp_loss = nn.CrossEntropyLoss()(nsp_logits, nsp_labels)
    return mlm_loss + nsp_loss
```

## 📚 学习要点

1. **双向注意力的代价**：无法进行自回归生成
2. **MLM 的优势**：充分使用双向上下文信息
3. **Segment Embedding**：用于处理句子对任务
4. **下游适配**：通过微调适应各种 NLP 任务

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
