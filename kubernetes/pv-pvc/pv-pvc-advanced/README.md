# ⚡ Kubernetes PV/PVC高级特性实战

> 深入探索Kubernetes PV/PVC的高级功能：访问模式详解、回收策略优化、容量调整、存储迁移等企业级特性

## 📋 案例概述

本案例专注于Kubernetes PV/PVC的高级配置和企业级特性，帮助您掌握生产环境中存储资源的精细化管理和优化配置。

### 🔧 核心技能点

- **高级访问模式**: RWOP、多访问模式组合使用
- **回收策略优化**: Retain策略的数据保护、Delete策略的自动化清理
- **容量调整**: 在线扩容、存储压缩、容量规划
- **存储迁移**: PV/PVC数据迁移、跨集群存储复制
- **存储性能调优**: I/O优化、缓存配置、QoS设置
- **存储安全**: 加密配置、访问控制、审计日志

### 🎯 适用人群

- 有经验的DevOps工程师
- 存储架构师
- 云平台管理员
- 性能优化专家

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建专用命名空间
kubectl create namespace pv-pvc-advanced

# 检查集群版本和支持的特性
kubectl version
kubectl api-versions | grep storage

# 检查存储扩展支持
kubectl get storageclass -o jsonpath='{range .items[*]}{.metadata.name}: {.allowVolumeExpansion}{"\n"}{end}'
```

### 2. 准备测试环境

```bash
# 创建测试目录
mkdir -p /tmp/k8s-advanced-pv/{fast,slow,encrypted}

# 设置权限
chmod 777 /tmp/k8s-advanced-pv/{fast,slow,encrypted}
```

---

## 📚 详细教程

### 1. 高级访问模式配置

#### 1.1 ReadWriteOncePod (RWOP) 访问模式

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-rwop-example
  labels:
    type: local
    performance: high
spec:
  storageClassName: fast-storage
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOncePod  # Kubernetes 1.22+ 支持
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: "/tmp/k8s-advanced-pv/fast"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-rwop-example
  namespace: pv-pvc-advanced
spec:
  accessModes:
    - ReadWriteOncePod
  resources:
    requests:
      storage: 15Gi
  storageClassName: fast-storage
```

#### 1.2 多访问模式组合使用

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-multi-mode
  labels:
    type: shared
spec:
  storageClassName: shared-storage
  capacity:
    storage: 50Gi
  accessModes:
    - ReadWriteMany
    - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    server: nfs-shared.example.com
    path: "/shared/data"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-readwrite-many
  namespace: pv-pvc-advanced
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 30Gi
  storageClassName: shared-storage
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-readonly-many
  namespace: pv-pvc-advanced
spec:
  accessModes:
    - ReadOnlyMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: shared-storage
```

### 2. 回收策略高级配置

#### 2.1 Retain策略的数据保护

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-retain-protected
  labels:
    data: critical
    retention: protected
  annotations:
    pv.kubernetes.io/provisioned-by: manual
    backup/schedule: "daily"
    backup/retention: "30d"
spec:
  storageClassName: protected-storage
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: "/tmp/k8s-advanced-pv/protected"
---
# 对应的备份Job配置
apiVersion: batch/v1
kind: Job
metadata:
  name: pv-backup-job
  namespace: pv-pvc-advanced
spec:
  template:
    spec:
      containers:
      - name: backup
        image: backup-tools:latest
        command: ["/backup-script.sh"]
        env:
        - name: PV_NAME
          value: "pv-retain-protected"
        - name: BACKUP_DEST
          value: "s3://backup-bucket/pv-backups/"
        volumeMounts:
        - name: pv-data
          mountPath: /data
      restartPolicy: OnFailure
      volumes:
      - name: pv-data
        persistentVolumeClaim:
          claimName: pvc-retain-example
```

#### 2.2 Delete策略的自动化清理

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-auto-cleanup
  labels:
    data: temporary
    cleanup: automatic
  finalizers:
  - kubernetes.io/pv-protection
spec:
  storageClassName: temp-storage
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  hostPath:
    path: "/tmp/k8s-advanced-pv/temp"
---
# 清理策略配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: cleanup-policy
  namespace: pv-pvc-advanced
data:
  retention-period: "7d"
  cleanup-schedule: "0 2 * * *"  # 每天凌晨2点执行
  size-threshold: "1Gi"
```

### 3. 容量调整和性能优化

#### 3.1 在线容量扩展

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-expandable
  namespace: pv-pvc-advanced
  annotations:
    volume.beta.kubernetes.io/storage-class: expandable-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: expandable-storage
---
# 扩容操作脚本
apiVersion: v1
kind: ConfigMap
metadata:
  name: expansion-scripts
  namespace: pv-pvc-advanced
data:
  expand-pvc.sh: |
    #!/bin/bash
    PVC_NAME=$1
    NEW_SIZE=$2
    NAMESPACE=${3:-default}
    
    echo "Expanding PVC $PVC_NAME to $NEW_SIZE in namespace $NAMESPACE"
    
    kubectl patch pvc $PVC_NAME -n $NAMESPACE -p \
      '{"spec":{"resources":{"requests":{"storage":"'$NEW_SIZE'"}}}}'
    
    # 监控扩容状态
    while true; do
      STATUS=$(kubectl get pvc $PVC_NAME -n $NAMESPACE -o jsonpath='{.status.conditions[?(@.type=="Resizing")].status}')
      if [ "$STATUS" != "True" ]; then
        echo "Expansion completed"
        break
      fi
      sleep 5
    done
```

#### 3.2 存储性能调优

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: performance-optimized
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io2
  iopsPerGB: "100"
  fsType: ext4
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
mountOptions:
  - noatime
  - nodiratime
  - barrier=0
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: storage-quota
  namespace: pv-pvc-advanced
spec:
  hard:
    requests.storage: 200Gi
    persistentvolumeclaims: "20"
  scopes:
  - NotTerminating
```

### 4. 存储迁移和复制

#### 4.1 PV/PVC数据迁移

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pv-migration-job
  namespace: pv-pvc-advanced
spec:
  template:
    spec:
      containers:
      - name: migrator
        image: storage-migrator:latest
        command: ["/migrate.sh"]
        env:
        - name: SOURCE_PVC
          value: "source-pvc-name"
        - name: DEST_PVC
          value: "destination-pvc-name"
        - name: NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        volumeMounts:
        - name: source-data
          mountPath: /source
        - name: dest-data
          mountPath: /dest
      restartPolicy: OnFailure
      volumes:
      - name: source-data
        persistentVolumeClaim:
          claimName: source-pvc-name
      - name: dest-data
        persistentVolumeClaim:
          claimName: destination-pvc-name
---
# 迁移状态监控
apiVersion: v1
kind: ConfigMap
metadata:
  name: migration-monitoring
  namespace: pv-pvc-advanced
data:
  monitor.sh: |
    #!/bin/bash
    JOB_NAME="pv-migration-job"
    NAMESPACE="pv-pvc-advanced"
    
    while true; do
      STATUS=$(kubectl get job $JOB_NAME -n $NAMESPACE -o jsonpath='{.status.conditions[?(@.type=="Complete")].status}')
      if [ "$STATUS" == "True" ]; then
        echo "Migration completed successfully"
        break
      fi
      
      FAILED=$(kubectl get job $JOB_NAME -n $NAMESPACE -o jsonpath='{.status.conditions[?(@.type=="Failed")].status}')
      if [ "$FAILED" == "True" ]; then
        echo "Migration failed"
        exit 1
      fi
      
      echo "Migration in progress..."
      sleep 30
    done
```

#### 4.2 跨集群存储复制

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cross-cluster-replicator
  namespace: pv-pvc-advanced
spec:
  replicas: 1
  selector:
    matchLabels:
      app: replicator
  template:
    metadata:
      labels:
        app: replicator
    spec:
      containers:
      - name: replicator
        image: cross-cluster-replicator:latest
        env:
        - name: SOURCE_CLUSTER_ENDPOINT
          value: "https://source-cluster-api:6443"
        - name: DEST_CLUSTER_ENDPOINT
          value: "https://dest-cluster-api:6443"
        - name: REPLICATION_SCHEDULE
          value: "0 */6 * * *"  # 每6小时同步一次
        volumeMounts:
        - name: config
          mountPath: /etc/replicator
      volumes:
      - name: config
        configMap:
          name: replication-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: replication-config
  namespace: pv-pvc-advanced
data:
  config.yaml: |
    replication:
      enabled: true
      schedule: "0 */6 * * *"
      retention:
        local: 7d
        remote: 30d
      compression: true
      encryption: true
```

### 5. 存储安全配置

#### 5.1 加密存储配置

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: encrypted-storage
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  fsType: ext4
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-west-2:123456789012:key/abcd1234-a123-456a-a12b-a123b4cd56ef"
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
---
apiVersion: v1
kind: Secret
metadata:
  name: storage-encryption-keys
  namespace: pv-pvc-advanced
type: Opaque
data:
  encryption-key: <base64-encoded-key>
```

#### 5.2 访问控制和审计

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: storage-admin-role
  namespace: pv-pvc-advanced
rules:
- apiGroups: [""]
  resources: ["persistentvolumes", "persistentvolumeclaims"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: ["storage.k8s.io"]
  resources: ["storageclasses"]
  verbs: ["get", "list", "watch"]
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: audit-policy
  namespace: pv-pvc-advanced
data:
  audit-policy.yaml: |
    apiVersion: audit.k8s.io/v1
    kind: Policy
    rules:
    - level: RequestResponse
      resources:
      - group: ""
        resources: ["persistentvolumes", "persistentvolumeclaims"]
      - group: "storage.k8s.io"
        resources: ["storageclasses"]
      verbs: ["create", "update", "delete", "patch"]
```

---

## 🔧 实践操作

### 1. 高级特性部署

```bash
# 1. 部署高级PV配置
kubectl apply -f advanced-pv-configs.yaml

# 2. 创建高级PVC
kubectl apply -f advanced-pvc-configs.yaml

# 3. 验证访问模式
kubectl get pv,pvc -n pv-pvc-advanced

# 4. 测试RWOP访问模式
kubectl apply -f rwop-test-pod.yaml
```

### 2. 容量扩展测试

```bash
# 1. 创建可扩展PVC
kubectl apply -f expandable-pvc.yaml

# 2. 执行扩容操作
kubectl patch pvc pvc-expandable -n pv-pvc-advanced -p \
  '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'

# 3. 监控扩容过程
kubectl describe pvc pvc-expandable -n pv-pvc-advanced

# 4. 验证扩容结果
kubectl exec -it test-pod -n pv-pvc-advanced -- df -h | grep /data
```

### 3. 存储迁移演练

```bash
# 1. 准备源数据
kubectl apply -f source-pvc.yaml
kubectl apply -f data-populator-pod.yaml

# 2. 执行迁移
kubectl apply -f migration-job.yaml

# 3. 验证迁移结果
kubectl apply -f verification-pod.yaml
kubectl logs verification-pod -n pv-pvc-advanced
```

---

## 📊 监控和告警

### 1. 存储使用监控

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: storage-monitor
  namespace: pv-pvc-advanced
spec:
  selector:
    matchLabels:
      app: storage-exporter
  endpoints:
  - port: metrics
    interval: 30s
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: storage-alerts
  namespace: pv-pvc-advanced
data:
  alerts.yaml: |
    groups:
    - name: storage.alerts
      rules:
      - alert: PVCStorageUsageHigh
        expr: kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "PVC {{ $labels.persistentvolumeclaim }} storage usage is high"
          description: "{{ $labels.persistentvolumeclaim }} is using {{ $value }}% of its storage"
```

### 2. 性能监控配置

```bash
# 存储性能监控脚本
cat > storage-performance-monitor.sh << 'EOF'
#!/bin/bash

NAMESPACE="pv-pvc-advanced"
THRESHOLD_IOPS=1000
THRESHOLD_LATENCY=50  # ms

echo "=== Storage Performance Monitor ==="

for pvc in $(kubectl get pvc -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
  echo "Checking PVC: $pvc"
  
  # 获取存储使用情况
  USAGE=$(kubectl exec -it <pod-using-pvc> -n $NAMESPACE -- iostat -x 1 1 | tail -1 | awk '{print $10}')
  
  # 检查IOPS
  IOPS=$(kubectl exec -it <pod-using-pvc> -n $NAMESPACE -- iostat -x 1 1 | tail -1 | awk '{print $4+$5}')
  
  echo "  Usage: ${USAGE}%"
  echo "  IOPS: $IOPS"
  
  if (( $(echo "$IOPS > $THRESHOLD_IOPS" | bc -l) )); then
    echo "  ⚠️  High IOPS detected!"
  fi
done
EOF
```

---

## ⚠️ 常见问题和解决方案

### 1. 容量扩展失败

**问题**: PVC扩容操作失败或无响应

**解决方案**:
```bash
# 1. 检查StorageClass是否支持扩展
kubectl get storageclass <sc-name> -o jsonpath='{.allowVolumeExpansion}'

# 2. 检查底层存储支持
# 根据具体存储后端文档确认

# 3. 手动触发文件系统扩容
kubectl exec -it <pod-name> -n <namespace> -- resize2fs /dev/<device>

# 4. 查看详细错误信息
kubectl describe pvc <pvc-name> -n <namespace>
```

### 2. RWOP访问模式不支持

**问题**: Pod启动失败，报错不支持ReadWriteOncePod访问模式

**解决方案**:
```bash
# 1. 检查Kubernetes版本
kubectl version | grep Server

# 2. RWOP需要Kubernetes 1.22+版本
# 如果版本较低，降级使用ReadWriteOnce

# 3. 检查存储插件支持
kubectl get csidrivers
```

### 3. 存储迁移数据不一致

**问题**: 迁移后的数据与源数据不一致

**解决方案**:
```bash
# 1. 使用校验和验证数据完整性
kubectl exec -it source-pod -n <namespace> -- find /data -type f -exec md5sum {} \; > source-md5.txt
kubectl exec -it dest-pod -n <namespace> -- find /data -type f -exec md5sum {} \; > dest-md5.txt

# 2. 比较校验和
diff source-md5.txt dest-md5.txt

# 3. 重新执行迁移
# 确保迁移过程中没有写入操作
```

---

## 🧪 实践练习

### 练习1：访问模式优化
配置不同访问模式的PVC，测试其并发访问能力和性能差异。

### 练习2：容量管理策略
实现自动化的存储容量监控和扩容策略。

### 练习3：存储迁移方案
设计并实现完整的PV/PVC数据迁移方案。

### 练习4：安全存储配置
配置加密存储和访问控制策略，确保数据安全。

---

## 📚 扩展阅读

### 官方文档
- [Volume Expansion](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims)
- [ReadWriteOncePod Access Mode](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes)
- [Storage Security](https://kubernetes.io/docs/concepts/security/)

### 相关案例
- [StorageClass高级特性](../storage-class-advanced/)
- [生产环境最佳实践](../pv-pvc-production/)
- [故障排查和监控](../pv-pvc-troubleshooting/)

### 进阶主题
- CSI驱动开发
- 存储快照和备份
- 多云存储管理
- 存储成本优化

---

## 📋 清理资源

```bash
# 删除测试Pod
kubectl delete pod --all -n pv-pvc-advanced

# 删除PVC
kubectl delete pvc --all -n pv-pvc-advanced

# 删除PV
kubectl delete pv pv-rwop-example pv-multi-mode pv-retain-protected pv-auto-cleanup

# 删除StorageClass（谨慎操作）
# kubectl delete storageclass performance-optimized encrypted-storage

# 删除命名空间
kubectl delete namespace pv-pvc-advanced

# 清理本地测试目录
rm -rf /tmp/k8s-advanced-pv/
```

---

> **💡 提示**: 高级存储特性需要根据具体业务场景谨慎配置，建议在测试环境中充分验证后再应用到生产环境。注意监控存储性能和成本。