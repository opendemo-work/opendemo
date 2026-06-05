# Text Generation Inference (TGI) 部署

> 本案例详解 TGI (Text Generation Inference) 推理服务部署

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      TGI 架构                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HTTP Request                                                   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  API Layer                               │   │
│  │              (FastAPI + Uvicorn)                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Request Handler                             │   │
│  │         (Batching, Streaming, Metrics)                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Text Generation Pipeline                     │   │
│  │                                                          │   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐              │   │
│  │   │ Tokenizer│→│  Model  │→│ Detector│              │   │
│  │   └─────────┘  └─────────┘  └─────────┘              │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  CUDA Kernels                            │   │
│  │       Flash Attention │ KV Cache │ Sampling            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

TGI 关键特性:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ✅ Continuous Batching - 动态批处理                            │
│  ✅ Flash Attention - 高效注意力计算                            │
│  ✅ Paged Attention - KV Cache 优化                           │
│  ✅ Weight Streaming - 分片加载大模型                           │
│  ✅ Speculative Decoding - 投机解码                            │
│  ✅ Token Streaming - 流式输出                                  │
│  ✅ OpenAI Compatible - 兼容 OpenAI API                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 部署与使用

### Docker 部署

```bash
# 启动 TGI 服务
docker run --gpus all \
    -p 8080:80 \
    -v $PWD/data:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id meta-llama/Llama-2-7b-hf \
    --quantize bitsandbytes \
    --num-shard 1
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  tgi:
    image: ghcr.io/huggingface/text-generation-inference:latest
    ports:
      - "8080:80"
    volumes:
      - ./data:/data
    environment:
      - MODEL_ID=meta-llama/Llama-2-7b-hf
      - QUANTIZE=bitsandbytes
      - NUM_SHARD=1
      - MAX_INPUT_LENGTH=4096
      - MAX_TOTAL_TOKENS=8192
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### API 使用

```python
from openai import OpenAI

# TGI 兼容 OpenAI API
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"  # TGI 不需要 API key
)

# Chat Completions
response = client.chat.completions.create(
    model="meta-llama/Llama-2-7b-hf",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=256,
    temperature=0.7,
)

print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="meta-llama/Llama-2-7b-hf",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True,
    max_tokens=500
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="", flush=True)
```

### 生成参数

```python
# TGI 特有参数
generation_config = {
    # 标准参数
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    
    # TGI 特有
    "typical_p": 0.95,          # Typical acceptance
    "repetition_penalty": 1.1,   # 重复惩罚
    "frequency_penalty": 0.0,   # 频率惩罚
    "presence_penalty": 0.0,    # 存在惩罚
    "stop": ["\n", "User:"],    # 停止序列
}
```

## 📋 命令速查

```bash
# 启动 TGI
text-generation-router --model-id meta-llama/Llama-2-7b-hf

# 查看模型列表
curl http://localhost:3000/v1/models

# 健康检查
curl http://localhost:3000/health
```

## 🔗 相关案例

- `vllm-inference` - vLLM 推理
- `continuous-batching` - Continuous Batching
- `speculative-decoding` - 投机解码
