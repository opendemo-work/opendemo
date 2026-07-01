# KServe 模型监控 Demo

## 简介
本演示展示了如何在 Kubernetes 上为 KServe 部署的机器学习模型启用基本的模型监控功能。通过集成 Prometheus 和 KServe 的指标导出功能，我们可以收集推理请求延迟、调用频率和错误率等关键性能指标。

## 学习目标
- 理解 KServe 如何暴露模型服务指标
- 学会配置 Prometheus 抓取 KServe 推理服务的自定义指标
- 掌握基于 Prometheus 的模型行为监控基础方法

## 环境要求
- Kubernetes 集群（v1.25+）
- kubectl 已配置并连接到集群
- KServe v0.10.0 已安装
- Knative v1.10+ 已部署
- Helm v3+（用于安装 Prometheus）
- 网络访问权限：能够拉取公开镜像（如 prom/prometheus）

## 安装依赖步骤

1. **安装 KServe**（若未安装）：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
export VERSION=v0.10.0
kubectl apply -f https://github.com/kserve/kserve/releases/download/${VERSION}/kserve.yaml
kubectl apply -f https://github.com/kserve/kserve/releases/download/${VERSION}/kserve-runtimes.yaml
```

2. **安装 Prometheus（使用 Helm）**：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
```

3. 等待 Prometheus 启动：
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
kubectl get pods -n monitoring
# 预期输出包含 'prometheus-server-...' 并处于 Running 状态
```

## 文件说明
- `inference-service.yaml`：定义一个 KServe InferenceService 示例，启用了指标导出
- `prometheus-configmap.yaml`：配置 Prometheus 抓取 KServe 服务指标的 Job
- `port-forward.sh`：本地端口转发脚本，便于访问 Prometheus UI

## 逐步实操指南

### 第一步：部署 KServe 模型服务
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f inference-service.yaml
```

预期输出：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
inferenceservice.serving.kserve.io/sklearn-iris created
```

等待服务就绪：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl wait --for=condition=Ready inferenceservice/sklearn-iris --timeout=300s
```

### 第二步：配置 Prometheus 抓取规则
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f prometheus-configmap.yaml
```

重启 Prometheus Server 以加载新配置：
🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
kubectl delete pod -n monitoring -l app=prometheus,component=server
```

### 第三步：发送测试推理请求（触发指标生成）
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
SERVICE_HOST=$(kubectl get inferenceservice sklearn-iris -o jsonpath='{.status.url}' | cut -d '/' -f 3)
kubectl port-forward service/sklearn-iris-predictor 8080:80 &

# 发送请求
curl -H "Host: ${SERVICE_HOST}" http://localhost:8080/v1/models/sklearn-iris:predict -d '{"instances": [[1,2,3,4]]}'
```

### 第四步：查看 Prometheus 指标
运行端口转发：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl port-forward -n monitoring svc/prometheus-server 9090
```

打开浏览器访问：`http://localhost:9090`

在查询栏输入：
```promql
kserve_request_count{service_name="sklearn-iris"}
```
应看到计数随请求增加。

## 代码解析

### inference-service.yaml
- 使用 `tracing` 和 `metrics` 配置启用指标收集
- 设置 `logging` 字段确保访问日志输出，辅助调试
- 利用 Knative 服务自动扩缩特性，监控指标也反映副本变化

### prometheus-configmap.yaml
- 自定义 scrape job 名为 `kserve-metrics`
- 抓取目标指向 KServe 系统服务 `kserve-controller-metrics` 和用户模型的 `/metrics` 端点
- 使用 Kubernetes 服务发现机制动态识别目标

## 预期输出示例
在 Prometheus 中执行查询：
```promql
kserve_request_duration_milliseconds{le="100", service_name="sklearn-iris"}
```
返回类似：
```text
kserve_request_duration_milliseconds{...}  5
```
表示有5个请求响应时间小于100ms。

## 常见问题解答

**Q: Prometheus 抓不到 KServe 指标？**
A: 确保 KServe 控制器和推理服务都正常运行，并检查 Prometheus 的 target 页面（http://localhost:9090/targets）是否显示 `kserve-metrics` job 处于 UP 状态。

**Q: 指标中没有我的服务名称？**
A: 可能尚未收到任何请求。请先发送至少一次推理请求再查询。

**Q: 端口冲突？**
A: 修改 `port-forward` 命令中的本地端口号，例如 `9091:90`。

## 扩展学习建议
- 集成 Grafana 可视化 KServe 指标
- 配置告警规则（如高错误率触发通知）
- 使用 OpenTelemetry 实现分布式追踪
- 探索 KServe 的数据漂移检测功能（需集成 Alibi Detect）

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/apply.sh
```

### 检查状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/check.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 Kubernetes 核心概念。

### 2. 适用场景

- 场景 1：开发与测试
- 场景 2：生产环境参考
- 场景 3：故障排查

## 💻 代码示例

### 基本命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
