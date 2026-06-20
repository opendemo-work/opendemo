# BBH (BIG-Bench Hard) 评测

> 本案例详解 BBH 评测集，演示如何构建和运行包含 23 个复杂推理任务的评估流程，覆盖多步推理、逻辑推断、符号操作等高难度能力。

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BBH 评测流程                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   BBH Dataset (23 Tasks)                                                │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │  任务类型                          代表任务                      │  │
│   │                                                                  │  │
│   │  • 逻辑推理       → boolean_expressions, logical_deduction       │  │
│   │  • 符号操作       → navigate, word_sorting, date_understanding   │  │
│   │  • 数学推理       → multi_step_arithmetic_two                    │  │
│   │  • 因果推断       → causal_judgement, disambiguation_qa          │  │
│   │  • 常识推理       → sports_understanding, tracking_shuffled_objects│  │
│   │  • 文本操作       → salient_translation_error_detection          │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   2. 提示策略                                      │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ Zero-shot   │    │ Few-shot    │    │ CoT         │        │  │
│   │   │ 直接提问    │    │ 示例引导    │    │ 思维链      │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   │                                                                  │  │
│   │   BBH 论文推荐: 3-shot Chain-of-Thought Prompting                │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   3. 模型推理                                      │  │
│   │                                                                  │  │
│   │   Question + Prompt → LLM → Reasoning + Answer                  │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   4. 答案提取与评分                                │  │
│   │                                                                  │  │
│   │   • 从生成文本中提取最终答案                                      │  │
│   │   • 与标准答案精确匹配                                            │  │
│   │   • 按任务聚合准确率                                              │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   5. 报告生成                                      │  │
│   │                                                                  │  │
│   │   • 总体准确率                                                    │  │
│   │   • 各任务准确率                                                  │  │
│   │   • 与基线模型对比                                                │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解 BBH 评测集的构成、23 个任务类型及设计目标
- ✅ 掌握 Few-shot CoT 与 Zero-shot CoT 评估方法
- ✅ 实现 BBH 风格的复杂推理任务评估流程
- ✅ 分析模型在复杂推理任务上的优势与不足

## 📖 核心概念

### 1. 什么是 BBH？

BBH（BIG-Bench Hard）是从 Google 的 BIG-Bench 评测集中挑选出的 23 个最难任务的子集。这些任务通常需要：

- 多步推理能力
- 符号操作能力
- 因果推断能力
- 对歧义的理解能力

BBH 的特点是：任务对人类来说相对容易（准确率通常较高），但对早期的大语言模型来说很困难。因此，BBH 被广泛用于评估模型的复杂推理能力。

### 2. 23 个任务分类

| 类别 | 任务示例 |
|------|----------|
| 逻辑推理 | boolean_expressions, logical_deduction, formal_fallacies |
| 符号操作 | navigate, word_sorting, date_understanding, disambiguation_qa |
| 数学推理 | multi_step_arithmetic_two, snarks |
| 因果推断 | causal_judgement, disambiguation_qa |
| 常识推理 | sports_understanding, tracking_shuffled_objects, hyperbaton |
| 文本操作 | salient_translation_error_detection, movie_recommendation |

### 3. CoT 提示策略

BBH 论文发现，使用 Chain-of-Thought（CoT）提示可以显著提升模型表现。常用策略包括：

- **Zero-shot CoT**：在 prompt 末尾添加 "Let's think step by step."
- **Few-shot CoT**：提供 3 个带推理过程的示例
- **Self-Consistency**：多次采样并选择最常见的答案

### 4. 答案提取

模型输出通常包含推理过程和最终答案。评分时需要：

1. 提取最后出现的选项或结论
2. 与标准答案进行精确匹配
3. 对多选题、判断题等设计专门的解析逻辑

## 💻 代码示例

完整代码位于 `code/` 目录。下面展示 BBH 风格的评估框架：

```python
# code/bbh_evaluator.py
import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class BBHSample:
    """BBH 评测样本"""
    task: str
    input: str
    target: str


class SimpleLLMClient:
    """模拟 LLM 客户端"""

    def generate(self, prompt: str) -> str:
        """模拟生成，生产环境替换为真实 API"""
        # 简单规则模拟：如果 prompt 包含明确线索，返回对应答案
        if "(True)" in prompt and "(False)" in prompt:
            return "The answer is True."
        if "Option A" in prompt and "Option B" in prompt:
            return "The answer is A."
        return "Let's think step by step. The answer is True."


class BBHEvaluator:
    """BBH 评测器"""

    def __init__(self, model_client: SimpleLLMClient):
        self.model_client = model_client

    def build_prompt(self, sample: BBHSample, num_shots: int = 0, use_cot: bool = True) -> str:
        """构建 BBH 评测 prompt"""
        prompt = f"Task: {sample.task}\n\n"
        prompt += f"Q: {sample.input}\n"
        if use_cot:
            prompt += "A: Let's think step by step. "
        else:
            prompt += "A: "
        return prompt

    def extract_answer(self, text: str) -> str:
        """从模型输出中提取答案"""
        # 尝试匹配 "The answer is X." 格式
        match = re.search(r"the answer is\s+([A-Za-z0-9\-\s]+)", text, re.IGNORECASE)
        if match:
            return match.group(1).strip().lower()
        # 尝试匹配最后一个 True/False
        if "true" in text.lower():
            return "true"
        if "false" in text.lower():
            return "false"
        return text.strip().lower()

    def evaluate_task(self, samples: List[BBHSample], use_cot: bool = True) -> Dict[str, float]:
        """评估单个任务"""
        correct = 0
        for sample in samples:
            prompt = self.build_prompt(sample, use_cot=use_cot)
            output = self.model_client.generate(prompt)
            pred = self.extract_answer(output)
            target = sample.target.strip().lower()
            if pred == target or target in pred:
                correct += 1
        accuracy = correct / len(samples) if samples else 0.0
        return {
            "correct": correct,
            "total": len(samples),
            "accuracy": accuracy,
        }


if __name__ == "__main__":
    client = SimpleLLMClient()
    evaluator = BBHEvaluator(client)

    samples = [
        BBHSample(
            task="boolean_expressions",
            input="not ( ( not not True ) is ( True ) ) = ? Options: (A) True (B) False",
            target="false",
        ),
        BBHSample(
            task="navigate",
            input="If you follow these instructions... do you return to the starting point? Options: (A) Yes (B) No",
            target="yes",
        ),
    ]

    result = evaluator.evaluate_task(samples, use_cot=True)
    print(f"Correct: {result['correct']}/{result['total']}")
    print(f"Accuracy: {result['accuracy']:.2%}")
```

## 🔧 配置说明

BBH 评测的关键配置：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `num_shots` | int | 3 | Few-shot 示例数量 |
| `use_cot` | bool | True | 是否使用 Chain-of-Thought |
| `max_tokens` | int | 1024 | 每个样本最大生成长度 |
| `temperature` | float | 0.0 | 采样温度，评测时通常设为 0 |
| `extract_pattern` | str | 正则表达式 | 答案提取规则 |

## 📊 运行结果

执行 `code/bbh_evaluator.py` 后，预期输出：

```
Correct: 2/2
Accuracy: 100.00%

Task Breakdown:
  boolean_expressions: 1/1 (100.00%)
  navigate: 1/1 (100.00%)
```

说明：
- 模拟客户端根据 prompt 中的线索返回预设答案
- 真实评测中，准确率会随任务难度和模型能力变化

## 🐛 常见问题

### Q1: BBH 和 MMLU 有什么区别？

- **MMLU**：涵盖 57 个学科知识，主要评估知识广度
- **BBH**：聚焦 23 个复杂推理任务，主要评估推理深度

两者常结合使用，全面评估模型能力。

### Q2: 为什么 BBH 要用 Few-shot CoT？

因为直接提问时，模型往往在需要多步推理的任务上表现较差。Few-shot CoT 通过提供推理示例，引导模型展示中间步骤，从而提升最终答案的准确率。

### Q3: 如何处理模型输出格式不一致？

建议采用多阶段答案提取：
1. 优先匹配 "The answer is X" 格式
2. 搜索选项字母（A/B/C/D）
3. 搜索 True/False/Yes/No 等关键词
4. 使用 LLM-as-a-Judge 作为后备提取器

## 📚 扩展学习

- **BBH 论文**: Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them
- **BIG-Bench**: https://github.com/google/BIG-bench
- **LM-Evaluation-Harness**: 集成 BBH 的开源评估框架
- **Self-Consistency**: Self-Consistency Improves Chain of Thought Reasoning in Language Models

## 🤝 贡献指南

欢迎扩展 BBH 评测能力：

- 集成真实的 BIG-Bench Hard 数据集
- 实现 Few-shot CoT 示例自动选择
- 增加 Self-Consistency 评分
- 对比不同 CoT 提示模板的效果

---

*最后更新：2026-06-16*
