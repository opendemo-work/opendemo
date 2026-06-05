# Tree of Thought (ToT) 思维树

> 本案例详解 ToT 思维树推理框架，通过多路径探索和自我评估提升 LLM 复杂问题解决能力。

## 📐 ToT 架构

```
                    问题输入
                        │
                        ▼
              ┌─────────────────┐
              │   Thought 1     │ ← 初始思考
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ Thought │  │ Thought │  │ Thought │
    │   1.1   │  │   1.2   │  │   1.3   │
    └────┬────┘  └────┬────┘  └────┬────┘
         │            │            │
         ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ Evaluate│  │ Evaluate│  │ Evaluate│
    │   BAD   │  │  GOOD   │  │   BAD   │
    └─────────┘  └────┬────┘  └─────────┘
                      │ GOOD 路径继续
                      ▼
                 继续扩展...
```

## 与 CoT 对比

| 特性 | Chain of Thought | Tree of Thought |
|------|------------------|-----------------|
| 结构 | 线性链 | 树状分支 |
| 探索 | 单路径 | 多路径 |
| 评估 | 无 | 自我评估 |
| 适用 | 简单推理 | 复杂规划 |

## 💻 核心实现

### ToT Controller

```python
from typing import List, Callable
from langchain.llms import OpenAI

class ToTController:
    def __init__(self, llm, k=3, max_depth=3):
        self.llm = llm
        self.k = k  # 每个节点保留 k 个分支
        self.max_depth = max_depth
    
    def generate_thoughts(self, state, prompt_template):
        prompt = prompt_template.format(state=state)
        response = self.llm.invoke(prompt)
        thoughts = response.split('\n')
        return [t.strip() for t in thoughts if t.strip()]
    
    def evaluate_states(self, states: List[str]) -> List[float]:
        eval_prompt = """Rate each state from 0-10 for likely to solve the problem:
        States:
        {states}
        
        Ratings (one per line):"""
        
        prompt = eval_prompt.format(states='\n'.join(
            [f"{i+1}. {s}" for i, s in enumerate(states)]
        ))
        response = self.llm.invoke(prompt)
        return [float(x.strip()) for x in response.split('\n') if x.strip()]
    
    def select_top_k(self, states, scores, k=None):
        k = k or self.k
        paired = sorted(zip(states, scores), key=lambda x: x[1], reverse=True)
        return [state for state, _ in paired[:k]]
    
    def search(self, initial_state, thought_prompt, max_iterations=10):
        current_states = [initial_state]
        
        for depth in range(self.max_depth):
            all_thoughts = []
            
            for state in current_states:
                thoughts = self.generate_thoughts(state, thought_prompt)
                all_thoughts.extend(thoughts)
            
            if not all_thoughts:
                break
            
            scored = self.evaluate_states(all_thoughts)
            current_states = self.select_top_k(all_thoughts, scored)
            
            if depth >= max_iterations:
                break
        
        return current_states
```

### 实际应用示例：数学问题

```python
class MathToT(ToTController):
    def solve_math_problem(self, problem: str):
        thought_prompt = """Given the math problem: {state}
        
        Think step by step and propose the next calculation or transformation:
        """
        
        final_states = self.search(problem, thought_prompt, max_iterations=5)
        
        answer_prompt = """Based on these solution paths, determine the answer:
        Problem: {problem}
        Paths: {states}
        
        Final answer:"""
        
        answer = self.llm.invoke(answer_prompt.format(
            problem=problem,
            states='\n'.join(final_states)
        ))
        return answer
```

## 📋 命令速查

```bash
pip install langchain openai

# 运行 ToT 示例
python tree_of_thought/math_solver.py

# 测试创意写作
python tree_of_thought/creative_writing.py
```

## 🔗 相关案例

- `chain-of-thought` - 思维链
- `few-shot-learning` - Few-shot Learning
- `prompt-patterns` - Prompt 工程
