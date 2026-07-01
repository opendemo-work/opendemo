<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# MT-Bench 多轮对话评测

> 本案例详解 MT-Bench 评测，理解如何评估 LLM 的多轮对话能力

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    MT-Bench 评测框架                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MT-Bench 包含 8 个类别的多轮对话问题:                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  1. Multi-turn Reasoning (多轮推理)                      │   │
│  │     Q1: Why is the sky blue?                           │   │
│  │     A1: Rayleigh scattering...                          │   │
│  │     Q2: What would happen if atmosphere was thicker?   │   │
│  │     A2: If atmosphere thicker...                        │   │
│  │                                                          │   │
│  │  2. Writing (写作)                                      │   │
│  │  3. Roleplay (角色扮演)                                  │   │
│  │  4. Extraction (信息抽取)                               │   │
│  │  5. Coding (编程)                                       │   │
│  │  6. Math (数学)                                         │   │
│  │  7. Science (科学)                                      │   │
│  │  8. Humanities (人文)                                    │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

LLM-as-Judge 评分流程:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  问题 Q1, Q2, ... (多轮)                                        │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Test Model                             │   │
│  │                   Response A                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Judge Model                             │   │
│  │                   (通常是 GPT-4)                         │   │
│  │                                                          │   │
│  │   Prompt:                                                 │   │
│  │   "You are a judge. Rate the response from 1-10.       │   │
│  │    Consider: accuracy, helpfulness, coherence."           │   │
│  │                                                          │   │
│  │   Response: Score 8/10, Explanation..."                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

评分维度:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  MT-Bench 评分标准:                                            │
│                                                                 │
│  1. Accuracy (准确性)                                          │
│     - 答案是否正确?                                            │
│     - 推理是否正确?                                            │
│                                                                 │
│  2. Helpfulness (有用性)                                       │
│     - 是否满足用户需求?                                        │
│     - 是否提供了额外价值?                                      │
│                                                                 │
│  3. Coherence (连贯性)                                         │
│     - 回复是否流畅?                                            │
│     - 上下文是否连贯?                                          │
│                                                                 │
│  4. Conciseness (简洁性)                                       │
│     - 是否简洁不啰嗦?                                          │
│     - 是否冗余?                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. MT-Bench 数据集

| 类别 | 题数 | 多轮比例 | 说明 |
|------|------|----------|------|
| Reasoning | 120 | 80% | 多轮推理 |
| Writing | 120 | 30% | 写作任务 |
| Roleplay | 120 | 50% | 角色扮演 |
| Extraction | 120 | 40% | 信息抽取 |
| Coding | 120 | 20% | 编程问题 |
| Math | 120 | 30% | 数学问题 |
| Science | 120 | 40% | 科学问题 |
| Humanities | 120 | 30% | 人文问题 |

### 2. 评分方法

```python
# Pairwise Comparison
def pairwise_judge(response_a, response_b, question, judge_model):
    """两个回复 pairwise 比较"""
    prompt = f"""Compare these two responses to the question.
    
Question: {question}

Response A: {response_a}
Response B: {response_b}

Which is better? Respond with just "A" or "B"."""

# Single Response Grading
def grade_response(response, question, judge_model):
    """单个回复评分"""
    prompt = f"""Rate this response from 1-10.

Question: {question}
Response: {response}

Consider: accuracy, helpfulness, coherence, conciseness.
Provide a score and brief explanation."""
```

### 3. 对比基准

| 模型 | MT-Bench | 说明 |
|------|----------|------|
| GPT-4 | 8.99 | 最强 |
| GPT-3.5-turbo | 7.94 | 强 |
| Claude 2 | 8.55 | 强 |
| Vicuna 33B | 7.12 | 开源领先 |
| Llama 2 70B | 6.86 | 中等 |
| Llama 2 7B | 5.45 | 较弱 |

## 💻 完整实现

### MT-Bench 评测实现

```python
import json
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class MTBenchQuestion:
    """MT-Bench 问题"""
    id: str
    category: str
    turns: List[str]  # 多轮对话

@dataclass
class MTBenchResult:
    """评测结果"""
    question_id: str
    category: str
    scores: List[float]  # 每轮得分
    total_score: float


class MTBenchEvaluator:
    """MT-Bench 评测器"""
    
    def __init__(self, judge_model="gpt-4"):
        self.judge_model = judge_model
        self.client = OpenAI()
    
    def generate_response(
        self,
        model,
        conversation: List[Dict]
    ) -> str:
        """生成回复"""
        messages = []
        for turn in conversation:
            if turn["role"] == "user":
                messages.append({"role": "user", "content": turn["content"]})
            elif turn["role"] == "assistant":
                messages.append({"role": "assistant", "content": turn["content"]})
        
        response = model.generate(messages)
        return response
    
    def grade_response(
        self,
        question: str,
        response: str,
        context: str = ""
    ) -> float:
        """LLM-as-Judge 评分"""
        
        prompt = f"""Rate the assistant's response from 1-10.

Question: {question}
{f'Context: {context}' if context else ''}
Response: {response}

Evaluate on:
1. Accuracy: Is the response factually correct?
2. Helpfulness: Does it fully address the question?
3. Coherence: Is it well-organized and clear?

Provide your score as a number between 1-10, followed by a brief explanation.
Format: Score: X/10
Explanation: ..."""

        response = self.client.chat.completions.create(
            model=self.judge_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        result = response.choices[0].message.content
        
        # 解析分数
        try:
            score_str = result.split("Score:")[1].split("/")[0].strip()
            score = float(score_str)
        except:
            score = 5.0  # 默认分数
        
        return score
    
    def evaluate_model(
        self,
        model,
        questions: List[MTBenchQuestion]
    ) -> List[MTBenchResult]:
        """评测整个模型"""
        results = []
        
        for q in questions:
            # 构建对话
            conversation = []
            scores = []
            
            for turn_text in q.turns:
                # 添加用户输入
                conversation.append({"role": "user", "content": turn_text})
                
                # 生成回复
                response = self.generate_response(model, conversation)
                
                # 评分
                score = self.grade_response(
                    question=turn_text,
                    response=response,
                    context=str(conversation[:-1])
                )
                scores.append(score)
                
                # 添加回复到对话
                conversation.append({"role": "assistant", "content": response})
            
            results.append(MTBenchResult(
                question_id=q.id,
                category=q.category,
                scores=scores,
                total_score=sum(scores) / len(scores)
            ))
        
        return results
    
    def summarize_results(
        self,
        results: List[MTBenchResult]
    ) -> Dict:
        """汇总结果"""
        category_scores = {}
        
        for result in results:
            if result.category not in category_scores:
                category_scores[result.category] = []
            category_scores[result.category].append(result.total_score)
        
        summary = {
            "overall": sum(r.total_score for r in results) / len(results),
            "by_category": {
                cat: sum(scores) / len(scores)
                for cat, scores in category_scores.items()
            }
        }
        
        return summary
```

### 使用 FastChat 评测

```python
from fastchat.llm_judge.gen_model_judgment import make_judge
from fastchat.llm_judge.gen_judgment import load_questions

# 加载问题
questions = load_questions("mtbench")

# 创建 judge
judge_model = make_judge("gpt-4")

# 评测
for q in questions:
    for model_name, model in models_to_evaluate.items():
        # 生成回复
        answer = model.generate(q)
        
        # 评分
        judgment = judge_model.make_judgment(
            question=q,
            answer=answer,
            judge=judge_model
        )
```

## 📊 MT-Bench vs 其他基准

| 基准 | 特点 | 适用场景 |
|------|------|----------|
| MT-Bench | 多轮对话, LLM-as-Judge | 对话质量 |
| AlpacaFarm | 偏好对比 | 指令遵循 |
| ChatArena | ELO 排名 | 开放对话 |
| MMLU | 多选题 | 知识水平 |
| HumanEval | 代码执行 | 编程能力 |

## 📋 命令速查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装 FastChat
pip install fschat

# 评测
python -m fastchat.llm_judge.gen_judgment \
    --model gpt-4 \
    --questions mtbench

# 可视化结果
python mtbench/visualize.py --results results.json
```

## 📚 学习要点

1. **多轮评估**：MT-Bench 关注多轮对话连贯性
2. **LLM-as-Judge**：用强模型评估弱模型
3. **类别差异**：不同类别评测结果差异大
4. **对标 GPT-4**：常用 GPT-4 作为基准

## 🔗 相关案例

- `mmlu-evaluation` - MMLU 评测
- `humaneval-evaluation` - HumanEval 代码评测
- `llm-as-judge` - LLM-as-Judge 评估
- `safety-evaluation` - Safety 评测

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
