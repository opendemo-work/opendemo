# Kubernetes网络拓扑可视化演示

## 简介
本演示项目展示了如何在Kubernetes集群中收集和可视化Pod之间的网络通信拓扑。通过部署Prometheus监控系统、服务发现机制以及自定义数据采集器，我们能够实时查看集群内各服务间的调用关系和流量路径。

## 学习目标
- 理解Kubernetes中的网络通信模型
- 掌握使用Prometheus进行网络指标采集的方法
- 学会构建简单的网络拓扑可视化方案
- 了解Service、Endpoint与Pod间的关系映射

## 环境要求
- 操作系统：Windows 10+/macOS 10.14+/Linux（Ubuntu 20.04+）
- kubectl v1.20 或更高版本
- Helm v3.5+（用于安装Prometheus和Grafana）
- 可运行的Kubernetes集群（Minikube或Kind也可）

## 安装依赖步骤
```bash
# 1. 安装kubectl（若未安装）
# 参考官方文档: https://kubernetes.io/docs/tasks/tools/

# 2. 安装Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 3. 添加Prometheus社区仓库并安装kube-prometheus-stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```

## 文件说明
- `network-topology-collector.yaml`: 自定义指标采集器Deployment，用于抓取服务间调用数据
- `service-graph-service.yaml`: Service定义，暴露拓扑数据接口
- `configmap-metrics-config.yaml`: 配置采集规则的ConfigMap

## 逐步实操指南

### 步骤1：启动监控栈
```bash
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```
**预期输出**：
> NAME: prometheus
> NAMESPACE: monitoring
> ... Status: deployed

### 步骤2：部署网络拓扑采集器
```bash
kubectl apply -f network-topology-collector.yaml
```
**预期输出**：
> deployment.apps/network-topology-collector created

### 步骤3：创建服务和配置
```bash
kubectl apply -f service-graph-service.yaml
kubectl apply -f configmap-metrics-config.yaml
```
**预期输出**：
> service/service-graph created
> configmap/metrics-config created

### 步骤4：访问Grafana查看拓扑（可选）
```bash
# 端口转发到本地
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
```
打开浏览器访问 http://localhost:3000，使用默认账号 `admin` / `prom-operator` 登录，导入拓扑仪表盘。

## 代码解析

### network-topology-collector.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: network-topology-collector
spec:
  replicas: 1
  selector:
    matchLabels:
      app: topology-collector
  template:
    metadata:
      labels:
        app: topology-collector
    spec:
      containers:
      - name: collector
        image: busybox
        command: ['sh', '-c', 'echo "模拟网络拓扑数据生成" && sleep 3600']
        # 实际生产中应替换为eBPF或Istio等真实采集工具
```
该Deployment模拟一个拓扑数据采集器，实际场景中可集成Cilium、Istio或eBPF技术进行真实流量分析。

### service-graph-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: service-graph
spec:
  selector:
    app: topology-collector
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```
定义一个Service将采集器暴露出来，便于其他组件查询拓扑信息。

## 预期输出示例
执行 `kubectl get pods -A` 后应看到：
> monitoring     prometheus-kube-prometheus-sta...   Running
> default        network-topology-collector-...     Running

## 常见问题解答

**Q: 为什么采集器使用busybox？**
A: 本演示为简化结构，使用busybox模拟行为。实际应用应使用支持网络追踪的镜像如`cilium/cilium`或`istio/proxyv2`。

**Q: 如何查看真实的拓扑图？**
A: 在Grafana中导入ID为11827的“Kubernetes Network Topology”仪表盘，或使用Kiali（Istio生态）进行可视化。

**Q: 是否支持跨命名空间服务发现？**
A: 是的，Prometheus默认会抓取所有命名空间的服务指标，只要ServiceMonitor配置正确。

## 扩展学习建议
- 探索Cilium + Hubble实现深度网络可视化
- 学习Istio服务网格中的Kiali控制台使用
- 使用eBPF程序（如Pixie）自动发现微服务依赖
- 结合OpenTelemetry实现分布式追踪与拓扑融合