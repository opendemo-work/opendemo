# Rook Ceph Storage

Kubernetes云原生存储解决方案。

## Rook Ceph架构

```
Rook Ceph架构:
┌─────────────────────────────────────────────────────────┐
│                    Rook Operator                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Cluster     │  │  Pool        │  │  Volume      │   │
│  │  Controller  │  │  Controller  │  │  Controller  │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                       Ceph Cluster                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Ceph Mon    │  │  Ceph Mgr    │  │  Ceph OSD    │   │
│  │  (Monitor)   │  │  (Manage)    │  │  (Storage)   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │  Ceph MDS    │  │  RGW         │                     │
│  │  (Metadata)  │  │  (Object)    │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

## 安装Rook

```bash
# 克隆Rook仓库
git clone --single-branch --branch v1.12.0 https://github.com/rook/rook.git
cd rook/deploy/examples

# 安装CRD和Operator
kubectl apply -f crds.yaml
kubectl apply -f common.yaml
kubectl apply -f operator.yaml

# 创建Ceph集群
kubectl apply -f cluster.yaml
```

## CephCluster配置

```yaml
apiVersion: ceph.rook.io/v1
kind: CephCluster
metadata:
  name: rook-ceph
  namespace: rook-ceph
spec:
  cephVersion:
    image: quay.io/ceph/ceph:v17.2.6
  dataDirHostPath: /var/lib/rook
  mon:
    count: 3
    allowMultiplePerNode: false
  storage:
    useAllNodes: true
    useAllDevices: false
    deviceFilter: "^sd[bc]"
    config:
      osdsPerDevice: "1"
  resources:
    mon:
      limits:
        memory: "2Gi"
      requests:
        memory: "1Gi"
```

## 存储类创建

```yaml
# Block Storage
apiVersion: ceph.rook.io/v1
kind: CephBlockPool
metadata:
  name: replicapool
  namespace: rook-ceph
spec:
  failureDomain: host
  replicated:
    size: 3
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rook-ceph-block
provisioner: rook-ceph.rbd.csi.ceph.com
parameters:
  clusterID: rook-ceph
  pool: replicapool
  imageFormat: "2"
  imageFeatures: layering
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

## 使用PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  storageClassName: rook-ceph-block
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## 学习要点

1. Ceph组件架构
2. Rook Operator
3. 存储池配置
4. CSI驱动
5. 数据冗余与恢复
