"""
GGUF 量化分析器单元测试

使用标准库 unittest，无需额外安装 pytest 即可运行。
"""

import sys
import unittest
from pathlib import Path

# 添加 code 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from gguf_analyzer import GGUFAnalyzer, GGUF_QUANT_TYPES


class TestGGUFAnalyzer(unittest.TestCase):
    """GGUFAnalyzer 测试"""

    def setUp(self):
        self.analyzer = GGUFAnalyzer(params=7_000_000_000)

    def test_estimate_size_positive(self):
        """测试估算大小为正数"""
        size = self.analyzer.estimate_size_mb("Q4_K_M")
        self.assertGreater(size, 0)

    def test_q8_smaller_than_f16(self):
        """测试 Q8_0 比 F16 小"""
        q8 = self.analyzer.estimate_size_mb("Q8_0")
        f16 = self.analyzer.estimate_size_mb("F16")
        self.assertLess(q8, f16)

    def test_q4_smaller_than_q8(self):
        """测试 Q4_K_M 比 Q8_0 小"""
        q4 = self.analyzer.estimate_size_mb("Q4_K_M")
        q8 = self.analyzer.estimate_size_mb("Q8_0")
        self.assertLess(q4, q8)

    def test_invalid_quant_type_raises(self):
        """测试无效量化类型抛出异常"""
        with self.assertRaises(ValueError):
            self.analyzer.estimate_size_mb("INVALID")

    def test_compare_quantizations(self):
        """测试对比所有量化类型"""
        sizes = self.analyzer.compare_quantizations()
        self.assertEqual(len(sizes), len(GGUF_QUANT_TYPES))
        self.assertIn("Q4_K_M", sizes)
        self.assertIn("F16", sizes)

    def test_recommend_quantization(self):
        """测试量化类型推荐"""
        self.assertEqual(self.analyzer.recommend_quantization(16, True), "Q8_0")
        self.assertEqual(self.analyzer.recommend_quantization(8), "Q5_K_M")
        self.assertEqual(self.analyzer.recommend_quantization(4), "Q4_K_M")
        self.assertEqual(self.analyzer.recommend_quantization(2), "Q3_K_M")
        self.assertEqual(self.analyzer.recommend_quantization(1), "Q2_K")


if __name__ == "__main__":
    unittest.main()
