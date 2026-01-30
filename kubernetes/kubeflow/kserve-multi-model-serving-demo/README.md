# KServe 多模型服务演示

## 简介
本演示展示了如何使用 KServe 在 Kubernetes 集群中部署和管理多个机器学习模型，实现高效的多模型推理服务。KServe 是一个为 Kubernetes 构建的高性能、可扩展的模型服务框架，支持 TensorFlow、PyTorch、ONNX 等多种框架。

## 学习目标
- 理解 KServe 的基本架构和核心概念
- 掌握如何定义和部署多个机器学习模型
- 学会通过 REST API 调用模型进行推理
- 了解多模型服务的最佳实践

## 环境要求
- Python 3.9 或更高版本
- Kubernetes 集群（v1.25+）
- kubectl 已配置并连接到集群
- Istio 1.18+（KServe 依赖）
- KServe v0.11.0 已安装

## 安装依赖步骤
1. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

2. 确保已安装 Istio 和 KServe：
```bash
# 安装 Istio（如果尚未安装）
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH="$PWD/bin:$PATH"
ikt install --set profile=demo -y

# 安装 KServe
git clone https://github.com/kserve/kserve
kubectl apply -f kserve/config/rbac
kubectl apply -f kserve/config/manager
```

## 文件说明
- `inference-service-multi.yaml`: 定义两个模型（sklearn 和 xgboost）的服务配置
- `predict-request.py`: 发送预测请求的客户端脚本
- `requirements.txt`: Python 依赖声明文件

## 逐步实操指南

### 步骤 1: 应用 KServe 模型服务配置
```bash
kubectl apply -f inference-service-multi.yaml
```

**预期输出**:
```
service.serving.kserve.io/multi-model-service created
inferenceservice.serving.kserve.io/sklearn-model created
inferenceservice.serving.kserve.io/xgboost-model created
```

### 步骤 2: 检查服务状态
```bash
kubectl get inferenceservices
```

**预期输出**:
```
NAME            URL                                        READY   AGE
sklearn-model   http://sklearn-model.default.example.com   True    2m
xgboost-model   http://xgboost-model.default.example.com   True    2m
```

### 步骤 3: 发送预测请求
```bash
python predict-request.py
```

**预期输出**:
```
Sklearn 模型响应: {'predictions': [1, 0]}
XGBoost 模型响应: {'predictions': [0.823, 0.177]}
```

## 代码解析

### `inference-service-multi.yaml`
- 使用 `InferenceService` CRD 定义模型服务
- 每个模型指定存储路径（支持 S3、GCS、HTTP 等）
- 自动创建 Istio VirtualService 实现路由
- 支持自动扩缩容（Knative）

### `predict-request.py`
- 使用标准 HTTP 请求调用 KServe 端点
- 遵循 KServe v2 推理协议格式
- 包含正确的 headers（'Content-Type': 'application/json'）

## 预期输出示例
```
Sklearn 模型响应: {'predictions': [1, 0]}
XGBoost 模型响应: {'predictions': [0.823, 0.177]}
```

## 常见问题解答

**Q: 如何查看模型日志？**
A: 使用命令 `kubectl logs -l serving.kserve.io/inferenceservice=<model-name>`

**Q: 服务一直处于未就绪状态怎么办？**
A: 检查镜像拉取是否成功，确认模型存储路径可访问，使用 `kubectl describe inferenceservice <name>` 查看事件

**Q: 如何更新模型？**
A: 修改 YAML 文件中的镜像或存储路径，重新应用即可触发滚动更新

## 扩展学习建议
- 尝试添加更多类型的模型（如 PyTorch、TensorFlow）
- 配置模型监控和指标收集（Prometheus + Grafana）
- 实现 A/B 测试或多臂赌博机策略
- 探索 KServe 的 Transformer 模式进行预处理/后处理
- 集成 KFServing 协议兼容的客户端库