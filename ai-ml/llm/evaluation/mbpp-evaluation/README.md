<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# MBPP 编程评测

> 本案例详解 MBPP (Mostly Basic Python Problems) 评测数据集和评估方法

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                       MBPP 评测架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MBPP 数据集 (约 1000 道编程题)                                  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  题目类型                                                │   │
│  │  ├── 基础语法 (20%)                                      │   │
│  │  ├── 数据结构操作 (30%)                                  │   │
│  │  ├── 算法实现 (30%)                                      │   │
│  │  └── 字符串处理 (20%)                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  评测模式                                                │   │
│  │  ├── Sanitized (标准化函数签名)                          │   │
│  │  ├── Unsanitized (原始函数签名)                           │   │
│  │  └── 3-shot / 0-shot                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  评测流程                                                │   │
│  │                                                           │   │
│  │  Prompt ──→ Model ──→ Code ──→ Execute ──→ Pass/Fail    │   │
│  │                   │              │                       │   │
│  │                   │              └──→ 单元测试验证       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. MBPP 数据集结构

| 统计 | 数值 |
|------|------|
| 总题目数 | 974 |
| 训练集 | 500 |
| 测试集 | 500 |
| 平均代码长度 | ~15 行 |
| 平均测试用例 | 3-5 个 |

### 2. 评测指标

```python
# MBPP 评测指标
MBPP_CONFIG = {
    "num_prompt_examples": 3,   # 3-shot
    "metric": "pass_at_k",     # Pass@K 指标
    "k_values": [1, 10, 100],  # K 值
    "timeout": 5,              # 执行超时(秒)
}

# Pass@K 定义
"""
Pass@K: 生成 K 次代码，至少有一次通过所有测试用例的概率估计
pass@1 = 一次生成通过率
pass@10 = 10次生成至少一次通过率
"""

# 无偏估计
"""
pass@k = 1 - C(n-c, k) / C(n, k)
n: 总生成数, c: 通过数
"""
```

## 💻 完整实现

### MBPP 数据集加载

```python
from datasets import load_dataset

def load_mbpp():
    """加载 MBPP 数据集"""
    
    # 加载完整数据集
    mbpp_full = load_dataset("mbpp", split="full")
    
    # 加载 sanitized 版本（标准函数签名）
    mbpp_test = load_dataset("mbpp", split="test")
    mbpp_train = load_dataset("mbpp", split="train")
    
    return {
        "full": mbpp_full,
        "test": mbpp_test,
        "train": mbpp_train
    }


def format_prompt(problem: dict, fewshot_examples: list):
    """格式化 MBPP 提示词"""
    
    prompt = "Solve the following Python problem:\n\n"
    
    # 添加 few-shot 示例
    for ex in fewshot_examples:
        prompt += f"Problem: {ex['text']}\n"
        prompt += f"Code: {ex['code']}\n\n"
    
    # 添加测试问题
    prompt += f"Problem: {problem['text']}\n"
    prompt += "Code: "
    
    return prompt


def get_test_cases(problem: dict) -> list:
    """获取测试用例"""
    return problem["test_list"]
```

### MBPP 评测实现

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import Counter

def evaluate_mbpp(
    model_name: str,
    num_prompt: int = 3,
    num_samples: int = 100,
    temperature: float = 0.8,
    k_values: list = [1, 10]
):
    """MBPP 评测实现"""
    
    # 加载模型
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    
    # 加载数据
    dataset = load_mbpp()
    train_data = dataset["train"]
    test_data = dataset["test"]
    
    results = {}
    
    for i in range(min(num_samples, len(test_data))):
        problem = test_data[i]
        
        # 获取 few-shot 示例
        fewshot = train_data[:num_prompt]
        
        # 格式化 prompt
        prompt = format_prompt(problem, fewshot)
        
        # 生成代码
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=True,
                temperature=temperature,
                num_return_sequences=max(k_values)
            )
        
        # 提取代码
        generated_codes = [
            tokenizer.decode(outputs[j][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            for j in range(len(outputs))
        ]
        
        # 执行测试
        passed = execute_tests(problem, generated_codes, k_values)
        
        results[i] = {
            "problem": problem["text"],
            "passed_at_1": passed[0],
            "passed_at_10": passed[9] if 10 in k_values else None
        }
    
    # 计算总体 Pass@K
    pass_at_k = calculate_pass_at_k(results, k_values)
    
    return {"results": results, "pass_at_k": pass_at_k}


def execute_tests(problem: dict, generated_codes: list, k_values: list) -> dict:
    """执行测试用例"""
    import subprocess
    import sys
    
    passed_counts = {k: 0 for k in k_values}
    
    for code in generated_codes[:max(k_values)]:
        try:
            # 构造完整代码
            full_code = f"""
{problem['code']}
{code}
"""
            
            # 执行测试
            exec_globals = {}
            exec(full_code, exec_globals)
            
            # 运行测试用例
            for test_case in problem["test_list"]:
                result = eval(test_case, exec_globals)
                if not result:
                    break
            else:
                # 所有测试通过
                for k in k_values:
                    if passed_counts[k] == 0:  # 第一次通过
                        passed_counts[k] = 1
                        break
                        
        except Exception as e:
            continue
    
    return passed_counts


def calculate_pass_at_k(results: dict, k_values: list) -> dict:
    """计算 Pass@K"""
    
    pass_at_k = {}
    
    for k in k_values:
        total = len(results)
        passed = sum(1 for r in results.values() if r.get(f"passed_at_{k}"))
        pass_at_k[f"pass@{k}"] = passed / total if total > 0 else 0
    
    return pass_at_k
```

## 📊 结果分析

### 典型结果

| 模型 | Pass@1 | Pass@10 | Pass@100 |
|------|--------|---------|----------|
| GPT-3 | 45% | 62% | 71% |
| Codex | 72% | 86% | 94% |
| CodeGen | 48% | 67% | 78% |
| StarCoder | 52% | 69% | 80% |

### 结果解读

```python
def analyze_mbpp_results(results: dict, pass_at_k: dict):
    """分析 MBPP 结果"""
    
    print("=== MBPP Results ===")
    for k, v in pass_at_k.items():
        print(f"{k}: {v:.2%}")
    
    # 按问题类型分析
    by_difficulty = {
        "easy": [],
        "medium": [],
        "hard": []
    }
    
    for idx, result in results.items():
        if "string" in result["problem"].lower():
            category = "easy"
        elif "sort" in result["problem"].lower() or "search" in result["problem"].lower():
            category = "medium"
        else:
            category = "hard"
        
        by_difficulty[category].append(result["passed_at_1"])
    
    for cat, scores in by_difficulty.items():
        avg = sum(scores) / len(scores) if scores else 0
        print(f"{cat}: {avg:.2%}")
```

## 📋 命令速查

```bash
# 使用 lm-evaluation-harness 评测
lm_eval \
    --model hf \
    --model_args pretrained=mymodel \
    --tasks mbpp \
    --batch_size 8

# 3-shot 设置
lm_eval \
    --model hf \
    --model_args pretrained=mymodel \
    --tasks mbpp \
    --num_fewshot 3

# Python API
python -c "
from lm_eval import evaluator
results = evaluator.simple_evaluate(
    model='hf',
    model_args=dict(pretrained='mymodel'),
    tasks=['mbpp']
)
print(evaluator.make_table(results))
"
```

## 📚 学习要点

1. **Pass@K 指标**：MBPP 使用 Pass@K 而非准确率，反映生成多样性
2. **Few-shot 重要性**：3-shot 显著提升效果
3. **代码执行**：需要沙箱环境执行生成的代码
4. **Sanitized vs Unsanitized**：标准函数签名使评测更稳定

## 🔗 相关案例

- `humaneval-evaluation` - HumanEval 代码评测
- `mmlu-evaluation` - MMLU 语言理解评测
- `gsm8k-evaluation` - GSM8K 数学推理评测

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
