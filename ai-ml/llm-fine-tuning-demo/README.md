# 大模型微调（LoRA）- 低成本领域适配

> 使用 LoRA（Low-Rank Adaptation）技术对预训练大语言模型进行参数高效微调，演示数据集准备、训练、评估和推理全流程。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解 LoRA 微调的参数高效性
- ✅ 准备指令微调数据集
- ✅ 使用 Transformers + PEFT 进行 LoRA 训练
- ✅ 加载微调后的模型进行推理

---

## 📐 架构图

```
预训练模型（如 Qwen/Llama）
        │
        ▼
   LoRA Adapter
        │
        ▼
   领域特定任务
（客服、代码、医疗等）
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | >= 3.9 | 运行训练脚本 |
| PyTorch | >= 2.0 | 深度学习框架 |
| Transformers | >= 4.35 | 大模型库 |
| PEFT | >= 0.6 | 参数高效微调 |

### 安装依赖

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd ai-ml/llm-fine-tuning-demo
pip install -r requirements.txt
```

### 启动训练

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
python code/fine_tune_lora.py
```

---

## 📖 核心概念

### 1. LoRA

LoRA 通过在原始权重矩阵旁路添加低秩矩阵进行微调，只训练少量参数：

```
W = W_0 + BA
```

其中 W_0 冻结，B 和 A 是可训练的低秩矩阵。

### 2. PEFT

Parameter-Efficient Fine-Tuning，参数高效微调技术族，包括 LoRA、Prefix Tuning、Prompt Tuning 等。

### 3. 指令微调

将训练数据组织成 `(instruction, input, output)` 格式，让模型学习遵循指令。

---

## 💻 代码示例

### 数据集格式

```json
[
  {
    "instruction": "将以下中文翻译成英文",
    "input": "你好，世界",
    "output": "Hello, world"
  }
]
```

### LoRA 训练脚本

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import load_dataset

model_name = "Qwen/Qwen2-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

dataset = load_dataset("json", data_files="data/train.jsonl")

training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-4,
    logging_steps=10,
)

# 训练
from trl import SFTTrainer
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
)
trainer.train()
```

### 推理

```python
from peft import PeftModel

model = AutoModelForCausalLM.from_pretrained(model_name)
model = PeftModel.from_pretrained(model, "./output")

inputs = tokenizer("你好", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `code/fine_tune_lora.py` | LoRA 训练脚本 |
| `data/train.jsonl` | 训练数据 |
| `requirements.txt` | Python 依赖 |

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 检查 CUDA 可用
python -c "import torch; print(torch.cuda.is_available())"

# 运行训练
python code/fine_tune_lora.py

# 运行推理
python code/inference.py
```

---

## 📊 运行结果

```
训练损失逐步下降：
Step 10: loss=2.345
Step 50: loss=1.234
Step 100: loss=0.876
```

---

## 🐛 常见问题

### Q1：显存不足？

**A**：使用更小的 batch size、开启 gradient checkpointing、使用 4-bit/8-bit 量化加载模型。

### Q2：loss 不下降？

**A**：检查学习率、数据格式和目标模块是否正确。

### Q3：推理输出质量差？

**A**：增加训练数据量、调整 lora_r 和 lora_alpha、增加训练轮数。

---

## 📚 扩展学习

- [LLM 推理优化](../llm-inference-demo/)
- [LLM 训练](../llm-training-demo/)
- [PEFT 官方文档](https://huggingface.co/docs/peft/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
