# 梯度检查点

> 本案例详解梯度检查点 (Gradient Checkpointing) 原理，演示如何用时间换空间训练超大模型

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    梯度检查点原理                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  标准 Forward (时间换空间):                                      │
│                                                                 │
│  Input → Layer1 → Layer2 → Layer3 → Layer4 → Output            │
│    │       │       │       │       │                           │
│    │       │       │       │       └── [激活值全部保存]          │
│    │       │       │       └── [激活值全部保存]                  │
│    │       │       └── [激活值全部保存]                          │
│    │       └── [激活值全部保存]                                  │
│    └── [激活值全部保存]                                          │
│                                                                 │
│  内存: O(N) - 所有激活值常驻显存                                  │
│                                                                 │
│  Gradient Checkpointing (空间换时间):                            │
│                                                                 │
│  Input → Layer1 → [ckpt] → Layer2 → [ckpt] → Layer3 → [ckpt]    │
│    │                            │                            │
│    │                            └─→ Recompute:                │
│    │                                 Layer1 → Layer2            │
│    │                                 (反向时重新计算)            │
│    │                                                         │
│    └── [激活值保存] ──→ Backward:                               │
│                              Layer3 → Recompute Layer2 → Layer1 │
│                                                                 │
│  内存: O(√N) - 只保存部分检查点                                  │
│                                                                 │
│  7B 模型对比:                                                    │
│  ┌─────────────────────────────────────────────────────────────┐
│  │ 标准训练: ~28GB 激活值 (30层)                                │ │
│  │ Checkpointing: ~4GB 激活值 (6个检查点)                       │ │
│  │ 内存节省: ~85%                                               │ │
│  │ 时间增加: ~20-30%                                            │ │
│  └─────────────────────────────────────────────────────────────┘
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心概念

### 1. 梯度检查点原理

梯度检查点通过在反向传播时重新计算激活值来节省显存：

- Forward 时只保存部分检查点
- Backward 时从检查点重新计算中间激活值
- 用 20-30% 的计算时间换 50-80% 的显存

### 2. PyTorch 实现

```python
from torch.utils.checkpoint import checkpoint, checkpoint_sequential
import torch.nn as nn

# 方法1: 使用 checkpoint 包装层
class ModelWithCheckpoint(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(4096, 4096)
        self.layer2 = nn.Linear(4096, 4096)
        self.layer3 = nn.Linear(4096, 4096)
    
    def forward(self, x):
        # checkpoint 会释放中间激活值，需要时重新计算
        x = checkpoint(self.layer1, x)
        x = checkpoint(self.layer2, x)
        x = checkpoint(self.layer3, x)
        return x

# 方法2: 使用 checkpoint_sequential
def forward_with_checkpoint(model, input):
    # 将模型分成多个段，每段用 checkpoint 包裹
    modules = [model.layer1, model.layer2, model.layer3, model.layer4]
    return checkpoint_sequential(modules, 2, input)  # 每2层一个检查点
```

### 3. 完整训练脚本

```python
from torch.utils.checkpoint import checkpoint
import torch.nn.functional as F

class TransformerBlock(nn.Module):
    def __init__(self, hidden_size, num_heads):
        super().__init__()
        self.attention = nn.MultiheadAttention(hidden_size, num_heads)
        self.mlp = nn.Sequential(
            nn.Linear(hidden_size, hidden_size * 4),
            nn.GELU(),
            nn.Linear(hidden_size * 4, hidden_size)
        )
        self.norm1 = nn.LayerNorm(hidden_size)
        self.norm2 = nn.LayerNorm(hidden_size)
    
    def forward(self, x):
        # 自注意力 + 残差
        attn_out, _ = self.attention(x, x, x)
        x = self.norm1(x + attn_out)
        
        # MLP + 残差
        mlp_out = self.mlp(x)
        x = self.norm2(x + mlp_out)
        
        return x

class LMWithCheckpoint(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers, num_heads):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.blocks = nn.ModuleList([
            TransformerBlock(hidden_size, num_heads) 
            for _ in range(num_layers)
        ])
        self.lm_head = nn.Linear(hidden_size, vocab_size)
    
    def forward(self, input_ids):
        x = self.embedding(input_ids)
        
        # 使用 checkpoint 包裹 Transformer 块
        for block in self.blocks:
            x = checkpoint(block, x, use_reentrant=True)
        
        return self.lm_head(x)

def train_with_checkpoint():
    model = LMWithCheckpoint(vocab_size=32000, hidden_size=4096, 
                            num_layers=32, num_heads=32)
    model = model.cuda()
    
    # 训练
    for batch in dataloader:
        outputs = model(batch.cuda())
        loss = F.cross_entropy(outputs.view(-1, vocab_size), 
                               batch.labels.cuda())
        loss.backward()
        optimizer.step()
```

## 命令速查

```bash
# PyTorch 原生 checkpoint
python train.py --use_checkpoint --checkpoint_ratio 2

# FasterTransformer checkpoint
python train.py --gradient_checkpointing

# DeepSpeed activation checkpointing
deepspeed train.py --deepspeed_config ds_config.json
```

## 学习要点

1. **时间换空间**：用额外计算换取更低显存
2. **检查点策略**：平衡检查点数量和重计算开销
3. **use_reentrant**：控制反向传播行为
4. **混合策略**：与混合精度、并行策略结合使用
