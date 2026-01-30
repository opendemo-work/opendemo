# Kubernetes节点故障排查实战

## 1. 案例概述

本案例提供了Kubernetes节点故障的排查方法和解决方案，包括：
- 节点状态异常（NotReady、Unknown）
- Kubelet故障
- 节点资源不足
- 节点网络问题
- 节点磁盘问题
- 节点压力问题（MemoryPressure、DiskPressure、PIDPressure）
- 节点组件故障

## 2. 环境准备

- Kubernetes集群（v1.20+）
- 节点访问权限（SSH）
- kubectl命令行工具
- 系统管理工具（如systemctl、journalctl、df、free等）
- 网络测试工具（如ping、nc、ip等）

## 3. 常见节点故障排查

### 3.1 节点状态异常（NotReady/Unknown）

**症状**：
- kubectl get nodes显示节点状态为NotReady或Unknown
- Pod无法调度到该节点
- 节点上的现有Pod可能无法正常运行

**排查步骤**：

1. 查看节点详细信息：
   ```bash
   kubectl describe node <node-name>
   ```

2. 检查节点条件：
   ```bash
   kubectl get node <node-name> -o jsonpath='{.status.conditions}' | jq
   ```

3. 检查Kubelet状态：
   ```bash
   ssh <node-name> systemctl status kubelet
   ```

4. 查看Kubelet日志：
   ```bash
   ssh <node-name> journalctl -u kubelet -f
   ```

5. 检查节点网络连接：
   ```bash
   ping <node-ip>
   ssh <node-name> ping <control-plane-ip>
   ```

**解决方案示例**：

```bash
# 重启Kubelet服务
ssh <node-name> systemctl restart kubelet

# 检查并修复节点网络问题
ssh <node-name> ip a
ssh <node-name> ip route
ssh <node-name> systemctl restart networking
```

### 3.2 Kubelet故障

**症状**：
- Kubelet服务停止或崩溃
- 节点状态NotReady
- 无法在节点上运行Pod
- Kubelet日志显示错误

**排查步骤**：

1. 检查Kubelet服务状态：
   ```bash
   ssh <node-name> systemctl status kubelet
   ```

2. 查看Kubelet日志：
   ```bash
   ssh <node-name> journalctl -u kubelet --no-pager
   ```

3. 检查Kubelet配置：
   ```bash
   ssh <node-name> cat /etc/kubernetes/kubelet.conf
   ssh <node-name> cat /var/lib/kubelet/config.yaml
   ```

4. 检查Kubelet证书：
   ```bash
   ssh <node-name> openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem -text -noout | grep -A 3 Validity
   ```

5. 检查Kubelet端口：
   ```bash
   ssh <node-name> netstat -tuln | grep 10250
   ```

**解决方案示例**：

```bash
# 修复Kubelet配置错误
ssh <node-name> vi /var/lib/kubelet/config.yaml
ssh <node-name> systemctl restart kubelet

# 重新生成Kubelet证书
kubeadm alpha certs renew kubelet-client
ssh <node-name> systemctl restart kubelet

# 重置Kubelet状态
ssh <node-name> systemctl stop kubelet
ssh <node-name> rm -rf /var/lib/kubelet/*
ssh <node-name> systemctl start kubelet
```

### 3.3 节点资源不足

**症状**：
- 节点CPU或内存使用率接近100%
- Pod被驱逐（Evicted）
- 新Pod无法调度到节点
- 节点状态显示MemoryPressure或DiskPressure

**排查步骤**：

1. 查看节点资源使用情况：
   ```bash
   kubectl top node <node-name>
   ssh <node-name> top
   ```

2. 查看节点条件：
   ```bash
   kubectl describe node <node-name> | grep -A 20 Conditions
   ```

3. 查看节点上运行的Pod及其资源使用情况：
   ```bash
   kubectl get pods -o wide -A | grep <node-name>
   kubectl top pod -A --sort-by=cpu | grep <node-name>
   kubectl top pod -A --sort-by=memory | grep <node-name>
   ```

4. 检查节点磁盘使用情况：
   ```bash
   ssh <node-name> df -h
   ```

**解决方案示例**：

```bash
# 驱逐占用资源过多的Pod
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# 增加节点资源（如果是云环境）
# 或添加新节点到集群

# 清理节点上的临时文件和日志
ssh <node-name> find /var/log -name "*.log" -type f -delete
ssh <node-name> docker system prune -f
```

### 3.4 节点网络问题

**症状**：
- 节点无法与控制平面通信
- 节点间无法通信
- Pod无法通过网络访问
- CNI插件故障

**排查步骤**：

1. 检查节点网络连接：
   ```bash
   # 测试节点到控制平面的连接
   ssh <node-name> ping <control-plane-ip>
   ssh <node-name> curl -k https://<control-plane-ip>:6443/healthz
   
   # 测试节点间通信
   ssh <node1-name> ping <node2-ip>
   
   # 测试CNI插件状态
   ssh <node-name> systemctl status <cni-plugin-service>
   ```

2. 检查节点网络配置：
   ```bash
   ssh <node-name> ip a
   ssh <node-name> ip route
   ```

3. 检查CNI插件日志：
   ```bash
   # Calico
   ssh <node-name> journalctl -u calico-node -f
   
   # Flannel
   ssh <node-name> journalctl -u flanneld -f
   
   # Cilium
   ssh <node-name> cilium status
   ```

4. 检查节点上的Pod网络：
   ```bash
   ssh <node-name> crictl pods
   ssh <node-name> crictl inspect <pod-id> | grep -A 10 "Network"
   ```

**解决方案示例**：

```bash
# 重启CNI插件
ssh <node-name> systemctl restart calico-node

# 检查并修复节点网络配置
ssh <node-name> ifconfig eth0 up
ssh <node-name> ip route add default via <gateway-ip>

# 重置节点网络
kubeadm reset network
```

### 3.5 节点磁盘问题

**症状**：
- 节点状态显示DiskPressure
- Pod无法写入数据到磁盘
- 容器日志无法写入
- 节点上的磁盘使用率过高

**排查步骤**：

1. 检查节点磁盘使用情况：
   ```bash
   ssh <node-name> df -h
   ```

2. 检查节点磁盘inode使用情况：
   ```bash
   ssh <node-name> df -i
   ```

3. 找出占用磁盘空间最多的文件和目录：
   ```bash
   ssh <node-name> du -h --max-depth=1 / | sort -hr | head -10
   ssh <node-name> find /var/lib/docker -type f -size +100M | head -10
   ```

4. 检查节点条件：
   ```bash
   kubectl describe node <node-name> | grep -A 10 "DiskPressure"
   ```

**解决方案示例**：

```bash
# 清理Docker镜像和容器
ssh <node-name> docker system prune -f

# 清理旧的容器日志
ssh <node-name> find /var/log/containers -name "*.log" -type f -mtime +7 -delete

# 扩展节点磁盘空间（如果是云环境）
# 或添加新磁盘并挂载到适当的目录
```

### 3.6 节点压力问题

**症状**：
- 节点条件显示MemoryPressure、DiskPressure或PIDPressure
- Pod被驱逐
- 新Pod无法调度到节点
- 节点性能下降

**排查步骤**：

1. 查看节点条件：
   ```bash
   kubectl describe node <node-name> | grep -A 20 Conditions
   ```

2. 检查内存使用情况：
   ```bash
   ssh <node-name> free -h
   ssh <node-name> top -b -n 1 | head -20
   ```

3. 检查磁盘使用情况：
   ```bash
   ssh <node-name> df -h
   ```

4. 检查PID使用情况：
   ```bash
   ssh <node-name> ps aux --no-heading | wc -l
   ssh <node-name> cat /proc/sys/kernel/pid_max
   ```

**解决方案示例**：

```bash
# 处理MemoryPressure
ssh <node-name> systemctl stop non-essential-services
ssh <node-name> echo 1 > /proc/sys/vm/drop_caches

# 处理DiskPressure
ssh <node-name> docker system prune -f
ssh <node-name> journalctl --vacuum-time=7d

# 处理PIDPressure
ssh <node-name> pkill -f <unnecessary-process>
ssh <node-name> echo 4194304 > /proc/sys/kernel/pid_max
```

### 3.7 节点组件故障

**症状**：
- 节点上的kube-proxy、容器运行时等组件故障
- Pod网络连接问题
- 容器无法启动

**排查步骤**：

1. 检查kube-proxy状态：
   ```bash
   kubectl get pods -n kube-system | grep kube-proxy
   kubectl logs <kube-proxy-pod-name> -n kube-system
   ```

2. 检查容器运行时状态：
   ```bash
   ssh <node-name> systemctl status docker
   ssh <node-name> docker info
   
   # 或
   ssh <node-name> systemctl status containerd
   ssh <node-name> ctr version
   ```

3. 检查容器运行时日志：
   ```bash
   ssh <node-name> journalctl -u docker -f
   
   # 或
   ssh <node-name> journalctl -u containerd -f
   ```

**解决方案示例**：

```bash
# 重启kube-proxy
kubectl delete pod -n kube-system -l k8s-app=kube-proxy

# 重启容器运行时
ssh <node-name> systemctl restart docker
# 或
ssh <node-name> systemctl restart containerd

# 修复容器运行时配置
ssh <node-name> vi /etc/docker/daemon.json
ssh <node-name> systemctl restart docker
```

## 4. 实用工具和命令

### 4.1 节点诊断命令

```bash
# 查看所有节点状态
kubectl get nodes

# 查看节点详细信息
kubectl describe node <node-name>

# 查看节点资源使用情况
kubectl top node <node-name>

# 查看节点条件
kubectl get node <node-name> -o jsonpath='{.status.conditions}' | jq

# 查看节点上运行的Pod
kubectl get pods -o wide -A | grep <node-name>

# 查看节点上Pod的资源使用情况
kubectl top pod -A --sort-by=cpu | grep <node-name>
kubectl top pod -A --sort-by=memory | grep <node-name>

# 查看Kubelet状态
ssh <node-name> systemctl status kubelet

# 查看Kubelet日志
ssh <node-name> journalctl -u kubelet -f

# 检查节点网络
ssh <node-name> ip a
ssh <node-name> ip route
ssh <node-name> ping <control-plane-ip>

# 检查节点资源
ssh <node-name> df -h
ssh <node-name> free -h
ssh <node-name> top -b -n 1

# 检查容器运行时
ssh <node-name> docker info
ssh <node-name> ctr version
```

### 4.2 节点分析脚本

```bash
#!/bin/bash
# 节点分析脚本

NODE_NAME=$1

# 检查节点基本信息
echo "=== 节点基本信息 ==="
kubectl get node $NODE_NAME

# 检查节点详细信息
echo -e "\n=== 节点详细信息 ==="
kubectl describe node $NODE_NAME

# 检查节点条件
echo -e "\n=== 节点条件 ==="
kubectl get node $NODE_NAME -o jsonpath='{.status.conditions}' | jq

# 检查节点资源使用情况
echo -e "\n=== 节点资源使用情况 ==="
kubectl top node $NODE_NAME

# 检查节点上运行的Pod
echo -e "\n=== 节点上运行的Pod ==="
kubectl get pods -o wide -A | grep $NODE_NAME

# 检查节点组件状态
echo -e "\n=== 节点组件状态 ==="
kubectl get pods -n kube-system | grep $NODE_NAME

# 检查Kubelet状态
echo -e "\n=== Kubelet状态 ==="
ssh $NODE_NAME systemctl status kubelet --no-pager

# 检查容器运行时状态
echo -e "\n=== 容器运行时状态 ==="
ssh $NODE_NAME docker info 2>/dev/null || ssh $NODE_NAME ctr version

# 检查节点网络
echo -e "\n=== 节点网络 ==="
ssh $NODE_NAME ip a | grep -A 5 eth0
ssh $NODE_NAME ip route

# 检查节点磁盘
echo -e "\n=== 节点磁盘 ==="
ssh $NODE_NAME df -h

# 检查节点内存
echo -e "\n=== 节点内存 ==="
ssh $NODE_NAME free -h
```

### 4.3 节点修复工具

```bash
# 重启Kubelet
systemctl restart kubelet

# 重启容器运行时
systemctl restart docker
systemctl restart containerd

# 重启网络服务
systemctl restart networking

# 清理Docker资源
docker system prune -f
docker volume prune -f

# 重置Kubelet状态
kubeadm reset node
```

## 5. 故障模拟和练习

### 5.1 模拟节点NotReady状态

```bash
# 注意：这会影响集群，请在测试环境执行
# 停止Kubelet服务
ssh <node-name> systemctl stop kubelet

# 或停止CNI插件
ssh <node-name> systemctl stop calico-node

# 查看节点状态变化
watch kubectl get nodes
```

### 5.2 模拟节点资源不足

```bash
# 注意：这会影响节点性能，请在测试环境执行
# 创建内存密集型Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: memory-hog
spec:
  containers:
  - name: memory-hog
    image: polinux/stress:latest
    command: ["stress", "--vm", "4", "--vm-bytes", "80%", "--timeout", "300"]
EOF

# 查看节点状态
watch kubectl describe node <node-name>
```

### 5.3 模拟节点磁盘压力

```bash
# 注意：这会占用节点磁盘空间，请在测试环境执行
# 创建大文件
ssh <node-name> dd if=/dev/zero of=/large-file bs=1G count=10

# 查看节点状态
watch kubectl describe node <node-name>

# 清理
ssh <node-name> rm /large-file
```

## 6. 最佳实践

1. **监控节点健康状态**：
   - 实施节点监控，包括CPU、内存、磁盘、网络等指标
   - 设置告警规则，及时发现节点异常
   - 定期检查节点状态和条件

2. **合理分配资源**：
   - 为节点设置适当的资源预留
   - 为Pod设置合理的资源请求和限制
   - 避免单个Pod占用过多节点资源

3. **实施节点自动扩缩容**：
   - 使用Cluster Autoscaler根据资源需求自动添加或删除节点
   - 配置合适的扩缩容策略

4. **定期清理节点资源**：
   - 定期清理未使用的Docker镜像和容器
   - 定期清理旧的容器日志
   - 监控和清理临时文件

5. **确保节点高可用性**：
   - 部署足够数量的节点以保证高可用性
   - 实施节点故障转移机制
   - 定期测试节点故障恢复流程

6. **保持节点组件版本一致**：
   - 确保所有节点上的Kubelet、容器运行时等组件版本一致
   - 按照官方升级流程升级节点组件

7. **实施节点隔离策略**：
   - 使用节点标签和污点隔离不同类型的工作负载
   - 为关键应用预留专用节点

8. **定期备份节点配置**：
   - 定期备份节点配置文件
   - 记录节点硬件和软件配置
   - 建立节点恢复流程

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

本案例提供了Kubernetes节点故障的全面排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决各种节点故障
- 了解节点组件的工作原理和常见问题
- 掌握节点资源管理和优化技巧
- 建立节点监控和维护策略
- 提高集群的整体可靠性和可用性

通过合理的节点管理、监控和维护，您将能够确保Kubernetes集群中的节点始终处于健康状态，为应用提供稳定可靠的运行环境。