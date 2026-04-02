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
