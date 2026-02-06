# 🚀 minikube macOS本地部署详细指南

> 面向初学者的完整minikube部署教程，从环境准备到高级配置的全步骤指南

## 📋 方案概述

minikube是在本地运行Kubernetes的最简单方式，特别适合学习和开发使用。它创建一个单节点Kubernetes集群，运行在本地虚拟机或容器中。

### 🎯 适用场景
- Kubernetes学习入门
- 应用开发和测试
- 本地环境验证
- 教学演示

### 🔧 技术特点
- **简单易用**：一键部署，自动配置
- **功能完整**：支持大部分Kubernetes特性
- **插件丰富**：内置多种实用插件
- **文档完善**：社区支持和文档丰富

## 🛠️ 环境准备

### 1. 系统要求检查

```bash
# 检查macOS版本
sw_vers
# 推荐：macOS 12.0 (Monterey) 或更高版本

# 检查硬件资源
echo "CPU核心数: $(sysctl -n hw.ncpu)"
echo "内存大小: $(sysctl -n hw.memsize / 1024 / 1024 / 1024)GB"
# 推荐：CPU >= 4核心，内存 >= 8GB

# 检查虚拟化支持
sysctl -a | grep machdep.cpu.features | grep VMX
# 应该输出包含VMX的信息
```

### 2. 必要工具安装

```bash
# 安装Homebrew（如果没有）
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 安装kubectl（Kubernetes命令行工具）
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

## 📦 minikube安装

### 1. 安装minikube

```bash
# 使用Homebrew安装minikube
brew install minikube

# 验证安装
minikube version

# 检查可用驱动
minikube config list
minikube config view
```

### 2. 配置minikube

```bash
# 查看可用的配置选项
minikube config defaults

# 设置默认配置（可选）
minikube config set driver docker
minikube config set memory 6144
minikube config set cpus 4
minikube config set disk-size 20g
minikube config set kubernetes-version v1.28.0

# 查看当前配置
minikube config view
```

## 🚀 集群部署

### 1. 启动minikube集群

```bash
# 启动基础集群
minikube start --driver=docker

# 或指定更详细的配置
minikube start \
  --driver=docker \
  --memory=8192 \
  --cpus=4 \
  --disk-size=20g \
  --kubernetes-version=v1.28.0 \
  --addons=dashboard,metrics-server

# 查看启动过程日志
minikube logs
```

### 2. 验证集群状态

```bash
# 检查集群信息
kubectl cluster-info

# 查看节点状态
kubectl get nodes

# 查看系统Pod
kubectl get pods -A

# 检查集群组件状态
minikube status

# 查看集群详细信息
minikube node list
```

### 3. 访问Dashboard

```bash
# 启动Dashboard
minikube dashboard

# 或者获取Dashboard URL
minikube dashboard --url

# 创建访问令牌（如果需要认证）
kubectl create token default -n kubernetes-dashboard
```

## 🔧 高级配置

### 1. 网络配置

```bash
# 启用Ingress插件
minikube addons enable ingress

# 启用Registry插件
minikube addons enable registry

# 查看所有可用插件
minikube addons list

# 配置端口转发
minikube tunnel
```

### 2. 存储配置

```bash
# 创建持久卷
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /tmp/data
EOF

# 创建存储类
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
EOF
```

### 3. 性能调优

```bash
# 调整Docker资源限制
# Docker Desktop → Preferences → Resources
# 建议设置：CPU 4核，内存 8GB

# minikube资源配置
minikube config set memory 8192
minikube config set cpus 4
minikube config set disk-size 30g

# 重启集群应用新配置
minikube delete
minikube start
```

## 🧪 实战演练

### 1. 部署简单应用

```bash
# 部署nginx应用
kubectl create deployment nginx-demo --image=nginx:latest
kubectl expose deployment nginx-demo --port=80 --type=NodePort

# 获取服务信息
kubectl get services
minikube service nginx-demo --url

# 在浏览器中访问应用
minikube service nginx-demo
```

### 2. 使用本地镜像

```bash
# 构建本地镜像
docker build -t my-app:local .

# 将镜像加载到minikube
minikube image load my-app:local

# 或者使用minikube docker-env
eval $(minikube docker-env)
docker build -t my-app:local .
```

### 3. 数据持久化

```bash
# 创建持久卷声明
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: standard
EOF

# 使用PVC部署应用
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-pvc
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-pvc
  template:
    metadata:
      labels:
        app: nginx-pvc
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        volumeMounts:
        - name: nginx-storage
          mountPath: /usr/share/nginx/html
      volumes:
      - name: nginx-storage
        persistentVolumeClaim:
          claimName: demo-pvc
EOF
```

## 🛠️ 日常管理

### 1. 集群控制

```bash
# 启动集群
minikube start

# 停止集群
minikube stop

# 暂停集群（保留状态）
minikube pause

# 恢复暂停的集群
minikube unpause

# 重启集群
minikube restart
```

### 2. 集群信息

```bash
# 查看集群状态
minikube status

# 查看集群配置
minikube config view

# 查看IP地址
minikube ip

# 查看集群版本
minikube version
kubectl version
```

### 3. 插件管理

```bash
# 查看已启用插件
minikube addons list

# 启用插件
minikube addons enable dashboard
minikube addons enable metrics-server
minikube addons enable ingress

# 禁用插件
minikube addons disable dashboard
```

## 🔍 监控和调试

### 1. 基础监控

```bash
# 查看节点资源使用
kubectl top nodes

# 查看Pod资源使用
kubectl top pods -A

# 查看集群事件
kubectl get events --all-namespaces

# 查看系统日志
minikube logs
```

### 2. 高级调试

```bash
# 进入minikube节点
minikube ssh

# 查看Docker容器
minikube ssh -- docker ps

# 检查系统服务
minikube ssh -- sudo systemctl status kubelet

# 查看网络配置
minikube ssh -- ip addr show
```

### 3. Dashboard使用

```bash
# 启动Dashboard
minikube dashboard

# 启用metrics-server（如果未启用）
minikube addons enable metrics-server

# 查看资源使用图表
# 在Dashboard中导航到工作负载 → Pods
```

## 🧹 清理和维护

### 1. 清理资源

```bash
# 删除所有资源
kubectl delete deployments,services,pods,pvc --all

# 清理特定命名空间
kubectl delete all --all -n default

# 重置集群
minikube delete
minikube start
```

### 2. 集群清理

```bash
# 停止集群
minikube stop

# 删除集群
minikube delete

# 删除特定集群
minikube delete --profile=minikube

# 删除所有集群
minikube delete --all

# 清理缓存
minikube cache delete
```

### 3. 磁盘清理

```bash
# 清理Docker镜像
docker system prune -a

# 清理minikube缓存
minikube cache delete

# 查看磁盘使用
minikube ssh -- df -h

# 清理临时文件
minikube ssh -- sudo rm -rf /tmp/*
```

## 🚨 常见问题解决

### 1. 启动失败问题

```bash
# 问题：驱动不可用
# 解决：检查Docker是否运行
docker info

# 问题：资源不足
# 解决：调整资源配置
minikube config set memory 4096
minikube config set cpus 2

# 问题：网络连接失败
# 解决：重置网络配置
minikube delete
minikube start --force
```

### 2. 网络连接问题

```bash
# 检查集群IP
minikube ip

# 测试连通性
ping $(minikube ip)

# 检查服务端口
minikube service --url <service-name>

# 重启网络插件
minikube addons disable ingress
minikube addons enable ingress
```

### 3. 镜像相关问题

```bash
# 问题：镜像拉取失败
# 解决：配置镜像加速
minikube start --image-mirror-country=cn

# 使用本地镜像
minikube image load <image-name>

# 构建镜像到minikube环境
eval $(minikube docker-env)
docker build -t myapp .
```

### 4. 资源相关问题

```bash
# 检查资源使用
kubectl describe nodes
minikube ssh -- free -h

# 调整资源限制
minikube config set memory 8192
minikube stop && minikube start

# 查看Pod资源请求
kubectl describe pod <pod-name>
```

## 📈 性能优化

### 1. 启动优化

```bash
# 预拉取镜像
minikube start --preload=true

# 跳过预加载（加快启动速度）
minikube start --preload=false

# 指定特定版本
minikube start --kubernetes-version=v1.28.0
```

### 2. 资源优化

```bash
# 配置适当的资源限制
minikube config set memory 6144
minikube config set cpus 4

# 启用性能监控
minikube addons enable metrics-server

# 调整Docker资源
# Docker Desktop → Preferences → Resources
```

### 3. 网络优化

```bash
# 使用高效的网络驱动
minikube start --driver=docker

# 启用网络策略
minikube addons enable ingress

# 配置DNS
minikube ssh -- echo "nameserver 8.8.8.8" | sudo tee -a /etc/resolv.conf
```

## 🎯 最佳实践

### 1. 部署规范
```bash
# 使用命名空间隔离
kubectl create namespace development
kubectl config set-context --current --namespace=development

# 设置资源限制
# 在Deployment中指定requests和limits

# 使用标签管理
# 为所有资源添加环境标签
```

### 2. 安全配置
```bash
# 启用RBAC
minikube start --extra-config=apiserver.authorization-mode=RBAC

# 使用安全镜像
# 优先使用官方和认证的镜像

# 定期更新
minikube update-check
```

### 3. 备份恢复
```bash
# 导出配置
kubectl get all -o yaml > backup.yaml

# 备份持久卷数据
# 定期备份重要数据目录

# 集群配置备份
minikube config view > minikube-config.yaml
```

## 📚 扩展学习

### 相关文档
- [minikube官方文档](https://minikube.sigs.k8s.io/docs/)
- [Kubernetes基础概念](https://kubernetes.io/docs/concepts/)
- [kubectl命令参考](https://kubernetes.io/docs/reference/kubectl/)

### 进阶主题
- Helm包管理
- Ingress控制器配置
- 持久化存储方案
- 监控告警配置
- CI/CD集成

---

> **💡 提示**: minikube最适合学习和开发场景，对于生产环境建议使用完整的Kubernetes发行版。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日  
**适用范围**: minikube v1.32+  
**测试环境**: macOS 13.x, Docker Desktop 4.20+