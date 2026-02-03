# KServe 请求日志记录 Demo

## 简介
本演示展示如何在 KServe 中为机器学习模型服务启用请求日志记录功能。通过配置 `requestLogging` 字段，可以将每个推理请求和响应记录到指定的日志收集系统（如 stdout 或外部日志服务），便于调试、审计和性能分析。

## 学习目标
- 理解 KServe 的 requestLogging 功能
- 掌握如何在 InferenceService 中启用请求日志记录
- 查看并验证生成的日志输出
- 了解日志结构和关键字段含义

## 环境要求
- Kubernetes 集群（版本 >=1.25）
- kubectl 命令行工具
- KServe v0.11.0 已安装（依赖 Knative Serving v1.10.0）
- 支持容器镜像拉取（如 Docker Hub 或私有仓库）

> 提示：可使用 Kind 或 Minikube 搭建本地测试环境

## 安装依赖的详细步骤

### 1. 安装本地 Kubernetes 环境（以 Minikube 为例）
```bash
minikube start --kubernetes-version=v1.25.0 --memory=8192 --cpus=4
```

### 2. 安装 Knative Serving
```bash
kubectl apply -f https://github.com/knative/serving/releases/download/v1.10.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/v1.10.0/serving-core.yaml
```

### 3. 安装 KServe v0.11.0
```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.11.0/kserve.yaml
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.11.0/kserve-runtimes.yaml
```

等待所有组件就绪：
```bash
kubectl wait --for=condition=Available -n knative-serving --all deployments
kubectl wait --for=condition=Available -n kserve-system --all deployments
```

## 文件说明
- `inferenceservice-with-logging.yaml`: 启用请求日志的 InferenceService 示例
- `inferenceservice-with-response-logging.yaml`: 同时记录请求和响应体的高级配置
- `test-request.sh`: 发送测试推理请求的脚本

## 逐步实操指南

### 步骤 1: 部署启用请求日志的服务
```bash
kubectl apply -f inferenceservice-with-logging.yaml
```

**预期输出**：
```bash
inferenceservice.serving.kserve.io/simple-model created
```

### 步骤 2: 等待服务就绪
```bash
kubectl wait --for=condition=Ready inferenceservice/simple-model --timeout=600s
```

### 步骤 3: 发送测试请求
```bash
./test-request.sh
```

### 步骤 4: 查看日志
```bash
# 获取预测器 Pod 名称
export POD=$(kubectl get pods -l=server-name=simple-model-predictor -o jsonpath='{.items[0].metadata.name}')

# 查看日志
kubectl logs $POD -c kserve-container
```

**预期输出**（部分）：
```json
{
  "level": "info",
  "ts": "2023-10-01T12:00:00Z",
  "logger": "request-logger",
  "msg": "Incoming request",
  "method": "POST",
  "url": "/v1/models/simple-model:predict",
  "requestBody": "{\"instances\": [1.0, 2.0]}",
  "responseStatus": 200
}
```

## 代码解析

### `inferenceservice-with-logging.yaml`
- `.spec.predictor.componentSpecs.logger`：定义日志记录器配置
- `url`：日志输出目标，此处为 stdout（默认）
- `mode`：设置为 `RequestResponse` 可记录完整请求/响应

### `inferenceservice-with-response-logging.yaml`
- 启用了 `responseBody: true`，用于捕获模型返回结果
- 适用于需要审计或调试模型输出的场景

### `test-request.sh`
- 使用 `curl` 向 KServe 服务发送标准 JSON 推理请求
- 目标地址通过 `simple-model.kserve-test.example.com` 虚拟主机访问（需确保 DNS 或 Hosts 配置正确）

## 预期输出示例
见上文“查看日志”部分，日志将以结构化 JSON 格式输出，包含时间戳、请求路径、状态码等信息。

## 常见问题解答

**Q: 日志没有输出？**
A: 确保 Pod 已完全启动，并检查是否使用了正确的容器名 (`kserve-container`) 查看日志。

**Q: 如何将日志发送到外部系统（如 Fluentd）？**
A: 修改 `logger.url` 为外部 HTTP 接收端点，例如 `http://fluentd.logging.svc.cluster.local`。

**Q: 是否会影响性能？**
A: 是的，尤其是记录响应体时。建议在生产环境中按需开启，并结合采样率控制（KServe 尚未原生支持采样，需自定义实现）。

## 扩展学习建议
- 结合 Prometheus 和 Grafana 实现指标+日志联合分析
- 使用 OpenTelemetry 进行分布式追踪
- 配置日志轮转与保留策略
- 探索 KServe 的批量预测与异步推理日志模式