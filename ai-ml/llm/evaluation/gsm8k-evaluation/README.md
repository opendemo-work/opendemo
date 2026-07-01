<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# GSM8K 数学推理评测

> 本案例详解 GSM8K (Grade School Math 8K) 评测数据集和评估方法

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      GSM8K 评测架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GSM8K 数据集 (8,500 道小学数学题)                               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  难度分布                                                │   │
│  │  ├── Grade 3: 40%                                       │   │
│  │  ├── Grade 4: 30%                                       │   │
│  │  ├── Grade 5: 20%                                       │   │
│  │  └── Grade 6: 10%                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  评测流程                                                │   │
│  │                                                           │   │
│  │  Question ──→ Model (CoT) ──→ Reasoning ──→ Answer      │   │
│  │                 │                                         │   │
│  │                 └──→ Final Number Extraction             │   │
│  │                                                           │   │
│  │  Answer Match ──→ Pass / Fail                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Chain-of-Thought 提示                                   │   │
│  │                                                           │   │
│  │  Q: "Tom has 5 apples, buys 3 more, gives away 2..."     │   │
│  │  A: "Step 1: Tom starts with 5 apples"                   │   │
│  │     "Step 2: He buys 3 more, so 5 + 3 = 8"              │   │
│  │     "Step 3: He gives away 2, so 8 - 2 = 6"             │   │
│  │     "Step 4: Final answer is 6"                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. GSM8K 数据集结构

| 统计 | 数值 |
|------|------|
| 总题目数 | 8,592 |
| 训练集 | 7,473 |
| 测试集 | 1,319 |
| 平均解题步骤 | 2-5 步 |
| 需要多步运算 | 100% |

### 2. 评测设置

```python
# GSM8K 评测配置
GSM8K_CONFIG = {
    "num_fewshot": 5,
    "metric": "exact_match",
    "max_new_tokens": 512,
    "chain_of_thought": True,
}

# 答案匹配
"""
- 先提取最终答案数字
- 与标准答案比较（允许小误差）
- 需要处理货币、百分比等格式
"""

# 答案提取模式
"""
Answer: 42
The answer is 42
42
"""
```

## 💻 完整实现

### GSM8K 数据集加载

```python
from datasets import load_dataset

def load_gsm8k():
    """加载 GSM8K 数据集"""
    
    train_data = load_dataset("openai/gsm8k", "main", split="train")
    test_data = load_dataset("openai/gsm8k", "main", split="test")
    
    return {
        "train": train_data,
        "test": test_data
    }


def format_prompt(question: str, fewshot_examples: list):
    """格式化 GSM8K 提示词（带 CoT）"""
    
    prompt = "Solve the following math problem step by step.\n\n"
    
    # 添加 few-shot 示例（带解题过程）
    for ex in fewshot_examples:
        prompt += f"Problem: {ex['question']}\n"
        prompt += f"Solution:\n{ex['answer']}\n\n"
    
    # 添加测试问题
    prompt += f"Problem: {question}\n"
    prompt += "Solution:\n"
    
    return prompt


def extract_final_number(answer: str) -> float:
    """从答案中提取最终数字"""
    import re
    
    # 清理答案
    answer = answer.strip()
    
    # 提取最后一个数字（通常是最终答案）
    numbers = re.findall(r'-?\d+\.?\d*', answer)
    
    if numbers:
        return float(numbers[-1])
    
    return None
```

### GSM8K 评测实现

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def evaluate_gsm8k(
    model_name: str,
    num_fewshot: int = 5,
    batch_size: int = 8
):
    """完整 GSM8K 评测"""
    
    # 加载模型
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    
    # 加载数据
    dataset = load_gsm8k()
    train_data = dataset["train"]
    test_data = dataset["test"]
    
    fewshot_examples = train_data.select(range(num_fewshot))
    
    correct = 0
    total = 0
    results = []
    
    for i in range(len(test_data)):
        question = test_data[i]["question"]
        
        # 格式化 prompt
        prompt = format_prompt(question, list(fewshot_examples))
        
        # 生成
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False
            )
        
        # 提取答案
        generated = tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True
        )
        
        # 提取最终数字
        predicted = extract_final_number(generated)
        ground_truth = extract_final_number(test_data[i]["answer"])
        
        # 判断正确
        is_correct = (predicted is not None and 
                     ground_truth is not None and 
                     abs(predicted - ground_truth) < 0.01)
        
        if is_correct:
            correct += 1
        
        total += 1
        
        results.append({
            "question": question,
            "predicted": predicted,
            "ground_truth": ground_truth,
            "correct": is_correct,
            "full_response": generated
        })
    
    accuracy = correct / total if total > 0 else 0
    print(f"GSM8K Accuracy: {accuracy:.4f} ({correct}/{total})")
    
    return {"accuracy": accuracy, "results": results}
```

### 使用 Chain-of-Thought 提示

```python
def format_cot_prompt(question: str, examples: list):
    """Chain-of-Thought 提示模板"""
    
    prompt = "Let's solve this problem step by step.\n\n"
    
    for ex in examples:
        prompt += f"Q: {ex['question']}\n"
        prompt += f"A: "
        
        # 解析答案中的步骤
        solution = ex['answer']
        prompt += solution + "\n\n"
    
    prompt += f"Q: {question}\n"
    prompt += f"A: "
    
    return prompt


def evaluate_with_cot(model, tokenizer, dataset, num_fewshot=5):
    """使用 CoT 评测"""
    
    train_data = load_gsm8k()["train"]
    
    correct = 0
    total = 0
    
    for item in dataset["test"]:
        prompt = format_cot_prompt(
            item["question"],
            list(train_data.select(range(num_fewshot)))
        )
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        outputs = model.generate(**inputs, max_new_tokens=512)
        
        generated = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:])
        
        # 提取答案并比较
        if is_answer_correct(generated, item["answer"]):
            correct += 1
        
        total += 1
    
    return correct / total
```

## 📊 结果分析

### 典型结果

| 模型 | GSM8K (5-shot) | GSM8K (CoT) |
|------|----------------|-------------|
| GPT-3 | 46% | 55% |
| GPT-3.5 | 68% | 76% |
| GPT-4 | 87% | 92% |
| PaLM-2 | 80% | 86% |
| LLaMA-65B | 58% | 67% |

### 错误分析

```python
def analyze_gsm8k_errors(results: dict):
    """分析 GSM8K 错误类型"""
    
    error_types = {
        "calculation_error": 0,
        "reasoning_error": 0,
        "misunderstanding": 0,
        "other": 0
    }
    
    for result in results["results"]:
        if not result["correct"]:
            error_type = classify_error(result["full_response"])
            error_types[error_type] += 1
    
    print("=== Error Distribution ===")
    for error_type, count in error_types.items():
        print(f"{error_type}: {count}")
```

## 📋 命令速查

```bash
# 使用 lm-evaluation-harness 评测
lm_eval \
    --model hf \
    --model_args pretrained=mymodel \
    --tasks gsm8k \
    --batch_size 8 \
    --num_fewshot 5

# 带 Chain-of-Thought
lm_eval \
    --model hf \
    --model_args pretrained=mymodel \
    --tasks gsm8k_cot \
    --batch_size 8

# Python API
python -c "
from lm_eval import evaluator
results = evaluator.simple_evaluate(
    model='hf',
    model_args=dict(pretrained='mymodel'),
    tasks=['gsm8k'],
    num_fewshot=5
)
print(evaluator.make_table(results))
"
```

## 📚 学习要点

1. **Chain-of-Thought**：CoT 提示显著提升数学推理效果
2. **多步推理**：GSM8K 需要 2-5 步推理，不能直接得答案
3. **答案提取**：需要从推理过程中提取最终数字
4. **易错点**：计算错误和推理跳跃是最常见的错误类型

## 🔗 相关案例

- `mmlu-evaluation` - MMLU 语言理解评测
- `mbpp-evaluation` - MBPP 编程评测
- `mmlu-pro-evaluation` - MMLU-Pro 高难度评测

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

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

```bash
python code/main.py
```
