# Kubernetes持久化存储问题排查实战

## 1. 案例概述

本案例提供了Kubernetes环境中持久化存储问题的排查方法和解决方案，包括：
- PVC绑定失败
- PV挂载失败
- 存储类配置问题
- 持久化卷扩容问题
- 存储资源不足问题
- 存储访问模式问题
- 存储插件问题

## 2. 环境准备

- Kubernetes集群（v1.20+）
- kubectl命令行工具
- 集群访问权限
- 存储系统访问权限（如NFS服务器、云存储控制台等，可选）

## 3. 常见持久化存储问题排查

### 3.1 PVC绑定失败

**症状**：
- PVC状态显示Pending
- 事件信息显示"waiting for a volume to be created, either by external provisioner 'provisioner.example.com' or manually created by system administrator"
- 或"no persistent volumes available for this claim and no storage class is set"

**排查步骤**：

1. 查看PVC事件：
   ```bash
   kubectl describe pvc <pvc-name> -n <namespace>
   ```

2. 查看存储类配置：
   ```bash
   kubectl get storageclass
   kubectl describe storageclass <storageclass-name>
   ```

3. 查看是否有可用的PV：
   ```bash
   kubectl get pv
   kubectl describe pv <pv-name>
   ```

4. 检查PVC和PV的匹配条件：
   - 存储类名称
   - 资源请求大小
   - 访问模式
   - 选择器标签

**解决方案示例**：

```yaml
# 修复PVC存储类配置
aapiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: fixed-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard  # 确保存储类存在
  resources:
    requests:
      storage: 1Gi
```

### 3.2 PV挂载失败

**症状**：
- Pod状态显示ContainerCreating
- 事件信息显示"Unable to mount volumes for pod": "timeout expired waiting for volumes to attach or mount for pod"
- 或"MountVolume.SetUp failed for volume": "mount failed: exit status 32"

**排查步骤**：

1. 查看Pod事件：
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. 查看PV和PVC状态：
   ```bash
   kubectl get pv <pv-name>
   kubectl get pvc <pvc-name> -n <namespace>
   ```

3. 查看PV配置：
   ```bash
   kubectl get pv <pv-name> -o yaml
   ```

4. 登录节点检查挂载情况：
   ```bash
   ssh <node-ip>
   mount | grep <pv-name>
   ```

**解决方案示例**：

```yaml
# 修复PV挂载配置
aapiVersion: v1
kind: PersistentVolume
metadata:
  name: fixed-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  nfs:
    path: /exports/share1  # 确保NFS路径存在且可访问
    server: nfs-server.example.com  # 确保NFS服务器可达
  storageClassName: standard
```

### 3.3 存储类配置问题

**症状**：
- PVC无法自动创建PV
- 事件信息显示"failed to provision volume with StorageClass": "provisioning failed"
- 或"no provisioner specified for StorageClass"

**排查步骤**：

1. 查看存储类配置：
   ```bash
   kubectl get storageclass <storageclass-name> -o yaml
   ```

2. 检查存储类控制器运行状态：
   ```bash
   kubectl get pods -n kube-system | grep <provisioner-name>
   kubectl logs <provisioner-pod-name> -n kube-system
   ```

3. 检查存储类参数配置：
   ```bash
   kubectl describe storageclass <storageclass-name>
   ```

**解决方案示例**：

```yaml
# 修复存储类配置
aapiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fixed-storageclass
provisioner: kubernetes.io/aws-ebs  # 确保使用正确的provisioner
parameters:
  type: gp2
  encrypted: "false"
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: Immediate
```

### 3.4 持久化卷扩容问题

**症状**：
- PVC扩容后容量未增加
- 事件信息显示"PersistentVolumeClaim expansion failed": "resize volume failed"
- 或"PersistentVolumeClaim expansion is not supported for this storage class"

**排查步骤**：

1. 检查存储类是否支持扩容：
   ```bash
   kubectl get storageclass <storageclass-name> -o jsonpath='{.allowVolumeExpansion}'
   ```

2. 查看PVC扩容事件：
   ```bash
   kubectl describe pvc <pvc-name> -n <namespace>
   ```

3. 检查PV类型是否支持扩容：
   ```bash
   kubectl get pv <pv-name> -o yaml | grep -A 5 spec
   ```

4. 检查Pod是否需要重启：
   ```bash
   kubectl get pod <pod-name> -n <namespace>
   ```

**解决方案示例**：

```yaml
# 启用存储类扩容支持
aapiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: expandable-storageclass
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
reclaimPolicy: Delete
allowVolumeExpansion: true  # 启用扩容支持
volumeBindingMode: Immediate
```

### 3.5 存储资源不足问题

**症状**：
- PVC绑定失败
- 事件信息显示"no persistent volumes available for this claim: Insufficient storage"
- 或"provisioning failed: no available volume size"

**排查步骤**：

1. 查看可用的PV和容量：
   ```bash
   kubectl get pv
   ```

2. 检查存储系统容量：
   - 对于云存储，查看云控制台中的存储容量
   - 对于本地存储，登录节点检查磁盘空间
   - 对于NFS，登录NFS服务器检查共享目录空间

3. 检查PVC资源请求大小：
   ```bash
   kubectl get pvc <pvc-name> -n <namespace> -o yaml | grep -A 5 resources
   ```

**解决方案示例**：

```yaml
# 调整PVC资源请求大小
aapiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: small-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 512Mi  # 降低存储请求大小
```

### 3.6 存储访问模式问题

**症状**：
- PVC绑定失败
- 事件信息显示"no persistent volumes available for this claim and no storage class is set"
- 或"requested access mode incompatible with available volumes"

**排查步骤**：

1. 查看PVC访问模式：
   ```bash
   kubectl get pvc <pvc-name> -n <namespace> -o yaml | grep -A 5 accessModes
   ```

2. 查看PV访问模式：
   ```bash
   kubectl get pv <pv-name> -o yaml | grep -A 5 accessModes
   ```

3. 检查访问模式兼容性：
   - ReadWriteOnce (RWO): 只能被一个节点挂载为读写
   - ReadOnlyMany (ROX): 可以被多个节点挂载为只读
   - ReadWriteMany (RWX): 可以被多个节点挂载为读写

**解决方案示例**：

```yaml
# 调整PVC访问模式
aapiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rwx-pvc
spec:
  accessModes:
    - ReadWriteMany  # 使用正确的访问模式
  storageClassName: nfs-storage  # 使用支持RWX的存储类
  resources:
    requests:
      storage: 1Gi
```

### 3.7 存储插件问题

**症状**：
- PV无法创建或挂载
- 事件信息显示"Failed to get plugin from volumeSpec"
- 或"failed to find driver name for volume plugin"

**排查步骤**：

1. 检查存储插件运行状态：
   ```bash
   kubectl get pods -n kube-system | grep <plugin-name>
   ```

2. 查看存储插件日志：
   ```bash
   kubectl logs <plugin-pod-name> -n kube-system
   ```

3. 检查存储插件配置：
   ```bash
   kubectl get daemonset <plugin-daemonset> -n kube-system -o yaml
   ```

4. 检查节点上的存储插件状态：
   ```bash
   ssh <node-ip>
   docker ps | grep <plugin-name>
   ```

**解决方案示例**：

```yaml
# 修复存储插件配置
aapiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fixed-storage-plugin
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: storage-plugin
  template:
    metadata:
      labels:
        name: storage-plugin
    spec:
      containers:
      - name: storage-plugin
        image: storage-plugin:latest
        volumeMounts:
        - name: plugin-dir
          mountPath: /var/lib/kubelet/plugins
        - name: mountpoint-dir
          mountPath: /var/lib/kubelet/pods
          mountPropagation: Bidirectional
      volumes:
      - name: plugin-dir
        hostPath:
          path: /var/lib/kubelet/plugins
      - name: mountpoint-dir
        hostPath:
          path: /var/lib/kubelet/pods
```

## 4. 实用工具和命令

### 4.1 存储诊断命令

```bash
# 查看PVC状态
kubectl get pvc -n <namespace>
kubectl describe pvc <pvc-name> -n <namespace>

# 查看PV状态
kubectl get pv
kubectl describe pv <pv-name>

# 查看存储类
kubectl get storageclass
kubectl describe storageclass <storageclass-name>

# 查看Pod卷配置
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 20 volumes

# 查看Pod卷挂载情况
kubectl exec -it <pod-name> -n <namespace> -- df -h

# 检查节点上的卷挂载
ssh <node-ip> mount | grep kubelet
```

### 4.2 存储分析脚本

```bash
#!/bin/bash
# 存储分析脚本

NAMESPACE=${1:-default}

# 查看命名空间PVC状态
echo "=== 命名空间PVC状态 ==="
kubectl get pvc -n $NAMESPACE

# 查看所有PV状态
echo -e "\n=== 所有PV状态 ==="
kubectl get pv

# 查看存储类配置
echo -e "\n=== 存储类配置 ==="
kubectl get storageclass -o wide

# 查看PVC详细信息
echo -e "\n=== PVC详细信息 ==="
kubectl describe pvc -n $NAMESPACE

# 检查PV和PVC绑定关系
echo -e "\n=== PV和PVC绑定关系 ==="
kubectl get pvc -n $NAMESPACE -o json | jq -r '.items[] | "PVC: " + .metadata.name + " Bound to PV: " + .spec.volumeName + " StorageClass: " + (.spec.storageClassName // "None")'
```

### 4.3 存储性能测试

```bash
# 在Pod中测试存储性能
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash

dd if=/dev/zero of=/path/to/mount/point/testfile bs=1M count=1024 oflag=direct
dd if=/path/to/mount/point/testfile of=/dev/null bs=1M count=1024 iflag=direct

# 使用fio进行更全面的性能测试
fio --name=test --rw=randwrite --direct=1 --bs=4k --size=1G --numjobs=4 --time_based --runtime=60 --group_reporting
```

## 5. 故障模拟和练习

### 5.1 模拟PVC绑定失败

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: unbound-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: non-existent-sc  # 不存在的存储类
  resources:
    requests:
      storage: 1Gi
```

### 5.2 模拟PV挂载失败

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: unmountable-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  nfs:
    path: /non-existent-path  # 不存在的NFS路径
    server: non-existent-server.example.com  # 不存在的NFS服务器
  storageClassName: standard
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pv-mount-fail-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 1Gi
```

### 5.3 模拟存储访问模式不匹配

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: rwo-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce  # 仅支持RWO
  hostPath:
    path: /tmp/rwo-test
  storageClassName: standard
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rwx-mismatch-pvc
spec:
  accessModes:
    - ReadWriteMany  # 请求RWX，但PV仅支持RWO
  storageClassName: standard
  resources:
    requests:
      storage: 1Gi
```

## 6. 最佳实践

1. **使用合适的存储类**：
   - 为不同类型的工作负载选择合适的存储类
   - 确保存储类配置正确，包括provisioner、参数和扩容支持
   - 定期审查和清理未使用的存储类

2. **合理规划存储容量**：
   - 根据应用需求设置合理的存储请求大小
   - 考虑使用存储监控工具监控存储使用情况
   - 为增长型应用预留足够的存储空间

3. **使用适当的访问模式**：
   - 根据应用需求选择合适的访问模式（RWO、ROX、RWX）
   - 了解不同存储类型支持的访问模式
   - 避免使用不支持的访问模式组合

4. **实施存储备份策略**：
   - 定期备份持久化存储数据
   - 测试备份恢复流程
   - 考虑使用Kubernetes原生备份工具如Velero

5. **监控存储性能**：
   - 监控存储IOPS、延迟和吞吐量
   - 及时发现和解决存储性能问题
   - 根据性能需求调整存储类型

6. **优化存储配置**：
   - 为不同的应用场景优化存储参数
   - 考虑使用存储缓存提高性能
   - 合理设置存储回收策略

7. **定期清理存储资源**：
   - 及时清理未使用的PV和PVC
   - 清理过期的备份数据
   - 定期检查和清理存储系统中的垃圾数据

8. **使用存储CSI驱动**：
   - 优先使用CSI驱动而非in-tree驱动
   - 保持CSI驱动版本与Kubernetes版本兼容
   - 定期更新CSI驱动以获取新功能和 bug 修复

## 7. 版本兼容性

| Kubernetes版本 | 兼容性 |
|---------------|--------|
| v1.20.x       | ✅     |
| v1.21.x       | ✅     |
| v1.22.x       | ✅     |
| v1.23.x       | ✅     |
| v1.24.x       | ✅     |
| v1.25.x       | ✅     |
| v1.26.x       | ✅     |

## 8. 总结

本案例提供了Kubernetes环境中持久化存储问题的排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决各种持久化存储问题
- 了解Kubernetes持久化存储的工作原理
- 掌握存储类、PV和PVC的配置和管理技巧
- 建立良好的存储规划和管理习惯

通过合理的存储规划、配置和监控，您将能够提高Kubernetes集群中持久化存储的可靠性和性能，确保应用数据的安全和可用性。