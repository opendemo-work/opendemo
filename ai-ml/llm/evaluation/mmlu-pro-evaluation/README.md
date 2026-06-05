# MMLU-Pro 高难度评测

> 本案例详解 MMLU-Pro 评测数据集和评估方法

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      MMLU-Pro 评测架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MMLU-Pro 数据集 (更难的选择题)                                    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  题目来源                                                │   │
│  │  ├── MMLU 原题 (保留)                                    │   │
│  │  ├── GPQA 精选 (研究生水平)                             │   │
│  │  └── 专家标注新题                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  难度特征                                                │   │
│  │  ├── 选项数量: 4 → 10 (增加干扰项)                       │   │
│  │  ├── 需要多步推理                                        │   │
│  │  └── 更深学科知识                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  评测设置                                                │   │
│  │  ├── 5-shot (与 MMLU 一致)                               │   │
│  │  ├── Chain-of-Thought 提示                               │   │
│  │  └── 10-way 选择题                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. MMLU-Pro 与 MMLU 对比

| 特征 | MMLU | MMLU-Pro |
|------|------|----------|
| 题目数 | ~15,000 | ~12,000 |
| 选项数 | 4 | 10 |
| 难度 | 中等 | 高 |
| 推理需求 | 单步 | 多步 |
| 随机准确率 | 25% | 10% |

### 2. 评测设置

```python
# MMLU-Pro 评测配置
MMLU_PRO_CONFIG = {
    "num_fewshot": 5,
    "num_choices": 10,         # 10 个选项
    "metric": "multiple_choice_grade",
    "include_reasoning": True, # CoT 提示
}

# 答案提取（更复杂）
"""
从模型输出中提取 0-9 的选项索引
- 需要更健壮的提取逻辑
- 处理更长的推理过程
"""
```

## 💻 完整实现

### MMLU-Pro 数据集加载

```python
from datasets import load_dataset

def load_mmlu_pro():
    """加载 MMLU-Pro 数据集"""
    
    dataset = load_dataset(
        "cais/mmlu",
        "mmlu_pro",
        split="test"
    )
    
    return dataset


def format_prompt_pro(question: dict, fewshot_examples: list):
    """格式化 MMLU-Pro 提示词"""
    
    prompt = f"Solve the following problem step by step.\n\n"
    
    # 添加 few-shot 示例（带推理）
    for ex in fewshot_examples:
        prompt += f"Question: {ex['question']}\n"
        prompt += f"Options:\n"
        for i, choice in enumerate(ex['options']):
            prompt += f"  {i}. {choice}\n"
        prompt += f"Reasoning: {ex['reasoning']}\n"
        prompt += f"Answer: {ex['answer']}\n\n"
    
    # 添加测试问题
    prompt += f"Question: {question['question']}\n"
    prompt += f"Options:\n"
    for i, choice in enumerate(question['options']):
        prompt += f"  {i}. {choice}\n"
    prompt += f"Reasoning: "
    
    return prompt
```

### MMLU-Pro 评测实现

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def evaluate_mmlu_pro(
    model_name: str,
    num_fewshot: int = 5,
    batch_size: int = 8
):
    """完整 MMLU-Pro 评测"""
    
    # 加载模型
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    
    # 加载数据
    dataset = load_mmlu_pro()
    fewshot_data = load_mmlu_pro(split="train")
    
    correct = 0
    total = 0
    
    for i in range(len(dataset)):
        question = dataset[i]
        fewshot_examples = fewshot_data[:num_fewshot]
        
        # 格式化 prompt
        prompt = format_prompt_pro(question, fewshot_examples)
        
        # 生成（更长输出以支持 CoT）
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False
            )
        
        # 提取答案
        generated = tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True
        )
        predicted = extract_answer_pro(generated)
        
        if predicted == question["answer"]:
            correct += 1
        total += 1
    
    accuracy = correct / total
    print(f"MMLU-Pro Accuracy: {accuracy:.4f} ({correct}/{total})")
    
    return {"accuracy": accuracy, "correct": correct, "total": total}


def extract_answer_pro(generated: str) -> int:
    """从模型输出中提取答案索引"""
    import re
    
    # 匹配 "Answer: X" 或 "The answer is X"
    patterns = [
        r"Answer:\s*(\d+)",
        r"The answer is\s*(\d+)",
        r"^\s*(\d+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, generated)
        if match:
            return int(match.group(1))
    
    return -1
```

## 📊 结果分析

### 典型结果

| 模型 | MMLU | MMLU-Pro | 下降幅度 |
|------|------|----------|----------|
| GPT-4 | 86% | 72% | -14% |
| Claude-3 | 88% | 70% | -18% |
| LLaMA-65B | 68% | 45% | -23% |
| LLaMA-7B | 48% | 28% | -20% |

### 难度分析

```python
def analyze_mmlu_pro_results(results: dict):
    """分析 MMLU-Pro 结果"""
    
    # 按学科分组
    subjects = ["physics", "chemistry", "mathematics", "law", "medicine"]
    
    for subject in subjects:
        subject_results = {k: v for k, v in results.items() if subject in k}
        avg_accuracy = sum(r["accuracy"] for r in subject_results.values()) / len(subject_results)
        print(f"{subject}: {avg_accuracy:.2%}")
```

## 📋 命令速查

```bash
# 使用 lm-evaluation-harness 评测
lm_eval \
    --model hf \
    --model_args pretrained=mymodel \
    --tasks mmlu_pro \
    --batch_size 8 \
    --num_fewshot 5

# 10-way 选择题
lm_eval \
    --model hf \
    --model_args pretrained=mymodel \
    --tasks mmlu_pro_10way
```

## 📚 学习要点

1. **更高难度**：MMLU-Pro 通过增加选项和题目难度更好区分顶级模型
2. **CoT 重要性**：10-way 选择题更需要链式推理
3. **结果解读**：准确率下降 15-20% 是正常的，说明评测更严格
4. **模型排序**：在 MMLU-Pro 上的排序可能与 MMLU 不同

## 🔗 相关案例

- `mmlu-evaluation` - MMLU 标准评测
- `truthfulqa-evaluation` - TruthfulQA 真实性评测
- `gsm8k-evaluation` - GSM8K 数学推理评测
