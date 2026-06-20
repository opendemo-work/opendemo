"""
KV Cache 压缩分析器单元测试

使用标准库 unittest，无需额外安装 pytest 即可运行。
"""

import sys
import unittest
from pathlib import Path

# 添加 code 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from kv_cache_compression import KVCacheAnalyzer, ModelConfig, compare_strategies


class TestKVCacheAnalyzer(unittest.TestCase):
    """KVCacheAnalyzer 测试"""

    def setUp(self):
        self.config = ModelConfig(
            num_layers=2,
            num_heads=4,
            head_dim=8,
            seq_len=16,
            dtype_bytes=2,
        )
        self.analyzer = KVCacheAnalyzer(self.config)

    def test_mha_kv_cache_positive(self):
        """测试 MHA KV Cache 为正数"""
        memory = self.analyzer.mha_kv_cache_gb()
        self.assertGreater(memory, 0)

    def test_gqa_reduces_memory(self):
        """测试 GQA 能减少显存占用"""
        mha = self.analyzer.mha_kv_cache_gb()
        gqa = self.analyzer.gqa_kv_cache_gb(kv_heads=2)
        self.assertLess(gqa, mha)
        self.assertEqual(mha / gqa, 2.0)

    def test_mqa_reduces_memory_more(self):
        """测试 MQA 比 GQA 压缩比更高"""
        gqa = self.analyzer.gqa_kv_cache_gb(kv_heads=2)
        mqa = self.analyzer.mqa_kv_cache_gb()
        self.assertLess(mqa, gqa)

    def test_quantization_reduces_memory(self):
        """测试量化能减少显存占用"""
        mha = self.analyzer.mha_kv_cache_gb()
        int8 = self.analyzer.quantized_kv_cache_gb(bits=8)
        int4 = self.analyzer.quantized_kv_cache_gb(bits=4)
        self.assertLess(int8, mha)
        self.assertLess(int4, int8)

    def test_compression_ratio(self):
        """测试压缩比计算"""
        mha = self.analyzer.mha_kv_cache_gb()
        int8 = self.analyzer.quantized_kv_cache_gb(bits=8)
        ratio = self.analyzer.compression_ratio(int8)
        self.assertAlmostEqual(ratio, mha / int8)

    def test_compare_strategies(self):
        """测试策略对比返回多个结果"""
        results = compare_strategies(self.config)
        self.assertIn("MHA", results)
        self.assertIn("GQA (8 KV heads)", results)
        self.assertIn("INT8 Quantized", results)


if __name__ == "__main__":
    unittest.main()
