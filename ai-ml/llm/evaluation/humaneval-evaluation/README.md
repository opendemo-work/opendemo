# HumanEval 代码评测

> 本案例详解 HumanEval 基准测试，理解代码生成模型的能力评估方法

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    HumanEval 数据集结构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HumanEval 包含 164 道 Python 编程题                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Task ID: 0                                              │   │
│  │  Canonical Solution:                                     │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │  def has_close_elements(numbers: List[float],   │   │   │
│  │  │                           threshold: float) -> bool:   │   │
│  │  │      for i, n1 in enumerate(numbers):           │   │   │
│  │  │          for j, n2 in enumerate(numbers):        │   │   │
│  │  │              if i != j and abs(n1 - n2) < threshold:   │   │
│  │  │                  return True                      │   │   │
│  │  │      return False                                 │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  Test Cases:                                            │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │  assert has_close_elements([1.0, 2.0, 3.0], 0.5)   │   │   │
│  │  │  assert not has_close_elements([1.0, 2.0, 3.0], 0.1) │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Pass@k 评测流程:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  对每道题:                                                      │
│                                                                 │
│  1. 生成 k 个候选代码                                           │
│     ┌─────────────────────────────────────────────────────────┐ │
│     │  Prompt → [Code 1] [Code 2] ... [Code k]               │ │
│     └─────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  2. 逐个运行测试用例                                           │
│     ┌─────────────────────────────────────────────────────────┐ │
│     │  Code 1: ✓ pass                                        │ │
│     │  Code 2: ✗ fail (assertion error)                      │ │
│     │  Code 3: ✓ pass                                        │ │
│     │  ...                                                   │ │
│     └─────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  3. 计算 Pass@k                                                │
│     ┌─────────────────────────────────────────────────────────┐ │
│     │  Pass@1 = 正确数 / k (k=1时)                          │ │
│     │  Pass@10 = 正确数 / k (k=10时)                        │ │
│     │  Pass@100 = 正确数 / k (k=100时)                       │ │
│     └─────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

代码评测的特殊性:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  自然语言 vs 代码生成:                                          │
│                                                                 │
│  自然语言:                                                      │
│  - 答案相对模糊                                                 │
│  - 可以人工评估或 LLM 评估                                      │
│  - 边界情况少                                                  │
│                                                                 │
│  代码生成:                                                      │
│  - 必须正确执行                                                 │
│  - 必须通过测试用例                                             │
│  - 需要处理边界情况                                             │
│  - 性能也是评估维度                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. HumanEval 数据集

| 统计 | 数值 |
|------|------|
| 总题数 | 164 |
| 题目来源 | OpenAI 人工编写 |
| 难度 | LeetCode Easy-Medium |
| 平均长度 | ~50 tokens |
| 函数签名 | 有类型标注 |

### 2. Pass@k 指标

```python
import math

def pass_at_k(n: int, c: int, k: int) -> float:
    """
    计算 Pass@k
    
    n: 总生成数量 (通常为 c 的 k 倍)
    c: 通过的正确代码数量
    k: 每个问题生成 k 个候选
    
    公式: 1 - C(n-c, k) / C(n, k)
    """
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)

# 示例: 生成 200 个, 通过 100 个, k=10
# Pass@10 = 1 - C(100, 10) / C(200, 10) ≈ 0.73
```

### 3. 常见 Benchmark

| Benchmark | 题数 | 语言 | 特点 |
|-----------|------|------|------|
| HumanEval | 164 | Python | 官方基线 |
| MBPP | 974 | Python | 更多样化 |
| APPS | 5000+ | 多语言 | 竞赛级别 |
| MultiPL-E | 2000+ | 多语言 | 多语言测试 |
| BigCodeBench | 1140 | 多语言 | 真实任务 |

## 💻 完整实现

### HumanEval 评测实现

```python
import json
import tempfile
import subprocess
import multiprocessing
from typing import List, Dict, Callable
from dataclasses import dataclass

@dataclass
class HumanEvalItem:
    """HumanEval 题目"""
    task_id: str
    prompt: str
    canonical_solution: str
    test: str
    entry_point: str


def load_humaneval() -> List[HumanEvalItem]:
    """加载 HumanEval 数据集"""
    with open("data/HumanEval.json", "r") as f:
        data = json.load(f)
    return [HumanEvalItem(**item) for item in data]


def evaluate_code(
    code: str,
    test_code: str,
    timeout: int = 5
) -> Dict[str, any]:
    """运行代码测试"""
    
    # 组合完整程序
    full_program = code + "\n\n" + test_code
    
    # 执行
    try:
        result = subprocess.run(
            ["python", "-c", full_program],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            return {"passed": True, "error": None}
        else:
            return {"passed": False, "error": result.stderr}
    
    except subprocess.TimeoutExpired:
        return {"passed": False, "error": "Timeout"}
    except Exception as e:
        return {"passed": False, "error": str(e)}


def generate_with_llm(
    prompt: str,
    model_fn: Callable,
    temperature: float = 0.8,
    max_tokens: int = 256,
) -> str:
    """使用 LLM 生成代码"""
    
    response = model_fn(
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=["\nclass ", "\ndef ", "\n#", "\nif "]
    )
    
    return response


def evaluate_humaneval(
    model_fn: Callable,
    dataset: List[HumanEvalItem],
    k_values: List[int] = [1, 10, 100],
    num_samples_per_task: int = 200,
) -> Dict[str, float]:
    """
    评估 HumanEval
    
    Args:
        model_fn: LLM 调用函数
        dataset: HumanEval 数据集
        k_values: 要计算的 k 值列表
        num_samples_per_task: 每题生成的候选数
    """
    
    results = {}
    for k in k_values:
        results[f"pass@{k}"] = []
    
    for item in dataset:
        # 构建 prompt
        prompt = f"Complete the following Python function:\n\n{item.prompt}\n\n"
        
        # 生成多个候选
        candidates = []
        for _ in range(num_samples_per_task):
            code = generate_with_llm(prompt, model_fn, temperature=0.8)
            candidates.append(code)
        
        # 计算不同 k 下的通过数
        for k in k_values:
            correct = 0
            for candidate in candidates[:k]:
                result = evaluate_code(candidate, item.test)
                if result["passed"]:
                    correct += 1
                    break  # 只要有一个通过就行
            
            # 计算该 k 值下的通过率
            pass_rate = correct / len(candidates[:k])
            results[f"pass@{k}"].append(pass_rate)
    
    # 计算平均
    return {k: sum(v) / len(v) for k, v in results.items()}


# 使用示例
def example_model_fn(prompt: str, **kwargs) -> str:
    """示例 LLM 调用"""
    from openai import OpenAI
    client = OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        **kwargs
    )
    
    return response.choices[0].message.content


# 运行评测
dataset = load_humaneval()
results = evaluate_humaneval(example_model_fn, dataset)
print(results)
# {'pass@1': 0.45, 'pass@10': 0.72, 'pass@100': 0.85}
```

### 使用 lm_eval

```bash
# 安装
pip install lm-eval

# 评测
lm_eval \
    --model openai \
    --model_args model=gpt-4 \
    --tasks humaneval \
    --batch_size 10

# 评测本地模型
lm_eval \
    --model hf \
    --model_args pretrained=codellama/CodeLlama-7b-Instruct-hf \
    --tasks humaneval \
    --batch_size 8
```

### 使用 BigCode-Evaluation-Harness

```python
# 使用 BigCode 的评测框架
from bigcode_eval import Evaluator

evaluator = Evaluator(
    model=model,
    tokenizer=tokenizer,
    tasks=["humaneval", "mbpp"],
    temperature=0.8,
    n_samples=200,
)

results = evaluator.evaluate()
print(results["humaneval"]["pass@10"])
```

## 📊 主流模型结果

| 模型 | Pass@1 | Pass@10 | Pass@100 |
|------|--------|---------|----------|
| Codex (OpenAI) | 28% | 47% | 71% |
| CodeGen | 31% | 50% | 73% |
| PaLM-Coder | 35% | 53% | 76% |
| GPT-4 | 67% | 85% | 93% |
| Claude 3 | 62% | 82% | 91% |
| DeepSeek-Coder | 70% | 86% | 94% |

## 📋 命令速查

```bash
# 使用 lm_eval 评测
lm_eval --model hf --model_args pretrained=codellama --tasks humaneval

# 使用 BigCode 框架
python -m bigcode_eval --model codellama --tasks humaneval

# 评测多个 benchmark
lm_eval --model hf --tasks humaneval,mbpp,apps
```

## 📚 学习要点

1. **Pass@k 指标**：允许生成多个候选，通过任一个即可
2. **测试用例驱动**：代码必须通过测试才算正确
3. **Temperature 影响**：高 temperature 有利于 Pass@100
4. **生成多样性**：k 越大，通过率越高

## 🔗 相关案例

- `mmlu-evaluation` - MMLU 评测
- `mt-bench-evaluation` - MT-Bench 对话评测
- `safety-evaluation` - Safety 评测
- `llm-as-judge` - LLM-as-Judge
