# 🚀 Kubernetes Ingress高级特性实战

> 深入探索Kubernetes Ingress的高级功能：TLS/SSL证书管理、路径重写、自定义注解、蓝绿部署等企业级特性

## 📋 案例概述

本案例专注于Kubernetes Ingress的高级配置和企业级特性，帮助您掌握生产环境中Ingress的精细化管理和优化配置。

### 🔧 核心技能点

- **TLS/SSL证书管理**: Let's Encrypt自动证书、自签名证书、证书轮换
- **路径重写和正则表达式**: 高级路由规则配置
- **自定义注解**: 控制器特定配置和优化
- **蓝绿部署**: 无缝应用版本切换
- **金丝雀发布**: 渐进式流量迁移
- **请求重定向**: HTTP到HTTPS、域名重定向

### 🎯 适用人群

- 有一定Kubernetes经验的开发者
- DevOps/SRE工程师
- 系统架构师
- 性能优化专家

---

## 🚀 快速开始

### 1. 环境准备

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建专用命名空间
kubectl create namespace ingress-advanced

# 部署测试应用
kubectl apply -f advanced-apps.yaml -n ingress-advanced

# 验证部署
kubectl get pods -n ingress-advanced
```

### 2. 安装必备工具

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装cert-manager（用于TLS证书管理）
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml

# 等待cert-manager就绪
kubectl wait --for=condition=available deployment/cert-manager -n cert-manager --timeout=300s
```

---

## 📚 详细教程

### 1. TLS/SSL证书管理

#### 1.1 自签名证书配置

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
  namespace: ingress-advanced
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR...
  tls.key: LS0tLS1CRUdJTiBSU0EgUFJJV...
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - secure.example.com
    secretName: tls-secret
  rules:
  - host: secure.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

#### 1.2 Let's Encrypt自动证书

```yaml
# Certificate资源定义
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: letsencrypt-cert
  namespace: ingress-advanced
spec:
  secretName: letsencrypt-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: secure.example.com
  dnsNames:
  - secure.example.com
  - www.secure.example.com
---
# ClusterIssuer配置
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
    - http01:
        ingress:
          class: nginx
---
# 使用自动证书的Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: automated-tls-ingress
  namespace: ingress-advanced
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - secure.example.com
    secretName: letsencrypt-tls
  rules:
  - host: secure.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

#### 1.3 证书监控和轮换

```yaml
# 证书监控配置
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: cert-manager-monitor
  namespace: ingress-advanced
spec:
  selector:
    matchLabels:
      app: cert-manager
  endpoints:
  - port: metrics
    interval: 30s
---
# 证书到期告警规则
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: certificate-expiry-alerts
  namespace: ingress-advanced
spec:
  groups:
  - name: certificate.rules
    rules:
    - alert: CertificateExpirySoon
      expr: certmanager_certificate_expiration_timestamp_seconds - time() < 86400 * 14
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Certificate {{ $labels.name }} expires in 14 days"
        description: "Certificate will expire soon, needs renewal"
```

### 2. 高级路径重写

#### 2.1 基础路径重写

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rewrite-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /api/v1(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /static/(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: static-service
            port:
              number: 80
```

#### 2.2 复杂正则表达式重写

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: complex-rewrite-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$3
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      # 匹配 /users/{id}/profile -> /profile?id={id}
      - path: ^/users/([0-9]+)/profile$
        pathType: ImplementationSpecific
        backend:
          service:
            name: user-service
            port:
              number: 80
      # 匹配 /products/category/{name} -> /category?name={name}
      - path: ^/products/category/([^/]+)$
        pathType: ImplementationSpecific
        backend:
          service:
            name: product-service
            port:
              number: 80
      # 匹配 /admin/panel -> /admin/index.html
      - path: ^/admin/panel$
        pathType: ImplementationSpecific
        backend:
          service:
            name: admin-service
            port:
              number: 80
```

#### 2.3 条件重写

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: conditional-rewrite-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/configuration-snippet: |
      if ($request_uri ~* "^/mobile/(.*)") {
        rewrite ^/mobile/(.*) /mobile-app/$1 break;
      }
      if ($http_user_agent ~* "Mobile") {
        rewrite ^/(.*) /mobile/$1 break;
      }
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: main-service
            port:
              number: 80
```

### 3. 自定义注解配置

#### 3.1 性能优化注解

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: optimized-ingress
  namespace: ingress-advanced
  annotations:
    # 连接优化
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "10"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    
    # 缓冲区配置
    nginx.ingress.kubernetes.io/proxy-buffering: "on"
    nginx.ingress.kubernetes.io/proxy-buffer-size: "4k"
    nginx.ingress.kubernetes.io/proxy-buffers-number: "8"
    
    # 客户端限制
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/client-max-body-size: "50m"
    
    # 压缩配置
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "*"
    nginx.ingress.kubernetes.io/enable-gzip: "true"
    
    # 日志配置
    nginx.ingress.kubernetes.io/log-format-upstream: '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_length $request_time [$proxy_upstream_name] [$proxy_alternative_upstream_name] $upstream_addr $upstream_response_length $upstream_response_time $upstream_status $req_id'
spec:
  ingressClassName: nginx
  rules:
  - host: optimized.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

#### 3.2 安全相关注解

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
  namespace: ingress-advanced
  annotations:
    # 安全头配置
    nginx.ingress.kubernetes.io/configuration-snippet: |
      more_set_headers "X-Frame-Options: SAMEORIGIN";
      more_set_headers "X-Content-Type-Options: nosniff";
      more_set_headers "X-XSS-Protection: 1; mode=block";
      more_set_headers "Strict-Transport-Security: max-age=31536000; includeSubDomains";
    
    # IP白名单
    nginx.ingress.kubernetes.io/whitelist-source-range: "192.168.1.0/24,10.0.0.0/8"
    
    # 速率限制
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    
    # 请求限制
    nginx.ingress.kubernetes.io/limit-connections: "10"
    nginx.ingress.kubernetes.io/limit-rps: "5"
spec:
  ingressClassName: nginx
  rules:
  - host: secure.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### 4. 蓝绿部署和金丝雀发布

#### 4.1 蓝绿部署配置

```yaml
# 绿色环境（当前生产）
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
  namespace: ingress-advanced
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
      version: green
  template:
    metadata:
      labels:
        app: app
        version: green
    spec:
      containers:
      - name: app
        image: app:v1.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app-green-service
  namespace: ingress-advanced
spec:
  selector:
    app: app
    version: green
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
---
# 蓝色环境（新版本测试）
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
  namespace: ingress-advanced
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
      version: blue
  template:
    metadata:
      labels:
        app: app
        version: blue
    spec:
      containers:
      - name: app
        image: app:v2.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app-blue-service
  namespace: ingress-advanced
spec:
  selector:
    app: app
    version: blue
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
---
# 蓝绿切换Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: blue-green-ingress
  namespace: ingress-advanced
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-green-service  # 切换这里实现蓝绿部署
            port:
              number: 80
```

#### 4.2 金丝雀发布配置

```yaml
# 稳定版本服务
apiVersion: v1
kind: Service
metadata:
  name: app-stable-service
  namespace: ingress-advanced
spec:
  selector:
    app: app
    version: stable
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
---
# 金丝雀版本服务
apiVersion: v1
kind: Service
metadata:
  name: app-canary-service
  namespace: ingress-advanced
spec:
  selector:
    app: app
    version: canary
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
---
# 金丝雀发布Ingress配置
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: canary-ingress
  namespace: ingress-advanced
  annotations:
    # 金丝雀配置
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "20"  # 20%流量到金丝雀
    # 或者基于header路由
    # nginx.ingress.kubernetes.io/canary-by-header: "X-Canary"
    # nginx.ingress.kubernetes.io/canary-by-header-value: "always"
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-canary-service
            port:
              number: 80
---
# 主Ingress（接收剩余80%流量）
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  namespace: ingress-advanced
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-stable-service
            port:
              number: 80
```

### 5. 请求重定向和重写

#### 5.1 HTTP到HTTPS重定向

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: https-redirect-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/from-to-www-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - example.com
    - www.example.com
    secretName: tls-secret
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
  - host: www.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

#### 5.2 域名重定向

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: domain-redirect-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/permanent-redirect: https://newdomain.com$request_uri
spec:
  ingressClassName: nginx
  rules:
  - host: olddomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: dummy-service
            port:
              number: 80
```

#### 5.3 路径重定向

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: path-redirect-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/configuration-snippet: |
      location ~* ^/old-path(.*)$ {
        return 301 /new-path$1;
      }
spec:
  ingressClassName: nginx
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

---

## 🔧 实际应用场景

### 场景1：电商平台多版本API管理

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-api-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: nginx
  rules:
  - host: api.ecommerce.com
    http:
      paths:
      # v1 API路由
      - path: ^/api/v1(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: api-v1-service
            port:
              number: 80
      # v2 API路由（金丝雀发布）
      - path: ^/api/v2(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: api-v2-service
            port:
              number: 80
      # 管理后台
      - path: ^/admin(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: admin-service
            port:
              number: 80
```

### 场景2：微服务架构路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: microservices-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx
  rules:
  - host: services.company.com
    http:
      paths:
      - path: /user(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: user-service
            port:
              number: 80
      - path: /order(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: order-service
            port:
              number: 80
      - path: /payment(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: payment-service
            port:
              number: 80
      - path: /notification(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: notification-service
            port:
              number: 80
```

---

## 📊 性能调优

### 1. 负载均衡算法优化

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: loadbalancing-optimized-ingress
  namespace: ingress-advanced
  annotations:
    # 负载均衡算法
    nginx.ingress.kubernetes.io/upstream-hash-by: "$remote_addr"
    # 或者使用一致性哈希
    # nginx.ingress.kubernetes.io/upstream-hash-by-subset: "true"
    # nginx.ingress.kubernetes.io/upstream-hash-by-subset-size: "3"
    
    # 连接池优化
    nginx.ingress.kubernetes.io/proxy-next-upstream: "error timeout invalid_header http_500 http_502 http_503 http_504"
    nginx.ingress.kubernetes.io/proxy-next-upstream-tries: "3"
    nginx.ingress.kubernetes.io/proxy-next-upstream-timeout: "0"
spec:
  ingressClassName: nginx
  rules:
  - host: optimized.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### 2. 缓存优化配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: caching-optimized-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/configuration-snippet: |
      location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_lock on;
        add_header X-Cache-Status $upstream_cache_status;
      }
spec:
  ingressClassName: nginx
  rules:
  - host: cached.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

---

## ⚠️ 常见问题和解决方案

### 1. 证书续期失败

**问题**: Let's Encrypt证书无法自动续期

**解决方案**:
🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 检查证书状态
kubectl get certificates -n ingress-advanced

# 查看证书请求状态
kubectl describe certificaterequest -n ingress-advanced

# 检查Challenge状态
kubectl get challenges -n ingress-advanced

# 手动触发证书续期
kubectl delete certificate letsencrypt-cert -n ingress-advanced
```

### 2. 路径重写不生效

**问题**: 正则表达式路径重写没有按预期工作

**解决方案**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fixed-rewrite-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /api(/|$)(.*)
        pathType: ImplementationSpecific  # 必须使用ImplementationSpecific
        backend:
          service:
            name: api-service
            port:
              number: 80
```

### 3. 金丝雀权重不生效

**问题**: 金丝雀发布流量分配不符合预期

**解决方案**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: corrected-canary-ingress
  namespace: ingress-advanced
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "30"
    nginx.ingress.kubernetes.io/canary-weight-total: "100"
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: canary-service
            port:
              number: 80
```

---

## 🧪 实践练习

### 练习1：TLS证书管理
配置Let's Encrypt自动证书，并实现证书到期监控告警。

### 练习2：复杂路径重写
实现电商网站的复杂URL重写规则，包括商品、分类、用户等不同路径。

### 练习3：蓝绿部署实践
搭建完整的蓝绿部署环境，实现无缝版本切换。

### 练习4：金丝雀发布验证
配置金丝雀发布策略，验证不同权重下的流量分配效果。

---

## 📋 清理资源

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 删除命名空间和所有资源
kubectl delete namespace ingress-advanced

# 删除cert-manager（如果需要）
kubectl delete -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml

# 或单独删除各项资源
kubectl delete ingress --all -n ingress-advanced
kubectl delete svc --all -n ingress-advanced
kubectl delete deploy --all -n ingress-advanced
kubectl delete secrets --all -n ingress-advanced
```

---

> **💡 提示**: 高级Ingress特性需要根据具体业务场景谨慎配置，建议在测试环境中充分验证后再应用到生产环境。
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 Kubernetes 核心概念。

### 2. 适用场景

- 场景 1：开发与测试
- 场景 2：生产环境参考
- 场景 3：故障排查

## 💻 代码示例

### 基本命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
