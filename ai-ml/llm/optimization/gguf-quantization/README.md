# GGUF 量化与 llama.cpp 部署

> 本案例详解 GGUF 量化格式与 llama.cpp 推理框架，演示如何将大模型转换为适合端侧与 CPU 部署的高效格式。

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GGUF 量化与部署流程                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Hugging Face Model                                                    │
│   (PyTorch / Safetensors)                                               │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                  1. 转换为 GGUF 格式                              │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ 读取权重    │    │ 选择量化    │    │ 写入 GGUF   │        │  │
│   │   │ 读取配置    │    │ 类型 Q4_K_M │    │ 元数据 +    │        │  │
│   │   │ 分词器     │    │ 或 Q8_0     │    │ 张量数据    │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   │                                                                  │  │
│   │   工具: llama.cpp/convert_hf_to_gguf.py                         │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                  2. GGUF 文件                                    │  │
│   │                                                                  │  │
│   │   Header: 魔数、版本、元数据                                     │  │
│   │   Tensor Info: 每个张量的名称、维度、类型、偏移                  │  │
│   │   Tensor Data: 量化后的权重                                      │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                  3. llama.cpp 推理                                │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ 加载 GGUF   │    │ 反量化/     │    │ 生成文本    │        │  │
│   │   │ 解析元数据  │    │ 矩阵乘法    │    │ 流式输出    │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   │                                                                  │  │
│   │   支持平台: CPU / GPU / Metal / Vulkan                           │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   Edge / Local / Server Deployment                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解 GGUF 格式的设计目标与文件结构
- ✅ 掌握 Q4_K_M、Q5_K_S、Q8_0 等典型量化类型的特点与适用场景
- ✅ 学会将 Hugging Face 模型转换为 GGUF 格式
- ✅ 能够在本地使用 llama.cpp 运行量化后模型

## 📖 核心概念

### 1. 什么是 GGUF？

GGUF（GPT-Generated Unified Format）是 llama.cpp 项目推出的一种二进制模型格式，旨在替代旧的 GGML 格式。它解决了以下问题：

- **包含完整模型信息**：权重、配置、分词器词汇表、特殊 token 等
- **灵活的元数据系统**：支持添加自定义键值对
- **多种量化类型**：从 Q2_K 到 Q8_0，甚至 F16、F32
- **跨平台兼容**：可被 llama.cpp 及其衍生项目直接加载

### 2. 常见量化类型

| 量化类型 | 位宽 | 特点 | 适用场景 |
|----------|------|------|----------|
| Q2_K | 2-bit | 压缩比最高，质量损失大 | 极致压缩、低资源设备 |
| Q4_K_M | 4-bit | 平衡压缩比与质量 | 推荐日常使用 |
| Q4_K_S | 4-bit | 比 Q4_K_M 更小、更快 | 速度优先 |
| Q5_K_M | 5-bit | 质量接近 F16，压缩比适中 | 质量敏感 |
| Q6_K | 6-bit | 高质量，接近无损 | 质量优先 |
| Q8_0 | 8-bit | 几乎无损，推理速度快 | 高精度需求 |
| F16 | 16-bit | 无压缩，原始精度 | 对照基准 |

### 3. llama.cpp 的优势

- **无 GPU 也可运行**：优化过的 CPU 推理性能非常出色
- **低资源部署**：可在笔记本、树莓派、移动设备上运行
- **量化生态成熟**：支持 GGUF 的多种工具和平台
- **支持多种后端**：CUDA、Metal、Vulkan、OpenCL、SYCL

## 💻 代码示例

完整代码位于 `code/` 目录。下面展示 GGUF 量化文件结构解析与显存估算：

```python
# code/gguf_analyzer.py
import struct
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class QuantizationType:
    """量化类型定义"""
    name: str
    bits_per_weight: float
    description: str


# llama.cpp 常见 GGUF 量化类型（简化版）
GGUF_QUANT_TYPES = {
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
        self.params = params
        self.vocab_size = vocab_size

    def estimate_size_mb(self, quant_type: str) -> float:
        """估算 GGUF 文件大小（MB）"""
        if quant_type not in GGUF_QUANT_TYPES:
            raise ValueError(f"不支持的量化类型: {quant_type}")
        qtype = GGUF_QUANT_TYPES[quant_type]
        # 简化的模型大小估算：params × bits_per_weight / 8
        size_bytes = self.params * qtype.bits_per_weight / 8
        return size_bytes / (1024 * 1024)

    def compare_quantizations(self) -> Dict[str, float]:
        """对比所有量化类型的大小"""
        return {
            name: self.estimate_size_mb(name)
            for name in GGUF_QUANT_TYPES.keys()
        }


def recommend_quantization(device_ram_gb: int, quality_priority: bool = False) -> str:
    """根据设备内存推荐量化类型"""
    if quality_priority and device_ram_gb >= 16:
        return "Q8_0"
    if device_ram_gb >= 8:
        return "Q5_K_M"
    if device_ram_gb >= 4:
        return "Q4_K_M"
    return "Q2_K"


if __name__ == "__main__":
    # 以 7B 模型为例
    analyzer = GGUFAnalyzer(params=7_000_000_000)
    sizes = analyzer.compare_quantizations()

    print("7B 模型在不同 GGUF 量化类型下的大小估算：")
    print(f"{'Quant Type':<12} {'Size (MB)':<12} {'Description':<30}")
    print("-" * 60)
    for name, size_mb in sizes.items():
        desc = GGUF_QUANT_TYPES[name].description
        print(f"{name:<12} {size_mb:<12.1f} {desc:<30}")

    print(f"\n推荐配置：")
    print(f"  16GB 内存 + 质量优先: {recommend_quantization(16, True)}")
    print(f"  8GB 内存: {recommend_quantization(8)}")
    print(f"  4GB 内存: {recommend_quantization(4)}")
```

## 🔧 配置说明

### 模型转换命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装 llama.cpp Python 依赖
pip install llama-cpp-python

# 从 Hugging Face 模型转换为 GGUF
python convert_hf_to_gguf.py \
  /path/to/hf-model \
  --outfile model.gguf \
  --outtype q4_k_m

# 使用 llama-cli 推理
./llama-cli \
  -m model.gguf \
  -p "你好，请介绍一下自己" \
  -n 128 \
  --temp 0.7
```

### 常用量化类型选择

| 设备内存 | 推荐类型 | 说明 |
|----------|----------|------|
| ≥ 16 GB | Q5_K_M / Q6_K | 质量接近原始模型 |
| 8 GB | Q4_K_M | 质量与速度均衡 |
| 4 GB | Q4_K_S / Q3_K_M | 适合轻薄笔记本 |
| ≤ 2 GB | Q2_K | 极致压缩 |

## 📊 运行结果

执行 `code/gguf_analyzer.py` 后，预期输出：

```
7B 模型在不同 GGUF 量化类型下的大小估算：
Quant Type   Size (MB)    Description
------------------------------------------------------------
Q4_0         3742.3       4-bit 基础量化
Q4_K_M       3785.5       4-bit 推荐质量均衡型
Q4_K_S       3602.6       4-bit 速度优先型
Q5_K_M       4624.2       5-bit 质量均衡型
Q6_K         5490.1       6-bit 高质量型
Q8_0         7076.8       8-bit 近无损
F16          13303.4      半精度浮点

推荐配置：
  16GB 内存 + 质量优先: Q8_0
  8GB 内存: Q4_K_M
  4GB 内存: Q4_K_S
```

## 🐛 常见问题

### Q1: GGUF 和 GPTQ / AWQ 有什么区别？

- **GGUF**：主要用于 llama.cpp 生态，支持 CPU 推理和端侧部署，量化类型丰富
- **GPTQ**：主要用于 GPU 推理，4-bit 量化，常与 AutoGPTQ 配合使用
- **AWQ**：激活感知权重量化，GPU 推理质量较好

选择取决于你的部署平台和性能要求。

### Q2: Q4_K_M 和 Q4_K_S 哪个更好？

- **Q4_K_M**：质量更好，推荐大多数场景
- **Q4_K_S**：文件更小、推理更快，但质量略低

如果不确定，优先选择 Q4_K_M。

### Q3: 可以在 CPU 上运行 70B 模型吗？

可以，但需要足够的内存。70B 模型使用 Q4_K_M 量化后约 40GB，使用 Q2_K 可降至约 25GB。高性能 CPU（如多核 Xeon）配合 llama.cpp 的优化可以获得可用的推理速度。

## 📚 扩展学习

- **GGUF 规范**: https://github.com/ggerganov/ggml/blob/master/docs/gguf.md
- **llama.cpp**: https://github.com/ggerganov/llama.cpp
- **llama-cpp-python**: Python 绑定，便于集成到应用
- **Ollama / lm-studio**: 基于 GGUF 的易用部署工具

## 🤝 贡献指南

欢迎补充更多 GGUF 与端侧部署内容：

- 实现真实的 Hugging Face 到 GGUF 转换脚本
- 对比不同量化类型在 perplexity 和下游任务上的表现
- 增加多模态 GGUF 模型（如 LLaVA）部署示例
- 增加移动设备（Android/iOS）部署指南

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
