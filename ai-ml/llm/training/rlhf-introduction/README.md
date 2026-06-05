# RLHF 人类反馈强化学习

> 本案例详解 RLHF (Reinforcement Learning from Human Feedback) 原理与实现

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        RLHF 三阶段流程                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stage 1: 预训练 (Pre-training)                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │   Corpus ──▶ [LLM Pretraining] ──▶ Pretrained LLM       │   │
│  │                                                          │   │
│  │   目标: 学习语言模型,掌握基础知识                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Stage 2: 监督微调 (SFT)                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │   Demonstrations ──▶ [Fine-tune with Supervision] ──▶ SFT LLM  │   │
│  │                                                          │   │
│  │   目标: 学习遵循指令                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Stage 3: RLHF                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │   ┌─────────────┐    ┌─────────────┐    ┌───────────┐ │   │
│  │   │ Reward Model │◀───│ Human      │───▶│ Comparisons│ │   │
│  │   │  Training   │    │ Feedback   │    │            │ │   │
│  │   └──────┬──────┘    └─────────────┘    └───────────┘ │   │
│  │          │                                              │   │
│  │          ▼                                              │   │
│  │   ┌──────────────────────────────────────────────┐    │   │
│  │   │         PPO Optimization                       │    │   │
│  │   │                                              │    │   │
│  │   │   π_θ (SFT) ──▶ π_θ RL (Final Model)        │    │   │
│  │   │        ▲                                      │    │   │
│  │   │        │                                      │    │   │
│  │   │        └─── (PPO Gradient Update)              │    │   │
│  │   │                                              │    │   │
│  │   └──────────────────────────────────────────────┘    │   │
│  │              │                                        │   │
│  │              ▼                                        │   │
│  │         Aligned LLM                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

奖励模型训练:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Prompt 1: "How to make a bomb?"                                │
│      │                                                          │
│      ├── Response A: "Here's how to..."  (好, +)                │
│      └── Response B: "I can't help with that." (更好, ++)       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Reward Model                            │   │
│  │                                                          │   │
│  │   r_θ(Prompt, Response) → Reward Score                  │   │
│  │                                                          │   │
│  │   Loss = -log(σ(r_θ(A) - r_θ(B)))                       │   │
│  │          (对比排序损失)                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. RLHF 解决的问题

| 问题 | 预训练 | SFT | +RLHF |
|------|--------|-----|-------|
| 遵循指令 | ❌ | ✅ | ✅ |
| 有害内容 | ❌ | ❌ | ✅ |
| 真实性 | ❌ | ❌ | ✅ |
| 帮助性 | ⚠️ | ⚠️ | ✅ |

### 2. 三个阶段详解

```
1. Pretraining → 基座模型 (语言能力)
2. SFT → 学会遵循指令 (但可能有害/不真实)
3. RLHF → 对齐人类价值观 (安全+有用)
```

### 3. PPO 算法核心

```python
# PPO 目标函数
def ppo_objective(π_θ, π_θ_old, s, a, r, γ=1.0, clip=0.2):
    """
    π_θ: 当前策略
    π_θ_old: 旧策略
    s, a: 状态动作
    r: 奖励
    γ: 折扣因子
    clip: PPO 剪辑范围
    """
    
    # 重要性采样比率
    ratio = π_θ(a|s) / π_θ_old(a|s)
    
    # Clipped 目标
    clipped_ratio = torch.clamp(ratio, 1 - clip, 1 + clip)
    
    # 原始目标
    surr1 = ratio * r
    
    # Clipped 目标
    surr2 = clipped_ratio * r
    
    # 取较小值
    ppo_loss = -min(surr1, surr2)
    
    return ppo_loss.mean()
```

## 💻 完整实现

### 奖励模型

```python
import torch
import torch.nn as nn
from transformers import AutoModel, AutoConfig

class RewardModel(nn.Module):
    """奖励模型 - 预测人类偏好"""
    
    def __init__(self, base_model_name: str, reward_scale: float = 1.0):
        super().__init__()
        
        self.base_model = AutoModel.from_pretrained(
            base_model_name,
            config=AutoConfig.from_pretrained(base_model_name)
        )
        self.reward_scale = reward_scale
        
        # 奖励头
        hidden_size = self.base_model.config.hidden_size
        self.reward_head = nn.Linear(hidden_size, 1, bias=False)
        
        # 初始化
        self.reward_head.weight.data.normal_(mean=0.0, std=1.0 / hidden_size)
        
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor
    ) -> torch.Tensor:
        """
        返回奖励分数
        """
        outputs = self.base_model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        # 使用最后一个 token 的 hidden state
        last_hidden_state = outputs.last_hidden_state
        last_token_hidden = last_hidden_state[:, -1, :]
        
        reward = self.reward_head(last_token_hidden).squeeze(-1)
        
        return reward * self.reward_scale


def reward_model_loss(
    reward_model: RewardModel,
    chosen_ids: torch.Tensor,
    chosen_mask: torch.Tensor,
    rejected_ids: torch.Tensor,
    rejected_mask: torch.Tensor
) -> torch.Tensor:
    """
    奖励模型对比损失
    
    chosen_ids: 被选中的回复 token ids
    rejected_ids: 被拒绝的回复 token ids
    """
    
    chosen_reward = reward_model(chosen_ids, chosen_mask)
    rejected_reward = reward_model(rejected_ids, rejected_mask)
    
    # Bradley-Terry 模型
    # P(preferred) = σ(r_chosen - r_rejected)
    # Loss = -log(σ(r_chosen - r_rejected))
    loss = -nn.functional.logsigmoid(chosen_reward - rejected_reward).mean()
    
    return loss
```

### PPO 训练

```python
class PPOTrainer:
    """PPO 训练器"""
    
    def __init__(
        self,
        policy_model,       # SFT 模型
        ref_model,          # Reference 模型 (冻结的 SFT)
        reward_model,       # 奖励模型
        tokenizer,
        config: dict = None
    ):
        self.policy = policy_model
        self.ref = ref_model
        self.reward = reward_model
        self.tokenizer = tokenizer
        
        # 默认配置
        self.config = config or {
            "ppo_epochs": 4,
            "mini_batch_size": 4,
            "learning_rate": 1e-5,
            "clip_range": 0.2,
            "value_loss_coef": 0.1,
            "gamma": 1.0,
            "lam": 0.95,
            "kl_coef": 0.02,  # KL 散度惩罚系数
        }
        
    def step(self, queries: list, responses: list, rewards: list):
        """
        执行一步 PPO 更新
        """
        # 1. 构建输入
        query_tensors = [self.tokenizer(q, return_tensors="pt") for q in queries]
        response_tensors = [self.tokenizer(r, return_tensors="pt") for r in responses]
        
        # 2. 计算旧策略的 log probs
        with torch.no_grad():
            old_log_probs = self._get_log_probs(self.policy, query_tensors, response_tensors)
            ref_log_probs = self._get_log_probs(self.ref, query_tensors, response_tensors)
            
        # 3. PPO 更新
        for _ in range(self.config["ppo_epochs"]):
            # 计算新的 log probs 和 values
            log_probs, values = self._get_log_probs_and_values(
                self.policy, query_tensors, response_tensors
            )
            
            # 计算 advantages
            advantages = self._compute_advantages(rewards, values)
            
            # 计算 PPO 损失
            ppo_loss = self._compute_ppo_loss(
                log_probs, old_log_probs, advantages
            )
            
            # KL 惩罚
            kl_penalty = self._compute_kl_penalty(log_probs, ref_log_probs)
            
            # 价值损失
            value_loss = self._compute_value_loss(values, rewards)
            
            # 总损失
            total_loss = (
                ppo_loss 
                + self.config["kl_coef"] * kl_penalty
                + self.config["value_loss_coef"] * value_loss
            )
            
            # 更新策略
            self.policy.optimizer.zero_grad()
            total_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 1.0)
            self.policy.optimizer.step()
            
    def _get_log_probs(self, model, query_tensors, response_tensors):
        """获取 log probs"""
        # 实现省略...
        pass
        
    def _compute_ppo_loss(self, log_probs, old_log_probs, advantages, clip=0.2):
        """计算 PPO 损失"""
        ratio = torch.exp(log_probs - old_log_probs)
        
        clipped_ratio = torch.clamp(ratio, 1 - clip, 1 + clip)
        
        surr1 = ratio * advantages
        surr2 = clipped_ratio * advantages
        
        return -torch.min(surr1, surr2).mean()
        
    def _compute_kl_penalty(self, log_probs, ref_log_probs):
        """计算 KL 惩罚"""
        # KL(π || π_ref) = π * log(π / π_ref) = π * (log π - log π_ref)
        return (log_probs - ref_log_probs).mean()
```

### 使用 TRL 库

```python
from trl import PPOTrainer, PPOTrainingArguments
from trl.models import AutoModelForCausalLMWithValueHead
from transformers import AutoTokenizer

# 加载模型
model = AutoModelForCausalLMWithValueHead.from_pretrained("your-sft-model")
ref_model = AutoModelForCausalLMWithValueHead.from_pretrained("your-sft-model")
tokenizer = AutoTokenizer.from_pretrained("your-sft-model")

# PPO 配置
training_args = PPOTrainingArguments(
    output_dir="./rlhf_output",
    learning_rate=1e-5,
    ppo_epochs=4,
    mini_batch_size=4,
    batch_size=16,
    gradient_accumulation_steps=1,
)

# PPO 训练器
ppo_trainer = PPOTrainer(
    args=training_args,
    model=model,
    ref_model=ref_model,
    tokenizer=tokenizer,
)

# 训练
for epoch in range(num_epochs):
    for batch in dataloader:
        # 生成 response
        query_tensors = [tokenize(q) for q in batch["queries"]]
        response_tensors = ppo_trainer.generate(query_tensors)
        
        # 计算奖励
        rewards = reward_model(query_tensors, response_tensors)
        
        # PPO 更新
        ppo_trainer.step(query_tensors, response_tensors, rewards)
```

## 📊 RLHF vs 其他对齐方法

| 方法 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| **RLHF** | PPO + 人类偏好 | 效果最好 | 复杂,不稳定 |
| **DPO** | 直接优化偏好 | 简单,稳定 | 效果略差 |
| **RLAIF** | AI 反馈替代人类 | 可扩展 | 质量依赖 AI |
| **Constitutional AI** | 原则驱动 | 可解释 | 需要设计原则 |

## 📋 命令速查

```bash
# 安装 TRL 库
pip install trl

# 训练 Reward Model
python reward_model/train.py --model your-sft-model

# PPO 训练
python ppo/train.py \
    --policy_model your-sft-model \
    --ref_model your-sft-model \
    --reward_model reward_model_checkpoint

# 使用 DPO (更简单)
python dpo/train.py --model your-sft-model --dataset preference_data
```

## 📚 学习要点

1. **RLHF 目的**：让模型输出符合人类价值观
2. **奖励模型关键**：人类偏好数据的质量和数量
3. **PPO 稳定性**：KL 惩罚防止策略崩溃
4. **替代方案**：DPO 更简单但效果略差

## 🔗 相关案例

- `dpo-training` - DPO 直接偏好优化
- `reward-model-training` - 奖励模型训练
- `ppo-training` - PPO 算法实现
- `lora-fine-tuning` - SFT 微调基础
