# DPO 直接偏好优化

> 本案例详解 DPO (Direct Preference Optimization) 原理，实现更简单稳定的对齐训练

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    DPO vs RLHF 对比                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  RLHF (复杂，需要训练 Reward Model + PPO):                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │   Pretrained ──▶ SFT ──▶ Reward Model ──▶ PPO ──▶ Final  │   │
│  │                      Model      Training     Training      │   │
│  │                                 (~5B)      (~20B)       │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  DPO (简单，直接优化偏好):                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │   Pretrained ──▶ SFT ──▶ DPO Training ──▶ Final        │   │
│  │                      Model    (直接优化)                  │   │
│  │                                 (~7B)                   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

DPO 核心思想:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  偏好数据格式:                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Prompt: "Explain quantum entanglement"                 │   │
│  │                                                          │   │
│  │  Chosen: "Quantum entanglement is a phenomenon where..." │   │
│  │  Rejected: "Let me think... It's really complicated..." │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  DPO Loss:                                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  L = - log σ(                                           │   │
│  │        β * (log π(y_c|x) - log π(y_r|x))              │   │
│  │        - β * KL(π || π_ref)                             │   │
│  │      )                                                  │   │
│  │                                                          │   │
│  │  其中:                                                   │   │
│  │    y_c = chosen response (被选中的回复)                   │   │
│  │    y_r = rejected response (被拒绝的回复)                 │   │
│  │    π = 当前策略 (待优化模型)                               │   │
│  │    π_ref = 参考策略 (SFT 模型，冻结)                      │   │
│  │    β = KL 惩罚系数                                       │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. DPO vs RLHF

| 方面 | RLHF | DPO |
|------|------|-----|
| 训练阶段 | 2 阶段 (RM + PPO) | 1 阶段 |
| 训练复杂度 | 高 | 低 |
| 显存需求 | 高 (PPO 需要 critic) | 中等 |
| 稳定性 | 中等 | 好 |
| 样本效率 | 低 | 高 |
| 效果 | 最好 | 略逊但接近 |

### 2. DPO 关键洞察

```
RLHF 需要单独训练 Reward Model 的原因:
- Reward Model 需要从人类偏好中学习
- 然后 PPO 用 Reward Model 提供的信号优化策略

DPO 的关键洞察:
- Reward 可以用策略概率隐式表示
- 不需要显式训练 Reward Model
- 直接用对比损失优化策略
```

### 3. DPO 超参数

```python
dpo_config = {
    "beta": 0.1,           # KL 惩罚系数，越大越保守
    "learning_rate": 1e-6,
    "num_epochs": 3,
    "batch_size": 8,
    "gradient_accumulation_steps": 4,
    "max_seq_length": 2048,
}
```

## 💻 完整实现

### DPO 训练实现

```python
import torch
import torch.nn as nn
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PreferenceDataset:
    """偏好数据集"""
    prompt: str
    chosen: str
    rejected: str


class DPOTrainer:
    """DPO 训练器"""
    
    def __init__(
        self,
        model,
        ref_model,
        beta: float = 0.1,
        learning_rate: float = 1e-6,
    ):
        self.model = model
        self.ref_model = ref_model
        self.beta = beta
        
        # 冻结参考模型
        for param in self.ref_model.parameters():
            param.requires_grad = False
        
        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=learning_rate,
        )
    
    def compute_log_probs(
        self,
        model,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        label_ids: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """计算 log probabilities"""
        
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )
        
        logits = outputs.logits  # [batch, seq_len, vocab_size]
        
        # 计算 log probabilities
        log_probs = F.log_softmax(logits, dim=-1)
        
        if label_ids is not None:
            # 只取 label 位置的 log prob
            label_log_probs = log_probs.gather(-1, label_ids.unsqueeze(-1)).squeeze(-1)
            # Mask padding
            mask = (label_ids != -100).float()
            label_log_probs = (label_log_probs * mask).sum(-1) / mask.sum(-1)
        
        return log_probs, label_log_probs
    
    def dpo_loss(
        self,
        chosen_log_probs: torch.Tensor,
        rejected_log_probs: torch.Tensor,
        ref_chosen_log_probs: torch.Tensor,
        ref_rejected_log_probs: torch.Tensor,
    ) -> torch.Tensor:
        """
        计算 DPO 损失
        
        L = - log σ( β * (log π(y_c|x) - log π(y_r|x)
                          - log π_ref(y_c|x) + log π_ref(y_r|x) ) )
        
        = - log σ( β * (Δlogπ - Δlogπ_ref) )
        """
        
        # 策略的概率差
        policy_logratios = chosen_log_probs - rejected_log_probs
        
        # 参考模型的概率差
        ref_logratios = ref_chosen_log_probs - ref_rejected_log_probs
        
        # DPO 损失
        logits = self.beta * (policy_logratios - ref_logratios)
        loss = -F.logsigmoid(logits).mean()
        
        return loss
    
    def step(self, batch: List[PreferenceDataset]):
        """一步训练"""
        
        # Tokenize
        chosen_encodings = self.tokenize(batch, 'chosen')
        rejected_encodings = self.tokenize(batch, 'rejected')
        
        # 计算策略的 log probs
        chosen_log_probs = self.compute_policy_log_probs(chosen_encodings)
        rejected_log_probs = self.compute_policy_log_probs(rejected_encodings)
        
        # 计算参考模型的 log probs
        with torch.no_grad():
            ref_chosen_log_probs = self.compute_ref_log_probs(chosen_encodings)
            ref_rejected_log_probs = self.compute_ref_log_probs(rejected_encodings)
        
        # 计算损失
        loss = self.dpo_loss(
            chosen_log_probs,
            rejected_log_probs,
            ref_chosen_log_probs,
            ref_rejected_log_probs,
        )
        
        # 反向传播
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()


class DPODataset(torch.utils.data.Dataset):
    """DPO 数据集"""
    
    def __init__(self, data: List[PreferenceDataset], tokenizer):
        self.data = data
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        return PreferenceDataset(
            prompt=item.prompt,
            chosen=item.chosen,
            rejected=item.rejected,
        )
```

### 使用 TRL 库

```python
from trl import DPOTrainer, DPOConfig
from datasets import load_dataset

# 加载数据
dataset = load_dataset("your-preference-dataset", split="train")

# DPO 配置
dpo_config = DPOConfig(
    output_dir="./dpo_output",
    beta=0.1,
    learning_rate=1e-6,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    max_seq_length=2048,
    warmup_ratio=0.1,
)

# 初始化 trainer
dpo_trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=dpo_config,
    train_dataset=dataset,
    processing_class=tokenizer,
)

# 训练
dpo_trainer.train()

# 保存
dpo_trainer.save_model()
```

### 偏好数据格式

```json
// preference_data.jsonl
{"prompt": "What is quantum entanglement?", "chosen": "Quantum entanglement is...", "rejected": "That's a complex topic..."}
{"prompt": "Write a haiku about autumn:", "chosen": "Leaves fall to the ground...", "rejected": "Autumn is a season..."}
```

## 📊 DPO vs RLHF 效果对比

| 数据集 | RLHF | DPO | 差异 |
|--------|------|-----|------|
| HH-RLHF (Helpful) | 65% | 63% | -2% |
| HH-RLHF (Harmless) | 80% | 78% | -2% |
| Summarization | 52% | 51% | -1% |

## 📋 命令速查

```bash
# 安装 TRL
pip install trl

# 训练 DPO
python dpo/train.py \
    --model_path meta-llama/Llama-2-7b \
    --dataset_path ./preference_data.jsonl \
    --output_dir ./dpo_output \
    --beta 0.1

# 评估
python dpo/evaluate.py --model_path ./dpo_output
```

## 📚 学习要点

1. **单阶段训练**：DPO 不需要单独的 Reward Model
2. **KL 惩罚**：通过 β 控制与参考模型的偏离程度
3. **数据质量**：偏好数据的质量直接影响效果
4. **比 RLHF 稳定**：不需要 PPO 的超参数调优

## 🔗 相关案例

- `rlhf-introduction` - RLHF 详解
- `lora-fine-tuning` - LoRA 微调
- `sft-fundamentals` - SFT 基础
- `orpo-training` - ORPO 对比优化
