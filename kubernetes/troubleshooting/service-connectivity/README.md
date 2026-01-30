# Kubernetes服务连通性问题排查实战

## 1. 案例概述

本案例提供了Kubernetes环境中服务连通性问题的排查方法和解决方案，包括：
- 服务DNS解析问题
- 服务端口配置问题
- 服务选择器匹配问题
- 服务类型相关问题（ClusterIP、NodePort、LoadBalancer）
- 网络策略问题
- 跨命名空间访问问题
- 服务代理问题

## 2. 环境准备

- Kubernetes集群（v1.20+）
- kubectl命令行工具
- 网络测试工具（如curl、nslookup、telnet）

## 3. 常见服务连通性问题排查

### 3.1 服务DNS解析问题

**症状**：Pod无法通过服务名称解析到服务IP

**排查步骤**：

1. 检查CoreDNS运行状态：
   ```bash
   kubectl get pods -n kube-system | grep coredns
   kubectl logs <coredns-pod-name> -n kube-system
   ```

2. 在Pod内部测试DNS解析：
   ```bash
   kubectl run -it --rm dns-test --image=busybox:1.35 -- /bin/sh
   nslookup <service-name>.<namespace>.svc.cluster.local
   nslookup kubernetes.default.svc.cluster.local
   ```

3. 检查服务是否存在：
   ```bash
   kubectl get svc -n <namespace>
   ```

4. 检查DNS配置：
   ```bash
   kubectl get configmap coredns -n kube-system -o yaml
   ```

**解决方案示例**：

```yaml
# 修复CoreDNS配置错误（如果需要）
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

### 3.2 服务端口配置问题

**症状**：服务IP可访问，但特定端口无法连接

**排查步骤**：

1. 检查服务端口配置：
   ```bash
   kubectl get svc <service-name> -n <namespace> -o yaml
   ```

2. 检查后端Pod端口配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 containerPort
   ```

3. 测试端口连通性：
   ```bash
   kubectl run -it --rm port-test --image=busybox:1.35 -- /bin/sh
   telnet <service-ip> <service-port>
   curl http://<service-ip>:<service-port>
   ```

4. 检查服务端点：
   ```bash
   kubectl get endpoints <service-name> -n <namespace>
   ```

**解决方案示例**：

```yaml
# 修复服务端口映射错误
aapiVersion: v1
kind: Service
metadata:
  name: fix-port-mapping
  namespace: default
spec:
  selector:
    app: my-app
  ports:
  - name: http
    port: 80        # 服务端口
    targetPort: 8080  # 容器端口（确保与Pod配置一致）
    protocol: TCP
```

### 3.3 服务选择器匹配问题

**症状**：服务没有后端端点（Endpoints为空）

**排查步骤**：

1. 检查服务选择器：
   ```bash
   kubectl get svc <service-name> -n <namespace> -o yaml | grep -A 5 selector
   ```

2. 检查Pod标签：
   ```bash
   kubectl get pods -n <namespace> --show-labels
   kubectl describe pod <pod-name> -n <namespace> | grep Labels
   ```

3. 验证选择器匹配：
   ```bash
   kubectl get pods -n <namespace> -l <key>=<value>
   ```

**解决方案示例**：

```yaml
# 修复服务选择器不匹配问题
aapiVersion: v1
kind: Service
metadata:
  name: fix-selector
  namespace: default
spec:
  selector:
    app: my-app  # 确保与Pod标签一致
  ports:
  - name: http
    port: 80
    targetPort: 8080
```

### 3.4 服务类型相关问题

#### 3.4.1 ClusterIP服务

**症状**：Pod无法通过ClusterIP访问服务

**排查步骤**：

1. 检查服务ClusterIP配置：
   ```bash
   kubectl get svc <service-name> -n <namespace>
   ```

2. 在同一命名空间的Pod中测试访问：
   ```bash
   kubectl run -it --rm clusterip-test --image=busybox:1.35 -- /bin/sh
   curl http://<cluster-ip>:<port>
   ```

3. 检查网络策略：
   ```bash
   kubectl get networkpolicies -n <namespace>
   ```

#### 3.4.2 NodePort服务

**症状**：无法通过NodePort访问服务

**排查步骤**：

1. 检查NodePort配置：
   ```bash
   kubectl get svc <service-name> -n <namespace>
   ```

2. 检查节点端口是否已打开：
   ```bash
   kubectl describe node <node-name> | grep Allocated
   ```

3. 测试节点端口访问：
   ```bash
   curl http://<node-ip>:<node-port>
   ```

#### 3.4.3 LoadBalancer服务

**症状**：LoadBalancer服务外部IP处于pending状态或无法访问

**排查步骤**：

1. 检查LoadBalancer状态：
   ```bash
   kubectl get svc <service-name> -n <namespace>
   kubectl describe svc <service-name> -n <namespace>
   ```

2. 检查云提供商负载均衡器配置（如果使用云提供商）：
   - AWS: 检查ELB/ALB状态
   - GCP: 检查GCLB状态
   - Azure: 检查Azure Load Balancer状态

**解决方案示例**：

```yaml
# 修复NodePort范围问题
aapiVersion: v1
kind: Service
metadata:
  name: fix-nodeport
  namespace: default
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
  - name: http
    port: 80
    targetPort: 8080
    nodePort: 30080  # 使用集群允许的NodePort范围
```

### 3.5 网络策略问题

**症状**：Pod之间或Pod与服务之间的通信被拒绝

**排查步骤**：

1. 检查网络策略配置：
   ```bash
   kubectl get networkpolicies -n <namespace>
   kubectl describe networkpolicy <networkpolicy-name> -n <namespace>
   ```

2. 检查Pod标签是否与网络策略匹配：
   ```bash
   kubectl get pods -n <namespace> --show-labels
   ```

3. 测试网络策略是否阻止通信：
   ```bash
   kubectl run -it --rm network-test --image=busybox:1.35 -- /bin/sh
   curl http://<service-ip>:<port>
   ```

**解决方案示例**：

```yaml
# 创建允许特定Pod访问服务的网络策略
aapiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-service-access
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: my-app
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: allowed-client
    ports:
    - protocol: TCP
      port: 8080
```

### 3.6 跨命名空间访问问题

**症状**：Pod无法跨命名空间访问服务

**排查步骤**：

1. 检查目标命名空间的服务是否存在：
   ```bash
   kubectl get svc -n <target-namespace>
   ```

2. 使用完整服务域名测试访问：
   ```bash
   kubectl run -it --rm cross-namespace-test --image=busybox:1.35 -- /bin/sh
   curl http://<service-name>.<target-namespace>.svc.cluster.local:<port>
   ```

3. 检查目标命名空间的网络策略：
   ```bash
   kubectl get networkpolicies -n <target-namespace>
   ```

**解决方案示例**：

```yaml
# 创建允许跨命名空间访问的网络策略
aapiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-cross-namespace
  namespace: target-namespace
spec:
  podSelector:
    matchLabels:
      app: my-service
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: source-namespace
    ports:
    - protocol: TCP
      port: 80
```

### 3.7 服务代理问题

**症状**：kube-proxy配置问题导致服务无法访问

**排查步骤**：

1. 检查kube-proxy运行状态：
   ```bash
   kubectl get pods -n kube-system | grep kube-proxy
   ```

2. 查看kube-proxy日志：
   ```bash
   kubectl logs <kube-proxy-pod-name> -n kube-system
   ```

3. 检查kube-proxy模式：
   ```bash
   kubectl get configmap kube-proxy -n kube-system -o yaml
   ```

**解决方案示例**：

```yaml
# 修复kube-proxy配置（如果需要）
aapiVersion: v1
kind: ConfigMap
metadata:
  name: kube-proxy
  namespace: kube-system
data:
  config.conf: |
    apiVersion: kubeproxy.config.k8s.io/v1alpha1
    bindAddress: 0.0.0.0
    clientConnection:
      acceptContentTypes: ""
      burst: 10
      contentType: application/vnd.kubernetes.protobuf
      kubeconfig: /var/lib/kube-proxy/kubeconfig.conf
      qps: 5
    clusterCIDR: 10.244.0.0/16
    configSyncPeriod: 15m0s
    conntrack:
      maxPerCore: 32768
      min: 131072
      tcpCloseWaitTimeout: 1h0m0s
      tcpEstablishedTimeout: 24h0m0s
    enableProfiling: false
    healthzBindAddress: 0.0.0.0:10256
    hostnameOverride: ""
    iptables:
      masqueradeAll: false
      masqueradeBit: 14
      minSyncPeriod: 0s
      syncPeriod: 30s
    ipvs:
      excludeCIDRs: null
      minSyncPeriod: 0s
      scheduler: rr
      syncPeriod: 30s
      tcpFinTimeout: 0s
      tcpTimeout: 0s
      udpTimeout: 0s
    kind: KubeProxyConfiguration
    metricsBindAddress: 127.0.0.1:10249
    mode: "iptables"  # 或 "ipvs"
    nodePortAddresses: null
    oomScoreAdj: -999
    portRange: ""
    resourceContainer: /kube-proxy
    udpIdleTimeout: 250ms
    winkernel:
      enableDSR: false
      networkName: ""
      sourceVip: ""
```

## 4. 实用工具和命令

### 4.1 网络测试工具部署

```bash
# 部署网络测试Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: network-tools
spec:
  containers:
  - name: network-tools
    image: praqma/network-multitool:latest
    command:
    - /bin/sh
    - -c
    - sleep infinity
    ports:
    - containerPort: 80
EOF
```

### 4.2 常用测试命令

```bash
# 进入测试Pod
kubectl exec -it network-tools -- /bin/bash

# 测试DNS解析
nslookup <service-name>.<namespace>.svc.cluster.local

# 测试TCP连接
nc -zv <service-ip> <port>
telnet <service-ip> <port>

# 测试HTTP访问
curl -v http://<service-name>.<namespace>.svc.cluster.local:<port>
curl -v http://<service-ip>:<port>

# 测试NodePort访问
curl -v http://<node-ip>:<node-port>

# 测试跨命名空间访问
curl -v http://<service-name>.<target-namespace>.svc.cluster.local:<port>
```

### 4.3 服务诊断脚本

```bash
#!/bin/bash
# 服务诊断脚本

SERVICE_NAME=$1
NAMESPACE=${2:-default}

# 检查服务状态
echo "=== 服务状态 ==="
kubectl get svc $SERVICE_NAME -n $NAMESPACE

# 检查服务详情
echo -e "\n=== 服务详情 ==="
kubectl describe svc $SERVICE_NAME -n $NAMESPACE

# 检查服务端点
echo -e "\n=== 服务端点 ==="
kubectl get endpoints $SERVICE_NAME -n $NAMESPACE

# 检查匹配的Pod
echo -e "\n=== 匹配的Pod ==="
SELECTOR=$(kubectl get svc $SERVICE_NAME -n $NAMESPACE -o jsonpath='{.spec.selector}')
if [ -n "$SELECTOR" ]; then
  SELECTOR_ARGS=$(echo $SELECTOR | sed 's/[{}]/''/g' | sed 's/,/''/g' | sed 's/: /=/g')
  kubectl get pods -n $NAMESPACE -l $SELECTOR_ARGS
else
  echo "服务没有选择器"
fi

# 检查网络策略
echo -e "\n=== 网络策略 ==="
kubectl get networkpolicies -n $NAMESPACE
```

## 5. 故障模拟和练习

### 5.1 模拟服务选择器不匹配

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
  labels:
    app: my-application  # 注意标签名是my-application
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: mismatched-selector-service
spec:
  selector:
    app: my-app  # 选择器是my-app，与Pod标签不匹配
  ports:
  - name: http
    port: 80
    targetPort: 80
```

### 5.2 模拟服务端口映射错误

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-2
  labels:
    app: my-app
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80  # 容器端口是80
---
apiVersion: v1
kind: Service
metadata:
  name: wrong-port-service
spec:
  selector:
    app: my-app
  ports:
  - name: http
    port: 80
    targetPort: 8080  # 目标端口是8080，与容器端口不匹配
```

## 6. 最佳实践

1. **使用标准服务命名**：遵循`<service-name>.<namespace>.svc.cluster.local`命名规范
2. **合理配置健康探针**：为Pod配置适当的readinessProbe和livenessProbe
3. **使用网络策略**：根据最小权限原则配置网络策略
4. **监控服务状态**：设置服务端点和连通性监控
5. **使用服务网格**：考虑使用Istio、Linkerd等服务网格增强服务管理和监控
6. **文档化服务依赖**：记录服务之间的依赖关系和通信方式

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

本案例提供了Kubernetes环境中服务连通性问题的排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决服务连通性问题
- 了解Kubernetes服务的工作原理和常见问题
- 掌握网络测试工具和命令的使用
- 建立良好的服务连通性监控和管理习惯

通过不断实践和总结，您将能够更高效地管理和维护Kubernetes集群中的服务连通性。