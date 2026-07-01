<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Mixture of Experts 混合专家

> 本案例详解 MoE (Mixture of Experts) 架构，理解其如何实现大模型的高效扩展

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Dense vs MoE 模型对比                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Dense Model (全部激活):                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │   Input                                                    │   │
│  │      │                                                     │   │
│  │      ▼                                                     │   │
│  │   [W_up] ──────────────────────────────────────────▶ FFN │   │
│  │   [W_gate] ──────────────────────────────────────▶ FFN     │   │
│  │   所有 FFN 专家全部激活                                   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  MoE Model (稀疏激活):                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │   Input                                                    │   │
│  │      │                                                     │   │
│  │      ▼                                                     │   │
│  │   ┌──────────────────────────────────────────────────┐   │   │
│  │   │  Router: Softmax(W_gates · x)                    │   │   │
│  │   │                    │                              │   │   │
│  │   │   ┌────┬────┬────┴────┬────┬────┐              │   │   │
│  │   │   │    │    │         │    │    │              │   │   │
│  │   │   ▼    ▼    ▼         ▼    ▼    ▼              │   │   │
│  │   │  Exp1 Exp2 Exp3 ... ExpN Exp4 Exp8             │   │   │
│  │   │  (top-2 激活)                                    │   │   │
│  │   └──────────────────────────────────────────────────┘   │   │
│  │                    │                                      │   │
│  │                    ▼                                      │   │
│  │              Output (加权求和)                            │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Mixtral 8x22B 架构:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Input: [batch, seq_len, hidden_dim]                           │
│                                                                 │
│       ┌─────────────────────────────────────────────────────┐   │
│       │                 Attention (共享)                      │   │
│       │                                                     │   │
│       │  ┌─────────────────────────────────────────────┐   │   │
│       │  │ Q_proj, K_proj, V_proj, O_proj (共享)       │   │   │
│       │  └─────────────────────────────────────────────┘   │   │
│       └─────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│       ┌─────────────────────────────────────────────────────┐   │
│       │                 MoE FFN Layer                        │   │
│       │                                                     │   │
│       │   Router ──▶ [Exp1] [Exp2] [Exp3] ... [Exp8]       │   │
│       │    (top-2)     (每个是独立的 FFN)                    │   │
│       │                                                     │   │
│       │   Output = Σ (gate_i * expert_i(x))                  │   │
│       │                                                     │   │
│       └─────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  重复 48 层...                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

专家负载均衡:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  问题: Router 可能总是选择相同的专家                              │
│                                                                 │
│  解决方案: Auxiliary Load Balancing Loss                          │
│                                                                 │
│  L_aux = α * Σ(f_i * P_i)                                      │
│                                                                 │
│  其中:                                                         │
│    f_i = 被选中的 token 中选择专家 i 的比例                       │
│    P_i = 专家 i 接收到的平均路由概率                              │
│    α = 0.01 (平衡系数)                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. MoE 核心思想

```
传统 Dense 模型:
- 每次前向所有参数都激活
- 计算量 ∝ 参数数量

MoE 模型:
- 每次只激活部分专家
- 计算量 ∝ 激活参数 + 路由开销
- 参数量可以很大，但计算量可控
```

### 2. 路由机制

```python
class MoELayer(nn.Module):
    def __init__(self, d_model, num_experts, top_k):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        
        # 路由器
        self.router = nn.Linear(d_model, num_experts)
        
        # 专家
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.GELU(),
                nn.Linear(d_ff, d_model),
            )
            for _ in range(num_experts)
        ])
    
    def forward(self, x):
        # x: [batch, seq_len, d_model]
        batch_size, seq_len, d_model = x.shape
        
        # 路由计算
        router_logits = self.router(x)  # [batch, seq_len, num_experts]
        router_probs = F.softmax(router_logits, dim=-1)
        
        # 选择 top-k 专家
        top_k_probs, top_k_indices = torch.topk(router_probs, self.top_k, dim=-1)
        
        # 归一化
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)
        
        # 专家计算
        output = torch.zeros_like(x)
        for k in range(self.top_k):
            expert_idx = top_k_indices[:, :, k]
            expert_prob = top_k_probs[:, :, k]
            
            for i in range(self.num_experts):
                mask = (expert_idx == i)
                if mask.any():
                    expert_input = x[mask]
                    expert_output = self.experts[i](expert_input)
                    output[mask] += expert_output * expert_prob[mask].unsqueeze(-1)
        
        return output
```

### 3. 主流 MoE 模型

| 模型 | 参数量 | 激活专家 | 特点 |
|------|--------|----------|------|
| Switch Transformer | 1.6T | 1/2048 | Switch 路由，只选 1 个 |
| GLaM | 1.2T | 2/64 | 双专家 |
| Mixtral 8x7B | 46.7B | 2/8 | 7B 专家 8 个 |
| DBRX | 132B | 4/16 | 16 个专家 |
| DeepSeek V2 | 236B | 2/128 | 128 个专家 |
| Grok-1 | 314B | 8/64 | 64 个专家 |

## 💻 完整实现

### MoE 层实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List

class Expert(nn.Module):
    """单个专家"""
    def __init__(self, d_model, d_ff, dropout=0.0):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )
    
    def forward(self, x):
        return self.net(x)


class MoELayer(nn.Module):
    """MoE 层"""
    def __init__(
        self,
        d_model: int,
        d_ff: int,
        num_experts: int,
        top_k: int = 2,
        dropout: float = 0.0,
    ):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        
        # 路由器
        self.router = nn.Linear(d_model, num_experts, bias=False)
        
        # 专家
        self.experts = nn.ModuleList([
            Expert(d_model, d_ff, dropout)
            for _ in range(num_experts)
        ])
        
        # 负载均衡损失系数
        self.alpha = 0.01
        
    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, dict]:
        """
        Returns:
            output: MoE 输出
            aux_loss: 辅助损失
        """
        batch_size, seq_len, d_model = x.shape
        
        # Reshape for batch processing
        x_flat = x.view(-1, d_model)  # [batch*seq_len, d_model]
        
        # 路由计算
        router_logits = self.router(x_flat)  # [batch*seq_len, num_experts]
        router_probs = F.softmax(router_logits, dim=-1)
        
        # 选择 top-k 专家
        top_k_probs, top_k_indices = torch.topk(router_probs, self.top_k, dim=-1)
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)
        
        # 计算辅助损失 (负载均衡)
        # f_i: 选择专家 i 的 token 比例
        # P_i: 专家 i 的平均路由概率
        gates = F.one_hot(top_k_indices[:, 0], num_classes=self.num_experts).float()
        f_i = gates.sum(0) / gates.sum()
        P_i = router_probs.mean(0)
        aux_loss = self.alpha * (self.num_experts ** 2) * (f_i * P_i).sum()
        
        # 专家计算
        output = torch.zeros_like(x_flat)
        for k in range(self.top_k):
            expert_idx = top_k_indices[:, k]
            expert_prob = top_k_probs[:, k]
            
            for i in range(self.num_experts):
                mask = (expert_idx == i)
                if mask.any():
                    expert_input = x_flat[mask]
                    expert_output = self.experts[i](expert_input)
                    # 加权累加
                    output[mask] += expert_output * expert_prob[mask].unsqueeze(-1)
        
        # 恢复形状
        output = output.view(batch_size, seq_len, d_model)
        
        return output, aux_loss


class MoETransformerLayer(nn.Module):
    """使用 MoE 的 Transformer 层"""
    def __init__(self, d_model, num_heads, d_ff, num_experts, top_k, dropout=0.0):
        super().__init__()
        
        # Self Attention
        self.attn = nn.MultiheadAttention(d_model, num_heads, dropout, batch_first=True)
        self.attn_norm = nn.LayerNorm(d_model)
        
        # MoE FFN
        self.moe = MoELayer(d_model, d_ff, num_experts, top_k, dropout)
        self.moe_norm = nn.LayerNorm(d_model)
        
    def forward(self, x, mask=None):
        # Self Attention + 残差
        attn_out, _ = self.attn(x, x, x, attn_mask=mask)
        x = self.attn_norm(x + attn_out)
        
        # MoE + 残差
        moe_out, aux_loss = self.moe(x)
        x = self.moe_norm(x + moe_out)
        
        return x, aux_loss
```

### DeepSeek MoE 优化

```python
class DeepSeekMoELayer(nn.Module):
    """
    DeepSeek V2 的 MoE 实现
    - Fine-grained Expert Splitting
    - Shared Expert Isolation
    """
    
    def __init__(
        self,
        d_model: int,
        d_ff: int,
        num_experts: int = 64,
        top_k: int = 8,
        num_shared_experts: int = 2,
    ):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.num_shared_experts = num_shared_experts
        
        # 共享专家 (始终激活)
        self.shared_experts = nn.ModuleList([
            Expert(d_model, d_ff)
            for _ in range(num_shared_experts)
        ])
        
        # 路由专家
        self.router = nn.Linear(d_model, num_experts, bias=False)
        self.experts = nn.ModuleList([
            Expert(d_model, d_ff)
            for _ in range(num_experts)
        ])
        
    def forward(self, x):
        # 共享专家输出 (始终激活)
        shared_output = sum(expert(x) for expert in self.shared_experts)
        
        # 路由专家
        router_logits = self.router(x)
        router_probs = F.softmax(router_logits, dim=-1)
        top_k_probs, top_k_indices = torch.topk(router_probs, self.top_k)
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)
        
        # 路由专家输出
        routed_output = torch.zeros_like(x)
        for k in range(self.top_k):
            expert_idx = top_k_indices[:, k]
            expert_prob = top_k_probs[:, k]
            
            for i in range(self.num_experts):
                mask = (expert_idx == i)
                if mask.any():
                    output = self.experts[i](x[mask])
                    routed_output[mask] += output * expert_prob[mask].unsqueeze(-1)
        
        return shared_output + routed_output
```

## 📊 MoE vs Dense 对比

| 模型 | 参数量 | 激活参数量 | 相对计算量 |
|------|--------|------------|------------|
| LLaMA 2 7B (Dense) | 7B | 7B | 1x |
| LLaMA 2 70B (Dense) | 70B | 70B | 10x |
| Mixtral 8x7B (MoE) | 46.7B | 12.9B | 1.8x |
| DeepSeek V2 (MoE) | 236B | 21B | 3x |

## 📋 命令速查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 加载 Mixtral
python -c "
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained('mistralai/Mixtral-8x7B-v0.1')
print(model)
"

# 评测 MoE 模型
lm_eval --model hf --model_args pretrained=mixtral --tasks mmlu,humaneval
```

## 📚 学习要点

1. **稀疏激活**：参数量大但计算量可控
2. **负载均衡**：防止 Router 总是选择相同专家
3. **共享专家**：DeepSeek 等加入共享专家提升效果
4. **通信开销**：分布式训练时专家间需要通信

## 🔗 相关案例

- `transformer-scratch` - Transformer 从零实现
- `llama-architecture` - LLaMA 架构
- `rotary-embedding` - RoPE 位置编码
- `distributed-training` - 分布式训练

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
