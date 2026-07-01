# ⚡ Kubernetes Workload高级特性实战

> 深入探索Kubernetes Workload的高级功能：亲和性配置、污点容忍、资源管理、调度优化等企业级特性

## 📋 案例概述

本案例专注于Kubernetes Workload的高级配置和企业级特性，帮助您掌握生产环境中工作负载的精细化管理和优化配置。

### 🔧 核心技能点

- **节点亲和性**: NodeAffinity和PodAffinity配置
- **污点和容忍度**: Taints和Tolerations高级用法
- **资源管理优化**: QoS等级、资源配额、限制范围
- **调度策略**: 自定义调度器、调度约束
- **拓扑感知**: 拓扑分布约束、区域感知调度
- **工作负载隔离**: 命名空间隔离、资源隔离

### 🎯 适用人群

- 有经验的DevOps工程师
- 系统架构师
- 云平台管理员
- 性能优化专家

---

## 🚀 核心内容

### 1. 高级亲和性配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: affinity-demo
  namespace: workload-advanced
spec:
  replicas: 3
  selector:
    matchLabels:
      app: affinity-demo
  template:
    metadata:
      labels:
        app: affinity-demo
    spec:
      # 节点亲和性
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: kubernetes.io/arch
                operator: In
                values:
                - amd64
              - key: disktype
                operator: In
                values:
                - ssd
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 1
            preference:
              matchExpressions:
              - key: availability-zone
                operator: In
                values:
                - zone-1
        
        # Pod亲和性
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: security
                operator: In
                values:
                - S1
            topologyKey: topology.kubernetes.io/zone
        
        # Pod反亲和性
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - affinity-demo
              topologyKey: kubernetes.io/hostname
```

### 2. 污点和容忍度高级配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: toleration-demo
  namespace: workload-advanced
spec:
  replicas: 2
  selector:
    matchLabels:
      app: toleration-demo
  template:
    metadata:
      labels:
        app: toleration-demo
    spec:
      tolerations:
      # 容忍特定污点
      - key: "dedicated"
        operator: "Equal"
        value: "database"
        effect: "NoSchedule"
      
      # 容忍多个污点
      - key: "node.kubernetes.io/not-ready"
        operator: "Exists"
        effect: "NoExecute"
        tolerationSeconds: 300
      
      # 容忍所有污点（谨慎使用）
      - operator: "Exists"
      
      containers:
      - name: app
        image: nginx:1.21
```

### 3. 资源管理高级配置

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: workload-advanced
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    requests.storage: 100Gi
    persistentvolumeclaims: "10"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
  namespace: workload-advanced
spec:
  limits:
  - default:
      memory: 512Mi
      cpu: 500m
    defaultRequest:
      memory: 256Mi
      cpu: 250m
    type: Container
```

---

## 📋 完整案例文件

包含以下核心内容：
- 高级亲和性和反亲和性配置
- 污点和容忍度的深度应用
- 资源配额和限制范围管理
- 自定义调度策略
- 拓扑感知和区域调度
- 工作负载隔离和安全性

---
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
