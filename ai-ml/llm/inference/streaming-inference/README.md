# Streaming Inference 流式输出

> 本案例详解 LLM 流式输出：Server-Sent Events、Token 流式生成、前端实现

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Streaming Inference 流程                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  传统方式 (等待完成):                                            │
│                                                                 │
│  Client ──── Request ────▶ Server                               │
│         ◀── Full Response ────                                 │
│                                                                 │
│  等待时间: 2-5 秒                                               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Streaming (流式输出):                                           │
│                                                                 │
│  Client ──── Request ────▶ Server                               │
│         ◀── token1 ──────                                       │
│         ◀── token2 ──────                                       │
│         ◀── token3 ──────  (SSE)                                │
│         ◀── token4 ──────                                       │
│         ◀── [DONE] ─────                                        │
│                                                                 │
│  首 Token 延迟: <100ms                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

WebSocket / SSE 通信协议:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Server-Sent Events (SSE) 格式:                                 │
│                                                                 │
│  data: {"token": "Hello", "done": false}                       │
│                                                                 │
│  data: {"token": " world", "done": false}                      │
│                                                                 │
│  data: {"token": "!", "done": true}                            │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  浏览器端处理:                                                   │
│                                                                 │
│  const eventSource = new EventSource('/generate');             │
│  eventSource.onmessage = (event) => {                           │
│      const data = JSON.parse(event.data);                       │
│      if (data.done) {                                           │
│          eventSource.close();                                   │
│      } else {                                                   │
│          displayToken(data.token);                              │
│      }                                                          │
│  };                                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 为什么需要流式输出

- **用户体验**：首 token <100ms vs 等待 2-5s
- **交互感**：实时看到生成进度
- **资源释放**：早生成的 token 可先消费

### 2. 后端实现

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

async def generate_stream(prompt: str, model):
    """流式生成"""
    tokenizer = model.tokenizer
    input_ids = tokenizer(prompt).input_ids

    generated = []
    max_new_tokens = 100

    for _ in range(max_new_tokens):
        # 单步推理
        output = model.forward(torch.tensor([input_ids + generated]))
        next_token = output.logits[:, -1, :].argmax(dim=-1).item()

        if next_token == tokenizer.eos_token_id:
            yield json.dumps({"token": "", "done": True}) + "\n"
            break

        # 解码 token
        token_text = tokenizer.decode([next_token])
        generated.append(next_token)

        # 流式发送
        yield json.dumps({
            "token": token_text,
            "done": False,
            "complete": "".join(generated)
        }) + "\n"

        await asyncio.sleep(0.01)  # 模拟延迟

@app.post("/stream")
async def stream_generate(request: GenerateRequest):
    return StreamingResponse(
        generate_stream(request.prompt, model),
        media_type="text/event-stream"
    )
```

### 3. 前端实现

```python
# Python Client 示例
import requests
import json

def stream_generate(prompt):
    """流式调用示例"""
    response = requests.post(
        "http://localhost:8000/stream",
        json={"prompt": prompt},
        stream=True
    )

    for line in response.iter_lines():
        if line.startswith("data: "):
            data = json.loads(line[6:])
            print(data["token"], end="", flush=True)
            if data["done"]:
                print()  # 换行
                break

# JavaScript 前端示例
async function streamGenerate(prompt) {
    const response = await fetch('/stream', {
        method: 'POST',
        body: JSON.stringify({ prompt }),
        headers: { 'Content-Type': 'application/json' }
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        for (const line of text.split('\n')) {
            if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                document.getElementById('output').textContent += data.token;
            }
        }
    }
}
```

### 4. vLLM 流式输出

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-2-7b-hf")

# 流式生成
outputs = llm.generate(
    ["Hello, my name is"],
    SamplingParams(max_tokens=100),
    stream=True
)

for output in outputs:
    # output 是一个生成器
    print(output.outputs[0].text, end="", flush=True)
```

## 📊 性能对比

| 方式 | 首 Token 延迟 | 用户感知延迟 | 完整生成 |
|------|--------------|--------------|----------|
| 传统 | 2000ms | 2000ms | 2000ms |
| **Streaming** | 50ms | 50ms | 2050ms |

## 📚 学习要点

1. **SSE 协议**：基于 HTTP 的简单流协议
2. **流式解码**：yield 每步结果
3. **前端处理**：EventSource 或 fetch 流式读取
4. **背压控制**：消费者慢时自动限速

## 🔗 相关案例

- `vllm-inference` - vLLM 高吞吐推理
- `batch-inference` - Batch 推理优化
- `tgi-deployment` - TGI 部署
