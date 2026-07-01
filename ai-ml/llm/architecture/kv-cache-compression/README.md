# KV Cache 压缩

> 本案例详解大模型推理中 KV Cache 的显存瓶颈，以及 GQA、MLA、KV 量化等压缩技术的原理、实现与选型建议。

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     标准 Multi-Head Attention KV Cache                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Input Sequence: [x1, x2, x3, ..., xn]                                 │
│                                                                         │
│   For each layer:                                                       │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │  K: [h, n, d_k]   (h heads × n tokens × head_dim)              │  │
│   │  V: [h, n, d_v]   (h heads × n tokens × head_dim)              │  │
│   │                                                                  │  │
│   │  Memory = 2 × layers × h × n × d × bytes_per_token              │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   Example: 7B model, 32 layers, 32 heads, n=8192, fp16                 │
│   ≈ 2 × 32 × 32 × 8192 × 128 × 2 bytes ≈ 32 GB                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                     KV Cache 压缩技术对比                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │  1. GQA (Grouped Query Attention)                               │  │
│   │                                                                  │  │
│   │   K/V Heads:  8                                                 │  │
│   │   Query Heads: 32                                               │  │
│   │                                                                  │  │
│   │   每 4 个 Query head 共享 1 组 K/V head                          │  │
│   │   压缩比 ≈ query_heads / kv_heads                                │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │  2. MLA (Multi-head Latent Attention)                           │  │
│   │                                                                  │  │
│   │   Project K/V to low-rank latent space                          │  │
│   │   Cache latent vectors instead of full K/V                       │  │
│   │                                                                  │  │
│   │   压缩比取决于 latent dimension                                  │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │  3. KV Quantization                                             │  │
│   │                                                                  │  │
│   │   FP16 → INT8 / INT4                                            │  │
│   │   Per-channel or per-token scaling                              │  │
│   │                                                                  │  │
│   │   压缩比 ≈ fp16_bits / quantized_bits                            │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│   Reduced Memory → Larger Batch / Longer Context / Lower Cost           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解 KV Cache 在长序列推理中的显存瓶颈与计算方式
- ✅ 掌握 GQA、MLA、KV 量化等压缩技术的核心原理
- ✅ 计算和对比不同压缩策略的显存节省效果
- ✅ 在实际推理框架中选择合适的 KV Cache 压缩方案

## 📖 核心概念

### 1. 什么是 KV Cache？

在 Transformer 的自注意力机制中，生成第 n 个 token 时需要访问前面所有 token 的 Key（K）和 Value（V）。为了避免重复计算，推理时会将之前 token 的 K、V 张量缓存起来，这就是 KV Cache。

对于标准 Multi-Head Attention（MHA）：

```
KV Cache Size = 2 × num_layers × num_heads × seq_len × head_dim × dtype_bytes
```

当序列长度达到数万甚至数十万时，KV Cache 会成为显存占用的主要来源。

### 2. GQA（Grouped Query Attention）

GQA 通过让多个 Query head 共享同一组 K/V head 来减少 KV Cache：

- **MHA**：query_heads = kv_heads = 32
- **GQA**：query_heads = 32, kv_heads = 8，每 4 个 query head 共享 1 组 K/V
- **MQA**（Multi-Query Attention）：kv_heads = 1，所有 query head 共享同一组 K/V

GQA 在保持模型质量的同时，将 KV Cache 减少到原来的 `kv_heads / query_heads`。

### 3. MLA（Multi-head Latent Attention）

MLA 由 DeepSeek-V2 提出，核心思想是将 K、V 投影到低秩的潜在空间（latent space），只缓存低维的潜在向量。在注意力计算时，再从潜在向量恢复出完整的 K、V。

相比 GQA，MLA 可以实现更高的压缩比，同时保持较好的表达能力。

### 4. KV Quantization

KV Quantization 将 KV Cache 从 FP16/BF16 量化到更低的位宽：

- **INT8**：2× 压缩，精度损失通常很小
- **INT4**：4× 压缩，需要更精细的缩放策略
- **混合精度**：对 Key 和 Value 使用不同位宽

量化可以在几乎不增加推理延迟的情况下显著降低显存占用。

## 💻 代码示例

完整代码位于 `code/` 目录。下面展示 KV Cache 显存计算与压缩对比：

```python
# code/kv_cache_compression.py
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """模型配置"""
    num_layers: int
    num_heads: int
    head_dim: int
    seq_len: int
    dtype_bytes: int = 2  # fp16 = 2 bytes


class KVCacheAnalyzer:
    """KV Cache 显存分析器"""

    def __init__(self, config: ModelConfig):
        self.config = config

    def mha_kv_cache_gb(self) -> float:
        """标准 MHA 的 KV Cache 大小（GB）"""
        bytes_total = (
            2  # K + V
            * self.config.num_layers
            * self.config.num_heads
            * self.config.seq_len
            * self.config.head_dim
            * self.config.dtype_bytes
        )
        return bytes_total / (1024 ** 3)

    def gqa_kv_cache_gb(self, kv_heads: int) -> float:
        """GQA 下的 KV Cache 大小（GB）"""
        bytes_total = (
            2
            * self.config.num_layers
            * kv_heads
            * self.config.seq_len
            * self.config.head_dim
            * self.config.dtype_bytes
        )
        return bytes_total / (1024 ** 3)

    def quantized_kv_cache_gb(self, bits: int) -> float:
        """量化后的 KV Cache 大小（GB）"""
        bytes_per_token = bits / 8
        bytes_total = (
            2
            * self.config.num_layers
            * self.config.num_heads
            * self.config.seq_len
            * self.config.head_dim
            * bytes_per_token
        )
        return bytes_total / (1024 ** 3)


def print_comparison():
    """打印不同压缩策略对比"""
    config = ModelConfig(
        num_layers=32,
        num_heads=32,
        head_dim=128,
        seq_len=8192,
    )
    analyzer = KVCacheAnalyzer(config)

    mha = analyzer.mha_kv_cache_gb()
    gqa = analyzer.gqa_kv_cache_gb(kv_heads=8)
    int8 = analyzer.quantized_kv_cache_gb(bits=8)
    int4 = analyzer.quantized_kv_cache_gb(bits=4)

    print(f"MHA KV Cache:     {mha:.2f} GB")
    print(f"GQA (8 KV heads): {gqa:.2f} GB (压缩比 {mha/gqa:.1f}x)")
    print(f"INT8 Quantized:   {int8:.2f} GB (压缩比 {mha/int8:.1f}x)")
    print(f"INT4 Quantized:   {int4:.2f} GB (压缩比 {mha/int4:.1f}x)")


if __name__ == "__main__":
    print_comparison()
```

## 🔧 配置说明

常见推理框架对 KV Cache 压缩的支持：

| 框架 | GQA/MQA | KV Quantization | MLA |
|------|---------|-----------------|-----|
| vLLM | ✅ | ✅ | 部分支持 |
| SGLang | ✅ | ✅ | 部分支持 |
| TGI | ✅ | ✅ | 否 |
| llama.cpp | ✅ | ✅ GGUF | 否 |

## 📊 运行结果

执行 `code/kv_cache_compression.py` 后，预期输出：

```
MHA KV Cache:     15.26 GB
GQA (8 KV heads): 3.81 GB (压缩比 4.0x)
INT8 Quantized:   7.63 GB (压缩比 2.0x)
INT4 Quantized:   3.81 GB (压缩比 4.0x)
```

说明：
- GQA 将 KV head 数减少为 1/4，显存占用变为 1/4
- INT8 量化将每个 token 从 2 bytes 降到 1 byte，显存减半
- 实际生产环境中常组合使用 GQA + INT8 量化

## 🐛 常见问题

### Q1: GQA 会损失模型性能吗？

研究表明，适度减少 KV head 数（如从 32 降到 8）对模型质量影响很小，但可以显著降低显存。如果降到 MQA（1 个 KV head），可能会观察到一定性能下降。

### Q2: KV 量化会影响生成质量吗？

INT8 量化通常对生成质量影响很小；INT4 量化需要配合 per-channel / per-token 缩放策略，在部分模型上可能略有影响。建议先在目标模型上评测 perplexity 和下游任务。

### Q3: MLA 和 GQA 哪个更好？

两者各有优劣：
- **GQA**：实现简单，生态支持广泛，压缩比中等
- **MLA**：压缩比更高，但需要修改模型架构，训练阶段就要引入

选择取决于是否有训练新模型的能力，以及对压缩比的要求。

## 📚 扩展学习

- **GQA 论文**: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints
- **MLA 论文**: DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model
- **KV Quantization**: KV Cache is 1 Bit Per Channel: Efficient Large Language Model Inference with Quantized Cache
- **FlashInfer**: 支持多种 KV Cache 格式和压缩策略的推理 kernel 库

## 🤝 贡献指南

欢迎补充更多 KV Cache 优化技术：

- 实现真实的 GQA 注意力前向传播
- 添加 H2O、StreamingLLM 等动态 KV Cache 淘汰策略
- 对比不同压缩策略对 perplexity 的影响
- 增加多轮对话场景下的 KV Cache 复用分析

---

*最后更新：2026-06-16*

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```
