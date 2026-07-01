<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# SFT 监督微调基础

> 本案例详解 SFT (Supervised Fine-Tuning) 的核心原理、数据构建、训练策略

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    SFT 完整流程                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 预训练模型 (Pretrained Model)                               │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              指令数据 (Instruction Data)                  │   │
│  │                                                          │   │
│  │   ┌─────────────────────────────────────────────────┐  │   │
│  │   │  System: You are a helpful assistant.           │  │   │
│  │   │  User: What is Python?                           │  │   │
│  │   │  Assistant: Python is a programming language...  │  │   │
│  │   └─────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 SFT Training                             │   │
│  │                                                          │   │
│  │   Loss = CrossEntropy(output_tokens, target_tokens)      │   │
│  │   只计算 Assistant 部分的 loss                            │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  2. SFT 模型 (Instruct Model)                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

数据格式对比:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ChatML Format (推荐):                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ <|im_start|>system                                      │   │
│  │ You are a helpful assistant.<|im_end|>                   │   │
│  │ <|im_start|>user                                        │   │
│  │ What is Python?<|im_end|>                               │   │
│  │ <|im_start|>assistant                                   │   │
│  │ Python is a programming language...<|im_end|>            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Llama 2 Format:                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ [INST] <<SYS>>                                          │   │
│  │ You are a helpful assistant.                            │   │
│  │ <</SYS>>                                               │   │
│  │                                                         │   │
│  │ What is Python? [/INST]                                 │   │
│  │ Python is a programming language...                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. SFT vs Pretraining

| 阶段 | 数据 | 目标 | Loss |
|------|------|------|------|
| Pretrain | 互联网文本 | 语言建模 | All tokens |
| SFT | 指令数据 | 遵循指令 | Assistant tokens |

### 2. 指令数据格式

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."}
  ]
}
```

### 3. SFT 关键配置

```python
sft_config = {
    "learning_rate": 1e-5 to 3e-5,     # 比预训练低
    "batch_size": 4 to 16,
    "epochs": 2 to 5,                   # 避免过拟合
    "warmup_ratio": 0.03 to 0.1,
    "lr_scheduler": "cosine",
    "max_seq_length": 4096,
    "gradient_accumulation_steps": 4,
}
```

## 💻 完整实现

### 数据处理

```python
from dataclasses import dataclass
from typing import List, Dict
import torch

@dataclass
class Conversation:
    """对话数据"""
    messages: List[Dict[str, str]]
    
    def to_string(self, format: str = "chatml") -> str:
        """转换为字符串格式"""
        if format == "chatml":
            return self.to_chatml()
        elif format == "llama2":
            return self.to_llama2()
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def to_chatml(self) -> str:
        """ChatML 格式"""
        result = ""
        for msg in self.messages:
            role = msg["role"]
            content = msg["content"]
            result += f"<|im_start|>{role}\n{content}<|im_end|>\n"
        return result
    
    def to_llama2(self) -> str:
        """Llama 2 格式"""
        result = ""
        for i, msg in enumerate(self.messages):
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                result += f"[INST] <<SYS>>\n{content}\n<</SYS>>\n\n"
            elif role == "user":
                if i > 0:
                    result += f"[/INST]\n{content}\n[INST]"
                else:
                    result += f"[INST]{content}[/INST]\n"
            elif role == "assistant":
                result += f"{content}\n"
        return result


def preprocess_dataset(
    dataset: List[Dict],
    tokenizer,
    max_length: int = 4096
) -> torch.utils.data.Dataset:
    """预处理指令数据集"""
    
    class SFTDataset(torch.utils.data.Dataset):
        def __init__(self, data):
            self.data = data
        
        def __len__(self):
            return len(self.data)
        
        def __getitem__(self, idx):
            item = self.data[idx]
            
            # 构建对话
            conv = Conversation(item["messages"])
            text = conv.to_string("chatml") + "<|im_start|>assistant\n"
            
            # Tokenize
            encodings = tokenizer(
                text,
                max_length=max_length,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            )
            
            input_ids = encodings["input_ids"].squeeze()
            attention_mask = encodings["attention_mask"].squeeze()
            
            # 创建 labels (只在 assistant 部分计算 loss)
            labels = input_ids.clone()
            
            # 找到 assistant 开始位置
            assistant_token = tokenizer.encode("<|im_start|>assistant\n", add_special_tokens=False)
            
            # 找到最后一个 assistant 标记
            last_assistant_idx = 0
            for i in range(len(input_ids) - len(assistant_token)):
                if input_ids[i:i+len(assistant_token)].tolist() == assistant_token:
                    last_assistant_idx = i + len(assistant_token)
            
            # assistant 之前的位置 loss 设为 -100
            labels[:last_assistant_idx] = -100
            
            return {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "labels": labels
            }
    
    return SFTDataset(dataset)
```

### SFT 训练

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model

def train_sft_model(
    model_name: str,
    train_dataset,
    eval_dataset,
    output_dir: str,
    use_lora: bool = True,
    lora_rank: int = 8,
    num_epochs: int = 3,
    learning_rate: float = 2e-4,
    batch_size: int = 4,
):
    """SFT 训练"""
    
    # 加载模型和 tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    
    # 应用 LoRA (推荐，节省显存)
    if use_lora:
        lora_config = LoraConfig(
            r=lora_rank,
            lora_alpha=2 * lora_rank,
            target_modules=[
                "q_proj", "v_proj", "k_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj"
            ],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
    
    # 数据整理器
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        padding=True,
        return_tensors="pt"
    )
    
    # 训练参数
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        logging_steps=10,
        save_strategy="epoch",
        bf16=True,
        gradient_checkpointing=True,
        optim="paged_adamw_32bit",
        max_grad_norm=0.3,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )
    
    # 开始训练
    trainer.train()
    
    # 保存模型
    trainer.save_model(f"{output_dir}/final_model")
    
    return model, tokenizer
```

### 使用 TRL 库

```python
from trl import SFTTrainer
from datasets import load_dataset

# 加载数据
dataset = load_dataset("your-instruction-dataset", split="train")

# 训练
trainer = SFTTrainer(
    model="meta-llama/Llama-2-7b-hf",
    train_dataset=dataset,
    dataset_text_field="text",  # 或 "messages"
    max_seq_length=4096,
    args=training_args,
)

trainer.train()
```

## 📊 SFT 数据集资源

| 数据集 | 规模 | 质量 | 来源 |
|--------|------|------|------|
| Alpaca | 52K | 中 | GPT-3.5 生成 |
| Vicuna | 70K | 中高 | 用户共享 |
| ShareGPT | 100K+ | 高 | 真实用户 |
| WizardLM | 250K | 高 | 指令进化 |
| UltraChat | 1.5M | 高 | 多轮对话 |
| OpenOrca | 4.2M | 高 | FLAN 生成 |

## 📋 命令速查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用 transformers 训练
python sft/train.py \
    --model_name meta-llama/Llama-2-7b \
    --dataset_path ./data/train.json \
    --output_dir ./output/sft_model \
    --num_epochs 3 \
    --batch_size 4 \
    --use_lora

# 使用 PEFT 加载
python sft/load_lora.py --lora_path ./output/sft_model
```

## 📚 学习要点

1. **只计算 Assistant Loss**：避免 System/User 部分影响训练
2. **数据质量关键**：SFT 效果很大程度上取决于数据质量
3. **避免过拟合**：epoch 不要太多，2-3 通常足够
4. **LoRA 推荐**：SFT 使用 LoRA 可以大幅节省显存

## 🔗 相关案例

- `lora-fine-tuning` - LoRA 微调
- `rlhf-introduction` - RLHF 对齐
- `dpo-training` - DPO 直接偏好优化
- `q-lora-tuning` - QLoRA 高效微调

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
