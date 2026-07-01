<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# PagedAttention 内存管理

> 本案例详解 PagedAttention 技术：类操作系统分页的 KV Cache 管理机制

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  PagedAttention 核心原理                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  传统 KV Cache (连续显存分配):                                   │
│                                                                 │
│  Request 1: [K0][K1][K2][K3][K4][K5]...        占满 2048 slots   │
│  Request 2: [K0][K1]...                          内部碎片化       │
│                                                                 │
│  Internal Fragmentation: ~40-60%                                │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PagedAttention (分页管理):                                      │
│                                                                 │
│  Logical KV Blocks (对用户可见):                                 │
│  ┌────────┬────────┬────────┬────────┐                           │
│  │ Block 0│ Block 1│ Block 2│ Block 3│  ...                     │
│  │ [0-15] │ [16-31]│ [32-47]│ [48-63]│                         │
│  └────────┴────────┴────────┴────────┘                           │
│                                                                 │
│  Physical KV Blocks (GPU 显存):                                  │
│  ┌────────┬────────┬────────┬────────┬────────┐                 │
│  │ Block 3│ Block 7│ Block 1│ Block 5│ Block 0│  非连续分配      │
│  └────────┴────────┴────────┴────────┴────────┘                 │
│     ▲         ▲         ▲         ▲         ▲                   │
│     └─────────┴─────────┴─────────┴─────────┘                    │
│           通过 block_table 映射                                   │
│                                                                 │
│  Fragmentation: ~4%                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Block Table 结构:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Block Table: {request_id: [physical_block_ids]}                │
│                                                                 │
│  Request 1: block_table = [0, 5, 3, 7]  (4 个逻辑块)           │
│  Request 2: block_table = [2, 9]        (2 个逻辑块)             │
│                                                                 │
│  Attention 计算时，通过 block_table 查找物理块:                  │
│  for i in range(seq_len):                                       │
│      block_idx = i // block_size                                │
│      offset = i % block_size                                    │
│      physical_block = block_table[block_idx]                    │
│      physical_addr = physical_block * block_size + offset       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 为什么需要 PagedAttention

传统显存管理的问题：
- 预分配连续显存导致 Internal Fragmentation
- 不同请求序列长度差异大，显存利用率低
- 无法高效处理变长输出

**PagedAttention 解决方案：**
- 将 KV Cache 分成固定大小的 Block (如 16 tokens/block)
- 通过 Block Table 实现逻辑块到物理块的映射
- 类似 OS Page Table 机制，按需分配物理块

### 2. 核心数据结构

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

### 3. 注意力计算

```python
def paged_attention(query, key_cache, value_cache, block_table, block_size=16):
    """PagedAttention 计算"""
    seq_len = query.shape[1]
    num_blocks = (seq_len + block_size - 1) // block_size

    output = torch.zeros_like(query)

    for block_idx in range(num_blocks):
        physical_block = block_table[block_idx]
        start_token = block_idx * block_size
        end_token = min(start_token + block_size, seq_len)

        # 获取物理块中的 key/value
        k = key_cache[physical_block, :, start_token:end_token]
        v = value_cache[physical_block, :, start_token:end_token]

        # 计算注意力
        attn_weights = torch.matmul(query, k.transpose(-2, -1))
        attn_weights = F.softmax(attn_weights, dim=-1)
        output[:, start_token:end_token] = torch.matmul(attn_weights, v)

    return output
```

## 📊 性能对比

| 策略 | 显存利用率 | 最大并发 | 吞吐提升 |
|------|-----------|----------|----------|
| 连续分配 | 40-60% | 16 | 1x |
| **PagedAttention** | **96%** | **64** | **3-4x** |

## 📚 学习要点

1. **类 OS 分页**：借鉴操作系统虚拟内存思想
2. **非连续存储**：物理块可离散分布
3. **Block Table**：逻辑到物理的地址映射
4. **减少碎片**：从 40-60% 降到 4% 以下

## 🔗 相关案例

- `vllm-inference` - vLLM 高吞吐推理
- `kv-cache-optimization` - KV Cache 优化策略
- `continuous-batching` - Continuous Batching

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
