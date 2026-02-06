# 大语言模型微调实战演示

## 🎯 学习目标

通过本案例你将掌握：
- 大语言模型微调的基本概念和方法
- 使用LoRA、P-Tuning等参数高效微调技术
- 数据集准备和预处理技巧
- 微调过程中的性能优化和资源管理

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- GPU环境（推荐NVIDIA GPU，CUDA 11.0+）
- 至少16GB内存，推荐32GB+

### 依赖安装
```bash
pip install torch transformers datasets accelerate peft bitsandbytes
pip install trl wandb  # 用于训练和实验跟踪
```

## 📁 项目结构

```
llm-fine-tuning-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── prepare_dataset.py             # 数据集准备脚本
│   ├── fine_tune_model.py             # 模型微调脚本
│   └── evaluate_model.py              # 模型评估脚本
├── configs/                           # 配置文件
│   ├── lora_config.json               # LoRA配置
│   ├── training_config.json           # 训练配置
│   └── quantization_config.json       # 量化配置
├── data/                              # 数据文件
│   ├── raw/                           # 原始数据
│   ├── processed/                     # 处理后数据
│   └── splits/                        # 训练/验证/测试分割
├── models/                            # 模型文件
│   ├── base_models/                   # 基础模型
│   ├── fine_tuned/                    # 微调后模型
│   └── checkpoints/                   # 检查点
└── notebooks/                         # Jupyter笔记本
    ├── 01_data_preparation.ipynb     # 数据准备
    ├── 02_model_fine_tuning.ipynb    # 模型微调
    └── 03_evaluation.ipynb           # 模型评估
```

## 🚀 快速开始

### 步骤1：数据准备

```bash
# 准备微调数据集
python scripts/prepare_dataset.py \
  --input_file data/raw/train.jsonl \
  --output_dir data/processed/ \
  --task_type classification
```

### 步骤2：模型微调

```bash
# 使用LoRA进行参数高效微调
python scripts/fine_tune_model.py \
  --model_name_or_path facebook/opt-350m \
  --dataset_path data/processed/ \
  --output_dir models/fine_tuned/ \
  --peft_method lora \
  --lora_r 16 \
  --lora_alpha 32 \
  --lora_dropout 0.05 \
  --num_epochs 3 \
  --batch_size 4 \
  --gradient_accumulation_steps 4
```

### 步骤3：模型评估

```bash
# 评估微调后模型性能
python scripts/evaluate_model.py \
  --model_path models/fine_tuned/ \
  --test_dataset data/processed/test.jsonl \
  --metrics accuracy f1
```

## 🔍 代码详解

### 核心概念解析

#### 1. 参数高效微调技术
```python
# LoRA (Low-Rank Adaptation)
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,  # 低秩矩阵的秩
    lora_alpha=32,  # 缩放因子
    target_modules=["q_proj", "v_proj"],  # 目标模块
    lora_dropout=0.05,  # dropout概率
    bias="none",  # 是否训练偏置
    task_type="CAUSAL_LM"  # 任务类型
)

model = get_peft_model(model, lora_config)
```

#### 2. 实际应用示例

##### 场景1：指令微调
```python
# 使用Alpaca-style指令微调
def format_instruction(example):
    """格式化指令数据"""
    return f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""

# 准备指令数据集
dataset = dataset.map(lambda x: {"text": format_instruction(x)})
```

##### 场景2：领域适应
```python
# 针对特定领域的微调
def domain_adaptation_training():
    """领域适应训练流程"""
    # 1. 加载基础模型
    model = AutoModelForCausalLM.from_pretrained(base_model_path)
    
    # 2. 应用LoRA适配器
    model = get_peft_model(model, lora_config)
    
    # 3. 准备领域特定数据
    train_dataset = prepare_domain_data(domain_data_path)
    
    # 4. 训练
    trainer = Trainer(
        model=model,
        train_dataset=train_dataset,
        args=training_args,
        data_collator=data_collator
    )
    
    trainer.train()
```

## 🧪 验证测试

### 测试1：微调流程验证
```python
#!/usr/bin/env python
# 验证微调流程
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def test_fine_tuning_pipeline():
    print("=== 大语言模型微调流程测试 ===")
    
    # 加载基础模型和tokenizer
    model_name = "facebook/opt-350m"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # 验证tokenizer功能
    test_text = "Hello, world!"
    tokens = tokenizer(test_text)
    print(f"✅ Tokenizer功能正常，输入: '{test_text}', 输出token数量: {len(tokens['input_ids'])}")
    
    # 验证模型前向传播
    inputs = tokenizer(test_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    print(f"✅ 模型前向传播正常，logits形状: {outputs.logits.shape}")

if __name__ == "__main__":
    test_fine_tuning_pipeline()
```

### 测试2：LoRA适配器验证
```python
#!/usr/bin/env python
# 验证LoRA适配器
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

def test_lora_adapter():
    print("=== LoRA适配器测试 ===")
    
    # 加载模型
    model = AutoModelForCausalLM.from_pretrained("facebook/opt-350m")
    
    # 配置LoRA
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # 应用LoRA
    model = get_peft_model(model, lora_config)
    
    # 检查参数数量
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print(f"✅ LoRA适配器应用成功")
    print(f"总参数: {total_params:,}")
    print(f"可训练参数: {trainable_params:,}")
    print(f"参数效率: {(trainable_params/total_params)*100:.2f}%")

if __name__ == "__main__":
    test_lora_adapter()
```

## ❓ 常见问题

### Q1: 如何选择合适的LoRA参数？
**解决方案**：
```python
# LoRA参数选择指南
"""
- r (rank): 一般选择8, 16, 32, 64。较小的r值更参数高效，较大的r值可能有更好的表现。
- lora_alpha: 通常设为2*r或4*r。控制缩放程度。
- lora_dropout: 0.05或0.1，防止过拟合。
- target_modules: 通常针对Q、V投影矩阵，也可以包括其他线性层。
"""
```

### Q2: 如何处理内存不足问题？
**解决方案**：
```python
# 内存优化策略
from transformers import BitsAndBytesConfig

# 4-bit量化
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)
```

## 📚 扩展学习

### 相关技术
- **QLoRA**: 4-bit量化LoRA，进一步减少内存使用
- **P-Tuning**: 连续提示学习方法
- **Adapter**: 插入式适配器方法
- **Prefix-Tuning**: 前缀微调方法

### 进阶学习路径
1. 掌握不同微调方法的特点和适用场景
2. 学习高效的数据预处理和增强技术
3. 理解模型评估和性能优化策略
4. 掌握分布式训练和推理优化

### 企业级应用场景
- 个性化客服机器人微调
- 行业知识库问答系统
- 文本摘要和生成应用
- 代码生成和理解模型

---
> **💡 提示**: 大语言模型微调是将通用模型适应特定任务或领域的重要技术，通过参数高效微调方法可以在保持模型性能的同时显著减少计算资源需求。