<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# KV Cache 优化策略

> 本案例详解 KV Cache 优化策略：缓存复用、量化压缩、分级存储

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    KV Cache 优化体系                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  KV Cache 生命周期                       │   │
│  │                                                           │   │
│  │  Prompt → Prefill → Decode → Output                     │   │
│  │           ↑                                     ↑         │   │
│  │           └───────── KV Cache 保存 ─────────┘            │   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  优化策略:                                                       │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  量化压缩   │  │  缓存复用   │  │  分级存储   │             │
│  │  FP16→FP8  │  │ Prefix Cache│  │  GPU→CPU→SSD│             │
│  │  INT8/INT4 │  │  Chat History│ │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Prefix Caching 复用:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  System Prompt (共享):                                           │
│  "You are a helpful assistant."                                │
│  ↓ 生成 KV Cache                                               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  User 1: "Hello"     → 复用 System 的 KV Cache         │   │
│  │  User 2: "Hi there"  → 复用 System 的 KV Cache         │   │
│  │  User 3: "How are you" → 复用 System 的 KV Cache       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  节省: 60-80% Prefill 时间                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. KV Cache 量化的三种策略

| 量化方法 | 精度损失 | 显存节省 | 适用场景 |
|----------|----------|----------|----------|
| FP8 | ~0% | 50% | 高质量需求 |
| INT8 | ~1% | 75% | 平衡场景 |
| INT4 | ~5% | 87.5% | 内存受限场景 |

```python
# INT8 量化实现
def quantize_kv_cache(k_cache, v_cache, quantize_ratio=0.5):
    """KV Cache INT8 量化"""
    # 动态量化：按 tensor 的 min/max 缩放
    k_quantized = torch.quantize_per_tensor(k_cache, scale, zero_point, torch.int8)
    v_quantized = torch.quantize_per_tensor(v_cache, scale, zero_point, torch.int8)
    return k_quantized, v_quantized

# FP8 量化 (H100 支持)
def fp8_quantize(tensor):
    """FP8 E4M3 量化"""
    scale = tensor.abs().max() / 448.0  # FP8 最大值
    return (tensor / scale).to(torch.float8_e4m3fn), scale
```

### 2. Prefix Caching

```python
class PrefixCacheManager:
    """前缀缓存管理器"""

    def __init__(self):
        self.cache = {}  # {prompt_hash: kv_cache}
        self.access_count = {}  # 统计访问频率

    def get_or_compute(self, prompt_tokens, model):
        prompt_hash = hash(prompt_tokens)

        if prompt_hash in self.cache:
            self.access_count[prompt_hash] += 1
            return self.cache[prompt_hash]

        # 计算 KV Cache
        kv_cache = model.compute_kv_cache(prompt_tokens)
        self.cache[prompt_hash] = kv_cache
        return kv_cache

    def evict_lfu(self):
        """LRU-FU 淘汰策略"""
        min_access = min(self.access_count.values())
        for k in list(self.cache.keys()):
            if self.access_count[k] == min_access:
                del self.cache[k]
                del self.access_count[k]
```

### 3. 分级存储

```python
class HierarchicalKVCache:
    """分级 KV Cache 存储"""

    def __init__(self, gpu_threshold=0.85):
        self.gpu_cache = {}  # GPU 显存
        self.cpu_cache = {}  # CPU 内存
        self.disk_cache = {}  # SSD
        self.gpu_threshold = gpu_threshold

    def store(self, request_id, kv_cache):
        gpu_memory_ratio = get_gpu_memory_usage()

        if gpu_memory_ratio < self.gpu_threshold:
            self.gpu_cache[request_id] = kv_cache
        elif cpu_memory_available():
            self.cpu_cache[request_id] = kv_cache
        else:
            self.disk_cache[request_id] = kv_cache

    def retrieve(self, request_id):
        if request_id in self.gpu_cache:
            return self.gpu_cache[request_id]
        elif request_id in self.cpu_cache:
            kv = self.cpu_cache.pop(request_id)
            self.store(request_id, kv)  # 尝试回 GPU
            return kv
        else:
            return self.disk_cache.pop(request_id)
```

## 📊 性能对比

| 优化策略 | 显存节省 | 延迟变化 | 吞吐提升 |
|----------|----------|----------|----------|
| FP8 量化 | 50% | +5% | 2x |
| INT8 量化 | 75% | +10% | 2.5x |
| Prefix Cache | 0% | -60% | 3x |
| **组合优化** | **85%** | -40% | **4x** |

## 📚 学习要点

1. **量化有损**：FP8 < INT8 < INT4
2. **Prefix 复用**：共享系统提示词
3. **分级存储**：GPU/CPU/SSD 分层管理
4. **动态策略**：根据负载自动选择策略

## 🔗 相关案例

- `paged-attention` - PagedAttention 详解
- `vllm-inference` - vLLM 高吞吐推理
- `continuous-batching` - Continuous Batching

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
