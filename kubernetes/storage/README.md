# Kubernetes Storage

Kubernetes存储管理深度演示，涵盖CSI、存储类、动态供给等。

## 存储架构

```
K8s存储生态:
┌─────────────────────────────────────────────────────────┐
│                   Applications                           │
│              ┌──────────────────┐                       │
│              │   PVC (请求)      │                       │
│              └────────┬─────────┘                       │
└───────────────────────┼─────────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────────┐
│                       ▼         Storage Layer            │
│  ┌─────────────────────────────────────────┐             │
│  │           StorageClass                  │             │
│  │    (provisioner: ebs.csi.aws.com)       │             │
│  └───────────────────┬─────────────────────┘             │
│                      │                                   │
│  ┌───────────────────▼─────────────────────┐             │
│  │              CSI Driver                 │             │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐   │             │
│  │  │Controller│ │  Node   │ │Identity │   │             │
│  │  │Service  │ │ Service │ │ Service │   │             │
│  │  └────┬────┘ └────┬────┘ └─────────┘   │             │
│  └───────┼───────────┼─────────────────────┘             │
└──────────┼───────────┼───────────────────────────────────┘
           │           │
           ▼           ▼
┌─────────────────────────────────────────────────────────┐
│              Backend Storage Systems                     │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐          │
│  │  EBS   │ │  NFS   │ │  Ceph  │ │  iSCSI │          │
│  └────────┘ └────────┘ └────────┘ └────────┘          │
└─────────────────────────────────────────────────────────┘
```

## CSI (Container Storage Interface)

### 架构组件
```
CSI组件:
┌─────────────────────────────────────────────────────┐
│                 Kubernetes Cluster                   │
│  ┌─────────────────────────────────────────────┐   │
│  │            External Provisioner              │   │
│  │     (watch PVC → call CSI CreateVolume)      │   │
│  └─────────────────────┬───────────────────────┘   │
│                        │ gRPC                       │
│  ┌─────────────────────▼───────────────────────┐   │
│  │           CSI Controller Plugin              │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │ Create  │ │ Delete  │ │ Publish │       │   │
│  │  │ Volume  │ │ Volume  │ │ Volume  │       │   │
│  │  └─────────┘ └─────────┘ └─────────┘       │   │
│  └─────────────────────┬───────────────────────┘   │
│                        │                            │
│  ┌─────────────────────▼───────────────────────┐   │
│  │            CSI Node Plugin                   │   │
│  │         (NodePublishVolume)                  │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 部署CSI Driver
```yaml
# AWS EBS CSI Driver
apiVersion: storage.k8s.io/v1
kind: CSIDriver
metadata:
  name: ebs.csi.aws.com
spec:
  attachRequired: true
  podInfoOnMount: false
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ebs-csi-controller
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ebs-csi-controller
  template:
    spec:
      serviceAccountName: ebs-csi-controller-sa
      containers:
      - name: ebs-plugin
        image: amazon/aws-ebs-csi-driver:latest
        args:
        - --endpoint=$(CSI_ENDPOINT)
        env:
        - name: CSI_ENDPOINT
          value: unix:///var/lib/csi/sockets/pluginproxy/csi.sock
```

## 高级存储配置

### 快照与克隆
```yaml
# VolumeSnapshotClass
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-snapclass
driver: ebs.csi.aws.com
parameters:
  type: snap
---
# 创建快照
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: mysql-snapshot
spec:
  volumeSnapshotClassName: csi-snapclass
  source:
    persistentVolumeClaimName: mysql-pvc
---
# 从快照恢复
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-restored
spec:
  storageClassName: gp3
  dataSource:
    name: mysql-snapshot
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
```

### 存储扩容
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: expandable
provisioner: ebs.csi.aws.com
allowVolumeExpansion: true
parameters:
  type: gp3
```

```bash
# 在线扩容
kubectl patch pvc mysql-pvc -p '{"spec":{"resources":{"requests":{"storage":"200Gi"}}}}'
```

## 存储性能优化

### IO调度器
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: high-performance
provisioner: ebs.csi.aws.com
parameters:
  type: io1
  iopsPerGB: "50"
  encrypted: "true"
allowVolumeExpansion: true
mountOptions:
  - noatime
  - nodiratime
volumeBindingMode: WaitForFirstConsumer
```

## 学习要点

1. CSI架构与Driver开发
2. 存储拓扑感知
3. 快照与克隆机制
4. 存储扩容实现
5. 多存储后端管理
