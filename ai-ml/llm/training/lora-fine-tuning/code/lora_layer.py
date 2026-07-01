"""
简化版 LoRA (Low-Rank Adaptation) 层实现。

不依赖 transformers 或 peft 库，仅使用 PyTorch 标准 API，
便于理解 LoRA 的核心数学：W' = W + (B @ A) * (alpha / rank)。
"""

import math
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


class LoRALinear(nn.Module):
    """
    将普通 nn.Linear 替换为支持 LoRA 的线性层。

    Args:
        in_features: 输入维度
        out_features: 输出维度
        rank: 低秩维度 r
        alpha: 缩放因子
        dropout: LoRA 路径上的 dropout 概率
        bias: 是否使用偏置
    """

    def __init__(
        self,
        in_features: int,
        out_features: int,
        rank: int = 8,
        alpha: int = 16,
        dropout: float = 0.0,
        bias: bool = True,
    ):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.alpha = alpha
        self.scaling = alpha / rank

        # 原始权重（冻结）
        self.weight = nn.Parameter(torch.empty(out_features, in_features), requires_grad=False)
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))

        if bias:
            self.bias = nn.Parameter(torch.zeros(out_features))
        else:
            self.register_parameter("bias", None)

        # LoRA 可训练参数
        self.lora_A = nn.Parameter(torch.randn(rank, in_features) * 0.01)
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
        self.lora_dropout = nn.Dropout(p=dropout) if dropout > 0 else nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 原始路径
        base_output = F.linear(x, self.weight, self.bias)

        # LoRA 路径: x @ A^T @ B^T
        lora_output = (
            self.lora_dropout(x) @ self.lora_A.T @ self.lora_B.T
        ) * self.scaling

        return base_output + lora_output

    def merge_weights(self) -> torch.Tensor:
        """将 LoRA 增量合并到原始权重中，返回合并后的权重。"""
        delta_W = (self.lora_B @ self.lora_A) * self.scaling
        return self.weight + delta_W

    def count_parameters(self) -> dict:
        """统计原始参数与 LoRA 新增参数数量。"""
        base_params = self.weight.numel() + (self.bias.numel() if self.bias is not None else 0)
        lora_params = self.lora_A.numel() + self.lora_B.numel()
        return {
            "base_params": base_params,
            "lora_params": lora_params,
            "lora_ratio": lora_params / base_params,
        }


def apply_lora_to_linear(
    linear: nn.Linear, rank: int = 8, alpha: int = 16, dropout: float = 0.0
) -> LoRALinear:
    """将现有的 nn.Linear 替换为等价的 LoRALinear。"""
    lora = LoRALinear(
        in_features=linear.in_features,
        out_features=linear.out_features,
        rank=rank,
        alpha=alpha,
        dropout=dropout,
        bias=linear.bias is not None,
    )
    lora.weight.data = linear.weight.data.clone()
    if linear.bias is not None:
        lora.bias.data = linear.bias.data.clone()
    return lora
