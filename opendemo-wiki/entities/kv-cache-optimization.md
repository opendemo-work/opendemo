---
title: KV Cache Optimization
summary: KV Cache optimization via quantization (FP8/INT8/INT4), prefix caching reuse, and hierarchical GPU-CPU-SSD storage.
updated: 2026-06-05
tags:
  - llm
  - inference
  - kv-cache
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/inference/kv-cache-optimization/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# KV Cache Optimization

KV Cache optimization strategies including quantization compression, cache reuse, and tiered storage.

## Optimization Strategies

```
┌─────────────────────────────────────────────────────────────────┐
│                    KV Cache Optimization                        │
├─────────────────────────────────────────────────────────────────┤
│  Optimization Strategies:                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Quantization│  │Cache Reuse  │  │Tiered Storage│            │
│  │ FP16→FP8   │  │ Prefix Cache│  │GPU→CPU→SSD │            │
│  │ INT8/INT4  │  │ Chat History│  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

## Quantization Strategies

| Method | Accuracy Loss | Memory Savings | Use Case |
|--------|--------------|----------------|----------|
| FP8 | ~0% | 50% | High quality |
| INT8 | ~1% | 75% | Balanced |
| INT4 | ~5% | 87.5% | Memory constrained |

```python
# INT8 Quantization
def quantize_kv_cache(k_cache, v_cache, quantize_ratio=0.5):
    k_quantized = torch.quantize_per_tensor(k_cache, scale, zero_point, torch.int8)
    v_quantized = torch.quantize_per_tensor(v_cache, scale, zero_point, torch.int8)
    return k_quantized, v_quantized

# FP8 Quantization (H100 support)
def fp8_quantize(tensor):
    scale = tensor.abs().max() / 448.0  # FP8 max value
    return (tensor / scale).to(torch.float8_e4m3fn), scale
```

## Prefix Caching

System prompts generate shared KV Cache that all requests can reuse:

```python
class PrefixCacheManager:
    def __init__(self):
        self.cache = {}  # {prompt_hash: kv_cache}
        self.access_count = {}

    def get_or_compute(self, prompt_tokens, model):
        prompt_hash = hash(prompt_tokens)
        if prompt_hash in self.cache:
            self.access_count[prompt_hash] += 1
            return self.cache[prompt_hash]
        kv_cache = model.compute_kv_cache(prompt_tokens)
        self.cache[prompt_hash] = kv_cache
        return kv_cache

    def evict_lfu(self):
        min_access = min(self.access_count.values())
        for k in list(self.cache.keys()):
            if self.access_count[k] == min_access:
                del self.cache[k]
                del self.access_count[k]
```

## Hierarchical Storage

```python
class HierarchicalKVCache:
    def __init__(self, gpu_threshold=0.85):
        self.gpu_cache = {}
        self.cpu_cache = {}
        self.disk_cache = {}
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
            self.store(request_id, kv)
            return kv
        return self.disk_cache.pop(request_id)
```

## Performance Comparison

| Strategy | Memory Savings | Latency Change | Throughput |
|----------|---------------|----------------|------------|
| FP8 Quantization | 50% | +5% | 2x |
| INT8 Quantization | 75% | +10% | 2.5x |
| Prefix Cache | 0% | -60% | 3x |
| **Combined** | **85%** | -40% | **4x** |

## Key Takeaways

1. **Quantization是有损的**: FP8 < INT8 < INT4
2. **Prefix复用**: Share system prompt KV Cache
3. **分层存储**: GPU/CPU/SSD tiered management
4. **动态策略**: Auto-select based on workload

## Related

- [[entities/paged-attention]] - PagedAttention memory management
- [[entities/awq-quantization]] - Weight quantization methods
- [[entities/tech-stacks]] - LLM inference stack
