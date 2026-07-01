# 🐳 kind (Kubernetes in Docker) macOS部署指南

> 基于Docker的轻量级Kubernetes集群部署方案，适合开发和测试环境

## 📋 方案概述

kind (Kubernetes in Docker) 是一个使用Docker容器作为节点运行本地Kubernetes集群的工具。它专为测试Kubernetes本身而设计，但也非常适合本地开发。

### 🎯 适用场景
- Kubernetes开发测试
- CI/CD流水线集成
- 多节点集群测试
- 控制器和Operator开发
- 网络插件测试

### 🔧 技术特点
- **轻量级**：基于Docker容器运行
- **快速启动**：集群启动时间短
- **多节点支持**：支持创建多节点集群
- **与CI/CD集成**：天然支持自动化测试
- **资源效率**：相比虚拟机更节省资源

## 🛠️ 环境准备

### 1. 系统要求检查

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查macOS版本
sw_vers
# 推荐：macOS 12.0 (Monterey) 或更高版本

# 检查硬件资源
echo "CPU核心数: $(sysctl -n hw.ncpu)"
echo "内存大小: $(sysctl -n hw.memsize / 1024 / 1024 / 1024)GB"
# 推荐：CPU >= 4核心，内存 >= 8GB

# 检查Docker环境
docker --version
docker info | grep "Total Memory"
# 确保Docker Desktop正在运行
```

### 2. 必要工具安装

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装Homebrew（如果没有）
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 安装kubectl
brew install kubectl

# 验证kubectl安装
kubectl version --client

# 安装Docker Desktop for Mac
brew install --cask docker

# 启动Docker Desktop
open -a Docker

# 等待Docker启动完成
until docker info &> /dev/null; do
    echo "等待Docker启动..."
    sleep 5
done
echo "Docker已启动"
```

### 3. Docker资源配置

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查当前Docker资源配置
docker info | grep -E "(CPUs|Memory)"

# 建议的Docker资源配置：
# Docker Desktop → Preferences → Resources
# - CPUs: 4-6
# - Memory: 8-12GB
# - Swap: 2-4GB
# - Disk image size: 64GB+
```

## 📦 kind安装和配置

### 1. 安装kind

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用Homebrew安装kind
brew install kind

# 或者直接下载二进制文件
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-darwin-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# 验证安装
kind version

# 检查可用命令
kind --help
```

### 2. 基础集群创建

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建默认集群
kind create cluster

# 创建指定名称的集群
kind create cluster --name dev-cluster

# 创建集群并等待准备就绪
kind create cluster --wait 5m

# 验证集群创建
kubectl cluster-info --context kind-dev-cluster
```

## 🏗️ 高级集群配置

### 1. 多节点集群配置

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建多节点集群配置文件
cat <<EOF > kind-multi-node.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
EOF

# 创建多节点集群
kind create cluster --config kind-multi-node.yaml --name multi-node

# 验证节点
kubectl get nodes
```

### 2. Ingress控制器配置

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 创建支持Ingress的集群配置
cat <<EOF > kind-ingress.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
- role: worker
EOF

# 创建支持Ingress的集群
kind create cluster --config kind-ingress.yaml --name ingress-cluster

# 验证端口映射
docker port ingress-cluster-control-plane 80
docker port ingress-cluster-control-plane 443
```

### 3. 完整生产级配置

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 创建生产级集群配置
cat <<EOF > kind-production.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  # 使用自定义网络
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
  # 启用IPv6
  ipFamily: ipv4
nodes:
- role: control-plane
  # 控制平面配置
  kubeadmConfigPatches:
  - |
    kind: ClusterConfiguration
    apiServer:
      extraArgs:
        enable-admission-plugins: "NodeRestriction"
    controllerManager:
      extraArgs:
        bind-address: "0.0.0.0"
    scheduler:
      extraArgs:
        bind-address: "0.0.0.0"
  # 端口映射配置
  extraPortMappings:
  - containerPort: 30080
    hostPort: 30080
    protocol: TCP
  - containerPort: 30443
    hostPort: 30443
    protocol: TCP
- role: worker
  replicas: 2
  # 工作节点配置
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "role=worker"
  # 挂载本地目录（可选）
  extraMounts:
  - containerPath: /tmp/test-volume
    hostPath: /tmp/test-volume
    readOnly: false
EOF

# 创建生产级集群
kind create cluster --config kind-production.yaml --name prod-cluster
```

## 🚀 集群管理和验证

### 1. 集群基本信息

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 列出所有集群
kind get clusters

# 获取集群详细信息
kind get kubeconfig --name prod-cluster

# 检查集群状态
kubectl cluster-info --context kind-prod-cluster

# 查看节点信息
kubectl get nodes --context kind-prod-cluster

# 查看系统组件
kubectl get pods -n kube-system --context kind-prod-cluster
```

### 2. 上下文管理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查看所有kubectl上下文
kubectl config get-contexts

# 切换到kind集群
kubectl config use-context kind-prod-cluster

# 设置默认命名空间
kubectl config set-context --current --namespace=default

# 验证当前上下文
kubectl config current-context
```

### 3. 集群验证测试

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 部署测试应用
kubectl create deployment nginx-test --image=nginx:latest

# 暴露服务
kubectl expose deployment nginx-test --port=80 --type=NodePort

# 获取服务信息
kubectl get services

# 测试服务访问
kubectl get nodes -o wide
curl http://localhost:30080  # 使用NodePort访问

# 删除测试资源
kubectl delete deployment nginx-test
kubectl delete service nginx-test
```

## 🔧 核心组件安装

### 1. Ingress Controller安装

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 为支持Ingress的集群安装nginx-ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# 等待Ingress控制器就绪
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

# 验证Ingress控制器
kubectl get pods -n ingress-nginx
```

### 2. Metrics Server安装

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 下载Metrics Server配置
curl -LO https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# 修改配置以支持本地环境
sed -i '' 's/--secure-port=443/--secure-port=10250/g' components.yaml
sed -i '' '/- --secure-port=10250/a\
        - --kubelet-insecure-tls' components.yaml

# 部署Metrics Server
kubectl apply -f components.yaml

# 验证安装
kubectl get pods -n kube-system | grep metrics-server
kubectl top nodes
```

### 3. Dashboard安装

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装Kubernetes Dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# 创建管理员用户
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
EOF

# 获取访问令牌
kubectl -n kubernetes-dashboard create token admin-user

# 启动代理访问Dashboard
kubectl proxy
# 访问地址: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

## 🧪 实战演练

### 1. 应用部署示例

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建示例应用
cat <<EOF > sample-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app
  labels:
    app: sample-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: sample-app-service
spec:
  selector:
    app: sample-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: NodePort
EOF

# 部署应用
kubectl apply -f sample-app.yaml

# 验证部署
kubectl get deployments
kubectl get pods
kubectl get services
```

### 2. Ingress配置示例

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建Ingress资源
cat <<EOF > sample-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: sample-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: sample.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: sample-app-service
            port:
              number: 80
EOF

# 应用Ingress配置
kubectl apply -f sample-ingress.yaml

# 测试Ingress访问
curl -H "Host: sample.local" http://localhost
```

### 3. 持久化存储示例

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建持久卷和持久卷声明
cat <<EOF > storage-example.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /tmp/kind-pv
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: local-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: storage-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: storage-test
  template:
    metadata:
      labels:
        app: storage-test
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ["sleep", "3600"]
        volumeMounts:
        - name: storage
          mountPath: /data
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: local-pvc
EOF

# 部署存储示例
kubectl apply -f storage-example.yaml

# 验证持久化
kubectl exec -it deployment/storage-test -- sh -c "echo 'Hello World' > /data/test.txt"
kubectl exec -it deployment/storage-test -- cat /data/test.txt
```

## 🛠️ 日常管理操作

### 1. 集群控制

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 启动已存在的集群
docker start kind-prod-cluster-control-plane

# 停止集群
docker stop kind-prod-cluster-control-plane

# 重启集群
docker restart kind-prod-cluster-control-plane

# 查看集群容器状态
docker ps -a | grep kind
```

### 2. 镜像管理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 将本地镜像加载到集群
kind load docker-image nginx:latest --name prod-cluster

# 从tar文件加载镜像
kind load image-archive my-app.tar --name prod-cluster

# 查看集群中的镜像
docker exec kind-prod-cluster-control-plane crictl images
```

### 3. 日志和调试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查看控制平面日志
docker logs kind-prod-cluster-control-plane

# 进入控制平面容器
docker exec -it kind-prod-cluster-control-plane bash

# 查看Kubernetes组件日志
kubectl logs -n kube-system kube-apiserver-kind-prod-cluster-control-plane

# 查看特定Pod日志
kubectl logs <pod-name>
```

## 🔍 监控和性能

### 1. 资源监控

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 查看节点资源使用
kubectl top nodes

# 查看Pod资源使用
kubectl top pods

# 查看集群事件
kubectl get events --all-namespaces

# 查看Pod详细信息
kubectl describe pod <pod-name>
```

### 2. 性能调优

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 调整Docker资源限制
# Docker Desktop → Preferences → Resources

# 优化集群配置
cat <<EOF > optimized-kind.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  # 优化kubelet配置
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        max-pods: "200"
        pods-per-core: "10"
        system-reserved: "cpu=500m,memory=1Gi"
- role: worker
  replicas: 2
EOF

# 创建优化集群
kind create cluster --config optimized-kind.yaml --name optimized
```

### 3. 网络性能监控

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 测试Pod间网络延迟
kubectl run debug-pod --image=busybox -- sleep 3600
kubectl exec -it debug-pod -- ping <another-pod-ip>

# 测试服务网络性能
kubectl run curl-test --image=curlimages/curl -- curl -w "@curl-format.txt" -o /dev/null -s http://sample-app-service

# 查看网络策略
kubectl get networkpolicies --all-namespaces
```

## 🧹 清理和维护

### 1. 资源清理

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 删除所有应用资源
kubectl delete deployments,services,ingresses --all

# 清理特定命名空间
kubectl delete all --all -n default

# 清理配置资源
kubectl delete configmaps,secrets --all
```

### 2. 集群删除

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 删除特定集群
kind delete cluster --name prod-cluster

# 删除所有集群
kind delete clusters --all

# 验证删除
kind get clusters
docker ps | grep kind
```

### 3. 磁盘清理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 清理未使用的Docker镜像
docker image prune -a

# 清理未使用的卷
docker volume prune

# 清理构建缓存
docker builder prune

# 查看磁盘使用情况
docker system df
```

## 🚨 常见问题解决

### 1. 集群创建失败

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 问题：端口已被占用
# 解决：检查端口使用情况
lsof -i :80
lsof -i :443

# 问题：资源不足
# 解决：增加Docker资源配置
# Docker Desktop → Preferences → Resources

# 问题：镜像拉取失败
# 解决：配置镜像加速
# Docker Desktop → Preferences → Docker Engine
# 添加 {"registry-mirrors": ["https://<mirror-url>"]}
```

### 2. 网络连接问题

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 问题：无法访问服务
# 解决：检查端口映射
docker port kind-prod-cluster-control-plane

# 问题：Ingress无法工作
# 解决：验证Ingress控制器状态
kubectl get pods -n ingress-nginx

# 问题：DNS解析失败
# 解决：检查CoreDNS状态
kubectl get pods -n kube-system | grep coredns
```

### 3. 性能相关问题

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 问题：Pod调度缓慢
# 解决：检查资源请求和限制
kubectl describe nodes

# 问题：内存不足
# 解决：调整资源分配
docker stats kind-prod-cluster-control-plane

# 问题：磁盘空间不足
# 解决：清理无用资源
docker system prune -a
```

### 4. 调试命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 深入调试集群问题
# 进入控制平面容器
docker exec -it kind-prod-cluster-control-plane bash

# 查看kubelet状态
systemctl status kubelet

# 检查容器运行时
crictl ps

# 查看集群配置
cat /etc/kubernetes/kubeconfig
```

## 🎯 最佳实践

### 1. 集群管理最佳实践

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 使用有意义的集群命名
kind create cluster --name development
kind create cluster --name testing
kind create cluster --name staging

# 2. 合理规划资源配置
# 控制平面节点: 2-4 CPU, 4-8GB内存
# 工作节点: 2-4 CPU, 4-8GB内存 每个节点

# 3. 使用版本控制配置文件
# 将集群配置保存为YAML文件进行版本控制
```

### 2. 应用部署最佳实践

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 使用命名空间隔离
kubectl create namespace dev
kubectl create namespace prod

# 2. 设置合理的资源限制
# 在Deployment中明确指定requests和limits

# 3. 使用健康检查探针
# 配置livenessProbe和readinessProbe

# 4. 标签和注解规范
# 为所有资源添加环境、版本等标签
```

### 3. 安全配置

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 启用RBAC
# kind默认启用RBAC

# 2. 网络策略配置
# 部署网络策略限制流量

# 3. 定期更新组件
kind delete cluster --name old-cluster
kind create cluster --name new-cluster
```

## 📚 扩展学习资源

### 相关文档
- [kind官方文档](https://kind.sigs.k8s.io/docs/)
- [Kubernetes官方文档](https://kubernetes.io/docs/)
- [Docker文档](https://docs.docker.com/)

### 进阶主题
- 多集群管理
- 网络策略配置
- 存储类和动态供应
- 安全配置和最佳实践
- CI/CD集成方案

---

> **💡 提示**: kind非常适合需要快速创建和销毁Kubernetes集群的开发和测试场景，是CI/CD流水线的理想选择。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日  
**适用范围**: kind v0.20+, Kubernetes v1.25+  
**测试环境**: macOS 13.x, Docker Desktop 4.20+
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
