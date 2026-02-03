# Kubernetes资源不足问题排查实战

## 1. 案例概述

本案例提供了Kubernetes环境中资源不足问题的排查方法和解决方案，包括：
- CPU资源不足
- 内存资源不足
- 磁盘资源不足
- 节点资源压力
- 资源配额和限制问题
- 资源碎片问题

## 2. 环境准备

- Kubernetes集群（v1.20+）
- kubectl命令行工具
- 集群监控工具（如Prometheus+Grafana，可选）
- 节点访问权限（用于磁盘和系统资源检查）

## 3. 常见资源不足问题排查

### 3.1 CPU资源不足

**症状**：
- Pod状态显示CPUThrottled
- 应用响应缓慢
- kubectl top pod显示CPU使用率接近或达到限制
- 节点CPU使用率过高

**排查步骤**：

1. 查看Pod资源使用情况：
   ```bash
   kubectl top pod <pod-name> -n <namespace>
   ```

2. 查看Pod资源限制配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 15 resources
   ```

3. 查看节点CPU使用情况：
   ```bash
   kubectl top node
   kubectl describe node <node-name> | grep -A 10 Allocated
   ```

4. 查看节点上运行的Pod及其CPU使用情况：
   ```bash
   kubectl get pods -n <namespace> -o wide | grep <node-name>
   kubectl top pod -n <namespace> | grep <node-name>
   ```

5. 检查是否有CPU密集型应用：
   ```bash
   kubectl top pod -n <namespace> --sort-by=cpu
   ```

**解决方案示例**：

```yaml
# 调整Pod CPU资源限制
aapiVersion: v1
kind: Pod
metadata:
  name: cpu-intensive-app
spec:
  containers:
  - name: app-container
    image: your-app-image:latest
    resources:
      requests:
        cpu: "500m"
        memory: "512Mi"
      limits:
        cpu: "1"
        memory: "1Gi"
```

### 3.2 内存资源不足

**症状**：
- Pod状态显示OOMKilled
- 应用崩溃并显示内存不足错误
- kubectl top pod显示内存使用率接近或达到限制
- 节点内存使用率过高

**排查步骤**：

1. 查看Pod资源使用情况：
   ```bash
   kubectl top pod <pod-name> -n <namespace>
   ```

2. 查看Pod事件，确认OOMKilled原因：
   ```bash
   kubectl describe pod <pod-name> -n <namespace> | grep -A 10 Events
   ```

3. 查看节点内存使用情况：
   ```bash
   kubectl top node
   kubectl describe node <node-name> | grep -A 10 Allocated
   ```

4. 检查应用内存泄漏：
   ```bash
   kubectl exec -it <pod-name> -n <namespace> -- ps aux
   ```

**解决方案示例**：

```yaml
# 调整Pod内存资源限制
aapiVersion: v1
kind: Pod
metadata:
  name: memory-intensive-app
spec:
  containers:
  - name: app-container
    image: your-app-image:latest
    resources:
      requests:
        cpu: "500m"
        memory: "1Gi"
      limits:
        cpu: "1"
        memory: "2Gi"  # 增加内存限制
```

### 3.3 磁盘资源不足

**症状**：
- Pod无法创建或运行失败，提示磁盘空间不足
- 节点磁盘使用率过高
- 持久化卷(PV)空间不足
- 容器日志无法写入

**排查步骤**：

1. 检查节点磁盘使用情况：
   ```bash
   kubectl describe node <node-name> | grep -A 5 Conditions
   kubectl describe node <node-name> | grep -A 10 Capacity
   ```

2. 登录节点检查磁盘空间：
   ```bash
   ssh <node-ip>
   df -h
   ```

3. 检查持久化卷使用情况：
   ```bash
   kubectl get pv
   kubectl get pvc -n <namespace>
   ```

4. 检查容器日志使用情况：
   ```bash
   kubectl logs --tail=100 <pod-name> -n <namespace> > /dev/null
   ```

**解决方案示例**：

```yaml
# 清理旧容器和镜像（在节点上执行）
docker system prune -f

# 增加持久化卷大小
aapiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi  # 增加存储请求
  storageClassName: standard
```

### 3.4 节点资源压力

**症状**：
- 节点状态显示Ready,SchedulingDisabled
- 节点条件显示DiskPressure、MemoryPressure或PIDPressure
- Pod无法调度到节点
- 节点上的Pod频繁重启

**排查步骤**：

1. 查看节点状态和条件：
   ```bash
   kubectl get node <node-name> -o yaml | grep -A 20 conditions
   ```

2. 查看节点资源使用情况：
   ```bash
   kubectl top node <node-name>
   kubectl describe node <node-name> | grep -A 20 Allocated
   ```

3. 检查节点上的Pod：
   ```bash
   kubectl get pods -A -o wide | grep <node-name>
   ```

4. 登录节点检查系统资源：
   ```bash
   ssh <node-ip>
   top
   free -h
   df -h
   ```

**解决方案示例**：

```bash
# 驱逐节点上的非关键Pod
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# 清理节点资源
docker system prune -f
journalctl --vacuum-time=7d

# 恢复节点调度
kubectl uncordon <node-name>
```

### 3.5 资源配额和限制问题

**症状**：
- Pod创建失败，提示超出资源配额
- 命名空间资源使用率接近或达到限制
- 无法扩展应用

**排查步骤**：

1. 查看命名空间资源配额：
   ```bash
   kubectl get resourcequota -n <namespace>
   kubectl describe resourcequota <quota-name> -n <namespace>
   ```

2. 查看命名空间资源使用情况：
   ```bash
   kubectl describe namespace <namespace>
   ```

3. 检查Pod资源请求是否超过配额：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 15 resources
   ```

**解决方案示例**：

```yaml
# 调整资源配额
aapiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: default
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "20"
```

### 3.6 资源碎片问题

**症状**：
- 集群总体资源充足，但Pod无法调度
- 节点资源分布不均衡
- 大资源请求的Pod无法找到合适节点

**排查步骤**：

1. 查看节点资源分布：
   ```bash
   kubectl top node
   kubectl describe node | grep -A 10 Allocated | head -40
   ```

2. 检查调度器事件：
   ```bash
   kubectl get events -n <namespace> | grep FailedScheduling
   ```

3. 查看Pod调度约束：
   ```bash
   kubectl get pod <pending-pod> -n <namespace> -o yaml | grep -A 20 nodeSelector
   kubectl get pod <pending-pod> -n <namespace> -o yaml | grep -A 20 affinity
   ```

**解决方案示例**：

```bash
# 均衡节点资源分布
kubectl drain <overloaded-node> --ignore-daemonsets --delete-emptydir-data
# 等待Pod重新调度到其他节点
kubectl uncordon <overloaded-node>

# 使用Pod拓扑分散约束
aapiVersion: v1
kind: Pod
metadata:
  name: balanced-pod
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: my-app
  containers:
  - name: app-container
    image: your-app-image:latest
    resources:
      requests:
        cpu: "500m"
        memory: "512Mi"
```

## 4. 实用工具和命令

### 4.1 资源监控命令

```bash
# 查看所有节点资源使用情况
kubectl top node

# 查看特定节点资源使用情况
kubectl top node <node-name>

# 查看命名空间下所有Pod资源使用情况
kubectl top pod -n <namespace>

# 按CPU使用率排序
kubectl top pod -n <namespace> --sort-by=cpu

# 按内存使用率排序
kubectl top pod -n <namespace> --sort-by=memory

# 查看节点详细资源信息
kubectl describe node <node-name>

# 查看命名空间资源配额和使用情况
kubectl describe namespace <namespace>
```

### 4.2 资源清理命令

```bash
# 清理终止状态的Pod
kubectl delete pods --field-selector=status.phase==Failed -n <namespace>
kubectl delete pods --field-selector=status.phase==Succeeded -n <namespace>

# 清理未使用的PVC
kubectl delete pvc --field-selector=status.phase==Released -n <namespace>

# 清理未使用的ConfigMap和Secret
kubectl delete configmap --field-selector=metadata.name!=kube-root-ca.crt -n <namespace>
kubectl delete secret --field-selector=metadata.name!=default-token* -n <namespace>
```

### 4.3 资源分析脚本

```bash
#!/bin/bash
# 资源分析脚本

NAMESPACE=${1:-default}

# 查看命名空间资源使用情况
echo "=== 命名空间资源使用情况 ==="
kubectl top pod -n $NAMESPACE

# 查看命名空间资源配额
echo -e "\n=== 命名空间资源配额 ==="
kubectl get resourcequota -n $NAMESPACE

# 查看节点资源使用情况
echo -e "\n=== 节点资源使用情况 ==="
kubectl top node

# 查看高资源消耗Pod
echo -e "\n=== 高CPU消耗Pod ==="
kubectl top pod -n $NAMESPACE --sort-by=cpu | head -10

# 查看高内存消耗Pod
echo -e "\n=== 高内存消耗Pod ==="
kubectl top pod -n $NAMESPACE --sort-by=memory | head -10
```

## 5. 故障模拟和练习

### 5.1 模拟CPU资源不足

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cpu-stress-test
spec:
  containers:
  - name: stress-container
    image: polinux/stress:latest
    command: ["stress", "--cpu", "2", "--timeout", "300"]
    resources:
      limits:
        cpu: "1"  # 限制CPU为1核，但容器尝试使用2核
        memory: "128Mi"
```

### 5.2 模拟内存资源不足

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: memory-stress-test
spec:
  containers:
  - name: stress-container
    image: polinux/stress:latest
    command: ["stress", "--vm", "1", "--vm-bytes", "512M", "--timeout", "300"]
    resources:
      limits:
        cpu: "1"
        memory: "256Mi"  # 限制内存为256Mi，但容器尝试使用512Mi
```

### 5.3 模拟磁盘资源不足

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: disk-stress-test
spec:
  containers:
  - name: stress-container
    image: busybox:1.35
    command: ["/bin/sh", "-c", "dd if=/dev/zero of=/testfile bs=1M count=10000; sleep 300"]
    volumeMounts:
    - name: test-volume
      mountPath: /data
  volumes:
  - name: test-volume
    emptyDir:
      sizeLimit: 1Gi  # 限制emptyDir大小为1Gi，但容器尝试写入10Gi
```

## 6. 最佳实践

1. **合理设置资源请求和限制**：
   - 根据应用实际需求设置resources.requests和resources.limits
   - 避免设置过低的资源限制导致频繁OOMKilled或CPUThrottled
   - 避免设置过高的资源请求导致资源浪费和调度困难

2. **实施资源配额管理**：
   - 为每个命名空间设置合理的资源配额
   - 定期监控和调整资源配额

3. **优化资源使用**：
   - 优化应用代码，减少资源消耗
   - 使用更轻量级的基础镜像
   - 合理设置Pod生命周期，及时清理资源

4. **实施节点资源监控**：
   - 部署Prometheus+Grafana等监控工具
   - 设置资源使用率告警
   - 定期分析资源使用趋势

5. **实施集群自动扩缩容**：
   - 配置Cluster Autoscaler实现节点自动扩缩容
   - 配置Horizontal Pod Autoscaler实现Pod自动扩缩容

6. **资源碎片管理**：
   - 使用Pod拓扑分散约束均衡资源分布
   - 定期清理未使用的资源
   - 考虑使用节点池隔离不同类型的工作负载

7. **定期资源审计**：
   - 定期检查和优化资源使用
   - 识别和移除僵尸资源
   - 调整资源配置以适应应用需求变化

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

本案例提供了Kubernetes环境中资源不足问题的排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决CPU、内存、磁盘等资源不足问题
- 了解Kubernetes资源管理的工作原理
- 掌握资源监控和优化的最佳实践
- 建立良好的资源管理习惯

通过合理的资源配置、监控和优化，您将能够更高效地利用Kubernetes集群资源，提高应用的稳定性和性能。