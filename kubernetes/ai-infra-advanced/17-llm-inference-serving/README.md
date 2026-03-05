# LLM推理服务

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **推理引擎**: vLLM, TensorRT-LLM, TGI

---

## 概述

大语言模型(LLM)推理服务是AI基础设施的关键应用场景，涵盖模型部署、推理优化、服务编排等内容。

---

## vLLM推理部署

### 单机部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-llama2-7b
  namespace: llm-serving
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm-llama2
  template:
    metadata:
      labels:
        app: vllm-llama2
    spec:
      containers:
        - name: vllm
          image: vllm/vllm-openai:latest
          args:
            - --model
            - /models/llama-2-7b-hf
            - --host
            - "0.0.0.0"
            - --port
            - "8000"
            - --tensor-parallel-size
            - "1"
            - --gpu-memory-utilization
            - "0.9"
          ports:
            - containerPort: 8000
          resources:
            limits:
              nvidia.com/gpu: 1
              memory: 24Gi
            requests:
              nvidia.com/gpu: 1
              memory: 16Gi
          volumeMounts:
            - name: model-storage
              mountPath: /models
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: llama2-models-pvc
```

### 多GPU分布式部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-llama2-70b
  namespace: llm-serving
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm-llama2-70b
  template:
    metadata:
      labels:
        app: vllm-llama2-70b
    spec:
      containers:
        - name: vllm
          image: vllm/vllm-openai:latest
          args:
            - --model
            - /models/llama-2-70b-hf
            - --tensor-parallel-size
            - "4"
            - --pipeline-parallel-size
            - "1"
            - --max-model-len
            - "4096"
            - --gpu-memory-utilization
            - "0.95"
          ports:
            - containerPort: 8000
          resources:
            limits:
              nvidia.com/gpu: 4
              memory: 128Gi
            requests:
              nvidia.com/gpu: 4
              memory: 96Gi
          volumeMounts:
            - name: model-storage
              mountPath: /models
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: llama2-70b-models-pvc
```

---

## KServe推理服务

### InferenceService部署

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llama2-7b
  namespace: llm-serving
  annotations:
    serving.kserve.io/autoscalerClass: hpa
    serving.kserve.io/metric: concurrency
    serving.kserve.io/target: "4"
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      storageUri: "s3://models/llama-2-7b-hf"
      resources:
        requests:
          nvidia.com/gpu: 1
          memory: 16Gi
        limits:
          nvidia.com/gpu: 1
          memory: 24Gi
```

### 多模型服务

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: multi-llm-serving
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      storageUri: "s3://models/"
      resources:
        requests:
          nvidia.com/gpu: 2
          memory: 48Gi
    multiModel:
      models:
        - name: llama-2-7b
          weight: 50
        - name: mistral-7b
          weight: 30
        - name: codellama-7b
          weight: 20
```

---

## 推理服务暴露

### Service配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vllm-service
  namespace: llm-serving
spec:
  type: ClusterIP
  selector:
    app: vllm-llama2
  ports:
    - port: 8000
      targetPort: 8000
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vllm-ingress
  namespace: llm-serving
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
spec:
  ingressClassName: nginx
  rules:
    - host: llm.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: vllm-service
                port:
                  number: 8000
```

---

## 自动扩缩容

### HPA配置

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-hpa
  namespace: llm-serving
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-llama2-7b
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: nvidia.com/gpu
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: vllm_num_requests_waiting
        target:
          type: AverageValue
          averageValue: "10"
```

---

## 推理性能优化

### 1. PagedAttention配置

```yaml
args:
  - --model
  - /models/llama-2-7b-hf
  - --block-size
  - "16"
  - --max-num-seqs
  - "256"
  - --max-model-len
  - "4096"
```

### 2. KV Cache优化

```yaml
args:
  - --gpu-memory-utilization
  - "0.95"
  - --swap-space
  - "4"
  - --max-num-batched-tokens
  - "8192"
```

### 3. 量化配置

```yaml
args:
  - --model
  - /models/llama-2-7b-hf
  - --quantization
  - awq
  - --load-format
  - awq
```

---

## 相关案例

- [LLM微调训练](../16-llm-finetuning/) - 模型微调
- [LLM量化压缩](../19-llm-quantization/) - 模型优化
- [向量数据库RAG](../20-vector-database-rag/) - RAG架构

---

**维护者**: OpenDemo Team | **许可证**: MIT
