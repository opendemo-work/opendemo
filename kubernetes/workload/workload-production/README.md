# 🏭 Kubernetes Workload生产环境最佳实践

> 企业级Kubernetes工作负载解决方案：高可用架构、性能优化、监控告警、安全合规等生产环境必备技能

## 📋 案例概述

本案例提供Kubernetes Workload在生产环境中的完整最佳实践指南，涵盖高可用设计、性能优化、监控体系和安全配置。

### 🔧 核心技能点

- **高可用架构**: 多副本、故障转移、负载均衡
- **性能优化**: 资源调优、调度优化、缓存策略
- **监控告警**: 工作负载指标采集、异常检测、告警配置
- **安全合规**: 访问控制、网络安全、审计日志
- **成本管控**: 资源优化、容量规划、成本分析
- **灾备恢复**: 备份策略、异地容灾、快速恢复

### 🎯 适用人群

- 生产环境运维工程师
- 系统架构师
- SRE团队成员
- 企业安全管理员

---

## 🚀 生产环境配置

### 1. 高可用Deployment配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: production-app
  namespace: production
  labels:
    app: production-app
    tier: frontend
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 2
  selector:
    matchLabels:
      app: production-app
  template:
    metadata:
      labels:
        app: production-app
        version: v1.2.3
        environment: production
    spec:
      # 节点选择和容忍度
      nodeSelector:
        node-type: app-server
        kubernetes.io/arch: amd64
      tolerations:
      - key: dedicated
        operator: Equal
        value: production
        effect: NoSchedule
      
      # 资源管理
      containers:
      - name: app
        image: production-app:v1.2.3
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        
        # 健康检查
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        # 安全配置
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          readOnlyRootFilesystem: true
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
      volumes:
      - name: tmp-volume
        emptyDir: {}
```

### 2. 生产级StatefulSet配置

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: production-database
  namespace: production
spec:
  serviceName: database-service
  replicas: 3
  updateStrategy:
    type: RollingUpdate
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
        version: v2.1.0
    spec:
      # 反亲和性确保Pod分散到不同节点
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - database
            topologyKey: kubernetes.io/hostname
      
      containers:
      - name: database
        image: postgres:14
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: password
        volumeMounts:
        - name: database-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
  volumeClaimTemplates:
  - metadata:
      name: database-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi
```

---

## 📋 完整生产实践方案

包含以下核心内容：
- 高可用架构设计原则
- 性能基准测试和优化
- 监控告警体系搭建
- 安全合规配置
- 成本优化策略
- 灾备恢复流程

---
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

```bash
./scripts/apply.sh
```

### 检查状态

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

```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
