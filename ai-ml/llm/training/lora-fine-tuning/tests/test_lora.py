import sys
from pathlib import Path

import torch

# 将 code 目录加入路径
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from lora_layer import LoRALinear, apply_lora_to_linear


def test_lora_forward_shape():
    layer = LoRALinear(in_features=16, out_features=32, rank=4, alpha=8)
    x = torch.randn(8, 16)
    y = layer(x)
    assert y.shape == (8, 32), f"期望输出形状 (8, 32)，实际 {y.shape}"


def test_lora_initial_delta_is_zero():
    """初始化时 B 为零矩阵，因此 LoRA 增量应为 0。"""
    layer = LoRALinear(in_features=16, out_features=32, rank=4, alpha=8)
    x = torch.zeros(4, 16)
    # 原始输出
    base = torch.nn.functional.linear(x, layer.weight, layer.bias)
    # 带 LoRA 的输出
    out = layer(x)
    assert torch.allclose(base, out, atol=1e-6), "初始化时 LoRA 增量应为零"


def test_lora_trainable_only_lora_params():
    layer = LoRALinear(in_features=16, out_features=32, rank=4, alpha=8)
    trainable = [name for name, p in layer.named_parameters() if p.requires_grad]
    assert "lora_A" in trainable
    assert "lora_B" in trainable
    assert "weight" not in trainable
    assert "bias" not in trainable


def test_apply_lora_to_linear():
    original = torch.nn.Linear(16, 32)
    lora = apply_lora_to_linear(original, rank=4, alpha=8)
    assert isinstance(lora, LoRALinear)
    assert lora.in_features == 16
    assert lora.out_features == 32


def test_count_parameters():
    layer = LoRALinear(in_features=16, out_features=32, rank=4, alpha=8)
    stats = layer.count_parameters()
    expected_base = 16 * 32 + 32
    expected_lora = 4 * 16 + 32 * 4
    assert stats["base_params"] == expected_base
    assert stats["lora_params"] == expected_lora
