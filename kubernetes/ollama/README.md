# Ollama LLM Deployment

Ollama本地大模型部署与管理演示。

## 什么是Ollama

Ollama是本地运行大语言模型的工具，支持多种开源模型：

```
Ollama架构:
┌─────────────────────────────────────────────────────────┐
│                   Ollama API                            │
│              (REST/gRPC接口)                            │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │  Llama  │  │  Mistral│  │  Gemma  │  │  Code   │   │
│  │   2     │  │         │  │         │  │ Llama   │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
├─────────────────────────────────────────────────────────┤
│              llama.cpp Runtime                          │
│              (GPU/CPU推理加速)                           │
├─────────────────────────────────────────────────────────┤
│              Model Storage                              │
│              (~/.ollama/models)                         │
└─────────────────────────────────────────────────────────┘
```

## 快速开始

```bash
# 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 启动服务
ollama serve

# 拉取模型
ollama pull llama2
ollama pull mistral
ollama pull codellama

# 运行模型
ollama run llama2

# API调用
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?"
}'
```

## Kubernetes部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
spec:
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        ports:
        - containerPort: 11434
        resources:
          limits:
            nvidia.com/gpu: 1  # GPU支持
        volumeMounts:
        - name: models
          mountPath: /root/.ollama
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: ollama-models
---
apiVersion: v1
kind: Service
metadata:
  name: ollama
spec:
  selector:
    app: ollama
  ports:
  - port: 11434
    targetPort: 11434
```

## 学习要点

1. 本地LLM运行原理
2. 模型量化与优化
3. GPU加速配置
4. API集成开发
5. 多模型管理
