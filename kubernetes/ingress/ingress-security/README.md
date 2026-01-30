# 🔐 Kubernetes Ingress安全配置实战

> 全面掌握Kubernetes Ingress的安全配置，包括认证授权、网络安全、访问控制等企业级安全实践

## 📋 案例概述

本案例深入探讨Kubernetes Ingress的安全配置和访问控制机制，帮助您构建安全可靠的外部访问入口。

### 🔧 核心技能点

- **认证与授权**: OAuth2、JWT、Basic Auth等认证方式
- **网络安全**: 网络策略、防火墙规则、IP白名单
- **访问控制**: 细粒度的权限管理和访问限制
- **安全审计**: 日志记录、监控告警、合规检查
- **DDoS防护**: 速率限制、连接限制、恶意请求防护

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
kubectl create namespace ingress-security

# 部署测试应用
kubectl apply -f security-test-apps.yaml -n ingress-security
```

### 2. 安装安全组件

```bash
# 安装oauth2-proxy
helm repo add oauth2-proxy https://oauth2-proxy.github.io/manifests
helm install oauth2-proxy oauth2-proxy/oauth2-proxy -n ingress-security

# 安装modsecurity
kubectl apply -f modsecurity-config.yaml -n ingress-security
```

---

## 📚 详细教程

### 1. 认证配置

#### 1.1 Basic Authentication

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: basic-auth
  namespace: ingress-security
type: Opaque
data:
  auth: YWRtaW46JGFwcjEkVHRScUE3NlkkLk5ENmJkdzlTd2RkME1NYW9Mc1B6LwoK  # admin:password
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: basic-auth-ingress
  namespace: ingress-security
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: "Authentication Required"
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

#### 1.2 OAuth2/JWT认证

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: oauth2-ingress
  namespace: ingress-security
  annotations:
    nginx.ingress.kubernetes.io/auth-url: "https://oauth2-proxy.ingress-security.svc.cluster.local/oauth2/auth"
    nginx.ingress.kubernetes.io/auth-signin: "https://oauth2.example.com/oauth2/start?rd=$escaped_request_uri"
    nginx.ingress.kubernetes.io/auth-response-headers: "x-auth-request-user,x-auth-request-email"
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
            name: app-service
            port:
              number: 80
```

### 2. 网络安全配置

#### 2.1 IP白名单

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: whitelist-ingress
  namespace: ingress-security
  annotations:
    nginx.ingress.kubernetes.io/whitelist-source-range: "192.168.1.0/24,10.0.0.0/8,172.16.0.0/12"
spec:
  ingressClassName: nginx
  rules:
  - host: internal.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: internal-service
            port:
              number: 80
```

#### 2.2 网络策略集成

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-controller-policy
  namespace: ingress-security
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: ingress-nginx
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: ingress-security
    ports:
    - protocol: TCP
      port: 80
```

### 3. WAF和攻击防护

#### 3.1 ModSecurity配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: waf-protected-ingress
  namespace: ingress-security
  annotations:
    nginx.ingress.kubernetes.io/modsecurity-snippet: |
      SecRuleEngine On
      SecRequestBodyAccess On
      SecAuditEngine RelevantOnly
      SecAuditLogParts ABIJDEFHZ
      SecRule REQUEST_HEADERS:User-Agent "^(.*)$" \
        "id:1000,phase:3,pass,setvar:tx.blocked_user_agents=%{tx.0}"
      SecRule ARGS_NAMES "union.*select|insert.*into|select.*from" \
        "id:1001,phase:2,block,msg:'SQL Injection Attack'"
spec:
  ingressClassName: nginx
  rules:
  - host: protected.example.com
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

## 🧪 实践练习

### 练习1：多层认证配置
配置Basic Auth + OAuth2的双重认证机制。

### 练习2：网络安全策略
实现完整的网络隔离和访问控制策略。

### 练习3：攻击防护测试
模拟常见攻击并验证防护机制的有效性。

---

## 📋 清理资源

```bash
kubectl delete namespace ingress-security
```