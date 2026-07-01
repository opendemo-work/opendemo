<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# BitsAndBytes 量化

> 本案例详解 BitsAndBytes (bnb) 量化技术，NF4 格式原理与 LLM.int8() 推理加速实战

## 核心原理

### NF4 格式

```
NF4 (4-bit Normal Float) 专为神经网络设计：
- 非均匀量化，分段设置量化间隔
- 量化间隔在零点附近更密，远离零点更疏
- 更好地捕捉权重分布特性

NF4 量化表 (16 个值):
[-1.0, -0.696, -0.525, -0.394, -0.275, -0.183, -0.113, -0.051, 
  0.051,  0.113,  0.183,  0.275,  0.394,  0.525,  0.696,  1.0]
```

### BitsAndBytes 核心特性

| 特性 | 描述 | 效果 |
|------|------|------|
| NF4 | 4bit 量化格式 | 4x 显存减少 |
| Double Quant | 量化因子二次量化 | 额外 30% 减少 |
| LLM.int8() | 8bit 混合量化 | 2x 加速，精度保持 |

## 实现代码

### NF4 量化配置

```python
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,                    # 启用 4bit 加载
    bnb_4bit_quant_type="nf4",            # NF4 量化格式
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,       # 双重量化
)

# 加载量化模型
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)
```

### LLM.int8() 实现

```python
class LLMInt8Linear(nn.Module):
    def __init__(self, in_features, out_features, bias=False):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        
        # 8bit 量化权重
        self.weight_int8 = None
        self.weight_scale = None
        
    def quantize_llm_int8(self, weight):
        # 分离异常值通道 (> 阈值)
        threshold = 6.0
        mask = (weight.abs() > threshold).float()
        weight_abs = weight.abs()
        
        # 正常通道进行 INT8 量化
        normal_weight = weight * (1 - mask)
        max_val = normal_weight.abs().max()
        scale = max_val / 127.0
        
        self.weight_int8 = (normal_weight / scale).round().to(torch.int8)
        self.weight_scale = scale
        self.outliers = weight * mask
        
    def forward(self, x):
        # INT8 部分计算
        w_int8 = self.weight_int8.to(x.dtype)
        output_int8 = torch.nn.functional.linear(x, w_int8) * self.weight_scale
        
        # 异常值部分计算 (FP16)
        if self.outliers is not None:
            output_fp16 = torch.nn.functional.linear(x, self.outliers)
            return output_int8 + output_fp16
        
        return output_int8
```

## 稳定性处理

```python
# 处理 LLM.int8() 溢出问题
def stable_llm_int8_forward(x, weight, threshold=6.0):
    # 检测异常值
    quant_mask = (weight.abs() > threshold).any(dim=0)
    
    # 分离处理
    quant_weight = weight.clone()
    quant_weight[:, quant_mask] = 0
    
    fp16_weight = weight[:, quant_mask]
    int8_weight = quant_weight
    
    # 分开计算后合并
    out = F.linear(x, int8_weight) + F.linear(x, fp16_weight)
    return out
```

## 使用命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装 BitsAndBytes
pip install bitsandbytes

# 4bit 加载
python -m transformers-cli download meta-llama/Llama-2-7b

# 推理测试
python inference.py --model Llama-2-7b --quantization bnb4
```

## 学习要点

1. **NF4 格式**：专为 LLM 设计的非均匀 4bit 量化
2. **双重量化**：量化因子本身再量化，额外节省显存
3. **LLM.int8()**：混合精度处理异常值，保持稳定精度
4. **阈值调整**：threshold 影响精度与速度平衡

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

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

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 AI/ML 核心概念。

### 2. 适用场景

- 场景 1：学术研究
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
python code/main.py
```
