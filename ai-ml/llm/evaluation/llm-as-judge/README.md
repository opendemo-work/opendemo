# LLM-as-Judge 评估

> 本案例详解 LLM-as-Judge 方法，理解如何用强模型评估弱模型

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    LLM-as-Judge 评估框架                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 被评估模型 Response                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Judge Model                            │   │
│  │                   (GPT-4/Claude)                        │   │
│  │                                                          │   │
│  │   ┌─────────────────────────────────────────────────┐   │   │
│  │   │  System: You are an expert evaluator...         │   │   │
│  │   │  User: Question: {Q}                          │   │   │
│  │   │         Response: {R}                          │   │   │
│  │   │         Score and provide feedback.            │   │   │
│  │   └─────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Evaluation Result                     │   │
│  │                                                          │   │
│  │   Score: 8/10                                            │   │
│  │   Strengths: Clear explanation, accurate...          │   │
│  │   Weaknesses: Could be more concise...                  │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Pairwise vs Single Scoring:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Pairwise Comparison:                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Question: What is Python?                              │   │
│  │                                                          │   │
│  │  Response A: Python is a programming language...        │   │
│  │  Response B: Python? You mean the snake or language?    │   │
│  │                                                          │   │
│  │  Judgment: A is better (more helpful and accurate)    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Single Scoring:                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Question: Explain quantum entanglement                  │   │
│  │  Response: Quantum entanglement is...                    │   │
│  │                                                          │   │
│  │  Score: 8/10                                             │   │
│  │  Explanation: Good explanation, but could use analogy. │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

评估维度框架:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  General Evaluation Dimensions:                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Accuracy (准确性)                                    │  │
│  │     - Factual correctness                                │  │
│  │     - Logical soundness                                   │  │
│  │                                                          │  │
│  │  2. Helpfulness (有用性)                                 │  │
│  │     - Relevance to user intent                            │  │
│  │     - Completeness                                       │  │
│  │                                                          │  │
│  │  3. Coherence (连贯性)                                    │  │
│  │     - Logical flow                                        │  │
│  │     - Readability                                         │  │
│  │                                                          │  │
│  │  4. Safety (安全性)                                       │  │
│  │     - No harmful content                                  │  │
│  │     - Appropriate tone                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 为什么需要 LLM-as-Judge

```
传统评估的局限:
- 代码: 可以执行测试
- 数学: 有标准答案
- 对话: 主观性强，难以自动化

LLM-as-Judge 的优势:
- 可以评估任何文本输出
- 模拟人类判断
- 可扩展性强
- 成本较低 (相比人工标注)
```

### 2. Prompt 设计

```python
JUDGE_PROMPTS = {
    "scoring": """You are an expert evaluator. Rate the response from 1-10.

Question: {question}
Response: {response}

Score: X/10
Explanation: ...""",

    "pairwise": """Compare these two responses. Which is better?

Question: {question}
Response A: {response_a}
Response B: {response_b}

Choose: A or B
Reason: ...""",

    "detailed": """Evaluate this response on multiple dimensions:

Question: {question}
Response: {response}

Rate each dimension 1-10:
- Accuracy: ...
- Helpfulness: ...
- Coherence: ...
- Safety: ...

Overall Score: X/10
Detailed Feedback: ..."""
}
```

### 3. 潜在问题

| 问题 | 说明 | 解决方案 |
|------|------|----------|
| 位置偏见 | 可能偏向 A 或 B |swap 顺序再判断 |
| 长度偏见 | 可能偏向更长回复 | 长度控制 |
| 自我偏好 | 可能偏好自己的输出 | 使用更强的 judge |

## 💻 完整实现

### Judge 实现

```python
from typing import List, Dict, Optional, Tuple
import anthropic

class LLMJudge:
    """LLM-as-Judge 评估器"""
    
    def __init__(
        self,
        judge_model: str = "gpt-4",
        judge_type: str = "scoring"
    ):
        self.judge_model = judge_model
        self.judge_type = judge_type
        self.client = OpenAI()
        
    def score(
        self,
        question: str,
        response: str,
        dimensions: Optional[List[str]] = None
    ) -> Dict:
        """评分评估"""
        
        prompt = self._build_prompt(question, response, dimensions)
        
        response = self.client.chat.completions.create(
            model=self.judge_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        result = response.choices[0].message.content
        
        return self._parse_result(result, self.judge_type)
    
    def pairwise(
        self,
        question: str,
        response_a: str,
        response_b: str
    ) -> Dict:
        """Pairwise 比较"""
        
        prompt = f"""Compare these two responses. Which is better?

Question: {question}

Response A: {response_a}

Response B: {response_b}

Choose "A" if response A is better, "B" if response B is better.
Provide a brief explanation.

Format:
Winner: A or B
Reason: ..."""

        response = self.client.chat.completions.create(
            model=self.judge_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        result = response.choices[0].message.content
        
        return self._parse_pairwise_result(result)
    
    def _build_prompt(
        self,
        question: str,
        response: str,
        dimensions: Optional[List[str]]
    ) -> str:
        """构建评估 prompt"""
        
        if self.judge_type == "scoring":
            return f"""Rate the following response from 1-10.

Question: {question}
Response: {response}

Provide:
1. A score from 1-10
2. A brief explanation of your rating

Format:
Score: X/10
Explanation: ..."""

        elif self.judge_type == "detailed":
            dims_str = "\n".join(f"- {d}" for d in dimensions) if dimensions else ""
            return f"""Evaluate this response on multiple dimensions.

Question: {question}
Response: {response}

Dimensions to evaluate:
{dims_str or "- Overall Quality"}

Provide a score for each dimension and an overall score.

Format:
Dimension Scores:
- Dimension: X/10
Overall: X/10
Feedback: ..."""

        return ""
    
    def _parse_result(self, result: str, judge_type: str) -> Dict:
        """解析评估结果"""
        # 简单解析，可根据实际情况改进
        score = 5.0
        explanation = result
        
        # 提取分数
        import re
        match = re.search(r'Score:\s*(\d+(?:\.\d+)?)', result, re.IGNORECASE)
        if match:
            score = float(match.group(1))
        
        return {
            "score": score,
            "explanation": explanation,
            "raw_response": result
        }
    
    def _parse_pairwise_result(self, result: str) -> Dict:
        """解析 pairwise 结果"""
        winner = None
        if "Winner: A" in result or "winner: a" in result.lower():
            winner = "A"
        elif "Winner: B" in result or "winner: b" in result.lower():
            winner = "B"
        
        return {
            "winner": winner,
            "reason": result,
            "raw_response": result
        }
```

### 完整评估流程

```python
class EvaluationPipeline:
    """完整评估流程"""
    
    def __init__(self, judge: LLMJudge):
        self.judge = judge
    
    def evaluate_responses(
        self,
        questions: List[str],
        responses: List[str],
        use_swap: bool = True
    ) -> List[Dict]:
        """
        评估多个回复
        use_swap: 是否交换顺序减少偏见
        """
        results = []
        
        for question, response in zip(questions, responses):
            # 评分
            score_result = self.judge.score(question, response)
            results.append(score_result)
        
        return results
    
    def evaluate_pairwise(
        self,
        question: str,
        response_a: str,
        response_b: str,
        num_judges: int = 2
    ) -> Dict:
        """
        Pairwise 比较，多次评估取多数
        """
        votes = {"A": 0, "B": 0, "tie": 0}
        
        for i in range(num_judges):
            # 交换顺序 (如果 i 是奇数)
            if i % 2 == 1:
                q, a, b = question, response_b, response_a
            else:
                q, a, b = question, response_a, response_b
            
            result = self.judge.pairwise(q, a, b)
            
            if result["winner"] == "A":
                votes["A" if i % 2 == 0 else "B"] += 1
            elif result["winner"] == "B":
                votes["B" if i % 2 == 0 else "A"] += 1
            else:
                votes["tie"] += 1
        
        # 最终判决
        final_winner = max(votes, key=votes.get)
        
        return {
            "votes": votes,
            "winner": final_winner,
            "confidence": votes[final_winner] / num_judges
        }
```

### 使用 Claude 作为 Judge

```python
import anthropic

class ClaudeJudge:
    """使用 Claude 作为 Judge"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def score(self, question: str, response: str) -> Dict:
        """Claude 评分"""
        
        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""Rate this response from 1-10.

Question: {question}
Response: {response}

Score: X/10
Explanation: ..."""
            }]
        )
        
        result = message.content[0].text
        
        # 解析
        import re
        match = re.search(r'(\d+(?:\.\d+)?)', result)
        score = float(match.group(1)) if match else 5.0
        
        return {"score": score, "explanation": result}
```

## 📊 Judge 模型对比

| Judge 模型 | 一致性 | 成本 | 准确性 |
|------------|--------|------|--------|
| GPT-4 | 高 | 高 | 基准 |
| GPT-3.5 | 中 | 低 | 较低 |
| Claude 3 | 高 | 中高 | 高 |
| Claude 2 | 高 | 中 | 高 |

## 📋 命令速查

```bash
# 运行评估
python llm_judge/evaluate.py --model gpt-4 --dataset eval_data.json

# Pairwise 比较
python llm_judge/pairwise.py --response_a a.txt --response_b b.txt

# 评估 LLM 输出
python llm_judge/judge.py --input "What is AI?" --response "AI is..."
```

## 📚 学习要点

1. **Prompt 设计关键**：清晰的结构化输出格式
2. **位置偏见**：Pairwise 时交换顺序
3. **多次评估**：取多数投票更可靠
4. **维度评估**：多维度评分更全面

## 🔗 相关案例

- `mt-bench-evaluation` - MT-Bench 对话评测
- `safety-evaluation` - Safety 评测
- `llm-evaluation-harness` - LM-Eval Harness
- `pairwise-comparison` - 成对比较评估
