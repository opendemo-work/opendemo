"""
数据清洗 Pipeline 单元测试

使用标准库 unittest，无需额外安装 pytest 即可运行。
"""

import sys
import unittest
from pathlib import Path

# 添加 code 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from curation_pipeline import DataCurationPipeline


class TestDataCurationPipeline(unittest.TestCase):
    """DataCurationPipeline 测试用例"""

    def test_normalize_removes_extra_whitespace(self):
        """测试标准化去除多余空白"""
        pipeline = DataCurationPipeline({})
        self.assertEqual(pipeline.normalize("  hello   world  "), "hello world")

    def test_exact_dedup_removes_duplicates(self):
        """测试精确去重"""
        pipeline = DataCurationPipeline({})
        self.assertTrue(pipeline.exact_dedup("same document"))
        self.assertFalse(pipeline.exact_dedup("same document"))
        self.assertTrue(pipeline.exact_dedup("different document"))

    def test_quality_filter_by_length(self):
        """测试长度过滤"""
        pipeline = DataCurationPipeline({"min_length": 10, "min_unique_words": 2})
        self.assertTrue(pipeline.quality_filter("this is long enough"))
        self.assertFalse(pipeline.quality_filter("short"))

    def test_quality_filter_by_symbol_ratio(self):
        """测试特殊字符占比过滤"""
        pipeline = DataCurationPipeline({"min_length": 1, "max_symbol_ratio": 0.3, "min_unique_words": 2})
        self.assertTrue(pipeline.quality_filter("hello world"))
        self.assertFalse(pipeline.quality_filter("!!!@@@###"))

    def test_remove_pii_masks_email_and_phone(self):
        """测试 PII 脱敏"""
        pipeline = DataCurationPipeline({})
        text = "联系 example@email.com 或 13800138000"
        masked = pipeline.remove_pii(text)
        self.assertIn("[EMAIL]", masked)
        self.assertIn("[PHONE]", masked)
        self.assertNotIn("example@email.com", masked)
        self.assertNotIn("13800138000", masked)

    def test_full_pipeline(self):
        """测试完整 Pipeline"""
        config = {
            "min_length": 15,
            "max_symbol_ratio": 0.3,
            "min_unique_words": 3,
        }
        pipeline = DataCurationPipeline(config)

        docs = [
            "这是第一段有效的训练文本，内容足够长，可以通过过滤。",
            "这是第一段有效的训练文本，内容足够长，可以通过过滤。",
            "!!! 太多符号 !!!",
            "联系 admin@example.com 获取帮助。",
        ]

        result = pipeline.process(docs)
        # 第 1 条保留，第 2 条去重，第 3 条过滤，第 4 条保留并脱敏
        self.assertEqual(len(result), 2)
        self.assertNotIn("admin@example.com", result[1])
        self.assertIn("[EMAIL]", result[1])


if __name__ == "__main__":
    unittest.main()
