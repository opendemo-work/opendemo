# 🚀 Kubernetes本地环境性能优化与故障排除

> 全面的性能调优指南和常见问题解决方案，帮助你获得最佳的本地Kubernetes体验

## 📋 性能优化指南

### 1. 系统资源配置优化

#### Docker Desktop优化
```bash
# 调整Docker资源配置
# Docker Desktop → Preferences → Resources
# 推荐配置：
# - CPUs: 4-6核心 (根据本地CPU核心数调整)
# - Memory: 8-12GB (至少为物理内存的1/4)
# - Swap: 2-4GB
# - Disk image size: 64GB+

# 通过命令行验证配置
docker info | grep -E "(CPUs|Memory)"
```

#### macOS系统优化
```bash
# 关闭不必要的系统服务
# 系统偏好设置 → 用户与群组 → 登录项
# 移除不必要的开机启动项

# 调整系统内存管理
sudo sysctl -w vm.swappiness=10
sudo sysctl -w vm.dirty_ratio=15
sudo sysctl -w vm.dirty_background_ratio=5

# 创建系统优化配置文件
sudo tee /etc/sysctl.conf <<EOF
vm.swappiness=10
vm.dirty_ratio=15
vm.dirty_background_ratio=5
net.core.somaxconn=65535
EOF
```

### 2. Kubernetes资源配置

#### minikube优化配置
```bash
# 设置合理的资源分配
minikube config set memory 8192
minikube config set cpus 4
minikube config set disk-size 30g

# 启用性能相关插件
minikube addons enable metrics-server
minikube addons enable dashboard

# 使用优化的启动参数
minikube start \
  --memory=8192 \
  --cpus=4 \
  --disk-size=30g \
  --kubernetes-version=v1.28.0 \
  --extra-config=kubelet.max-pods=200 \
  --extra-config=kubelet.pods-per-core=10
```

#### kind优化配置
```bash
# 创建优化的集群配置
cat <<EOF > kind-optimized.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        max-pods: "200"
        pods-per-core: "10"
        system-reserved: "cpu=500m,memory=1Gi"
        kube-reserved: "cpu=200m,memory=512Mi"
- role: worker
  replicas: 2
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        max-pods: "100"
        system-reserved: "cpu=200m,memory=512Mi"
EOF

kind create cluster --config kind-optimized.yaml
```

#### k3s优化配置
```bash
# 创建优化的k3s配置
cat <<EOF | sudo tee /etc/rancher/k3s/config.yaml
write-kubeconfig-mode: "0644"
kubelet-arg:
  - "max-pods=200"
  - "pods-per-core=10"
  - "system-reserved=cpu=200m,memory=512Mi"
  - "kube-reserved=cpu=100m,memory=256Mi"
  - "eviction-hard=memory.available<200Mi"
node-label:
  - "node-role.kubernetes.io/worker=true"
disable:
  - traefik
  - servicelb
  - local-storage
EOF

# 重启k3s应用配置
sudo systemctl restart k3s
```

### 3. 应用性能优化

#### 资源请求和限制
```yaml
# 优化的Deployment资源配置示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: optimized-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: my-app:latest
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        # 健康检查优化
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 2
```

#### 存储优化
```bash
# 使用高效的存储类
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
parameters:
  type: local
mountOptions:
  - noatime
  - nodiratime
EOF

# 为Pod配置高效的卷挂载
# 在Deployment中使用：
# volumes:
# - name: cache-volume
#   emptyDir:
#     medium: Memory  # 使用内存作为存储介质
```

### 4. 网络性能优化

#### DNS优化
```bash
# 优化CoreDNS配置
kubectl get configmap coredns -n kube-system -o yaml > coredns-config.yaml

# 修改配置添加缓存和优化
# 在Corefile中添加：
# cache 30
# reload

kubectl apply -f coredns-config.yaml
kubectl rollout restart deployment coredns -n kube-system
```

#### 网络策略优化
```yaml
# 优化的网络策略配置
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: optimized-network-policy
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: default
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53  # DNS
```

## 🔧 故障排除指南

### 1. 启动和连接问题

#### 集群无法启动
```bash
# 问题诊断步骤：

# 1. 检查系统资源
echo "CPU核心数: $(sysctl -n hw.ncpu)"
echo "内存大小: $(sysctl -n hw.memsize / 1024 / 1024 / 1024)GB"
free -h

# 2. 检查端口占用
lsof -i :6443  # Kubernetes API Server
lsof -i :80    # HTTP服务
lsof -i :443   # HTTPS服务

# 3. 检查Docker状态
docker info
docker ps

# 4. 重启相关服务
# Docker Desktop重启
# 或特定工具重启
minikube stop && minikube start
```

#### kubectl连接失败
```bash
# 1. 检查kubectl配置
kubectl config view
kubectl config current-context

# 2. 重新生成kubeconfig
# minikube
minikube update-context

# kind
kind export kubeconfig --name <cluster-name>

# k3s
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
chmod 600 ~/.kube/config

# 3. 测试连接
kubectl cluster-info
kubectl get nodes
```

### 2. 资源相关问题

#### Pod无法调度
```bash
# 1. 检查资源请求
kubectl describe pod <pod-name>

# 2. 检查节点资源
kubectl describe nodes
kubectl top nodes

# 3. 调整资源限制
# 减少Pod资源请求
kubectl patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","resources":{"requests":{"memory":"64Mi","cpu":"50m"}}}]}}}}'

# 4. 清理资源
kubectl delete pods --field-selector=status.phase==Failed
kubectl delete pods --field-selector=status.phase==Succeeded
```

#### 内存不足问题
```bash
# 1. 检查内存使用
kubectl top nodes
kubectl top pods

# 2. 调整Docker资源限制
# Docker Desktop → Preferences → Resources → Memory

# 3. 优化应用内存使用
# 减少应用内存限制
kubectl set resources deployment <deployment-name> --limits=memory=128Mi

# 4. 清理无用资源
docker system prune -a
kubectl delete pods --all
```

### 3. 网络连接问题

#### 服务无法访问
```bash
# 1. 检查服务配置
kubectl get services
kubectl describe service <service-name>

# 2. 检查端点
kubectl get endpoints <service-name>

# 3. 测试网络连通性
kubectl run debug-pod --image=busybox --rm -it -- sh
# 在容器内测试：
# ping <service-cluster-ip>
# telnet <service-cluster-ip> <port>

# 4. 检查网络策略
kubectl get networkpolicies --all-namespaces
```

#### DNS解析失败
```bash
# 1. 检查CoreDNS状态
kubectl get pods -n kube-system | grep coredns
kubectl logs -n kube-system -l k8s-app=kube-dns

# 2. 测试DNS解析
kubectl run dns-test --image=busybox --rm -it -- sh
# nslookup kubernetes.default

# 3. 重启CoreDNS
kubectl rollout restart deployment coredns -n kube-system

# 4. 检查DNS配置
kubectl get configmap coredns -n kube-system -o yaml
```

### 4. 存储相关问题

#### 持久卷挂载失败
```bash
# 1. 检查存储类
kubectl get storageclass
kubectl describe storageclass

# 2. 检查持久卷状态
kubectl get pv
kubectl get pvc
kubectl describe pv <pv-name>
kubectl describe pvc <pvc-name>

# 3. 检查节点存储
kubectl describe nodes

# 4. 重新创建存储资源
kubectl delete pvc <pvc-name>
kubectl apply -f <pvc-definition.yaml>
```

#### 磁盘空间不足
```bash
# 1. 检查磁盘使用情况
df -h
docker system df

# 2. 清理Docker资源
docker image prune -a
docker container prune
docker volume prune

# 3. 清理Kubernetes资源
kubectl delete pods --field-selector=status.phase==Succeeded
kubectl delete pods --field-selector=status.phase==Failed

# 4. 扩展磁盘空间
# Docker Desktop → Preferences → Resources → Disk image size
```

### 5. 镜像相关问题

#### 镜像拉取失败
```bash
# 1. 检查镜像仓库连接
docker login  # 如果需要认证
kubectl describe pod <pod-name>

# 2. 配置镜像加速器
# Docker Desktop → Preferences → Docker Engine
# 添加：
# {
#   "registry-mirrors": [
#     "https://<mirror-url>"
#   ]
# }

# 3. 使用本地镜像
# minikube
minikube image load <image-name>

# kind
kind load docker-image <image-name> --name <cluster-name>

# 4. 检查镜像标签
docker images
kubectl set image deployment/<deployment-name> <container-name>=<image>:<tag>
```

### 6. 性能问题诊断

#### 集群响应缓慢
```bash
# 1. 检查系统资源
kubectl top nodes
kubectl top pods -A

# 2. 检查组件状态
kubectl get componentstatuses
kubectl get pods -n kube-system

# 3. 分析事件日志
kubectl get events --all-namespaces --sort-by='.lastTimestamp'

# 4. 检查API Server性能
kubectl get --raw /metrics | grep apiserver
```

#### 应用性能问题
```bash
# 1. 应用资源分析
kubectl top pods -n <namespace>
kubectl describe pod <pod-name>

# 2. 应用日志分析
kubectl logs <pod-name> --previous
kubectl logs <pod-name> -c <container-name>

# 3. 网络延迟测试
kubectl exec -it <pod-name> -- ping <target-service>

# 4. 资源调整
kubectl set resources deployment <deployment-name> --requests=cpu=100m,memory=128Mi --limits=cpu=200m,memory=256Mi
```

## 🛠️ 调试工具和命令

### 1. 基础调试命令

```bash
# 集群状态检查
kubectl cluster-info
kubectl get nodes
kubectl get componentstatuses

# 资源查看
kubectl get all --all-namespaces
kubectl get events --all-namespaces --sort-by='.lastTimestamp'

# 详细信息查看
kubectl describe node <node-name>
kubectl describe pod <pod-name>
kubectl describe service <service-name>

# 日志查看
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # 实时日志
kubectl logs <pod-name> --previous  # 上次容器日志
```

### 2. 高级调试技巧

```bash
# 进入容器调试
kubectl exec -it <pod-name> -- sh
kubectl exec -it <pod-name> -c <container-name> -- bash

# 端口转发调试
kubectl port-forward <pod-name> 8080:80
kubectl port-forward service/<service-name> 8080:80

# 临时调试Pod
kubectl run debug --image=busybox --rm -it -- sh

# 网络调试
kubectl run network-debug --image=nixery.dev/shell/curl/dig/nslookup --rm -it -- sh
```

### 3. 性能监控命令

```bash
# 资源使用监控
kubectl top nodes
kubectl top pods -A
watch -n 2 'kubectl top pods'

# 系统指标查看
kubectl get --raw /metrics
kubectl get --raw /api/v1/nodes/<node-name>/proxy/metrics

# 事件监控
kubectl get events --all-namespaces --watch
```

## 📊 性能基准测试

### 1. 启动性能测试

```bash
# 测试集群启动时间
time minikube start
time kind create cluster
time (curl -sfL https://get.k3s.io | sh -)

# 测试Pod调度时间
time kubectl run test-pod --image=nginx --restart=Never
kubectl wait --for=condition=Ready pod/test-pod --timeout=60s
```

### 2. 资源使用基准

```bash
# 内存使用基准
kubectl top nodes
docker stats --no-stream

# CPU使用基准
kubectl top pods -A
top -o CPU

# 磁盘使用基准
docker system df
kubectl describe nodes
```

### 3. 网络性能测试

```bash
# 网络延迟测试
kubectl run network-test --image=busybox --rm -it -- sh
# 在容器内执行：ping -c 10 kubernetes.default

# 带宽测试
kubectl run iperf-server --image=networkstatic/iperf3 --port=5201 -- -s
kubectl run iperf-client --image=networkstatic/iperf3 --rm -it -- sh
# 在客户端容器内执行：iperf3 -c <server-pod-ip> -t 10
```

## 🎯 最佳实践总结

### 1. 预防性措施
```bash
# 定期维护脚本
cat <<'EOF' > k8s-maintenance.sh
#!/bin/bash
# Kubernetes本地环境维护脚本

echo "开始Kubernetes环境维护..."

# 清理无用资源
echo "清理无用的Pod..."
kubectl delete pods --field-selector=status.phase==Succeeded
kubectl delete pods --field-selector=status.phase==Failed

# 清理Docker资源
echo "清理Docker资源..."
docker image prune -f
docker container prune -f

# 检查集群状态
echo "检查集群状态..."
kubectl get nodes
kubectl get componentstatuses

# 检查资源使用
echo "检查资源使用..."
kubectl top nodes

echo "维护完成！"
EOF

chmod +x k8s-maintenance.sh
```

### 2. 监控告警设置
```bash
# 简单的资源监控脚本
cat <<'EOF' > k8s-monitor.sh
#!/bin/bash
# 简单的Kubernetes资源监控

# 检查节点状态
NODE_STATUS=$(kubectl get nodes -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}')
if [[ $NODE_STATUS != *"True"* ]]; then
    echo "警告：节点状态异常"
    # 发送告警通知
fi

# 检查Pod状态
PENDING_PODS=$(kubectl get pods --all-namespaces --field-selector=status.phase=Pending --no-headers | wc -l)
if [ $PENDING_PODS -gt 5 ]; then
    echo "警告：有 $PENDING_PODS 个Pod处于Pending状态"
    # 发送告警通知
fi

# 检查资源使用
NODE_MEMORY=$(kubectl top nodes --no-headers | awk '{print $3}' | sed 's/%//')
for usage in $NODE_MEMORY; do
    if [ $usage -gt 80 ]; then
        echo "警告：节点内存使用率超过80%: $usage%"
        # 发送告警通知
    fi
done
EOF

chmod +x k8s-monitor.sh
```

### 3. 备份恢复策略
```bash
# 自动备份脚本
cat <<'EOF' > k8s-backup.sh
#!/bin/bash
# Kubernetes配置备份脚本

BACKUP_DIR="/tmp/k8s-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p $BACKUP_DIR

# 备份kubectl配置
cp ~/.kube/config $BACKUP_DIR/

# 备份所有资源配置
kubectl get all --all-namespaces -o yaml > $BACKUP_DIR/all-resources.yaml

# 备份重要配置
kubectl get configmaps --all-namespaces -o yaml > $BACKUP_DIR/configmaps.yaml
kubectl get secrets --all-namespaces -o yaml > $BACKUP_DIR/secrets.yaml

# 备份存储类和持久卷
kubectl get storageclass -o yaml > $BACKUP_DIR/storageclass.yaml
kubectl get pv -o yaml > $BACKUP_DIR/pv.yaml

echo "备份完成，位置：$BACKUP_DIR"
EOF

chmod +x k8s-backup.sh
```

---

> **💡 提示**: 定期执行维护和监控脚本，可以有效预防大多数性能和稳定性问题。

**更新时间**: 2026年2月6日  
**维护状态**: ✅ 活跃维护中