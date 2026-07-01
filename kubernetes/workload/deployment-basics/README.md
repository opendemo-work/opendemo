# 🚀 Kubernetes Deployment基础实战

> 深入学习Kubernetes Deployment的核心功能：滚动更新、回滚操作、自动扩缩容等应用部署管理技能

## 📋 案例概述

本案例详细介绍Kubernetes Deployment的基础知识和实践操作，帮助用户理解和掌握应用部署管理的核心技能。

### 🔧 核心技能点

- **Deployment基本概念**: 理解Deployment的作用和工作机制
- **滚动更新**: 零停机应用升级策略
- **版本回滚**: 快速恢复到历史版本
- **自动扩缩容**: 副本数量的动态调整
- **更新策略**: 不同的部署策略配置
- **健康检查集成**: 与Pod健康检查的协同工作

### 🎯 适用人群

- 有一定Kubernetes经验的开发者
- DevOps工程师
- 应用运维人员
- CI/CD流程设计者

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查Kubernetes集群状态
kubectl cluster-info
kubectl get nodes

# 创建专用命名空间
kubectl create namespace deployment-demo

# 验证Deployment API支持
kubectl api-resources | grep deployment
```

### 2. 基础Deployment部署

```bash
# 部署简单的Nginx应用
kubectl apply -f nginx-deployment.yaml -n deployment-demo

# 查看Deployment状态
kubectl get deployments -n deployment-demo

# 查看相关的ReplicaSet和Pod
kubectl get rs,pods -n deployment-demo
```

---

## 📚 详细教程

### 1. Deployment核心概念

#### 1.1 什么是Deployment

Deployment为Pod和ReplicaSet提供声明式的更新能力，是Kubernetes中最常用的工作负载资源。

**关键特性**：
- 声明式应用管理
- 滚动更新支持
- 版本历史记录
- 自动回滚能力
- 扩缩容管理

#### 1.2 Deployment工作原理

```
Deployment → ReplicaSet → Pod
     ↓           ↓         ↓
  声明期望状态  管理副本数   运行容器
```

### 2. 基础Deployment配置

#### 2.1 简单Deployment配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: deployment-demo
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
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

#### 2.2 带健康检查的Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-check-deployment
  namespace: deployment-demo
  labels:
    app: health-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: health-app
  template:
    metadata:
      labels:
        app: health-app
    spec:
      containers:
      - name: health-app
        image: nginx:1.21
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
```

### 3. 滚动更新配置

#### 3.1 更新策略配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rolling-update-deployment
  namespace: deployment-demo
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1      # 最大不可用副本数
      maxSurge: 1           # 最大额外副本数
  selector:
    matchLabels:
      app: rolling-app
  template:
    metadata:
      labels:
        app: rolling-app
    spec:
      containers:
      - name: app
        image: nginx:1.21
        ports:
        - containerPort: 80
```

#### 3.2 蓝绿部署策略

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blue-deployment
  namespace: deployment-demo
  labels:
    app: web-app
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
      version: blue
  template:
    metadata:
      labels:
        app: web-app
        version: blue
    spec:
      containers:
      - name: web-app
        image: nginx:1.21-blue
        ports:
        - containerPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: green-deployment
  namespace: deployment-demo
  labels:
    app: web-app
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
      version: green
  template:
    metadata:
      labels:
        app: web-app
        version: green
    spec:
      containers:
      - name: web-app
        image: nginx:1.21-green
        ports:
        - containerPort: 80
```

### 4. 版本管理和回滚

#### 4.1 查看部署历史

```bash
# 查看Deployment修订历史
kubectl rollout history deployment/nginx-deployment -n deployment-demo

# 查看特定修订版本详情
kubectl rollout history deployment/nginx-deployment -n deployment-demo --revision=2

# 查看当前Deployment状态
kubectl rollout status deployment/nginx-deployment -n deployment-demo
```

#### 4.2 执行回滚操作

```bash
# 回滚到上一个版本
kubectl rollout undo deployment/nginx-deployment -n deployment-demo

# 回滚到指定版本
kubectl rollout undo deployment/nginx-deployment -n deployment-demo --to-revision=2

# 暂停部署更新
kubectl rollout pause deployment/nginx-deployment -n deployment-demo

# 恢复部署更新
kubectl rollout resume deployment/nginx-deployment -n deployment-demo
```

### 5. 自动扩缩容配置

#### 5.1 手动扩缩容

```bash
# 扩展副本数
kubectl scale deployment nginx-deployment -n deployment-demo --replicas=5

# 缩减副本数
kubectl scale deployment nginx-deployment -n deployment-demo --replicas=2

# 查看扩缩容状态
kubectl get deployment nginx-deployment -n deployment-demo
```

#### 5.2 HorizontalPodAutoscaler配置

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
  namespace: deployment-demo
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 60
```

### 6. 高级配置选项

#### 6.1 资源配额和限制

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resource-managed-deployment
  namespace: deployment-demo
spec:
  replicas: 3
  selector:
    matchLabels:
      app: resource-app
  template:
    metadata:
      labels:
        app: resource-app
    spec:
      containers:
      - name: app
        image: nginx:1.21
        resources:
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        env:
        - name: RESOURCE_LIMIT
          value: "enabled"
```

#### 6.2 节点选择和亲和性

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: affinity-deployment
  namespace: deployment-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: affinity-app
  template:
    metadata:
      labels:
        app: affinity-app
    spec:
      nodeSelector:
        disktype: ssd
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - affinity-app
              topologyKey: kubernetes.io/hostname
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "app"
        effect: "NoSchedule"
      containers:
      - name: app
        image: nginx:1.21
```

---

## 🔧 实践操作

### 1. Deployment部署和验证

```bash
# 1. 创建Deployment
kubectl apply -f nginx-deployment.yaml -n deployment-demo

# 2. 查看Deployment状态
kubectl get deployments -n deployment-demo
kubectl describe deployment nginx-deployment -n deployment-demo

# 3. 查看相关的ReplicaSet
kubectl get rs -n deployment-demo

# 4. 查看Pod状态
kubectl get pods -n deployment-demo -o wide

# 5. 测试服务访问
kubectl port-forward deployment/nginx-deployment 8080:80 -n deployment-demo
```

### 2. 滚动更新演练

```bash
# 1. 查看当前部署状态
kubectl get deployment nginx-deployment -n deployment-demo

# 2. 更新镜像版本
kubectl set image deployment/nginx-deployment nginx=nginx:1.22 -n deployment-demo

# 3. 监控更新过程
kubectl rollout status deployment/nginx-deployment -n deployment-demo

# 4. 查看更新历史
kubectl rollout history deployment/nginx-deployment -n deployment-demo

# 5. 验证新版本
kubectl get pods -n deployment-demo -o jsonpath='{.items[*].spec.containers[*].image}'
```

### 3. 回滚操作练习

```bash
# 1. 查看可用的修订版本
kubectl rollout history deployment/nginx-deployment -n deployment-demo

# 2. 回滚到上一个版本
kubectl rollout undo deployment/nginx-deployment -n deployment-demo

# 3. 回滚到指定版本
kubectl rollout undo deployment/nginx-deployment -n deployment-demo --to-revision=1

# 4. 验证回滚结果
kubectl describe deployment/nginx-deployment -n deployment-demo
```

### 4. 自动扩缩容测试

```bash
# 1. 创建HPA
kubectl apply -f hpa-config.yaml -n deployment-demo

# 2. 查看HPA状态
kubectl get hpa -n deployment-demo

# 3. 生成负载测试
kubectl run load-test --image=busybox:1.35 -n deployment-demo --restart=Never -- \
  sh -c "while true; do wget -qO- http://nginx-deployment; done"

# 4. 监控自动扩缩容
kubectl get hpa nginx-hpa -n deployment-demo --watch
kubectl get deployment nginx-deployment -n deployment-demo
```

---

## 📊 监控和验证

### 1. Deployment状态检查

```bash
# 查看Deployment详细信息
kubectl describe deployment nginx-deployment -n deployment-demo

# 查看Deployment YAML配置
kubectl get deployment nginx-deployment -n deployment-demo -o yaml

# 查看Deployment事件
kubectl get events -n deployment-demo --field-selector involvedObject.kind=Deployment

# 监控Deployment状态变化
kubectl get deployment nginx-deployment -n deployment-demo --watch
```

### 2. 性能监控命令

```bash
# 查看Pod资源使用情况
kubectl top pods -n deployment-demo

# 查看Deployment资源使用汇总
kubectl top deployment -n deployment-demo

# 查看节点资源分配
kubectl describe nodes | grep -A 5 "Allocated resources"
```

---

## ⚠️ 常见问题和解决方案

### 1. Deployment更新卡住

**问题现象**: Deployment更新长时间处于 progressing 状态

**可能原因**:
- 新Pod无法通过健康检查
- 资源配额不足
- 镜像拉取失败
- 节点资源不足

**解决步骤**:
```bash
# 1. 检查Deployment状态
kubectl describe deployment <deployment-name> -n <namespace>

# 2. 检查Pod状态和事件
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>

# 3. 检查资源配额
kubectl describe resourcequota -n <namespace>

# 4. 手动重启Deployment
kubectl rollout restart deployment <deployment-name> -n <namespace>
```

### 2. 滚动更新失败

**问题现象**: 滚动更新过程中出现错误，新旧版本共存

**解决步骤**:
```bash
# 1. 暂停更新过程
kubectl rollout pause deployment <deployment-name> -n <namespace>

# 2. 检查失败原因
kubectl describe deployment <deployment-name> -n <namespace>

# 3. 修复配置问题后恢复更新
kubectl rollout resume deployment <deployment-name> -n <namespace>

# 4. 如需回滚
kubectl rollout undo deployment <deployment-name> -n <namespace>
```

### 3. 扩缩容不生效

**问题现象**: HPA配置后副本数没有按预期变化

**解决步骤**:
```bash
# 1. 检查HPA状态
kubectl describe hpa <hpa-name> -n <namespace>

# 2. 检查Metrics Server状态
kubectl get pods -n kube-system | grep metrics

# 3. 验证资源指标采集
kubectl top pods -n <namespace>

# 4. 检查HPA配置
kubectl get hpa <hpa-name> -n <namespace> -o yaml
```

---

## 🧪 实践练习

### 练习1：滚动更新策略优化
配置不同的maxUnavailable和maxSurge参数，观察更新过程的差异。

### 练习2：蓝绿部署实践
实现完整的蓝绿部署流程，包括流量切换和回滚操作。

### 练习3：自动扩缩容调优
配置HPA并进行压力测试，优化自动扩缩容参数。

### 练习4：故障恢复演练
模拟各种部署故障场景，练习快速恢复技能。

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Deployment Operations](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#updating-a-deployment)
- [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

### 相关案例
- [StatefulSet有状态应用](../statefulset-basics/)
- [DaemonSet节点部署](../daemonset-basics/)
- [Workload高级特性](../workload-advanced/)

### 进阶主题
- Deployment策略详解
- 金丝雀发布实现
- 多环境部署管理
- 部署流水线集成

---

## 📋 清理资源

```bash
# 删除HPA
kubectl delete hpa nginx-hpa -n deployment-demo

# 删除Deployment
kubectl delete deployments --all -n deployment-demo

# 删除负载测试Pod
kubectl delete pod load-test -n deployment-demo

# 删除命名空间
kubectl delete namespace deployment-demo
```

---

> **💡 提示**: Deployment是Kubernetes应用部署的核心资源，建议熟练掌握滚动更新和回滚操作。在生产环境中使用时要注意健康检查配置和资源限制设置。
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
