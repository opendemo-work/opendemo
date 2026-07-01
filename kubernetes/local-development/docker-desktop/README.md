# 🐳 Docker Desktop Kubernetes集成指南

> 一键启用的Kubernetes体验，最适合快速上手和简单开发场景

## 📋 方案概述

Docker Desktop内置了Kubernetes支持，通过简单的界面操作即可启用完整的Kubernetes环境。这是最快速、最简单的本地Kubernetes部署方式。

### 🎯 适用场景
- 快速体验Kubernetes
- 简单应用开发测试
- 学习入门
- 演示和教学

### 🔧 技术特点
- **一键启用**：图形界面操作，无需命令行
- **集成度高**：与Docker环境无缝集成
- **配置简单**：自动配置kubectl和集群连接
- **快速启动**：通常在几分钟内完成启用
- **CLI友好**：提供[专业的Docker CLI集成指南](./docker-cli-integration/README.md)

## 🛠️ 环境准备

### 1. 系统要求检查

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查macOS版本
sw_vers
# 要求：macOS 11.0 (Big Sur) 或更高版本

# 检查硬件资源
echo "CPU核心数: $(sysctl -n hw.ncpu)"
echo "内存大小: $(sysctl -n hw.memsize / 1024 / 1024 / 1024)GB"
# 最低要求：CPU 2核心，内存 4GB
# 推荐配置：CPU 4核心，内存 8GB

# 检查Docker Desktop版本
docker --version
# 要求：Docker Desktop 3.0.0 或更高版本
```

### 2. Docker Desktop安装

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用Homebrew安装Docker Desktop
brew install --cask docker

# 或从官网下载安装
# https://www.docker.com/products/docker-desktop

# 启动Docker Desktop
open -a Docker

# 等待Docker Desktop启动完成
until docker info &> /dev/null; do
    echo "等待Docker Desktop启动..."
    sleep 5
done
echo "Docker Desktop已启动"
```

### 3. Docker资源配置

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 重要：配置足够的系统资源
# Docker Desktop → Preferences → Resources
# 建议配置：
# - CPUs: 4-6核心
# - Memory: 8-12GB
# - Swap: 2-4GB
# - Disk image size: 64GB+

# 验证资源配置
docker info | grep -E "(CPUs|Memory)"
```

## 🚀 Kubernetes启用和配置

### 1. 启用Kubernetes

通过图形界面启用：
1. 打开Docker Desktop
2. 点击右上角的齿轮图标（Settings）
3. 选择"Kubernetes"选项卡
4. 勾选"Enable Kubernetes"
5. 点击"Apply & Restart"

或者使用命令行方式：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 通过修改Docker Desktop配置文件启用
# 配置文件位置：~/Library/Group Containers/group.com.docker/settings.json
# 添加或修改以下内容：
{
  "kubernetesEnabled": true,
  " orchestrator": "swarm"
}
```

### 2. 验证启用状态

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查Kubernetes上下文
kubectl config current-context
# 应该显示：docker-desktop

# 检查集群信息
kubectl cluster-info

# 查看节点状态
kubectl get nodes
# 应该看到一个名为 docker-desktop 的节点

# 查看系统组件
kubectl get pods -n kube-system
```

### 3. 等待初始化完成

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 等待Kubernetes组件启动完成
echo "等待Kubernetes初始化完成..."
until kubectl get nodes | grep -q "Ready"; do
    echo "Kubernetes仍在启动中..."
    sleep 10
done
echo "Kubernetes初始化完成！"

# 检查核心组件状态
kubectl get pods -n kube-system
```

## 🔧 集群配置优化

### 1. 资源配额调整

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 调整系统资源限制
# Docker Desktop → Preferences → Kubernetes
# 或通过修改配置文件：
cat <<EOF > ~/docker-desktop-config.json
{
  "kubernetes": {
    "resources": {
      "memoryMiB": 8192,
      "cpuCount": 4
    }
  }
}
EOF

# 应用配置需要重启Docker Desktop
```

### 2. 网络配置

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查集群网络配置
kubectl cluster-info
kubectl get nodes -o wide

# 查看服务网络
kubectl get services -A

# 查看DNS配置
kubectl get pods -n kube-system | grep dns
kubectl get configmap -n kube-system coredns -o yaml
```

### 3. 存储配置

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查看存储类
kubectl get storageclass

# 默认存储类应该是docker-desktop
# 如果没有，创建默认存储类
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: docker-desktop
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: docker.io/hostpath
EOF
```

## 🧪 基础使用示例

### 1. 简单应用部署

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 部署nginx应用
kubectl create deployment nginx-app --image=nginx:latest

# 暴露服务
kubectl expose deployment nginx-app --port=80 --type=LoadBalancer

# 查看部署状态
kubectl get deployments
kubectl get pods
kubectl get services

# 获取访问地址
kubectl get service nginx-app

# 由于LoadBalancer在Docker Desktop中通过localhost访问
# 实际访问地址是：http://localhost:<nodeport>
```

### 2. Ingress控制器安装

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# Docker Desktop内置的Ingress支持有限
# 可以安装Nginx Ingress Controller

# 安装Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# 等待Ingress控制器就绪
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# 创建测试Ingress
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: localhost
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-app
            port:
              number: 80
EOF

# 测试Ingress访问
curl http://localhost
```

### 3. Dashboard安装和访问

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# Docker Desktop内置简单的Kubernetes UI
# 或安装官方Dashboard
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

# 启动Dashboard代理
kubectl proxy &

# 在浏览器中访问：http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

## 🔧 日常管理操作

### 1. 重启Kubernetes

通过界面：
- Docker Desktop → Troubleshoot → Restart Docker Desktop

或命令行：
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 重置Kubernetes集群
# Docker Desktop → Reset → Reset Kubernetes cluster

# 纯命令行方式（需要重启Docker Desktop）
# 修改配置文件后重启应用
```

### 2. 集群状态检查

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查集群健康状态
kubectl cluster-info
kubectl get nodes
kubectl get componentstatuses

# 检查系统组件
kubectl get pods -n kube-system

# 检查资源使用
kubectl top nodes
kubectl top pods -A
```

### 3. 配置管理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查看kubectl配置
kubectl config view

# 查看当前上下文
kubectl config current-context

# 切换上下文（如果有多个集群）
kubectl config use-context docker-desktop

# 重置kubectl配置
# Docker Desktop会自动管理kubeconfig文件
```

## 🔍 监控和调试

### 1. 基础监控

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 查看节点资源使用
kubectl describe nodes

# 查看Pod资源使用
kubectl top pods

# 查看集群事件
kubectl get events --all-namespaces

# 查看系统日志
kubectl logs -n kube-system -l component=kube-apiserver
```

### 2. Docker Desktop集成监控

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查看Docker Desktop资源使用
# Docker Desktop界面 → Dashboard

# 查看容器统计信息
docker stats

# 查看Docker系统信息
docker system info
```

### 3. 性能分析

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查Docker Desktop性能
# Docker Desktop → Troubleshoot → Diagnose & Feedback

# 分析资源使用情况
kubectl describe nodes docker-desktop
docker system df
```

## 🧹 清理和维护

### 1. 应用清理

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

# 重置到初始状态
# Docker Desktop → Reset → Reset Kubernetes cluster
```

### 2. 系统清理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 清理Docker镜像
docker image prune -a

# 清理未使用的卷
docker volume prune

# 清理构建缓存
docker builder prune

# 查看磁盘使用情况
docker system df
```

### 3. 完全重置

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 重置Kubernetes集群
# Docker Desktop → Reset → Reset Kubernetes cluster

# 或通过命令行（需要重启Docker Desktop）
# 删除相关配置文件
rm -f ~/.kube/config
# 重启Docker Desktop后重新启用Kubernetes
```

## 🚨 常见问题解决

### 1. 启用失败问题

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 问题：Kubernetes启用卡住
# 解决：
# 1. 检查系统资源是否充足
# 2. 重启Docker Desktop
# 3. 重置Kubernetes集群

# 问题：端口冲突
# 解决：
# 检查端口占用
lsof -i :6443
lsof -i :80
lsof -i :443

# 问题：镜像拉取失败
# 解决：
# Docker Desktop → Preferences → Docker Engine
# 添加镜像加速器配置
```

### 2. 连接问题

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 问题：kubectl无法连接集群
# 解决：
kubectl config current-context
# 应该显示 docker-desktop

# 重置kubectl配置
# Docker Desktop会自动管理配置文件

# 问题：服务无法访问
# 解决：
# 检查服务类型和端口
kubectl get services
# LoadBalancer类型的服务通过localhost访问
```

### 3. 性能问题

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 问题：响应缓慢
# 解决：
# 1. 增加Docker Desktop资源配置
# 2. 清理无用的容器和镜像
# 3. 重启Docker Desktop

# 问题：内存不足
# 解决：
# Docker Desktop → Preferences → Resources
# 增加内存分配
```

### 4. 调试命令

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 深入调试
# 检查Docker Desktop日志
# Docker Desktop → Troubleshoot → Show logs

# 检查Kubernetes组件日志
kubectl logs -n kube-system -l component=kube-apiserver

# 检查系统状态
kubectl get componentstatuses
```

## 🎯 最佳实践

### 1. 资源管理
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 合理分配资源
# Docker Desktop → Preferences → Resources
# 根据实际需求调整CPU和内存

# 设置资源限制
# 在应用部署时明确指定requests和limits
```

### 2. 应用部署
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用命名空间隔离
kubectl create namespace dev
kubectl create namespace test

# 标签管理
# 为资源添加环境标签
kubectl label namespace dev environment=development
```

### 3. 安全配置
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 启用RBAC
# Docker Desktop Kubernetes默认启用RBAC

# 网络策略
# 部署网络策略限制流量访问

# 定期更新
# 保持Docker Desktop和Kubernetes版本更新
```

### 4. 备份恢复
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 导出重要配置
kubectl get all -o yaml > backup.yaml

# 备份自定义资源
kubectl get crds -o name | xargs -I {} kubectl get {} -o yaml > crds-backup.yaml

# 备份持久化数据
# 定期备份重要应用数据
```

## 📚 扩展学习

### 相关文档
- [Docker Desktop官方文档](https://docs.docker.com/desktop/)
- [Kubernetes官方文档](https://kubernetes.io/docs/)
- [Docker官方文档](https://docs.docker.com/)

### 进阶主题
- Docker Compose与Kubernetes集成
- 多集群管理
- CI/CD集成
- 监控告警配置
- 安全最佳实践

## ⚠️ 注意事项

### 商业使用限制
- Docker Desktop个人使用免费
- 商业用途需要Docker订阅
- 详细条款请参考Docker官网

### 功能限制
- 不支持某些企业级Kubernetes特性
- 网络功能相对简化
- 存储选项有限制

### 性能考虑
- 资源消耗相对较高
- 不适合大规模应用部署
- 最适合轻量级开发测试

---

> **💡 提示**: Docker Desktop Kubernetes最适合快速体验和简单开发场景，对于复杂的企业级应用建议使用其他部署方案。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日  
**适用范围**: Docker Desktop 4.0+, Kubernetes 1.25+  
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
