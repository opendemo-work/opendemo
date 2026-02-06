# 🐳 Docker CLI 与 Docker Desktop Kubernetes 集成完全指南

> 为已安装 Docker Desktop 的 macOS 用户提供专业级 Docker CLI 与 Kubernetes 集成方案

## 🎯 面向对象和特点

### 🎯 目标用户群体
本指南特别适用于以下场景：
- ✅ **macOS环境**
- ✅ **Docker Desktop v4.0+**
- ✅ **基础 Kubernetes 学习/应用开发场景**
- ✅ **简单工作或业余探索（0企业支持必要场景，特别如笔记本/闲时光偶尔处理）**

### 🌟 本指南特色
- **CLI 优先**：重点介绍 Docker CLI 与 Kubernetes 的集成操作
- **实用性强**：所有命令均可直接在终端执行
- **场景导向**：针对 macOS + Docker Desktop 的特定优化
- **问题导向**：包含常见问题的详细解决方案

## 🛠️ Docker CLI 环境准备

### 1. Docker CLI 基础环境验证

```bash
# 验证 Docker CLI 安装状态
docker --version
docker-compose --version
docker info

# 检查 Docker Desktop 运行状态
docker info | grep -E "(Server Version|Operating System|Kernel Version)"

# 验证 Docker CLI 与 Docker Desktop 连接
docker context ls
docker context use desktop-linux  # 确保使用 Docker Desktop 上下文
```

### 2. Docker CLI 资源配置优化

```bash
# 查看当前 Docker 资源分配
docker info | grep -E "(CPUs|Memory|Total Memory)"

# Docker CLI 资源监控命令
docker stats --no-stream  # 单次查看资源使用
docker system df          # 查看磁盘使用情况
docker system info        # 详细系统信息

# Docker CLI 资源清理
docker system prune -a --volumes  # 清理所有未使用资源
docker builder prune              # 清理构建缓存
docker volume ls                  # 查看所有卷
```

### 3. Docker CLI 与 Kubernetes 集成配置

```bash
# 验证 kubectl 是否通过 Docker Desktop 安装
kubectl version --client
which kubectl  # 应该指向 Docker Desktop 的 kubectl

# 检查 Kubernetes 上下文配置
kubectl config view
kubectl config current-context  # 应该显示 docker-desktop

# Docker CLI 管理 Kubernetes 集群
docker context ls  # 查看所有 Docker 上下文
docker context use desktop-linux  # 切换到 Docker Desktop 上下文
```

## 🚀 Docker Desktop Kubernetes CLI 操作

### 1. Kubernetes 集群状态管理

```bash
# 启用 Kubernetes（通过 Docker CLI）
# 注意：这需要先在 Docker Desktop GUI 中启用
# 但可以通过 CLI 验证和管理

# 验证 Kubernetes 集群状态
kubectl cluster-info
kubectl get nodes
kubectl get componentstatuses

# Docker CLI 辅助检查
docker info | grep -A 10 "Kubernetes"
```

### 2. Docker CLI 与 Kubernetes 资源交互

```bash
# 通过 Docker CLI 构建镜像并部署到 Kubernetes
# 1. 构建应用镜像
docker build -t my-app:latest .

# 2. 部署到 Kubernetes
kubectl create deployment my-app --image=my-app:latest

# 3. 暴露服务
kubectl expose deployment my-app --port=80 --type=LoadBalancer

# 4. 验证部署
kubectl get deployments
kubectl get pods
kubectl get services
```

### 3. Docker CLI 镜像管理与 Kubernetes 集成

```bash
# Docker CLI 镜像操作
docker images  # 查看本地镜像
docker pull nginx:latest  # 拉取镜像
docker tag nginx:latest my-nginx:latest  # 标记镜像

# 将本地镜像部署到 Kubernetes
kubectl create deployment nginx-test --image=my-nginx:latest

# Docker CLI 清理镜像
docker image prune -a  # 清理未使用的镜像
docker rmi <image-id>  # 删除特定镜像
```

## 🔧 Docker Desktop Kubernetes 高级配置

### 1. 通过 Docker CLI 配置 Kubernetes 资源

```bash
# Docker CLI 管理 Kubernetes 资源
# 创建命名空间
kubectl create namespace dev
kubectl create namespace prod

# Docker CLI 验证资源配置
docker info | grep -A 5 "Resources"

# Kubernetes 资源配额设置
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: dev
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
EOF
```

### 2. Docker CLI 网络配置管理

```bash
# Docker 网络与 Kubernetes 服务集成
# 查看 Docker 网络
docker network ls

# Kubernetes 服务配置
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: docker-bridge-service
spec:
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer
EOF

# Docker CLI 测试网络连通性
docker run --rm busybox ping -c 3 kubernetes.default
```

### 3. Docker CLI 存储卷管理

```bash
# Docker 卷与 Kubernetes PVC 集成
# 创建 Docker 卷
docker volume create my-data-volume

# Kubernetes PVC 配置
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: docker-volume-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
EOF

# 在 Pod 中使用 Docker 卷
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: volume-test
spec:
  containers:
  - name: test-container
    image: busybox
    command: ["sleep", "3600"]
    volumeMounts:
    - name: docker-volume
      mountPath: /data
  volumes:
  - name: docker-volume
    persistentVolumeClaim:
      claimName: docker-volume-claim
EOF
```

## 🧪 Docker CLI 开发工作流

### 1. 本地开发与测试流程

```bash
# 完整的 Docker CLI + Kubernetes 开发流程

# 1. 代码开发阶段
# 使用 Docker CLI 构建和测试
docker build -t my-app:dev .
docker run -p 8080:80 my-app:dev

# 2. Kubernetes 测试阶段
kubectl create deployment my-app-dev --image=my-app:dev
kubectl expose deployment my-app-dev --port=80 --target-port=8080 --type=LoadBalancer

# 3. 验证和调试
kubectl get pods
kubectl logs deployment/my-app-dev
kubectl port-forward deployment/my-app-dev 8080:8080

# 4. 清理测试环境
kubectl delete deployment my-app-dev
kubectl delete service my-app-dev
```

### 2. Docker Compose 与 Kubernetes 集成

```bash
# Docker Compose 转 Kubernetes 部署
# 1. 创建 docker-compose.yml
cat <<EOF > docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
  api:
    image: my-api:latest
    ports:
      - "8080:8080"
EOF

# 2. 使用 kompose 转换（需要安装 kompose）
# brew install kompose
kompose convert -f docker-compose.yml

# 3. 部署到 Kubernetes
kubectl apply -f .
```

### 3. Docker CLI 调试和监控

```bash
# Docker CLI 调试 Kubernetes 应用
# 实时日志查看
kubectl logs -f deployment/my-app

# 进入容器调试
kubectl exec -it deployment/my-app -- sh

# Docker CLI 性能监控
docker stats $(docker ps --format '{{.ID}}')
kubectl top pods

# 资源使用分析
kubectl describe nodes
docker system df -v
```

## 🚨 Docker CLI 常见问题解决

### 1. Docker Desktop Kubernetes 连接问题

```bash
# 问题：kubectl 无法连接到 Docker Desktop Kubernetes
# 解决方案：

# 1. 检查 Docker Desktop 状态
docker info | grep -i kubernetes

# 2. 重置 kubectl 配置
kubectl config use-context docker-desktop
kubectl config set-cluster docker-desktop --server=https://kubernetes.docker.internal:6443

# 3. 验证连接
kubectl cluster-info
kubectl get nodes
```

### 2. Docker CLI 镜像拉取问题

```bash
# 问题：Kubernetes 无法拉取镜像
# 解决方案：

# 1. 使用本地镜像
docker build -t my-app:local .
kubectl create deployment my-app --image=my-app:local

# 2. 配置镜像拉取策略
kubectl patch deployment my-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"my-app","imagePullPolicy":"IfNotPresent"}]}}}}'

# 3. 检查镜像仓库配置
docker info | grep -i registry
```

### 3. Docker CLI 资源不足问题

```bash
# 问题：Docker Desktop 资源不足导致 Kubernetes 性能问题
# 解决方案：

# 1. Docker CLI 资源监控
docker stats --no-stream
docker system df

# 2. 清理 Docker 资源
docker system prune -a --volumes -f

# 3. 调整 Docker Desktop 资源分配
# 通过 Docker Desktop GUI 或配置文件调整：
# ~/Library/Group Containers/group.com.docker/settings.json
```

### 4. Docker CLI 网络问题

```bash
# 问题：Kubernetes 服务无法从 Docker 容器访问
# 解决方案：

# 1. 检查网络配置
docker network ls
kubectl get services

# 2. 测试网络连通性
docker run --rm busybox wget -qO- http://kubernetes.default

# 3. 配置服务访问
kubectl port-forward service/my-service 8080:80
```

## 🎯 Docker CLI 最佳实践

### 1. 资源管理最佳实践

```bash
# Docker CLI 资源管理规范
# 1. 合理设置资源限制
kubectl set resources deployment my-app \
  --requests=cpu=100m,memory=128Mi \
  --limits=cpu=200m,memory=256Mi

# 2. 定期清理资源
# 创建清理脚本
cat <<'EOF' > docker-k8s-cleanup.sh
#!/bin/bash
echo "清理 Docker 资源..."
docker system prune -af --volumes
echo "清理 Kubernetes 资源..."
kubectl delete pods --field-selector=status.phase==Succeeded
kubectl delete pods --field-selector=status.phase==Failed
EOF
chmod +x docker-k8s-cleanup.sh
```

### 2. 开发工作流最佳实践

```bash
# Docker CLI 开发工作流模板
# 1. 开发环境初始化
alias kdev='kubectl config use-context docker-desktop'

# 2. 快速部署命令
alias kdeploy='kubectl apply -f k8s/'

# 3. 日志查看快捷方式
alias klogs='kubectl logs -f'

# 4. 资源监控
alias ktop='kubectl top pods'

# 5. 环境清理
alias kclean='kubectl delete all --all'
```

### 3. 安全配置最佳实践

```bash
# Docker CLI 安全配置
# 1. 启用 RBAC
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dev-user
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: dev-role
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "create", "update", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-rolebinding
  namespace: default
subjects:
- kind: ServiceAccount
  name: dev-user
  namespace: default
roleRef:
  kind: Role
  name: dev-role
  apiGroup: rbac.authorization.k8s.io
EOF

# 2. 网络策略配置
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF
```

## 📚 扩展学习资源

### Docker CLI 相关工具
```bash
# 推荐的 Docker CLI 扩展工具
brew install kubectl  # Kubernetes CLI
brew install kubectx  # Kubernetes 上下文切换
brew install kubens   # Kubernetes 命名空间切换
brew install stern    # 多 Pod 日志查看
brew install k9s      # Kubernetes CLI 管理工具
```

### 学习路径建议
1. **基础阶段**：熟练掌握 Docker CLI 基本命令
2. **集成阶段**：学习 Docker CLI 与 Kubernetes 的协同工作
3. **进阶阶段**：掌握复杂场景下的问题诊断和解决
4. **专家阶段**：优化工作流，建立自动化运维体系

---

> **💡 提示**: 本指南专注于 Docker CLI 与 Docker Desktop Kubernetes 的集成使用，适合已经熟悉 Docker 基础操作的用户深入学习 Kubernetes。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日  
**适用环境**: macOS + Docker Desktop 4.0+  
**Kubernetes版本**: 1.25+