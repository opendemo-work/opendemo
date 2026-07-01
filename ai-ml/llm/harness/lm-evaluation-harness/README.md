<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# LM-Evaluation-Harness 实战

> 本案例详解如何使用 LM-Evaluation-Harness 对大模型进行全面评测

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│              LM-Evaluation-Harness 架构                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   User Interface                        │   │
│  │                                                          │   │
│  │   lm_eval \                                              │   │
│  │     --model hf \                                         │   │
│  │     --model_args pretrained=mymodel \                   │   │
│  │     --tasks mmlu \                                      │   │
│  │     --batch_size 8                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Task Registry                          │   │
│  │                                                          │   │
│  │   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │   │  MMLU   │ │HumanEval │ │  GSM8K   │ │   BBH    │  │   │
│  │   └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Model Interface                         │   │
│  │                                                          │   │
│  │   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │   │HuggingFace│ │   vLLM   │ │  GPTQ    │ │   OAI    │  │   │
│  │   └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Evaluator                              │   │
│  │                                                          │   │
│  │   • Exact Match (EM)                                    │   │
│  │   • Pass@k                                               │   │
│  │   • Perplexity (PPL)                                    │   │
│  │   • BLEU / ROUGE                                        │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│                       Results / Logs                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

评测流程:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. Task Definition (YAML)                                      │
│     ┌─────────────────────────────────────────────────────┐     │
│     │  dataset_name: mmlu                                 │     │
│     │  dataset_config_name: all                          │     │
│     │  num_fewshot: 5                                    │     │
│     │  metric: multiple_choice_grade                      │     │
│     └─────────────────────────────────────────────────────┘     │
│                              │                                  │
│                              ▼                                  │
│  2. Dataset Loading                                             │
│                              │                                  │
│                              ▼                                  │
│  3. Prompt Construction (Few-shot)                             │
│                              │                                  │
│                              ▼                                  │
│  4. Model Inference                                             │
│                              │                                  │
│                              ▼                                  │
│  5. Metrics Calculation                                         │
│                              │                                  │
│                              ▼                                  │
│  6. Results Aggregation                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 支持的任务类型

| 任务类型 | 说明 | 评测指标 |
|----------|------|----------|
| **Multiple Choice** | 多选题 | Accuracy |
| **Code Generation** | 代码生成 | Pass@k, EM |
| **Math Reasoning** | 数学推理 | Exact Match |
| **Language Modeling** | 语言建模 | Perplexity |
| **Summarization** | 摘要 | ROUGE, BLEU |
| **Translation** | 翻译 | BLEU, chrF |

### 2. 常用 Benchmark

| Benchmark | 任务类型 | 说明 |
|-----------|----------|------|
| MMLU | 多选题 | 57 个学科选择题 |
| HumanEval | 代码生成 | 164 道 Python 题 |
| GSM8K | 数学 | 8.5K 小学数学题 |
| BBH | 综合 | 23 个 BIG-Bench 难题 |
| TruthfulQA | 真实性 | 817 个问答对 |
| MT-Bench | 对话 | 多轮对话 |

### 3. Pass@k 指标

```python
def pass_at_k(n, c, k):
    """计算 Pass@k
    
    n: 总生成数量
    c: 通过数量
    k: 每题生成 k 个样本
    """
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)
```

## 💻 完整实现

### 安装与配置

```bash
# 安装 lm-evaluation-harness
pip install lm-eval

# 或者从源码安装
git clone https://github.com/EleutherAI/lm-evaluation-harness
cd lm-evaluation-harness
pip install -e .

# 验证安装
lm_eval --version
```

### 基本评测命令

```bash
# 评测 HuggingFace 模型
lm_eval \
    --model hf \
    --model_args pretrained=mymodel,tokenizer=mytokenizer \
    --tasks mmlu,arc_easy \
    --batch_size 8

# 评测 vLLM 模型
lm_eval \
    --model vllm \
    --model_args pretrained=mymodel,tensor_parallel_size=4 \
    --tasks humaneval,mbpp \
    --batch_size 16

# 评测 OpenAI 模型
lm_eval \
    --model openai \
    --model_args model=gpt-4,api_key=$OPENAI_API_KEY \
    --tasks mmlu,gsm8k
```

### Python API 评测

```python
from lm_eval import evaluator, tasks, models

def evaluate_model():
    """使用 Python API 评测模型"""
    
    # 1. 配置模型
    model_config = {
        "pretrained": "meta-llama/Llama-2-7b-hf",
        "tokenizer": "meta-llama/Llama-2-7b-hf",
        "device": "cuda",
        "dtype": "bfloat16",
    }

    # 2. 配置任务
    task_list = ["mmlu", "arc_easy", "truthfulqa"]
    
    # 3. 运行评测
    results = evaluator.simple_evaluate(
        model="hf",
        model_args=model_config,
        tasks=task_list,
        batch_size=8,
        limit=100,  # 限制样本数用于快速测试
        device="cuda",
        num_fewshot=5,
    )

    # 4. 输出结果
    print(evaluator.make_table(results))
    
    # 5. 保存结果
    import json
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results
```

### 自定义任务配置

```yaml
# tasks/my_custom_task.yaml
task: my_custom_task
dataset_path: mydataset
dataset_name: main
output_type: multiple_choice
test_split: test
num_fewshot: 5

metrics:
  - name: multiple_choice_grade
    display_name: Accuracy

doc_to_text: "{{question}}\n\nChoices:"
doc_to_target: "{{answer}}"
doc_to_choice: "{{options}}"

validation_split: val
fewshot_split: train
```

### 批量评测脚本

```python
#!/usr/bin/env python3
# batch_evaluate.py

import os
import json
import subprocess
from datetime import datetime

MODELS = [
    "meta-llama/Llama-2-7b-hf",
    "mistralai/Mistral-7B-v0.1",
    "Qwen/Qwen2-7B",
]

TASKS = [
    "mmlu",
    "arc_easy",
    "truthfulqa",
    "gsm8k",
]

def run_evaluation(model_name: str, task: str) -> dict:
    """运行单次评测"""
    print(f"\n{'='*60}")
    print(f"Evaluating: {model_name} on {task}")
    print(f"{'='*60}\n")
    
    output_file = f"results/{model_name.replace('/', '_')}_{task}.json"
    
    cmd = [
        "lm_eval",
        "--model", "hf",
        "--model_args", f"pretrained={model_name}",
        "--tasks", task,
        "--batch_size", "8",
        "--limit", "100",  # 快速测试用
        "--output_path", f"results/{task}",
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 小时超时
        )
        
        # 解析结果
        results_file = f"results/{task}/results.json"
        if os.path.exists(results_file):
            with open(results_file) as f:
                return json.load(f)
                
    except subprocess.TimeoutExpired:
        return {"error": "Timeout"}
    except Exception as e:
        return {"error": str(e)}
    
    return {}

def main():
    # 创建结果目录
    os.makedirs("results", exist_ok=True)
    
    all_results = {}
    
    for model in MODELS:
        all_results[model] = {}
        for task in TASKS:
            result = run_evaluation(model, task)
            all_results[model][task] = result
    
    # 保存汇总结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = f"results/summary_{timestamp}.json"
    
    with open(summary_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nResults saved to {summary_file}")

if __name__ == "__main__":
    main()
```

## 📊 评测结果解读

### 典型输出格式

```
================================================================================
                                      Task                  |         Dataset |  Metrics (n=100)
================================================================================
                               arc_easy |   arc_easy |   acc: 0.8500
                                     mmlu |       mmlu |   acc: 0.6800
                               truthfulqa | truthfulqa |   acc: 0.5500
                                   gsm8k |      gsm8k |   exact_match,strict-match: 0.5200
================================================================================
```

### 结果分析

```python
def analyze_results(results: dict):
    """分析评测结果"""
    
    # 按任务分组
    task_scores = {}
    for task_name, task_results in results["results"].items():
        metrics = task_results.get("metrics", {})
        task_scores[task_name] = {
            "accuracy": metrics.get("acc", 0),
            "exact_match": metrics.get("exact_match", 0),
        }
    
    # 找出最优和最差任务
    sorted_tasks = sorted(task_scores.items(), key=lambda x: x[1]["accuracy"])
    
    print("Best performing tasks:")
    for task, scores in sorted_tasks[-3:]]:
        print(f"  {task}: {scores}")
    
    print("\nWorst performing tasks:")
    for task, scores in sorted_tasks[:3]:
        print(f"  {task}: {scores}")
    
    return task_scores
```

## 📋 命令速查

```bash
# 安装
pip install lm-eval

# 快速评测 MMLU
lm_eval --model hf --model_args pretrained=mymodel --tasks mmlu

# 多任务评测
lm_eval --model hf --model_args pretrained=mymodel \
    --tasks mmlu,arc_easy,arc_challenge,boolq, Copa, rte, sciq, piqa, hella_swag, winogrande

# 代码能力评测
lm_eval --model vllm --model_args pretrained=codellama --tasks humaneval,mbpp

# 数学能力评测
lm_eval --model hf --model_args pretrained=mymodel --tasks gsm8k,math

# 查看支持的模型
lm_eval --list_models

# 查看支持的任务
lm_eval --list_tasks
```

## 📚 学习要点

1. **任务选择**：根据目标场景选择合适的 benchmark
2. **Few-shot 配置**：不同任务需要不同的 few-shot 数量
3. **Batch Size**：合理设置避免 OOM
4. **Limit 参数**：快速测试时限制样本数

## 🔗 相关案例

- `mmlu-evaluation` - MMLU 评测详解
- `humaneval-evaluation` - HumanEval 代码评测
- `mt-bench-evaluation` - MT-Bench 对话评测
- `safety-evaluation` - Safety 安全性评测

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
