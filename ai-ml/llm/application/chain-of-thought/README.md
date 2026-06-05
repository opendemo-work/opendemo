# Chain of Thought 思维链

> 本案例详解 Chain of Thought (CoT) 推理技术，提升 LLM 的推理能力

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Chain of Thought 演进                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Standard Prompting:                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Q: John has 5 apples. He gives 2 to Mary...           │   │
│  │  A: 3                                                 │   │
│  │  (直接给出答案，无推理过程)                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Chain of Thought (CoT):                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Q: John has 5 apples. He gives 2 to Mary...           │   │
│  │  A: Let me think step by step.                        │   │
│  │     Step 1: John starts with 5 apples                   │   │
│  │     Step 2: He gives 2 to Mary, so 5 - 2 = 3          │   │
│  │     Step 3: John has 3 apples left                      │   │
│  │  A: 3                                                 │   │
│  │  (显式推理过程)                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Tree of Thought (ToT):                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │         Question                                        │   │
│  │            │                                            │   │
│  │       ┌────┴────┐                                      │   │
│  │    Thought A  Thought B  Thought C                      │   │
│  │       │        │        │                               │   │
│  │    ┌──┴──┐   ┌┴──┐    ┌┴──┐                          │   │
│  │   A1     A2  B1   B2   C1                              │   │
│  │            │         │       │                           │   │
│  │         [Evaluate & Select Best]                        │   │
│  │                     │                                   │   │
│  │                 Final Answer                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Zero-shot CoT:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Prompt = 问题 + "Let's think step by step"                    │
│                                                                 │
│  Example:                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Q: If a train leaves at 2pm traveling 60mph...         │   │
│  │  "Let's think step by step."                           │   │
│  │                                                          │   │
│  │  The train travels 60 miles per hour...                  │   │
│  │  After 2 hours, it would have traveled 120 miles...      │   │
│  │  So at 4pm, the train is 120 miles from the start.     │   │
│  │                                                          │   │
│  │  A: 120 miles                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. CoT 有效性原因

```
为什么 CoT 有效？

1. 显式推理 → 减少 LLM "跳步" 错误
2. 中间步骤 → 提供更多生成 token，增加推理时间
3. 注意力机制 → 更好地建立问题各部分关系
4. 格式引导 → 让模型生成更结构化的输出
```

### 2. CoT 类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| Zero-shot CoT | 添加 "Let's think step by step" | 简单推理 |
| Few-shot CoT | 提供推理示例 | 复杂推理 |
| Tree of Thought | 探索多条推理路径 | 创意问题 |
| Graph of Thought | 更通用的推理图 | 复杂问题 |

### 3. Few-shot CoT 示例

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?\nA: He starts with 5 balls. He buys 2 cans × 3 balls = 6 balls. 5 + 6 = 11 balls. The answer is 11."
    },
    {
      "role": "user", 
      "content": "Q: Jennifer has 17 chocolates. She gives 5 to her friend. Then she buys 2 more boxes of chocolate. Each box has 12 chocolates. How many chocolates does Jennifer have now?\nA:"
    }
  ]
}
```

## 💻 完整实现

### Zero-shot CoT

```python
from openai import OpenAI

client = OpenAI()

def zero_shot_cot(question: str) -> str:
    """Zero-shot Chain of Thought"""
    
    # 添加 CoT 触发词
    cot_prompt = f"{question}\n\nLet's think step by step."
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": cot_prompt}]
    )
    
    return response.choices[0].message.content

def extract_final_answer(response: str) -> str:
    """从 CoT 响应中提取最终答案"""
    lines = response.strip().split('\n')
    
    # 查找 "The answer is" 或 "Therefore" 等模式
    for line in lines:
        if 'the answer is' in line.lower():
            # 提取答案
            import re
            match = re.search(r'(?:the answer is\s*)(.+?)(?:\.|$)', line, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    
    # 如果没找到，返回最后一行
    return lines[-1] if lines else ""
```

### Few-shot CoT

```python
def few_shot_cot(question: str, examples: list) -> str:
    """Few-shot Chain of Thought"""
    
    # 构建 few-shot prompt
    prompt = ""
    for ex in examples:
        prompt += f"Q: {ex['question']}\n"
        prompt += f"A: {ex['reasoning']}\n\n"
    
    prompt += f"Q: {question}\nA:"
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7  # 稍高温度增加多样性
    )
    
    return response.choices[0].message.content

# 数学推理示例
math_examples = [
    {
        "question": "There are 15 trees. The workers will plant trees in rows. Each row has 4 trees. How many complete rows can they plant?",
        "reasoning": "Step 1: We have 15 trees total. Step 2: Each row needs 4 trees. Step 3: 15 ÷ 4 = 3 complete rows with 3 trees remaining. Step 4: The answer is 3 complete rows."
    },
    {
        "question": "A shopkeeper sells 45 apples. He had 120 apples yesterday. How many apples does he have left?",
        "reasoning": "Step 1: The shopkeeper started with 120 apples. Step 2: He sold 45 apples. Step 3: 120 - 45 = 75 apples. Step 4: The answer is 75 apples."
    }
]

result = few_shot_cot("If a bus has 52 seats and 78 students want to ride, how many buses are needed?", math_examples)
```

### Tree of Thought

```python
import asyncio
from typing import List, Callable

class TreeOfThought:
    """Tree of Thought 实现"""
    
    def __init__(
        self,
        llm_fn: Callable,
        num_thoughts: int = 3,
        max_depth: int = 3,
    ):
        self.llm_fn = llm_fn
        self.num_thoughts = num_thoughts
        self.max_depth = max_depth
        
    def generate_thoughts(self, state: str, depth: int) -> List[str]:
        """生成多个思考分支"""
        prompt = f"""Given the current state: {state}

Generate {self.num_thoughts} different possible next steps or thoughts. 
Be creative and explore different approaches.

Step {depth + 1}:"""

        response = self.llm_fn(prompt)
        thoughts = [t.strip() for t in response.split('\n') if t.strip()]
        return thoughts[:self.num_thoughts]
    
    def evaluate_state(self, state: str) -> float:
        """评估当前状态"""
        prompt = f"""Evaluate how promising this solution path is:

{state}

Rate from 0 to 1 how likely this leads to the correct answer:"""

        response = self.llm_fn(prompt)
        # 解析评分
        try:
            score = float(response.strip())
            return max(0.0, min(1.0, score))
        except:
            return 0.5
    
    async def solve(self, problem: str) -> str:
        """解决问题"""
        from dataclasses import dataclass
        
        @dataclass
        class Node:
            state: str
            depth: int
            score: float
            parent: 'Node' = None
        
        # BFS/DFS 搜索
        root = Node(state=problem, depth=0, score=0.0)
        frontier = [root]
        best_leaf = root
        
        while frontier and root.depth < self.max_depth:
            current = frontier.pop(0)
            
            # 生成下一层思考
            thoughts = self.generate_thoughts(current.state, current.depth)
            
            for thought in thoughts:
                child = Node(
                    state=thought,
                    depth=current.depth + 1,
                    score=0.0,
                    parent=current
                )
                
                # 评估
                child.score = self.evaluate_state(thought)
                
                if child.score > best_leaf.score:
                    best_leaf = child
                
                frontier.append(child)
        
        # 回溯获取完整路径
        path = []
        node = best_leaf
        while node:
            path.append(node.state)
            node = node.parent
        
        return "\n".join(reversed(path))
```

### 自动 CoT (Self-Consistency)

```python
def self_consistency_cot(question: str, num_samples: int = 8) -> str:
    """自洽性 CoT - 多次采样选择最一致的答案"""
    
    # 多次采样推理
    responses = []
    for _ in range(num_samples):
        response = few_shot_cot(question, get_examples_for(question))
        responses.append(response)
    
    # 提取所有答案
    answers = []
    for response in responses:
        answer = extract_final_answer(response)
        if answer:
            answers.append(answer)
    
    # 多数投票
    from collections import Counter
    counter = Counter(answers)
    most_common = counter.most_common(1)[0][0]
    
    return most_common, responses
```

## 📊 CoT 效果对比

| 方法 | 数学 (GSM8K) | 逻辑 (BBH) | 常识 (CSQA) |
|------|--------------|------------|--------------|
| Standard | 46% | 39% | 45% |
| Zero-shot CoT | 72% | 57% | 53% |
| Few-shot CoT | 74% | 62% | 58% |
| Self-Consistency | **79%** | **67%** | **62%** |

## 📋 命令速查

```bash
# 测试 Zero-shot CoT
python chain_of_thought/zero_shot_cot.py

# 测试 Few-shot CoT
python chain_of_thought/few_shot_cot.py

# 测试 Tree of Thought
python chain_of_thought/tree_of_thought.py

# 运行 GSM8K 评测
python chain_of_thought/evaluate_gsm8k.py
```

## 📚 学习要点

1. **"Let me think step by step"**：Zero-shot CoT 的关键触发词
2. **Few-shot 效果更好**：提供推理示例能显著提升效果
3. **Self-Consistency**：多次采样+多数投票可进一步提升
4. **Tree of Thought**：探索多条推理路径，适合复杂问题

## 🔗 相关案例

- `prompt-patterns` - 高级 Prompt 模式
- `react-agent` - ReAct Agent
- `plan-and-execute` - Plan-and-Execute
- `tree-of-thought` - Tree of Thought
