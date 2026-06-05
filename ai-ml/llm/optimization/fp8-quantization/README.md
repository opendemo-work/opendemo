# FP8 量化原理与实践

> 本案例详解 FP8 (8-bit Floating Point) 量化技术，理解其在 LLM 中的应用和性能收益

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    FP8 量化架构                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  数值格式对比:                                                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  FP32 (32-bit Float)                                    │   │
│  │  ┌──────┬───────────────────────────────┐              │   │
│  │  │ Sign │ Exponent (8) │ Mantissa (23)  │              │   │
│  │  └──────┴───────────────────────────────┘              │   │
│  │  范围: ~3.4e38  精度: ~7 位十进制                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  FP16 (16-bit Float)                                    │   │
│  │  ┌──────┬─────────────┬──────────────┐                 │   │
│  │  │ Sign │ Exponent(5) │ Mantissa(10) │                 │   │
│  │  └──────┴─────────────┴──────────────┘                 │   │
│  │  范围: ~65500  精度: ~3 位十进制                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  BF16 (Brain Float)                                     │   │
│  │  ┌──────┬─────────────┬──────────────┐                 │   │
│  │  │ Sign │ Exponent(8) │ Mantissa(7)  │                 │   │
│  │  └──────┴─────────────┴──────────────┘                 │   │
│  │  范围: ~3.4e38  精度: ~2 位十进制                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  FP8 E4M3 (4-bit Exp, 3-bit Mantissa)                   │   │
│  │  ┌──────┬───────────┬──────────┐                        │   │
│  │  │ Sign │ Exp (4)   │ Mant(3)  │                        │   │
│  │  └──────┴───────────┴──────────┘                        │   │
│  │  范围: ±448  精度: ~2 位十进制                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  FP8 E5M2 (5-bit Exp, 2-bit Mantissa)                   │   │
│  │  ┌──────┬───────────┬──────────┐                        │   │
│  │  │ Sign │ Exp (5)   │ Mant(2)  │                        │   │
│  │  └──────┴───────────┴──────────┘                        │   │
│  │  范围: ±57344  精度: ~1 位十进制                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

FP8 在 Transformer 中的应用位置:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│         Layer Norm ──▶ FP8 ──▶ QKV Proj ──▶ FP8                 │
│                           │                                     │
│                           ▼                                     │
│                      ┌─────────┐                               │
│                      │ Attention│                               │
│                      └─────────┘                               │
│                           │                                     │
│                           ▼                                     │
│         Layer Norm ──▶ FP8 ──▶ Output Proj ──▶ FP8              │
│                           │                                     │
│                           ▼                                     │
│                      ┌─────────┐                               │
│                      │  FFN    │                               │
│                      └─────────┘                               │
│                           │                                     │
└─────────────────────────────────────────────────────────────────┘

Weight Only vs Activation Quantization:

Weight Only (用于推理):
  ┌─────────────────────────────────────┐
  │  weights: INT8/FP8 (量化)           │
  │  activations: FP16/BF16 (原生)      │
  └─────────────────────────────────────┘

Activation-Aware Quantization (用于训练):
  ┌─────────────────────────────────────┐
  │  weights: FP8 (原生或量化)          │
  │  activations: FP8 (量化)           │
  └─────────────────────────────────────┘
```

## 🎯 核心概念

### 1. FP8 格式

| 格式 | E (指数位) | M (尾数位) | 范围 | 精度 | 用途 |
|------|-----------|-----------|------|------|------|
| **E4M3** | 4 | 3 | ±448 | ~2位 | weights, activations |
| **E5M2** | 5 | 2 | ±57344 | ~1位 | gradients, optimizer states |

### 2. FP8 在 LLM 中的优势

```
Transformer 训练瓶颈:
1. 显存占用大 (activations ∝ batch_size × seq_len × hidden_dim)
2. 计算密集 (矩阵乘法占主导)
3. 通信瓶颈 (分布式训练)

FP8 优化效果:
- 显存减少: 50%+ (相比 BF16)
- 带宽减少: 50%+ 
- 计算速度: 2-3x (Tensor Core 原生支持)
```

### 3. 量化策略

```python
# FP8 量化配置
quantization_config = {
    "quant_method": "fp8",
    "activation_scheme": "dynamic",  # or "static"
    "weights": "fp8_e4m3",
    "activations": "fp8_e5m2",
}
```

## 💻 完整实现

### PyTorch FP8 实现

```python
import torch
import torch.nn as nn
from torch._tensor import Tensor
from typing import Optional

class FP8Quantizer:
    """FP8 量化器"""
    
    # FP8 格式定义
    FP8_E4M3_MAX = 448.0
    FP8_E5M2_MAX = 57344.0
    
    @staticmethod
    def quantize_e4m3(tensor: torch.Tensor) -> torch.Tensor:
        """E4M3 量化 (用于 weights 和 activations)"""
        # 缩放到 FP8 范围
        scale = tensor.abs().max() / FP8Quantizer.FP8_E4M3_MAX
        scaled = tensor / scale
        
        # Clamp 到 [-448, 448]
        clamped = torch.clamp(scaled, -FP8Quantizer.FP8_E4M3_MAX, FP8Quantizer.FP8_E4M3_MAX)
        
        # Round 到最近的 FP8 值
        quantized = torch.round(clamped).to(torch.float8_e4m3fn)
        
        return quantized, scale
    
    @staticmethod
    def quantize_e5m2(tensor: torch.Tensor) -> torch.Tensor:
        """E5M2 量化 (用于 gradients)"""
        scale = tensor.abs().max() / FP8Quantizer.FP8_E5M2_MAX
        scaled = tensor / scale
        clamped = torch.clamp(scaled, -FP8Quantizer.FP8_E5M2_MAX, FP8Quantizer.FP8_E5M2_MAX)
        quantized = torch.round(clamped).to(torch.float8_e5m2)
        
        return quantized, scale
    
    @staticmethod
    def dequantize(quantized: torch.Tensor, scale: torch.Tensor) -> torch.Tensor:
        """反量化"""
        return quantized.to(torch.float32) * scale


class FP8Linear(nn.Module):
    """FP8 量化线性层"""
    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        
        # 原始权重 (BF16)
        self.weight = nn.Parameter(torch.randn(out_features, in_features, dtype=torch.bfloat16))
        if bias:
            self.bias = nn.Parameter(torch.zeros(out_features, dtype=torch.bfloat16))
        else:
            self.bias = None
            
        # 缩放因子
        self.weight_scale = None
        self.activation_scale = None
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 量化权重
        weight_fp8, self.weight_scale = FP8Quantizer.quantize_e4m3(self.weight)
        
        # 动态量化 activations
        if x.dtype == torch.bfloat16:
            x_fp8, self.activation_scale = FP8Quantizer.quantize_e4m3(x)
        else:
            x_fp8 = x
            
        # 执行矩阵乘法 (FP8)
        output = torch.matmul(x_fp8, weight_fp8.t())
        
        # 反量化并加偏置
        if self.activation_scale is not None and self.weight_scale is not None:
            output = output * self.activation_scale * self.weight_scale
            
        if self.bias is not None:
            output = output + self.bias
            
        return output.to(torch.bfloat16)
```

### Transformer 中的 FP8

```python
import torch.nn as nn

class FP8TransformerLayer(nn.Module):
    """支持 FP8 的 Transformer 层"""
    def __init__(self, d_model: int, num_heads: int, d_ff: int):
        super().__init__()
        
        # Self Attention
        self.q_proj = FP8Linear(d_model, d_model)
        self.k_proj = FP8Linear(d_model, d_model)
        self.v_proj = FP8Linear(d_model, d_model)
        self.o_proj = FP8Linear(d_model, d_model)
        
        # FFN
        self.gate_proj = FP8Linear(d_model, d_ff)
        self.up_proj = FP8Linear(d_model, d_ff)
        self.down_proj = FP8Linear(d_ff, d_model)
        
        # Layer Norm (保持高精度)
        self.input_norm = nn.LayerNorm(d_model, dtype=torch.bfloat16)
        self.output_norm = nn.LayerNorm(d_model, dtype=torch.bfloat16)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Pre-LN
        x_norm = self.input_norm(x)
        
        # Self Attention
        q = self.q_proj(x_norm)
        k = self.k_proj(x_norm)
        v = self.v_proj(x_norm)
        
        # Attention 计算 (使用 BF16，因为 attention 计算对精度敏感)
        attn_output = nn.functional.scaled_dot_product_attention(q, k, v)
        attn_output = self.o_proj(attn_output)
        
        # 残差连接
        x = x + attn_output
        
        # Post-LN
        x_norm = self.output_norm(x)
        
        # FFN (SwiGLU)
        gate = nn.functional.silu(self.gate_proj(x_norm))
        up = self.up_proj(x_norm)
        ffn_output = self.down_proj(gate * up)
        
        # 残差连接
        x = x + ffn_output
        
        return x
```

### 使用 TransformerEngine

```python
# 使用 NVIDIA TransformerEngine
try:
    import transformer_engine.pytorch as te
    from transformer_engine.common.recipe import FP8Recipe

    # FP8 配方配置
    fp8_recipe = FP8Recipe(
        forward=True,      # 前向量化
        backward=True,     # 反向量化
        optimize=True,     # 优化器状态量化
    )

    class TETransformerLayer(nn.Module):
        def __init__(self, d_model: int, num_heads: int, d_ff: int):
            super().__init__()
            
            self.attn = te.MultiHeadAttention(
                d_model=d_model,
                n_heads=num_heads,
                qkv_format="thd"
            )
            
            self.mlp = te.FeedForward(
                d_model=d_model,
                d_ff=d_ff,
                activation="swiglu"
            )
            
            self.input_norm = te.LayerNorm(d_model)
            self.output_norm = te.LayerNorm(d_model)
            
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            # 使用 FP8
            with te.fp8_autocast(enabled=True, fp8_recipe=fp8_recipe):
                # Pre-LN
                x_norm = self.input_norm(x)
                
                # Attention
                qkv, _ = self.attn.qkv_mem_eff_attention(
                    te.SeqAttention(q=x_norm, k=x_norm, v=x_norm)
                )
                x = x + qkv
                
                # Post-LN
                x_norm = self.output_norm(x)
                
                # FFN
                x = x + self.mlp(x_norm)
                
            return x

except ImportError:
    print("TransformerEngine not installed. Install with: pip install transformer-engine")
```

### 训练配置

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import MixedPrecision
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy

def setup_fp8_training():
    """配置 FP8 训练"""
    
    # 混合精度配置
    mixed_precision_policy = MixedPrecision(
        param_dtype=torch.bfloat16,
        reduce_dtype=torch.float32,
        buffer_dtype=torch.bfloat16,
        # FP8 用于某些操作
    )
    
    # 模型包装
    model = FSDP(
        your_model,
        auto_wrap_policy=transformer_auto_wrap_policy,
        mixed_precision=mixed_precision_policy,
    )
    
    # 优化器配置
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=1e-4,
        # FP8 优化器状态 (需要 TransformerEngine)
    )
    
    return model, optimizer
```

## 📊 性能对比

### 显存节省

| 精度 | Activations (bs=1, seq=4096, hidden=4096) | 相对 BF16 |
|------|------------------------------------------|-----------|
| BF16 | ~64 GB | 1.0x |
| FP8 | ~32 GB | 0.5x |
| INT8 | ~16 GB | 0.25x |

### 计算性能

| 硬件 | BF16 TFLOPs | FP8 TFLOPs | 加速比 |
|------|-------------|------------|--------|
| A100 | 312 | 1248 | 4x |
| H100 | 989 | 3958 | 4x |

## 📋 命令速查

```bash
# 安装 TransformerEngine
pip install transformer-engine

# 启用 FP8 训练
torchrun --nproc_per_node=8 train.py \
    --fp8 True \
    --fp8_recipe forward_backward

# FP8 推理 (vLLM)
python -m vllm.entrypoints.openai.api_server \
    --model mymodel \
    --quantization fp8

# 验证 FP8 量化精度
python verify_fp8.py --model mymodel --task mmlu
```

## 📚 学习要点

1. **E4M3 vs E5M2**：E4M3 用于 weights/activations，E5M2 用于 gradients
2. **动态 vs 静态量化**：动态量化更简单，静态量化更精确
3. **Transformer Engine**：H100 原生支持，需要使用 TE 库
4. **精度 vs 速度**：FP8 通常在 0.99+ 精度保持

## 🔗 相关案例

- `int8-quantization` - INT8 量化实战
- `int4-quantization` - INT4 量化技术
- `gptq-quantization` - GPTQ 后训练量化
- `torch-compile` - PyTorch 编译优化
