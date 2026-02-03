# Kubernetes Prometheus 集成演示

## 简介
本演示展示了如何在 Kubernetes 集群中通过 Prometheus Operator 和 ServiceMonitor 实现对自定义应用的监控。包含部署 Prometheus、暴露应用指标以及配置自动发现监控目标。

## 学习目标
- 理解 Prometheus 在 Kubernetes 中的工作机制
- 掌握使用 Prometheus Operator 管理监控组件
- 学会使用 ServiceMonitor 自动发现监控目标
- 验证应用指标是否被正确采集

## 环境要求
- kubectl v1.20 或更高版本
- Helm v3.5+（用于安装 Prometheus Operator）
- 一个运行中的 Kubernetes 集群（Minikube、Kind、EKS、GKE 等均可）
- bash shell（支持 Windows WSL、macOS、Linux）

## 安装依赖步骤

1. 安装 kubectl：
   ```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   chmod +x kubectl
   sudo mv kubectl /usr/local/bin/
   ```

2. 安装 Helm：
   ```bash
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

3. 启动本地集群（如使用 Kind）：
   ```bash
   kind create cluster --name prom-demo
   ```

## 文件说明
- `prometheus-operator.yaml`: 使用 Helm 部署 Prometheus Operator
- `example-app.yaml`: 一个模拟的 HTTP 应用，暴露 Prometheus 格式的指标
- `service-monitor.yaml`: 告诉 Prometheus Operator 如何发现并抓取应用指标

## 逐步实操指南

### 步骤 1: 部署 Prometheus Operator
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```

预期输出：
```
NAME: prometheus
NAMESPACE: monitoring
... installed successfully
```

等待所有 Pod 启动：
```bash
kubectl get pods -n monitoring -w
```

### 步骤 2: 部署示例应用
```bash
kubectl apply -f example-app.yaml
```

预期输出：
```
service/example-app created
deployment.apps/example-app created
```

### 步骤 3: 创建 ServiceMonitor
```bash
kubectl apply -f service-monitor.yaml
```

预期输出：
```
servicemonitor.monitoring.coreos.com/example-app-monitor created
```

### 步骤 4: 访问 Prometheus UI
```bash
kubectl port-forward -n monitoring svc/prometheus-operated 9090
```

打开浏览器访问 `http://localhost:9090`，在查询栏输入 `http_requests_total`，应能看到指标数据。

## 代码解析

### example-app.yaml
- 部署了一个简单应用，监听 `/metrics` 路径返回 Prometheus 格式指标
- 设置了正确的端口名称 `metrics`，这是 ServiceMonitor 发现的关键

### service-monitor.yaml
- 指定选择器匹配 `app: example-app` 的 Service
- 目标端口为 `metrics`，与 Service 一致
- 必须位于同一命名空间或被 Prometheus 实例配置扫描

## 预期输出示例
在 Prometheus 查询页面执行 `http_requests_total` 应返回类似：
```
http_requests_total{app="example-app", endpoint="metrics", instance="10.244.0.6:8080", job="default/example-app-monitor", namespace="default", pod="example-app-7c6b9d974-xpz8j", service="example-app"}	36
```

## 常见问题解答

**Q: Prometheus 中看不到目标？**
A: 检查 ServiceMonitor 的命名空间和选择器是否匹配，确保 Prometheus 实例配置了正确的 `serviceMonitorSelector`。

**Q: 指标路径无法访问？**
A: 确保应用容器实际暴露了 `/metrics` 并返回 200，可通过 `kubectl port-forward` 测试。

**Q: 如何跨命名空间监控？**
A: 在 Prometheus CRD 中设置 `serviceMonitorNamespaceSelector: {}` 允许所有命名空间。

## 扩展学习建议
- 学习 Alertmanager 配置告警规则
- 使用 Prometheus Recording Rules 优化查询性能
- 探索 Grafana 可视化仪表板集成
- 实践 PodMonitor 监控无 Service 的工作负载