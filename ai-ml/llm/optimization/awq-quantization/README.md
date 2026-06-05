# AWQ 激活感知权重量化

> 本案例详解 AWQ (Activation-Aware Weight Quantization) 技术，理解其与 GPTQ 的差异及 4bit 量化优势

## 核心原理

### AWQ vs GPTQ

```
GPTQ: 仅考虑权重分布，忽略激活值统计特性
AWQ:  权重 × 激活分布，综合考虑量化误差

AWQ 核心思想：
- 不是所有权重都同等重要
- 激活值大的通道，权重精度更关键
- 通过激活比例自动调整缩放因子
```

### 量化公式

```python
# AWQ 缩放因子计算
def compute_awq_scale(weight, activation):
    # 获取每个通道的激活最大值
    act_scale = activation.abs().max(dim=0)[0]
    # 计算缩放因子
    scale = (act_scale / act_scale.max()).sqrt()
    # 应用缩放
    scaled_weight = weight / scale
    return scaled_weight, scale
```

## 实现代码

### AWQ 4bit 量化

```python
import torch
import torch.nn as nn

class AWQQuantizer:
    def __init__(self, w_bit=4, group_size=128):
        self.w_bit = w_bit
        self.group_size = group_size
        
    def quantize_awq(self, weight, activation):
        # 计算缩放因子
        scale = self.compute_scale(weight, activation)
        # 缩放权重
        scaled_w = weight / scale
        # 分组量化
        quantized = self.group_quantize(scaled_w)
        return quantized, scale
    
    def compute_scale(self, weight, activation):
        # AWQ 核心：激活感知缩放
        act_scale = activation.abs().mean(dim=0)
        weight_scale = weight.abs().mean(dim=0)
        combined = act_scale * weight_scale
        scale = (combined / combined.max()).clamp(min=1e-4)
        return scale
    
    def group_quantize(self, tensor):
        # 分组量化实现
        shape = tensor.shape
        tensor = tensor.view(-1, self.group_size)
        # 找最大值并量化
        max_val = tensor.abs().max(dim=-1, keepdim=True)[0]
        scale = (max_val * 2 / (2**self.w_bit - 1)).clamp(min=1e-8)
        quantized = (tensor / scale).round().to(torch.int8)
        return quantized, scale
```

## 精度对比

| 方法 | WikiText-2 PPL | MMLU | 显存减少 |
|------|---------------|------|---------|
| FP16 | 12.5 | 68.2 | 1.0x |
| GPTQ INT4 | 14.2 | 63.5 | 4.0x |
| AWQ INT4 | 13.1 | 66.8 | 4.0x |

## 使用命令

```bash
# 安装 AWQ
pip install autoawq

# 量化模型
python -m awq.quantize model --w_bit 4 --group_size 128

# 推理验证
python evaluate.py --model awq_model --task mmlu
```

## 学习要点

1. **AWQ 优势**：激活感知量化，精度优于纯权重量化方法
2. **与 GPTQ 对比**：AWQ 在保持激活分布同时进行权重量化
3. **4bit 量化**：group_size 越小精度越高，显存越大
4. **适用场景**：需要高精度 LLaMA/Vicuna 等模型量化部署
