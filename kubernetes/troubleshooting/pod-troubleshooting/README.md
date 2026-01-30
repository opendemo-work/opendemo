# Kubernetes Pod故障排查实战

## 1. 案例概述

本案例提供了Kubernetes环境中常见Pod故障的排查方法和解决方案，包括：
- CrashLoopBackOff
- ImagePullBackOff/ErrImagePull
- RunContainerError
- OOMKilled
- Pending状态
- ContainerCreating状态

## 2. 环境准备

- Kubernetes集群（v1.20+）
- kubectl命令行工具
- Docker命令行工具（可选，用于镜像问题排查）

## 3. 常见Pod故障排查

### 3.1 CrashLoopBackOff

**症状**：Pod反复启动后立即崩溃，状态显示CrashLoopBackOff

**排查步骤**：

1. 查看Pod基本信息：
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. 查看容器日志：
   ```bash
   kubectl logs <pod-name> -n <namespace>
   kubectl logs <pod-name> -n <namespace> --previous  # 查看上一次崩溃的日志
   ```

3. 检查容器健康探针：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 20 readinessProbe
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 20 livenessProbe
   ```

4. 进入容器检查（如果能启动足够长时间）：
   ```bash
   kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
   ```

**解决方案示例**：

```yaml
# 修复健康探针配置错误
apiVersion: v1
kind: Pod
metadata:
  name: fix-crashloopbackoff
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5  # 增加初始延迟时间
      periodSeconds: 10
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 10  # 增加初始延迟时间
      periodSeconds: 15
```

### 3.2 ImagePullBackOff/ErrImagePull

**症状**：Pod无法拉取镜像，状态显示ImagePullBackOff或ErrImagePull

**排查步骤**：

1. 查看Pod事件：
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. 验证镜像名称和标签：
   ```bash
   docker pull <image-name>:<tag>  # 本地验证镜像是否存在
   ```

3. 检查镜像仓库认证：
   ```bash
   kubectl get secret -n <namespace>  # 查看是否有镜像拉取密钥
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 imagePullSecrets
   ```

4. 检查网络连接：
   ```bash
   kubectl exec -it <healthy-pod> -n <namespace> -- ping -c 3 docker.io
   ```

**解决方案示例**：

```yaml
# 使用正确的镜像名称和标签
aapiVersion: v1
kind: Pod
metadata:
  name: fix-imagepullbackoff
spec:
  containers:
  - name: nginx
    image: nginx:1.21  # 使用正确的镜像标签
    ports:
    - containerPort: 80
  imagePullSecrets:
  - name: regcred  # 添加镜像拉取密钥（如果需要）
```

### 3.3 RunContainerError

**症状**：容器运行时错误，状态显示RunContainerError

**排查步骤**：

1. 查看详细错误信息：
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. 检查容器配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml
   ```

3. 检查权限问题：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 securityContext
   ```

4. 检查挂载卷配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 volumeMounts
   ```

**解决方案示例**：

```yaml
# 修复挂载卷配置错误
apiVersion: v1
kind: Pod
metadata:
  name: fix-runcontainererror
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    volumeMounts:
    - name: html-volume
      mountPath: /usr/share/nginx/html  # 使用正确的挂载路径
  volumes:
  - name: html-volume
    configMap:
      name: nginx-html-config  # 确保ConfigMap存在
```

### 3.4 OOMKilled

**症状**：容器因内存不足被杀死，状态显示OOMKilled

**排查步骤**：

1. 查看Pod事件和资源使用情况：
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   kubectl top pod <pod-name> -n <namespace>
   ```

2. 检查资源限制配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 resources
   ```

3. 分析应用内存使用：
   ```bash
   kubectl exec -it <pod-name> -n <namespace> -- ps aux
   ```

**解决方案示例**：

```yaml
# 调整资源限制
aapiVersion: v1
kind: Pod
metadata:
  name: fix-oomkilled
spec:
  containers:
  - name: memory-hungry-app
    image: your-app-image:latest
    ports:
    - containerPort: 8080
    resources:
      requests:
        memory: "512Mi"
        cpu: "500m"
      limits:
        memory: "1Gi"  # 增加内存限制
        cpu: "1"      # 增加CPU限制
```

### 3.5 Pending状态

**症状**：Pod长时间处于Pending状态，无法调度

**排查步骤**：

1. 查看调度事件：
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. 检查节点资源：
   ```bash
   kubectl top nodes
   kubectl describe node <node-name>
   ```

3. 检查Pod调度约束：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 nodeSelector
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 affinity
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 tolerations
   ```

**解决方案示例**：

```yaml
# 修复节点选择器配置
aapiVersion: v1
kind: Pod
metadata:
  name: fix-pending
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
  nodeSelector:
    disktype: ssd  # 确保集群中有匹配的节点标签
  tolerations:
  - key: "node-role.kubernetes.io/control-plane"
    operator: "Exists"
    effect: "NoSchedule"  # 添加容忍度（如果需要调度到控制平面节点）
```

### 3.6 ContainerCreating状态

**症状**：Pod长时间处于ContainerCreating状态

**排查步骤**：

1. 查看详细事件：
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. 检查网络插件：
   ```bash
   kubectl get pods -n kube-system | grep -E "calico|flannel|cilium"
   ```

3. 检查存储配置：
   ```bash
   kubectl get pv
   kubectl get pvc -n <namespace>
   ```

4. 检查CNI配置：
   ```bash
   kubectl get configmap -n kube-system | grep cni
   ```

**解决方案示例**：

```yaml
# 修复存储配置错误
aapiVersion: v1
kind: Pod
metadata:
  name: fix-containercreating
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    volumeMounts:
    - name: data-volume
      mountPath: /data
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: existing-pvc  # 使用已存在的PVC
```

## 4. 实用工具和命令

### 4.1 常用kubectl命令

```bash
# 查看所有命名空间的Pod状态
kubectl get pods --all-namespaces

# 按状态过滤Pod
kubectl get pods -n <namespace> | grep CrashLoopBackOff

# 查看Pod的YAML配置
kubectl get pod <pod-name> -n <namespace> -o yaml

# 查看Pod的JSON配置（便于机器处理）
kubectl get pod <pod-name> -n <namespace> -o json

# 监控Pod状态变化
watch kubectl get pods -n <namespace>
```

### 4.2 高级排查工具

- **kubelet日志**：
  ```bash
  journalctl -u kubelet -f  # 在节点上查看kubelet日志
  ```

- **crictl**：
  ```bash
  crictl ps  # 查看容器状态
  crictl logs <container-id>  # 查看容器日志
  crictl inspect <container-id>  # 查看容器详细信息
  ```

## 5. 故障模拟和练习

### 5.1 模拟CrashLoopBackOff

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: crashloopbackoff-demo
spec:
  containers:
  - name: crash-container
    image: busybox
    command: ["/bin/sh", "-c", "echo 'Starting...'; sleep 1; exit 1"]  # 容器启动后立即退出
    ports:
    - containerPort: 80
```

### 5.2 模拟ImagePullBackOff

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: imagepullbackoff-demo
spec:
  containers:
  - name: invalid-image
    image: invalid-image-name:invalid-tag  # 不存在的镜像
    ports:
    - containerPort: 80
```

### 5.3 模拟OOMKilled

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: oomkilled-demo
spec:
  containers:
  - name: memory-hog
    image: busybox
    command: ["/bin/sh", "-c", "while true; do echo 'Allocating memory...'; dd if=/dev/zero of=/dev/shm/test bs=1M count=1000; done"]
    resources:
      limits:
        memory: "256Mi"  # 限制内存为256Mi，导致OOM
    ports:
    - containerPort: 80
```

## 6. 最佳实践

1. **配置健康探针**：为所有Pod配置适当的readinessProbe和livenessProbe
2. **合理设置资源限制**：根据应用实际需求设置resources.requests和resources.limits
3. **使用镜像标签**：避免使用latest标签，使用具体版本标签
4. **监控和告警**：设置Pod状态监控和告警
5. **定期备份**：定期备份重要应用数据
6. **文档化**：记录应用的正常运行状态和常见故障处理方法

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

本案例提供了Kubernetes环境中常见Pod故障的排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决Pod故障
- 了解Kubernetes Pod的生命周期和常见问题
- 掌握kubectl和其他工具的使用技巧
- 建立良好的故障排查习惯

通过不断实践和总结，您将能够更高效地管理和维护Kubernetes集群中的Pod资源。