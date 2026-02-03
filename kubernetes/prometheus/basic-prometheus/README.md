# Kubernetes Prometheus 监控基础案例

## 什么是 Prometheus？

Prometheus 是一个开源的监控和告警系统，专为容器化环境设计，它使用拉取（pull）模式收集指标，并提供强大的查询语言（PromQL）进行数据分析。

## 本案例包含的内容

- **namespace-rbac.yaml**: 创建命名空间和 RBAC 权限配置
- **prometheus-config.yaml**: Prometheus 配置文件，定义监控目标
- **prometheus-deployment.yaml**: Prometheus Deployment 和 Service

## 快速开始

### 1. 部署命名空间和 RBAC 权限

```bash
kubectl apply -f namespace-rbac.yaml
```

### 2. 部署 Prometheus 配置

```bash
kubectl apply -f prometheus-config.yaml
```

### 3. 部署 Prometheus 实例

```bash
kubectl apply -f prometheus-deployment.yaml
```

### 4. 验证 Prometheus 部署

```bash
# 检查 Pod 状态
kubectl get pods -n prometheus

# 检查 Service 状态
kubectl get svc -n prometheus
```

### 5. 访问 Prometheus UI

#### 5.1 使用 NodePort 访问

```bash
# 获取 Node IP（根据你的 Kubernetes 环境调整）
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 访问 Prometheus UI
echo "http://$NODE_IP:30090"
```

#### 5.2 使用 Port Forward 访问

```bash
kubectl port-forward svc/prometheus 9090:9090 -n prometheus
```

然后访问：http://localhost:9090

## 基本使用

### 1. 查看指标

在 Prometheus UI 中，你可以使用 PromQL 查询语言查看各种指标：

#### 1.1 查看 CPU 使用情况

```
# 查看节点 CPU 使用率
sum(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance) / sum(rate(node_cpu_seconds_total[5m])) by (instance)

# 查看 Pod CPU 使用率
sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod, namespace)
```

#### 1.2 查看内存使用情况

```
# 查看节点内存使用率
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes

# 查看 Pod 内存使用率
sum(container_memory_usage_bytes{container!=""}) by (pod, namespace)
```

#### 1.3 查看 Pod 数量

```
# 查看命名空间中的 Pod 数量
kube_pod_info{namespace="default"}
```

### 2. 创建监控目标

要监控你的应用，只需在 Pod 或 Service 上添加以下注解：

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8080"
  prometheus.io/path: "/metrics"
```

### 3. 示例：监控一个简单的应用

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
  labels:
    app: demo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo-app
  template:
    metadata:
      labels:
        app: demo-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
    spec:
      containers:
      - name: demo-app
        image: prom/node-exporter:latest
        ports:
        - containerPort: 8080
```

## 清理资源

```bash
kubectl delete -f prometheus-deployment.yaml
kubectl delete -f prometheus-config.yaml
kubectl delete -f namespace-rbac.yaml
```

## 扩展建议

1. **添加持久化存储**: 将 Prometheus 的存储从 emptyDir 改为 PersistentVolumeClaim
2. **部署 Grafana**: 结合 Grafana 创建更美观的监控仪表盘
3. **配置告警规则**: 添加 Alertmanager 实现告警功能
4. **监控更多目标**: 配置监控 etcd、kubelet 等核心组件
5. **使用 ServiceMonitor**: 考虑使用 Prometheus Operator 简化配置管理

## 相关链接

- [Prometheus 官方文档](https://prometheus.io/docs/introduction/overview/)
- [PromQL 查询语言](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Kubernetes 监控最佳实践](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/)
