# 👤 Kubernetes DaemonSet基础实战

> 深入学习Kubernetes DaemonSet的核心功能：节点级应用部署、系统守护进程管理等基础设施运维技能

## 📋 案例概述

本案例详细介绍Kubernetes DaemonSet的基础知识和实践操作，帮助用户掌握节点级应用的部署管理技能。

### 🔧 核心技能点

- **DaemonSet基本概念**: 理解节点级部署的特点和优势
- **节点选择策略**: 污点、容忍度和节点选择器配置
- **系统级应用部署**: 日志收集、监控代理、网络插件等
- **更新策略配置**: 滚动更新和就地更新策略
- **资源管理优化**: 系统组件的资源限制和调度

### 🎯 适用人群

- 系统管理员
- SRE工程师
- 基础设施运维人员
- 监控和日志平台管理员

---

## 🚀 核心内容

### 1. DaemonSet基础配置

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-daemonset
  namespace: workload-demo
  labels:
    app: fluentd
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      tolerations:
      # 允许调度到master节点
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.14
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 100Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

### 2. 节点选择配置

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: workload-demo
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      nodeSelector:
        kubernetes.io/os: linux
      tolerations:
      - key: node.kubernetes.io/not-ready
        operator: Exists
        effect: NoSchedule
      - key: node.kubernetes.io/unreachable
        operator: Exists
        effect: NoSchedule
      containers:
      - name: node-exporter
        image: prom/node-exporter:v1.3.1
        ports:
        - containerPort: 9100
          name: metrics
```

---

## 📋 完整案例文件

包含以下核心内容：
- DaemonSet基础配置和部署
- 节点选择和容忍度配置
- 系统级应用部署实践
- 更新策略和滚动更新
- 资源管理和性能优化
- 监控和故障排查

---