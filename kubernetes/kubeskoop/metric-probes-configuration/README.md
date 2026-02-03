# Kubernetes Metric Probes 配置演示

## 简介
本示例演示如何在 Kubernetes Pod 中使用 Liveness、Readiness 和 Startup 探针，结合 HTTP 指标端点进行应用健康检查。通过模拟一个简单的 Web 服务，展示不同探针的行为及其对 Pod 生命周期的影响。

## 学习目标
- 理解 Kubernetes 健康探针的作用和类型
- 掌握如何配置基于 HTTP 的 liveness、readiness 和 startup 探针
- 学会通过指标端点监控应用健康状态
- 实践探针参数调优（如 initialDelaySeconds、periodSeconds）

## 环境要求
- Kubernetes 集群（版本 >= 1.20）
- kubectl 命令行工具（版本 >= 1.20）
- 支持 YAML 文件部署能力
- 可运行容器镜像的环境（Docker 或 containerd）

## 安装依赖步骤
1. 安装并配置 `kubectl` 工具：
   ```bash
   # 使用包管理器安装（以 macOS 为例）
   brew install kubectl
   
   # 验证安装
   kubectl version --client
   ```

2. 连接到 Kubernetes 集群（例如 Minikube、Kind、EKS、GKE 等）
   ```bash
   kubectl cluster-info
   ```

3. 确保集群处于就绪状态
   ```bash
   kubectl get nodes
   # 输出应显示所有节点为 Ready 状态
   ```

## 文件说明
- `deployment-liveness.yaml`：包含启用 livenessProbe 的 Deployment 示例
- `deployment-readiness.yaml`：展示 readinessProbe 如何控制流量接入
- `deployment-startup.yaml`：演示 startupProbe 在启动慢的应用中的作用

## 逐步实操指南

### 步骤 1: 部署带有 Liveness 探针的应用
```bash
kubectl apply -f deployment-liveness.yaml
```

**预期输出**：
```bash
deployment.apps/demo-liveness created
```

查看 Pod 状态：
```bash
kubectl get pods -l app=demo-liveness
# 预期看到 Pod 处于 Running 状态
```

### 步骤 2: 部署 Readiness 探针示例
```bash
kubectl apply -f deployment-readiness.yaml
```

验证服务是否接收流量：
```bash
kubectl get pods -l app=demo-readiness
kubectl get endpoints demo-readiness-service
# Endpoint 应仅包含处于 ready 状态的 Pod IP
```

### 步骤 3: 部署 Startup 探针示例（适用于启动较慢的服务）
```bash
kubectl apply -f deployment-startup.yaml
```

观察 Pod 启动过程：
```bash
kubectl describe pod -l app=demo-startup
# 查看 Events 是否显示 startup probe 成功
```

## 代码解析

### deployment-liveness.yaml
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
```
- `httpGet`：通过 HTTP 请求检查 `/healthz` 是否返回 200
- `initialDelaySeconds`：容器启动后等待 10 秒再开始探测
- `periodSeconds`：每 5 秒执行一次探测

若连续失败超过阈值（默认 3 次），Kubelet 将重启容器。

### deployment-readiness.yaml
```yaml
readinessProbe:
  httpGet:
    path: /readyz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```
- 探针失败时，Pod 不会被加入 Service 的 Endpoints，不接收新请求
- 适合用于数据库连接初始化等场景

### deployment-startup.yaml
```yaml
startupProbe:
  httpGet:
    path: /healthz
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```
- 在应用完全启动前禁用其他探针
- 最多尝试 30 次，每次间隔 10 秒（最长等待 5 分钟）
- 启动完成后自动交由 liveness/readiness 探针接管

## 预期输出示例
```bash
$ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
demo-liveness-76b8c6c99c-abcde    1/1     Running   0          2m
demo-readiness-5d9fdf987c-xyzab  1/1     Running   0          2m
demo-startup-6c8c7b9db4-uvwxy    1/1     Running   0          2m
```

## 常见问题解答

**Q: 探针频繁触发重启怎么办？**
A: 增加 `initialDelaySeconds` 或 `failureThreshold`，确保应用有足够时间初始化。

**Q: Readiness 探针失败但 Pod 仍在运行？**
A: 正常行为。此时 Pod 不会接收流量，但不会被重启。

**Q: StartupProbe 不生效？**
A: 确保未同时设置 livenessProbe 过早触发重启。建议在慢启动应用中使用 startupProbe 并禁用初期 liveness 检查。

## 扩展学习建议
- 结合 Prometheus 监控探针失败事件
- 使用 gRPC 探针（gRPC Health Checking Protocol）
- 实现自定义探针逻辑（如检查数据库连接）
- 探针与 Horizontal Pod Autoscaler（HPA）结合使用