# 大语言模型运维实战演示

## 🎯 学习目标

通过本案例你将掌握：
- 大语言模型的部署和管理策略
- 模型版本控制和A/B测试
- 性能监控和资源优化
- 模型安全和访问控制

## 🛠️ 环境准备

### 系统要求
- Kubernetes集群（推荐1.20+）
- Docker环境
- 至少64GB内存的节点用于模型部署

### 依赖安装
```bash
# Kubernetes工具
kubectl cluster-info
helm version

# 模型服务工具
pip install transformers accelerate
pip install kserve knative  # KFServing/Knative
```

## 📁 项目结构

```
llm-ops-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── manifests/                         # Kubernetes资源定义
│   ├── deployment.yaml                # 模型部署定义
│   ├── service.yaml                   # 服务暴露定义
│   ├── ingress.yaml                   # 流量入口定义
│   └── hpa.yaml                       # 水平伸缩定义
├── scripts/                           # 运维脚本
│   ├── deploy_model.sh                # 模型部署脚本
│   ├── scale_model.sh                 # 模型伸缩脚本
│   ├── backup_model.sh                # 模型备份脚本
│   └── monitor_model.py               # 模型监控脚本
├── configs/                           # 配置文件
│   ├── model_serving_config.yaml      # 模型服务配置
│   ├── resource_config.yaml           # 资源配置
│   └── security_config.yaml           # 安全配置
├── monitoring/                        # 监控配置
│   ├── prometheus_rules.yaml          # 监控规则
│   ├── grafana_dashboard.json         # 监控面板
│   └── alerts.yaml                    # 告警配置
├── tests/                             # 测试配置
│   ├── load_test.py                   # 负载测试
│   ├── chaos_test.py                  # 混沌测试
│   └── security_test.py               # 安全测试
└── docs/                              # 文档
    ├── deployment_guide.md             # 部署指南
    ├── scaling_strategies.md           # 伸缩策略
    └── security_best_practices.md      # 安全最佳实践
```

## 🚀 快速开始

### 步骤1：环境准备

```bash
# 验证Kubernetes集群
kubectl cluster-info
kubectl get nodes

# 安装KFServing（可选）
kubectl apply -f https://github.com/kserve/kserve/releases/latest/download/kserve.yaml
kubectl apply -f https://github.com/kserve/kserve/releases/latest/download/kserve-runtimes.yaml
```

### 步骤2：部署模型服务

```bash
# 部署模型服务
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
kubectl apply -f manifests/ingress.yaml

# 验证部署
kubectl get pods
kubectl logs -l app=llm-model
```

### 步骤3：配置监控

```bash
# 部署监控组件
kubectl apply -f monitoring/prometheus_rules.yaml
kubectl apply -f monitoring/alerts.yaml
```

## 🔍 代码详解

### 核心概念解析

#### 1. Kubernetes部署配置
```yaml
# manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-model
spec:
  replicas: 2
  selector:
    matchLabels:
      app: llm-model
  template:
    metadata:
      labels:
        app: llm-model
    spec:
      containers:
      - name: model-server
        image: ghcr.io/huggingface/text-generation-inference:latest
        ports:
        - containerPort: 80
        env:
        - name: MODEL_ID
          value: "facebook/opt-350m"
        - name: MAX_INPUT_LENGTH
          value: "1024"
        resources:
          requests:
            memory: "16Gi"
            nvidia.com/gpu: 1
          limits:
            memory: "32Gi"
            nvidia.com/gpu: 1
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 300
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 60
          periodSeconds: 10
```

#### 2. 实际应用示例

##### 场景1：自动伸缩配置
```yaml
# 水平Pod伸缩 (HPA)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-model-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-model
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

##### 场景2：A/B测试部署
```yaml
# 使用Argo Rollouts进行A/B测试
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: llm-model-rollout
spec:
  replicas: 4
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 2m}
      - setWeight: 40
      - pause: {duration: 2m}
      - setWeight: 60
      - pause: {duration: 2m}
      - setWeight: 80
      - pause: {duration: 2m}
  template:
    spec:
      containers:
      - name: model-server
        image: ghcr.io/huggingface/text-generation-inference:latest
        env:
        - name: MODEL_ID
          value: "facebook/opt-350m"
```

## 🧪 验证测试

### 测试1：部署验证
```bash
#!/bin/bash
# 验证模型部署
echo "=== 大语言模型部署验证 ==="

# 检查Pod状态
echo "检查Pod状态..."
kubectl get pods -l app=llm-model

# 检查服务状态
echo "检查服务状态..."
kubectl get svc llm-model-service

# 测试模型API
echo "测试模型API..."
kubectl port-forward svc/llm-model-service 8080:80 &
PORT_FORWARD_PID=$!

sleep 10  # 等待端口转发建立

# 发送测试请求
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "Explain artificial intelligence in simple terms",
    "parameters": {
      "max_new_tokens": 50,
      "temperature": 0.7
    }
  }'

# 清理端口转发
kill $PORT_FORWARD_PID

echo "✅ 部署验证完成"
```

### 测试2：性能监控验证
```python
#!/usr/bin/env python
# 验证性能监控
import requests
import time
import json

def test_performance_monitoring():
    print("=== 性能监控验证 ===")
    
    # 模拟负载
    url = "http://localhost:8080/generate"  # 假设服务在本地运行
    payload = {
        "inputs": "Explain artificial intelligence in simple terms",
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.7
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 发送多个请求以生成监控数据
    start_time = time.time()
    request_count = 10
    
    for i in range(request_count):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"请求 {i+1} 成功")
            else:
                print(f"请求 {i+1} 失败: {response.status_code}")
        except Exception as e:
            print(f"请求 {i+1} 异常: {e}")
        
        time.sleep(0.5)  # 控制请求频率
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"✅ 性能监控验证完成")
    print(f"总请求数: {request_count}")
    print(f"总耗时: {total_time:.2f} 秒")
    print(f"平均响应时间: {total_time/request_count:.2f} 秒")

if __name__ == "__main__":
    test_performance_monitoring()
```

## ❓ 常见问题

### Q1: 如何处理模型部署的GPU资源管理？
**解决方案**：
```yaml
# GPU资源管理最佳实践
"""
1. 资源请求和限制: 明确定义GPU和内存需求
2. 节点亲和性: 将模型部署到特定GPU节点
3. 污点和容忍: 确保GPU节点专用于模型推理
4. 资源配额: 控制GPU资源使用量
"""
```

### Q2: 如何实现模型的蓝绿部署？
**解决方案**：
```yaml
# 使用Service和Deployment实现蓝绿部署
apiVersion: v1
kind: Service
metadata:
  name: llm-model-service
spec:
  selector:
    app: llm-model
    version: v1  # 或 v2，切换流量
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

## 📚 扩展学习

### 相关技术
- **KFServing**: Kubernetes原生模型服务
- **Seldon Core**: 机器学习模型部署平台
- **Knative**: 无服务器容器平台
- **Argo Rollouts**: Kubernetes渐进式交付

### 进阶学习路径
1. 掌握云原生AI平台架构
2. 学习MLOps最佳实践
3. 理解模型治理和合规性
4. 掌握自动化运维和监控

### 企业级应用场景
- 多模型管理平台
- 模型版本控制和回滚
- A/B测试和灰度发布
- 模型性能监控和告警

---
> **💡 提示**: 大语言模型运维是确保模型在生产环境中稳定、高效运行的关键，需要综合考虑部署、监控、安全、成本等多个维度。