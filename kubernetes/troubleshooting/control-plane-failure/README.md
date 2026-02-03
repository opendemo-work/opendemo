# Kubernetes控制平面故障排查实战

## 1. 案例概述

本案例提供了Kubernetes控制平面故障的排查方法和解决方案，包括：
- API Server故障排查
- etcd故障排查
- Controller Manager故障排查
- Scheduler故障排查
- 控制平面组件间通信问题
- 控制平面高可用性问题
- 证书过期问题

## 2. 环境准备

- Kubernetes集群（v1.20+）
- 控制平面节点访问权限（SSH）
- kubectl命令行工具
- etcdctl命令行工具（用于etcd故障排查）
- 集群证书信息（用于API Server访问）
- 日志查看工具（如journalctl、tail等）

## 3. 常见控制平面故障排查

### 3.1 API Server故障

**症状**：
- kubectl命令超时或失败
- 集群状态不可用
- 控制平面组件无法连接到API Server
- API Server Pod状态异常

**排查步骤**：

1. 检查API Server Pod状态：
   ```bash
   kubectl get pods -n kube-system | grep kube-apiserver
   ```

2. 查看API Server日志：
   ```bash
   # 如果API Server是Pod部署
   kubectl logs <kube-apiserver-pod-name> -n kube-system
   
   # 如果API Server是系统服务
   ssh <control-plane-node> journalctl -u kube-apiserver -f
   ```

3. 检查API Server端口是否可访问：
   ```bash
   # 从控制平面节点本地测试
   curl -k https://localhost:6443/healthz
   
   # 从其他节点测试
   curl -k https://<control-plane-ip>:6443/healthz
   ```

4. 检查API Server配置：
   ```bash
   # 如果是Pod部署，查看Pod配置
   kubectl get pod <kube-apiserver-pod-name> -n kube-system -o yaml
   
   # 如果是系统服务，查看服务配置
   ssh <control-plane-node> cat /etc/kubernetes/manifests/kube-apiserver.yaml
   ```

5. 检查证书状态：
   ```bash
   # 查看API Server证书过期时间
   ssh <control-plane-node> openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout | grep -A 3 Validity
   ```

**解决方案示例**：

```yaml
# 修复API Server证书过期问题（重新生成证书）
# 在控制平面节点执行
kubeadm certs renew all
# 重启API Server
kubectl rollout restart deployment kube-apiserver -n kube-system
```

### 3.2 etcd故障

**症状**：
- API Server无法启动或频繁重启
- 集群数据无法持久化
- etcd Pod状态异常
- 控制平面节点间etcd通信失败

**排查步骤**：

1. 检查etcd Pod状态：
   ```bash
   kubectl get pods -n kube-system | grep etcd
   ```

2. 查看etcd日志：
   ```bash
   # 如果etcd是Pod部署
   kubectl logs <etcd-pod-name> -n kube-system
   
   # 如果etcd是系统服务
   ssh <control-plane-node> journalctl -u etcd -f
   ```

3. 检查etcd集群健康状态：
   ```bash
   # 使用etcdctl检查集群健康
   ETCDCTL_API=3 etcdctl --endpoints=https://<etcd-ip>:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key endpoint health
   
   # 检查etcd集群成员状态
   ETCDCTL_API=3 etcdctl --endpoints=https://<etcd-ip>:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key member list
   ```

4. 检查etcd数据目录：
   ```bash
   ssh <control-plane-node> df -h /var/lib/etcd
   ssh <control-plane-node> ls -la /var/lib/etcd
   ```

5. 检查etcd端口是否可访问：
   ```bash
   # 测试etcd客户端端口
   nc -zv <etcd-ip> 2379
   # 测试etcd集群端口
   nc -zv <etcd-ip> 2380
   ```

**解决方案示例**：

```bash
# 修复etcd数据损坏问题（从备份恢复）
ETCDCTL_API=3 etcdctl --endpoints=https://<etcd-ip>:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot restore /path/to/etcd-backup.db \
  --data-dir=/var/lib/etcd-restore

# 重启etcd服务，使用新的数据目录
# 注意：这将导致集群数据丢失，仅在紧急情况下使用
```

### 3.3 Controller Manager故障

**症状**：
- 资源控制器无法正常工作（如Deployment无法创建Pod）
- 节点状态更新延迟
- 事件无法正常记录
- Controller Manager Pod状态异常

**排查步骤**：

1. 检查Controller Manager Pod状态：
   ```bash
   kubectl get pods -n kube-system | grep kube-controller-manager
   ```

2. 查看Controller Manager日志：
   ```bash
   # 如果是Pod部署
   kubectl logs <kube-controller-manager-pod-name> -n kube-system
   
   # 如果是系统服务
   ssh <control-plane-node> journalctl -u kube-controller-manager -f
   ```

3. 检查Controller Manager配置：
   ```bash
   # 如果是Pod部署
   kubectl get pod <kube-controller-manager-pod-name> -n kube-system -o yaml
   
   # 如果是系统服务
   ssh <control-plane-node> cat /etc/kubernetes/manifests/kube-controller-manager.yaml
   ```

4. 检查Controller Manager是否能连接到API Server：
   ```bash
   # 查看Controller Manager是否注册到API Server
   kubectl get endpoints kube-controller-manager -n kube-system
   ```

**解决方案示例**：

```yaml
# 修复Controller Manager与API Server通信问题（更新证书）
apiVersion: v1
kind: Pod
metadata:
  name: kube-controller-manager
  namespace: kube-system
  annotations:
    scheduler.alpha.kubernetes.io/critical-pod: ""
spec:
  containers:
  - name: kube-controller-manager
    image: k8s.gcr.io/kube-controller-manager:v1.26.0
    command:
    - kube-controller-manager
    - --allocate-node-cidrs=true
    - --authentication-kubeconfig=/etc/kubernetes/controller-manager.conf
    - --authorization-kubeconfig=/etc/kubernetes/controller-manager.conf
    - --bind-address=0.0.0.0
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --cluster-cidr=10.244.0.0/16
    - --cluster-name=kubernetes
    - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
    - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key
    - --controllers=*,bootstrapsigner,tokencleaner
    - --kubeconfig=/etc/kubernetes/controller-manager.conf
    - --leader-elect=true
    - --node-cidr-mask-size=24
    - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
    - --root-ca-file=/etc/kubernetes/pki/ca.crt
    - --service-account-private-key-file=/etc/kubernetes/pki/sa.key
    - --service-cluster-ip-range=10.96.0.0/12
    - --use-service-account-credentials=true
    volumeMounts:
    - mountPath: /etc/ssl/certs
      name: ca-certs
      readOnly: true
    - mountPath: /etc/pki
      name: etc-pki
      readOnly: true
    - mountPath: /etc/kubernetes/pki
      name: k8s-certs
      readOnly: true
    - mountPath: /etc/kubernetes/controller-manager.conf
      name: kubeconfig
      readOnly: true
  hostNetwork: true
  priorityClassName: system-node-critical
  volumes:
  - hostPath:
      path: /etc/ssl/certs
      type: DirectoryOrCreate
    name: ca-certs
  - hostPath:
      path: /etc/pki
      type: DirectoryOrCreate
    name: etc-pki
  - hostPath:
      path: /etc/kubernetes/pki
      type: DirectoryOrCreate
    name: k8s-certs
  - hostPath:
      path: /etc/kubernetes/controller-manager.conf
      type: FileOrCreate
    name: kubeconfig
```

### 3.4 Scheduler故障

**症状**：
- Pod无法调度到节点
- 调度器日志显示错误
- Scheduler Pod状态异常
- 节点上没有新Pod被调度

**排查步骤**：

1. 检查Scheduler Pod状态：
   ```bash
   kubectl get pods -n kube-system | grep kube-scheduler
   ```

2. 查看Scheduler日志：
   ```bash
   # 如果是Pod部署
   kubectl logs <kube-scheduler-pod-name> -n kube-system
   
   # 如果是系统服务
   ssh <control-plane-node> journalctl -u kube-scheduler -f
   ```

3. 检查Scheduler配置：
   ```bash
   # 如果是Pod部署
   kubectl get pod <kube-scheduler-pod-name> -n kube-system -o yaml
   
   # 如果是系统服务
   ssh <control-plane-node> cat /etc/kubernetes/manifests/kube-scheduler.yaml
   ```

4. 检查Scheduler是否能连接到API Server：
   ```bash
   # 查看Scheduler是否注册到API Server
   kubectl get endpoints kube-scheduler -n kube-system
   ```

5. 检查Pending状态的Pod并查看调度事件：
   ```bash
   kubectl describe pod <pending-pod-name> -n <namespace>
   ```

**解决方案示例**：

```yaml
# 修复Scheduler配置问题
apiVersion: v1
kind: Pod
metadata:
  name: kube-scheduler
  namespace: kube-system
  annotations:
    scheduler.alpha.kubernetes.io/critical-pod: ""
spec:
  containers:
  - name: kube-scheduler
    image: k8s.gcr.io/kube-scheduler:v1.26.0
    command:
    - kube-scheduler
    - --authentication-kubeconfig=/etc/kubernetes/scheduler.conf
    - --authorization-kubeconfig=/etc/kubernetes/scheduler.conf
    - --bind-address=0.0.0.0
    - --kubeconfig=/etc/kubernetes/scheduler.conf
    - --leader-elect=true
    volumeMounts:
    - mountPath: /etc/kubernetes/scheduler.conf
      name: kubeconfig
      readOnly: true
    - mountPath: /etc/kubernetes/pki
      name: k8s-certs
      readOnly: true
  hostNetwork: true
  priorityClassName: system-node-critical
  volumes:
  - hostPath:
      path: /etc/kubernetes/scheduler.conf
      type: FileOrCreate
    name: kubeconfig
  - hostPath:
      path: /etc/kubernetes/pki
      type: DirectoryOrCreate
    name: k8s-certs
```

### 3.5 控制平面组件间通信问题

**症状**：
- 控制平面组件无法相互通信
- API Server无法连接到etcd
- Controller Manager和Scheduler无法连接到API Server
- 组件日志显示连接超时或拒绝

**排查步骤**：

1. 检查组件间网络连接：
   ```bash
   # 从控制平面节点测试etcd连接
   curl -k https://localhost:2379/health
   
   # 测试API Server连接
   curl -k https://localhost:6443/healthz
   ```

2. 检查组件证书是否匹配：
   ```bash
   # 检查API Server和etcd证书是否兼容
   ssh <control-plane-node> openssl x509 -in /etc/kubernetes/pki/apiserver-etcd-client.crt -text -noout
   ssh <control-plane-node> openssl x509 -in /etc/kubernetes/pki/etcd/server.crt -text -noout
   ```

3. 检查防火墙规则：
   ```bash
   # 检查控制平面节点防火墙规则
   ssh <control-plane-node> iptables -L -n
   ssh <control-plane-node> ufw status
   ```

4. 检查网络插件状态：
   ```bash
   kubectl get pods -n kube-system | grep -E "calico|flannel|cilium|weave"
   ```

**解决方案示例**：

```bash
# 修复控制平面组件间通信问题（开放必要端口）
# 在控制平面节点执行
ufw allow 6443/tcp  # API Server
ufw allow 2379/tcp  # etcd client
ufw allow 2380/tcp  # etcd peer
ufw allow 10250/tcp # Kubelet API
ufw allow 10251/tcp # Scheduler
ufw allow 10252/tcp # Controller Manager
```

### 3.6 控制平面高可用性问题

**症状**：
- 控制平面节点故障导致整个集群不可用
- 组件选举失败
- 脑裂问题
- 组件状态不一致

**排查步骤**：

1. 检查控制平面节点状态：
   ```bash
   kubectl get nodes -l node-role.kubernetes.io/control-plane
   ```

2. 检查etcd集群状态：
   ```bash
   ETCDCTL_API=3 etcdctl --endpoints=https://<etcd-ip1>:2379,https://<etcd-ip2>:2379,https://<etcd-ip3>:2379 \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/server.crt \
     --key=/etc/kubernetes/pki/etcd/server.key \
     endpoint health
   ```

3. 检查组件领导者选举状态：
   ```bash
   # 检查Controller Manager领导者
   kubectl get leases kube-controller-manager -n kube-system -o yaml
   
   # 检查Scheduler领导者
   kubectl get leases kube-scheduler -n kube-system -o yaml
   ```

4. 检查控制平面组件部署模式：
   ```bash
   kubectl get deployments -n kube-system | grep -E "apiserver|controller-manager|scheduler"
   ```

**解决方案示例**：

```bash
# 修复etcd集群脑裂问题（重新配置etcd集群）
# 在所有etcd节点停止etcd服务
ssh <etcd-node> systemctl stop etcd

# 在主节点初始化etcd集群
ETCDCTL_API=3 etcdctl --name etcd1 \
  --initial-advertise-peer-urls https://<etcd1-ip>:2380 \
  --listen-peer-urls https://<etcd1-ip>:2380 \
  --listen-client-urls https://<etcd1-ip>:2379,https://localhost:2379 \
  --advertise-client-urls https://<etcd1-ip>:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster etcd1=https://<etcd1-ip>:2380,etcd2=https://<etcd2-ip>:2380,etcd3=https://<etcd3-ip>:2380 \
  --initial-cluster-state new \
  --cert-file=/etc/kubernetes/pki/etcd/server.crt \
  --key-file=/etc/kubernetes/pki/etcd/server.key \
  --client-cert-auth \
  --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt \
  --peer-cert-file=/etc/kubernetes/pki/etcd/server.crt \
  --peer-key-file=/etc/kubernetes/pki/etcd/server.key \
  --peer-client-cert-auth \
  --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt

# 在其他节点加入集群
# ...
```

### 3.7 证书过期问题

**症状**：
- kubectl命令失败，显示证书过期
- 组件日志显示证书验证失败
- 集群无法正常运行
- 证书有效期已过

**排查步骤**：

1. 检查集群证书状态：
   ```bash
   # 查看所有证书的过期时间
   kubeadm certs check-expiration
   
   # 或手动检查
   for cert in /etc/kubernetes/pki/*.crt; do
     echo "=== $cert ==="
     openssl x509 -in $cert -text -noout | grep -A 3 Validity
   done
   ```

2. 查看组件日志中的证书错误：
   ```bash
   kubectl logs <component-pod-name> -n kube-system | grep -i cert
   ```

3. 检查kubeconfig文件中的证书：
   ```bash
   openssl x509 -in <(kubectl config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d) -text -noout | grep -A 3 Validity
   ```

**解决方案示例**：

```bash
# 重新生成所有证书
kubeadm certs renew all

# 重新生成kubeconfig文件
kubeadm kubeconfig user --client-name=admin > /etc/kubernetes/admin.conf
kubeadm kubeconfig user --client-name=kube-controller-manager > /etc/kubernetes/controller-manager.conf
kubeadm kubeconfig user --client-name=kube-scheduler > /etc/kubernetes/scheduler.conf

# 重启所有控制平面组件
kubectl rollout restart deployment -n kube-system kube-apiserver kube-controller-manager kube-scheduler
kubectl delete pod -n kube-system -l component=etcd

# 更新本地kubeconfig
cp /etc/kubernetes/admin.conf $HOME/.kube/config
```

## 4. 实用工具和命令

### 4.1 控制平面诊断命令

```bash
# 检查控制平面组件状态
kubectl get pods -n kube-system | grep -E "apiserver|etcd|controller-manager|scheduler"

# 查看组件日志
kubectl logs -l component=kube-apiserver -n kube-system
kubectl logs -l component=etcd -n kube-system
kubectl logs -l component=kube-controller-manager -n kube-system
kubectl logs -l component=kube-scheduler -n kube-system

# 检查API Server健康状态
curl -k https://<apiserver-ip>:6443/healthz
curl -k https://<apiserver-ip>:6443/livez
curl -k https://<apiserver-ip>:6443/readyz

# 检查etcd集群状态
ETCDCTL_API=3 etcdctl --endpoints=https://<etcd-ip>:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint status --write-out=table

# 检查证书状态
kubeadm certs check-expiration

# 查看组件领导者状态
kubectl get leases -n kube-system
```

### 4.2 控制平面分析脚本

```bash
#!/bin/bash
# 控制平面分析脚本

# 检查控制平面组件状态
echo "=== 控制平面组件状态 ==="
kubectl get pods -n kube-system | grep -E "apiserver|etcd|controller-manager|scheduler"

# 检查API Server健康状态
echo -e "\n=== API Server健康状态 ==="
curl -k https://localhost:6443/healthz
curl -k https://localhost:6443/livez
curl -k https://localhost:6443/readyz

# 检查etcd状态
echo -e "\n=== etcd状态 ==="
kubectl get pods -n kube-system | grep etcd

# 检查证书状态
echo -e "\n=== 证书状态 ==="
kubeadm certs check-expiration

# 检查组件日志错误
echo -e "\n=== 组件日志错误 ==="
echo "API Server错误："
kubectl logs -l component=kube-apiserver -n kube-system --tail=20 | grep -i error

echo -e "\netcd错误："
kubectl logs -l component=etcd -n kube-system --tail=20 | grep -i error

echo -e "\nController Manager错误："
kubectl logs -l component=kube-controller-manager -n kube-system --tail=20 | grep -i error

echo -e "\nScheduler错误："
kubectl logs -l component=kube-scheduler -n kube-system --tail=20 | grep -i error
```

### 4.3 应急恢复工具

```bash
# 备份etcd数据
ETCDCTL_API=3 etcdctl --endpoints=https://<etcd-ip>:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /backup/etcd-snapshot-$(date +%Y%m%d-%H%M%S).db

# 恢复etcd数据
ETCDCTL_API=3 etcdctl --endpoints=https://<etcd-ip>:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot restore /backup/etcd-snapshot.db \
  --data-dir=/var/lib/etcd-restore

# 重新初始化控制平面
kubeadm init phase control-plane all

# 检查集群状态
kubeadm upgrade diff
```

## 5. 故障模拟和练习

### 5.1 模拟API Server证书过期

```bash
# 注意：这会破坏集群，请在测试环境执行
# 修改API Server证书的过期时间（使用openssl）
# 1. 备份原始证书
cp /etc/kubernetes/pki/apiserver.crt /etc/kubernetes/pki/apiserver.crt.bak
cp /etc/kubernetes/pki/apiserver.key /etc/kubernetes/pki/apiserver.key.bak

# 2. 生成一个过期的证书
openssl req -x509 -newkey rsa:4096 -keyout /etc/kubernetes/pki/apiserver.key -out /etc/kubernetes/pki/apiserver.crt -days 1 -nodes -subj "/CN=kube-apiserver"

# 3. 重启API Server
kubectl delete pod -n kube-system -l component=kube-apiserver

# 4. 测试kubectl命令
kubectl get pods
```

### 5.2 模拟etcd故障

```bash
# 注意：这会破坏集群，请在测试环境执行
# 停止etcd服务
ssh <control-plane-node> systemctl stop etcd

# 或删除etcd数据目录
ssh <control-plane-node> rm -rf /var/lib/etcd/member

# 测试kubectl命令
kubectl get pods
```

## 6. 最佳实践

1. **定期备份etcd数据**：
   - 建立定期备份策略（如每小时备份一次）
   - 测试备份恢复流程
   - 将备份存储在安全的位置

2. **监控控制平面组件**：
   - 监控组件健康状态和性能指标
   - 设置告警规则
   - 定期检查日志

3. **实施高可用性**：
   - 部署至少3个控制平面节点
   - 确保etcd集群有奇数个节点
   - 使用负载均衡器访问API Server

4. **定期更新证书**：
   - 监控证书过期时间
   - 建立证书更新流程
   - 在证书过期前及时更新

5. **保持组件版本一致**：
   - 确保所有控制平面组件版本相同
   - 按照官方升级流程进行版本升级
   - 升级前备份数据

6. **限制访问权限**：
   - 限制控制平面节点的访问
   - 使用RBAC限制API Server访问
   - 保护证书和密钥文件

7. **文档化配置**：
   - 记录控制平面配置
   - 文档化应急恢复流程
   - 保存组件版本信息

8. **定期演练故障恢复**：
   - 定期进行故障模拟演练
   - 测试恢复流程
   - 优化恢复时间

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

本案例提供了Kubernetes控制平面故障的全面排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决控制平面组件故障
- 了解控制平面组件间的通信机制
- 掌握证书管理和更新方法
- 建立高可用性控制平面
- 实施有效的监控和备份策略
- 优化故障恢复流程

通过合理的设计、监控和维护，您将能够确保Kubernetes控制平面的高可用性和稳定性，提高集群的整体可靠性。