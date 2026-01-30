# Kubernetes Event Probes 配置演示

## 简介
本演示展示了如何在 Kubernetes 中使用存活探针（liveness probe）和就绪探针（readiness probe）来监控应用的健康状态。这些探针帮助 Kubernetes 决定何时重启容器或何时将流量路由到 Pod。

## 学习目标
- 理解 liveness 和 readiness 探针的作用
- 掌握 HTTP 和命令行探针的配置方法
- 学会调试探针失败问题

## 环境要求
- 操作系统：Windows、Linux 或 macOS
- kubectl >= 1.20
- Minikube >= 1.25（用于本地测试）
- Docker（可选，用于构建镜像）

## 安装依赖步骤
1. 安装 kubectl：https://kubernetes.io/docs/tasks/tools/install-kubectl/
2. 安装 Minikube：https://minikube.sigs.k8s.io/docs/start/
3. 启动集群：`minikube start`

## 文件说明
- `liveness-probe.yaml`：配置基于命令的存活探针
- `readiness-probe.yaml`：配置基于 HTTP 的就绪探针
- `both-probes.yaml`：同时配置两种探针

## 逐步实操指南

### 步骤 1: 启动 Minikube 集群
```bash
minikube start
```
**预期输出**：显示“Kubectl is now configured to use "minikube"”等信息

### 步骤 2: 应用存活探针配置
```bash
kubectl apply -f liveness-probe.yaml
```
**预期输出**：`pod/liveness-demo created`

### 步骤 3: 查看 Pod 状态
```bash
kubectl get pods liveness-demo
```
持续运行直到状态为 Running。若探针失败，Kubernetes 会重启容器。

### 步骤 4: 应用就绪探针配置
```bash
kubectl apply -f readiness-probe.yaml
```
**预期输出**：`pod/readiness-demo created`

### 步骤 5: 查看就绪状态变化
```bash
kubectl get pods readiness-demo
```
开始时 READY 列可能为 0/1，当服务启动后变为 1/1

### 步骤 6: 同时应用两个探针
```bash
kubectl apply -f both-probes.yaml
```
**预期输出**：`pod/both-probes-demo created`

### 步骤 7: 清理资源
```bash
kubectl delete -f liveness-probe.yaml
kubectl delete -f readiness-probe.yaml
kubectl delete -f both-probes.yaml
```

## 代码解析

### liveness-probe.yaml
使用 `exec` 探针执行命令检查文件是否存在。如果 `/tmp/healthy` 不存在，探针失败并触发重启。

### readiness-probe.yaml
使用 HTTP GET 请求探测端口 8080 的 `/health` 路径。只有当返回码在 200-399 之间时才认为准备就绪。

### both-probes.yaml
结合了前两者，定义了独立的存活和就绪逻辑，实现更精细的控制。

## 预期输出示例
```bash
NAME              READY   STATUS    RESTARTS   AGE
liveness-demo     1/1     Running   1          2m
readiness-demo    1/1     Running   0          90s
both-probes-demo  1/1     Running   0          60s
```

## 常见问题解答

**Q: 探针频繁失败怎么办？**
A: 检查初始延迟（initialDelaySeconds）是否足够长，确保应用有时间启动。

**Q: 就绪探针失败会影响什么？**
A: Pod 不会被加入 Service 的 Endpoints，不会接收新流量。

**Q: 存活探针失败会发生什么？**
A: Kubernetes 会杀死容器并根据重启策略重新创建它。

## 扩展学习建议
- 尝试使用 startupProbe 处理慢启动应用
- 配置 TCP 探针用于非 HTTP 服务
- 使用 Prometheus + kube-state-metrics 监控探针行为