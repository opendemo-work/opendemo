# 🏷️ Kubernetes StorageClass基础实战

> 深入学习Kubernetes StorageClass的核心概念和动态卷供应机制，掌握存储资源的自动化管理

## 📋 案例概述

本案例详细介绍Kubernetes StorageClass的基础知识和实践操作，帮助用户理解和掌握动态存储供应的核心概念和配置方法。

### 🔧 核心技能点

- **StorageClass基本概念**: 理解存储类的作用和工作机制
- **动态供应**: 掌握自动创建PV的机制
- **供应器配置**: 不同存储后端的供应器配置
- **参数调优**: StorageClass参数的配置和优化
- **默认存储类**: 设置和使用默认存储类

### 🎯 适用人群

- 有一定Kubernetes经验的开发者
- DevOps工程师
- 存储管理员
- 云平台运维人员

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查集群中的存储类
kubectl get storageclass
kubectl get sc

# 检查默认存储类
kubectl get storageclass -o jsonpath='{range .items[?(@.metadata.annotations.storageclass\.kubernetes\.io/is-default-class=="true")]}{.metadata.name}{"\n"}{end}'

# 创建专用命名空间
kubectl create namespace storageclass-demo
```

### 2. 安装必要组件

```bash
# 检查CSI驱动（以local-path-provisioner为例）
kubectl get pods -n kube-system | grep provisioner

# 如果没有默认的动态供应器，可以安装local-path-provisioner进行测试
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml
```

---

## 📚 详细教程

### 1. StorageClass核心概念

#### 1.1 什么是StorageClass

StorageClass为管理员提供了一种描述存储"类"的方法，不同的类可能会映射到不同的服务质量等级或备份策略，或者是由集群管理员制定的任意策略。

**关键特性**：
- 定义存储"类别"
- 支持动态卷供应
- 可配置供应器参数
- 支持默认存储类设置

#### 1.2 动态供应机制

```
用户(PVC) → StorageClass → Provisioner → PV → 存储后端
```

当用户创建PVC时，如果指定了StorageClass，相应的供应器会自动创建PV并绑定到PVC。

### 2. 基础StorageClass配置

#### 2.1 本地存储StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-path
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-fast
provisioner: rancher.io/local-path
parameters:
  nodePath: /var/local-path-provisioner/fast
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
```

#### 2.2 NFS StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner
parameters:
  server: nfs-server.example.com
  path: /nfs-storage
  onDelete: delete
volumeBindingMode: Immediate
reclaimPolicy: Delete
allowVolumeExpansion: true
mountOptions:
  - vers=4.1
```

### 3. 云存储StorageClass配置

#### 3.1 AWS EBS StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: aws-ebs-gp2
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  fsType: ext4
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: aws-ebs-io1
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io1
  iopsPerGB: "50"
  fsType: ext4
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
```

#### 3.2 Azure Disk StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-standard
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: Standard_LRS
  kind: Managed
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-premium
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: Premium_LRS
  kind: Managed
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
```

#### 3.3 Google Cloud StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gce-pd-standard
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gce-pd-ssd
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
```

### 4. StorageClass参数详解

#### 4.1 核心参数配置

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: advanced-storage
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: example.com/custom-provisioner
parameters:
  # 存储后端特定参数
  diskType: ssd
  encryption: true
  backup: daily
  
  # 性能相关参数
  iops: "3000"
  throughput: "250"
  
  # 位置相关参数
  zone: us-west-1a
  region: us-west-1

# 卷绑定模式
volumeBindingMode: WaitForFirstConsumer

# 回收策略
reclaimPolicy: Delete

# 是否允许扩容
allowVolumeExpansion: true

# 挂载选项
mountOptions:
  - discard
  - noatime

# 允许的拓扑区域
allowedTopologies:
- matchLabelExpressions:
  - key: topology.kubernetes.io/zone
    values:
    - us-west-1a
    - us-west-1b
```

#### 4.2 卷绑定模式

| 绑定模式 | 描述 | 适用场景 |
|---------|------|----------|
| Immediate | PV创建后立即绑定 | 无节点亲和性要求的存储 |
| WaitForFirstConsumer | Pod调度后再绑定 | 需要考虑节点拓扑的存储 |

### 5. 动态供应实践

#### 5.1 创建动态PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc-example
  namespace: storageclass-demo
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: local-path
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc-with-expansion
  namespace: storageclass-demo
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: local-path
```

#### 5.2 使用动态PVC的Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dynamic-storage-pod
  namespace: storageclass-demo
  labels:
    app: dynamic-storage-demo
spec:
  containers:
  - name: app
    image: nginx:1.21
    ports:
    - containerPort: 80
    volumeMounts:
    - name: data-volume
      mountPath: /usr/share/nginx/html
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: dynamic-pvc-example
```

---

## 🔧 实践操作

### 1. StorageClass部署和验证

```bash
# 1. 创建StorageClass
kubectl apply -f storageclass-configs.yaml

# 2. 查看StorageClass状态
kubectl get storageclass
kubectl get sc

# 3. 查看详细信息
kubectl describe storageclass local-path

# 4. 检查默认StorageClass
kubectl get storageclass -o jsonpath='{range .items[?(@.metadata.annotations.storageclass\.kubernetes\.io/is-default-class=="true")]}{.metadata.name}{"\n"}{end}'
```

### 2. 动态供应测试

```bash
# 1. 创建动态PVC
kubectl apply -f dynamic-pvc.yaml

# 2. 观察PV自动创建
kubectl get pv,pvc -n storageclass-demo

# 3. 查看PVC绑定状态
kubectl describe pvc dynamic-pvc-example -n storageclass-demo

# 4. 部署使用动态存储的Pod
kubectl apply -f pod-with-dynamic-pvc.yaml

# 5. 验证存储挂载
kubectl exec -it dynamic-storage-pod -n storageclass-demo -- df -h
```

### 3. 存储扩容测试

```bash
# 1. 检查当前PVC大小
kubectl get pvc dynamic-pvc-with-expansion -n storageclass-demo -o jsonpath='{.status.capacity.storage}'

# 2. 执行扩容操作
kubectl patch pvc dynamic-pvc-with-expansion -n storageclass-demo -p '{"spec":{"resources":{"requests":{"storage":"10Gi"}}}}'

# 3. 观察扩容过程
kubectl describe pvc dynamic-pvc-with-expansion -n storageclass-demo

# 4. 验证扩容结果
kubectl exec -it dynamic-storage-pod -n storageclass-demo -- df -h | grep /usr/share/nginx/html
```

---

## 📊 监控和验证

### 1. StorageClass状态检查

```bash
# 查看所有StorageClass
kubectl get storageclass -o wide

# 查看默认StorageClass
kubectl get storageclass -o jsonpath='{range .items[?(@.metadata.annotations.storageclass\.kubernetes\.io/is-default-class=="true")]}Default StorageClass: {.metadata.name}{"\n"}{end}'

# 查看StorageClass详细配置
kubectl get storageclass local-path -o yaml

# 查看供应器状态
kubectl get pods -n kube-system | grep provisioner
```

### 2. 动态供应监控

```bash
# 监控PV创建事件
kubectl get events --field-selector involvedObject.kind=PersistentVolume --sort-by=.metadata.creationTimestamp

# 监控PVC绑定事件
kubectl get events --field-selector involvedObject.kind=PersistentVolumeClaim --sort-by=.metadata.creationTimestamp

# 查看供应器日志
kubectl logs -n kube-system -l app=local-path-provisioner -f
```

### 3. 存储使用情况检查

```bash
# 查看各命名空间存储使用情况
kubectl get pvc --all-namespaces

# 按StorageClass统计存储使用
kubectl get pvc --all-namespaces -o jsonpath='{range .items[*]}{.spec.storageClassName}{" "}{.status.capacity.storage}{"\n"}{end}' | awk '{sum[$1]+=$2} END {for(i in sum) print i, sum[i]}'

# 查看未绑定的PVC
kubectl get pvc --all-namespaces --field-selector=status.phase!=Bound
```

---

## ⚠️ 常见问题和解决方案

### 1. PVC处于Pending状态

**问题现象**: PVC创建后长时间处于Pending状态，无法绑定到PV

**可能原因**:
- 没有可用的StorageClass
- 供应器配置错误
- 存储后端不可达
- 参数配置不当

**解决步骤**:
```bash
# 1. 检查PVC状态和事件
kubectl describe pvc <pvc-name> -n <namespace>

# 2. 检查StorageClass是否存在
kubectl get storageclass

# 3. 检查供应器Pod状态
kubectl get pods -n kube-system | grep provisioner

# 4. 查看供应器日志
kubectl logs -n kube-system <provisioner-pod-name>
```

### 2. 动态供应失败

**问题现象**: PVC创建时供应器无法创建PV

**解决步骤**:
```bash
# 1. 检查供应器配置
kubectl get storageclass <sc-name> -o yaml

# 2. 验证存储后端可达性
# 根据具体的存储后端进行验证

# 3. 检查RBAC权限
kubectl auth can-i create persistentvolumes --as=system:serviceaccount:kube-system:<provisioner-sa>

# 4. 查看详细错误日志
kubectl logs -n kube-system <provisioner-pod-name> --tail=100
```

### 3. 存储扩容失败

**问题现象**: PVC扩容操作失败或无响应

**解决步骤**:
```bash
# 1. 检查StorageClass是否支持扩容
kubectl get storageclass <sc-name> -o jsonpath='{.allowVolumeExpansion}'

# 2. 检查底层存储是否支持在线扩容
# 根据具体存储后端文档确认

# 3. 查看扩容事件
kubectl describe pvc <pvc-name> -n <namespace> | grep -A 10 Events

# 4. 手动验证存储大小
kubectl exec -it <pod-name> -n <namespace> -- df -h
```

---

## 🧪 实践练习

### 练习1：StorageClass配置
配置不同类型的StorageClass，包括本地存储、NFS和云存储。

### 练习2：动态供应验证
创建多个使用不同StorageClass的PVC，验证动态供应机制。

### 练习3：存储扩容实践
配置支持扩容的StorageClass，实践PVC在线扩容操作。

### 练习4：故障排查演练
模拟各种StorageClass相关故障，练习诊断和修复技能。

---

## 📚 扩展阅读

### 官方文档
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- [Dynamic Volume Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)
- [Volume Expansion](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims)

### 相关案例
- [PV/PVC基础入门](../pv-pvc-basics/)
- [StorageClass高级特性](../storage-class-advanced/)
- [生产环境最佳实践](../pv-pvc-production/)

### 进阶主题
- CSI驱动开发
- 存储拓扑感知
- 存储性能调优
- 多租户存储隔离

---

## 📋 清理资源

```bash
# 删除测试Pod
kubectl delete pod dynamic-storage-pod -n storageclass-demo

# 删除PVC
kubectl delete pvc --all -n storageclass-demo

# 等待PV自动删除（Delete回收策略）
kubectl get pv

# 删除StorageClass（谨慎操作）
# kubectl delete storageclass local-path

# 删除命名空间
kubectl delete namespace storageclass-demo
```

---

> **💡 提示**: StorageClass是实现存储自动化的关键组件，建议在测试环境中充分验证配置后再应用到生产环境。注意不同云厂商的StorageClass参数可能有所差异。