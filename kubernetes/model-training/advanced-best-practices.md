# 大模型训练高级最佳实践

## 1. 训练策略优化

### 1.1 混合精度训练最佳实践

```python
# advanced_mixed_precision_training.py
import torch
import torch.nn as nn
from torch.cuda.amp import autocast, GradScaler
from torch.utils.data import DataLoader
import torch.distributed as dist
from typing import Dict, Any, Optional

class AdvancedMixedPrecisionTrainer:
    def __init__(self, model: nn.Module, optimizer, scheduler=None):
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.scaler = GradScaler(enabled=True)
        self.gradient_accumulation_steps = 1
        self.clip_grad_norm = 1.0
        
    def train_step(self, batch: Dict[str, torch.Tensor], accumulation_step: int = 0) -> Dict[str, float]:
        """高级混合精度训练步骤"""
        # 自动混合精度上下文
        with autocast(enabled=True, dtype=torch.bfloat16):
            outputs = self.model(**batch)
            loss = outputs.loss
            
            # 梯度累积处理
            if self.gradient_accumulation_steps > 1:
                loss = loss / self.gradient_accumulation_steps
        
        # 反向传播（缩放梯度）
        self.scaler.scale(loss).backward()
        
        # 梯度累积完成时执行优化步骤
        if (accumulation_step + 1) % self.gradient_accumulation_steps == 0:
            # 梯度裁剪
            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.clip_grad_norm)
            
            # 更新参数
            self.scaler.step(self.optimizer)
            self.scaler.update()
            
            # 清零梯度
            self.optimizer.zero_grad()
            
            # 学习率调度
            if self.scheduler:
                self.scheduler.step()
        
        return {
            'loss': loss.item() * self.gradient_accumulation_steps,
            'learning_rate': self.optimizer.param_groups[0]['lr'],
            'scale_factor': self.scaler.get_scale()
        }
    
    def dynamic_precision_adjustment(self, loss_history: list, window_size: int = 100):
        """动态精度调整策略"""
        if len(loss_history) < window_size:
            return torch.bfloat16
            
        recent_losses = loss_history[-window_size:]
        loss_variance = torch.var(torch.tensor(recent_losses)).item()
        
        # 根据损失方差调整精度
        if loss_variance > 0.1:  # 高方差，使用更高精度
            return torch.float32
        elif loss_variance < 0.01:  # 低方差，可以使用更低精度
            return torch.bfloat16
        else:
            return torch.bfloat16

# 分布式混合精度训练配置
class DistributedAdvancedTrainer(AdvancedMixedPrecisionTrainer):
    def __init__(self, model: nn.Module, optimizer, scheduler=None, 
                 gradient_compression: bool = True):
        super().__init__(model, optimizer, scheduler)
        self.gradient_compression = gradient_compression
        self.world_size = dist.get_world_size() if dist.is_initialized() else 1
        
    def compressed_all_reduce(self, tensor: torch.Tensor) -> torch.Tensor:
        """压缩梯度的AllReduce操作"""
        if not self.gradient_compression:
            return tensor
            
        # 梯度压缩策略
        original_shape = tensor.shape
        tensor_flat = tensor.flatten()
        
        # 稀疏化处理
        threshold = torch.kthvalue(torch.abs(tensor_flat), 
                                 int(0.9 * tensor_flat.numel())).values
        mask = torch.abs(tensor_flat) >= threshold
        sparse_tensor = tensor_flat * mask
        
        # 量化压缩
        min_val, max_val = sparse_tensor.min(), sparse_tensor.max()
        quantized = ((sparse_tensor - min_val) / (max_val - min_val + 1e-8) * 255).byte()
        
        # AllReduce操作
        dist.all_reduce(quantized.float(), op=dist.ReduceOp.SUM)
        quantized = quantized / self.world_size
        
        # 反量化
        decompressed = quantized.float() / 255.0 * (max_val - min_val) + min_val
        decompressed = decompressed * mask  # 应用稀疏掩码
        
        return decompressed.reshape(original_shape)

# 使用示例
def create_advanced_training_setup():
    # 模型初始化
    model = create_large_model()  # 假设的大型模型创建函数
    model = model.cuda()
    
    # 优化器配置
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=1e-4,
        betas=(0.9, 0.999),
        eps=1e-8,
        weight_decay=0.01
    )
    
    # 学习率调度器
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=10000, eta_min=1e-6
    )
    
    # 创建高级训练器
    trainer = AdvancedMixedPrecisionTrainer(
        model=model,
        optimizer=optimizer,
        scheduler=scheduler
    )
    
    return trainer
```

### 1.2 学习率预热和调度策略

```python
# advanced_lr_scheduling.py
import math
import torch
from torch.optim.lr_scheduler import _LRScheduler

class AdvancedLRScheduler(_LRScheduler):
    def __init__(self, optimizer, warmup_steps: int, total_steps: int,
                 peak_lr: float, min_lr: float = 1e-6, 
                 warmup_type: str = 'linear', decay_type: str = 'cosine'):
        self.warmup_steps = warmup_steps
        self.total_steps = total_steps
        self.peak_lr = peak_lr
        self.min_lr = min_lr
        self.warmup_type = warmup_type
        self.decay_type = decay_type
        super().__init__(optimizer)
    
    def get_lr(self):
        current_step = self.last_epoch
        
        # 预热阶段
        if current_step < self.warmup_steps:
            if self.warmup_type == 'linear':
                # 线性预热
                progress = current_step / self.warmup_steps
                return [self.min_lr + (self.peak_lr - self.min_lr) * progress 
                       for _ in self.base_lrs]
            elif self.warmup_type == 'exponential':
                # 指数预热
                progress = current_step / self.warmup_steps
                return [self.min_lr + (self.peak_lr - self.min_lr) * (progress ** 2)
                       for _ in self.base_lrs]
        
        # 衰减阶段
        decay_steps = self.total_steps - self.warmup_steps
        decay_progress = (current_step - self.warmup_steps) / decay_steps
        
        if self.decay_type == 'cosine':
            # 余弦衰减
            cosine_factor = 0.5 * (1 + math.cos(math.pi * decay_progress))
            return [self.min_lr + (self.peak_lr - self.min_lr) * cosine_factor
                   for _ in self.base_lrs]
        elif self.decay_type == 'linear':
            # 线性衰减
            linear_factor = max(0.0, 1.0 - decay_progress)
            return [self.min_lr + (self.peak_lr - self.min_lr) * linear_factor
                   for _ in self.base_lrs]
        elif self.decay_type == 'polynomial':
            # 多项式衰减
            poly_factor = (1 - decay_progress) ** 2
            return [self.min_lr + (self.peak_lr - self.min_lr) * poly_factor
                   for _ in self.base_lrs]

class CyclicalLRScheduler(_LRScheduler):
    """循环学习率调度器"""
    def __init__(self, optimizer, base_lr: float, max_lr: float, 
                 step_size_up: int, step_size_down: int = None,
                 mode: str = 'triangular'):
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.step_size_up = step_size_up
        self.step_size_down = step_size_down or step_size_up
        self.mode = mode
        super().__init__(optimizer)
    
    def get_lr(self):
        cycle = math.floor(1 + self.last_epoch / (self.step_size_up + self.step_size_down))
        x = abs(self.last_epoch / self.step_size_up - 2 * cycle + 1)
        
        if self.mode == 'triangular':
            return [self.base_lr + (self.max_lr - self.base_lr) * max(0, (1 - x))
                   for _ in self.base_lrs]
        elif self.mode == 'triangular2':
            return [self.base_lr + (self.max_lr - self.base_lr) * max(0, (1 - x)) / float(2 ** (cycle - 1))
                   for _ in self.base_lrs]

# 自适应学习率调整
class AdaptiveLRScheduler:
    def __init__(self, optimizer, initial_lr: float, patience: int = 10):
        self.optimizer = optimizer
        self.initial_lr = initial_lr
        self.patience = patience
        self.best_loss = float('inf')
        self.bad_epochs = 0
        self.lr_reduction_factor = 0.5
        
    def step(self, current_loss: float):
        """根据验证损失自适应调整学习率"""
        if current_loss < self.best_loss:
            self.best_loss = current_loss
            self.bad_epochs = 0
        else:
            self.bad_epochs += 1
            
        if self.bad_epochs >= self.patience:
            # 降低学习率
            for param_group in self.optimizer.param_groups:
                param_group['lr'] *= self.lr_reduction_factor
            self.bad_epochs = 0
            print(f"Learning rate reduced to {param_group['lr']}")
            
        return self.optimizer.param_groups[0]['lr']

# 使用示例
def setup_advanced_schedulers(optimizer, total_steps: int):
    # 主调度器
    main_scheduler = AdvancedLRScheduler(
        optimizer=optimizer,
        warmup_steps=1000,
        total_steps=total_steps,
        peak_lr=5e-4,
        min_lr=1e-6,
        warmup_type='linear',
        decay_type='cosine'
    )
    
    # 循环调度器（可选）
    cyclical_scheduler = CyclicalLRScheduler(
        optimizer=optimizer,
        base_lr=1e-5,
        max_lr=1e-3,
        step_size_up=500,
        mode='triangular2'
    )
    
    # 自适应调度器
    adaptive_scheduler = AdaptiveLRScheduler(
        optimizer=optimizer,
        initial_lr=5e-4,
        patience=5
    )
    
    return {
        'main': main_scheduler,
        'cyclical': cyclical_scheduler,
        'adaptive': adaptive_scheduler
    }
```

## 2. 数据处理优化

### 2.1 高效数据加载管道

```python
# advanced_data_pipeline.py
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import Iterator, Optional, Callable
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
import queue
import time

class AdvancedDataset(Dataset):
    def __init__(self, data_path: str, tokenizer, max_length: int = 512,
                 preprocessing_fn: Optional[Callable] = None):
        self.data_path = data_path
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.preprocessing_fn = preprocessing_fn or self.default_preprocessing
        self.data = self._load_data()
        
    def _load_data(self):
        """高效数据加载"""
        # 这里实现具体的数据加载逻辑
        # 支持多种数据格式（JSON、Parquet、TFRecord等）
        pass
    
    def default_preprocessing(self, text: str) -> dict:
        """默认预处理函数"""
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        return {k: v.squeeze(0) for k, v in encoding.items()}
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        return self.preprocessing_fn(item)

class SmartDataLoader:
    def __init__(self, dataset: Dataset, batch_size: int, 
                 num_workers: int = 4, pin_memory: bool = True,
                 prefetch_factor: int = 2, persistent_workers: bool = True):
        self.dataset = dataset
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.prefetch_factor = prefetch_factor
        self.persistent_workers = persistent_workers
        
        # 智能批处理大小调整
        self.adaptive_batching = AdaptiveBatching(
            initial_batch_size=batch_size,
            memory_monitor=self._monitor_memory
        )
    
    def _monitor_memory(self) -> float:
        """监控GPU内存使用率"""
        if torch.cuda.is_available():
            return torch.cuda.memory_allocated() / torch.cuda.get_device_properties(0).total_memory
        return 0.0
    
    def get_dataloader(self, shuffle: bool = True) -> DataLoader:
        """获取优化的数据加载器"""
        current_batch_size = self.adaptive_batching.get_optimal_batch_size()
        
        return DataLoader(
            self.dataset,
            batch_size=current_batch_size,
            shuffle=shuffle,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            prefetch_factor=self.prefetch_factor,
            persistent_workers=self.persistent_workers,
            collate_fn=self._smart_collate,
            worker_init_fn=self._worker_init
        )
    
    def _smart_collate(self, batch):
        """智能批处理函数"""
        # 自动处理不同长度的序列
        max_length = max(len(item['input_ids']) for item in batch)
        
        # 填充到相同长度
        padded_batch = {}
        for key in batch[0].keys():
            if key in ['input_ids', 'attention_mask', 'labels']:
                padded_batch[key] = torch.stack([
                    torch.nn.functional.pad(
                        item[key], 
                        (0, max_length - len(item[key])), 
                        value=0
                    ) for item in batch
                ])
            else:
                padded_batch[key] = torch.stack([item[key] for item in batch])
        
        return padded_batch
    
    def _worker_init(self, worker_id):
        """工作进程初始化"""
        # 设置随机种子
        worker_seed = torch.initial_seed() % 2**32
        np.random.seed(worker_seed)
        
        # 设置CPU亲和性（可选）
        if hasattr(os, 'sched_setaffinity'):
            try:
                os.sched_setaffinity(0, {worker_id % mp.cpu_count()})
            except:
                pass

class AdaptiveBatching:
    def __init__(self, initial_batch_size: int, memory_monitor: Callable,
                 min_batch_size: int = 1, max_batch_size: int = 128):
        self.current_batch_size = initial_batch_size
        self.memory_monitor = memory_monitor
        self.min_batch_size = min_batch_size
        self.max_batch_size = max_batch_size
        self.memory_history = []
        self.adjustment_cooldown = 100  # 调整冷却步数
        self.steps_since_adjustment = 0
    
    def get_optimal_batch_size(self) -> int:
        """获取最优批处理大小"""
        if self.steps_since_adjustment < self.adjustment_cooldown:
            self.steps_since_adjustment += 1
            return self.current_batch_size
        
        current_memory = self.memory_monitor()
        self.memory_history.append(current_memory)
        
        # 保持最近100个内存使用记录
        if len(self.memory_history) > 100:
            self.memory_history.pop(0)
        
        # 根据内存使用情况调整批处理大小
        if len(self.memory_history) >= 10:
            avg_memory = np.mean(self.memory_history[-10:])
            
            if avg_memory > 0.85:  # 内存使用过高
                self.current_batch_size = max(
                    self.min_batch_size, 
                    self.current_batch_size // 2
                )
                print(f"Reducing batch size to {self.current_batch_size} due to high memory usage")
            elif avg_memory < 0.6:  # 内存使用较低
                self.current_batch_size = min(
                    self.max_batch_size,
                    self.current_batch_size * 2
                )
                print(f"Increasing batch size to {self.current_batch_size}")
            
            self.steps_since_adjustment = 0
        
        return self.current_batch_size

# 异步数据预取
class AsyncDataPrefetcher:
    def __init__(self, dataloader: DataLoader, device: torch.device):
        self.dataloader = dataloader
        self.device = device
        self.stream = torch.cuda.Stream() if device.type == 'cuda' else None
        
    def __iter__(self) -> Iterator:
        self.iterator = iter(self.dataloader)
        self.preload()
        return self
    
    def preload(self):
        try:
            self.next_batch = next(self.iterator)
        except StopIteration:
            self.next_batch = None
            return
            
        if self.stream is not None:
            with torch.cuda.stream(self.stream):
                self.next_batch = {k: v.cuda(non_blocking=True) 
                                 for k, v in self.next_batch.items()}
    
    def __next__(self):
        torch.cuda.current_stream().wait_stream(self.stream) if self.stream else None
        
        batch = self.next_batch
        if batch is None:
            raise StopIteration
            
        self.preload()
        return batch

# 使用示例
def create_optimized_data_pipeline(data_path: str, tokenizer, batch_size: int = 32):
    # 创建数据集
    dataset = AdvancedDataset(
        data_path=data_path,
        tokenizer=tokenizer,
        max_length=512
    )
    
    # 创建智能数据加载器
    smart_loader = SmartDataLoader(
        dataset=dataset,
        batch_size=batch_size,
        num_workers=min(8, mp.cpu_count()),
        pin_memory=torch.cuda.is_available()
    )
    
    # 获取优化的数据加载器
    dataloader = smart_loader.get_dataloader(shuffle=True)
    
    # 如果使用GPU，添加异步预取
    if torch.cuda.is_available():
        device = torch.device('cuda')
        dataloader = AsyncDataPrefetcher(dataloader, device)
    
    return dataloader
```

## 3. 模型优化技术

### 3.1 梯度优化和正则化

```python
# advanced_gradient_optimization.py
import torch
import torch.nn as nn
from torch.optim.optimizer import Optimizer
from typing import List, Tuple, Optional
import math

class GradientNoiseScheduler:
    """梯度噪声调度器"""
    def __init__(self, initial_noise: float = 0.01, decay_rate: float = 0.999):
        self.initial_noise = initial_noise
        self.decay_rate = decay_rate
        self.step_count = 0
    
    def get_noise_scale(self) -> float:
        """获取当前噪声尺度"""
        noise_scale = self.initial_noise * (self.decay_rate ** self.step_count)
        self.step_count += 1
        return noise_scale
    
    def add_gradient_noise(self, parameters: List[nn.Parameter]):
        """向梯度添加噪声"""
        noise_scale = self.get_noise_scale()
        
        for param in parameters:
            if param.grad is not None:
                noise = torch.randn_like(param.grad) * noise_scale
                param.grad.add_(noise)

class LookaheadOptimizer(Optimizer):
    """Lookahead优化器包装器"""
    def __init__(self, optimizer: Optimizer, k: int = 5, alpha: float = 0.5):
        self.optimizer = optimizer
        self.k = k
        self.alpha = alpha
        self.step_counter = 0
        
        # 保存慢权重
        self.slow_weights = [
            [param.clone().detach() for param in group['params']]
            for group in optimizer.param_groups
        ]
        
        # 注册参数组
        for i, group in enumerate(optimizer.param_groups):
            for j, param in enumerate(group['params']):
                if param.requires_grad:
                    param.register_hook(lambda grad: self._lookahead_step(i, j, grad))
    
    def _lookahead_step(self, group_idx: int, param_idx: int, grad: torch.Tensor):
        """Lookahead更新步骤"""
        if self.step_counter % self.k == 0:
            fast_param = self.optimizer.param_groups[group_idx]['params'][param_idx]
            slow_param = self.slow_weights[group_idx][param_idx]
            
            # 更新慢权重
            slow_param.add_(fast_param - slow_param, alpha=self.alpha)
            
            # 同步快权重到慢权重
            fast_param.data.copy_(slow_param)
        
        self.step_counter += 1
    
    def step(self, closure=None):
        """执行优化步骤"""
        loss = self.optimizer.step(closure)
        return loss
    
    def zero_grad(self):
        """清零梯度"""
        self.optimizer.zero_grad()

class SAMOptimizer(Optimizer):
    """Sharpness-Aware Minimization (SAM) 优化器"""
    def __init__(self, params, base_optimizer, rho: float = 0.05, **kwargs):
        defaults = dict(rho=rho, **kwargs)
        super(SAMOptimizer, self).__init__(params, defaults)
        
        self.base_optimizer = base_optimizer(params, **kwargs)
        self.param_groups = self.base_optimizer.param_groups
    
    @torch.no_grad()
    def first_step(self, zero_grad=False):
        """第一步：找到sharp direction"""
        grad_norm = self._grad_norm()
        for group in self.param_groups:
            scale = group['rho'] / (grad_norm + 1e-12)
            
            for p in group['params']:
                if p.grad is None:
                    continue
                e_w = p.grad * scale
                p.add_(e_w)  # w + e(w)
                self.state[p]['e_w'] = e_w
        
        if zero_grad:
            self.zero_grad()
    
    @torch.no_grad()
    def second_step(self, zero_grad=False):
        """第二步：沿着sharp direction优化"""
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                p.sub_(self.state[p]['e_w'])  # w + e(w) -> w
        
        self.base_optimizer.step()
        
        if zero_grad:
            self.zero_grad()
    
    def step(self, closure=None):
        """完整的SAM步骤"""
        if closure is None:
            raise ValueError("SAM requires closure")
        
        # 第一步
        closure()
        self.first_step(zero_grad=True)
        
        # 第二步
        closure()
        self.second_step()
    
    def _grad_norm(self):
        """计算梯度范数"""
        norm = torch.norm(
            torch.stack([
                p.grad.norm(p=2) for group in self.param_groups 
                for p in group['params'] if p.grad is not None
            ]),
            p=2
        )
        return norm

class GradientCentralization:
    """梯度中心化"""
    @staticmethod
    def apply(parameters: List[nn.Parameter]):
        """应用梯度中心化"""
        for param in parameters:
            if param.dim() > 1 and param.grad is not None:
                # 对卷积层和线性层应用梯度中心化
                grad = param.grad
                grad.add_(-grad.mean(dim=tuple(range(1, grad.dim())), keepdim=True))

# 使用示例
def create_advanced_optimizers(model: nn.Module):
    # 基础AdamW优化器
    base_optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=1e-4,
        betas=(0.9, 0.999),
        eps=1e-8,
        weight_decay=0.01
    )
    
    # 添加Lookahead
    lookahead_optimizer = LookaheadOptimizer(
        optimizer=base_optimizer,
        k=5,
        alpha=0.5
    )
    
    # 添加梯度噪声
    noise_scheduler = GradientNoiseScheduler(
        initial_noise=0.01,
        decay_rate=0.999
    )
    
    # 添加梯度中心化
    gradient_centralization = GradientCentralization()
    
    return {
        'optimizer': lookahead_optimizer,
        'noise_scheduler': noise_scheduler,
        'centralization': gradient_centralization
    }

# 训练循环中的使用
def advanced_training_step(model, batch, optimizers):
    # 前向传播
    outputs = model(**batch)
    loss = outputs.loss
    
    # 反向传播
    loss.backward()
    
    # 应用梯度中心化
    optimizers['centralization'].apply(model.parameters())
    
    # 添加梯度噪声
    optimizers['noise_scheduler'].add_gradient_noise(model.parameters())
    
    # 优化步骤
    optimizers['optimizer'].step()
    optimizers['optimizer'].zero_grad()
    
    return loss.item()
```

## 4. 训练监控和调试

### 4.1 高级监控系统

```python
# advanced_monitoring.py
import torch
import time
import psutil
import GPUtil
from typing import Dict, List, Optional
import json
import matplotlib.pyplot as plt
from collections import defaultdict, deque
import numpy as np

class TrainingMonitor:
    def __init__(self, log_dir: str = './logs', 
                 monitoring_interval: float = 1.0,
                 max_history: int = 10000):
        self.log_dir = log_dir
        self.monitoring_interval = monitoring_interval
        self.max_history = max_history
        
        # 监控指标历史
        self.metrics_history = defaultdict(deque)
        self.system_metrics = defaultdict(deque)
        
        # 训练状态
        self.start_time = time.time()
        self.step_count = 0
        self.epoch_count = 0
        
    def log_metrics(self, metrics: Dict[str, float], step: int = None):
        """记录训练指标"""
        if step is None:
            step = self.step_count
            self.step_count += 1
            
        timestamp = time.time()
        
        # 记录指标
        for key, value in metrics.items():
            self.metrics_history[key].append({
                'step': step,
                'value': value,
                'timestamp': timestamp
            })
            
            # 限制历史长度
            if len(self.metrics_history[key]) > self.max_history:
                self.metrics_history[key].popleft()
    
    def log_system_metrics(self):
        """记录系统指标"""
        timestamp = time.time()
        
        # CPU使用率
        cpu_percent = psutil.cpu_percent()
        
        # 内存使用
        memory_info = psutil.virtual_memory()
        
        # GPU使用率（如果有）
        gpu_metrics = {}
        try:
            gpus = GPUtil.getGPUs()
            for i, gpu in enumerate(gpus):
                gpu_metrics[f'gpu_{i}_utilization'] = gpu.load * 100
                gpu_metrics[f'gpu_{i}_memory_used'] = gpu.memoryUsed
                gpu_metrics[f'gpu_{i}_memory_total'] = gpu.memoryTotal
                gpu_metrics[f'gpu_{i}_temperature'] = gpu.temperature
        except:
            pass
        
        system_data = {
            'timestamp': timestamp,
            'cpu_percent': cpu_percent,
            'memory_percent': memory_info.percent,
            'memory_used_gb': memory_info.used / (1024**3),
            'elapsed_time': timestamp - self.start_time,
            **gpu_metrics
        }
        
        self.system_metrics['system'].append(system_data)
        
        # 限制历史长度
        if len(self.system_metrics['system']) > self.max_history:
            self.system_metrics['system'].popleft()
    
    def get_training_summary(self) -> Dict:
        """获取训练摘要"""
        elapsed_time = time.time() - self.start_time
        steps_per_second = self.step_count / elapsed_time if elapsed_time > 0 else 0
        
        # 计算最新的损失值
        loss_history = self.metrics_history.get('loss', [])
        recent_losses = [entry['value'] for entry in list(loss_history)[-100:]]
        
        summary = {
            'elapsed_time': elapsed_time,
            'total_steps': self.step_count,
            'steps_per_second': steps_per_second,
            'current_epoch': self.epoch_count,
            'recent_loss_mean': np.mean(recent_losses) if recent_losses else 0,
            'recent_loss_std': np.std(recent_losses) if recent_losses else 0
        }
        
        return summary
    
    def plot_metrics(self, metrics_to_plot: List[str] = None):
        """绘制指标图表"""
        if metrics_to_plot is None:
            metrics_to_plot = ['loss', 'learning_rate']
        
        fig, axes = plt.subplots(len(metrics_to_plot), 1, figsize=(12, 4*len(metrics_to_plot)))
        if len(metrics_to_plot) == 1:
            axes = [axes]
        
        for i, metric_name in enumerate(metrics_to_plot):
            if metric_name in self.metrics_history:
                data = self.metrics_history[metric_name]
                steps = [entry['step'] for entry in data]
                values = [entry['value'] for entry in data]
                
                axes[i].plot(steps, values, linewidth=1)
                axes[i].set_title(f'{metric_name} over time')
                axes[i].set_xlabel('Steps')
                axes[i].set_ylabel(metric_name)
                axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.log_dir}/training_metrics.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_logs(self):
        """保存日志到文件"""
        log_data = {
            'metrics': dict(self.metrics_history),
            'system_metrics': dict(self.system_metrics),
            'training_summary': self.get_training_summary()
        }
        
        with open(f'{self.log_dir}/training_log.json', 'w') as f:
            json.dump(log_data, f, indent=2, default=str)

class GradientMonitor:
    """梯度监控器"""
    def __init__(self, model: torch.nn.Module, log_interval: int = 100):
        self.model = model
        self.log_interval = log_interval
        self.gradient_stats = defaultdict(list)
        self.step_count = 0
    
    def monitor_gradients(self):
        """监控梯度统计"""
        if self.step_count % self.log_interval != 0:
            self.step_count += 1
            return
        
        timestamp = time.time()
        
        for name, param in self.model.named_parameters():
            if param.grad is not None:
                grad_norm = param.grad.norm().item()
                grad_mean = param.grad.mean().item()
                grad_std = param.grad.std().item()
                
                self.gradient_stats[name].append({
                    'step': self.step_count,
                    'norm': grad_norm,
                    'mean': grad_mean,
                    'std': grad_std,
                    'timestamp': timestamp
                })
        
        self.step_count += 1
    
    def get_gradient_summary(self) -> Dict:
        """获取梯度摘要"""
        summary = {}
        
        for name, stats in self.gradient_stats.items():
            if stats:
                recent_stats = stats[-10:]  # 最近10次记录
                norms = [s['norm'] for s in recent_stats]
                
                summary[name] = {
                    'avg_norm': np.mean(norms),
                    'max_norm': np.max(norms),
                    'min_norm': np.min(norms),
                    'vanishing_gradients': np.mean(norms) < 1e-6,
                    'exploding_gradients': np.mean(norms) > 100
                }
        
        return summary

class EarlyStopping:
    """早停机制"""
    def __init__(self, patience: int = 10, min_delta: float = 0.001, 
                 restore_best_weights: bool = True):
        self.patience = patience
        self.min_delta = min_delta
        self.restore_best_weights = restore_best_weights
        self.best_loss = float('inf')
        self.counter = 0
        self.best_weights = None
        self.early_stop = False
    
    def __call__(self, val_loss: float, model: torch.nn.Module = None):
        """检查是否应该早停"""
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
            if self.restore_best_weights and model is not None:
                self.best_weights = {
                    name: param.data.clone() 
                    for name, param in model.named_parameters()
                }
        else:
            self.counter += 1
            
        if self.counter >= self.patience:
            self.early_stop = True
            if self.restore_best_weights and model is not None and self.best_weights:
                # 恢复最佳权重
                for name, param in model.named_parameters():
                    param.data.copy_(self.best_weights[name])
            
        return self.early_stop

# 使用示例
def setup_advanced_monitoring(log_dir: str = './logs'):
    # 创建监控器
    monitor = TrainingMonitor(log_dir=log_dir)
    gradient_monitor = GradientMonitor(model)  # 需要传入实际模型
    
    # 创建早停机制
    early_stopping = EarlyStopping(patience=15, min_delta=0.001)
    
    return {
        'monitor': monitor,
        'gradient_monitor': gradient_monitor,
        'early_stopping': early_stopping
    }

# 在训练循环中使用
def training_loop_with_monitoring(model, train_loader, val_loader, optimizers, monitors, epochs: int):
    for epoch in range(epochs):
        # 训练阶段
        model.train()
        for batch in train_loader:
            # 训练步骤
            loss = advanced_training_step(model, batch, optimizers)
            
            # 记录指标
            monitors['monitor'].log_metrics({
                'loss': loss,
                'learning_rate': optimizers['optimizer'].param_groups[0]['lr']
            })
            
            # 监控梯度
            monitors['gradient_monitor'].monitor_gradients()
            
            # 记录系统指标
            monitors['monitor'].log_system_metrics()
        
        # 验证阶段
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                outputs = model(**batch)
                val_loss += outputs.loss.item()
        
        val_loss /= len(val_loader)
        
        # 检查早停
        if monitors['early_stopping'](val_loss, model):
            print(f"Early stopping at epoch {epoch}")
            break
        
        # 更新epoch计数
        monitors['monitor'].epoch_count = epoch + 1
        
        # 定期保存日志
        if epoch % 5 == 0:
            monitors['monitor'].save_logs()
    
    # 保存最终日志
    monitors['monitor'].save_logs()
    monitors['monitor'].plot_metrics(['loss', 'learning_rate'])
```

这个高级最佳实践文档包含了训练策略优化、数据处理优化、模型优化技术和训练监控调试等四个核心方面的深度内容，为大模型训练提供了专业级的指导方案。