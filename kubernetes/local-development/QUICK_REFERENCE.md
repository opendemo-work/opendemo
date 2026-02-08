# 📋 Kubernetes 本地开发快速参考卡

> 本地 Kubernetes 开发环境的常用命令和最佳实践速查表

## 🛠️ 常用工具命令

### kubectl 快速命令
```bash
# 基础操作
kubectl get pods                          # 获取 Pod 列表
kubectl get services                      # 获取服务列表
kubectl get deployments                   # 获取部署列表
kubectl describe pod <pod-name>          # 描述 Pod 详情
kubectl logs <pod-name>                  # 查看 Pod 日志
kubectl exec -it <pod-name> -- sh        # 进入 Pod

# 上下文和命名空间
kubectl config get-contexts              # 查看所有上下文
kubectl config use-context <context>     # 切换上下文
kubectl get namespaces                   # 查看所有命名空间
kubectl config set-context --current --namespace=<ns>  # 设置当前命名空间
```

### kubectx/kubens 快捷命令
```bash
kubectx                                 # 列出并选择上下文
kubectx <context-name>                  # 切换到指定上下文
kubens                                  # 列出并选择命名空间
kubens <namespace>                      # 切换到指定命名空间
```

## 🚀 本地开发工具

### Skaffold
```bash
# 初始化 Skaffold 项目
skaffold init

# 开发模式（自动构建和部署）
skaffold dev

# 构建镜像
skaffold build

# 部署到集群
skaffold run

# 清理部署
skaffold delete
```

### Tilt
```bash
# 启动 Tilt
tilt up

# 停止 Tilt
tilt down

# 查看 Tilt UI
open http://localhost:10350
```

### Telepresence
```bash
# 连接到集群
telepresence connect

# 交换流量到本地
telepresence intercept <deployment-name> --port <local-port>:<container-port>
```

## 📦 镜像和构建

### Docker 优化命令
```bash
# 多架构构建
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .

# 构建缓存优化
docker build --cache-from myapp:latest --build-arg BUILDKIT_INLINE_CACHE=1 -t myapp:latest .

# 清理构建缓存
docker builder prune
```

## 🌐 网络配置

### 常用网络命令
```bash
# 端口转发
kubectl port-forward deployment/<deployment-name> <local-port>:<container-port>

# 查看服务和端点
kubectl get svc,ep

# 测试 DNS 解析
kubectl run test --image=nicolaka/netshoot --rm -it --restart=Never -- nslookup <service-name>

# 网络策略示例
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF
```

## 💾 存储配置

### PVC/PV 操作
```bash
# 查看存储状态
kubectl get pv,pvc --all-namespaces

# 查看存储类
kubectl get storageclass

# 创建 PVC
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
EOF
```

## 🔍 调试和故障排除

### 常用调试命令
```bash
# Pod 调试
kubectl debug <pod-name> --image=busybox:1.35 --target=<container-name>

# 事件查看
kubectl get events --sort-by='.lastTimestamp'

# 资源使用
kubectl top nodes
kubectl top pods

# 详细状态
kubectl describe pod <pod-name>
kubectl describe deployment <deployment-name>
```

## ⚡ 性能优化

### 资源配置
```yaml
# 资源请求和限制示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: optimized-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
```

## 🚨 常见问题解决

### Pod 无法启动
```bash
# 检查 Pod 状态
kubectl describe pod <pod-name>

# 查看日志
kubectl logs <pod-name> --previous

# 检查事件
kubectl get events --field-selector involvedObject.name=<pod-name>
```

### 服务无法访问
```bash
# 检查服务和端点
kubectl get svc,ep <service-name>

# 测试连通性
kubectl run test --image=nicolaka/netshoot --rm -it --restart=Never -- ping <service-name>

# 端口转发测试
kubectl port-forward svc/<service-name> 8080:80
```

### 资源不足
```bash
# 检查节点资源
kubectl top nodes

# 检查 Pod 资源
kubectl top pods

# 查看节点状态
kubectl describe node <node-name>
```

## 📊 监控命令

### 实时监控
```bash
# 持续监控 Pod 状态
kubectl get pods -w

# 监控资源使用
watch kubectl top pods

# 查看所有事件
kubectl get events --all-namespaces --sort-by='.lastTimestamp' -w
```

## 🧹 清理命令

### 资源清理
```bash
# 删除命名空间及其所有资源
kubectl delete namespace <namespace-name>

# 删除所有 Pod（谨慎使用）
kubectl delete pods --all --all-namespaces

# 清理完成的 Jobs
kubectl delete jobs --field-selector=status.successful=1 --all-namespaces

# 清理失败的 Pods
kubectl delete pods --field-selector=status.phase=Failed --all-namespaces
```

## 🎯 开发工作流最佳实践

### 快速部署脚本
```bash
#!/bin/bash
# 快速部署脚本示例
DEPLOY_IMAGE="myapp:$(git rev-parse --short HEAD)"

# 构建镜像
docker build -t $DEPLOY_IMAGE .

# 更新部署
kubectl set image deployment/myapp *=myapp:$DEPLOY_IMAGE

# 等待部署完成
kubectl rollout status deployment/myapp
```

### 环境切换脚本
```bash
#!/bin/bash
# 环境切换脚本
switch_env() {
    local env=$1
    case $env in
        "dev")
            kubectl config use-context kind-dev-cluster
            ;;
        "test")
            kubectl config use-context kind-test-cluster
            ;;
        "local")
            kubectl config use-context docker-desktop
            ;;
        *)
            echo "Usage: switch_env [dev|test|local]"
            ;;
    esac
}
```

---

> **💡 提示**: 将此快速参考卡保存为书签或打印出来，以便在开发过程中快速查阅常用命令。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日