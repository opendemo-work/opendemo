<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# MMLU 多任务语言理解评测

> 本案例详解 MMLU (Massive Multitask Language Understanding) 评测数据集和评估方法

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        MMLU 评测架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MMLU 数据集 (57 个学科)                                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  STEM (25%)                                              │   │
│  │  ├── Mathematics (2.5%)                                  │   │
│  │  ├── Physics (2.5%)                                      │   │
│  │  ├── Chemistry (2.5%)                                    │   │
│  │  └── ...                                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Social Sciences (25%)                                   │   │
│  │  ├── History (5%)                                        │   │
│  │  ├── Economics (5%)                                      │   │
│  │  └── ...                                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Humanities (25%)                                       │   │
│  │  ├── Philosophy (5%)                                     │   │
│  │  ├── Law (5%)                                            │   │
│  │  └── ...                                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Other (25%)                                             │   │
│  │  ├── Business (5%)                                       │   │
│  │  ├── Medicine (5%)                                       │   │
│  │  └── ...                                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  5-shot Examples (从同类别中采样)                        │   │
│  │                                                           │   │
│  │  Q: What is the capital of France?                      │   │
│  │  A: Paris                                                │   │
│  │                                                           │   │
│  │  Q: [Test Question]                                      │   │
│  │  A: [Model Prediction]                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

评测流程:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Input:                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  The following are multiple choice questions (with       │   │
│  │  answers) about high school mathematics.                │   │
│  │                                                           │   │
│  │  Simplify: 3 + 5 * 2                                     │   │
│  │  A. 13                                                   │   │
│  │  B. 16                                                   │   │
│  │  C. 25                                                   │   │
│  │  D. 10                                                   │   │
│  │  Answer: A                                               │   │
│  │                                                           │   │
│  │  [More 5-shot examples...]                               │   │
│  │                                                           │   │
│  │  What is 8 + 4 * 3?                                      │   │
│  │  A. 20                                                   │   │
│  │  B. 36                                                   │   │
│  │  C. 24                                                   │   │
│  │  D. 12                                                   │   │
│  │  Answer:                                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│                      ┌──────────────┐                           │
│                      │    LLM       │                           │
│                      └──────┬───────┘                           │
│                             │                                   │
│                             ▼                                   │
│  Output: A (自动提取选项字母)                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. MMLU 数据集结构

| 统计 | 数值 |
|------|------|
| 总题目数 | 15,908 |
| 学科数量 | 57 |
| 平均每学科 | ~279 题 |
| 测试集 | 14,042 题 |
| 验证集 | 1,866 题 |

### 2. 学科分类

```
STEM (25%)
├── Mathematics (2.5%): abstract algebra, college mathematics, ...
├── Physics (2.5%): high school physics, college physics, ...
├── Chemistry (2.5%): high school chemistry, college chemistry, ...
└── Computer Science (2.5%): machine learning, cybersecurity, ...

Social Sciences (25%)
├── History (5%): world history, us history, european history, ...
├── Economics (5%): macroeconomics, microeconomics, ...
└── ...

Humanities (25%)
├── Philosophy (5%): formal logic, moral scenarios, ...
├── Law (5%): professional law, ...
└── ...

Other (25%)
├── Business (5%): business ethics, management, ...
├── Medicine (5%): anatomy, clinical knowledge, ...
└── ...
```

### 3. 评测设置

```python
# MMLU 评测配置
MMLU_CONFIG = {
    "num_fewshot": 5,           # 使用 5 个同类别例子
    "metric": "multiple_choice_grade",
    "batch_size": 8,
    "max_length": 512,
}

# Few-shot 采样策略
"""
对于每个测试问题，从同类别中采样 5 个例子作为 few-shot 示例
例如：测试 "college_mathematics" 时，从 mathematics 类别采样
"""

# 答案提取
"""
从模型输出中提取选项字母：
- "The answer is A"
- "A"
- "(A)"
- 提取第一个匹配 [A-Z] 的字母
"""
```

## 💻 完整实现

### MMLU 数据集加载

```python
from datasets import load_dataset
import json

def load_mmlu():
    """加载 MMLU 数据集"""
    
    # 加载所有 sub-subjects
    all_data = {}
    
    # MMLU 的 subject 列表
    subjects = [
        "abstract_algebra", "anatomy", "astronomy", "business_ethics",
        "clinical_knowledge", "college_biology", "college_chemistry",
        "college_computer_science", "college_mathematics", "college_medicine",
        "college_physics", "computer_security", "conceptual_physics",
        "econometrics", "electrical_engineering", "elementary_mathematics",
        "formal_logic", "global_facts", "high_school_biology",
        "high_school_chemistry", "high_school_computer_science",
        "high_school_european_history", "high_school_geography",
        "high_school_macroeconomics", "high_school_mathematics",
        "high_school_microeconomics", "high_school_physics",
        "high_school_psychology", "high_school_statistics",
        "high_school_us_history", "high_school_world_history",
        "human_aging", "human_sexuality", "international_law",
        "jurisprudence", "logical_fallacies", "machine_learning",
        "management", "marketing", "medical_genetics", "miscellaneous",
        "moral_disputes", "moral_scenarios", "nutrition", "philosophy",
        "prehistory", "professional_accounting", "professional_law",
        "professional_medicine", "professional_nursing", "professional_psychology",
        "public_relations", "security_studies", "sociology", "us_foreign_policy",
        "virology", "world_religions"
    ]
    
    for subject in subjects:
        try:
            dataset = load_dataset(
                "cais/mmlu",
                subject,
                split="test"
            )
            all_data[subject] = dataset
        except Exception as e:
            print(f"Failed to load {subject}: {e}")
    
    return all_data


def get_fewshot_examples(subject: str, num_shots: int = 5):
    """获取 few-shot 示例（从验证集采样）"""
    val_dataset = load_dataset(
        "cais/mmlu",
        subject,
        split="val"
    )
    
    # 随机采样
    examples = []
    for i in range(min(num_shots, len(val_dataset))):
        item = val_dataset[i]
        examples.append({
            "question": item["question"],
            "choices": item["choices"],
            "answer": item["answer"]
        })
    
    return examples


def format_prompt(subject: str, question: dict, fewshot_examples: list):
    """格式化 MMLU 提示词"""
    
    # Subject 描述
    subject_descriptions = {
        "abstract_algebra": "abstract algebra",
        "anatomy": "anatomy",
        "astronomy": "astronomy",
        # ... 更多映射
    }
    
    subject_name = subject_descriptions.get(subject, subject.replace("_", " "))
    
    prompt = f"The following are multiple choice questions (with answers) about {subject_name}.\n\n"
    
    # 添加 few-shot 示例
    for ex in fewshot_examples:
        prompt += f"{ex['question']}\n"
        for i, choice in enumerate(ex['choices']):
            prompt += f"{chr(65+i)}. {choice}\n"
        prompt += f"Answer: {chr(65+ex['answer'])}\n\n"
    
    # 添加测试问题
    prompt += f"{question['question']}\n"
    for i, choice in enumerate(question['choices']):
        prompt += f"{chr(65+i)}. {choice}\n"
    prompt += "Answer:"
    
    return prompt
```

### MMLU 评测实现

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

def evaluate_mmlu(
    model_name: str,
    subjects: list = None,
    num_fewshot: int = 5,
    batch_size: int = 8,
    limit: int = None
):
    """完整 MMLU 评测"""
    
    # 加载模型
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    
    # 加载数据
    all_data = load_mmlu()
    
    # 限制 subject 数量
    if subjects:
        all_data = {k: v for k, v in all_data.items() if k in subjects}
    
    results = {}
    
    for subject, dataset in tqdm(all_data.items(), desc="Evaluating subjects"):
        
        fewshot_examples = get_fewshot_examples(subject, num_fewshot)
        
        correct = 0
        total = 0
        
        # 限制测试样本数
        test_range = range(min(len(dataset), limit)) if limit else range(len(dataset))
        
        for i in test_range:
            question = {
                "question": dataset[i]["question"],
                "choices": dataset[i]["choices"]
            }
            correct_answer = dataset[i]["answer"]
            
            # 格式化 prompt
            prompt = format_prompt(subject, question, fewshot_examples)
            
            # 生成
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=1,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # 提取答案
            generated = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            predicted_answer = extract_answer(generated)
            
            if predicted_answer == chr(65 + correct_answer):
                correct += 1
            
            total += 1
        
        accuracy = correct / total if total > 0 else 0
        results[subject] = {
            "accuracy": accuracy,
            "correct": correct,
            "total": total
        }
        print(f"{subject}: {accuracy:.4f} ({correct}/{total})")
    
    # 计算总体准确率
    all_correct = sum(r["correct"] for r in results.values())
    all_total = sum(r["total"] for r in results.values())
    results["_overall"] = {
        "accuracy": all_correct / all_total,
        "correct": all_correct,
        "total": all_total
    }
    
    return results


def extract_answer(generated: str) -> str:
    """从模型输出中提取答案字母"""
    import re
    
    # 匹配模式
    patterns = [
        r'^([A-Z])',
        r'^The answer is ([A-Z])',
        r'([A-Z])\.',
        r'\(([A-Z])\)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, generated.strip())
        if match:
            return match.group(1)
    
    # 如果没有匹配，返回第一个大写字母
    for char in generated.strip()[:10]:
        if char.isalpha() and char.isupper():
            return char
    
    return ""
```

### 使用 lm_eval 评测

```bash
# 使用 lm-evaluation-harness 评测
lm_eval \
    --model hf \
    --model_args pretrained=meta-llama/Llama-2-7b-hf \
    --tasks mmlu \
    --batch_size 8 \
    --num_fewshot 5

# 只评测特定 subject
lm_eval \
    --model hf \
    --model_args pretrained=mymodel \
    --tasks mmlu_abstract_algebra,mmlu_high_school_mathematics \
    --batch_size 8

# MMLU-Pro (更难版本)
lm_eval \
    --model hf \
    --model_args pretrained=mymodel \
    --tasks mmlu_pro
```

## 📊 结果分析

### 典型结果

| 模型 | MMLU | STEM | Social Sciences | Humanities | Other |
|------|------|------|-----------------|------------|-------|
| Random | 25% | 25% | 25% | 25% | 25% |
| GPT-2 | 32% | 28% | 35% | 33% | 31% |
| LLaMA-7B | 48% | 42% | 51% | 46% | 51% |
| LLaMA-65B | 68% | 60% | 72% | 64% | 73% |
| GPT-4 | 86% | 84% | 88% | 85% | 87% |

### 结果解读

```python
def analyze_mmlu_results(results: dict):
    """分析 MMLU 结果"""
    
    # 按类别分组
    categories = {
        "STEM": ["mathematics", "physics", "chemistry", "computer_science"],
        "Social Sciences": ["history", "economics", "psychology", "sociology"],
        "Humanities": ["philosophy", "law"],
        "Other": ["business", "medicine", "miscellaneous"]
    }
    
    category_scores = {}
    
    for category, subjects in categories.items():
        scores = []
        for subject in subjects:
            if subject in results:
                scores.append(results[subject]["accuracy"])
        category_scores[category] = sum(scores) / len(scores) if scores else 0
    
    print("\n=== Category Analysis ===")
    for category, score in sorted(category_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"{category}: {score:.2%}")
    
    # 找出最强和最弱学科
    sorted_subjects = sorted(
        [(k, v["accuracy"]) for k, v in results.items() if k != "_overall"],
        key=lambda x: x[1]
    )
    
    print("\n=== Strongest Subjects ===")
    for subject, score in sorted_subjects[-5:]:
        print(f"{subject}: {score:.2%}")
    
    print("\n=== Weakest Subjects ===")
    for subject, score in sorted_subjects[:5]:
        print(f"{subject}: {score:.2%}")
```

## 📋 命令速查

```bash
# 评测 MMLU
lm_eval --model hf --model_args pretrained=mymodel --tasks mmlu

# 评测 MMLU-Pro (更难)
lm_eval --model hf --model_args pretrained=mymodel --tasks mmlu_pro

# 评测特定学科
lm_eval --model hf --model_args pretrained=mymodel \
    --tasks mmlu_high_school_mathematics,mmlu_physics

# Python API
python -c "
from lm_eval import evaluator;
results = evaluator.simple_evaluate(
    model='hf',
    model_args=dict(pretrained='mymodel'),
    tasks=['mmlu'],
    num_fewshot=5
);
print(evaluator.make_table(results))
"
```

## 📚 学习要点

1. **Few-shot 关键**：MMLU 使用 5-shot，few-shot 示例必须来自同类别
2. **答案提取**：需要处理多种输出格式
3. **学科差异**：不同学科难度差异大，STEM 通常最难
4. **模型选择**：MMLU 是检验模型综合能力的重要指标

## 🔗 相关案例

- `mmlu-pro-evaluation` - MMLU-Pro 高难度评测
- `humaneval-evaluation` - HumanEval 代码评测
- `bbh-evaluation` - BBH 难题评测
- `truthfulqa-evaluation` - TruthfulQA 真实性评测

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
