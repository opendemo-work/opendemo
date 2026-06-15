---
title: Self-Distillation
summary: Knowledge transfer from deeper layers to shallower layers within the same model, improving small model performance by 15-20%.
updated: 2026-06-05
tags:
  - llm
  - optimization
  - distillation
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/optimization/self-distillation/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Self-Distillation

Self-Distillation transfers knowledge from deeper model layers to shallower layers without requiring a larger teacher model.

## Core Principle

```
Traditional Knowledge Distillation:
  Teacher (large model) → Soft labels → Student (small model)
  Problem: Requires trained large model as teacher

Self-Distillation:
  Deep layers → Knowledge → Shallow layers
  Core: Knowledge transfer between different layers of the same model
```

## Self-Distillation Mechanism

```python
class SelfDistillationLoss(nn.Module):
    def __init__(self, alpha=0.5, temperature=2.0):
        super().__init__()
        self.alpha = alpha
        self.temperature = temperature
        
    def forward(self, student_logits, deep_features, shallow_features):
        ce_loss = F.cross_entropy(student_logits, labels)
        kd_loss = self.compute_kd_loss(deep_features, shallow_features)
        soft_loss = self.compute_soft_loss(student_logits)
        return self.alpha * ce_loss + (1 - self.alpha) * (kd_loss + soft_loss)
```

## Implementation

```python
class SelfDistillationTransformer(nn.Module):
    def __init__(self, d_model, n_heads, n_layers):
        super().__init__()
        self.layers = nn.ModuleList([
            TransformerLayer(d_model, n_heads) 
            for _ in range(n_layers)
        ])
        self.temperature = 2.0
        
    def forward(self, x):
        layer_outputs = []
        for i, layer in enumerate(self.layers):
            x = layer(x)
            layer_outputs.append(x)
        return x, layer_outputs
    
    def compute_self_distillation_loss(self, outputs, layer_outputs, labels):
        total_loss = 0
        teacher_layer = len(layer_outputs) - 1
        
        for student_layer in range(teacher_layer):
            teacher_out = layer_outputs[teacher_layer]
            student_out = layer_outputs[student_layer]
            align_loss = F.mse_loss(student_out, teacher_out.detach())
            total_loss += align_loss
        
        logits = outputs
        soft_labels = F.softmax(logits / self.temperature, dim=-1)
        soft_loss = F.kl_div(
            F.log_softmax(logits / self.temperature, dim=-1),
            soft_labels,
            reduction='batchmean'
        ) * (self.temperature ** 2)
        
        ce_loss = F.cross_entropy(F.log_softmax(logits, dim=-1), labels)
        return 0.5 * ce_loss + 0.3 * total_loss + 0.2 * soft_loss
```

## Training Protocol

```python
def self_distillation_training(model, train_loader, epochs=10):
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    for epoch in range(epochs):
        for batch in train_loader:
            outputs, layer_outputs = model(batch['input'])
            loss = model.compute_self_distillation_loss(
                outputs, layer_outputs, batch['labels']
            )
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
```

## Performance Comparison

| Model | Baseline PPL | +Self-Distillation | Improvement |
|-------|-------------|-------------------|-------------|
| 7B (from scratch) | 18.5 | - | - |
| 7B (standard finetune) | 14.2 | 13.1 | 7.7% |
| 3B (standard finetune) | 22.1 | 18.6 | 15.8% |
| 1B (standard finetune) | 28.5 | 22.3 | 21.7% |

## Usage

```bash
python train_self_distillation.py \
    --model llama-3b \
    --epochs 10 \
    --alpha 0.5 \
    --temperature 2.0
python evaluate.py --model distilled_3b --task mmlu
```

## Key Takeaways

1. **No teacher required**: Eliminates need for pretrained large model
2. **Deep to shallow**: Deep layer representations serve as soft targets
3. **Multi-layer alignment**: All shallow layers align to deepest layer
4. **More effective for small models**: Smaller models benefit more

## Related

- [[entities/sparsegpt-pruning]] - Structured pruning
- [[entities/awq-quantization]] - Quantization methods
- [[entities/tech-stacks]] - LLM optimization stack
