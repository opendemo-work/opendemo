# 📦 Kubernetes PV/PVC基础入门实战

> 全面掌握Kubernetes持久卷(PV)和持久卷声明(PVC)的核心概念、基础配置和实际应用，从零开始构建数据持久化解决方案

## 📋 案例概述

本案例详细介绍Kubernetes PV/PVC的基础知识和实践操作，帮助初学者快速理解和掌握持久化存储的核心概念和使用方法。

### 🔧 核心技能点

- **PV基本概念**: 理解持久卷的作用和工作机制
- **PVC基本概念**: 掌握持久卷声明的使用方法
- **静态供应**: 手动创建和管理持久卷
- **基础配置**: PV/PVC的基本配置参数
- **绑定机制**: PV与PVC的绑定过程和规则

### 🎯 适用人群

- Kubernetes初学者
- DevOps工程师
- 系统管理员
- 存储管理员

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查Kubernetes集群状态
kubectl cluster-info
kubectl get nodes

# 创建专用命名空间
kubectl create namespace pv-pvc-demo

# 检查存储相关资源
kubectl api-resources | grep -E "(persistentvolume|persistentvolumeclaim|storageclass)"
```

### 2. 创建测试目录（本地测试环境）

```bash
# 在各节点上创建测试目录
mkdir -p /tmp/k8s-pv-demo/{pv1,pv2,pv3}

# 设置权限
chmod 777 /tmp/k8s-pv-demo/{pv1,pv2,pv3}
```

---

## 📚 详细教程

### 1. PV/PVC核心概念

#### 1.1 什么是PV（Persistent Volume）

PV是集群中的一块存储资源，由管理员配置，独立于Pod的生命周期。

**关键特性**：
- 集群级别的存储资源
- 生命周期独立于Pod
- 支持多种存储后端（本地存储、NFS、云存储等）
- 可以静态创建或动态供应

#### 1.2 什么是PVC（Persistent Volume Claim）

PVC是用户对存储资源的请求，类似于Pod对计算资源的请求。

**关键特性**：
- 用户对PV的请求
- 可以指定存储大小和访问模式
- 自动绑定到合适的PV
- 支持存储类（StorageClass）

#### 1.3 PV与PVC的关系

```
用户(Pod) → PVC(请求) → PV(实际存储) → 存储后端
```

### 2. 静态PV配置

#### 2.1 本地存储PV

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-local-1
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: "/tmp/k8s-pv-demo/pv1"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-local-2
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: "/tmp/k8s-pv-demo/pv2"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-local-3
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 2Gi
  accessModes:
    - ReadOnlyMany
  persistentVolumeReclaimPolicy: Delete
  hostPath:
    path: "/tmp/k8s-pv-demo/pv3"
```

#### 2.2 NFS存储PV

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-1
spec:
  storageClassName: nfs-storage
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    server: nfs-server.example.com
    path: "/exports/data1"
```

### 3. PVC配置和使用

#### 3.1 基础PVC配置

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-demo-1
  namespace: pv-pvc-demo
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-demo-2
  namespace: pv-pvc-demo
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 8Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-demo-readonly
  namespace: pv-pvc-demo
spec:
  storageClassName: manual
  accessModes:
    - ReadOnlyMany
  resources:
    requests:
      storage: 1Gi
```

#### 3.2 使用PVC的Pod配置

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pv-pvc-test-pod
  namespace: pv-pvc-demo
  labels:
    app: storage-demo
spec:
  containers:
  - name: writer
    image: busybox:1.35
    command: ["sh", "-c", "while true; do echo $(date) >> /data/timestamp.log; sleep 10; done"]
    volumeMounts:
    - name: data-volume
      mountPath: /data
  - name: reader
    image: busybox:1.35
    command: ["sh", "-c", "while true; do cat /data/timestamp.log; sleep 30; done"]
    volumeMounts:
    - name: data-volume
      mountPath: /data
      readOnly: true
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: pvc-demo-1
```

### 4. 访问模式详解

#### 4.1 访问模式类型

| 访问模式 | 缩写 | 描述 | 适用场景 |
|---------|------|------|----------|
| ReadWriteOnce | RWO | 单节点读写 | 数据库、单实例应用 |
| ReadOnlyMany | ROX | 多节点只读 | 配置文件、静态内容 |
| ReadWriteMany | RWX | 多节点读写 | 文件共享、协作应用 |
| ReadWriteOncePod | RWOP | 单Pod读写 | 需要强隔离的存储 |

#### 4.2 访问模式配置示例

```yaml
# RWO示例
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-rwo
  namespace: pv-pvc-demo
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: manual

# ROX示例
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-rox
  namespace: pv-pvc-demo
spec:
  accessModes:
    - ReadOnlyMany
  resources:
    requests:
      storage: 2Gi
  storageClassName: manual

# RWX示例
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-rwx
  namespace: pv-pvc-demo
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: nfs-storage
```

### 5. 回收策略

#### 5.1 回收策略类型

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| Retain | 保留数据，需要手动清理 | 重要数据，防止误删 |
| Recycle | 清理数据并重新可用（已弃用） | 不推荐使用 |
| Delete | 删除PV和底层存储 | 临时数据，开发测试 |

#### 5.2 回收策略配置

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-with-retain
spec:
  storageClassName: manual
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain  # 保留策略
  hostPath:
    path: "/tmp/k8s-pv-demo/retain-pv"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-with-delete
spec:
  storageClassName: manual
  capacity:
    storage: 3Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete  # 删除策略
  hostPath:
    path: "/tmp/k8s-pv-demo/delete-pv"
```

---

## 🔧 实践操作

### 1. 部署和验证

```bash
# 1. 创建PV资源
kubectl apply -f pv-configs.yaml

# 2. 查看PV状态
kubectl get pv
kubectl describe pv pv-local-1

# 3. 创建PVC资源
kubectl apply -f pvc-configs.yaml

# 4. 查看PVC状态和绑定情况
kubectl get pvc -n pv-pvc-demo
kubectl describe pvc pvc-demo-1 -n pv-pvc-demo

# 5. 部署使用PVC的Pod
kubectl apply -f pod-with-pvc.yaml

# 6. 验证Pod和存储挂载
kubectl get pods -n pv-pvc-demo
kubectl describe pod pv-pvc-test-pod -n pv-pvc-demo
kubectl exec -it pv-pvc-test-pod -n pv-pvc-demo -c writer -- df -h
```

### 2. 数据持久化测试

```bash
# 1. 向存储中写入数据
kubectl exec -it pv-pvc-test-pod -n pv-pvc-demo -c writer -- sh -c "echo 'Hello PV/PVC!' > /data/hello.txt"

# 2. 读取数据验证
kubectl exec -it pv-pvc-test-pod -n pv-pvc-demo -c reader -- cat /data/hello.txt

# 3. 删除Pod测试数据持久化
kubectl delete pod pv-pvc-test-pod -n pv-pvc-demo

# 4. 重新创建Pod
kubectl apply -f pod-with-pvc.yaml

# 5. 验证数据仍然存在
kubectl exec -it pv-pvc-test-pod -n pv-pvc-demo -c reader -- cat /data/hello.txt
```

### 3. PV/PVC生命周期管理

```bash
# 1. 查看当前状态
kubectl get pv,pvc -n pv-pvc-demo

# 2. 删除PVC（测试回收策略）
kubectl delete pvc pvc-demo-1 -n pv-pvc-demo

# 3. 查看PV状态变化
kubectl get pv

# 4. 手动回收PV（Retain策略）
kubectl delete pv pv-local-1

# 5. 清理测试数据
rm -rf /tmp/k8s-pv-demo/*
```

---

## 📊 监控和验证

### 1. 状态检查命令

```bash
# 查看所有PV状态
kubectl get pv -o wide

# 查看特定命名空间的PVC
kubectl get pvc -n pv-pvc-demo

# 详细描述PV信息
kubectl describe pv <pv-name>

# 详细描述PVC信息
kubectl describe pvc <pvc-name> -n <namespace>

# 查看存储类
kubectl get storageclass

# 查看事件日志
kubectl get events -n pv-pvc-demo --sort-by=.metadata.creationTimestamp
```

### 2. 常用验证脚本

```bash
#!/bin/bash
# pv-pvc-status-check.sh

echo "=== PV/PVC状态检查 ==="

echo "1. PV状态:"
kubectl get pv -o custom-columns=NAME:.metadata.name,CAPACITY:.spec.capacity.storage,ACCESS_MODES:.spec.accessModes,STATUS:.status.phase,CLAIM:.spec.claimRef.name

echo -e "\n2. PVC状态:"
kubectl get pvc --all-namespaces -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase,VOLUME:.spec.volumeName,CAPACITY:.status.capacity.storage

echo -e "\n3. 绑定关系:"
kubectl get pv -o jsonpath='{range .items[*]}{.metadata.name}{" -> "}{.spec.claimRef.name}{"\n"}{end}'
```

---

## ⚠️ 常见问题和解决方案

### 1. PVC Pending状态

**问题现象**: PVC长时间处于Pending状态，无法绑定到PV

**可能原因**:
- 没有匹配的PV（容量、访问模式不匹配）
- StorageClass配置错误
- PV资源不足

**解决步骤**:
```bash
# 1. 检查PVC详细信息
kubectl describe pvc <pvc-name> -n <namespace>

# 2. 查看可用PV
kubectl get pv

# 3. 检查PV和PVC的匹配条件
kubectl get pv -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.spec.capacity.storage}{" "}{.spec.accessModes}{"\n"}{end}'

# 4. 如果需要，创建匹配的PV
```

### 2. Pod无法挂载卷

**问题现象**: Pod启动失败，报错"MountVolume.SetUp failed"

**可能原因**:
- PV路径不存在或权限不足
- 存储后端不可达
- SELinux/AppArmor限制

**解决步骤**:
```bash
# 1. 检查Pod事件
kubectl describe pod <pod-name> -n <namespace>

# 2. 检查节点上的路径
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.nodeName}'
# 然后登录对应节点检查路径

# 3. 检查权限设置
ls -la /tmp/k8s-pv-demo/

# 4. 查看kubelet日志
journalctl -u kubelet | grep -i mount
```

### 3. 存储容量不足

**问题现象**: 应用报错磁盘空间不足

**解决步骤**:
```bash
# 1. 检查实际使用情况
kubectl exec -it <pod-name> -n <namespace> -- df -h

# 2. 检查PVC申请容量
kubectl get pvc <pvc-name> -n <namespace> -o jsonpath='{.spec.resources.requests.storage}'

# 3. 如果支持扩容，进行扩容操作
kubectl patch pvc <pvc-name> -n <namespace> -p '{"spec":{"resources":{"requests":{"storage":"10Gi"}}}}'
```

---

## 🧪 实践练习

### 练习1：基础PV/PVC配置
创建3个不同容量的PV和对应的PVC，验证绑定关系和数据持久化。

### 练习2：访问模式测试
分别测试RWO、ROX、RWX三种访问模式的实际效果。

### 练习3：回收策略验证
配置不同回收策略的PV，验证删除PVC后的行为差异。

### 练习4：故障模拟
模拟各种存储故障场景，练习故障诊断和修复技能。

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- [Volume Snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)

### 相关案例
- [StorageClass基础配置](../storage-class-basics/)
- [PV/PVC高级特性](../pv-pvc-advanced/)
- [生产环境最佳实践](../pv-pvc-production/)

### 进阶主题
- 动态卷供应机制
- 存储性能优化
- 云存储集成
- 存储安全配置

---

## 📋 清理资源

```bash
# 删除测试Pod
kubectl delete pod pv-pvc-test-pod -n pv-pvc-demo

# 删除PVC
kubectl delete pvc --all -n pv-pvc-demo

# 删除PV
kubectl delete pv pv-local-1 pv-local-2 pv-local-3

# 删除命名空间
kubectl delete namespace pv-pvc-demo

# 清理本地测试目录
rm -rf /tmp/k8s-pv-demo/
```

---

> **💡 提示**: PV/PVC是Kubernetes存储的核心组件，建议先掌握静态供应再学习动态供应。在生产环境中使用时要注意数据安全和备份策略。