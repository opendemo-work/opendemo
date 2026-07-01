<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Reward Model 训练

> 本案例详解 Reward Model 原理，演示如何训练一个模型来评估人类偏好

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Reward Model 训练                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Reward Model 架构:                                              │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐
│  │                                                             │ │
│  │   Prompt: "如何学习编程?"                                    │ │
│  │           │                                                 │ │
│  │           ▼                                                 │ │
│  │   ┌─────────────────┐                                       │ │
│  │   │  Pretrained LM  │ (冻结或微调)                          │ │
│  │   │   (Backbone)    │                                       │ │
│  │   └────────┬────────┘                                       │ │
│  │            │                                                │ │
│  │            ▼                                                │ │
│  │   ┌─────────────────┐                                       │ │
│  │   │    Reward Head  │  (线性层 → 标量)                       │ │
│  │   │   R(s) ∈ ℝ      │                                       │ │
│  │   └─────────────────┘                                       │ │
│  │                                                             │ │
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
│  偏好数据格式:                                                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐
│  │  Prompt: "如何学习 Python?"                                  │ │
│  │                                                             │ │
│  │  Response A (chosen): "1. 基础语法..."  ✓                   │ │
│  │  Response B (rejected): "Python 是..."  ✗                  │ │
│  │                                                             │ │
│  │  Label: preferred = A                                       │ │
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
│  Bradley-Terry 损失函数:                                         │
│                                                                 │
│  L = -log(σ(R_chosen - R_rejected))                            │
│                                                                 │
│  即鼓励: R_chosen > R_rejected                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心概念

### 1. Reward Model 原理

Reward Model 训练一个模型来预测人类偏好：

- 输入: (prompt, response) → 输出: scalar reward
- 训练数据: 人类标注的偏好对
- 目标: R_chosen > R_rejected

### 2. 损失函数

```python
import torch
import torch.nn.functional as F

def reward_model_loss(reward_chosen, reward_rejected):
    """
    Bradley-Terry 模型损失
    
    L = -log(σ(R_chosen - R_rejected))
    """
    # 计算奖励差异
    reward_diff = reward_chosen - reward_rejected
    
    # Log-sigmoid 损失 (等于交叉熵)
    loss = -F.logsigmoid(reward_diff).mean()
    
    # 准确率: R_chosen > R_rejected 的比例
    accuracy = (reward_chosen > reward_rejected).float().mean()
    
    return loss, accuracy
```

### 3. 完整实现

```python
import torch
import torch.nn as nn
from transformers import AutoModel, AutoConfig

class RewardModel(nn.Module):
    """Reward Model: 基于预训练语言模型"""
    def __init__(self, model_name, num_padding_tokens=1):
        super().__init__()
        self.backbone = AutoModel.from_pretrained(model_name)
        hidden_size = self.backbone.config.hidden_size
        self.reward_head = nn.Linear(hidden_size, 1, bias=False)
        self.num_padding_tokens = num_padding_tokens
    
    def forward(self, input_ids, attention_mask):
        # 获取最后一层隐藏状态
        outputs = self.backbone(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        last_hidden = outputs.last_hidden_state
        
        # 只取 [EOS] token 或序列最后一个有效 token 的表示
        # 作为整个序列的 reward
        eos_mask = (input_ids == self.backbone.config.eos_token_id)
        eos_hidden = last_hidden * eos_mask.unsqueeze(-1)
        eos_hidden = eos_hidden.sum(dim=1) / eos_mask.sum(dim=1, keepdim=True).clamp(min=1)
        
        # 计算 reward
        reward = self.reward_head(eos_hidden).squeeze(-1)
        return reward

def train_reward_model():
    """训练 Reward Model"""
    model = RewardModel("meta-llama/Llama-2-7b")
    model = model.cuda()
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
    
    for epoch in range(num_epochs):
        for batch in dataloader:
            # 获取 chosen 和 rejected 的奖励
            reward_chosen = model(
                batch["chosen_input_ids"].cuda(),
                batch["chosen_attention_mask"].cuda()
            )
            reward_rejected = model(
                batch["rejected_input_ids"].cuda(),
                batch["rejected_attention_mask"].cuda()
            )
            
            # 计算损失
            loss, accuracy = reward_model_loss(reward_chosen, reward_rejected)
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            metrics["loss"].append(loss.item())
            metrics["accuracy"].append(accuracy.item())
    
    return model
```

## 偏好数据示例

| prompt | chosen | rejected | source |
|--------|--------|----------|--------|
| 如何学习 Python? | 详细学习路线... | Python 是... | HH-RLHF |
| 写一首诗 | 结构完整，意象丰富... | 太短，无韵律... | SHP |

## 命令速查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 训练 Reward Model
python train_reward_model.py \
    --model_name meta-llama/Llama-2-7b \
    --dataset Anthropic/hh-rlhf \
    --batch_size 4

# 使用 TRL 库
python -m trl.trainer.reward_trainer \
    --model_name meta-llama/Llama-2-7b \
    --dataset preference_data
```

## 学习要点

1. **标量奖励**：将序列映射为单一标量
2. **偏好学习**：用对比损失学习人类偏好
3. **EOS pooling**：使用结束符 token 表示序列
4. **数据质量**：偏好数据的质量决定 RM 效果

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
