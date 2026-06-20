"""
BBH (BIG-Bench Hard) 风格评测器

本脚本演示如何实现一个简化版的 BBH 复杂推理任务评估框架，包括：
- 样本定义与 prompt 构建
- Few-shot / CoT 提示策略
- 答案提取与评分
- 任务级准确率统计

注意：本示例仅使用标准库，便于在无网络环境下运行。
生产环境可替换为真实 LLM API 和 BIG-Bench Hard 数据集。
"""

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class BBHSample:
    """BBH 评测样本"""

    task: str
    input: str
    target: str


class SimpleLLMClient:
    """模拟 LLM 客户端

    生产环境中应替换为真实 API 调用。
    """

    def generate(self, prompt: str) -> str:
        """模拟生成"""
        prompt_lower = prompt.lower()
        # 针对 bool 任务
        if "(true)" in prompt_lower and "(false)" in prompt_lower:
            if "not not true" in prompt_lower:
                return "Let's think step by step. 'not not True' is True. So the answer is True."
            return "The answer is True."
        # 针对 yes/no 任务
        if "(a) yes" in prompt_lower and "(b) no" in prompt_lower:
            return "Let's think step by step. The answer is Yes."
        # 针对 A/B 选项
        if "option a" in prompt_lower and "option b" in prompt_lower:
            return "The answer is A."
        return "Let's think step by step. The answer is True."


class BBHEvaluator:
    """BBH 评测器"""

    def __init__(self, model_client: SimpleLLMClient):
        self.model_client = model_client

    def build_prompt(self, sample: BBHSample, use_cot: bool = True) -> str:
        """构建 BBH 评测 prompt"""
        prompt = f"Task: {sample.task}\n\n"
        prompt += f"Q: {sample.input}\n"
        if use_cot:
            prompt += "A: Let's think step by step. "
        else:
            prompt += "A: "
        return prompt

    def extract_answer(self, text: str) -> str:
        """从模型输出中提取答案

        优先匹配常见格式：
        - "The answer is X."
        - "答案是 X"
        - 最后一个 True/False/Yes/No
        """
        # 匹配 "The answer is X" 或 "答案是 X"
        match = re.search(
            r"(?:the answer is|答案是)\s+([A-Za-z0-9\-\s]+)", text, re.IGNORECASE
        )
        if match:
            return match.group(1).strip().lower()

        # 匹配选项字母
        match = re.search(r"\b([A-D])\b", text)
        if match:
            return match.group(1).lower()

        # 匹配 True/False/Yes/No
        text_lower = text.lower()
        for keyword in ["true", "false", "yes", "no"]:
            if keyword in text_lower:
                return keyword

        return text.strip().lower()

    def evaluate_task(
        self, samples: List[BBHSample], use_cot: bool = True
    ) -> Dict[str, any]:
        """评估单个任务

        Args:
            samples: 该任务的样本列表
            use_cot: 是否使用 Chain-of-Thought

        Returns:
            包含 correct、total、accuracy、details 的字典
        """
        correct = 0
        details = []

        for sample in samples:
            prompt = self.build_prompt(sample, use_cot=use_cot)
            output = self.model_client.generate(prompt)
            pred = self.extract_answer(output)
            target = sample.target.strip().lower()
            is_correct = pred == target or target in pred or pred in target
            if is_correct:
                correct += 1
            details.append(
                {
                    "input": sample.input,
                    "target": target,
                    "prediction": pred,
                    "correct": is_correct,
                }
            )

        accuracy = correct / len(samples) if samples else 0.0
        return {
            "correct": correct,
            "total": len(samples),
            "accuracy": accuracy,
            "details": details,
        }

    def evaluate_all(
        self, task_samples: Dict[str, List[BBHSample]], use_cot: bool = True
    ) -> Dict[str, any]:
        """评估多个任务

        Args:
            task_samples: 任务名到样本列表的映射
            use_cot: 是否使用 Chain-of-Thought

        Returns:
            各任务结果和总体准确率
        """
        results = {}
        total_correct = 0
        total_samples = 0

        for task, samples in task_samples.items():
            result = self.evaluate_task(samples, use_cot=use_cot)
            results[task] = result
            total_correct += result["correct"]
            total_samples += result["total"]

        overall_accuracy = total_correct / total_samples if total_samples else 0.0
        return {
            "overall_accuracy": overall_accuracy,
            "total_correct": total_correct,
            "total_samples": total_samples,
            "task_results": results,
        }


def main():
    """主函数：演示 BBH 评测"""
    client = SimpleLLMClient()
    evaluator = BBHEvaluator(client)

    task_samples = {
        "boolean_expressions": [
            BBHSample(
                task="boolean_expressions",
                input="( ( not not True ) ) = ? Options: (True) (False)",
                target="true",
            ),
            BBHSample(
                task="boolean_expressions",
                input="( ( True or False ) and False ) = ? Options: (True) (False)",
                target="false",
            ),
        ],
        "navigate": [
            BBHSample(
                task="navigate",
                input="If you walk forward 3 steps, then turn around and walk back 3 steps, do you return? Options: (A) Yes (B) No",
                target="yes",
            ),
        ],
    }

    result = evaluator.evaluate_all(task_samples, use_cot=True)

    print(f"Overall Accuracy: {result['overall_accuracy']:.2%}")
    print(f"Total: {result['total_correct']}/{result['total_samples']}\n")
    print("Task Breakdown:")
    for task, res in result["task_results"].items():
        print(f"  {task}: {res['correct']}/{res['total']} ({res['accuracy']:.2%})")


if __name__ == "__main__":
    main()
