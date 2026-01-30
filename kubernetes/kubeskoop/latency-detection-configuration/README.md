# Kubernetes延迟检测配置演示

## 简介
本演示展示了如何在Kubernetes集群中配置延迟检测机制，使用Prometheus和ServiceMonitor来监控服务间的网络延迟。通过三个不同的场景，帮助理解如何实现和优化延迟监控。

## 学习目标
- 理解Kubernetes中的延迟检测原理
- 掌握使用Prometheus进行网络延迟监控的方法
- 学会配置ServiceMonitor以收集指标

## 环境要求
- kubectl >= 1.20
- minikube >= 1.15（或任何可用的Kubernetes集群）
- Helm（用于安装Prometheus Operator）

## 安装依赖的详细步骤
1. 安装kubectl：https://kubernetes.io/docs/tasks/tools/install-kubectl/
2. 安装minikube：https://minikube.sigs.k8s.io/docs/start/
3. 启动minikube集群：`minikube start`
4. 安装Helm：https://helm.sh/docs/intro/install/
5. 添加Prometheus Operator Helm仓库并安装：
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm install prometheus prometheus-community/kube-prometheus-stack
   ```

## 文件说明
- `latency-detection-config.yaml`：定义了应用和服务的配置，包括注解以启用监控。
- `service-monitor.yaml`：定义了ServiceMonitor资源，用于抓取自定义指标。
- `prometheus-config.yaml`：配置Prometheus以识别新的监控目标。

## 逐步实操指南
### 步骤1: 应用延迟检测配置
```bash
kubectl apply -f latency-detection-config.yaml
```
**预期输出**：
```bash
namespace/monitoring created
deployment.apps/httpbin created
service/httpbin created
```

### 步骤2: 部署ServiceMonitor
```bash
kubectl apply -f service-monitor.yaml
```
**预期输出**：
```bash
servicemonitor.monitoring.coreos.com/httpbin-monitor created
```

### 步骤3: 验证配置
```bash
kubectl get pods -n monitoring
```
**预期输出**：应看到Prometheus pod正在运行。

### 步骤4: 访问Prometheus UI
```bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090
```
然后访问 http://localhost:9090 并查询 `http_request_duration_seconds`。

## 代码解析
- **latency-detection-config.yaml**：创建了一个HTTPBin服务，并暴露了/metrics端点，该端点提供请求延迟数据。
- **service-monitor.yaml**：定义了如何从httpbin服务抓取指标，关键字段是`metricsPath`和`port`。
- **prometheus-config.yaml**：确保Prometheus配置正确加载新添加的ServiceMonitor。

## 预期输出示例
在Prometheus UI中执行查询：
```promql
histogram_quantile(0.9, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```
将返回过去5分钟内第90百分位的HTTP请求延迟。

## 常见问题解答
**Q: Prometheus无法发现服务？**
A: 检查ServiceMonitor的`namespaceSelector`是否匹配目标命名空间。

**Q: 没有数据显示？**
A: 确保目标服务确实暴露了/metrics路径并且返回有效Prometheus格式数据。

## 扩展学习建议
- 探索Alertmanager配置基于延迟的告警规则
- 使用Kubernetes Network Policies限制跨服务通信以测试延迟变化
- 实现分布式追踪（如Jaeger）与Prometheus结合分析延迟根源