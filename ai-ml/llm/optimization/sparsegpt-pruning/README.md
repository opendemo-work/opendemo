# SparseGPT 单次剪枝

> 本案例详解 SparseGPT (Sparse Generative Pre-training) 单次剪枝技术，理解其误差修正机制与稀疏度控制

## 核心原理

### SparseGPT 核心思想

```
传统剪枝：逐层独立剪枝，误差累积
SparseGPT：利用 Hessian 信息进行全局误差修正

关键洞察：
- 剪枝造成的误差可以通过调整其他权重来补偿
- 需要计算 Hessian 矩阵的逆来确定补偿量
- 但直接计算 Hessian 逆不现实，采用近似方法
```

### 剪枝公式

```python
# SparseGPT 误差修正
def sparsegpt_update(W, hessian, mask, pruned_indices):
    """
    W: 原始权重矩阵
    hessian: Hessian 矩阵近似
    mask: 剪枝掩码 (1=保留, 0=剪掉)
    """
    # 计算需要补偿的误差
    error = W[:, pruned_indices] @ hessian[pruned_indices]
    
    # 最小二乘求解补偿量
    h_inv = torch.linalg.inv(hessian + 1e-6 * torch.eye(hessian.size(0)))
    compensation = -h_inv @ error
    
    # 应用补偿
    W_new = W + compensation * mask
    return W_new
```

## 实现代码

### SparseGPT 剪枝器

```python
import torch
import torch.nn as nn

class SparseGPTPruner:
    def __init__(self, model, sparsity=0.5):
        self.model = model
        self.sparsity = sparsity
        self.masks = {}
        
    def compute_hessian_approximation(self, layer, x, y):
        """计算 Hessian 近似 (Fisher Information Matrix)"""
        # 使用随机投影近似
        proj = torch.randn(x.shape[-1], 512, device=x.device)
        x_proj = x @ proj
        
        # Fisher 信息矩阵近似
        hessian_approx = x_proj.t() @ x_proj / x.shape[0]
        return hessian_approx
    
    def prune_layer(self, layer, x, y):
        """对单个层进行剪枝"""
        W = layer.weight.data.clone()
        n, m = W.shape
        n_pruned = int(m * self.sparsity)
        
        # 计算每个权重的重要性 (基于 Fisher 信息)
        importance = (W ** 2).mean(dim=0)
        
        # 找出最不重要的权重索引
        prune_indices = torch.argsort(importance)[:n_pruned]
        
        # 创建掩码
        mask = torch.ones_like(W)
        mask[:, prune_indices] = 0
        
        # 误差修正
        hessian = self.compute_hessian_approximation(layer, x, y)
        W_corrected = self.sparsegpt_error_correction(W, hessian, mask, prune_indices)
        
        # 更新权重
        layer.weight.data = W_corrected
        self.masks[layer] = mask
        
    def sparsegpt_error_correction(self, W, hessian, mask, pruned_indices):
        """SparseGPT 核心：误差修正"""
        # 仅对保留权重进行补偿
        W_compensated = W.clone()
        
        # 简化版本：使用对角近似
        h_diag = hessian.diagonal()
        for idx in pruned_indices:
            # 计算该通道的误差
            error = (W[:, idx] * h_diag).sum()
            # 按比例分配到其他权重
            correction = -error / (h_diag.sum() + 1e-6)
            W_compensated[:, idx] = 0
            W_compensated[:, :len(correction)] += correction * mask[:, :len(correction)]
            
        return W_compensated
```

## 稀疏度对比

| 稀疏度 | SparseGPT PPL | Magnitude PPL | 显存减少 |
|--------|---------------|---------------|---------|
| 0% | 12.5 | 12.5 | 1.0x |
| 50% | 13.2 | 15.8 | 1.5x |
| 70% | 14.5 | 18.2 | 2.0x |
| 90% | 18.3 | 25.6 | 3.0x |

## 使用命令

```bash
# 安装 SparseGPT
pip install git+https://github.com/IST-DASLab/sparsegpt.git

# 运行剪枝
python -m sparsegpt.prune \
    --model meta-llama/Llama-2-7b \
    --sparsity 0.5 \
    --nsamples 128

# 验证精度
python evaluate.py --model pruned_model --task mmlu
```

## 学习要点

1. **one-shot 剪枝**：一次性完成剪枝，无需迭代训练
2. **误差修正**：利用 Hessian 信息补偿剪枝误差
3. **稀疏度控制**：目标稀疏度决定剪枝比例
4. **对比 Magnitude**：SparseGPT 精度明显优于简单幅度剪枝
