"""
BBH 评测器单元测试

使用标准库 unittest，无需额外安装 pytest 即可运行。
"""

import sys
import unittest
from pathlib import Path

# 添加 code 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from bbh_evaluator import BBHEvaluator, BBHSample, SimpleLLMClient


class TestSimpleLLMClient(unittest.TestCase):
    """SimpleLLMClient 测试"""

    def test_generate_returns_answer(self):
        """测试模拟客户端返回答案"""
        client = SimpleLLMClient()
        answer = client.generate("Options: (True) (False)")
        self.assertGreater(len(answer), 0)


class TestBBHEvaluator(unittest.TestCase):
    """BBHEvaluator 测试"""

    def setUp(self):
        self.client = SimpleLLMClient()
        self.evaluator = BBHEvaluator(self.client)

    def test_extract_answer_the_answer_is(self):
        """测试提取 'The answer is X' 格式"""
        pred = self.evaluator.extract_answer("Let's think. The answer is True.")
        self.assertEqual(pred, "true")

    def test_extract_answer_option_letter(self):
        """测试提取选项字母"""
        pred = self.evaluator.extract_answer("I think the answer is B.")
        self.assertEqual(pred, "b")

    def test_extract_answer_keyword(self):
        """测试提取 True/False 关键词"""
        pred = self.evaluator.extract_answer("After thinking, yes.")
        self.assertEqual(pred, "yes")

    def test_evaluate_task(self):
        """测试评估单个任务"""
        samples = [
            BBHSample(
                task="boolean_expressions",
                input="not not True = ? Options: (True) (False)",
                target="true",
            ),
        ]
        result = self.evaluator.evaluate_task(samples, use_cot=True)
        self.assertEqual(result["total"], 1)
        self.assertIn("accuracy", result)
        self.assertIn("details", result)

    def test_evaluate_all(self):
        """测试评估多个任务"""
        task_samples = {
            "boolean_expressions": [
                BBHSample(
                    task="boolean_expressions",
                    input="not not True = ? Options: (True) (False)",
                    target="true",
                ),
            ],
            "navigate": [
                BBHSample(
                    task="navigate",
                    input="Walk 3 steps forward and 3 back. Return? Options: (A) Yes (B) No",
                    target="yes",
                ),
            ],
        }
        result = self.evaluator.evaluate_all(task_samples, use_cot=True)
        self.assertIn("overall_accuracy", result)
        self.assertIn("task_results", result)
        self.assertEqual(result["total_samples"], 2)

    def test_cot_prompt_contains_think_step_by_step(self):
        """测试 CoT prompt 包含思维链引导"""
        sample = BBHSample(
            task="test", input="What is 1+1?", target="2"
        )
        prompt = self.evaluator.build_prompt(sample, use_cot=True)
        self.assertIn("Let's think step by step", prompt)

    def test_no_cot_prompt(self):
        """测试非 CoT prompt 不包含思维链引导"""
        sample = BBHSample(
            task="test", input="What is 1+1?", target="2"
        )
        prompt = self.evaluator.build_prompt(sample, use_cot=False)
        self.assertNotIn("Let's think step by step", prompt)


if __name__ == "__main__":
    unittest.main()
