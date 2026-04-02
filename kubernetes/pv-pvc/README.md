# Persistent Volumes and Claims

Kubernetes持久化存储演示，展示PV、PVC、StorageClass的使用和动态供给。

## 核心概念

```
存储架构:
┌─────────────────────────────────────────────────────┐
│                     Pod                             │
│              ┌─────────────────┐                    │
│              │  Container      │                    │
│              │  ┌───────────┐  │                    │
│              │  │ /data     │  │                    │
│              │  └─────┬─────┘  │                    │
│              └────────┼────────┘                    │
│                       │ mount                       │
├───────────────────────┼─────────────────────────────┤
│                       │                             │
│              ┌────────┴────────┐                    │
│              │   PVC ( claim ) │                    │
│              │  Request: 10Gi  │                    │
│              │  Mode: RWO      │                    │
│              └────────┬────────┘                    │
│                       │ bound                       │
├───────────────────────┼─────────────────────────────┤
│                       │                             │
│              ┌────────┴────────┐                    │
│              │   PV ( volume ) │                    │
│              │  Capacity: 10Gi │                    │
│              │  Path: /nfs/xxx │                    │
│              └────────┬────────┘                    │
│                       │                             │
├───────────────────────┼─────────────────────────────┤
│                       │                             │
│              ┌────────┴────────┐                    │
│              │  Storage        │                    │
│              │  (NFS/iSCSI/云盘)│                    │
│              └─────────────────┘                    │
└─────────────────────────────────────────────────────┘
```

## 访问模式

| 模式 | 缩写 | 说明 |
|------|------|------|
| ReadWriteOnce | RWO | 单节点读写 |
| ReadOnlyMany | ROX | 多节点只读 |
| ReadWriteMany | RWX | 多节点读写 |
| ReadWriteOncePod | RWOP | 单Pod读写 (K8s 1.27+) |

```
访问模式示意图:
RWO:                        RWX:
Node1  Node2               Node1  Node2
┌───┐  ┌───┐               ┌───┐  ┌───┐
│R/W│  │   │               │R/W│  │R/W│
└─┬─┘  └───┘               └─┬─┘  └─┬─┘
  │                          │      │
┌─┴────────┐                ┌┴──────┴┐
│  Volume  │                │ Volume │
└──────────┘                └────────┘
```

## 静态供给

### 创建PV
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /data/nfs
    server: 192.168.1.100
```

### 创建PVC
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
  storageClassName: nfs
  volumeName: nfs-pv
```

### 使用PVC
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx
        volumeMounts:
        - name: data
          mountPath: /usr/share/nginx/html
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: nfs-pvc
```

## 动态供给

### 创建StorageClass
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: regional-distributed
reclaimPolicy: Delete
allowVolumeExpansion: true
mountOptions:
  - debug
volumeBindingMode: WaitForFirstConsumer
```

### 云厂商StorageClass示例

#### AWS EBS
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
  iops: "3000"
  throughput: "125"
```

#### Azure Disk
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-premium
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_LRS
  cachingMode: ReadOnly
```

#### 本地存储
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

## 回收策略

```
回收策略行为:

Retain (保留):               Delete (删除):
┌──────────────┐            ┌──────────────┐
│ PV deleted   │            │ PV deleted   │
├──────────────┤            ├──────────────┤
│ Data remains │            │ Data deleted │
│ on storage   │            │ by provisioner│
├──────────────┤            ├──────────────┤
│ Manual       │            │ Automatic    │
│ cleanup      │            │ cleanup      │
└──────────────┘            └──────────────┘
```

## 扩容

### 启用卷扩展
```yaml
# StorageClass中启用
allowVolumeExpansion: true
```

### 执行扩容
```bash
# 编辑PVC增加容量
kubectl patch pvc my-pvc -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'

# 查看扩容进度
kubectl get pvc my-pvc -w
```

## StatefulSet存储

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 10Gi
```

**StatefulSet会为每个Pod创建独立PVC：**
```
mysql-0 → pvc-data-mysql-0
mysql-1 → pvc-data-mysql-1
mysql-2 → pvc-data-mysql-2
```

## 常用命令

```bash
# 查看PV列表
kubectl get pv

# 查看PVC列表
kubectl get pvc

# 查看StorageClass
kubectl get sc

# 查看PV详情
kubectl describe pv <pv-name>

# 删除PVC
kubectl delete pvc <pvc-name>

# 强制删除Terminating状态的PVC
kubectl patch pvc <pvc-name> -p '{"metadata":{"finalizers":[]}}' --type=merge
```

## 学习要点

1. PV/PVC/StorageClass关系
2. 静态供给 vs 动态供给
3. 访问模式选择
4. 回收策略影响
5. 有状态应用存储管理
