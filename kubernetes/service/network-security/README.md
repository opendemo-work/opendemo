# 🔐 Kubernetes Service网络安全与访问控制

> 全面掌握Kubernetes Service的网络安全配置，包括Network Policies、RBAC权限控制、TLS加密、服务网格集成等企业级安全实践

## 📋 案例概述

本案例深入探讨Kubernetes Service的安全配置和访问控制机制，帮助您构建安全可靠的微服务架构。

### 🔧 核心技能点

- **Network Policies**: 网络策略配置和实施
- **RBAC权限控制**: 服务账户和角色绑定
- **TLS加密**: 服务间通信安全
- **服务网格集成**: Istio安全策略
- **访问控制**: 细粒度的访问权限管理
- **安全审计**: 日志记录和监控

### 🎯 适用人群

- 安全工程师
- DevSecOps从业者
- 云安全架构师
- 合规性管理人员

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建安全测试命名空间
kubectl create namespace service-security

# 启用网络策略支持（如果尚未启用）
kubectl apply -f network-policy-crd.yaml

# 部署测试应用
kubectl apply -f security-test-apps.yaml -n service-security
```

### 2. 验证初始状态

```bash
# 检查Pod状态
kubectl get pods -n service-security

# 测试基础连通性
kubectl run debug-pod --image=busybox --rm -it -n service-security -- ping -c 3 frontend-service
```

---

## 📚 详细教程

### 1. Network Policies基础配置

控制Pod间的网络通信。

#### 默认拒绝策略

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: service-security
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

#### 允许特定标签的Pod通信

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-access
  namespace: service-security
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

#### 基于命名空间的网络策略

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-monitoring
  namespace: service-security
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 9090
```

### 2. Service级别的RBAC控制

为Service配置细粒度的访问权限。

#### 创建专用服务账户

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: frontend-sa
  namespace: service-security
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: backend-sa
  namespace: service-security
```

#### 配置Role和RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: service-reader
  namespace: service-security
rules:
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: frontend-service-access
  namespace: service-security
subjects:
- kind: ServiceAccount
  name: frontend-sa
  namespace: service-security
roleRef:
  kind: Role
  name: service-reader
  apiGroup: rbac.authorization.k8s.io
```

#### 部署使用服务账户的应用

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
  namespace: service-security
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      serviceAccountName: frontend-sa
      containers:
      - name: frontend
        image: nginx:1.21
        ports:
        - containerPort: 80
```

### 3. TLS加密配置

为Service启用传输层安全加密。

#### 创建TLS证书Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
  namespace: service-security
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCi...
  tls.key: LS0tLS1CRUdJTiBSU0EgUFJJV...
```

#### 配置TLS Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: secure-service
  namespace: service-security
spec:
  selector:
    app: secure-app
  ports:
    - name: https
      protocol: TCP
      port: 443
      targetPort: 8443
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app-deployment
  namespace: service-security
spec:
  replicas: 2
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      containers:
      - name: secure-app
        image: nginx:1.21
        ports:
        - containerPort: 8443
        volumeMounts:
        - name: tls-certs
          mountPath: /etc/nginx/ssl
          readOnly: true
      volumes:
      - name: tls-certs
        secret:
          secretName: tls-secret
```

### 4. 服务网格安全集成（Istio）

利用服务网格实现更精细的安全控制。

#### 启用Sidecar注入

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: service-security
  labels:
    istio-injection: enabled
```

#### 配置mTLS策略

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: service-security
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: frontend-to-backend
  namespace: service-security
spec:
  selector:
    matchLabels:
      app: backend
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/service-security/sa/frontend-sa"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

#### 配置入口网关安全

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: secure-gateway
  namespace: service-security
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: gateway-tls-cert
    hosts:
    - "secure.example.com"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: secure-service-route
  namespace: service-security
spec:
  hosts:
  - "secure.example.com"
  gateways:
  - secure-gateway
  http:
  - match:
    - uri:
        prefix: /api
    route:
    - destination:
        host: secure-service
        port:
          number: 443
```

### 5. 外部访问安全控制

控制Service对外部的暴露程度。

#### 内部服务配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: internal-service
  namespace: service-security
  annotations:
    # AWS内部负载均衡器
    service.beta.kubernetes.io/aws-load-balancer-internal: "true"
    # Azure内部负载均衡器
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
spec:
  selector:
    app: internal-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

#### IP白名单配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: restricted-service
  namespace: service-security
  annotations:
    # AWS负载均衡器访问控制
    service.beta.kubernetes.io/aws-load-balancer-access-log-enabled: "true"
    service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-prefix: "access-logs"
spec:
  selector:
    app: restricted-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

### 6. 安全审计和监控

配置安全事件的日志记录和监控。

#### 启用审计日志

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
metadata:
  name: service-audit-policy
rules:
- level: RequestResponse
  resources:
  - group: ""
    resources: ["services", "endpoints"]
  verbs: ["create", "update", "delete", "patch"]
  userGroups: ["system:serviceaccounts"]
```

#### 配置安全监控

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: service-security-monitor
  namespace: service-security
spec:
  selector:
    matchLabels:
      app: security-monitor
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
---
apiVersion: v1
kind: Service
metadata:
  name: security-monitor
  namespace: service-security
  labels:
    app: security-monitor
spec:
  selector:
    app: security-collector
  ports:
    - name: metrics
      port: 8080
      targetPort: 8080
```

---

## 🔧 实际安全场景

### 场景1：零信任网络架构

```yaml
# 默认拒绝所有流量
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: zero-trust-default-deny
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

# 仅允许必要的服务间通信
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-gateway-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: user-service
    ports:
    - protocol: TCP
      port: 8080
  - to:
    - podSelector:
        matchLabels:
          app: order-service
    ports:
    - protocol: TCP
      port: 8080
```

### 场景2：多租户环境隔离

```yaml
# 租户A网络策略
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-a-isolation
  namespace: tenant-a
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          tenant: a
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          tenant: a

# 租户B网络策略
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-b-isolation
  namespace: tenant-b
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          tenant: b
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          tenant: b
```

### 场景3：合规性安全配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: pci-compliant-service
  namespace: pci-zone
  annotations:
    # 启用PCI DSS合规性检查
    security.alpha.kubernetes.io/sysctls: "net.ipv4.tcp_syncookies=1"
spec:
  selector:
    app: payment-service
  ports:
    - protocol: TCP
      port: 443
      targetPort: 8443
  type: LoadBalancer
  externalTrafficPolicy: Local
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: pci-network-policy
  namespace: pci-zone
spec:
  podSelector:
    matchLabels:
      app: payment-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          zone: dmz
    ports:
    - protocol: TCP
      port: 443
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/8
    ports:
    - protocol: TCP
      port: 5432  # PostgreSQL
```

---

## 📊 安全评估和测试

### 1. 网络策略有效性测试

```bash
# 测试网络策略是否生效
kubectl run test-pod --image=busybox --rm -it -n service-security -- sh

# 在测试Pod中尝试访问被限制的服务
wget -qO- http://restricted-service:80 || echo "Access denied as expected"

# 测试允许的访问
wget -qO- http://allowed-service:80 && echo "Access granted as expected"
```

### 2. TLS证书验证

```bash
# 验证TLS配置
openssl s_client -connect secure-service.service-security.svc:443 -servername secure.example.com

# 检查证书有效期
echo | openssl s_client -connect secure-service:443 2>/dev/null | openssl x509 -noout -dates
```

### 3. RBAC权限验证

```bash
# 测试服务账户权限
kubectl auth can-i get services --as=system:serviceaccount:service-security:frontend-sa

# 验证权限边界
kubectl auth can-i delete services --as=system:serviceaccount:service-security:frontend-sa
```

---

## ⚠️ 常见安全问题和解决方案

### 1. 网络策略配置不当

**问题**: 策略过于宽松导致安全风险

**解决方案**:
```yaml
# 采用最小权限原则
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrictive-policy
  namespace: critical-apps
spec:
  podSelector:
    matchLabels:
      app: critical-service
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: trusted-client
    - namespaceSelector:
        matchLabels:
          security-level: high
    ports:
    - protocol: TCP
      port: 443
```

### 2. TLS证书管理混乱

**问题**: 证书过期或配置错误

**解决方案**:
```bash
# 自动化证书轮换
kubectl create secret tls auto-renew-cert \
  --cert=new-cert.pem \
  --key=new-key.pem \
  --namespace=service-security

# 配置证书监控告警
kubectl apply -f certificate-monitor.yaml
```

### 3. 服务账户权限过大

**问题**: 服务账户拥有不必要的集群级权限

**解决方案**:
```yaml
# 限制服务账户权限范围
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: limited-service-role
  namespace: service-security
rules:
- apiGroups: [""]
  resources: ["services"]
  resourceNames: ["specific-service"]  # 限制只能访问特定服务
  verbs: ["get", "list"]
```

---

## 🧪 实践练习

### 练习1：构建零信任网络
为一个三层应用（前端、API、数据库）配置完整的网络策略，实现最小权限访问。

### 练习2：TLS端到端加密
配置服务间的mTLS通信，确保所有内部流量都经过加密传输。

### 练习3：多租户安全隔离
设计并实现一个多租户环境的安全隔离方案，确保租户间完全隔离。

### 练习4：安全审计实施
配置完整的安全审计日志收集和监控告警系统。

---

## 📋 清理资源

```bash
# 删除安全测试环境
kubectl delete namespace service-security

# 清理相关资源
kubectl delete networkpolicy --all -n service-security
kubectl delete rolebinding --all -n service-security
kubectl delete role --all -n service-security
kubectl delete serviceaccount --all -n service-security
```

---

> **💡 提示**: 网络安全配置需要根据具体的业务需求和合规要求进行定制，在生产环境中实施前务必进行充分测试。