# Kubernetes调度失败问题排查实战

## 1. 案例概述

本案例提供了Kubernetes环境中调度失败问题的排查方法和解决方案，包括：
- 资源不足导致的调度失败
- 节点亲和性/反亲和性导致的调度失败
- 污点和容忍度导致的调度失败
- Pod亲和性/反亲和性导致的调度失败
- 节点选择器导致的调度失败
- 调度器配置问题导致的调度失败
- 拓扑约束导致的调度失败

## 2. 环境准备

- Kubernetes集群（v1.20+）
- kubectl命令行工具
- 集群访问权限
- 调度器日志访问权限

## 3. 常见调度失败问题排查

### 3.1 资源不足导致的调度失败

**症状**：
- Pod状态显示Pending
- 事件信息显示"0/3 nodes are available: 3 Insufficient cpu."
- 或"0/3 nodes are available: 3 Insufficient memory."

**排查步骤**：

1. 查看Pod事件：
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. 查看节点资源使用情况：
   ```bash
   kubectl top node
   kubectl describe node <node-name> | grep -A 15 Allocated
   ```

3. 查看Pod资源请求：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 resources
   ```

4. 检查是否有足够的空闲资源：
   ```bash
   kubectl get nodes -o json | jq -r '.items[] | "Node: " + .metadata.name + " CPU: " + (.status.allocatable.cpu | tonumber | tostring) + " Memory: " + (.status.allocatable.memory)'
   ```

**解决方案示例**：

```yaml
# 降低Pod资源请求
aapiVersion: v1
kind: Pod
metadata:
  name: low-resource-pod
spec:
  containers:
  - name: app-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"  # 降低CPU请求
        memory: "128Mi"  # 降低内存请求
      limits:
        cpu: "500m"
        memory: "512Mi"
```

### 3.2 节点亲和性/反亲和性导致的调度失败

**症状**：
- Pod状态显示Pending
- 事件信息显示"0/3 nodes are available: 3 node(s) didn't match node selector."
- 或"0/3 nodes are available: 3 node(s) didn't satisfy existing pods anti-affinity rules."

**排查步骤**：

1. 查看Pod亲和性配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 30 affinity
   ```

2. 查看节点标签：
   ```bash
   kubectl get node --show-labels
   kubectl describe node <node-name> | grep -A 10 Labels
   ```

3. 检查节点亲和性规则是否匹配：
   ```bash
   # 检查节点是否有匹配的标签
   kubectl get node -l <key>=<value>
   ```

**解决方案示例**：

```yaml
# 修复节点亲和性配置
aapiVersion: v1
kind: Pod
metadata:
  name: fixed-node-affinity-pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd  # 确保集群中有带有disktype=ssd标签的节点
  containers:
  - name: app-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
```

### 3.3 污点和容忍度导致的调度失败

**症状**：
- Pod状态显示Pending
- 事件信息显示"0/3 nodes are available: 3 node(s) had taints that the pod didn't tolerate."

**排查步骤**：

1. 查看节点污点：
   ```bash
   kubectl describe node <node-name> | grep -A 5 Taints
   ```

2. 查看Pod容忍度配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 15 tolerations
   ```

3. 检查是否有匹配的容忍度：
   ```bash
   # 比较节点污点和Pod容忍度
   ```

**解决方案示例**：

```yaml
# 添加匹配的容忍度
aapiVersion: v1
kind: Pod
metadata:
  name: tolerate-node-taint-pod
spec:
  tolerations:
  - key: "node-role.kubernetes.io/control-plane"
    operator: "Exists"
    effect: "NoSchedule"
  containers:
  - name: app-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
```

### 3.4 Pod亲和性/反亲和性导致的调度失败

**症状**：
- Pod状态显示Pending
- 事件信息显示"0/3 nodes are available: 3 node(s) didn't satisfy pod affinity rules."
- 或"0/3 nodes are available: 3 node(s) didn't satisfy pod anti-affinity rules."

**排查步骤**：

1. 查看Pod亲和性配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 30 affinity
   ```

2. 查看集群中现有Pod的标签：
   ```bash
   kubectl get pods -n <namespace> --show-labels
   ```

3. 检查Pod亲和性规则是否有匹配的Pod：
   ```bash
   kubectl get pods -n <namespace> -l <key>=<value>
   ```

**解决方案示例**：

```yaml
# 修复Pod亲和性配置
aapiVersion: v1
kind: Pod
metadata:
  name: fixed-pod-affinity-pod
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - existing-app  # 确保集群中有带有app=existing-app标签的Pod
        topologyKey: kubernetes.io/hostname
  containers:
  - name: app-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
```

### 3.5 节点选择器导致的调度失败

**症状**：
- Pod状态显示Pending
- 事件信息显示"0/3 nodes are available: 3 node(s) didn't match node selector."

**排查步骤**：

1. 查看Pod节点选择器：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 nodeSelector
   ```

2. 查看节点标签：
   ```bash
   kubectl get node --show-labels
   ```

3. 检查是否有匹配的节点：
   ```bash
   kubectl get node -l <key>=<value>
   ```

**解决方案示例**：

```yaml
# 修复节点选择器配置
aapiVersion: v1
kind: Pod
metadata:
  name: fixed-node-selector-pod
spec:
  nodeSelector:
    disktype: ssd  # 确保集群中有带有disktype=ssd标签的节点
  containers:
  - name: app-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
```

### 3.6 调度器配置问题导致的调度失败

**症状**：
- 多个Pod同时调度失败
- 调度器日志显示错误信息
- 调度策略配置错误

**排查步骤**：

1. 查看调度器日志：
   ```bash
   kubectl logs <kube-scheduler-pod> -n kube-system
   ```

2. 查看调度器配置：
   ```bash
   kubectl get configmap kube-scheduler -n kube-system -o yaml
   ```

3. 检查调度器健康状态：
   ```bash
   kubectl get pods -n kube-system | grep kube-scheduler
   ```

**解决方案示例**：

```yaml
# 修复调度器配置（如果需要）
aapiVersion: kubescheduler.config.k8s.io/v1beta2
kind: KubeSchedulerConfiguration
dispatcher:
  leaseDurationSeconds: 15
  leaderElection:
    leaderElect: true
    resourceLock: leases
    resourceName: kube-scheduler
    resourceNamespace: kube-system
schedulerName: default-scheduler
profiles:
- schedulerName: default-scheduler
  plugins:
    score:
      enabled:
      - name: NodeResourcesFit
        weight: 1
      - name: ImageLocality
        weight: 1
      - name: PodTopologySpread
        weight: 2
      - name: NodeAffinity
        weight: 1
      - name: PodAffinity
        weight: 1
  pluginConfig:
  - name: NodeResourcesFit
    args:
      scoringStrategy:
        resources:
        - name: cpu
          weight: 1
        - name: memory
          weight: 1
        type: LeastAllocated
  - name: PodTopologySpread
    args:
      defaultConstraints:
      - maxSkew: 1
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: ScheduleAnyway
      defaultingType: List
```

### 3.7 拓扑约束导致的调度失败

**症状**：
- Pod状态显示Pending
- 事件信息显示"0/3 nodes are available: 3 node(s) didn't match pod topology spread constraints."

**排查步骤**：

1. 查看Pod拓扑约束配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 20 topologySpreadConstraints
   ```

2. 查看集群中现有Pod的分布情况：
   ```bash
   kubectl get pods -n <namespace> -o wide
   ```

3. 检查拓扑约束是否过于严格：
   ```bash
   # 分析当前Pod分布是否符合拓扑约束
   ```

**解决方案示例**：

```yaml
# 调整拓扑约束配置
aapiVersion: v1
kind: Pod
metadata:
  name: relaxed-topology-pod
  labels:
    app: my-app
spec:
  topologySpreadConstraints:
  - maxSkew: 2  # 放宽maxSkew值
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: ScheduleAnyway  # 改为ScheduleAnyway
    labelSelector:
      matchLabels:
        app: my-app
  containers:
  - name: app-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
```

## 4. 实用工具和命令

### 4.1 调度诊断命令

```bash
# 查看Pod详细事件
kubectl describe pod <pod-name> -n <namespace>

# 查看所有Pending状态的Pod
kubectl get pods -n <namespace> --field-selector=status.phase=Pending

# 查看节点资源和可调度性
kubectl describe node <node-name>

# 查看节点污点
kubectl taint nodes <node-name>

# 查看节点亲和性和反亲和性规则
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 30 affinity

# 查看节点选择器
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 nodeSelector

# 查看容忍度
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 15 tolerations

# 查看调度器日志
kubectl logs -l component=kube-scheduler -n kube-system
```

### 4.2 调度分析脚本

```bash
#!/bin/bash
# 调度分析脚本

POD_NAME=$1
NAMESPACE=${2:-default}

# 查看Pod状态
echo "=== Pod状态 ==="
kubectl get pod $POD_NAME -n $NAMESPACE

# 查看Pod事件
echo -e "\n=== Pod事件 ==="
kubectl describe pod $POD_NAME -n $NAMESPACE

# 查看Pod资源请求
echo -e "\n=== Pod资源请求 ==="
kubectl get pod $POD_NAME -n $NAMESPACE -o yaml | grep -A 15 resources

# 查看节点资源情况
echo -e "\n=== 节点资源情况 ==="
kubectl top node

# 查看节点可调度性
echo -e "\n=== 节点可调度性 ==="
kubectl get nodes -o json | jq -r '.items[] | "Node: " + .metadata.name + " Ready: " + (.status.conditions[] | select(.type=="Ready") | .status) + " Schedulable: " + (if .spec.unschedulable then "false" else "true" end)'

# 查看节点污点
echo -e "\n=== 节点污点 ==="
kubectl get nodes -o json | jq -r '.items[] | "Node: " + .metadata.name + " Taints: " + (.spec.taints | tostring)'
```

### 4.3 调度器性能分析

```bash
# 查看调度器性能指标
kubectl get --raw /metrics | grep scheduler_

# 查看调度延迟
kubectl get --raw /metrics | grep scheduler_scheduling_duration_seconds
```

## 5. 故障模拟和练习

### 5.1 模拟资源不足调度失败

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-insufficient-pod
spec:
  containers:
  - name: resource-hungry-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "5"  # 请求5核CPU，超过节点容量
        memory: "10Gi"  # 请求10Gi内存，超过节点容量
```

### 5.2 模拟节点亲和性调度失败

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: node-affinity-failure-pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: nonexistent-label
            operator: In
            values:
            - nonexistent-value  # 集群中没有带有这个标签的节点
  containers:
  - name: app-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
```

### 5.3 模拟污点容忍度调度失败

```yaml
# 首先给节点添加污点
kubectl taint nodes <node-name> key=value:NoSchedule

# 然后创建没有容忍度的Pod
apiVersion: v1
kind: Pod
metadata:
  name: taint-toleration-failure-pod
spec:
  containers:
  - name: app-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
  # 没有添加匹配的容忍度
```

### 5.4 模拟Pod亲和性调度失败

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-affinity-failure-pod
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: nonexistent-app
            operator: In
            values:
            - nonexistent-value  # 集群中没有带有这个标签的Pod
        topologyKey: kubernetes.io/hostname
  containers:
  - name: app-container
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
```

## 6. 最佳实践

1. **合理设置资源请求和限制**：
   - 根据应用实际需求设置resources.requests
   - 避免设置过高的资源请求导致调度困难
   - 避免设置过低的资源请求导致资源争用

2. **使用适当的亲和性规则**：
   - 优先使用软亲和性（preferredDuringSchedulingIgnoredDuringExecution）而非硬亲和性
   - 避免过于复杂的亲和性规则
   - 定期审查和优化亲和性规则

3. **合理使用污点和容忍度**：
   - 只为特殊节点设置污点
   - 避免滥用污点导致大部分Pod无法调度
   - 为需要调度到特殊节点的Pod添加相应的容忍度

4. **优化拓扑约束**：
   - 使用合理的maxSkew值
   - 考虑使用whenUnsatisfiable: ScheduleAnyway而非DoNotSchedule
   - 根据实际需求调整拓扑约束

5. **监控调度器性能**：
   - 定期查看调度器日志
   - 监控调度延迟指标
   - 及时发现和解决调度器问题

6. **使用节点池隔离工作负载**：
   - 为不同类型的工作负载创建专门的节点池
   - 使用标签和污点隔离节点池
   - 简化调度规则，提高调度成功率

7. **定期清理资源**：
   - 及时清理终止状态的Pod
   - 清理未使用的PVC和PV
   - 定期检查和调整资源配额

8. **使用调度器扩展**：
   - 根据需要使用调度器扩展（Scheduler Extenders）
   - 考虑使用自定义调度器（Custom Schedulers）
   - 定期更新调度器配置

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

本案例提供了Kubernetes环境中调度失败问题的排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决各种调度失败问题
- 了解Kubernetes调度器的工作原理
- 掌握调度器配置和优化技巧
- 建立良好的调度策略设计习惯

通过合理的资源配置、亲和性规则设计和调度器优化，您将能够提高Pod调度成功率，优化集群资源使用，提高应用的可用性和性能。