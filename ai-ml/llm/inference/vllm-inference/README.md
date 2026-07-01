<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# vLLM 高吞吐量推理

> 本案例详解 vLLM 推理引擎的核心技术：PagedAttention、Continuous Batching、KV Cache 管理

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        vLLM 架构                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Request 1 ──┐                                                  │
│  Request 2 ──┼──▶ ┌─────────────────┐                          │
│  Request 3 ──┤    │   Scheduler     │                          │
│  ...         ──┤    │                 │                          │
│              │    │  ┌─────────────┐  │                          │
│              │    │  │ Block Manager│  │                          │
│              │    │  └─────────────┘  │                          │
│              │    └────────┬──────────┘                          │
│              │             │                                      │
│              │    ┌────────▼──────────┐                          │
│              │    │   CUDA Graphs      │                          │
│              │    └────────┬──────────┘                          │
│              │             │                                      │
│              │    ┌────────▼──────────┐                          │
│              │    │  PyTorch Model    │                          │
│              │    │  (with PagedAttn) │                          │
│              │    └───────────────────┘                          │
│              │             │                                      │
│              │    ┌─────────▼──────────┐                         │
│              │    │  KV Cache Manager   │                         │
│              │    │                      │                         │
│              │    │  ┌──┬──┬──┬──┬──┐  │                         │
│              │    │  │P0│P1│P2│P3│P4│  │ ◀─ Physical Blocks     │
│              │    │  └──┴──┴──┴──┴──┘  │                         │
│              │    │  ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲  │                         │
│              │    │  └───────────────┘  │                         │
│              │    │   Logical KV Blocks  │                         │
│              │    └──────────────────────┘                         │
│              │             │                                      │
│              └──────────────┼──────────────────────────────────────┘
│                             │
│                             ▼
│                    Generated Tokens
│
└─────────────────────────────────────────────────────────────────┘

PagedAttention 内存管理:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Logical KV Blocks (对用户可见)                                  │
│  ┌────────┬────────┬────────┬────────┐                         │
│  │ Block 0│ Block 1│ Block 2│ Block 3│  ...                   │
│  │ [0-15] │ [16-31]│ [32-47]│ [48-63]│                         │
│  └────────┴────────┴────────┴────────┘                         │
│                                                                 │
│  Physical KV Blocks (GPU 显存)                                  │
│  ┌────────┬────────┬────────┬────────┬────────┐               │
│  │ Block 3│ Block 7│ Block 1│ Block 5│ Block 0│               │
│  └────────┴────────┴────────┴────────┴────────┘               │
│     ▲         ▲         ▲         ▲         ▲                    │
│     │         │         │         │         │                    │
│     └─────────┴─────────┴─────────┴─────────┘                    │
│           通过 block_table 映射                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. PagedAttention

传统 KV Cache 管理的问题：
- 预分配的连续显存可能导致 Internal Fragmentation
- 不同请求的序列长度差异大，显存利用率低

**PagedAttention 解决方案：**
- 将 KV Cache 分成固定大小的 Block (如 16 tokens/block)
- 通过 Block Table 实现逻辑块到物理块的映射
- 类似操作系统内存管理的 Page Table 机制

### 2. Continuous Batching

传统 Batching 的问题：
- Static Batching：所有请求必须等最慢的完成
- 显存占用与最大序列长度成正比

**Continuous Batching 解决方案：**
- 在 token 级别进行动态批处理
- 当某个请求完成时，立即插入新请求
- 迭代级别调度，最大化 GPU 利用率

### 3. KV Cache 管理

```python
# vLLM 的 KV Cache 管理
class KVCacheManager:
    def __init__(self, num_blocks, block_size=16):
        self.num_blocks = num_blocks
        self.block_size = block_size
        
        # 物理块数组
        self.free_blocks = set(range(num_blocks))
        selfallocated_blocks = {}
        
        # Block table: {request_id: [physical_block_ids]}
        self.block_table = {}
        
    def allocate(self, request_id, num_tokens):
        """为请求分配 KV cache blocks"""
        num_blocks_needed = (num_tokens + self.block_size - 1) // self.block_size
        blocks = []
        
        for _ in range(num_blocks_needed):
            if not self.free_blocks:
                raise OutOfMemoryError()
            block_id = self.free_blocks.pop()
            blocks.append(block_id)
            
        self.block_table[request_id] = blocks
        return blocks
        
    def free(self, request_id):
        """释放请求占用的 blocks"""
        if request_id in self.block_table:
            for block_id in self.block_table[request_id]:
                self.free_blocks.add(block_id)
            del self.block_table[request_id]
```

## 💻 完整实现

### vLLM 服务器部署

```python
# server.py
from vllm import LLM, SamplingParams

# 初始化 vLLM 引擎
llm = LLM(
    model="meta-llama/Llama-2-7b-hf",
    tensor_parallel_size=2,        # 多 GPU 并行
    gpu_memory_utilization=0.9,   # GPU 显存使用比例
    max_model_len=4096,           # 最大序列长度
    trust_remote_code=True,
)

# 采样参数
sampling_params = SamplingParams(
    temperature=0.8,
    top_p=0.95,
    max_tokens=256,
)

# 单请求推理
outputs = llm.generate(["Hello, my name is", "The capital of France is"], sampling_params)
for output in outputs:
    print(f"Generated: {output.outputs[0].text}")

# 批量推理
prompts = [
    "Explain the theory of relativity:",
    "What is quantum entanglement?",
    "How does photosynthesis work?",
]
outputs = llm.generate(prompts, sampling_params)
```

### API 服务化

```python
# api_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vllm import LLM, SamplingParams
import uvicorn

app = FastAPI()

class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9

class GenerationResponse(BaseModel):
    text: str
    num_tokens: int

# 全局 LLM 实例
llm = None

@app.on_event("startup")
async def startup():
    global llm
    llm = LLM(
        model="meta-llama/Llama-2-7b-hf",
        tensor_parallel_size=1,
        gpu_memory_utilization=0.85,
    )

@app.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    sampling_params = SamplingParams(
        temperature=request.temperature,
        top_p=request.top_p,
        max_tokens=request.max_tokens,
    )
    
    outputs = llm.generate([request.prompt], sampling_params)
    
    if not outputs:
        raise HTTPException(status_code=500, detail="Generation failed")
        
    return GenerationResponse(
        text=outputs[0].outputs[0].text,
        num_tokens=outputs[0].outputs[0].token_ids.__len__()
    )

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 自定义模型集成

```python
# custom_model.py
from vllm import LLM, SamplingParams
from vllm.model_loader import load_tensor_from_bin

# 加载自定义模型
llm = LLM(
    model="/path/to/your/model",
    tokenizer="your-tokenizer",
    tensor_parallel_size=4,
    max_model_len=8192,
    dtype="bfloat16",
    trust_remote_code=True,
)

# 使用自定义 chat template
sampling_params = SamplingParams(
    prompt="<|system|>
You are a helpful assistant.
<|user|>
What is the meaning of life?<|end|>
<|assistant|>",
    temperature=0.7,
    stop=["<|end|>", "<|user|>"],
)
```

## 📊 性能对比

### Throughput 对比 (Throughput vs. Latency)

| 引擎 | Throughput (req/s) | Latency P50 (ms) | Latency P99 (ms) |
|------|-------------------|------------------|------------------|
| HuggingFace (naive) | 10 | 500 | 2000 |
| Text Generation Inference | 45 | 180 | 600 |
| **vLLM** | **120** | **80** | **250** |

### 显存效率

| 配置 | 序列长度 | 最大并发 | 显存占用 |
|------|----------|----------|----------|
| 7B 模型 (FP16) | 2048 | 16 | 28GB |
| 7B 模型 (FP16) + vLLM | 2048 | **64** | 28GB |

## 📋 命令速查

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 启动 vLLM 服务器
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-7b-hf \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.9

# OpenAI 兼容 API
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "meta-llama/Llama-2-7b-hf", "prompt": "Hello", "max_tokens": 50}'

# 运行 Benchmark
python -m vllm.benchmarks.chatbot_arena

# 查看服务器状态
curl http://localhost:8000/v1/models
```

## 📚 学习要点

1. **PagedAttention 核心**：类 OS 分页的 KV Cache 管理
2. **Continuous Batching**：迭代级调度，最大化 GPU 利用率
3. **CUDA Graphs**：减少 kernel 启动开销
4. **量化集成**：支持 FP8、INT8、INT4 量化

## 🔗 相关案例

- `tgi-deployment` - Text Generation Inference 部署
- `continuous-batching` - Continuous Batching 详解
- `speculative-decoding` - 投机解码加速
- `int4-quantization` - INT4 量化推理

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
