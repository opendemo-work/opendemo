<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Longhorn Distributed Storage

轻量级分布式块存储解决方案。

## Longhorn架构

```
Longhorn架构:
┌─────────────────────────────────────────────────────────┐
│                  Longhorn Manager                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Volume      │  │  Node        │  │  Replica     │   │
│  │  Controller  │  │  Scheduler   │  │  Manager     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                   Longhorn Engine                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Volume      │  │  Replica 1   │  │  Replica 2   │   │
│  │  Controller  │  │  (Node A)    │  │  (Node B)    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐                                       │
│  │  Replica 3   │  (副本数量可配置)                      │
│  │  (Node C)    │                                       │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

## 安装Longhorn

```bash
# Helm安装
helm repo add longhorn https://charts.longhorn.io
helm repo update

helm install longhorn longhorn/longhorn \
  --namespace longhorn-system \
  --create-namespace

# 验证
kubectl get pods -n longhorn-system
```

## 存储类配置

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: longhorn
provisioner: driver.longhorn.io
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: Immediate
parameters:
  numberOfReplicas: "3"
  staleReplicaTimeout: "30"
  fromBackup: ""
  fsType: "ext4"
```

## 备份与快照

```yaml
# 创建快照
apiVersion: longhorn.io/v1beta1
kind: Snapshot
metadata:
  name: my-snapshot
spec:
  volume: my-volume
---
# 创建备份
apiVersion: longhorn.io/v1beta1
kind: RecurringJob
metadata:
  name: backup-job
spec:
  cron: "0 2 * * *"
  task: backup
  groups:
    - default
  retain: 7
```

## 灾难恢复

```yaml
# 从备份恢复
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: restored-pvc
spec:
  storageClassName: longhorn
  dataSource:
    name: backup-abc123
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## 学习要点

1. 分布式存储原理
2. 副本管理
3. 快照与备份
4. 存储扩容
5. 灾难恢复

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


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*
