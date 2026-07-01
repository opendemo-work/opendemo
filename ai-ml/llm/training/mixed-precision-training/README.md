<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 混合精度训练

> 本案例详解混合精度训练原理，演示如何利用 FP16/BF16 加速大模型训练并节省显存

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    混合精度训练原理                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  训练流程:                                                       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐
│  │                      Forward Pass                           │ │
│  │                                                             │ │
│  │   FP32 Master Weights                                       │ │
│  │         │                                                   │ │
│  │         ▼ Cast to FP16                                      │ │
│  │   FP16 Forward (激活值缓存)                                  │ │
│  │         │                                                   │ │
│  │         ▼ Loss 计算                                         │ │
│  │   FP16 Loss                                                 │ │
│  └─────────────────────────────────────────────────────────────┘
│                              │
│                              ▼
│  ┌─────────────────────────────────────────────────────────────┐
│  │                      Backward Pass                          │ │
│  │                                                             │ │
│  │   FP16 Gradients                                            │ │
│  │         │                                                   │ │
│  │         ▼ Loss Scale                                       │ │
│  │   梯度放大 (防止下溢)                                         │ │
│  └─────────────────────────────────────────────────────────────┘
│                              │
│                              ▼
│  ┌─────────────────────────────────────────────────────────────┐
│  │                      Optimizer Step                         │ │
│  │                                                             │ │
│  │   FP16 → FP32 转换                                           │ │
│  │   FP32 Optimizer State (动量, 方差)                          │ │
│  │   FP32 Master Weights 更新                                   │ │
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
│  精度对比:                                                       │
│  ┌─────────────────────────────────────────────────────────────┐
│  │  FP32:  符号(1) + 指数(8) + 尾数(23) = 32 bits               │ │
│  │  FP16:  符号(1) + 指数(5) + 尾数(10) = 16 bits               │ │
│  │  BF16:  符号(1) + 指数(8) + 尾数(7) = 16 bits (更宽指数)      │ │
│  │                                                             │ │
│  │  BF16 vs FP16:                                              │ │
│  │  - BF16 指数位与 FP32 相同，避免溢出                         │ │
│  │  - BF16 尾数位更少，精度略低但足够稳定                        │ │
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心概念

### 1. 混合精度原理

混合精度使用 FP16/BF16 进行计算，FP32 存储优化器状态：

- Forward/Backward 使用 FP16/BF16 (加速)
- Optimizer State 使用 FP32 (稳定)
- Master Weights 保持 FP32 (精度)

### 2. Loss Scale

```python
class DynamicLossScaler:
    """动态损失缩放"""
    def __init__(self, init_scale=2**16, scale_factor=2.0, scale_window=1000):
        self.scale = init_scale
        self.scale_factor = scale_factor
        self.scale_window = scale_window
        self.iteration = 0
        self.unskipped_iterations = 0
    
    def scale_loss(self, loss):
        return loss * self.scale
    
    def update_scale(self, overflow):
        if overflow:
            self.scale /= self.scale_factor
            self.unskipped_iterations = 0
        else:
            self.unskipped_iterations += 1
        
        if self.unskipped_iterations >= self.scale_window:
            self.scale *= self.scale_factor
```

### 3. PyTorch 自动混合精度

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
model = model.cuda()

for batch in dataloader:
    optimizer.zero_grad()
    
    # 自动混合精度
    with autocast(dtype=torch.bfloat16):
        outputs = model(batch.cuda())
        loss = compute_loss(outputs, labels.cuda())
    
    # 缩放损失
    scaler.scale(loss).backward()
    
    # 梯度裁剪
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    
    # 更新
    scaler.step(optimizer)
    scaler.update()
```

## 完整训练脚本

```python
import torch
from torch.cuda.amp import autocast, GradScaler

def train_amp(model, dataloader, optimizer, num_epochs):
    """混合精度训练"""
    device = torch.device("cuda")
    scaler = GradScaler()
    model = model.to(device)
    model.train()
    
    for epoch in range(num_epochs):
        for batch_idx, (inputs, labels) in enumerate(dataloader):
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            
            # 前向传播使用 AMP
            with autocast(dtype=torch.bfloat16):
                outputs = model(inputs)
                loss = F.cross_entropy(outputs, labels)
            
            # 反向传播
            scaler.scale(loss).backward()
            
            # 梯度裁剪
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            # 参数更新
            scaler.step(optimizer)
            scaler.update()
            
            if batch_idx % 100 == 0:
                print(f"Loss: {loss.item():.4f}, Scale: {scaler.get_scale()}")
    
    return model
```

## BF16 vs FP16

| 特性 | FP16 | BF16 |
|------|------|------|
| 动态范围 | 5.96e-8 ~ 65504 | 6.10e-5 ~ 3.40e+38 |
| 精度 | 3-4 位十进制 | 2-3 位十进制 |
| 溢出风险 | 容易 | 几乎不会 |
| 训练稳定性 | 需 Loss Scale | 无需 Loss Scale |

## 命令速查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# PyTorch AMP
python train.py --use_amp --amp_dtype bf16

# NVIDIA Apex
python train.py --fp16 --loss_scale dynamic

# DeepSpeed
deepspeed train.py --deepspeed_config ds_config_fp16.json
```

## 学习要点

1. **精度选择**：BF16 更稳定，FP16 更快
2. **Loss Scale**：防止梯度下溢
3. **混合精度**：计算用低精度，存储用高精度
4. **动态损失缩放**：自动调整缩放因子

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
