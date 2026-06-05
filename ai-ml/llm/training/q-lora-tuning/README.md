# QLoRA 高效微调

> 本案例详解 QLoRA (Quantized LoRA) 技术，在消费级 GPU 上微调大模型

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    QLoRA 核心原理                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  传统 LoRA:                                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  4-bit NF4 Quantized Model (冻结)                      │   │
│  │         │                                               │   │
│  │         ▼                                               │   │
│  │  LoRA Adapters (可训练, BF16)                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  显存对比:                                                     │
│  LLaMA 7B FP16: 14GB                                        │
│  LLaMA 7B + LoRA: 14GB + ~100MB                             │
│  LLaMA 7B QLoRA: 3.5GB + ~100MB                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 核心实现

### QLoRA 配置

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    llm_int8_threshold=6.0,
    llm_int8_has_fp16_weight=False,
)
```

### 训练脚本

```python
from peft import get_peft_model, LoraConfig, TaskType

# 加载量化模型
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
)

# 配置 LoRA
lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

## 🔗 相关案例

- `lora-fine-tuning` - LoRA 微调
- `int4-quantization` - INT4 量化
- `fp8-quantization` - FP8 量化
