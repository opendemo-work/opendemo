# 🔄 Kubernetes Ingress 路由策略完整指南

> 企业级 Ingress 路由配置、策略管理和流量治理完整解决方案

## 📋 案例概述

本案例提供 Kubernetes Ingress 路由策略的完整实践体系，涵盖从基础路由到高级流量治理的所有场景，帮助企业实现精细化的流量管理和路由控制。

### 🔧 核心能力覆盖

- **基础路由**: 路径路由、主机路由、默认后端
- **高级路由**: 正则表达式、权重路由、金丝雀发布
- **流量治理**: 蓝绿部署、A/B测试、地域路由
- **负载均衡**: 算法选择、会话保持、健康检查
- **路由优化**: 路径重写、请求转发、性能调优
- **故障处理**: 重试机制、熔断降级、错误处理

### 🎯 适用场景

- 微服务架构路由管理
- 多版本应用流量分发
- A/B测试和灰度发布
- 多地域服务路由
- 高可用流量调度

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查Ingress Controller状态
kubectl get pods -n ingress-system -l app.kubernetes.io/name=ingress-nginx

# 创建演示命名空间
kubectl create namespace routing-demo

# 部署测试应用
kubectl apply -f sample-apps.yaml -n routing-demo
```

### 2. 基础路由配置

```bash
# 部署基础路由规则
kubectl apply -f basic-routing.yaml -n routing-demo

# 验证路由配置
kubectl get ingress -n routing-demo
kubectl describe ingress basic-routing -n routing-demo
```

---

## 📚 核心路由策略

### 1. 路径路由策略

#### 1.1 简单路径匹配

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: path-based-routing
  namespace: routing-demo
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          # 精确路径匹配
          - path: /api/users
            pathType: Exact
            backend:
              service:
                name: user-service
                port:
                  number: 80
          
          # 前缀路径匹配
          - path: /api/products
            pathType: Prefix
            backend:
              service:
                name: product-service
                port:
                  number: 80
          
          # 实现特定路径匹配
          - path: /static
            pathType: Prefix
            backend:
              service:
                name: static-service
                port:
                  number: 80
```

#### 1.2 正则表达式路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: regex-routing
  namespace: routing-demo
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          # 版本路由
          - path: /api/v(1|2)/users(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: user-service
                port:
                  number: 80
          
          # 数字ID路由
          - path: /products/([0-9]+)(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: product-service
                port:
                  number: 80
          
          # 字母ID路由
          - path: /categories/([a-zA-Z]+)(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: category-service
                port:
                  number: 80
```

### 2. 主机路由策略

#### 2.1 基于域名的路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: host-based-routing
  namespace: routing-demo
spec:
  ingressClassName: nginx
  rules:
    # 主站路由
    - host: company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: main-website
                port:
                  number: 80
    
    # API子域名路由
    - host: api.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-gateway
                port:
                  number: 80
    
    # 博客子域名路由
    - host: blog.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: blog-service
                port:
                  number: 80
```

#### 2.2 通配符域名路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: wildcard-host-routing
  namespace: routing-demo
spec:
  ingressClassName: nginx
  rules:
    # 通配符子域名
    - host: "*.company.com"
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: tenant-service
                port:
                  number: 80
    
    # 特定租户覆盖
    - host: premium.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: premium-service
                port:
                  number: 80
```

### 3. 权重路由策略

#### 3.1 金丝雀发布路由

```yaml
# 稳定版本服务
apiVersion: v1
kind: Service
metadata:
  name: app-stable
  namespace: routing-demo
spec:
  selector:
    app: myapp
    version: stable
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

---
# 金丝雀版本服务
apiVersion: v1
kind: Service
metadata:
  name: app-canary
  namespace: routing-demo
spec:
  selector:
    app: myapp
    version: canary
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

---
# 金丝雀路由配置
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: canary-routing
  namespace: routing-demo
  annotations:
    # 金丝雀配置
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "20"  # 20%流量到金丝雀
spec:
  ingressClassName: nginx
  rules:
    - host: app.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-canary
                port:
                  number: 80

---
# 主路由（接收剩余80%流量）
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-routing
  namespace: routing-demo
spec:
  ingressClassName: nginx
  rules:
    - host: app.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-stable
                port:
                  number: 80
```

#### 3.2 基于Header的权重路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: header-based-canary
  namespace: routing-demo
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-by-header: "X-Canary"
    nginx.ingress.kubernetes.io/canary-by-header-value: "always"
spec:
  ingressClassName: nginx
  rules:
    - host: app.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-canary
                port:
                  number: 80
```

### 4. 负载均衡策略

#### 4.1 负载均衡算法配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: loadbalancing-strategy
  namespace: routing-demo
  annotations:
    # 基于客户端IP的哈希
    nginx.ingress.kubernetes.io/upstream-hash-by: "$remote_addr"
    
    # 或基于请求URI的哈希
    # nginx.ingress.kubernetes.io/upstream-hash-by: "$request_uri"
    
    # 或基于自定义变量的哈希
    # nginx.ingress.kubernetes.io/upstream-hash-by: "$http_x_user_id"
spec:
  ingressClassName: nginx
  rules:
    - host: lb.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: loadbalanced-service
                port:
                  number: 80
```

#### 4.2 会话保持配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: sticky-sessions
  namespace: routing-demo
  annotations:
    # Cookie-based会话保持
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "ROUTE"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
    nginx.ingress.kubernetes.io/session-cookie-change-on-failure: "true"
spec:
  ingressClassName: nginx
  rules:
    - host: sticky.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: session-service
                port:
                  number: 80
```

### 5. 高级路由策略

#### 5.1 蓝绿部署路由

```yaml
# 蓝色环境
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: blue-environment
  namespace: routing-demo
spec:
  ingressClassName: nginx
  rules:
    - host: blue.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-blue
                port:
                  number: 80

---
# 绿色环境
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: green-environment
  namespace: routing-demo
spec:
  ingressClassName: nginx
  rules:
    - host: green.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-green
                port:
                  number: 80

---
# 主路由（初始指向蓝色）
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-traffic
  namespace: routing-demo
  annotations:
    nginx.ingress.kubernetes.io/configuration-snippet: |
      # 初始流量全部导向蓝色环境
      set $target_service "app-blue";
spec:
  ingressClassName: nginx
  rules:
    - host: company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-blue
                port:
                  number: 80
```

#### 5.2 A/B测试路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ab-testing
  namespace: routing-demo
  annotations:
    nginx.ingress.kubernetes.io/configuration-snippet: |
      # 基于用户ID的A/B测试
      set $variant "A";
      if ($http_x_user_id ~ "^[0-4]") {
        set $variant "A";
      }
      if ($http_x_user_id ~ "^[5-9]") {
        set $variant "B";
      }
spec:
  ingressClassName: nginx
  rules:
    - host: abtest.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: variant-a-service  # 默认路由到A版本
                port:
                  number: 80
```

---

## 🔧 路径重写和转发

### 1. 路径重写配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rewrite-example
  namespace: routing-demo
  annotations:
    # 基础路径重写
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    
    # 添加前缀
    nginx.ingress.kubernetes.io/add-base-url: "true"
    
    # SSL重定向
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          # 将 /api/v1/users/123 重写为 /users/123
          - path: /api/v1(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

### 2. 请求转发配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: proxy-configuration
  namespace: routing-demo
  annotations:
    # 代理缓冲区配置
    nginx.ingress.kubernetes.io/proxy-buffering: "on"
    nginx.ingress.kubernetes.io/proxy-buffer-size: "4k"
    nginx.ingress.kubernetes.io/proxy-buffers-number: "8"
    
    # 超时配置
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "10"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    
    # 下游服务器配置
    nginx.ingress.kubernetes.io/proxy-next-upstream: "error timeout invalid_header http_500 http_502 http_503 http_504"
    nginx.ingress.kubernetes.io/proxy-next-upstream-timeout: "10"
    nginx.ingress.kubernetes.io/proxy-next-upstream-tries: "3"
spec:
  ingressClassName: nginx
  rules:
    - host: proxy.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: backend-service
                port:
                  number: 80
```

---

## 📊 路由监控和指标

### 1. 路由性能监控

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: monitored-routing
  namespace: routing-demo
  annotations:
    # 启用详细日志
    nginx.ingress.kubernetes.io/enable-access-log: "true"
    nginx.ingress.kubernetes.io/access-log-path: "/var/log/nginx/access.log"
    
    # 自定义日志格式
    nginx.ingress.kubernetes.io/log-format-upstream: '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_length $request_time [$proxy_upstream_name] $upstream_addr $upstream_response_length $upstream_response_time $upstream_status $req_id'
    
    # 慢查询日志
    nginx.ingress.kubernetes.io/configuration-snippet: |
      log_format timed_combined '$remote_addr - $remote_user [$time_local] '
                                '"$request" $status $body_bytes_sent '
                                '"$http_referer" "$http_user_agent" '
                                '$request_time $upstream_response_time';
      access_log /var/log/nginx/timed_access.log timed_combined if=$request_time > 1.0;
spec:
  ingressClassName: nginx
  rules:
    - host: monitored.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: monitored-service
                port:
                  number: 80
```

### 2. 路由指标收集

```yaml
# Prometheus ServiceMonitor配置
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ingress-routing-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: ingress-nginx
  namespaceSelector:
    matchNames:
      - ingress-system
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
      relabelings:
        - sourceLabels: [__meta_kubernetes_ingress_name]
          targetLabel: ingress
        - sourceLabels: [__meta_kubernetes_ingress_host]
          targetLabel: host
```

---

## ⚠️ 常见问题和解决方案

### 1. 路径匹配问题

**问题现象**: 路径路由不按预期工作

**解决方案**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fixed-path-matching
  namespace: routing-demo
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          # 使用ImplementationSpecific获得更精确的匹配
          - path: /app(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: app-service
                port:
                  number: 80
```

### 2. 路由冲突解决

**问题现象**: 多个Ingress规则冲突

**解决方案**:
```yaml
# 使用优先级注解
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: high-priority-routing
  namespace: routing-demo
  annotations:
    nginx.ingress.kubernetes.io/server-snippet: |
      set $priority "high";
spec:
  ingressClassName: nginx
  rules:
    - host: priority.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: high-priority-service
                port:
                  number: 80

---
# 低优先级路由
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: low-priority-routing
  namespace: routing-demo
spec:
  ingressClassName: nginx
  rules:
    - host: "*.company.com"
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: default-service
                port:
                  number: 80
```

---

## 🧪 实践练习

### 练习1：多路径路由配置
配置一个Ingress规则，实现对不同API路径的精确路由。

### 练习2：金丝雀发布实践
实现20%流量到新版本的金丝雀发布策略。

### 练习3：蓝绿部署演练
配置完整的蓝绿部署路由切换机制。

### 练习4：A/B测试配置
基于用户特征实现A/B测试路由策略。

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes Ingress路由文档](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [NGINX Ingress注解参考](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/)

### 相关案例
- [Ingress控制器管理](../controllers/nginx-controller/)
- [Ingress安全加固](../security-hardening/)
- [Ingress监控运维](../monitoring-operations/)

### 进阶主题
- 服务网格路由集成
- 多集群路由管理
- 智能DNS路由
- AI驱动的流量调度

---

## 📋 清理资源

```bash
# 删除演示资源
kubectl delete namespace routing-demo

# 或单独删除各项资源
kubectl delete ingress --all -n routing-demo
kubectl delete svc --all -n routing-demo
kubectl delete deploy --all -n routing-demo
```

---

> **💡 提示**: 合理的路由策略是微服务架构成功的关键，建议根据业务需求选择合适的路由模式并持续优化。