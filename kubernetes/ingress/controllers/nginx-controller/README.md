# 🚀 NGINX Ingress Controller 生产级部署

> 企业级 NGINX Ingress Controller 部署、配置和管理完整指南

## 📋 案例概述

本案例提供 NGINX Ingress Controller 的生产级部署方案，涵盖从基础安装到高级配置的完整实践，确保在生产环境中能够稳定、高效地运行。

### 🔧 核心能力覆盖

- **多环境部署**: 支持云环境、裸金属、混合云部署
- **高可用配置**: 主备部署、自动故障转移、负载均衡
- **性能优化**: 连接池优化、缓存配置、资源限制
- **安全加固**: TLS配置、访问控制、WAF集成
- **监控告警**: Prometheus指标、日志收集、健康检查
- **运维管理**: 滚动升级、配置热更新、故障排查

### 🎯 适用场景

- 企业级生产环境
- 高并发Web应用
- 微服务架构网关
- 多租户环境
- 混合云部署

---

## 🚀 快速部署

### 1. 环境准备

```bash
# 检查Kubernetes集群状态
kubectl cluster-info
kubectl get nodes

# 创建专用命名空间
kubectl create namespace ingress-system

# 验证Helm版本
helm version
```

### 2. 生产级部署配置

```bash
# 添加Helm仓库
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# 生产级部署命令
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-system \
  --version 4.8.3 \
  --set controller.replicaCount=3 \
  --set controller.service.type=LoadBalancer \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"="nlb" \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-cross-zone-load-balancing-enabled"="true" \
  --set controller.config.use-forwarded-headers=true \
  --set controller.config.compute-full-forwarded-for=true \
  --set controller.config.use-proxy-protocol=false \
  --set controller.metrics.enabled=true \
  --set controller.metrics.serviceMonitor.enabled=true \
  --set controller.resources.requests.cpu=200m \
  --set controller.resources.requests.memory=256Mi \
  --set controller.resources.limits.cpu=1000m \
  --set controller.resources.limits.memory=1Gi \
  --set controller.autoscaling.enabled=true \
  --set controller.autoscaling.minReplicas=3 \
  --set controller.autoscaling.maxReplicas=10 \
  --set controller.autoscaling.targetCPUUtilizationPercentage=80 \
  --set controller.autoscaling.targetMemoryUtilizationPercentage=80 \
  --set controller.podAnnotations."prometheus\.io/scrape"="true" \
  --set controller.podAnnotations."prometheus\.io/port"="10254" \
  --wait --timeout 600s
```

### 3. 验证部署

```bash
# 检查控制器状态
kubectl get pods -n ingress-system -l app.kubernetes.io/name=ingress-nginx
kubectl get svc -n ingress-system

# 验证外部IP
kubectl get svc ingress-nginx-controller -n ingress-system

# 检查版本信息
kubectl exec -n ingress-system deploy/ingress-nginx-controller -- /nginx-ingress-controller --version
```

---

## 📚 核心配置详解

### 1. ConfigMap 高级配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configuration
  namespace: ingress-system
data:
  # 基础性能配置
  use-forwarded-headers: "true"
  compute-full-forwarded-for: "true"
  proxy-real-ip-cidr: "0.0.0.0/0"
  
  # 连接优化
  keep-alive: "120"
  keep-alive-requests: "10000"
  proxy-connect-timeout: "10"
  proxy-send-timeout: "60"
  proxy-read-timeout: "60"
  
  # 缓存配置
  proxy-buffering: "on"
  proxy-buffer-size: "4k"
  proxy-buffers-number: "8"
  proxy-busy-buffers-size: "8k"
  
  # 安全配置
  ssl-protocols: "TLSv1.2 TLSv1.3"
  ssl-ciphers: "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384"
  ssl-prefer-server-ciphers: "false"
  
  # 日志配置
  log-format-upstream: '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_length $request_time [$proxy_upstream_name] $upstream_addr $upstream_response_length $upstream_response_time $upstream_status $req_id'
  
  # 自定义错误页面
  custom-http-errors: "404,500,502,503,504"
  
  # 启用压缩
  enable-brotli: "true"
  brotli-level: "6"
  brotli-types: "text/html text/css application/json application/javascript"
```

### 2. 多控制器部署

```yaml
# 区域控制器配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ingress-nginx-us-west
  namespace: ingress-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ingress-nginx
      region: us-west
  template:
    metadata:
      labels:
        app: ingress-nginx
        region: us-west
    spec:
      containers:
        - name: controller
          image: registry.k8s.io/ingress-nginx/controller:v1.9.4
          args:
            - /nginx-ingress-controller
            - --configmap=$(POD_NAMESPACE)/nginx-configuration
            - --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
            - --udp-services-configmap=$(POD_NAMESPACE)/udp-services
            - --publish-service=$(POD_NAMESPACE)/ingress-nginx-controller
            - --election-id=ingress-controller-leader-us-west
            - --ingress-class=nginx-us-west
            - --annotations-prefix=nginx.ingress.kubernetes.io
```

### 3. 蓝绿部署配置

```yaml
# 蓝色控制器
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ingress-nginx-blue
  namespace: ingress-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ingress-nginx
      color: blue
  template:
    metadata:
      labels:
        app: ingress-nginx
        color: blue
    spec:
      containers:
        - name: controller
          image: registry.k8s.io/ingress-nginx/controller:v1.9.4
          ports:
            - name: http
              containerPort: 80
            - name: https
              containerPort: 443
          livenessProbe:
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
          readinessProbe:
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 1Gi
---
# 绿色控制器
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ingress-nginx-green
  namespace: ingress-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ingress-nginx
      color: green
  template:
    metadata:
      labels:
        app: ingress-nginx
        color: green
    spec:
      containers:
        - name: controller
          image: registry.k8s.io/ingress-nginx/controller:v1.10.0  # 新版本
          # 其余配置同蓝色控制器
```

---

## 🔧 高级特性配置

### 1. 自定义模板

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-template
  namespace: ingress-system
data:
  nginx.tmpl: |
    # Custom NGINX template
    events {
        worker_connections 1024;
        use epoll;
        multi_accept on;
    }
    
    http {
        # 基础配置
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        
        # 自定义配置
        map $http_upgrade $connection_upgrade {
            default upgrade;
            '' close;
        }
        
        # 上游服务器配置
        upstream default_backend {
            server 127.0.0.1:8181 max_fails=3 fail_timeout=10s;
        }
        
        # 服务器块
        server {
            listen 80 default_server;
            listen [::]:80 default_server;
            
            location / {
                proxy_pass http://default_backend;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }
        }
    }
```

### 2. TCP/UDP 服务配置

```yaml
# TCP服务配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: tcp-services
  namespace: ingress-system
data:
  9000: "default/my-tcp-service:9000"
  9443: "default/my-tcp-service:9443"

---
# UDP服务配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: udp-services
  namespace: ingress-system
data:
  53: "kube-system/kube-dns:53"
```

### 3. 自定义注解

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: custom-annotations
  namespace: default
  annotations:
    # 自定义配置
    nginx.ingress.kubernetes.io/configuration-snippet: |
      more_set_headers "Server: MyCustomServer";
      more_set_headers "X-Frame-Options: DENY";
      
    # 客户端证书验证
    nginx.ingress.kubernetes.io/auth-tls-secret: "default/client-cert-secret"
    nginx.ingress.kubernetes.io/auth-tls-verify-client: "optional"
    
    # 自定义日志格式
    nginx.ingress.kubernetes.io/log-format-escape-json: "true"
    
    # 连接限制
    nginx.ingress.kubernetes.io/connection-proxy-header: "Connection"
```

---

## 🛡️ 安全配置

### 1. TLS配置

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
  namespace: ingress-system
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t...
  tls.key: LS0tLS1CRUdJTiBSU0EgUFJJV...

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/hsts: "true"
    nginx.ingress.kubernetes.io/hsts-max-age: "31536000"
spec:
  tls:
    - hosts:
        - example.com
      secretName: tls-secret
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```

### 2. 访问控制

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: access-controlled-ingress
  namespace: default
  annotations:
    # IP白名单
    nginx.ingress.kubernetes.io/whitelist-source-range: "192.168.1.0/24,10.0.0.0/8"
    
    # 基本认证
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: "Authentication Required"
spec:
  rules:
    - host: secure.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: secure-service
                port:
                  number: 80
```

---

## 📊 监控和告警

### 1. Prometheus监控

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
      - ingress-system
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

### 2. 告警规则

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ingress-nginx-alerts
  namespace: monitoring
spec:
  groups:
    - name: ingress-nginx.rules
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
        
        # 控制器不可用告警
        - alert: IngressControllerDown
          expr: absent(up{job="ingress-nginx"})
          for: 2m
          labels:
            severity: critical
          annotations:
            summary: "Ingress controller is down"
            description: "No Ingress controller instances are running"
```

---

## 🚨 故障排查

### 1. 常见问题诊断

```bash
# 1. 检查控制器状态
kubectl get pods -n ingress-system -l app.kubernetes.io/name=ingress-nginx

# 2. 查看控制器日志
kubectl logs -n ingress-system -l app.kubernetes.io/name=ingress-nginx --tail=100

# 3. 检查配置是否正确加载
kubectl exec -n ingress-system deploy/ingress-nginx-controller -- cat /etc/nginx/nginx.conf

# 4. 验证服务状态
kubectl get svc -n ingress-system
kubectl describe svc ingress-nginx-controller -n ingress-system

# 5. 测试外部访问
curl -v http://<external-ip>
```

### 2. 性能调优

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-performance-tuning
  namespace: ingress-system
data:
  # 工作进程优化
  worker-processes: "auto"
  worker-cpu-affinity: "auto"
  worker-shutdown-timeout: "240s"
  
  # 连接处理优化
  max-worker-connections: "16384"
  enable-underscores-in-headers: "true"
  
  # 缓冲区优化
  large-client-header-buffers: "4 32k"
  client-header-buffer-size: "32k"
  
  # 超时配置
  client-body-timeout: "120"
  client-header-timeout: "120"
  send-timeout: "120"
  
  # 限流配置
  limit-req-status-code: "429"
  limit-conn-status-code: "429"
```

---

## 📚 扩展阅读

### 官方文档
- [NGINX Ingress Controller官方文档](https://kubernetes.github.io/ingress-nginx/)
- [Kubernetes Ingress资源文档](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Helm Chart文档](https://artifacthub.io/packages/helm/ingress-nginx/ingress-nginx)

### 相关案例
- [Ingress路由策略](../routing-strategies/)
- [Ingress安全加固](../security-hardening/)
- [Ingress监控运维](../monitoring-operations/)

### 进阶主题
- 多集群Ingress管理
- Service Mesh集成
- 边缘计算网关部署
- AI驱动的流量调度

---

## 🧪 实践练习

### 练习1：生产级部署
按照生产级配置部署NGINX Ingress Controller，并验证各项功能。

### 练习2：性能调优
通过调整配置参数优化Ingress Controller的性能表现。

### 练习3：故障模拟
模拟各种故障场景，练习故障诊断和恢复技能。

### 练习4：版本升级
实践Ingress Controller的滚动升级和回滚操作。

---

## 📋 清理资源

```bash
# 删除Ingress Controller
helm uninstall ingress-nginx -n ingress-system

# 删除命名空间
kubectl delete namespace ingress-system

# 清理相关资源
kubectl delete crd ingressclasses.networking.k8s.io
kubectl delete clusterrolebinding nginx-ingress-clusterrole-nisa-binding
```

---

> **💡 提示**: NGINX Ingress Controller是Kubernetes生态系统中最流行的Ingress解决方案，合理的配置和监控对于生产环境的稳定性至关重要。