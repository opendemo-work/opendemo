# 💾 Kubernetes存储基础设施实战

> 深入学习Kubernetes存储系统：本地存储、CSI驱动、存储类管理等企业级存储解决方案

## 📋 案例概述

本案例详细介绍Kubernetes存储基础设施的核心配置和管理技能，帮助企业构建稳定可靠的存储服务体系。

### 🔧 核心技能点

- **本地存储管理**: HostPath、Local PV配置和优化
- **CSI驱动集成**: 主流存储供应商CSI驱动部署
- **存储类配置**: StorageClass动态供应和参数调优
- **存储性能优化**: I/O调优、缓存配置、QoS管理
- **数据保护策略**: 快照、备份、灾难恢复
- **存储监控告警**: 存储使用率监控、性能指标采集

### 🎯 适用人群

- 存储管理员
- Kubernetes运维工程师
- 云架构师
- 数据库管理员

---

## 🚀 核心内容

### 1. 本地存储配置

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-fast-ssd
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv-ssd1
spec:
  capacity:
    storage: 500Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-fast-ssd
  local:
    path: /mnt/fast-ssd
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - worker-node-1
```

### 2. CSI驱动配置

```yaml
apiVersion: storage.k8s.io/v1
kind: CSIDriver
metadata:
  name: ebs.csi.aws.com
spec:
  attachRequired: true
  podInfoOnMount: true
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: aws-ebs-gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

---

## 📋 完整案例文件

包含以下核心内容：
- 本地存储和网络存储配置
- CSI驱动部署和管理
- 存储类动态供应配置
- 存储性能优化方案
- 数据保护和备份策略
- 存储监控和告警体系

---