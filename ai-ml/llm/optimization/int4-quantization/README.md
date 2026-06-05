# INT4 量化技术

> 本案例详解 INT4 量化，理解如何在极低精度下运行大模型

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    量化精度对比                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FP16 (16-bit):                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  1 sign │ 5 exp │ 10 mantissa                         │   │
│  │  16 bits total                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│  范围: ±65504  |  精度: ~3 位十进制                            │
│                                                                 │
│  INT8 (8-bit):                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  -128 to 127  (256 levels)                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│  范围: ±127  |  精度: ~2% 相对误差                            │
│                                                                 │
│  INT4 (4-bit):                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  -8 to 7  (16 levels)                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│  范围: ±7  |  精度: ~6% 相对误差                              │
│  压缩比: 4x vs FP16, 2x vs INT8                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

NF4 (4-bit NormalFloat) 格式:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  问题: 均匀量化的不足                                            │
│                                                                 │
│  解决方案: NF4 - 针对神经网络权重分布优化的 4-bit 格式          │
│                                                                 │
│  量化等级 (16 个):                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Q = { -1, -1/sqrt(2), -0.6966, -0.5, -0.3552,          │   │
│  │        -0.1010, 0, 0.1010, 0.3552, 0.5,               │   │
│  │        0.6966, 1/sqrt(2), 1 }                          │   │
│  │  (基于量化器权重分位数)                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  优势: 更适合权重分布，减少量化误差                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

GPTQ vs AWQ vs NF4:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  GPTQ (Post-Training Quantization):                             │
│  - 后训练量化                                                   │
│  - 逐列处理，使用近似 Hessian                                   │
│  - INT4/INT8                                                   │
│                                                                 │
│  AWQ (Activation-Aware Weight Quantization):                   │
│  - 考虑激活分布                                                  │
│  - 保护显著权重                                                  │
│  - INT4/FP16                                                   │
│                                                                 │
│  NF4 (NormalFloat4):                                            │
│  - QLoRA 使用                                                   │
│  - 最优 4-bit 量化器                                           │
│  - 需要反量化到 BF16 计算                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. INT4 量化原理

```python
# 量化过程
def quantize_int4(weights: torch.Tensor):
    """INT4 量化"""
    # 归一化到 [-8, 7]
    max_val = weights.abs().max()
    scale = max_val / 7.0  # INT4 范围是 -8 to 7
    
    # 量化
    quantized = torch.round(weights / scale).clamp(-8, 7)
    
    # 转换为 uint4 (0-15)
    uint4 = (quantized + 8).to(torch.uint8)
    
    return uint4, scale

def dequantize_int4(uint4: torch.Tensor, scale: torch.Tensor):
    """INT4 反量化"""
    # 转回有符号
    int4 = uint4.to(torch.int8) - 8
    
    # 反量化
    return int4 * scale
```

### 2. QLoRA 中的 NF4

```python
# QLoRA 使用的 NF4
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",  # NormalFloat4
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,  # 双重量化
)
```

### 3. INT4 vs 其他精度

| 精度 | 显存 (7B) | 推理速度 | 精度损失 |
|------|-----------|----------|----------|
| BF16 | 14GB | 1x | 无 |
| INT8 | 7GB | 1.3x | ~1% |
| INT4 | 3.5GB | 1.8x | ~3-5% |
| NF4 | 3.5GB | 1.7x | ~2% |

## 💻 完整实现

### INT4 量化器

```python
import torch
import torch.nn as nn
from typing import Optional

class Int4Quantizer:
    """INT4 量化器"""
    
    def __init__(self, group_size: int = 128):
        self.group_size = group_size
    
    def quantize(self, weights: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """
        量化权重到 INT4
        
        Args:
            weights: [out_features, in_features]
        
        Returns:
            quantized: uint8 tensor (每字节存储两个 INT4)
            scales: [out_features, num_groups]
        """
        out_features, in_features = weights.shape
        num_groups = (in_features + self.group_size - 1) // self.group_size
        
        # 扩展到分组大小
        padded = torch.nn.functional.pad(
            weights, 
            (0, self.group_size * num_groups - in_features)
        )
        padded = padded.view(out_features, num_groups, self.group_size)
        
        # 计算每组的 scale
        scales = padded.abs().amax(dim=-1, keepdim=True) / 7.0
        
        # 量化
        quantized = torch.round(padded / scales).clamp(-8, 7)
        
        # 打包为 uint8
        quantized = quantized.view(out_features, -1)
        quantized_int8 = quantized.to(torch.int8)
        
        # 打包两个 INT4 到一个字节
        q_low = (quantized_int8[:, ::2] & 0x0F).to(torch.uint8)
        q_high = ((quantized_int8[:, 1::2] << 4) & 0xF0).to(torch.uint8)
        packed = (q_low | q_high).to(torch.uint8)
        
        return packed, scales.squeeze(-1)
    
    def dequantize(self, packed: torch.Tensor, scales: torch.Tensor) -> torch.Tensor:
        """
        反量化
        
        Args:
            packed: uint8 tensor
            scales: [out_features, num_groups]
        """
        # 解包
        out_features, num_packed = packed.shape
        
        # 解包两个 INT4
        q_low = (packed & 0x0F).to(torch.int8)
        q_high = ((packed >> 4) & 0x0F).to(torch.int8)
        
        # 交错
        quantized = torch.zeros(out_features, num_packed * 2, dtype=torch.int8, device=packed.device)
        quantized[:, ::2] = q_low
        quantized[:, 1::2] = q_high
        
        # 反量化
        num_groups = scales.shape[1]
        quantized = quantized[:, :num_groups * self.group_size]
        quantized = quantized.view(out_features, num_groups, self.group_size)
        
        return quantized * scales.unsqueeze(-1)


class Int4Linear(nn.Module):
    """INT4 量化线性层"""
    
    def __init__(self, in_features, out_features, bias=False):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        
        # 原始权重 (FP16, 用于初始化)
        self.weight = nn.Parameter(torch.zeros(out_features, in_features))
        self.quantizer = Int4Quantizer()
        
        # 量化后的权重
        self.quantized_weight = None
        self.scales = None
    
    def quantize(self):
        """量化权重"""
        self.quantized_weight, self.scales = self.quantizer.quantize(self.weight.data)
    
    def forward(self, x):
        # 如果没有量化，先量化
        if self.quantized_weight is None:
            self.quantize()
        
        # 反量化到 FP16 计算
        weight_fp16 = self.quantizer.dequantize(
            self.quantized_weight, 
            self.scales
        ).to(x.dtype)
        
        return torch.nn.functional.linear(x, weight_fp16)
```

### 使用 BitsAndBytes

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# QLoRA 配置
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# 加载量化模型
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto",
)

# 推理
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
inputs = tokenizer("Hello, world!", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs)
```

### 使用 AutoGPTQ

```python
from autogptq import AutoGPTQForCausalLM, BaseQuantizeConfig

# 量化配置
quantize_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    desc_act=True,  # 激活顺序量化，更准确但更慢
)

# 加载模型
model = AutoGPTQForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantize_config=quantize_config,
)

# 量化 (需要校准数据)
model.quantize(train_dataset)

# 保存
model.save_quantized("llama-2-7b-int4-gptq")
```

## 📊 量化效果对比

### 显存节省

| 模型 | BF16 | INT8 | INT4 | 压缩比 |
|------|------|------|------|--------|
| LLaMA-2 7B | 14GB | 7GB | 3.5GB | 4x |
| LLaMA-2 13B | 26GB | 13GB | 6.5GB | 4x |
| LLaMA-2 70B | 140GB | 70GB | 35GB | 4x |

### 精度保持

| 方法 | WikiText PPL | C4 PPL | MMLU |
|------|--------------|---------|------|
| BF16 | 5.12 | 6.89 | 68% |
| INT8 | 5.18 | 6.95 | 67% |
| INT4 (GPTQ) | 5.35 | 7.10 | 63% |
| INT4 (AWQ) | 5.22 | 7.00 | 65% |

## 📋 命令速查

```bash
# QLoRA 推理
python -c "
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
model = AutoModelForCausalLM.from_pretrained(
    'meta-llama/Llama-2-7b-hf',
    quantization_config=BitsAndBytesConfig(load_in_4bit=True)
)
"

# 使用 GPTQ
pip install autogptq
python -c "from autogptq import AutoGPTQForCausalLM"

# 量化自己的模型
python quantize.py --model_path your-model --output_path model-int4
```

## 📚 学习要点

1. **NF4 优于均匀量化**：QLoRA 采用的分位数量化
2. **双重量化**：对 scale 也量化，进一步节省
3. **group_size 影响**：越小精度越高，显存越大
4. **需要反量化计算**：INT4 存储，但通常反量化到 BF16 计算

## 🔗 相关案例

- `fp8-quantization` - FP8 量化
- `gptq-quantization` - GPTQ 量化
- `awq-quantization` - AWQ 量化
- `q-lora-tuning` - QLoRA 微调
