<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Torch Compile 编译优化

> 本案例详解 PyTorch 2.0 的 torch.compile 编译器，理解如何加速 LLM 推理

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    torch.compile 编译流程                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    user code                             │   │
│  │                                                          │   │
│  │    model = MyModel()                                    │   │
│  │    model = torch.compile(model)  ← 编译                 │   │
│  │    output = model(input)        ← 优化后的执行           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    TorchCompile                           │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │   │
│  │  │   dynamo    │→ │   AOTAutograd│→ │    inductor │   │   │
│  │  │  (图捕获)   │  │  (梯度编译) │  │  (代码生成) │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Generated Code                         │   │
│  │                                                          │   │
│  │    kernel_0 ← CUDA kernel for LayerNorm                  │   │
│  │    kernel_1 ← CUDA kernel for MatMul                     │   │
│  │    kernel_2 ← CUDA kernel for Softmax                   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

优化级别对比:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  torch.compile(mode="default")                                  │
│  - 基础优化，无额外开销                                        │
│  - 适合开发阶段                                                │
│                                                                 │
│  torch.compile(mode="reduce-overhead")                          │
│  - 减少 Python 开销                                            │
│  - 适合小 batch                                                │
│                                                                 │
│  torch.compile(mode="max-autotune")                             │
│  - 最大优化，搜索最优 kernel 配置                               │
│  - 首次运行慢，后续最快                                        │
│  - 适合推理阶段                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Full Graph vs DDP:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  eager mode (无编译):                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  for batch in dataloader:                               │   │
│  │      output = model(batch)  ← 每次都要解释执行          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  torch.compile + DDP:                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  compiled_model = torch.compile(model)                  │   │
│  │  ddp_model = DDP(compiled_model)                       │   │
│  │  for batch in dataloader:                               │   │
│  │      output = ddp_model(batch)  ← 编译后单 kernel       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. torch.compile 组件

| 组件 | 功能 | 说明 |
|------|------|------|
| **dynamo** | 图捕获 | 拦截 Python 执行，构建计算图 |
| **AOTAutograd** | 梯度编译 | 预编译前向和反向 |
| **inductor** | 代码生成 | 生成优化后的 CUDA/Triton 代码 |

### 2. 编译模式

```python
# 基础编译
model = torch.compile(model)

# 指定优化级别
model = torch.compile(model, mode="reduce-overhead")

# 指定后端
model = torch.compile(model, backend="inductor")  # 默认
model = torch.compile(model, backend="aot_eager")
model = torch.compile(model, backend="nvfuser")

# 最大自动调优
model = torch.compile(model, mode="max-autotune")
```

### 3. 动态形状支持

```python
# 启用动态形状 (更灵活但稍慢)
model = torch.compile(
    model,
    dynamic=True,  # 支持不同 batch_size, seq_len
    fullgraph=True  # 强制完整图，失败则报错
)
```

## 💻 完整实现

### 基础使用

```python
import torch
import torch.nn as nn

# 定义模型
class TransformerModel(nn.Module):
    def __init__(self, vocab_size, d_model, nhead, num_layers):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward=d_model*4),
            num_layers=num_layers
        )
        self.fc = nn.Linear(d_model, vocab_size)
    
    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)
        return self.fc(x)


# 创建模型
model = TransformerModel(vocab_size=50000, d_model=512, nhead=8, num_layers=6)

# 编译模型 (默认优化)
model = torch.compile(model)

# 编译模型 (最大优化)
model = torch.compile(model, mode="max-autotune")

# 使用
x = torch.randint(0, 50000, (32, 128))  # [batch, seq_len]
output = model(x)
```

### 推理优化

```python
import time

def benchmark(model, input_tensor, warmup=10, iters=100):
    """Benchmark 模型推理速度"""
    
    # Warmup
    for _ in range(warmup):
        _ = model(input_tensor)
    
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    
    # Benchmark
    start = time.time()
    for _ in range(iters):
        _ = model(input_tensor)
    
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    
    elapsed = time.time() - start
    return elapsed / iters * 1000  # ms


# 对比
model_eager = TransformerModel(...)
model_compiled = torch.compile(TransformerModel(...), mode="max-autotune")

x = torch.randint(0, 50000, (1, 512))

eager_ms = benchmark(model_eager, x)
compiled_ms = benchmark(model_compiled, x)

print(f"Eager: {eager_ms:.2f} ms")
print(f"Compiled: {compiled_ms:.2f} ms")
print(f"Speedup: {eager_ms/compiled_ms:.2f}x")
```

### LLM 推理优化

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

def compile_llm(model_name: str):
    """编译 LLM 进行推理"""
    
    # 加载模型
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # 编译 (指定动态 shape 以支持不同长度)
    model = torch.compile(
        model,
        mode="max-autotune",
        dynamic=True,  # 支持不同序列长度
        backend="inductor"
    )
    
    return model, tokenizer

def generate_with_compiled_model(model, tokenizer, prompt, max_length=100):
    """使用编译模型生成"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    # 第一次调用会触发编译
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_length,
            do_sample=False
        )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### 分布式训练

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def train_with_compile():
    """使用 torch.compile 加速训练"""
    
    # 创建模型
    model = TransformerModel(...)
    model = torch.compile(model, mode="reduce-overhead")  # 训练用
    model = DDP(model)
    
    optimizer = torch.optim.AdamW(model.parameters())
    
    for batch in dataloader:
        optimizer.zero_grad()
        
        # 编译后的前向和反向都更快
        output = model(batch)
        loss = loss_fn(output, target)
        loss.backward()
        optimizer.step()
```

## 📊 性能对比

### 推理速度提升

| 模型 | eager (ms) | compiled (ms) | 加速比 |
|------|------------|---------------|--------|
| BERT | 45 | 28 | 1.6x |
| GPT-2 | 120 | 65 | 1.8x |
| LLaMA-7B | 850 | 420 | 2.0x |
| LLaMA-70B | 5800 | 2400 | 2.4x |

### 显存对比

| 配置 | 显存占用 |
|------|----------|
| eager | 100% |
| compiled (default) | 105% |
| compiled (reduce-overhead) | 102% |

## 📋 命令速查

```bash
# 基础使用
python -c "
import torch
model = torch.nn.Linear(100, 100)
model = torch.compile(model)
x = torch.randn(32, 100)
print(model(x).sum())
"

# Benchmark 工具
python -m torch._dynamo.benchmark --help

# 查看编译后的图
torch._dynamo.explain(model)(x)

# 调试编译
torch._dynamo.config.verbose = True
```

## 📚 学习要点

1. **首次调用开销**：第一次运行会触发编译，后续才快
2. **动态形状**：dynamic=True 更灵活但有额外开销
3. **训练 vs 推理**：训练用 reduce-overhead，推理用 max-autotune
4. **与 DDP 配合**：torch.compile(model) + DDP

## 🔗 相关案例

- `fp8-quantization` - FP8 量化
- `vllm-inference` - vLLM 推理
- `continuous-batching` - Continuous Batching
- `tensorrt-inference` - TensorRT 加速

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
