"""
大模型数据清洗 Pipeline 示例

本脚本演示一个可扩展的数据清洗流程，包括：
- 文本标准化
- 精确去重
- 规则质量过滤
- PII 脱敏

注意：本示例仅使用标准库，便于在无网络环境下运行。
生产环境可扩展为使用 pandas、datasketch、presidio 等工具。
"""

import hashlib
import re
from typing import Any, Dict, List


class DataCurationPipeline:
    """大模型数据清洗 Pipeline"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化 Pipeline

        Args:
            config: 配置字典，包含 min_length、max_symbol_ratio 等阈值
        """
        self.config = config
        self.seen_hashes: set = set()

    def normalize(self, text: str) -> str:
        """文本标准化：统一编码、去除多余空白、过滤控制字符"""
        text = text.strip()
        # 统一空白字符为单个空格
        text = re.sub(r"\s+", " ", text)
        # 过滤不可见控制字符
        text = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]", "", text)
        return text

    def exact_dedup(self, text: str) -> bool:
        """精确去重

        Returns:
            True 表示保留（未重复），False 表示重复需丢弃
        """
        doc_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
        if doc_hash in self.seen_hashes:
            return False
        self.seen_hashes.add(doc_hash)
        return True

    def quality_filter(self, text: str) -> bool:
        """基于规则的质量过滤

        过滤条件：
        1. 文档长度不低于阈值
        2. 特殊字符占比不超过阈值
        3. 唯一词数不低于阈值（按空格分词简化处理）
        """
        min_len = self.config.get("min_length", 100)
        max_symbol_ratio = self.config.get("max_symbol_ratio", 0.3)
        min_unique_words = self.config.get("min_unique_words", 10)

        if len(text) < min_len:
            return False

        # 特殊字符占比
        symbol_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
        if symbol_count / max(len(text), 1) > max_symbol_ratio:
            return False

        # 唯一词数/字符数（中文按字符去重，英文按空格分词）
        # 对于中文字符，直接统计唯一字符数；对于英文，按空格分词
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            unique_units = set(c for c in text if '\u4e00' <= c <= '\u9fff')
        else:
            unique_units = set(text.split())
        if len(unique_units) < min_unique_words:
            return False

        return True

    def remove_pii(self, text: str) -> str:
        """简单 PII 脱敏

        覆盖：邮箱、中国大陆手机号、18 位身份证号
        """
        # 邮箱
        text = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", text
        )
        # 中国大陆手机号
        text = re.sub(r"1[3-9]\d{9}", "[PHONE]", text)
        # 18 位身份证号
        text = re.sub(r"\d{17}[\dXx]", "[ID_CARD]", text)
        return text

    def process(self, documents: List[str]) -> List[str]:
        """执行完整清洗流程

        Args:
            documents: 原始文档列表

        Returns:
            清洗后的文档列表
        """
        cleaned: List[str] = []
        for doc in documents:
            # 1. 标准化
            doc = self.normalize(doc)
            if not doc:
                continue

            # 2. 精确去重
            if not self.exact_dedup(doc):
                continue

            # 3. 质量过滤
            if not self.quality_filter(doc):
                continue

            # 4. PII 脱敏
            doc = self.remove_pii(doc)

            cleaned.append(doc)
        return cleaned


def main():
    """主函数：演示 Pipeline 效果"""
    config = {
        "min_length": 20,
        "max_symbol_ratio": 0.3,
        "min_unique_words": 5,
    }
    pipeline = DataCurationPipeline(config)

    raw_docs = [
        "  这是一段干净的训练文本，包含有效的中文内容，适合作为大模型预训练语料。  ",
        "这是一段干净的训练文本，包含有效的中文内容，适合作为大模型预训练语料。",
        "!!!@@@###  大量无意义符号  $$$%%%^^^",
        "请联系 example@email.com 或 13800138000 获取更多信息，我们会尽快回复。",
        "短。",
    ]

    result = pipeline.process(raw_docs)
    print(f"原始文档数: {len(raw_docs)}, 清洗后文档数: {len(result)}")
    for idx, doc in enumerate(result, 1):
        print(f"{idx}. {doc}")


if __name__ == "__main__":
    main()
