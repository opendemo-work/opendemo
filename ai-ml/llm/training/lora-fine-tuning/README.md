<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# LoRA 低秩适配微调

> 本案例详解 LoRA (Low-Rank Adaptation) 原理，演示如何在有限资源下高效微调大模型

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 解释 LoRA 的核心思想：大模型权重矩阵的低秩更新假设
- ✅ 使用 PyTorch 实现 `LoRALinear` 层，理解 `W' = W + (B @ A) * (alpha / rank)` 的数学含义
- ✅ 冻结预训练权重，只训练低秩矩阵 A 和 B
- ✅ 计算 LoRA 带来的参数节省比例
- ✅ 区分 LoRA、QLoRA、DoRA 等变体的适用场景

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    LoRA 微调原理                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  原始权重 W ∈ R^{d×k} (冻结)                                     │
│                                                                 │
│       ┌──────────────────────────────────────┐                 │
│       │            Forward Pass               │                 │
│       │                                      │                 │
│       │   h = W · x                          │                 │
│       │                                      │                 │
│       │   W 保持冻结,只更新 A 和 B            │                 │
│       └──────────────────────────────────────┘                 │
│                                                                 │
│  LoRA 增量更新:                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │   h = W · x + BA · x                                    │   │
│  │         │      └── LoRA 部分 (可训练)                    │   │
│  │         │                                               │   │
│  │         └── 原始权重 (冻结)                              │   │
│  │                                                          │   │
│  │   其中: B ∈ R^{d×r}, A ∈ R^{r×k}, r << min(d,k)        │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

参数效率对比:

Full Fine-tuning:              LoRA Fine-tuning:
┌─────────────────────┐       ┌─────────────────────┐
│  W: d×k (全部更新)   │       │  W: d×k (冻结)      │
│  需要更新全部参数     │       │  B: d×r (新增)      │
│                     │       │  A: r×k (新增)      │
│  7B 模型: ~28GB     │       │  r=8: ~8MB         │
└─────────────────────┘       └─────────────────────┘
```

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | >= 3.9 | 推荐使用 Python 3.10/3.11 |
| PyTorch | >= 2.0.0 | CPU 版本即可运行演示 |

### 安装与运行

```bash
# 1. 进入案例目录
cd ai-ml/llm/training/lora-fine-tuning

# 2. 安装依赖（建议使用虚拟环境）
pip install -r requirements.txt

# 3. 运行 LoRA 微调演示
python code/train_demo.py

# 4. 运行单元测试
python -m pytest tests/test_lora.py -v
```

### 预期输出

```
=== LoRA 微调演示 ===
预训练模型...
预训练后 Loss: 0.00xxxx
可训练参数: 1152 / 18624 (6.19%)
LoRA 微调...
微调后 Loss: 0.00xxxx
测试 Loss: 0.00xxxx
✅ LoRA 微调演示完成
```

---

## 🎯 核心概念

### 1. LoRA 核心思想

LoRA 的关键洞察：**大模型的权重矩阵通常是低秩的**

对于预训练模型，任务适配时权重更新可以分解为低秩矩阵：

```
ΔW = W_finetuned - W_pretrained ≈ B · A

其中 B ∈ R^{d×r}, A ∈ R^{r×k}, r << min(d,k)
```

### 2. 参数效率

| 秩 r | 参数量 (d=4096, k=4096) | 相对比例 |
|------|--------------------------|----------|
| 0 (全量微调) | 16,777,216 | 100% |
| 4 | 65,536 | 0.39% |
| 8 | 131,072 | 0.78% |
| 16 | 262,144 | 1.56% |
| 64 | 1,048,576 | 6.25% |

### 3. LoRA 超参数

```python
LoraConfig {
    r: int = 8                    # 低秩维度
    lora_alpha: int = 16          # 缩放因子
    lora_dropout: float = 0.05   # Dropout 概率
    target_modules: List[str]     # 应用 LoRA 的模块
}
```

## 💻 代码示例

### LoRA 层实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Optional
import math

class LoRALinear(nn.Module):
    """LoRA 线性层"""
    def __init__(
        self,
        in_features: int,
        out_features: int,
        rank: int = 8,
        alpha: int = 16,
        dropout: float = 0.05,
        bias: bool = True
    ):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.alpha = alpha
        self.scaling = alpha / rank

        # 原始权重 (冻结)
        self.weight = nn.Parameter(
            torch.randn(out_features, in_features),
            requires_grad=False
        )
        if bias:
            self.bias = nn.Parameter(torch.zeros(out_features))
        else:
            self.bias = None

        # LoRA 参数
        self.lora_A = nn.Parameter(torch.randn(rank, in_features) * 0.01)
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
        self.lora_dropout = nn.Dropout(p=dropout)

        # 初始化 A 为随机矩阵，B 为零矩阵
        # 这样初始状态 ΔW = BA = 0
        nn.init.normal_(self.lora_A, std=0.02)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 原始 forward
        base_output = F.linear(x, self.weight, self.bias)

        # LoRA 增量
        # x @ A^T @ B^T = x @ A^T @ B^T
        lora_output = (
            self.lora_dropout(x) 
            @ self.lora_A.T 
            @ self.lora_B.T
        ) * self.scaling

        return base_output + lora_output

    def merge_weights(self):
        """合并 LoRA 权重到原始权重"""
        W_merged = self.weight + self.lora_B.T @ self.lora_A.T * self.scaling
        return W_merged


class LoRAPatch(nn.Module):
    """将标准 Linear 层转换为 LoRA 层"""
    def __init__(self, linear: nn.Linear, rank: int = 8, alpha: int = 16, dropout: float = 0.05):
        super().__init__()
        self.in_features = linear.in_features
        self.out_features = linear.out_features
        self.rank = rank
        self.alpha = alpha
        self.scaling = alpha / rank

        # 复制原始权重并冻结
        self.weight = linear.weight.clone()
        self.weight.requires_grad = False
        if linear.bias is not None:
            self.bias = linear.bias.clone()
            self.bias.requires_grad = False
        else:
            self.bias = None

        # LoRA 参数
        self.lora_A = nn.Parameter(torch.randn(rank, in_features) * 0.01)
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
        self.lora_dropout = nn.Dropout(p=dropout)

    def forward(self, x):
        base = F.linear(x, self.weight, self.bias)
        lora = (self.lora_dropout(x) @ self.lora_A.T @ self.lora_B.T) * self.scaling
        return base + lora


def apply_lora_to_model(
    model: nn.Module,
    target_modules: List[str],
    rank: int = 8,
    alpha: int = 16,
    dropout: float = 0.05
) -> nn.Module:
    """将模型指定层替换为 LoRA 层"""
    for name, module in model.named_modules():
        for target in target_modules:
            if target in name and isinstance(module, nn.Linear):
                parent_name = '.'.join(name.split('.')[:-1])
                child_name = name.split('.')[-1]
                parent = model.get_submodule(parent_name) if parent_name else model

                lora_linear = LoRALinear(
                    in_features=module.in_features,
                    out_features=module.out_features,
                    rank=rank,
                    alpha=alpha,
                    dropout=dropout,
                    bias=module.bias is not None
                )

                # 复制原始权重
                lora_linear.weight.data = module.weight.data.clone()
                lora_linear.weight.requires_grad = False
                if module.bias is not None:
                    lora_linear.bias.data = module.bias.data.clone()
                    lora_linear.bias.requires_grad = False

                setattr(parent, child_name, lora_linear)
                print(f"Applied LoRA to: {name}")

    return model
```

### 训练脚本

```python
import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

def train_lora_model():
    # 加载基础模型
    model_name = "meta-llama/Llama-2-7b-hf"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )

    # 配置 LoRA
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=[
            "q_proj", "v_proj", "k_proj", 
            "o_proj", "gate_proj", "up_proj", "down_proj"
        ],
        bias="none"
    )

    # 应用 LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    # 输出: trainable params: 8,388,608 || all params: 6,738,415,616 || trainable%: 0.124%

    # 准备数据
    train_dataset = ...  # 你的指令数据集
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

    # 训练配置
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    model.train()

    # 训练循环
    for epoch in range(3):
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")

    # 保存 LoRA 权重
    model.save_pretrained("./lora_weights")

    return model


def merge_and_export(model, output_path):
    """合并 LoRA 权重并导出"""
    merged_model = model.merge_and_unload()
    merged_model.save_pretrained(output_path)
```

## 📊 不同 LoRA 变体对比

| 变体 | 原理 | 适用场景 |
|------|------|----------|
| **LoRA** | 标准低秩分解 | 通用微调 |
| **QLoRA** | 4-bit NF4 + LoRA | 消费级 GPU |
| **LoRA+** | 自适应学习率 | 稳定训练 |
| **AdaLoRA** | 动态秩调整 | 极端效率 |
| **DoRA** | 权重分解方向 | 更高精度 |

## 📋 命令速查

```bash
# 安装依赖
pip install peft bitsandbytes transformers accelerate

# 训练 QLoRA
python lora_fine_tuning/train_qlora.py --model_name meta-llama/Llama-2-7b

# 导出合并后的模型
python lora_fine_tuning/merge_model.py --lora_path ./lora_weights

# 推理测试
python lora_fine_tuning/inference.py --model_path ./merged_model
```

## 📚 学习要点

1. **低秩假设**：大模型权重更新本质是低秩的
2. **参数效率**：通过冻结原始权重，只训练小部分参数
3. **推理延迟**：可选择合并权重或动态注入
4. **秩的选择**：r 越大精度越高，但参数量也增加

## 🔗 相关案例

- `q-lora-tuning` - QLoRA 高效微调
- `adalora-fine-tuning` - AdaLoRA 自适应秩分配
- `rlhf-introduction` - RLHF 对齐训练
- `dpo-training` - DPO 直接偏好优化

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 AI/ML 核心概念。

### 2. 适用场景

- 场景 1：学术研究
- 场景 2：工程实践
- 场景 3：面试准备
