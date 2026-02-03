# 🌐 Kubernetes Ingress 生产级完整套件

> 企业级 Ingress 配置、管理、安全和监控的完整解决方案，满足生产环境所有需求

## 📋 案例概述

本案例提供 Kubernetes Ingress 的企业级完整实践体系，涵盖从基础配置到高级特性的全方位内容，确保在生产环境中能够安全、高效地管理和维护入口流量。

### 🔧 核心能力覆盖

- **多控制器支持**: NGINX、Traefik、HAProxy、Istio Gateway
- **高级路由配置**: 路径路由、主机路由、权重路由、金丝雀发布
- **安全加固**: TLS/SSL、认证授权、WAF防护、速率限制
- **监控告警**: Prometheus指标、访问日志、性能分析
- **故障排查**: 诊断工具、常见问题解决、性能优化
- **生产最佳实践**: 配置管理、蓝绿部署、灰度发布

### 🎯 适用场景

- 企业级微服务网关
- 生产环境流量入口
- 安全合规要求
- 高性能API网关
- 多租户环境管理

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查集群状态
kubectl cluster-info
kubectl get nodes

# 创建生产环境命名空间
kubectl create namespace ingress-prod

# 验证Ingress API可用性
kubectl get ingressclasses
```

### 2. 部署Ingress Controller

```bash
# 使用Helm部署NGINX Ingress Controller（生产推荐）
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"="nlb" \
  --set controller.config.use-forwarded-headers=true \
  --set controller.metrics.enabled=true \
  --set controller.resources.requests.cpu=100m \
  --set controller.resources.requests.memory=90Mi \
  --set controller.resources.limits.cpu=1000m \
  --set controller.resources.limits.memory=512Mi
```

### 3. 部署测试应用

```bash
# 部署生产级应用
kubectl apply -f production-apps.yaml -n ingress-prod

# 验证部署状态
kubectl get pods -n ingress-prod
kubectl get services -n ingress-prod
```

---

## 📚 核心组件详解

### 1. 高级路由配置

#### 1.1 复杂路径路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: advanced-routing
  namespace: ingress-prod
  annotations:
    # 路径重写配置
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    # 请求速率限制
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    # 连接限制
    nginx.ingress.kubernetes.io/limit-connections: "100"
    # 代理缓冲区优化
    nginx.ingress.kubernetes.io/proxy-buffering: "on"
    nginx.ingress.kubernetes.io/proxy-buffer-size: "4k"
    # 客户端最大体大小
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
spec:
  ingressClassName: nginx
  rules:
    - host: api.company.com
      http:
        paths:
          # API版本路由
          - path: /api/v1(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: api-v1-service
                port:
                  number: 80
          - path: /api/v2(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: api-v2-service
                port:
                  number: 80
          # 静态资源路由
          - path: /static(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: static-service
                port:
                  number: 80
          # 健康检查路由
          - path: /healthz
            pathType: Exact
            backend:
              service:
                name: health-service
                port:
                  number: 8080
```

#### 1.2 基于Header的路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: header-based-routing
  namespace: ingress-prod
  annotations:
    # 基于User-Agent的路由
    nginx.ingress.kubernetes.io/configuration-snippet: |
      if ($http_user_agent ~* "(mobile|android|iphone)") {
        set $proxy_upstream_name "mobile-backend-service-80";
      }
      if ($http_user_agent ~* "(bot|crawler|spider)") {
        set $proxy_upstream_name "bot-service-80";
      }
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
                name: default-service
                port:
                  number: 80
```

### 2. 安全加固配置

#### 2.1 TLS/SSL配置

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
  namespace: ingress-prod
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR2akNDQXFhZ0F3SUJBZ0lKQU5mNmZrVTV5dW1ITUEwR0NTcUdTSWIzRFFFQkN3VUFNRFF4Q3pBSkJnTlYKQkFZVEFsVlRNUXN3Q1FZRFZRUUlEQUpEUVRFZk1CMEdBMVVFQXd3WVNXNTBaWEp1WlhRZ1YybGtaMmwwYTNFZwpIaGNOTVRrd05ERXhNVGt3TkRRMldoY05NalF3TkRFeE1Ua3dORFEyV2pBZU1CNEdBMVVFQXd3WVNXNTBaWEp1ClpoUTNNQjRYRFRJeE1EZ3lOVEF5TXpFMU5Gb1hEVEl6TURneE5UQXlNekUxTkZvd2NERUxNQWtHQTFVRUJoTUMKVlZNeEV6QVJCZ05WQkFnTUNrTmhiR2xtYjNKdWFXRXdnZ0VpTUEwR0NTcUdTSWIzRFFFQkN3VUFBNElCQVFCCkFJdm9iMnhKZ2dKdW1qYkx5RzJxWk90c2hYRk55cGZ5bHl1Rk91R05mZzB3a0l4VlB4Q05mTlZqM21yTlJ5c1UKVkhzZnR6N2hJN255V09rZjJ5aG94V0tKbG95dG5sR1Z3Rk12MzZkRjV2bU55V09rZjJ5aG94V0tKbG95dG5sRwpWM0Z1bTV2bU55V09rZjJ5aG94V0tKbG95dG5sR1Z3Rk12MzZkRjV2bU55V09rZjJ5aG94V0tKbG95dG5sR1Z3CkYzRnVtNXZtTnlXT2tmMnlobeC0KCg==
  tls.key: LS0tLS1CRUdJTiBSU0EgUFJJV

---

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-secured-ingress
  namespace: ingress-prod
  annotations:
    # TLS配置
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    # HSTS配置
    nginx.ingress.kubernetes.io/hsts: "true"
    nginx.ingress.kubernetes.io/hsts-max-age: "31536000"
    nginx.ingress.kubernetes.io/hsts-include-subdomains: "true"
    nginx.ingress.kubernetes.io/hsts-preload: "true"
    # 安全头部
    nginx.ingress.kubernetes.io/configuration-snippet: |
      more_set_headers "X-Frame-Options: DENY";
      more_set_headers "X-Content-Type-Options: nosniff";
      more_set_headers "X-XSS-Protection: 1; mode=block";
      more_set_headers "Strict-Transport-Security: max-age=31536000; includeSubDomains; preload";
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.company.com
        - app.company.com
      secretName: tls-secret
  rules:
    - host: api.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
    - host: app.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
```

#### 2.2 认证和授权

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: authenticated-ingress
  namespace: ingress-prod
  annotations:
    # Basic Auth配置
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: "Authentication Required - Company API"
    
    # JWT/OAuth2配置
    nginx.ingress.kubernetes.io/auth-url: "https://oauth2-proxy.ingress-prod.svc.cluster.local/oauth2/auth"
    nginx.ingress.kubernetes.io/auth-signin: "https://login.company.com/oauth2/start?rd=$escaped_request_uri"
    nginx.ingress.kubernetes.io/auth-response-headers: "x-auth-request-user,x-auth-request-email,x-auth-request-groups"
    
    # IP白名单
    nginx.ingress.kubernetes.io/whitelist-source-range: "192.168.1.0/24,10.0.0.0/8,172.16.0.0/12"
spec:
  ingressClassName: nginx
  rules:
    - host: secure-api.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: secure-api-service
                port:
                  number: 80
```

### 3. WAF和攻击防护

#### 3.1 ModSecurity配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: waf-protected-ingress
  namespace: ingress-prod
  annotations:
    # ModSecurity启用
    nginx.ingress.kubernetes.io/enable-modsecurity: "true"
    nginx.ingress.kubernetes.io/modsecurity-snippet: |
      SecRuleEngine On
      SecRequestBodyAccess On
      SecAuditEngine RelevantOnly
      SecAuditLogParts ABIJDEFHZ
      SecAuditLog /var/log/modsec_audit.log
      
      # SQL注入防护
      SecRule ARGS_NAMES "union.*select|insert.*into|select.*from" \
        "id:1001,phase:2,block,msg:'SQL Injection Attack Detected',logdata:'Matched Data: %{MATCHED_VAR}',severity:'CRITICAL'"
      
      # XSS防护
      SecRule ARGS_NAMES|ARGS|XML:/* "<script|javascript:|vbscript:|onload|onerror" \
        "id:1002,phase:2,block,msg:'Cross Site Scripting Attack Detected',logdata:'Matched Data: %{MATCHED_VAR}',severity:'HIGH'"
      
      # 文件包含防护
      SecRule ARGS_NAMES "(\.\./|\.\.\\)" \
        "id:1003,phase:2,block,msg:'Path Traversal Attack Detected',logdata:'Matched Data: %{MATCHED_VAR}',severity:'HIGH'"
      
      # 命令执行防护
      SecRule ARGS "|;|&&|cmd\.exe|powershell\.exe" \
        "id:1004,phase:2,block,msg:'Command Execution Attempt Detected',logdata:'Matched Data: %{MATCHED_VAR}',severity:'CRITICAL'"
spec:
  ingressClassName: nginx
  rules:
    - host: protected-api.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: protected-service
                port:
                  number: 80
```

### 4. 监控和告警配置

#### 4.1 Prometheus指标集成

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: monitored-ingress
  namespace: ingress-prod
  annotations:
    # Prometheus指标
    nginx.ingress.kubernetes.io/enable-access-log: "true"
    nginx.ingress.kubernetes.io/access-log-path: "/var/log/nginx/access.log"
    nginx.ingress.kubernetes.io/error-log-path: "/var/log/nginx/error.log"
    
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
    - host: metrics-api.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: metrics-service
                port:
                  number: 80
```

#### 4.2 ServiceMonitor配置

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ingress-nginx-monitor
  namespace: monitoring
  labels:
    app: ingress-nginx
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: ingress-nginx
  namespaceSelector:
    matchNames:
      - ingress-nginx
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
      scheme: http
      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_node_name]
          targetLabel: node
        - sourceLabels: [__meta_kubernetes_namespace]
          targetLabel: namespace
        - sourceLabels: [__meta_kubernetes_pod_name]
          targetLabel: pod
```

### 5. 高可用和性能优化

#### 5.1 负载均衡优化

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: optimized-ingress
  namespace: ingress-prod
  annotations:
    # 负载均衡算法
    nginx.ingress.kubernetes.io/upstream-hash-by: "$remote_addr"
    
    # 会话保持
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "ROUTE"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
    nginx.ingress.kubernetes.io/session-cookie-change-on-failure: "true"
    
    # 连接池优化
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "10"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-next-upstream: "error timeout invalid_header http_500 http_502 http_503 http_504"
    nginx.ingress.kubernetes.io/proxy-next-upstream-timeout: "10"
    nginx.ingress.kubernetes.io/proxy-next-upstream-tries: "3"
spec:
  ingressClassName: nginx
  rules:
    - host: high-available.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ha-service
                port:
                  number: 80
```

---

## 🏭 生产环境最佳实践

### 1. 多环境配置管理

```yaml
# 开发环境
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: dev-api-ingress
  namespace: dev
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
    nginx.ingress.kubernetes.io/rate-limit: "1000"
spec:
  ingressClassName: nginx
  rules:
    - host: api-dev.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80

---
# 生产环境
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: prod-api-ingress
  namespace: prod
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/limit-connections: "1000"
    nginx.ingress.kubernetes.io/hsts: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.company.com
      secretName: prod-tls-secret
  rules:
    - host: api.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

### 2. 蓝绿部署配置

```yaml
# 蓝色环境
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: blue-ingress
  namespace: ingress-prod
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
                name: app-blue-service
                port:
                  number: 80

---
# 绿色环境
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: green-ingress
  namespace: ingress-prod
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
                name: app-green-service
                port:
                  number: 80

---
# 主入口（初始指向蓝色）
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  namespace: ingress-prod
  annotations:
    nginx.ingress.kubernetes.io/canary: "false"
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
                name: app-blue-service
                port:
                  number: 80
```

### 3. 金丝雀发布策略

```yaml
# 稳定版本
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: stable-ingress
  namespace: ingress-prod
spec:
  ingressClassName: nginx
  rules:
    - host: canary.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-stable-service
                port:
                  number: 80

---
# 金丝雀版本
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: canary-ingress
  namespace: ingress-prod
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "20"
    # 或基于header路由
    # nginx.ingress.kubernetes.io/canary-by-header: "X-Canary"
    # nginx.ingress.kubernetes.io/canary-by-header-value: "always"
    # 或基于cookie路由
    # nginx.ingress.kubernetes.io/canary-by-cookie: "canary"
spec:
  ingressClassName: nginx
  rules:
    - host: canary.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-canary-service
                port:
                  number: 80
```

---

## 🚨 常见问题和解决方案

### 1. Ingress路由不生效

**问题现象**: 404 Not Found 或路由未按预期工作

**诊断步骤**:
```bash
# 1. 检查Ingress状态
kubectl get ingress -n ingress-prod

# 2. 查看Ingress详细信息
kubectl describe ingress <ingress-name> -n ingress-prod

# 3. 检查Ingress Controller日志
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# 4. 验证Service和Endpoints
kubectl get services -n ingress-prod
kubectl get endpoints -n ingress-prod

# 5. 测试DNS解析
nslookup company.com
```

**解决方案**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fixed-ingress
  namespace: ingress-prod
  annotations:
    # 确保路径匹配正确
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx  # 确保指定正确的IngressClass
  rules:
    - host: company.com
      http:
        paths:
          - path: /api(/|$)(.*)  # 使用正确的正则表达式
            pathType: ImplementationSpecific
            backend:
              service:
                name: api-service  # 确保Service名称正确
                port:
                  number: 80
```

### 2. TLS证书问题

**问题现象**: SSL证书错误或HTTPS访问失败

**解决方案**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-fixed-ingress
  namespace: ingress-prod
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - company.com
        - www.company.com
      secretName: company-tls  # 确保证书Secret存在
  rules:
    - host: company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
---
# 创建证书Secret
apiVersion: v1
kind: Secret
metadata:
  name: company-tls
  namespace: ingress-prod
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-certificate>
  tls.key: <base64-encoded-private-key>
```

### 3. 性能瓶颈

**问题现象**: 响应慢、超时、连接数过多

**解决方案**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: performance-optimized-ingress
  namespace: ingress-prod
  annotations:
    # 连接优化
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "5"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    
    # 缓冲区优化
    nginx.ingress.kubernetes.io/proxy-buffering: "on"
    nginx.ingress.kubernetes.io/proxy-buffer-size: "4k"
    nginx.ingress.kubernetes.io/proxy-buffers-number: "8"
    
    # 限流配置
    nginx.ingress.kubernetes.io/rate-limit: "1000"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/limit-connections: "1000"
    
    # 压缩配置
    nginx.ingress.kubernetes.io/configuration-snippet: |
      gzip on;
      gzip_vary on;
      gzip_min_length 1024;
      gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
spec:
  ingressClassName: nginx
  rules:
    - host: high-performance.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: optimized-service
                port:
                  number: 80
```

---

## 📊 监控告警配置

### 1. 关键指标监控

```yaml
# Prometheus告警规则
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ingress-alerts
  namespace: monitoring
spec:
  groups:
    - name: ingress.rules
      rules:
        # 高错误率告警
        - alert: IngressHighErrorRate
          expr: rate(nginx_ingress_controller_requests{status=~"5.."}[5m]) / rate(nginx_ingress_controller_requests[5m]) > 0.05
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High error rate in Ingress controller"
            description: "{{ $labels.controller }} has error rate of {{ printf \"%.2f\" $value }}%"
        
        # 高延迟告警
        - alert: IngressHighLatency
          expr: histogram_quantile(0.95, rate(nginx_ingress_controller_request_duration_seconds_bucket[5m])) > 2
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High latency in Ingress controller"
            description: "{{ $labels.controller }} has 95th percentile latency of {{ printf \"%.2f\" $value }}s"
        
        # 高连接数告警
        - alert: IngressHighConnections
          expr: nginx_ingress_controller_nginx_process_connections{state="active"} > 10000
          for: 2m
          labels:
            severity: warning
          annotations:
            summary: "High active connections in Ingress controller"
            description: "{{ $labels.controller }} has {{ $value }} active connections"
```

### 2. 日志分析配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/nginx/access.log
      pos_file /var/log/fluentd-nginx.pos
      tag nginx.access
      <parse>
        @type regexp
        expression /^(?<remote>[^ ]*) (?<host>[^ ]*) (?<user>[^ ]*) \[(?<time>[^\]]*)\] "(?<method>\S+)(?: +(?<path>[^\"]*?)(?: +\S*)?)?" (?<code>[^ ]*) (?<size>[^ ]*)(?: "(?<referer>[^\"]*)" "(?<agent>[^\"]*)"(?:\s+(?<http_x_forwarded_for>[^ ]+))?)?$/
        time_format %d/%b/%Y:%H:%M:%S %z
      </parse>
    </source>
    
    <filter nginx.access>
      @type record_transformer
      <record>
        hostname ${hostname}
        service ingress-nginx
      </record>
    </filter>
    
    <match nginx.access>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      logstash_format true
      logstash_prefix nginx-access
    </match>
```

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes Ingress官方文档](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [NGINX Ingress Controller文档](https://kubernetes.github.io/ingress-nginx/)
- [Traefik Ingress Controller](https://doc.traefik.io/traefik/providers/kubernetes-ingress/)

### 相关案例
- [Service完整体系](../service-complete-demo/)
- [Service和Ingress集成](../service-ingress-integration-demo/)
- [Ingress安全配置](../../ingress/ingress-security/)

### 进阶主题
- Service Mesh集成（Istio Gateway、Ambient Mesh）
- 多集群Ingress管理
- 边缘计算网关部署
- AI驱动的流量治理

---

## 🧪 实践练习

### 练习1：生产级Ingress部署
配置完整的Ingress Controller，实现TLS加密、认证授权和监控告警。

### 练习2：安全加固实践
为Ingress配置WAF防护、速率限制和IP白名单等安全措施。

### 练习3：蓝绿部署演练
实现完整的蓝绿部署流程，包括流量切换和回滚机制。

### 练习4：性能优化
通过调整Ingress配置和负载均衡策略，优化入口网关性能。

---

## 📋 清理资源

```bash
# 删除生产环境命名空间
kubectl delete namespace ingress-prod

# 删除Ingress Controller
helm uninstall ingress-nginx -n ingress-nginx
kubectl delete namespace ingress-nginx

# 或单独删除资源
kubectl delete ingress --all -n ingress-prod
kubectl delete svc --all -n ingress-prod
kubectl delete deploy --all -n ingress-prod
```

---

> **💡 提示**: 本案例提供了完整的Ingress生产级解决方案，建议结合实际业务场景进行定制化配置。定期审查和更新Ingress配置以适应业务发展需求。