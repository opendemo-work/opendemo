# 🚀 Kubernetes 本地开发最佳实践汇总

> 涵盖本地 Kubernetes 开发环境的全面最佳实践指南

## 📚 目录结构

本指南涵盖了本地 Kubernetes 开发的各个方面：

- [多集群管理](./best-practices/multi-cluster/README.md) - 本地多集群管理最佳实践
- [开发工作流](./best-practices/dev-workflow/README.md) - 高效开发、测试、调试工作流
- [网络存储配置](./best-practices/network-storage/README.md) - 网络与存储最佳配置指南
- [性能优化](./performance-troubleshooting/performance.md) - 系统调优和资源配置优化
- [故障排除](./performance-troubleshooting/troubleshooting.md) - 常见问题解决和调试方法
- [工具对比选择](./tools-comparison/README.md) - 详细的工具对比分析和选择建议

## 🎯 核心原则

### 1. 环境一致性
- 保持开发、测试、生产环境的一致性
- 使用相同的配置管理工具（如 Kustomize、Helm）
- 采用相同的镜像构建流程

### 2. 资源效率
- 合理分配 CPU、内存等资源
- 使用轻量级的本地开发方案
- 定期清理未使用的资源

### 3. 安全性
- 遵循最小权限原则
- 使用命名空间进行资源隔离
- 正确配置 RBAC 规则

## 🚀 快速启动

### 开发环境设置
```bash
# 1. 选择适合的本地 Kubernetes 方案
# 推荐：kind 用于开发，k3s 用于轻量级部署

# 2. 安装必要的工具
brew install kubectl kubectx kubens stern k9s
brew install skaffold tilt telepresence

# 3. 配置开发环境
# 设置别名和快捷命令
alias k='kubectl'
alias kcx='kubectx'
alias kns='kubens'

# 4. 启动开发集群
kind create cluster --name dev-cluster
```

### 开发工作流
```bash
# 使用 Skaffold 进行热重载开发
skaffold dev

# 或使用 Tilt 进行可视化开发
tilt up

# 使用 Telepresence 进行本地调试
telepresence intercept my-app --port 8080:80
```

## 🛠️ 工具推荐

### 核心工具
- **kubectl** - Kubernetes 命令行工具
- **kubectx/kubens** - 快速切换上下文和命名空间
- **stern** - 多 Pod 日志查看
- **k9s** - Kubernetes CLI 管理工具

### 开发工具
- **Skaffold** - 自动化构建和部署
- **Tilt** - 开发环境自动化
- **Telepresence** - 本地开发连接远程集群
- **Helm/Kustomize** - 配置管理

### 监控调试
- **Netshoot** - 网络诊断工具箱
- **Prometheus/Grafana** - 监控和可视化
- **Jaeger** - 分布式追踪

## 🔧 配置优化

### 1. 网络配置
```yaml
# CoreDNS 优化配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```

### 2. 存储配置
```yaml
# 本地存储类配置
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-path
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
```

### 3. 资源配置
```yaml
# 应用资源配置示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: optimized-app
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: app
        image: my-app:latest
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
            ephemeral-storage: "100Mi"
          limits:
            memory: "256Mi"
            cpu: "200m"
            ephemeral-storage: "500Mi"
        securityContext:
          readOnlyRootFilesystem: false
          allowPrivilegeEscalation: false
```

## 📊 性能监控

### 监控指标
- **CPU 使用率** - 确保不超过请求值
- **内存使用** - 防止 OOMKill
- **网络延迟** - 检查服务间通信
- **存储性能** - 监控 I/O 延迟

### 基准测试
```bash
# 网络性能测试
kubectl run netperf --image=nicolaka/netshoot --rm -it --restart=Never -- iperf3 -c <target-service>

# 存储性能测试
kubectl run storagetest --image=polinux/stress --rm -it --restart=Never -- dd if=/dev/zero of=/tmp/test.dat bs=1G count=1 oflag=dsync

# 应用响应时间测试
kubectl run responsetime --image=nicolaka/netshoot --rm -it --restart=Never -- time curl -s http://<app-service>
```

## 🚨 故障排除

### 常见问题及解决方案

1. **Pod 无法启动**
   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name> --previous
   ```

2. **服务无法访问**
   ```bash
   kubectl get svc,endpoints
   kubectl exec -it <debug-pod> -- nslookup <service-name>
   ```

3. **资源不足**
   ```bash
   kubectl top nodes
   kubectl describe node <node-name>
   ```

4. **DNS 解析问题**
   ```bash
   kubectl run debug --image=nicolaka/netshoot --rm -it --restart=Never -- nslookup kubernetes.default
   ```

## 🎯 高级技巧

### 1. 多集群管理
- 使用命名规范区分不同环境
- 配置不同的 kubeconfig 文件
- 使用脚本自动化集群切换

### 2. 开发效率提升
- 使用热重载工具（Skaffold/Tilt）
- 配置 IDE 插件
- 设置常用别名和函数

### 3. 资源优化
- 合理设置资源请求和限制
- 使用命名空间进行资源隔离
- 定期清理未使用的资源

## 📈 持续改进

### 定期维护任务
- 更新工具链到最新稳定版本
- 清理未使用的镜像和资源
- 优化资源配置和性能

### 学习资源
- 定期关注 Kubernetes 官方文档
- 参与社区讨论和会议
- 实践新的特性和功能

---

> **💡 提示**: 本地 Kubernetes 开发环境的优化是一个持续的过程。根据项目需求和团队经验不断调整和改进配置。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日