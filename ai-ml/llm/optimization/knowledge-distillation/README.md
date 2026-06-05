# Knowledge Distillation 知识蒸馏

> 本案例详解 Knowledge Distillation 技术，从大模型提取知识到小模型

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Knowledge Distillation                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Teacher Model (大模型)                                          │
│       │                                                         │
│       ├── Soft Labels (温度 softmax) ──────────────────┐       │
│       │                                                         │       │
│       ▼                                                         ▼       │
│  Student Model (小模型)                    KL Divergence Loss   │
│       │                                                         │       │
│       └── Hard Labels ──▶ Cross Entropy Loss ──────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

蒸馏类型:

┌─────────────────────────────────────────────────────────────────┐
│  Response Distillation: 直接用 teacher 的输出监督                 │
│  Feature Distillation: 用 teacher 的中间层特征                   │
│  MiniMax Distillation: 自研方法，关注 teacher 的思考过程        │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 核心实现

### 蒸馏损失

```python
def distillation_loss(student_logits, teacher_logits, labels, T=2.0, alpha=0.5):
    """知识蒸馏损失"""
    # Soft loss (KL Divergence)
    soft_loss = F.kl_div(
        F.log_softmax(student_logits / T, dim=-1),
        F.softmax(teacher_logits / T, dim=-1),
        reduction='batchmean'
    ) * (T * T)
    
    # Hard loss (Cross Entropy)
    hard_loss = F.cross_entropy(student_logits, labels)
    
    # 组合
    return alpha * soft_loss + (1 - alpha) * hard_loss
```

## 🔗 相关案例

- `llm-compression-demo` - 模型压缩
- `lora-fine-tuning` - LoRA 微调
- `int4-quantization` - INT4 量化
