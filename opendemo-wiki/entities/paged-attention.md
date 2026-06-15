---
title: PagedAttention
summary: OS-style virtual memory management for KV Cache, reducing fragmentation from 40-60% to 4% and enabling 3-4x throughput improvement.
updated: 2026-06-05
tags:
  - llm
  - inference
  - paged-attention
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/inference/paged-attention/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# PagedAttention

PagedAttention applies OS virtual memory paging concepts to KV Cache management, solving internal fragmentation issues in LLM inference.

## Core Mechanism

**Traditional KV Cache (Continuous Allocation):**
- Pre-allocated contiguous GPU memory causes 40-60% internal fragmentation
- Variable sequence lengths across requests waste memory
- Cannot efficiently handle variable-length outputs

**PagedAttention Solution:**
- KV Cache divided into fixed-size blocks (e.g., 16 tokens/block)
- Block Table maps logical blocks to physical blocks
- On-demand physical block allocation, similar to OS Page Table

```
Logical KV Blocks (user-visible):
┌────────┬────────┬────────┬────────┐
│ Block 0│ Block 1│ Block 2│ Block 3│
│  [0-15]│ [16-31]│ [32-47]│ [48-63]│
└────────┴────────┴────────┴────────┘

Physical KV Blocks (GPU memory):
┌────────┬────────┬────────┬────────┬────────┐
│ Block 3│ Block 7│ Block 1│ Block 5│ Block 0│  Non-contiguous
└────────┴────────┴────────┴────────┴────────┘
     ▲         ▲         ▲         ▲         ▲
     └─────────┴─────────┴─────────┴─────────┘
           Mapped via block_table
```

## Core Data Structures

```python
class KVCacheManager:
    def __init__(self, num_blocks, block_size=16):
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.free_blocks = set(range(num_blocks))
        self.block_table = {}  # {request_id: [physical_block_ids]}

    def allocate(self, request_id, num_tokens):
        num_blocks_needed = (num_tokens + block_size - 1) // block_size
        blocks = [self.free_blocks.pop() for _ in range(num_blocks_needed)]
        self.block_table[request_id] = blocks
        return blocks

    def free(self, request_id):
        for block_id in self.block_table.pop(request_id, []):
            self.free_blocks.add(block_id)
```

## Attention Computation

```python
def paged_attention(query, key_cache, value_cache, block_table, block_size=16):
    seq_len = query.shape[1]
    num_blocks = (seq_len + block_size - 1) // block_size
    output = torch.zeros_like(query)

    for block_idx in range(num_blocks):
        physical_block = block_table[block_idx]
        start_token = block_idx * block_size
        end_token = min(start_token + block_size, seq_len)
        
        k = key_cache[physical_block, :, start_token:end_token]
        v = value_cache[physical_block, :, start_token:end_token]
        
        attn_weights = torch.matmul(query, k.transpose(-2, -1))
        attn_weights = F.softmax(attn_weights, dim=-1)
        output[:, start_token:end_token] = torch.matmul(attn_weights, v)

    return output
```

## Performance Comparison

| Strategy | Memory Utilization | Max Concurrency | Throughput |
|----------|-------------------|-----------------|------------|
| Contiguous Allocation | 40-60% | 16 | 1x |
| **PagedAttention** | **96%** | **64** | **3-4x** |

## Key Takeaways

1. **OS-style paging**: Borrowed from OS virtual memory concepts
2. **Non-contiguous storage**: Physical blocks can be scattered
3. **Block Table**: Logical-to-physical address mapping
4. **Reduced fragmentation**: From 40-60% down to 4%

## Related

- [[entities/kv-cache-optimization]] - KV Cache optimization strategies
- [[entities/tech-stacks]] - LLM inference stack overview
