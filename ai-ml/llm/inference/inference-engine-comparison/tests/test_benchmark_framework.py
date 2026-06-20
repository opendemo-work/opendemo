"""
推理引擎对比框架单元测试

使用标准库 unittest，无需额外安装 pytest 即可运行。
"""

import sys
import unittest
from pathlib import Path

# 添加 code 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from benchmark_framework import (
    BenchmarkResult,
    recommend_engine,
    run_comparison,
    simulate_engine_inference,
)


class TestBenchmarkFramework(unittest.TestCase):
    """基准测试框架测试用例"""

    def test_simulate_engine_inference_returns_valid_result(self):
        """测试模拟推理返回有效结果"""
        result = simulate_engine_inference(
            engine="vllm",
            num_requests=100,
            avg_input_len=100,
            avg_output_len=50,
        )
        self.assertIsInstance(result, BenchmarkResult)
        self.assertEqual(result.engine, "vllm")
        self.assertGreater(result.throughput, 0)
        self.assertGreater(result.avg_latency, 0)
        self.assertGreater(result.p99_latency, result.avg_latency)
        self.assertGreater(result.gpu_memory_gb, 0)

    def test_run_comparison_returns_three_engines(self):
        """测试对比实验返回三个引擎结果"""
        results = run_comparison(
            num_requests=100,
            avg_input_len=100,
            avg_output_len=50,
        )
        self.assertEqual(len(results), 3)
        engines = {r.engine for r in results}
        self.assertEqual(engines, {"vllm", "tgi", "sglang"})

    def test_results_sorted_by_throughput(self):
        """测试结果按吞吐量降序排列"""
        results = run_comparison(
            num_requests=100,
            avg_input_len=100,
            avg_output_len=50,
        )
        for i in range(len(results) - 1):
            self.assertGreaterEqual(
                results[i].throughput,
                results[i + 1].throughput,
            )

    def test_recommend_engine_for_scenarios(self):
        """测试场景推荐"""
        self.assertEqual(recommend_engine("throughput"), "vllm")
        self.assertEqual(recommend_engine("latency"), "sglang")
        self.assertEqual(recommend_engine("structured"), "sglang")
        self.assertEqual(recommend_engine("ecosystem"), "tgi")

    def test_recommend_engine_defaults_to_vllm(self):
        """测试未知场景默认推荐 vllm"""
        self.assertEqual(recommend_engine("unknown"), "vllm")

    def test_invalid_engine_raises_error(self):
        """测试无效引擎抛出异常"""
        with self.assertRaises(ValueError):
            simulate_engine_inference(
                engine="invalid",
                num_requests=100,
                avg_input_len=100,
                avg_output_len=50,
            )


if __name__ == "__main__":
    unittest.main()
