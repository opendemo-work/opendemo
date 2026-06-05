# INT8 量化实战

> 本案例详解 INT8 量化技术，理解动态量化与静态量化的实现差异，掌握 LLM 推理部署优化

## 核心概念

### 量化原理

```
FP32 → 量化 → INT8 → 反量化 → FP32
       ↓
  Scale: 0.01
  Zero: 128
```

### 量化方案对比

| 类型 | 权重 | 激活 | 速度 | 精度损失 |
|------|------|------|------|---------|
| FP32 | FP32 | FP32 | 1x | 无 |
| INT8 动态 | INT8 | FP32 | 2-3x | 低 |
| INT8 静态 | INT8 | INT8 | 3-4x | 中等 |
| INT8 QAT | INT8 | INT8 | 3-4x | 低 |

## 实现代码

### 动态量化

```python
import torch
import torch.nn as nn

class DynamicQuantizedLinear(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        
    def forward(self, x):
        # 动态量化权重
        quantized_weight = self.linear.weight().quantize(
            dtype=torch.qint8,
            qscheme=torch.per_tensor_symmetric
        )
        # 动态反量化计算
        return torch.ops.aten._quantize_linear(
            x, quantized_weight, self.linear.bias, 'none'
        )
```

### 静态量化

```python
from torch.ao.quantization import QuantStub, DeQuantStub

class StaticQuantizedTransformer(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.quant = QuantStub()
        self.dequant = DeQuantStub()
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        
    def forward(self, x):
        x = self.quant(x)
        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)
        x = self.dequant(x)
        return x
```

## 部署命令

```bash
# 动态量化推理
python quantize.py --mode dynamic --model LLM

# 静态量化校准
python quantize.py --mode static --calibrate --dataset wiki

# 导出 TorchScript
torch.jit.save(model_quantized, 'model_int8.pt')
```

## 学习要点

1. **动态量化**：权重 INT8，激活 FP32，适合 CPU 推理
2. **静态量化**：权重+激活都 INT8，需要校准数据集
3. **QAT**：量化感知训练，精度损失最小
4. **部署**：TorchScript 导出生产环境使用
