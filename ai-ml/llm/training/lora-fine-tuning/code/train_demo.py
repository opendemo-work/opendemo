"""
LoRA 微调简化演示。

使用一个极小的 MLP 模拟语言模型中的某一层，
展示如何用 LoRA 只训练少量参数来拟合新任务。
"""

import torch
import torch.nn as nn
import torch.optim as optim

from lora_layer import LoRALinear


class TinyModel(nn.Module):
    """一个微型模型，用于演示 LoRA 微调。"""

    def __init__(self, dim: int = 64, hidden: int = 128):
        super().__init__()
        self.fc1 = nn.Linear(dim, hidden)
        self.fc2 = nn.Linear(hidden, dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc2(torch.relu(self.fc1(x)))


def freeze_base_params(model: nn.Module) -> None:
    """冻结模型中所有原始参数。"""
    for param in model.parameters():
        param.requires_grad = False


def replace_with_lora(model: nn.Module, rank: int = 4, alpha: int = 8) -> None:
    """将模型中的 nn.Linear 替换为 LoRALinear。"""
    for name, module in model.named_children():
        if isinstance(module, nn.Linear):
            lora_module = LoRALinear(
                in_features=module.in_features,
                out_features=module.out_features,
                rank=rank,
                alpha=alpha,
                bias=module.bias is not None,
            )
            lora_module.weight.data = module.weight.data.clone()
            if module.bias is not None:
                lora_module.bias.data = module.bias.data.clone()
            setattr(model, name, lora_module)
        else:
            replace_with_lora(module, rank, alpha)


def count_trainable_params(model: nn.Module) -> int:
    """统计可训练参数数量。"""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def main():
    print("=== LoRA 微调演示 ===")

    # 1. 创建预训练模型并模拟一个下游任务
    dim = 64
    model = TinyModel(dim=dim, hidden=128)

    # 目标函数：输入 x，期望输出为 2*x
    torch.manual_seed(42)
    x = torch.randn(200, dim)
    y = 2 * x

    # 2. 在全部参数上快速预训练（模拟已有预训练权重）
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    print("预训练模型...")
    for epoch in range(100):
        optimizer.zero_grad()
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()
        optimizer.step()
    print(f"预训练后 Loss: {loss.item():.6f}")

    # 3. 应用 LoRA：冻结原始参数，只训练 LoRA 增量
    replace_with_lora(model, rank=4, alpha=8)
    freeze_base_params(model)

    trainable = count_trainable_params(model)
    total = sum(p.numel() for p in model.parameters())
    print(f"可训练参数: {trainable} / {total} ({trainable / total * 100:.2f}%)")

    # 4. 使用 LoRA 在新任务上微调（这里继续拟合 2*x，但只更新 LoRA）
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3)
    print("LoRA 微调...")
    for epoch in range(50):
        optimizer.zero_grad()
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()
        optimizer.step()
    print(f"微调后 Loss: {loss.item():.6f}")

    # 5. 合并权重并验证
    with torch.no_grad():
        test_x = torch.randn(10, dim)
        test_y = 2 * test_x
        pred = model(test_x)
        test_loss = criterion(pred, test_y)
        print(f"测试 Loss: {test_loss.item():.6f}")

    print("✅ LoRA 微调演示完成")


if __name__ == "__main__":
    main()
