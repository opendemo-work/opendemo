# Kubernetes网络策略问题排查实战

## 1. 案例概述

本案例提供了Kubernetes环境中网络策略问题的排查方法和解决方案，包括：
- 网络策略导致的Pod间通信失败
- 策略规则配置错误
- 命名空间隔离问题
- 入口策略（Ingress）配置问题
- 出口策略（Egress）配置问题
- 标签选择器匹配问题
- 网络策略优先级问题

## 2. 环境准备

- Kubernetes集群（v1.20+）
- 支持NetworkPolicy的CNI插件（如Calico、Cilium、Weave Net等）
- kubectl命令行工具
- 网络测试工具（如curl、nc、telnet）

## 3. 常见网络策略问题排查

### 3.1 网络策略导致的Pod间通信失败

**症状**：
- Pod间无法正常通信
- 服务访问超时
- 应用日志显示连接被拒绝
- 网络策略启用前后通信状态变化

**排查步骤**：

1. 验证CNI插件是否支持NetworkPolicy：
   ```bash
   # 检查CNI插件类型
   kubectl get pods -n kube-system | grep -E "calico|cilium|weave|flannel"
   ```

2. 查看命名空间中的网络策略：
   ```bash
   kubectl get networkpolicy -n <namespace>
   kubectl describe networkpolicy <policy-name> -n <namespace>
   ```

3. 测试Pod间通信：
   ```bash
   kubectl run -it --rm test-pod --image=busybox:1.35 -- /bin/sh
   nc -zv <target-pod-ip> <target-port>
   curl -v http://<target-pod-ip>:<target-port>
   ```

4. 检查Pod标签是否与网络策略匹配：
   ```bash
   kubectl get pod <pod-name> -n <namespace> --show-labels
   ```

**解决方案示例**：

```yaml
# 修复网络策略，允许Pod间通信
aapiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-pod-communication
spec:
  podSelector:
    matchLabels:
      app: target-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: source-app
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: source-app
    ports:
    - protocol: TCP
      port: 80
```

### 3.2 策略规则配置错误

**症状**：
- 网络策略不生效
- 预期允许的通信被阻止
- 预期阻止的通信被允许
- 策略语法错误导致创建失败

**排查步骤**：

1. 检查网络策略语法：
   ```bash
   kubectl apply -f <network-policy-file.yaml> --dry-run=client
   ```

2. 查看网络策略详细配置：
   ```bash
   kubectl get networkpolicy <policy-name> -n <namespace> -o yaml
   ```

3. 测试不同方向的通信：
   ```bash
   # 测试Ingress
   kubectl run -it --rm ingress-test --image=busybox:1.35 -- /bin/sh
   curl -v http://<target-pod-ip>:<target-port>
   
   # 测试Egress
   kubectl exec -it <target-pod> -n <namespace> -- /bin/sh
   curl -v http://<external-service-ip>:<external-port>
   ```

4. 检查策略规则的逻辑关系：
   - 多个from/to规则是OR关系
   - 单个from/to中的多个条件是AND关系

**解决方案示例**：

```yaml
# 修复网络策略规则，允许所有Pod访问
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector:
    matchLabels:
      app: my-app
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector: {}
    ports:
    - protocol: TCP
      port: 80
```

### 3.3 命名空间隔离问题

**症状**：
- 跨命名空间通信失败
- 同一命名空间内通信正常
- 服务访问跨命名空间时超时

**排查步骤**：

1. 查看目标命名空间的网络策略：
   ```bash
   kubectl get networkpolicy -n <target-namespace>
   ```

2. 检查命名空间选择器配置：
   ```bash
   kubectl describe networkpolicy <policy-name> -n <target-namespace> | grep -A 10 from
   ```

3. 测试跨命名空间通信：
   ```bash
   kubectl run -it --rm cross-ns-test --image=busybox:1.35 -- /bin/sh
   curl -v http://<service-name>.<target-namespace>.svc.cluster.local:<port>
   ```

4. 检查命名空间标签：
   ```bash
   kubectl get namespace --show-labels
   ```

**解决方案示例**：

```yaml
# 允许跨命名空间访问的网络策略
aapiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-cross-namespace
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

### 3.4 入口策略（Ingress）配置问题

**症状**：
- 外部无法访问Pod服务
- 入口流量被拒绝
- 健康检查失败
- 负载均衡器无法连接到后端Pod

**排查步骤**：

1. 查看Ingress策略配置：
   ```bash
   kubectl get networkpolicy <policy-name> -n <namespace> -o yaml | grep -A 20 ingress
   ```

2. 检查端口配置：
   ```bash
   kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 containerPort
   ```

3. 测试Ingress规则：
   ```bash
   kubectl run -it --rm ingress-test --image=busybox:1.35 -- /bin/sh
   nc -zv <pod-ip> <port>
   ```

4. 检查策略类型是否包含Ingress：
   ```bash
   kubectl get networkpolicy <policy-name> -n <namespace> -o yaml | grep policyTypes
   ```

**解决方案示例**：

```yaml
# 修复Ingress策略配置
aapiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: fix-ingress-policy
spec:
  podSelector:
    matchLabels:
      app: web-app
  policyTypes:
  - Ingress  # 确保包含Ingress类型
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0  # 允许所有IP访问
    ports:
    - protocol: TCP
      port: 80  # 确保端口正确
      targetPort: 8080  # 可选，指定容器端口
```

### 3.5 出口策略（Egress）配置问题

**症状**：
- Pod无法访问外部服务
- DNS解析失败
- 外部API调用超时
- 容器无法拉取外部资源

**排查步骤**：

1. 查看Egress策略配置：
   ```bash
   kubectl get networkpolicy <policy-name> -n <namespace> -o yaml | grep -A 20 egress
   ```

2. 检查策略类型是否包含Egress：
   ```bash
   kubectl get networkpolicy <policy-name> -n <namespace> -o yaml | grep policyTypes
   ```

3. 测试Egress规则：
   ```bash
   kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
   ping -c 3 google.com
   curl -v http://example.com
   nslookup kubernetes.default.svc.cluster.local
   ```

4. 检查DNS访问权限：
   ```bash
   # 确保允许访问DNS服务器
   kubectl get networkpolicy <policy-name> -n <namespace> -o yaml | grep -A 10 "53"
   ```

**解决方案示例**：

```yaml
# 修复Egress策略，允许访问外部服务和DNS
aapiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: fix-egress-policy
spec:
  podSelector:
    matchLabels:
      app: my-app
  policyTypes:
  - Egress  # 确保包含Egress类型
  egress:
  # 允许DNS查询
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
  # 允许访问外部服务
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
```

### 3.6 标签选择器匹配问题

**症状**：
- 网络策略不生效
- 预期的Pod未被策略覆盖
- 策略应用到了错误的Pod

**排查步骤**：

1. 检查Pod标签：
   ```bash
   kubectl get pods -n <namespace> --show-labels
   ```

2. 检查网络策略的podSelector：
   ```bash
   kubectl get networkpolicy <policy-name> -n <namespace> -o yaml | grep -A 5 podSelector
   ```

3. 验证标签选择器匹配：
   ```bash
   kubectl get pods -n <namespace> -l <key>=<value>
   ```

4. 检查from/to规则中的标签选择器：
   ```bash
   kubectl get networkpolicy <policy-name> -n <namespace> -o yaml | grep -A 10 from
   ```

**解决方案示例**：

```yaml
# 修复标签选择器配置
aapiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: fix-label-selector
spec:
  podSelector:
    matchLabels:
      app: correct-app-label  # 使用正确的Pod标签
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: allowed-app  # 使用正确的来源Pod标签
    ports:
    - protocol: TCP
      port: 80
```

### 3.7 网络策略优先级问题

**症状**：
- 多个网络策略应用到同一Pod
- 策略间存在冲突
- 预期的策略规则未生效

**排查步骤**：

1. 查看命名空间中的所有网络策略：
   ```bash
   kubectl get networkpolicy -n <namespace>
   ```

2. 分析每个策略的覆盖范围：
   ```bash
   for policy in $(kubectl get networkpolicy -n <namespace> -o name); do
     echo "=== $policy ==="
     kubectl get $policy -n <namespace> -o yaml | grep -A 5 podSelector
   done
   ```

3. 测试不同Pod组合的通信：
   ```bash
   # 测试不同标签组合的Pod通信
   ```

4. 理解网络策略的应用规则：
   - 多个策略规则是累加关系
   - 没有优先级概念，所有匹配的规则都会应用
   - 策略是白名单机制，默认拒绝所有流量

**解决方案示例**：

```yaml
# 整合网络策略，避免冲突
aapiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: consolidated-policy
spec:
  podSelector:
    matchLabels:
      app: my-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # 允许前端应用访问
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  # 允许监控系统访问
  - from:
    - podSelector:
        matchLabels:
          app: monitoring
    ports:
    - protocol: TCP
      port: 9100
  egress:
  # 允许访问数据库
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  # 允许访问DNS
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - protocol: UDP
      port: 53
```

## 4. 实用工具和命令

### 4.1 网络策略诊断命令

```bash
# 查看命名空间中的网络策略
kubectl get networkpolicy -n <namespace>
kubectl describe networkpolicy <policy-name> -n <namespace>
kubectl get networkpolicy <policy-name> -n <namespace> -o yaml

# 检查Pod标签
kubectl get pods -n <namespace> --show-labels
kubectl describe pod <pod-name> -n <namespace> | grep Labels

# 测试网络连接
kubectl run -it --rm network-test --image=busybox:1.35 -- /bin/sh
nc -zv <target-ip> <target-port>
curl -v http://<target-ip>:<target-port>
ping -c 3 <target-ip>

# 查看CNI插件状态
kubectl get pods -n kube-system | grep -E "calico|cilium|weave|flannel"
kubectl logs <cni-pod-name> -n kube-system

# 验证网络策略是否应用
kubectl exec -it <calico-node-pod> -n kube-system -- calicoctl get networkpolicy -n <namespace>
```

### 4.2 网络策略分析脚本

```bash
#!/bin/bash
# 网络策略分析脚本

NAMESPACE=${1:-default}

# 查看命名空间中的网络策略
echo "=== 命名空间网络策略 ==="
kubectl get networkpolicy -n $NAMESPACE

# 查看每个网络策略的详细信息
echo -e "\n=== 网络策略详细信息 ==="
for policy in $(kubectl get networkpolicy -n $NAMESPACE -o name); do
  echo -e "\n--- $policy ---"
  kubectl describe $policy -n $NAMESPACE
 done

# 查看Pod标签和策略匹配情况
echo -e "\n=== Pod标签和策略匹配情况 ==="
kubectl get pods -n $NAMESPACE --show-labels

# 检查网络策略覆盖的Pod
echo -e "\n=== 网络策略覆盖的Pod ==="
for policy in $(kubectl get networkpolicy -n $NAMESPACE -o name); do
  echo -e "\n--- $policy ---
覆盖的Pod："
  selector=$(kubectl get $policy -n $NAMESPACE -o jsonpath='{.spec.podSelector.matchLabels}')
  if [ -n "$selector" ]; then
    # 将selector转换为kubectl label selector格式
    label_selector=$(echo $selector | sed 's/[{}]/''/g' | sed 's/,/''/g' | sed 's/: /=/g')
    kubectl get pods -n $NAMESPACE -l $label_selector
  else
    echo "所有Pod"
  fi
done
```

### 4.3 网络测试Pod部署

```bash
# 部署网络测试Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: network-test-pod
  labels:
    app: network-test
spec:
  containers:
  - name: network-test
    image: praqma/network-multitool:latest
    command:
    - /bin/sh
    - -c
    - sleep infinity
    ports:
    - containerPort: 80
EOF
```

## 5. 故障模拟和练习

### 5.1 模拟网络策略阻止Pod通信

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: source-pod
  labels:
    app: source
spec:
  containers:
  - name: source-container
    image: nginx:1.21
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Pod
metadata:
  name: target-pod
  labels:
    app: target
spec:
  containers:
  - name: target-container
    image: nginx:1.21
    ports:
    - containerPort: 80
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-all-ingress
spec:
  podSelector:
    matchLabels:
      app: target
  policyTypes:
  - Ingress
  # 没有ingress规则，默认拒绝所有Ingress流量
```

### 5.2 模拟标签选择器不匹配

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
  labels:
    app: my-application  # 注意标签名是my-application
spec:
  containers:
  - name: app-container
    image: nginx:1.21
    ports:
    - containerPort: 80
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: wrong-label-selector
spec:
  podSelector:
    matchLabels:
      app: my-app  # 选择器是my-app，与Pod标签不匹配
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: any-app
    ports:
    - protocol: TCP
      port: 80
```

### 5.3 模拟Egress策略阻止外部访问

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: egress-pod
  labels:
    app: egress-test
spec:
  containers:
  - name: egress-container
    image: busybox:1.35
    command:
    - /bin/sh
    - -c
    - sleep infinity
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-all-egress
spec:
  podSelector:
    matchLabels:
      app: egress-test
  policyTypes:
  - Egress
  # 没有egress规则，默认拒绝所有Egress流量
```

## 6. 最佳实践

1. **默认拒绝所有流量**：
   - 遵循最小权限原则，默认拒绝所有流量
   - 只允许明确需要的通信

2. **使用标签进行精确匹配**：
   - 为Pod和服务添加明确的标签
   - 使用精确的标签选择器

3. **明确指定策略类型**：
   - 明确指定Ingress和/或Egress类型
   - 避免依赖默认行为

4. **允许DNS访问**：
   - 确保所有需要DNS解析的Pod允许访问DNS服务
   - 添加DNS服务的Egress规则

5. **定期审查网络策略**：
   - 定期审查和更新网络策略
   - 移除不再需要的策略
   - 合并冲突的策略

6. **测试网络策略**：
   - 部署前测试网络策略
   - 验证预期的通信被允许
   - 验证非预期的通信被阻止

7. **使用工具辅助管理**：
   - 使用Calicoctl、Cilium CLI等工具管理网络策略
   - 考虑使用网络策略可视化工具

8. **文档化网络策略**：
   - 记录网络策略的设计意图
   - 文档化通信流和依赖关系
   - 保持策略与应用架构一致

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

本案例提供了Kubernetes环境中网络策略问题的排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决网络策略导致的通信问题
- 了解NetworkPolicy的工作原理和配置规则
- 掌握网络策略的最佳实践
- 建立良好的网络安全习惯

通过合理配置和管理网络策略，您将能够提高Kubernetes集群的网络安全性，实现精细的网络访问控制，保护应用和数据的安全。