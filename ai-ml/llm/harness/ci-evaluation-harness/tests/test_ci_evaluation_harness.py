"""
LLM CI 集成评估 Harness 单元测试

使用标准库 unittest，无需额外安装 pytest 即可运行。
"""

import sys
import unittest
from pathlib import Path

# 添加 code 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from ci_evaluation_harness import CIEvaluationHarness, EvalSample, SimpleLLMClient


class TestSimpleLLMClient(unittest.TestCase):
    """SimpleLLMClient 测试"""

    def test_generate_returns_capital_answer(self):
        """测试首都问题生成相关回答"""
        client = SimpleLLMClient()
        answer = client.generate("中国的首都是哪里？")
        self.assertIn("北京", answer)

    def test_generate_returns_python_answer(self):
        """测试 Python 问题生成相关回答"""
        client = SimpleLLMClient()
        answer = client.generate("What is Python?")
        self.assertIn("Python", answer)


class TestCIEvaluationHarness(unittest.TestCase):
    """CIEvaluationHarness 测试"""

    def setUp(self):
        self.client = SimpleLLMClient()
        self.harness = CIEvaluationHarness(self.client, threshold=-0.05)
        self.dataset = [
            EvalSample("q1", "中国的首都是哪里？", "北京是中国的首都。", "geography"),
            EvalSample("q2", "Python 是什么？", "Python 是一种流行的编程语言。", "tech"),
        ]

    def test_score_prediction_exact_match(self):
        """测试完全匹配的评分"""
        score = self.harness.score_prediction("北京是中国的首都。", "北京是中国的首都。")
        self.assertEqual(score, 1.0)

    def test_score_prediction_partial_match(self):
        """测试部分匹配的评分"""
        score = self.harness.score_prediction("北京 是 中国 的 首都", "北京 是 首都")
        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)

    def test_run_evaluation_returns_metrics(self):
        """测试评估返回关键指标"""
        result = self.harness.run_evaluation(self.dataset)
        self.assertIn("avg_score", result)
        self.assertIn("avg_latency_ms", result)
        self.assertIn("num_samples", result)
        self.assertEqual(result["num_samples"], 2)
        self.assertGreaterEqual(result["avg_score"], 0.0)
        self.assertLessEqual(result["avg_score"], 1.0)

    def test_check_regression_passes_when_improved(self):
        """测试分数提升时通过回归检查"""
        regression = self.harness.check_regression(0.85, 0.80)
        self.assertTrue(regression["passed"])
        self.assertEqual(regression["delta"], 0.05)

    def test_check_regression_fails_when_severe_regression(self):
        """测试严重回归时检查失败"""
        regression = self.harness.check_regression(0.70, 0.80)
        self.assertFalse(regression["passed"])
        self.assertEqual(regression["delta"], -0.1)

    def test_generate_report_contains_status(self):
        """测试报告包含状态信息"""
        eval_result = self.harness.run_evaluation(self.dataset)
        regression = self.harness.check_regression(eval_result["avg_score"], 0.75)
        report = self.harness.generate_report(eval_result, regression)
        self.assertIn("LLM CI 评估报告", report)
        self.assertIn("状态", report)

    def test_load_golden_dataset(self):
        """测试加载黄金数据集"""
        dataset_path = Path(__file__).parent.parent / "code" / "golden_dataset.json"
        samples = self.harness.load_golden_dataset(str(dataset_path))
        self.assertEqual(len(samples), 3)
        self.assertEqual(samples[0].id, "q1")


if __name__ == "__main__":
    unittest.main()
