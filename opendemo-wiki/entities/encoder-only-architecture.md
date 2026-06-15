---
title: Encoder-Only Architecture
summary: BERT series models use bidirectional attention and masked language modeling for understanding tasks.
updated: 2026-06-05
tags:
  - llm
  - architecture
  - encoder-only-architecture
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/architecture/encoder-only-architecture/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Encoder-Only Architecture

Encoder-Only architecture powers BERT-series models with bidirectional attention and masked language modeling (MLM).

## Architecture

```
Input: [CLS] 今天 [MASK] 很好 [SEP]
  ▼
Token Embedding + Positional Encoding + Segment Embedding
  ▼
[N × Encoder Layers] (bidirectional self-attention)
  ▼
[CLS] Classification Output → Task-specific heads
```

## Core Concepts

### Masked Language Modeling (MLM)

- 15% of tokens masked
- 80% replaced with [MASK], 10% random, 10% unchanged
- Train to predict original masked tokens

### Bidirectional Context

Every position can attend to all other positions, capturing both left and right context simultaneously.

### [CLS] Token

Special classification token output used for downstream classification tasks.

## Key Implementation

```python
class BertEncoder(nn.Module):
    def forward(self, input_ids, segment_ids=None, attention_mask=None):
        token_embeds = self.embedding(input_ids)
        position_embeds = self.position_embedding(position_ids)
        segment_embeds = self.segment_embedding(segment_ids)
        
        hidden_states = token_embeds + position_embeds + segment_embeds
        
        for layer in self.encoder_layers:
            hidden_states = layer(hidden_states, attention_mask)
        
        pooled_output = torch.tanh(self.pooler(hidden_states[:, 0]))
        return hidden_states, pooled_output
```

## BERT vs GPT Comparison

| Feature | BERT (Encoder) | GPT (Decoder) |
|---------|----------------|---------------|
| Attention | Bidirectional | Unidirectional |
| Training Objective | MLM + NSP | Next Token Prediction |
| Primary Use | Understanding | Generation |
| Representatives | BERT, RoBERTa, DeBERTa | GPT-2/3/4, LLaMA |

## Key Insights

- [[entities/decoder-only-architecture]] for unidirectional generation
- [[entities/tech-stacks]] for LLM technology stacks overview
- Bidirectional attention sacrifices autoregressive generation capability
- Segment embeddings handle sentence-pair tasks
- Fine-tuning adapts pre-trained encoder for downstream tasks
