<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Continuous Batching 详解

> 本案例详解 Continuous Batching（迭代级调度）技术，理解其如何最大化 LLM 推理吞吐量

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Static Batching vs Continuous Batching         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Static Batching:                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Time →                                                    │   │
│  │                                                          │   │
│  │ Req1 [████████████]                                       │   │
│  │ Req2 [████████████████████]                               │   │
│  │ Req3 [██████████]                                         │   │
│  │ Req4 [███████████████████████████████]                   │   │
│  │                                                          │   │
│  │ GPU Utilization: LOW (等待最慢的请求完成)                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Continuous Batching:                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Time →                                                    │   │
│  │                                                          │   │
│  │ Iter 1: [Req1][Req2][Req3][Req4]  (4个请求同时处理)        │   │
│  │         ↓                                                 │   │
│  │ Iter 2: [Req1][Req2][Req3][Req4]                        │   │
│  │         ↓                                                 │   │
│  │ Iter 3: [Req1 completes][Req5 joins]                     │   │
│  │         ↓                                                 │   │
│  │ Iter 4: [Req2][Req3][Req4][Req5]  (新请求加入)            │   │
│  │         ↓                                                 │   │
│  │ Iter 5: [Req3 completes][Req6 joins]                     │   │
│  │         ↓                                                 │   │
│  │ Iter 6: [Req4][Req5][Req6][Req7]                         │   │
│  │                                                          │   │
│  │ GPU Utilization: HIGH (始终处理 batch_size 个请求)          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

调度器工作流程:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────────┐                                              │
│  │   Requests   │                                              │
│  │    Queue     │                                              │
│  └──────┬───────┘                                              │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Scheduler                              │   │
│  │                                                           │   │
│  │  1. 遍历所有 running sequences                           │   │
│  │  2. 生成 token                                           │   │
│  │  3. 检查完成的 sequences                                  │   │
│  │  4. 释放 KV cache blocks                                 │   │
│  │  5. 从 waiting queue 调度新 sequences                     │   │
│  │  6. 转备下一轮 batch                                     │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐                                              │
│  │  Block Mgr  │ ← 动态分配 KV Cache Blocks                    │
│  └──────────────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. Static Batching 的问题

```python
# Static Batching 示例
batch = [
    request_1,  # 短回复 (100 tokens)
    request_2,  # 长回复 (500 tokens) 
    request_3,  # 短回复 (80 tokens)
    request_4,  # 中等回复 (200 tokens)
]

# GPU 必须等待 request_2 完成才能处理下一个 batch
# GPU 利用率: ~30-50%
```

**问题：**
- 请求长度差异大，短请求被长请求阻塞
- GPU 空闲等待
- 吞吐量低

### 2. Continuous Batching 核心思想

**迭代级调度**：在每个 token 生成后检查：
1. 是否有请求完成？
2. 是否有新请求可以加入？
3. KV cache 空间是否足够？

### 3. 关键技术

| 技术 | 作用 |
|------|------|
| **Sequence Parallelism** | 允许不同序列使用不同序列长度 |
| **Dynamic Block Allocation** | 按需分配 KV cache blocks |
| **Iterative Scheduling** | 每迭代重新调度 |
| **Prefix Caching** | 复用共享前缀的 KV cache |

## 💻 完整实现

### 调度器实现

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from queue import Queue
import asyncio

@dataclass
class Sequence:
    """一个生成序列"""
    seq_id: str
    prompt_tokens: List[int]
    output_tokens: List[int] = field(default_factory=list)
    status: str = "waiting"  # waiting, running, completed, aborted
    blocks: List[int] = field(default_factory=list)  # KV cache blocks

    @property
    def is_finished(self) -> bool:
        return self.status in ("completed", "aborted")

    @property
    def total_tokens(self) -> int:
        return len(self.prompt_tokens) + len(self.output_tokens)


class ContinuousBatchingScheduler:
    """Continuous Batching 调度器"""

    def __init__(
        self,
        max_batch_size: int = 32,
        max_seq_len: int = 4096,
        block_size: int = 16,
        gpu_memory_utilization: float = 0.9,
    ):
        self.max_batch_size = max_batch_size
        self.max_seq_len = max_seq_len
        self.block_size = block_size
        self.gpu_memory_utilization = gpu_memory_utilization

        self.waiting_queue: Queue[Sequence] = Queue()
        self.running_sequences: Dict[str, Sequence] = {}
        self.block_manager = BlockManager(
            num_blocks=self.calculate_num_blocks(),
            block_size=block_size
        )

    def calculate_num_blocks(self) -> int:
        """根据显存计算可用 blocks 数量"""
        # 简化计算：假设每个 block 需要 1MB
        total_memory_mb = 80 * 1024  # 80GB
        available_memory = total_memory_mb * self.gpu_memory_utilization
        return int(available_memory)

    def add_request(self, seq_id: str, prompt_tokens: List[int]) -> Sequence:
        """添加新请求"""
        seq = Sequence(
            seq_id=seq_id,
            prompt_tokens=prompt_tokens
        )
        self.waiting_queue.put(seq)
        return seq

    def schedule(self) -> List[Sequence]:
        """调度迭代 - 返回当前 batch"""
        
        # 1. 清理已完成的 sequences
        completed = []
        for seq_id, seq in list(self.running_sequences.items()):
            if seq.is_finished:
                completed.append(seq)
                self._release_blocks(seq)
                del self.running_sequences[seq_id]

        # 2. 尝试调度新 sequences
        while (
            len(self.running_sequences) < self.max_batch_size
            and not self.waiting_queue.empty()
        ):
            seq = self.waiting_queue.get()
            
            # 分配 blocks
            num_blocks_needed = self._calculate_blocks_needed(seq)
            if self.block_manager.has_free_blocks(num_blocks_needed):
                blocks = self.block_manager.allocate(num_blocks_needed)
                seq.blocks = blocks
                seq.status = "running"
                self.running_sequences[seq.seq_id] = seq
            else:
                # 没有足够空间，放回队列
                self.waiting_queue.put(seq)
                break

        return list(self.running_sequences.values())

    def _calculate_blocks_needed(self, seq: Sequence) -> int:
        """计算需要的 blocks 数量"""
        total_len = seq.total_tokens
        return (total_len + self.block_size - 1) // self.block_size

    def _release_blocks(self, seq: Sequence):
        """释放 blocks"""
        for block_id in seq.blocks:
            self.block_manager.free(block_id)

    def step(self, outputs: Dict[str, int]) -> Dict[str, Sequence]:
        """
        执行一步推理
        outputs: {seq_id: generated_token}
        """
        for seq_id, token in outputs.items():
            if seq_id in self.running_sequences:
                seq = self.running_sequences[seq_id]
                seq.output_tokens.append(token)

                # 检查是否完成
                if token == EOS_TOKEN or seq.total_tokens >= self.max_seq_len:
                    seq.status = "completed"

        # 重新调度
        self.schedule()

        return self.running_sequences


class BlockManager:
    """KV Cache Block 管理器"""

    def __init__(self, num_blocks: int, block_size: int):
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.free_blocks: set = set(range(num_blocks))
        self.allocated: Dict[int, List[int]] = {}  # seq_id -> blocks

    def has_free_blocks(self, num_needed: int) -> bool:
        return len(self.free_blocks) >= num_needed

    def allocate(self, num_blocks: int) -> List[int]:
        blocks = []
        for _ in range(num_blocks):
            blocks.append(self.free_blocks.pop())
        return blocks

    def free(self, block_id: int):
        self.free_blocks.add(block_id)
```

### vLLM 中的 Continuous Batching

```python
# vLLM 的 continuous batching 是自动的
from vllm import LLM, SamplingParams

llm = LLM(
    model="meta-llama/Llama-2-7b-hf",
    gpu_memory_utilization=0.9,
    max_num_batched_tokens=8192,      # 单批次最大 token 数
    max_num_seqs=256,                 # 最大并发序列数
)

# 所有请求自动进行 continuous batching
outputs = llm.generate(prompts, sampling_params)

# 或者使用 OpenAI 兼容 API
# POST /v1/chat/completions
# 调度器自动处理并发请求
```

## 📊 性能对比

### Throughput 对比

| 策略 | 吞吐 (req/s) | 延迟 P50 (ms) | 延迟 P99 (ms) |
|------|-------------|---------------|---------------|
| Static Batch (size=1) | 10 | 100 | 150 |
| Static Batch (size=8) | 15 | 400 | 800 |
| **Continuous Batching** | **120** | **80** | **250** |

### 关键参数调优

```python
# 影响吞吐的参数
config = {
    # 批次大小
    "max_num_seqs": 256,           # 最大并发序列数
    
    # 显存利用
    "gpu_memory_utilization": 0.9, # GPU 显存使用比例
    
    # 调度粒度
    "max_num_batched_tokens": 8192, # 单批次最大 token 数
    "max_tokens": 1024,            # 单请求最大生成长度
    
    # KV Cache
    "block_size": 16,               # 越大越省显存但越碎片化
}
```

## 📋 命令速查

```bash
# 启动 vLLM (自动使用 Continuous Batching)
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-7b-hf \
    --gpu-memory-utilization 0.9 \
    --max-num-batched-tokens 8192

# 压力测试
python benchmark.py \
    --num-requests 1000 \
    --concurrency 64 \
    --model mymodel
```

## 📚 学习要点

1. **迭代级调度**：不是请求级，是 token 级
2. **动态加入**：完成的请求腾出空间，新请求立即加入
3. **Block Manager**：Paged Attention 的 KV cache 管理
4. **参数调优**：max_num_seqs 和 gpu_memory_utilization 关键

## 🔗 相关案例

- `vllm-inference` - vLLM 高吞吐推理
- `paged-attention` - PagedAttention 详解
- `speculative-decoding` - 投机解码

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
