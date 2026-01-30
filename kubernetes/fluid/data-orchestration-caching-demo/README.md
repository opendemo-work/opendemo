# Kubernetes 数据编排与缓存 Demo

本演示展示如何在 Kubernetes 中通过 ConfigMap 和 EmptyDir 卷实现简单的数据编排与临时缓存机制，适用于初学者理解 Pod 内数据共享和配置管理。

## 学习目标

- 理解 ConfigMap 如何将配置数据注入到容器中
- 掌握使用 EmptyDir 实现 Pod 内容器间临时数据共享（缓存）
- 熟悉 Kubernetes 卷挂载的基本语法和最佳实践
- 能够部署并验证多容器 Pod 的数据交互行为

## 环境要求

- 操作系统：Windows、Linux 或 macOS
- kubectl：v1.20 或更高版本
- Minikube：v1.25 或更高版本（用于本地集群）
- Docker：v20.10 或更高版本

## 安装依赖的详细步骤

1. **安装 Docker**
   - 下载地址：https://docs.docker.com/get-docker/
   - 安装后运行 `docker --version` 验证

2. **安装 kubectl**
   ```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/$(uname | tr '[:upper:]' '[:lower:]')/amd64/kubectl"
   chmod +x kubectl
   sudo mv kubectl /usr/local/bin/
   ```

3. **安装 Minikube**
   ```bash
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   sudo install minikube-linux-amd64 /usr/local/bin/minikube
   ```

4. **启动本地 Kubernetes 集群**
   ```bash
   minikube start
   ```

## 文件说明

- `demo-pod.yaml`：定义一个包含两个容器的 Pod，使用 ConfigMap 提供配置，并通过 EmptyDir 共享缓存数据
- `dependency`：项目依赖声明文件

## 逐步实操指南

### 步骤 1：创建 ConfigMap

```bash
kubectl create configmap app-config --from-literal=app_env=development --from-literal=cache_ttl=60
```

**预期输出**：
```
configmap/app-config created
```

### 步骤 2：应用 Pod 配置

```bash
kubectl apply -f demo-pod.yaml
```

**预期输出**：
```
pod/data-orchestration-pod created
```

### 步骤 3：查看 Pod 状态

```bash
kubectl get pod data-orchestration-pod
```

**预期输出**：
```
NAME                          READY   STATUS    RESTARTS   AGE
data-orchestration-pod        2/2     Running   0          30s
```

### 步骤 4：进入 writer 容器写入缓存数据

```bash
kubectl exec -it data-orchestration-pod -c writer -- sh -c "echo 'cached data' > /cache/data.txt"
```

### 步骤 5：从 reader 容器读取缓存数据

```bash
kubectl exec -it data-orchestration-pod -c reader -- cat /cache/data.txt
```

**预期输出**：
```
cached data
```

### 步骤 6：查看环境变量（来自 ConfigMap）

```bash
kubectl exec -it data-orchestration-pod -c writer -- printenv | grep APP_
```

**预期输出**：
```
APP_ENV=development
CACHE_TTL=60
```

## 代码解析

### `demo-pod.yaml` 关键段解释

- `volumes`: 定义了两个卷：
  - `app-config-volume`：从 ConfigMap 挂载只读配置
  - `cache-volume`：使用 EmptyDir 创建 Pod 级临时存储，容器间共享
- `volumeMounts`: 将卷挂载到容器指定路径
- `envFrom`: 从 ConfigMap 自动注入环境变量，前缀为 `APP_`
- 两个容器 (`writer` 和 `reader`) 共享同一个 EmptyDir，实现缓存数据传递

## 预期输出示例

```bash
$ kubectl exec -it data-orchestration-pod -c reader -- cat /cache/data.txt
cached data
```

```bash
$ kubectl exec -it data-orchestration-pod -c writer -- printenv | grep APP_
APP_ENV=development
CACHE_TTL=60
```

## 常见问题解答

**Q: 如果 Pod 被删除，缓存数据会保留吗？**
A: 不会。EmptyDir 是临时存储，Pod 删除后数据即丢失。如需持久化，请使用 PersistentVolume。

**Q: ConfigMap 修改后，Pod 内容会自动更新吗？**
A: 挂载为文件时会异步更新（延迟约1分钟），但环境变量不会动态更新，需重启 Pod。

**Q: 可以跨 Pod 共享 EmptyDir 吗？**
A: 不可以。EmptyDir 仅限同一 Pod 内容器共享。

## 扩展学习建议

- 学习使用 PersistentVolume 和 PersistentVolumeClaim 实现持久化存储
- 探索 Init Containers 在数据初始化中的应用
- 尝试使用 Redis 或 Memcached 替代 EmptyDir 实现真正的缓存服务
- 研究 Kubernetes 中的 StatefulSet 与有状态应用管理