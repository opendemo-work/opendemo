# Ollama 基础演示

## 概述

Ollama是一个简单易用的工具，用于在本地运行大型语言模型（LLM）。它提供了一个轻量级、功能强大的方式来运行、自定义和共享模型。Ollama支持多种流行的开源模型，如Llama 2、Llama 3、Mixtral等，可以在Kubernetes环境中进行部署和管理。

## 架构

Ollama架构主要包括以下几个核心组件：

- **Ollama Server**：运行模型的服务端，处理API请求
- **模型管理器**：负责模型的下载、加载和卸载
- **API接口**：提供REST API和库接口供应用程序调用
- **资源管理器**：管理GPU/CPU资源分配

## 快速开始

### 环境准备

确保您的系统满足以下要求：
- Kubernetes v1.19+
- GPU支持（可选，取决于模型需求）
- 至少8GB可用内存

### 安装 Ollama

```bash
# 在 Kubernetes 集群中部署 Ollama
kubectl apply -f ollama-deployment.yaml
```

### 使用示例

```bash
# 检查 Ollama 服务状态
kubectl get pods -n ollama-system

# 访问 Ollama API
curl http://<ollama-service-ip>:11434/api/tags

# 运行模型（示例）
curl -X POST http://<ollama-service-ip>:11434/api/generate \
  -H "Content-Type: content-type: application/json" \
  -d '{
    "model": "llama3",
    "prompt": "为什么天空是蓝色的？",
    "stream": false
  }'
```

## 示例配置

### Ollama 服务部署配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: ollama-system
  labels:
    app: ollama
spec:
  replicas: 1
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
        env:
        - name: OLLAMA_HOST
          value: "0.0.0.0"
        - name: OLLAMA_PORT
          value: "11434"
        - name: OLLAMA_NUM_PARALLEL
          value: "1"
        - name: OLLAMA_MAX_LOADED_MODELS
          value: "1"
        resources:
          requests:
            memory: "8Gi"
            cpu: "2000m"
          limits:
            memory: "16Gi"
            cpu: "4000m"
            # 如果有GPU支持，取消下面的注释
            # nvidia.com/gpu: 1
        volumeMounts:
        - name: models
          mountPath: /root/.ollama
        livenessProbe:
          httpGet:
            path: /api/tags
            port: 11434
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/tags
            port: 11434
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: ollama-models-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: ollama-service
  namespace: ollama-system
spec:
  selector:
    app: ollama
  ports:
    - protocol: TCP
      port: 80
      targetPort: 11434
      nodePort: 31434
  type: NodePort
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ollama-ingress
  namespace: ollama-system
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: ollama.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ollama-service
            port:
              number: 80
```

### Ollama 模型管理配置

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: ollama-model-loader
  namespace: ollama-system
spec:
  template:
    spec:
      containers:
      - name: model-loader
        image: ollama/ollama:latest
        command: ["/bin/sh", "-c"]
        args:
        - |
          # 拉取模型
          ollama pull llama3
          ollama pull mistral
          
          # 检查可用模型
          ollama list
        env:
        - name: OLLAMA_HOST
          value: "ollama-service.ollama-system.svc.cluster.local"
        volumeMounts:
        - name: models
          mountPath: /root/.ollama
      restartPolicy: Never
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: ollama-models-pvc
```

## 支持的模型

Ollama支持多种流行的开源模型：

- **Llama系列**: llama2, llama3, codellama
- **Mistral**: mistral, mixtral
- **其他模型**: phi, gemma, qwen等

### 模型拉取示例

```bash
# 拉取模型到 Ollama 服务
ollama pull llama3
ollama pull mistral
ollama pull phi

# 列出本地模型
ollama list

# 运行对话
ollama run llama3
```

## API 使用示例

### 获取模型列表

```bash
curl http://<ollama-service-ip>:11434/api/tags
```

### 生成文本

```bash
curl -X POST http://<ollama-service-ip>:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "prompt": "解释量子计算的基本概念",
    "stream": false
  }'
```

### 创建模型

```bash
curl -X POST http://<ollama-service-ip>:11434/api/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "mymodel",
    "modelfile": "FROM llama3\nSYSTEM You are a helpful assistant"
  }'
```

## 使用场景

1. **本地AI开发**：在本地环境中进行AI模型实验和开发
2. **模型测试**：测试不同模型的性能和准确性
3. **私有部署**：在私有环境中部署模型，确保数据安全
4. **教育研究**：用于学术研究和教育目的
5. **原型开发**：快速构建AI应用原型

## 最佳实践

- 根据模型大小合理分配内存和计算资源
- 使用持久化存储保存模型文件
- 启用健康检查确保服务可用性
- 使用GPU加速提升推理性能
- 实施适当的访问控制和安全措施

## 故障排除

### 服务无法启动

检查日志以确定问题：

```bash
kubectl logs -n ollama-system deployment/ollama
```

### 模型加载失败

确认有足够的磁盘空间和内存：

```bash
kubectl describe pod -n ollama-system -l app=ollama
```

### API调用超时

检查资源限制和网络连接：

```bash
kubectl top pod -n ollama-system -l app=ollama
```

## 扩展阅读

- [Ollama 官方文档](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama GitHub 仓库](https://github.com/ollama/ollama)
- [模型库](https://ollama.ai/library)
- [Kubernetes 最佳实践](https://kubernetes.io/docs/setup/best-practices/)