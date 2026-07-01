<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Batch Inference 批处理推理

> 本案例详解 LLM 批处理推理：静态批处理、动态批处理、Prompt 缓存

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Batch Inference 演进                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Naive Batch (逐个推理):                                         │
│                                                                 │
│  Request 1: [███████████████████████████████] 2000ms            │
│  Request 2: [███████████████████████████████] 2000ms            │
│  Request 3: [███████████████████████████████] 2000ms            │
│                                                                 │
│  Total: 6000ms, Throughput: 0.5 req/s                           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Static Batching (静态批处理):                                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Batch [R1][R2][R3]                                      │   │
│  │                                                           │   │
│  │  问题: 必须等最长请求完成，短请求被阻塞                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Total: 2000ms, Throughput: 1.5 req/s                          │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Dynamic Batching (动态批处理):                                  │
│                                                                 │
│  Time 0ms:   [R1][R2][R3][R4]                                   │
│  Time 500ms: [R1 completed][R5 joins]                          │
│  Time 1000ms:[R2 completed][R6 joins]                           │
│                                                                 │
│  Total: 1500ms, Throughput: 4 req/s                             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Continuous Batching + Paged Attention:                         │
│                                                                 │
│  Iter 1: [R1][R2][R3][R4]  ──▶ token 生成                        │
│  Iter 2: [R1][R2][R3][R4]                                       │
│  Iter 3: [R1 done][R5][R6][R7]  ──▶ 新请求动态加入              │
│                                                                 │
│  GPU Utilization: 95%, Throughput: 10+ req/s                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 批处理的三种形态

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| Naive | 逐个处理 | 开发调试 |
| Static | 固定 batch，等待所有完成 | 离线批处理 |
| Dynamic | 动态加入，迭代调度 | 在线服务 |

### 2. 批处理核心实现

```python
class StaticBatcher:
    """静态批处理器"""

    def __init__(self, model, max_batch_size=8):
        self.model = model
        self.max_batch_size = max_batch_size
        self.pending_requests = []

    def add_request(self, prompt: str) -> str:
        """添加请求，返回 request_id"""
        request_id = str(uuid.uuid4())
        self.pending_requests.append({
            'id': request_id,
            'prompt': prompt,
            'status': 'pending'
        })
        return request_id

    def process_batch(self):
        """处理一个批次"""
        if len(self.pending_requests) < self.max_batch_size:
            return []

        # 等待达到批次大小
        batch = self.pending_requests[:self.max_batch_size]

        # Padding 到相同长度
        prompts = [r['prompt'] for r in batch]
        padded = self.pad_prompts(prompts)

        # 批量推理
        outputs = self.model.generate(padded)

        # 清理完成的请求
        self.pending_requests = self.pending_requests[self.max_batch_size:]

        return outputs

    def pad_prompts(self, prompts):
        """Padding 到相同长度"""
        max_len = max(len(p) for p in prompts)
        padded = []
        for p in prompts:
            padded.append(p + [PAD_TOKEN] * (max_len - len(p)))
        return padded
```

### 3. 混合批处理策略

```python
class HybridBatcher:
    """混合批处理：结合 Static 和 Dynamic"""

    def __init__(self, model, max_batch_size=32):
        self.model = model
        self.max_batch_size = max_batch_size

        # 短请求队列 (优先处理)
        self.short_queue = []
        # 长请求队列
        self.long_queue = []

        self.running = []
        self.max_wait_time = 0.1  # 100ms 超时

    def add_request(self, prompt, estimated_len):
        if estimated_len < 512:
            self.short_queue.append(prompt)
        else:
            self.long_queue.append(prompt)

    def schedule(self):
        """迭代调度"""
        now = time.time()

        # 合并短请求
        batch = []
        while (self.short_queue and len(batch) < self.max_batch_size // 2):
            batch.append(self.short_queue.pop(0))

        # 尝试加入长请求
        while (self.long_queue and len(batch) < self.max_batch_size):
            if time.time() - now > self.max_wait_time:
                break
            batch.append(self.long_queue.pop(0))

        if batch:
            return self.model.generate(batch)

        return []
```

## 📊 性能对比

| 策略 | 吞吐 (req/s) | 平均延迟 (s) | GPU 利用率 |
|------|-------------|--------------|------------|
| Naive | 0.5 | 2.0 | 30% |
| Static Batch | 2.0 | 2.5 | 60% |
| Dynamic Batch | 5.0 | 1.8 | 80% |
| **Continuous + Paged** | **15.0** | **1.5** | **95%** |

## 📚 学习要点

1. **静态批处理**：简单但浪费 GPU
2. **动态批处理**：迭代调度提高利用率
3. **混合策略**：长短请求分开处理
4. **Padding 优化**：减少无效计算

## 🔗 相关案例

- `continuous-batching` - Continuous Batching 详解
- `vllm-inference` - vLLM 高吞吐推理
- `streaming-inference` - 流式输出实现

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
