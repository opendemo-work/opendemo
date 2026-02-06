# 🐄 k3s macOS轻量级部署指南

> 轻量级Kubernetes发行版，专为资源受限环境和边缘计算设计

## 📋 方案概述

k3s是Rancher Labs推出的轻量级Kubernetes发行版，打包了所有必要的组件，安装包小于100MB，内存占用极低，非常适合开发测试和边缘计算场景。

### 🎯 适用场景
- 资源受限的开发环境
- 边缘计算和IoT设备
- CI/CD流水线
- 本地快速测试
- 学习和实验环境

### 🔧 技术特点
- **超轻量级**：安装包小于100MB
- **低资源消耗**：内存占用仅512MB左右
- **快速启动**：启动时间通常在30秒内
- **功能完整**：包含标准Kubernetes核心功能
- **易于安装**：单个二进制文件，一键安装

## 🛠️ 环境准备

### 1. 系统要求检查

```bash
# 检查macOS版本
sw_vers
# 支持：macOS 10.15 (Catalina) 或更高版本

# 检查硬件资源
echo "CPU核心数: $(sysctl -n hw.ncpu)"
echo "内存大小: $(sysctl -n hw.memsize / 1024 / 1024 / 1024)GB"
# 最低要求：CPU 2核心，内存 2GB
# 推荐配置：CPU 4核心，内存 4GB

# 检查系统架构
uname -m
# 支持：x86_64, arm64 (Apple Silicon)
```

### 2. 必要工具安装

```bash
# 安装Homebrew（如果没有）
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 安装kubectl
brew install kubectl

# 验证kubectl安装
kubectl version --client

# 安装必要的系统工具
brew install curl wget
```

## 📦 k3s安装

### 1. 官方安装脚本安装

```bash
# 使用官方安装脚本（推荐）
curl -sfL https://get.k3s.io | sh -

# 安装特定版本
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.28.3+k3s1 sh -

# 安装时指定配置
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik --write-kubeconfig-mode 644" sh -

# 验证安装
sudo k3s --version
sudo systemctl status k3s
```

### 2. Homebrew安装

```bash
# 使用Homebrew安装
brew install k3s

# 启动k3s服务
k3s server &

# 等待服务启动
sleep 30

# 验证集群状态
kubectl cluster-info
```

### 3. 手动安装

```bash
# 下载二进制文件
wget https://github.com/k3s-io/k3s/releases/download/v1.28.3+k3s1/k3s
chmod +x k3s
sudo mv k3s /usr/local/bin/

# 创建配置目录
sudo mkdir -p /etc/rancher/k3s

# 创建基本配置文件
cat <<EOF | sudo tee /etc/rancher/k3s/config.yaml
write-kubeconfig-mode: "0644"
disable:
  - traefik
  - servicelb
EOF

# 启动k3s
sudo k3s server --config /etc/rancher/k3s/config.yaml &

# 等待启动完成
sleep 30
```

## 🚀 集群配置和验证

### 1. 基础配置

```bash
# 配置kubectl访问权限
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER ~/.kube/config
chmod 600 ~/.kube/config

# 验证kubectl配置
kubectl config current-context
kubectl cluster-info

# 查看节点信息
kubectl get nodes

# 查看系统组件
kubectl get pods -n kube-system
```

### 2. 服务配置

```bash
# 启用Traefik Ingress Controller
sudo k3s server --disable servicelb &

# 或禁用默认Ingress Controller
sudo k3s server --disable traefik --disable servicelb &

# 配置外部数据库（可选）
# export K3S_DATASTORE_ENDPOINT='mysql://username:password@tcp(hostname:3306)/database-name'
# sudo k3s server
```

### 3. 网络配置

```bash
# 配置自定义网络
cat <<EOF | sudo tee /etc/rancher/k3s/config.yaml
cluster-cidr: "10.42.0.0/16"
service-cidr: "10.43.0.0/16"
cluster-dns: "10.43.0.10"
cluster-domain: "cluster.local"
EOF

# 重启k3s应用配置
sudo systemctl restart k3s
```

## 🔧 高级配置选项

### 1. 资源限制配置

```bash
# 配置资源限制
cat <<EOF | sudo tee /etc/rancher/k3s/config.yaml
kubelet-arg:
  - "kube-reserved=cpu=200m,memory=256Mi"
  - "system-reserved=cpu=100m,memory=128Mi"
  - "eviction-hard=memory.available<200Mi"
node-label:
  - "node-role.kubernetes.io/worker=true"
node-taint:
  - "node-role.kubernetes.io/master=true:NoSchedule"
EOF
```

### 2. 存储配置

```bash
# 配置本地存储类
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
EOF

# 创建本地持久卷
cat <<EOF | kubectl apply -f -
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
  storageClassName: local-storage
  hostPath:
    path: /tmp/k3s-pv
EOF
```

### 3. 安全配置

```bash
# 启用审计日志
cat <<EOF | sudo tee /etc/rancher/k3s/config.yaml
kube-apiserver-arg:
  - "audit-log-path=/var/log/k3s-audit.log"
  - "audit-policy-file=/etc/rancher/k3s/audit-policy.yaml"
EOF

# 创建审计策略文件
cat <<EOF | sudo tee /etc/rancher/k3s/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
EOF
```

## 🧪 实战应用示例

### 1. 基础应用部署

```bash
# 部署简单的nginx应用
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: NodePort
EOF

# 验证部署
kubectl get deployments
kubectl get pods
kubectl get services

# 测试服务访问
NODE_PORT=$(kubectl get service nginx-service -o jsonpath='{.spec.ports[0].nodePort}')
curl http://localhost:$NODE_PORT
```

### 2. Ingress配置示例

```bash
# 安装Traefik Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v2.10/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v2.10/docs/content/reference/dynamic-configuration/kubernetes-crd-rbac.yml

# 部署Traefik
helm repo add traefik https://traefik.github.io/charts
helm install traefik traefik/traefik

# 创建Ingress资源
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  annotations:
    kubernetes.io/ingress.class: traefik
spec:
  rules:
  - host: nginx.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-service
            port:
              number: 80
EOF

# 测试Ingress访问
curl -H "Host: nginx.local" http://localhost
```

### 3. Helm应用部署

```bash
# 安装Helm
brew install helm

# 添加常用仓库
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
helm repo update

# 部署WordPress示例
helm install my-wordpress bitnami/wordpress \
  --set wordpressUsername=admin \
  --set wordpressPassword=password \
  --set mariadb.auth.rootPassword=secretpassword

# 查看部署状态
kubectl get pods
kubectl get services

# 获取访问信息
echo "WordPress URL: http://localhost:$(kubectl get svc my-wordpress -o jsonpath='{.spec.ports[0].nodePort}')"
echo "WordPress Admin: admin"
echo "WordPress Password: password"
```

## 🛠️ 日常管理操作

### 1. 服务管理

```bash
# 启动k3s服务
sudo systemctl start k3s

# 停止k3s服务
sudo systemctl stop k3s

# 重启k3s服务
sudo systemctl restart k3s

# 查看服务状态
sudo systemctl status k3s

# 查看服务日志
sudo journalctl -u k3s -f
```

### 2. 集群信息查看

```bash
# 查看集群信息
kubectl cluster-info

# 查看节点详细信息
kubectl describe nodes

# 查看系统组件
kubectl get pods -n kube-system

# 查看集群版本
kubectl version

# 查看API资源
kubectl api-resources
```

### 3. 资源管理

```bash
# 查看资源使用情况
kubectl top nodes
kubectl top pods

# 查看事件日志
kubectl get events --all-namespaces

# 查看Pod详细信息
kubectl describe pod <pod-name>

# 查看日志
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # 实时日志
```

## 🔍 监控和调试

### 1. 基础监控

```bash
# 安装metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# 等待metrics-server就绪
kubectl wait deployment metrics-server -n kube-system --for condition=Available=True --timeout=300s

# 查看资源使用
kubectl top nodes
kubectl top pods
```

### 2. 日志收集

```bash
# 查看系统日志
sudo journalctl -u k3s

# 查看容器日志
kubectl logs -n kube-system -l app.kubernetes.io/name=traefik

# 导出所有日志
kubectl get events --all-namespaces > events.log
kubectl get pods --all-namespaces > pods.log
```

### 3. 性能分析

```bash
# 检查节点资源
kubectl describe nodes

# 检查Pod资源请求
kubectl describe pod <pod-name>

# 分析资源使用趋势
# 可以集成Prometheus和Grafana进行详细监控
```

## 🧹 清理和维护

### 1. 应用清理

```bash
# 删除所有应用资源
kubectl delete deployments,services,ingresses --all

# 清理特定命名空间
kubectl delete all --all -n default

# 删除Helm releases
helm list
helm uninstall <release-name>
```

### 2. 系统清理

```bash
# 停止k3s服务
sudo systemctl stop k3s

# 删除k3s数据
sudo rm -rf /var/lib/rancher/k3s
sudo rm -rf /etc/rancher/k3s

# 删除配置文件
rm -f ~/.kube/config

# 卸载k3s（使用官方脚本）
/usr/local/bin/k3s-uninstall.sh
```

### 3. 磁盘清理

```bash
# 清理Docker镜像（如果使用）
docker system prune -a

# 清理临时文件
sudo rm -rf /tmp/k3s-*

# 查看磁盘使用
df -h
sudo du -sh /var/lib/rancher/k3s
```

## 🚨 常见问题解决

### 1. 启动问题

```bash
# 问题：端口被占用
# 解决：检查端口使用
sudo lsof -i :6443
sudo netstat -tlnp | grep 6443

# 问题：权限不足
# 解决：检查文件权限
sudo chown root:root /usr/local/bin/k3s
sudo chmod 755 /usr/local/bin/k3s

# 问题：配置文件错误
# 解决：检查配置语法
sudo k3s check-config
```

### 2. 网络问题

```bash
# 问题：Pod无法访问外部网络
# 解决：检查网络配置
kubectl get pods -n kube-system
kubectl logs -n kube-system -l k8s-app=kube-dns

# 问题：服务无法访问
# 解决：检查服务配置
kubectl describe service <service-name>
kubectl get endpoints <service-name>
```

### 3. 资源问题

```bash
# 问题：内存不足
# 解决：调整资源限制
# 编辑 /etc/rancher/k3s/config.yaml
# 添加资源限制配置

# 问题：磁盘空间不足
# 解决：清理无用资源
sudo journalctl --vacuum-size=100M
sudo rm -rf /var/lib/rancher/k3s/agent/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/*
```

### 4. 调试命令

```bash
# 深入调试
# 检查k3s进程
ps aux | grep k3s

# 检查系统资源
top
free -h
df -h

# 检查网络连接
ss -tlnp | grep k3s
```

## 🎯 性能优化

### 1. 启动优化

```bash
# 禁用不必要的组件
sudo k3s server \
  --disable traefik \
  --disable servicelb \
  --disable local-storage \
  --disable metrics-server &

# 使用轻量级CNI
# k3s默认使用flannel，已经很轻量
```

### 2. 资源优化

```bash
# 配置资源限制
cat <<EOF | sudo tee /etc/rancher/k3s/config.yaml
kubelet-arg:
  - "kube-reserved=cpu=100m,memory=128Mi"
  - "system-reserved=cpu=50m,memory=64Mi"
  - "eviction-hard=memory.available<100Mi"
EOF

# 重启应用配置
sudo systemctl restart k3s
```

### 3. 存储优化

```bash
# 使用tmpfs提高性能
sudo mount -t tmpfs -o size=1G tmpfs /tmp/k3s-storage

# 配置日志轮转
sudo tee /etc/logrotate.d/k3s <<EOF
/var/log/k3s*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

## 🎯 最佳实践

### 1. 部署规范
```bash
# 使用命名空间
kubectl create namespace development
kubectl create namespace production

# 设置资源限制
# 在所有Deployment中明确指定requests和limits

# 使用标签管理
# 为资源添加环境、版本、应用等标签
```

### 2. 安全配置
```bash
# 启用RBAC
# k3s默认启用RBAC

# 配置网络策略
# 限制不必要的网络访问

# 定期更新
# 关注k3s版本更新和安全补丁
```

### 3. 备份策略
```bash
# 备份重要配置
sudo cp -r /etc/rancher/k3s /backup/k3s-config-$(date +%Y%m%d)

# 备份etcd数据
sudo cp -r /var/lib/rancher/k3s/server/db /backup/k3s-db-$(date +%Y%m%d)

# 导出应用配置
kubectl get all -o yaml > backup-$(date +%Y%m%d).yaml
```

## 📚 扩展学习

### 相关文档
- [k3s官方文档](https://docs.k3s.io/)
- [Rancher文档](https://rancher.com/docs/)
- [Kubernetes官方文档](https://kubernetes.io/docs/)

### 进阶主题
- 多节点集群部署
- 边缘计算场景应用
- 与IoT设备集成
- Rancher管理平台
- 安全加固配置

---

> **💡 提示**: k3s是资源受限环境的理想选择，特别适合边缘计算、CI/CD和快速原型开发场景。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日  
**适用范围**: k3s v1.25+  
**测试环境**: macOS 13.x (Intel/Apple Silicon)