<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Pairwise Comparison 评测

> 本案例详解 Pairwise Comparison (成对比较) 评测方法

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                   Pairwise Comparison 评测架构                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  成对比较评测流程                                                │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  输入                                                    │   │
│  │  ┌─────────────────┐    ┌─────────────────┐              │   │
│  │  │  Model A Output │    │  Model B Output │              │   │
│  │  │  (Response A)   │    │  (Response B)   │              │   │
│  │  └─────────────────┘    └─────────────────┘              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                    │
│                           ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Judge Prompt                                           │   │
│  │                                                           │   │
│  │  "Which response is better?"                             │   │
│  │  "[Response A]"                                          │   │
│  │  "[Response B]"                                          │   │
│  │                                                           │   │
│  │  Options: A wins / B wins / Tie                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                    │
│                           ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Elo Rating System                                      │   │
│  │                                                           │   │
│  │  Rating_A' = Rating_A + K * (S - E)                      │   │
│  │  E = 1 / (1 + 10^((Rating_B - Rating_A) / 400))         │   │
│  │                                                           │   │
│  │  S = 1 (win), 0.5 (tie), 0 (lose)                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. Pairwise Comparison 方法

| 特征 | 说明 |
|------|------|
| 核心思想 | 让模型成对比较两个回答，判断哪个更好 |
| Judge 模型 | GPT-4, Claude 等强模型作为评判 |
| 输出类型 | A wins, B wins, Tie |
| 优势 | 避免绝对评分的不一致性 |

### 2. Elo Rating 系统

```python
# Elo 评分系统
ELO_CONFIG = {
    "k_factor": 32,           # 调整系数
    "initial_rating": 1500,   # 初始分数
    "rating_periods": 100,    # 评估轮数
}

# 期望胜率
"""
E_A = 1 / (1 + 10^((R_B - R_A) / 400))

当 R_A = 1500, R_B = 1500 时, E_A = 0.5
当 R_A = 1600, R_B = 1500 时, E_A = 0.64
当 R_A = 1500, R_B = 1600 时, E_A = 0.36
"""

# 评分更新
"""
R_new = R_old + K * (S - E)

R_old: 当前分数
K: 调整系数(通常32)
S: 实际结果(1/0.5/0)
E: 期望胜率
"""
```

## 💻 完整实现

### Pairwise Comparison 数据集

```python
from datasets import load_dataset

def load_pairwise_benchmark():
    """加载成对比较基准数据集"""
    
    # 使用 MT-Bench 或自定义数据集
    mt_bench = load_dataset("mt-bench", split="single")
    
    return mt_bench


def generate_pairwise_prompts(dataset, model_a, model_b):
    """生成成对比较的 prompt 对"""
    
    prompts = []
    
    for item in dataset:
        question = item["question"]
        
        # 模型 A 生成回答
        response_a = generate_response(model_a, question)
        
        # 模型 B 生成回答
        response_b = generate_response(model_b, question)
        
        prompts.append({
            "question": question,
            "response_a": response_a,
            "response_b": response_b,
            "category": item.get("category", "general")
        })
    
    return prompts
```

### Pairwise Comparison 评测实现

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import openai

def evaluate_pairwise(
    model_a_name: str,
    model_b_name: str,
    judge_model: str = "gpt-4",
    num_samples: int = 100
):
    """完整 Pairwise Comparison 评测"""
    
    # 加载模型
    model_a = load_model(model_a_name)
    model_b = load_model(model_b_name)
    
    # 加载数据集
    dataset = load_pairwise_benchmark()
    
    results = []
    wins_a = 0
    wins_b = 0
    ties = 0
    
    for i in range(min(num_samples, len(dataset))):
        item = dataset[i]
        
        # 生成回答
        response_a = generate_response(model_a, item["question"])
        response_b = generate_response(model_b, item["question"])
        
        # Judge 判断
        judgment = judge_pairwise(
            item["question"],
            response_a,
            response_b,
            judge_model
        )
        
        if judgment == "a":
            wins_a += 1
        elif judgment == "b":
            wins_b += 1
        else:
            ties += 1
        
        results.append({
            "question": item["question"],
            "response_a": response_a,
            "response_b": response_b,
            "winner": judgment
        })
    
    total = wins_a + wins_b + ties
    win_rate_a = wins_a / total if total > 0 else 0
    win_rate_b = wins_b / total if total > 0 else 0
    
    results_summary = {
        "wins_a": wins_a,
        "wins_b": wins_b,
        "ties": ties,
        "win_rate_a": win_rate_a,
        "win_rate_b": win_rate_b,
        "total": total
    }
    
    print(f"Model A Win Rate: {win_rate_a:.2%}")
    print(f"Model B Win Rate: {win_rate_b:.2%}")
    print(f"Ties: {ties}/{total}")
    
    return {"results": results, "summary": results_summary}


def judge_pairwise(
    question: str,
    response_a: str,
    response_b: str,
    judge_model: str = "gpt-4"
) -> str:
    """使用 Judge 模型评判成对比较"""
    
    prompt = f"""You are evaluating two AI assistant responses to a question.

Question: {question}

Response A:
{response_a}

Response B:
{response_b}

Which response is better? Consider:
- Accuracy and correctness
- Helpfulness and relevance
- Clarity and completeness
- Honesty and safety

Your verdict must be exactly one of: A wins, B wins, Tie

Your verdict:"""
    
    response = openai.ChatCompletion.create(
        model=judge_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    verdict = response.choices[0].message.content.strip()
    
    if "A wins" in verdict:
        return "a"
    elif "B wins" in verdict:
        return "b"
    else:
        return "tie"


def generate_response(model, question: str, max_tokens: int = 512) -> str:
    """生成模型回答"""
    
    tokenizer = AutoTokenizer.from_pretrained(model.name)
    
    inputs = tokenizer(question, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.8
        )
    
    response = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[1]:],
        skip_special_tokens=True
    )
    
    return response
```

### Elo Rating 实现

```python
import math

class EloRatingSystem:
    """Elo 评分系统"""
    
    def __init__(self, k_factor: int = 32, initial_rating: float = 1500):
        self.k_factor = k_factor
        self.ratings = {}
        self.initial_rating = initial_rating
    
    def get_rating(self, model_name: str) -> float:
        """获取模型评分"""
        if model_name not in self.ratings:
            self.ratings[model_name] = self.initial_rating
        return self.ratings[model_name]
    
    def expected_score(self, rating_a: float, rating_b: float) -> float:
        """计算期望胜率"""
        return 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))
    
    def update_ratings(
        self,
        model_a: str,
        model_b: str,
        winner: str  # "a", "b", "tie"
    ):
        """更新评分"""
        rating_a = self.get_rating(model_a)
        rating_b = self.get_rating(model_b)
        
        expected_a = self.expected_score(rating_a, rating_b)
        
        # 确定实际分数
        if winner == "a":
            actual_a = 1
        elif winner == "b":
            actual_a = 0
        else:
            actual_a = 0.5
        
        # 更新评分
        self.ratings[model_a] = rating_a + self.k_factor * (actual_a - expected_a)
        self.ratings[model_b] = rating_b + self.k_factor * ((1 - actual_a) - (1 - expected_a))
    
    def run_evaluation(self, model_names: list, comparison_results: list):
        """运行完整 Elo 评估"""
        
        # 初始化所有模型
        for model in model_names:
            self.ratings[model] = self.initial_rating
        
        # 处理每场比较
        for result in comparison_results:
            self.update_ratings(
                result["model_a"],
                result["model_b"],
                result["winner"]
            )
        
        return self.ratings
```

## 📊 结果分析

### 典型结果

| 对比 | Win Rate A | Win Rate B | Tie Rate |
|------|------------|------------|----------|
| GPT-4 vs Claude-2 | 52% | 45% | 3% |
| GPT-4 vs LLaMA-65B | 78% | 18% | 4% |
| Claude-2 vs GPT-3.5 | 65% | 30% | 5% |

### Elo 排名示例

| 模型 | Elo 分数 |
|------|----------|
| GPT-4 | 1680 |
| Claude-2 | 1650 |
| LLaMA-65B | 1520 |
| GPT-3.5 | 1480 |
| LLaMA-7B | 1320 |

### 结果分析

```python
def analyze_pairwise_results(results: dict, by_category: bool = True):
    """分析成对比较结果"""
    
    summary = results["summary"]
    
    print("=== Overall Results ===")
    print(f"Model A Wins: {summary['wins_a']} ({summary['win_rate_a']:.2%})")
    print(f"Model B Wins: {summary['wins_b']} ({summary['win_rate_b']:.2%})")
    print(f"Ties: {summary['ties']} ({summary['ties']/summary['total']:.2%})")
    
    if by_category:
        print("\n=== Results by Category ===")
        category_stats = {}
        
        for r in results["results"]:
            cat = r.get("category", "general")
            if cat not in category_stats:
                category_stats[cat] = {"a": 0, "b": 0, "tie": 0, "total": 0}
            
            category_stats[cat][r["winner"]] += 1
            category_stats[cat]["total"] += 1
        
        for cat, stats in sorted(category_stats.items()):
            win_rate = stats["a"] / stats["total"]
            print(f"{cat}: {win_rate:.2%} ({stats['a']}/{stats['total']})")
```

## 📋 命令速查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用 lm-evaluation-harness 进行成对比较
lm_eval \
    --model hf \
    --model_args pretrained=model_a \
    --tasks pairwise \
    --compare_with pretrained=model_b \
    --batch_size 8

# Python API
python -c "
from lm_eval import evaluator
results = evaluator.simple_evaluate(
    model='hf',
    model_args=dict(pretrained='model_a'),
    tasks=['pairwise'],
    compare_with='model_b'
)
print(evaluator.make_table(results))
"
```

## 📚 学习要点

1. **相对评估**：Pairwise Comparison 通过相对比较避免绝对评分问题
2. **Judge 模型**：GPT-4 等强模型作为 Judge 更可靠
3. **Elo 系统**：动态评分反映模型真实实力差距
4. **类别分析**：不同任务类别结果可能完全不同

## 🔗 相关案例

- `mt-bench-evaluation` - MT-Bench 多轮对话评测
- `llm-as-judge` - LLM-as-Judge 评测方法
- `safety-evaluation` - 安全评测

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
