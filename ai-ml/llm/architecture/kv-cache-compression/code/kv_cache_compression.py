"""
KV Cache 压缩技术分析器

本脚本演示如何计算和对比不同 KV Cache 压缩策略下的显存占用，包括：
- 标准 Multi-Head Attention (MHA)
- Grouped Query Attention (GQA)
- KV Quantization (INT8 / INT4)

所有计算均为理论显存估算，便于快速评估不同方案。
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelConfig:
    """模型配置

    Attributes:
        num_layers: Transformer 层数
        num_heads: Query head 数量
        head_dim: 每个 head 的维度
        seq_len: 序列长度
        dtype_bytes: 数据类型字节数，fp16=2，bf16=2，fp32=4
    """

    num_layers: int
    num_heads: int
    head_dim: int
    seq_len: int
    dtype_bytes: int = 2


class KVCacheAnalyzer:
    """KV Cache 显存分析器"""

    def __init__(self, config: ModelConfig):
        self.config = config

    def _base_bytes(self, heads: int, bytes_per_token: float) -> float:
        """计算基础 KV Cache 字节数"""
        return (
            2  # K + V
            * self.config.num_layers
            * heads
            * self.config.seq_len
            * self.config.head_dim
            * bytes_per_token
        )

    def mha_kv_cache_gb(self) -> float:
        """标准 MHA 的 KV Cache 大小（GB）"""
        bytes_total = self._base_bytes(
            self.config.num_heads, self.config.dtype_bytes
        )
        return bytes_total / (1024 ** 3)

    def gqa_kv_cache_gb(self, kv_heads: int) -> float:
        """GQA 下的 KV Cache 大小（GB）

        Args:
            kv_heads: K/V head 数量
        """
        bytes_total = self._base_bytes(kv_heads, self.config.dtype_bytes)
        return bytes_total / (1024 ** 3)

    def mqa_kv_cache_gb(self) -> float:
        """MQA 下的 KV Cache 大小（GB）"""
        return self.gqa_kv_cache_gb(kv_heads=1)

    def quantized_kv_cache_gb(self, bits: int) -> float:
        """量化后的 KV Cache 大小（GB）

        Args:
            bits: 量化位宽，如 8 表示 INT8
        """
        bytes_per_token = bits / 8
        bytes_total = self._base_bytes(self.config.num_heads, bytes_per_token)
        return bytes_total / (1024 ** 3)

    def compression_ratio(self, compressed_gb: float) -> float:
        """计算压缩比"""
        baseline = self.mha_kv_cache_gb()
        if compressed_gb == 0:
            return float("inf")
        return baseline / compressed_gb


def compare_strategies(config: ModelConfig) -> Dict[str, float]:
    """对比多种压缩策略的显存占用"""
    analyzer = KVCacheAnalyzer(config)

    results = {
        "MHA": analyzer.mha_kv_cache_gb(),
        "GQA (8 KV heads)": analyzer.gqa_kv_cache_gb(kv_heads=8),
        "GQA (4 KV heads)": analyzer.gqa_kv_cache_gb(kv_heads=4),
        "MQA": analyzer.mqa_kv_cache_gb(),
        "INT8 Quantized": analyzer.quantized_kv_cache_gb(bits=8),
        "INT4 Quantized": analyzer.quantized_kv_cache_gb(bits=4),
    }
    return results


def print_comparison(config: ModelConfig):
    """打印压缩策略对比"""
    results = compare_strategies(config)
    baseline = results["MHA"]

    print(f"模型配置: {config.num_layers} layers, {config.num_heads} heads, "
          f"{config.head_dim} head_dim, seq_len={config.seq_len}")
    print("-" * 60)
    print(f"{'Strategy':<20} {'Memory (GB)':<15} {'Compression Ratio':<20}")
    print("-" * 60)
    for name, memory_gb in results.items():
        ratio = baseline / memory_gb if memory_gb > 0 else float("inf")
        print(f"{name:<20} {memory_gb:<15.2f} {ratio:<20.1f}x")


def main():
    """主函数：演示 KV Cache 压缩对比"""
    config = ModelConfig(
        num_layers=32,
        num_heads=32,
        head_dim=128,
        seq_len=8192,
        dtype_bytes=2,
    )
    print_comparison(config)


if __name__ == "__main__":
    main()
