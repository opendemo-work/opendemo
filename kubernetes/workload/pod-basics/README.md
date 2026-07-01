# 🐳 Kubernetes Pod基础入门实战

> 全面掌握Kubernetes Pod的核心概念、基础配置和生命周期管理，从零开始构建容器化应用部署

## 📋 案例概述

本案例详细介绍Kubernetes Pod的基础知识和实践操作，帮助初学者快速理解和掌握Pod的核心概念和使用方法。

### 🔧 核心技能点

- **Pod基本概念**: 理解Pod的作用和工作机制
- **基础配置**: Pod的YAML配置和常用字段
- **生命周期管理**: Pod的创建、运行、终止过程
- **多容器Pod**: 在同一个Pod中运行多个容器
- **资源限制**: CPU和内存资源的配置
- **健康检查**: 就绪探针和存活探针配置

### 🎯 适用人群

- Kubernetes初学者
- DevOps工程师
- 系统管理员
- 容器化应用开发者

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查Kubernetes集群状态
kubectl cluster-info
kubectl get nodes

# 创建专用命名空间
kubectl create namespace pod-demo

# 验证kubectl连接
kubectl get namespaces
```

### 2. 基础Pod部署

```bash
# 部署简单的Nginx Pod
kubectl apply -f simple-pod.yaml -n pod-demo

# 查看Pod状态
kubectl get pods -n pod-demo

# 查看Pod详细信息
kubectl describe pod nginx-pod -n pod-demo
```

---

## 📚 详细教程

### 1. Pod核心概念

#### 1.1 什么是Pod

Pod是Kubernetes中最小的可部署单元，可以包含一个或多个容器，这些容器共享存储、网络和配置。

**关键特性**：
- 最小部署单元
- 共享网络命名空间
- 共享存储卷
- 原子性调度

#### 1.2 Pod网络模型

```
Pod内部: localhost通信
Pod之间: 直接IP通信
外部访问: 通过Service
```

### 2. 基础Pod配置

#### 2.1 简单单容器Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  namespace: pod-demo
  labels:
    app: nginx
    version: v1.0
spec:
  containers:
  - name: nginx-container
    image: nginx:1.21
    ports:
    - containerPort: 80
      protocol: TCP
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

#### 2.2 多容器Pod配置

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  namespace: pod-demo
  labels:
    app: web-app
spec:
  containers:
  # 应用容器
  - name: app-container
    image: nginx:1.21
    ports:
    - containerPort: 80
    volumeMounts:
    - name: shared-data
      mountPath: /usr/share/nginx/html
    resources:
      requests:
        memory: "128Mi"
        cpu: "250m"
  
  # 日志收集容器
  - name: log-collector
    image: busybox:1.35
    command: ['sh', '-c']
    args:
    - while true; do
        date >> /shared/logs/app.log;
        sleep 30;
      done
    volumeMounts:
    - name: shared-data
      mountPath: /shared
    resources:
      requests:
        memory: "32Mi"
        cpu: "100m"
  
  # 共享卷
  volumes:
  - name: shared-data
    emptyDir: {}
```

### 3. Pod生命周期管理

#### 3.1 Pod状态详解

```bash
# 查看Pod状态
kubectl get pods -n pod-demo -o wide

# 查看Pod详细状态
kubectl describe pod nginx-pod -n pod-demo

# 实时监控Pod状态
kubectl get pods -n pod-demo --watch
```

**Pod状态说明**：
- **Pending**: Pod已被接受但容器还未准备好
- **Running**: Pod已绑定到节点，所有容器已创建
- **Succeeded**: Pod成功完成退出
- **Failed**: Pod中有容器失败退出
- **Unknown**: 无法获取Pod状态

#### 3.2 Pod重启策略

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: restart-policy-pod
  namespace: pod-demo
spec:
  restartPolicy: Always  # Always, OnFailure, Never
  containers:
  - name: unstable-app
    image: busybox:1.35
    command: ['sh', '-c', 'exit 1']  # 故意失败
```

### 4. 资源管理配置

#### 4.1 CPU和内存限制

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-limited-pod
  namespace: pod-demo
spec:
  containers:
  - name: resource-app
    image: nginx:1.21
    resources:
      # 请求资源（调度依据）
      requests:
        memory: "128Mi"
        cpu: "250m"  # 0.25个CPU核心
      # 限制资源（硬限制）
      limits:
        memory: "256Mi"
        cpu: "500m"   # 0.5个CPU核心
```

#### 4.2 QoS服务质量等级

```yaml
# Guaranteed - 最高等级
apiVersion: v1
kind: Pod
metadata:
  name: qos-guaranteed
  namespace: pod-demo
spec:
  containers:
  - name: app
    image: nginx:1.21
    resources:
      requests:
        memory: "128Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"  # 等于request
        cpu: "250m"      # 等于request

---
# Burstable - 中等等级
apiVersion: v1
kind: Pod
metadata:
  name: qos-burstable
  namespace: pod-demo
spec:
  containers:
  - name: app
    image: nginx:1.21
    resources:
      requests:
        memory: "64Mi"
        cpu: "100m"
      limits:
        memory: "128Mi"  # 大于request
        cpu: "200m"      # 大于request

---
# BestEffort - 最低等级
apiVersion: v1
kind: Pod
metadata:
  name: qos-besteffort
  namespace: pod-demo
spec:
  containers:
  - name: app
    image: nginx:1.21
    # 无资源限制
```

### 5. 健康检查配置

#### 5.1 存活探针(Liveness Probe)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-probe-pod
  namespace: pod-demo
spec:
  containers:
  - name: health-app
    image: nginx:1.21
    livenessProbe:
      # HTTP探针
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 30  # 启动后30秒开始检查
      periodSeconds: 10        # 每10秒检查一次
      timeoutSeconds: 5        # 超时时间5秒
      failureThreshold: 3      # 连续3次失败后重启容器
```

#### 5.2 就绪探针(Readiness Probe)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: readiness-probe-pod
  namespace: pod-demo
spec:
  containers:
  - name: ready-app
    image: nginx:1.21
    readinessProbe:
      # TCP探针
      tcpSocket:
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 5
```

#### 5.3 启动探针(Startup Probe)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: startup-probe-pod
  namespace: pod-demo
spec:
  containers:
  - name: slow-start-app
    image: nginx:1.21
    startupProbe:
      # 执行命令探针
      exec:
        command:
        - cat
        - /tmp/healthy
      initialDelaySeconds: 10
      periodSeconds: 5
      failureThreshold: 30  # 给应用更多启动时间
```

### 6. 环境变量和配置

#### 6.1 环境变量配置

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-var-pod
  namespace: pod-demo
spec:
  containers:
  - name: env-app
    image: nginx:1.21
    env:
    - name: APP_ENV
      value: "production"
    - name: DATABASE_URL
      value: "mysql://db-host:3306/myapp"
    - name: PORT
      value: "8080"
    - name: DEBUG
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: debug-level
```

#### 6.2 ConfigMap引用

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: pod-demo
data:
  app.properties: |
    server.port=8080
    logging.level=INFO
  database.properties: |
    db.host=localhost
    db.port=3306
---
apiVersion: v1
kind: Pod
metadata:
  name: configmap-pod
  namespace: pod-demo
spec:
  containers:
  - name: config-app
    image: nginx:1.21
    envFrom:
    - configMapRef:
        name: app-config
    volumeMounts:
    - name: config-volume
      mountPath: /etc/app-config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

---

## 🔧 实践操作

### 1. Pod部署和验证

```bash
# 1. 创建基础Pod
kubectl apply -f simple-pod.yaml -n pod-demo

# 2. 查看Pod状态
kubectl get pods -n pod-demo

# 3. 查看Pod详细信息
kubectl describe pod nginx-pod -n pod-demo

# 4. 查看Pod日志
kubectl logs nginx-pod -n pod-demo

# 5. 进入Pod执行命令
kubectl exec -it nginx-pod -n pod-demo -- /bin/bash

# 6. 端口转发测试
kubectl port-forward nginx-pod 8080:80 -n pod-demo
```

### 2. 多容器Pod测试

```bash
# 1. 部署多容器Pod
kubectl apply -f multi-container-pod.yaml -n pod-demo

# 2. 查看容器状态
kubectl get pod multi-container-pod -n pod-demo -o jsonpath='{.status.containerStatuses[*].name}'

# 3. 查看特定容器日志
kubectl logs multi-container-pod -n pod-demo -c app-container
kubectl logs multi-container-pod -n pod-demo -c log-collector

# 4. 在不同容器间通信测试
kubectl exec -it multi-container-pod -n pod-demo -c app-container -- curl localhost
kubectl exec -it multi-container-pod -n pod-demo -c log-collector -- cat /shared/logs/app.log
```

### 3. 健康检查验证

```bash
# 1. 部署带健康检查的Pod
kubectl apply -f health-check-pod.yaml -n pod-demo

# 2. 监控探针状态
kubectl describe pod liveness-probe-pod -n pod-demo | grep -A 10 "Liveness"

# 3. 模拟应用故障
kubectl exec -it liveness-probe-pod -n pod-demo -c health-app -- rm /usr/share/nginx/html/index.html

# 4. 观察Pod重启
kubectl get pods liveness-probe-pod -n pod-demo --watch
```

---

## 📊 监控和日志

### 1. Pod监控命令

```bash
# 查看资源使用情况
kubectl top pods -n pod-demo

# 查看Pod事件
kubectl get events -n pod-demo --sort-by='.lastTimestamp'

# 查看Pod YAML配置
kubectl get pod nginx-pod -n pod-demo -o yaml

# 查看Pod JSON格式
kubectl get pod nginx-pod -n pod-demo -o json
```

### 2. 日志管理

```bash
# 查看Pod日志
kubectl logs nginx-pod -n pod-demo

# 实时跟踪日志
kubectl logs -f nginx-pod -n pod-demo

# 查看前100行日志
kubectl logs --tail=100 nginx-pod -n pod-demo

# 查看最近1小时日志
kubectl logs --since=1h nginx-pod -n pod-demo

# 查看特定容器日志（多容器Pod）
kubectl logs multi-container-pod -n pod-demo -c app-container
```

---

## ⚠️ 常见问题和解决方案

### 1. Pod处于Pending状态

**问题现象**: Pod长时间处于Pending状态，无法调度

**可能原因**:
- 资源不足（CPU、内存）
- 节点选择器不匹配
- 污点和容忍度配置问题
- 存储卷绑定失败

**解决步骤**:
```bash
# 1. 检查Pod事件
kubectl describe pod <pod-name> -n <namespace>

# 2. 检查节点资源
kubectl describe nodes

# 3. 检查资源配额
kubectl describe resourcequota -n <namespace>

# 4. 查看调度器日志
kubectl logs -n kube-system <scheduler-pod>
```

### 2. Pod频繁重启

**问题现象**: Pod不断重启，状态不稳定

**可能原因**:
- 应用程序崩溃
- 健康检查配置不当
- 资源限制过严
- 存活探针过于敏感

**解决步骤**:
```bash
# 1. 查看Pod重启原因
kubectl describe pod <pod-name> -n <namespace> | grep -A 20 "Last State"

# 2. 检查容器日志
kubectl logs <pod-name> -n <namespace> --previous

# 3. 调整健康检查配置
# 修改探针的initialDelaySeconds和periodSeconds参数

# 4. 检查资源使用情况
kubectl top pod <pod-name> -n <namespace>
```

### 3. 容器启动失败

**问题现象**: Pod状态显示ContainerCreating或CrashLoopBackOff

**解决步骤**:
```bash
# 1. 检查详细错误信息
kubectl describe pod <pod-name> -n <namespace>

# 2. 检查镜像拉取状态
kubectl get events --field-selector involvedObject.name=<pod-name>

# 3. 验证镜像是否存在
docker pull <image-name>:<tag>

# 4. 检查镜像拉取密钥
kubectl get secrets -n <namespace>
```

---

## 🧪 实践练习

### 练习1：基础Pod配置
创建一个包含Nginx和BusyBox两个容器的Pod，配置共享存储卷，实现日志收集功能。

### 练习2：资源管理实践
配置不同资源限制的Pod，观察QoS等级的变化和资源使用情况。

### 练习3：健康检查配置
为应用配置完整的健康检查体系，包括存活探针、就绪探针和启动探针。

### 练习4：故障排查演练
模拟各种Pod故障场景，练习系统化的故障诊断和修复技能。

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes Pod官方文档](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Pod生命周期](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [容器探针](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)

### 相关案例
- [Deployment基础配置](../deployment-basics/)
- [StatefulSet有状态应用](../statefulset-basics/)
- [DaemonSet节点部署](../daemonset-basics/)

### 进阶主题
- Pod安全策略
- Pod中断预算
- Pod亲和性和反亲和性
- Pod拓扑分布约束

---

## 📋 清理资源

```bash
# 删除所有测试Pod
kubectl delete pods --all -n pod-demo

# 删除ConfigMap
kubectl delete configmap app-config -n pod-demo

# 删除命名空间
kubectl delete namespace pod-demo
```

---

> **💡 提示**: Pod是Kubernetes的基础单元，建议先熟练掌握Pod的各种配置再学习更高级的工作负载资源。在生产环境中使用时要注意资源限制和健康检查配置。
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 Kubernetes 核心概念。

### 2. 适用场景

- 场景 1：开发与测试
- 场景 2：生产环境参考
- 场景 3：故障排查

## 💻 代码示例

### 基本命令

```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
