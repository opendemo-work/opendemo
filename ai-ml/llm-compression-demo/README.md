# 大语言模型压缩实战演示

## 🎯 学习目标

通过本案例你将掌握：
- 大语言模型压缩的基本技术和方法
- 模型量化、剪枝和知识蒸馏技术
- 压缩模型的性能评估和权衡分析
- 压缩模型的部署和推理优化

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- GPU或CPU环境
- 至少32GB内存用于模型压缩操作

### 依赖安装
```bash
pip install torch transformers accelerate
pip install bitsandbytes optimum neural-compressor  # 压缩工具
pip install torch-pruning  # 剪枝工具
pip install nni  # 神经网络智能工具包
```

## 📁 项目结构

```
llm-compression-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── quantize_model.py              # 模型量化脚本
│   ├── prune_model.py                 # 模型剪枝脚本
│   ├── distill_model.py               # 知识蒸馏脚本
│   └── compress_pipeline.py           # 压缩流水线脚本
├── configs/                           # 配置文件
│   ├── quantization_config.json       # 量化配置
│   ├── pruning_config.json            # 剪枝配置
│   └── distillation_config.json       # 蒸馏配置
├── models/                            # 模型文件
│   ├── original/                      # 原始模型
│   ├── quantized/                     # 量化模型
│   ├── pruned/                        # 剪枝模型
│   └── distilled/                     # 蒸馏模型
├── utils/                             # 工具函数
│   ├── compression_utils.py           # 压缩工具
│   ├── evaluation_utils.py            # 评估工具
│   └── visualization_utils.py         # 可视化工具
├── experiments/                       # 实验结果
│   ├── compression_ratios/            # 压缩比例数据
│   ├── performance_comparison/        # 性能对比数据
│   └── accuracy_tradeoffs/            # 准确性权衡数据
└── notebooks/                         # Jupyter笔记本
    ├── 01_quantization_techniques.ipynb   # 量化技术
    ├── 02_pruning_strategies.ipynb        # 剪枝策略
    └── 03_distillation_methods.ipynb      # 蒸馏方法
```

## 🚀 快速开始

### 步骤1：模型量化

```bash
# 对模型进行4-bit量化
python scripts/quantize_model.py \
  --model_name_or_path facebook/opt-350m \
  --output_dir models/quantized/ \
  --quantization_method bitsandbytes \
  --quantization_bits 4
```

### 步骤2：模型剪枝

```bash
# 对模型进行结构化剪枝
python scripts/prune_model.py \
  --model_path models/quantized/ \
  --output_dir models/pruned/ \
  --pruning_ratio 0.2 \
  --pruning_method magnitude
```

### 步骤3：知识蒸馏

```bash
# 使用知识蒸馏创建小型模型
python scripts/distill_model.py \
  --teacher_model facebook/opt-350m \
  --student_model facebook/opt-125m \
  --output_dir models/distilled/ \
  --distillation_loss mse
```

## 🔍 代码详解

### 核心概念解析

#### 1. 模型量化实现
```python
# 使用bitsandbytes进行量化
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 4-bit量化配置
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)
```

#### 2. 实际应用示例

##### 场景1：模型剪枝
```python
# 使用torch_pruning进行结构化剪枝
import torch_pruning as tp
import torch

def structured_pruning(model, importance, example_inputs, pruning_ratio):
    """结构化剪枝实现"""
    # 构建依赖图
    DG = tp.DependencyGraph().build_dependency(
        model, 
        example_inputs=example_inputs
    )
    
    # 获取重要性指标
    imp = importance(model)
    
    # 获取可剪枝组
    prunable_groups = []
    for m in model.modules():
        if isinstance(m, torch.nn.Linear) and m.out_features != model.config.vocab_size:
            prunable_groups.append(DG.get_pruning_group(m, tp.prune_linear_out_channels, idxs=[]))
    
    # 计算每个组的剪枝数量
    for group in prunable_groups:
        pruning_num = int(len(group.indices) * pruning_ratio)
        if pruning_num > 0:
            group.prune(pruning_num)
    
    return model
```

##### 场景2：知识蒸馏
```python
# 知识蒸馏实现
import torch
import torch.nn.functional as F

class DistillationTrainer:
    def __init__(self, teacher_model, student_model, alpha=0.5, temperature=3.0):
        self.teacher_model = teacher_model
        self.student_model = student_model
        self.alpha = alpha  # 软标签和硬标签的权重
        self.temperature = temperature  # 温度参数
    
    def compute_distillation_loss(self, student_outputs, teacher_outputs, labels):
        """计算蒸馏损失"""
        # 软标签损失 (KL散度)
        soft_loss = F.kl_div(
            F.log_softmax(student_outputs.logits / self.temperature, dim=-1),
            F.softmax(teacher_outputs.logits / self.temperature, dim=-1),
            reduction='batchmean'
        ) * (self.temperature ** 2)
        
        # 硬标签损失 (原始任务损失)
        hard_loss = F.cross_entropy(student_outputs.logits, labels)
        
        # 组合损失
        total_loss = self.alpha * soft_loss + (1 - self.alpha) * hard_loss
        return total_loss
```

## 🧪 验证测试

### 测试1：量化效果验证
```python
#!/usr/bin/env python
# 验证模型量化效果
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BitsAndBytesConfig
import sys

def test_quantization_effect():
    print("=== 模型量化效果验证 ===")
    
    model_name = "facebook/opt-125m"
    
    # 加载原始模型
    original_model = AutoModelForCausalLM.from_pretrained(model_name)
    original_size = sys.getsizeof(original_model.state_dict().__str__())
    
    print(f"原始模型大小: {original_model.get_memory_footprint() / 1024**3:.2f} GB")
    
    # 4-bit量化模型
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    quantized_model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    print(f"✅ 4-bit量化模型加载成功")
    print(f"量化后模型内存使用: {quantized_model.get_memory_footprint() / 1024**3:.2f} GB")
    
    # 验证推理功能
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    test_prompt = "The future of artificial intelligence"
    inputs = tokenizer(test_prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = quantized_model.generate(
            **inputs,
            max_length=len(inputs.input_ids[0]) + 20,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"✅ 量化模型推理功能正常")
    print(f"输入: {test_prompt}")
    print(f"输出: {generated_text[len(test_prompt):][:50]}...")

if __name__ == "__main__":
    test_quantization_effect()
```

### 测试2：压缩模型性能对比
```python
#!/usr/bin/env python
# 压缩模型性能对比
import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

def test_compression_performance():
    print("=== 压缩模型性能对比测试 ===")
    
    model_name = "facebook/opt-125m"
    
    # 加载量化模型
    from transformers import BitsAndBytesConfig
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    quantized_model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    test_prompt = "Explain quantum computing in simple terms"
    inputs = tokenizer(test_prompt, return_tensors="pt")
    
    # 测试推理时间
    start_time = time.time()
    with torch.no_grad():
        outputs = quantized_model.generate(
            **inputs,
            max_length=len(inputs.input_ids[0]) + 50,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    end_time = time.time()
    inference_time = end_time - start_time
    
    print(f"✅ 性能测试完成")
    print(f"推理时间: {inference_time:.2f} 秒")
    print(f"生成长度: {len(outputs[0]) - len(inputs.input_ids[0])} tokens")
    print(f"吞吐量: {(len(outputs[0]) - len(inputs.input_ids[0])) / inference_time:.2f} tokens/秒")

if __name__ == "__main__":
    test_compression_performance()
```

## ❓ 常见问题

### Q1: 如何选择合适的压缩比率？
**解决方案**：
```python
# 压缩比率选择指南
"""
1. 任务复杂度: 简单任务可以使用更高压缩比
2. 精度要求: 高精度要求的任务需谨慎压缩
3. 资源限制: 根据部署环境的资源约束选择
4. 性能权衡: 在速度提升和精度下降间找平衡
"""
```

### Q2: 如何评估压缩模型的质量？
**解决方案**：
```python
# 压缩模型质量评估
"""
1. 功能正确性: 确保基本功能正常
2. 性能指标: 评估准确率、F1分数等
3. 推理速度: 测量推理延迟和吞吐量
4. 内存使用: 测量内存占用减少情况
"""
```

## 📚 扩展学习

### 相关技术
- **AWQ**: Activation-aware Weight Quantization
- **GPTQ**: Generative Pre-trained Transformer Quantization
- **LoRA**: Low-Rank Adaptation（参数高效方法）
- **SparseGPT**: 结构化稀疏化方法

### 进阶学习路径
1. 掌握不同压缩技术的理论基础
2. 学习压缩感知和信息论基础
3. 理解硬件加速器对压缩模型的支持
4. 掌握自适应压缩和动态量化技术

### 企业级应用场景
- 边缘设备上的模型部署
- 移动端AI应用优化
- 云端推理服务成本优化
- 实时AI系统性能提升

---
> **💡 提示**: 大语言模型压缩是在资源受限环境下部署AI模型的关键技术，需要在模型大小、推理速度和准确率之间找到最佳平衡点。