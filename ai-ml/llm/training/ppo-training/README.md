<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# PPO 强化学习训练

> 本案例详解 PPO (Proximal Policy Optimization) 算法原理，演示如何用 RLHF 对齐大模型

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    PPO 训练流程                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐
│  │                    PPO Algorithm                             │ │
│  │                                                             │ │
│  │   Rollout Phase:                                            │ │
│  │   ┌──────────────────────────────────────────────────────┐   │ │
│  │   │  Policy π_old (actor)                               │   │ │
│  │   │    │                                                 │   │ │
│  │   │    ▼                                                 │   │ │
│  │   │  生成 (prompt, response, log_probs, values)           │   │ │
│  │   │    │                                                 │   │ │
│  │   │    ▼                                                 │   │ │
│  │   │  Reward 计算: r = RewardModel(prompt, response)      │   │ │
│  │   │    │                                                 │   │ │
│  │   │    ▼                                                 │   │ │
│  │   │  Advantage 计算: A(s,a) = Q(s,a) - V(s)              │   │ │
│  │   └──────────────────────────────────────────────────────┘   │ │
│  │                           │                                   │ │
│  │                           ▼                                   │ │
│  │   Update Phase:                                            │ │
│  │   ┌──────────────────────────────────────────────────────┐   │ │
│  │   │  for epoch in range(ppo_epochs):                     │   │ │
│  │   │    ratio = π_new(a|s) / π_old(a|s)                   │   │ │
│  │   │    clipped_ratio = clip(ratio, 1-ε, 1+ε)             │   │ │
│  │   │    L = min(ratio * A, clipped_ratio * A)             │   │ │
│  │   │    更新 Actor 和 Critic                               │   │ │
│  │   └──────────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
│  KL Penalty (PPO-Penalty):                                      │
│  ┌─────────────────────────────────────────────────────────────┐
│  │  L_total = L_PPO - β * KL(π_new || π_ref)                   │ │
│  │                                                             │ │
│  │  β 动态调整:                                                │ │
│  │  - KL > target → 减小 β (减少约束)                          │ │
│  │  - KL < target → 增大 β (加强约束)                          │ │
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
│  价值函数更新:                                                   │
│  ┌─────────────────────────────────────────────────────────────┐
│  │  V_target = r + γ * r + ... + γ^T * V(s_T)                  │ │
│  │  L_critic = MSE(V(s), V_target)                             │ │
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心概念

### 1. PPO 核心公式

```python
def ppo_loss(old_log_probs, new_log_probs, advantages, clip_eps=0.2):
    """
    PPO-Clip 损失函数
    
    L = min(ratio * advantages, clipped_ratio * advantages)
    其中 ratio = π_new(a|s) / π_old(a|s)
    """
    ratio = torch.exp(new_log_probs - old_log_probs)
    
    # 未裁剪的目标
    unclipped = ratio * advantages
    
    # 裁剪后的目标
    clipped = torch.clamp(ratio, 1 - clip_eps, 1 + clip_eps) * advantages
    
    # 取较小值 (pessimistic bound)
    return -torch.min(unclipped, clipped).mean()
```

### 2. Reward 与 KL 散度

```python
def compute_rewards(log_probs, ref_log_probs, reward_scores, kl_coef=0.1):
    """
    计算带 KL 惩罚的奖励
    
    R_final = r_reward - β * KL(π || π_ref)
    """
    # KL 散度 (π_new - π_ref 的对数概率差)
    kl = log_probs - ref_log_probs
    
    # 加上 reward
    rewards = reward_scores - kl_coef * kl
    
    return rewards
```

### 3. 完整训练实现

```python
import torch
import torch.nn.functional as F
from trl import PPOTrainer, PPOConfig

def train_ppo():
    """PPO 训练"""
    config = PPOConfig(
        model_name="meta-llama/Llama-2-7b",
        learning_rate=1.4e-5,
        ppo_epochs=4,
        mini_batch_size=1,
        batch_size=8,
        gradient_accumulation_steps=1,
        kl_penalty="kl",
        target_kl=0.1,
    )
    
    # 初始化
    ppo_trainer = PPOTrainer(config)
    
    # 生成器模型 (待对齐)
    model = AutoModelForCausalLM.from_pretrained(config.model_name)
    ref_model = AutoModelForCausalLM.from_pretrained(config.model_name)
    
    # Reward Model
    reward_model = RewardModel(config.model_name)
    reward_model.load_state_dict(torch.load("reward_model.pt"))
    reward_model.eval()
    
    for step in range(num_steps):
        # Rollout: 生成响应
        query_tensors = [get_query_prompt() for _ in range(config.batch_size)]
        response_tensors = []
        
        for query in query_tensors:
            with torch.no_grad():
                response = model.generate(
                    query,
                    max_new_tokens=128,
                    do_sample=True,
                    temperature=0.9
                )
            response_tensors.append(response)
        
        # 计算奖励
        rewards = []
        for query, response in zip(query_tensors, response_tensors):
            with torch.no_grad():
                reward = reward_model(query, response)
            rewards.append(reward)
        
        # PPO 更新
        stats = ppo_trainer.step(query_tensors, response_tensors, rewards)
        
        # 记录
        logger.log_stats(stats, rewards=rewards)
    
    return model
```

## PPO vs 其他算法

| 特性 | PPO | DPO | GRPO |
|------|-----|-----|------|
| 采样需求 | 高 | 低 | 中 |
| 训练稳定性 | 中 | 高 | 高 |
| 效果 | 最好 | 接近PPO | 接近PPO |
| 计算成本 | 高 | 低 | 中 |

## 命令速查

```bash
# 使用 TRL 库训练
python -m trl.trainer.ppo_trainer \
    --model_name meta-llama/Llama-2-7b \
    --reward_model_path ./reward_model \
    --dataset Anthropic/hh-rlhf

# DeepSpeed-Chat PPO
deepspeed --num_gpus=8 train_ppo.py \
    --policy_model meta-llama/Llama-2-7b \
    --reward_model_path ./reward_model
```

## 学习要点

1. **PPO-Clip**：用裁剪限制策略更新幅度
2. **Reward Model**：提供学习信号
3. **KL Penalty**：防止策略偏离 SFT 模型太远
4. **价值函数**：估计未来累积奖励

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

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

```bash
python code/main.py
```
