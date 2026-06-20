"""
GGUF 量化分析器

本脚本提供 GGUF 量化类型的介绍、文件大小估算和配置推荐。
所有计算均为理论估算，便于快速对比不同量化方案。
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class QuantizationType:
    """量化类型定义

    Attributes:
        name: 量化类型名称
        bits_per_weight: 每个权重的平均位数（含 overhead）
        description: 中文描述
    """

    name: str
    bits_per_weight: float
    description: str


# llama.cpp 常见 GGUF 量化类型（简化版，bits_per_weight 为经验估算值）
GGUF_QUANT_TYPES: Dict[str, QuantizationType] = {
    "Q2_K": QuantizationType("Q2_K", 2.63, "2-bit 极致压缩"),
    "Q3_K_M": QuantizationType("Q3_K_M", 3.06, "3-bit 质量均衡型"),
    "Q4_0": QuantizationType("Q4_0", 4.5, "4-bit 基础量化"),
    "Q4_K_M": QuantizationType("Q4_K_M", 4.55, "4-bit 推荐质量均衡型"),
    "Q4_K_S": QuantizationType("Q4_K_S", 4.33, "4-bit 速度优先型"),
    "Q5_K_M": QuantizationType("Q5_K_M", 5.55, "5-bit 质量均衡型"),
    "Q6_K": QuantizationType("Q6_K", 6.59, "6-bit 高质量型"),
    "Q8_0": QuantizationType("Q8_0", 8.5, "8-bit 近无损"),
    "F16": QuantizationType("F16", 16.0, "半精度浮点"),
}


class GGUFAnalyzer:
    """GGUF 文件分析器"""

    def __init__(self, params: int, vocab_size: int = 32000):
        """
        初始化分析器

        Args:
            params: 模型参数量
            vocab_size: 词表大小（当前未参与大小估算，保留扩展）
        """
        self.params = params
        self.vocab_size = vocab_size

    def estimate_size_mb(self, quant_type: str) -> float:
        """估算指定量化类型的 GGUF 文件大小（MB）

        Args:
            quant_type: 量化类型名称

        Returns:
            估算文件大小（MB）
        """
        if quant_type not in GGUF_QUANT_TYPES:
            raise ValueError(f"不支持的量化类型: {quant_type}")
        qtype = GGUF_QUANT_TYPES[quant_type]
        size_bytes = self.params * qtype.bits_per_weight / 8
        return size_bytes / (1024 * 1024)

    def compare_quantizations(self) -> Dict[str, float]:
        """对比所有量化类型的文件大小"""
        return {
            name: self.estimate_size_mb(name) for name in GGUF_QUANT_TYPES.keys()
        }

    def recommend_quantization(
        self, device_ram_gb: int, quality_priority: bool = False
    ) -> str:
        """根据设备内存推荐量化类型

        Args:
            device_ram_gb: 设备可用内存（GB）
            quality_priority: 是否优先考虑质量

        Returns:
            推荐的量化类型名称
        """
        if quality_priority and device_ram_gb >= 16:
            return "Q8_0"
        if device_ram_gb >= 8:
            return "Q5_K_M"
        if device_ram_gb >= 4:
            return "Q4_K_M"
        if device_ram_gb >= 2:
            return "Q3_K_M"
        return "Q2_K"


def print_comparison(params: int = 7_000_000_000):
    """打印量化类型对比"""
    analyzer = GGUFAnalyzer(params=params)
    sizes = analyzer.compare_quantizations()

    print(f"{params / 1e9:.1f}B 模型在不同 GGUF 量化类型下的大小估算：")
    print(f"{'Quant Type':<12} {'Size (MB)':<12} {'Description':<30}")
    print("-" * 60)
    for name, size_mb in sizes.items():
        desc = GGUF_QUANT_TYPES[name].description
        print(f"{name:<12} {size_mb:<12.1f} {desc:<30}")


if __name__ == "__main__":
    print_comparison(params=7_000_000_000)

    analyzer = GGUFAnalyzer(params=7_000_000_000)
    print("\n推荐配置：")
    print(f"  16GB 内存 + 质量优先: {analyzer.recommend_quantization(16, True)}")
    print(f"  8GB 内存: {analyzer.recommend_quantization(8)}")
    print(f"  4GB 内存: {analyzer.recommend_quantization(4)}")
