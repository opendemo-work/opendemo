# 🌐 Kubernetes Service和Ingress集成演示

> Service和Ingress协同工作的完整生产级解决方案，展示企业级流量管理的最佳实践

## 📋 案例概述

本案例演示Service和Ingress在生产环境中的深度集成，涵盖从内部服务发现到外部流量管理的完整链路，提供企业级流量治理的最佳实践方案。

### 🔧 核心集成能力

- **服务发现与路由**: Service作为Ingress后端的完整链路
- **流量治理**: 负载均衡、金丝雀发布、蓝绿部署
- **安全管控**: 端到端安全策略、认证授权集成
- **监控告警**: 统一指标收集、链路追踪、性能分析
- **故障排查**: 全链路诊断、根因分析、快速恢复
- **自动化运维**: 配置管理、滚动更新、自动扩缩容

### 🎯 适用场景

- 微服务架构的完整流量治理
- 企业级API网关解决方案
- 多层次安全防护体系
- 高可用服务部署架构
- 智能化运维管理平台

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查集群状态
kubectl cluster-info
kubectl get nodes

# 创建集成演示命名空间
kubectl create namespace service-ingress-integration

# 验证必要的CRDs
kubectl get crds | grep -E "(ingresses|services)"
```

### 2. 部署基础组件

```bash
# 部署Service和Ingress控制器
kubectl apply -f integration-components.yaml -n service-ingress-integration

# 部署示例应用
kubectl apply -f sample-applications.yaml -n service-ingress-integration

# 验证部署状态
kubectl get pods,services,ingresses -n service-ingress-integration
```

---

## 📚 核心集成模式

### 1. 标准三层架构

```yaml
# 第一层：前端应用Service
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: service-ingress-integration
  labels:
    app: frontend
    tier: web
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
spec:
  selector:
    app: frontend
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: metrics
      protocol: TCP
      port: 8080
      targetPort: 8080
  type: ClusterIP

---
# 第二层：API网关Service
apiVersion: v1
kind: Service
metadata:
  name: api-gateway-service
  namespace: service-ingress-integration
  labels:
    app: api-gateway
    tier: gateway
spec:
  selector:
    app: api-gateway
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: https
      protocol: TCP
      port: 443
      targetPort: 8443
  type: ClusterIP

---
# 第三层：后端微服务Services
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: service-ingress-integration
  labels:
    app: user-service
    tier: backend
spec:
  selector:
    app: user-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: service-ingress-integration
  labels:
    app: order-service
    tier: backend
spec:
  selector:
    app: order-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP

---
# Ingress入口配置
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  namespace: service-ingress-integration
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-buffering: "on"
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - company.com
        - api.company.com
      secretName: company-tls
  rules:
    # 前端网站路由
    - host: company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
    
    # API网关路由
    - host: api.company.com
      http:
        paths:
          # 用户服务API
          - path: /api/users(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: user-service
                port:
                  number: 80
          
          # 订单服务API
          - path: /api/orders(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: order-service
                port:
                  number: 80
          
          # 网关管理API
          - path: /gateway(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: api-gateway-service
                port:
                  number: 80
```

### 2. 服务网格集成模式

```yaml
# 带Sidecar的服务配置
apiVersion: v1
kind: Service
metadata:
  name: mesh-enabled-service
  namespace: service-ingress-integration
  labels:
    app: mesh-app
    version: v1
  annotations:
    # Istio服务网格注解
    sidecar.istio.io/inject: "true"
    traffic.sidecar.istio.io/includeInboundPorts: "8080,8081"
spec:
  selector:
    app: mesh-app
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: grpc
      protocol: TCP
      port: 8081
      targetPort: 8081
  type: ClusterIP

---
# Ingress Gateway配置（Istio）
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: istio-gateway
  namespace: service-ingress-integration
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "*.company.com"
      tls:
        httpsRedirect: true
    - port:
        number: 443
        name: https
        protocol: HTTPS
      hosts:
        - "*.company.com"
      tls:
        mode: SIMPLE
        credentialName: company-tls

---
# VirtualService路由配置
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: mesh-routing
  namespace: service-ingress-integration
spec:
  hosts:
    - api.company.com
  gateways:
    - istio-gateway
  http:
    - match:
        - uri:
            prefix: /api/v1/users
      route:
        - destination:
            host: user-service
            port:
              number: 80
          weight: 100
    - match:
        - uri:
            prefix: /api/v1/orders
      route:
        - destination:
            host: order-service
            port:
              number: 80
          weight: 90
        - destination:
            host: order-service-canary
            port:
              number: 80
          weight: 10
```

### 3. 多租户隔离模式

```yaml
# 租户A服务配置
apiVersion: v1
kind: Service
metadata:
  name: tenant-a-web
  namespace: tenant-a
  labels:
    app: web
    tenant: a
spec:
  selector:
    app: web
    tenant: a
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP

---
# 租户B服务配置
apiVersion: v1
kind: Service
metadata:
  name: tenant-b-web
  namespace: tenant-b
  labels:
    app: web
    tenant: b
spec:
  selector:
    app: web
    tenant: b
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP

---
# 多租户Ingress配置
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-tenant-ingress
  namespace: service-ingress-integration
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    # 租户隔离配置
    nginx.ingress.kubernetes.io/configuration-snippet: |
      set $tenant "";
      if ($http_host ~* "^([^\.]+)\.company\.com$") {
        set $tenant $1;
      }
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - "*.company.com"
      secretName: wildcard-tls
  rules:
    # 租户A路由
    - host: tenant-a.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: tenant-a-web
                port:
                  number: 80
                namespace: tenant-a  # 跨命名空间引用
    
    # 租户B路由
    - host: tenant-b.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: tenant-b-web
                port:
                  number: 80
                namespace: tenant-b
```

### 4. 智能路由和负载均衡

```yaml
# 带权重的服务配置
apiVersion: v1
kind: Service
metadata:
  name: main-service
  namespace: service-ingress-integration
  annotations:
    # 负载均衡策略
    service.alpha.kubernetes.io/topology-aware-hints: "auto"
spec:
  selector:
    app: main-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP

---
# 金丝雀版本服务
apiVersion: v1
kind: Service
metadata:
  name: canary-service
  namespace: service-ingress-integration
  labels:
    app: main-app
    version: canary
spec:
  selector:
    app: main-app
    version: canary
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP

---
# 智能Ingress路由
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: smart-routing
  namespace: service-ingress-integration
  annotations:
    # 基于Header的路由
    nginx.ingress.kubernetes.io/configuration-snippet: |
      set $target_service "main-service";
      if ($http_x_version = "canary") {
        set $target_service "canary-service";
      }
      if ($http_user_agent ~* "bot|crawler") {
        set $target_service "bot-service";
      }
    
    # 速率限制
    nginx.ingress.kubernetes.io/rate-limit: "1000"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    
    # 连接限制
    nginx.ingress.kubernetes.io/limit-connections: "1000"
spec:
  ingressClassName: nginx
  rules:
    - host: smart.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: main-service  # 默认路由到主服务
                port:
                  number: 80
```

---

## 🔧 高级集成特性

### 1. 统一监控体系

```yaml
# 带监控注解的Service
apiVersion: v1
kind: Service
metadata:
  name: monitored-service
  namespace: service-ingress-integration
  labels:
    app: business-app
  annotations:
    # Prometheus监控
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
    
    # OpenTelemetry追踪
    instrumentation.opentelemetry.io/inject-sdk: "true"
    
    # 自定义指标标签
    metrics.custom/team: "backend"
    metrics.custom/environment: "production"
spec:
  selector:
    app: business-app
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: metrics
      protocol: TCP
      port: 9090
      targetPort: 9090

---
# 统一日志收集
apiVersion: v1
kind: Service
metadata:
  name: logging-service
  namespace: service-ingress-integration
  annotations:
    # Fluentd日志配置
    fluentdConfiguration: |
      <source>
        @type tail
        path /var/log/containers/*_service-ingress-integration_*.log
        tag kubernetes.*
        <parse>
          @type json
        </parse>
      </source>
spec:
  selector:
    app: log-collector
  ports:
    - protocol: TCP
      port: 24224
      targetPort: 24224
```

### 2. 安全集成策略

```yaml
# 带网络策略的Service
apiVersion: v1
kind: Service
metadata:
  name: secure-service
  namespace: service-ingress-integration
spec:
  selector:
    app: secure-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: secure-service-policy
  namespace: service-ingress-integration
spec:
  podSelector:
    matchLabels:
      app: secure-app
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # 仅允许来自Ingress控制器的流量
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
          podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
    # 允许监控系统访问
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 8080

---
# 安全Ingress配置
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
  namespace: service-ingress-integration
  annotations:
    # WAF防护
    nginx.ingress.kubernetes.io/enable-modsecurity: "true"
    nginx.ingress.kubernetes.io/modsecurity-snippet: |
      SecRuleEngine On
      SecRequestBodyAccess On
      
    # 认证集成
    nginx.ingress.kubernetes.io/auth-url: "https://oauth2-proxy.service-ingress-integration.svc.cluster.local/oauth2/auth"
    nginx.ingress.kubernetes.io/auth-signin: "https://login.company.com/oauth2/start?rd=$escaped_request_uri"
    
    # IP白名单
    nginx.ingress.kubernetes.io/whitelist-source-range: "203.0.113.0/24,198.51.100.0/24"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - secure.company.com
      secretName: secure-tls
  rules:
    - host: secure.company.com
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

### 3. 自动扩缩容集成

```yaml
# 带HPA的服务配置
apiVersion: v1
kind: Service
metadata:
  name: autoscale-service
  namespace: service-ingress-integration
spec:
  selector:
    app: autoscale-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: autoscale-app
  namespace: service-ingress-integration
spec:
  replicas: 3
  selector:
    matchLabels:
      app: autoscale-app
  template:
    metadata:
      labels:
        app: autoscale-app
    spec:
      containers:
        - name: app
          image: company/autoscale-app:v1.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "200m"
---
# HorizontalPodAutoscaler配置
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: autoscale-hpa
  namespace: service-ingress-integration
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: autoscale-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
---
# 基于Ingress指标的扩缩容
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ingress-based-hpa
  namespace: service-ingress-integration
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: autoscale-app
  minReplicas: 1
  maxReplicas: 20
  metrics:
    - type: Object
      object:
        metric:
          name: nginx_ingress_controller_requests
        describedObject:
          apiVersion: networking.k8s.io/v1
          kind: Ingress
          name: main-ingress
        target:
          type: Value
          value: "10000"  # 基于总请求数扩缩容
```

---

## 🚨 故障排查和诊断

### 1. 全链路诊断脚本

```bash
#!/bin/bash
# Service-Ingress Integration Diagnostic Script

NAMESPACE="service-ingress-integration"

echo "🔧 Service-Ingress Integration Diagnostic"
echo "========================================"

# 1. 基础资源状态检查
echo "📋 1. 基础资源状态检查"
echo "Services:"
kubectl get services -n $NAMESPACE -o wide
echo ""
echo "Ingresses:"
kubectl get ingress -n $NAMESPACE -o wide
echo ""
echo "Pods:"
kubectl get pods -n $NAMESPACE -o wide

# 2. 网络连通性测试
echo ""
echo "🌐 2. 网络连通性测试"
for svc in $(kubectl get services -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "Testing service: $svc"
    kubectl run debug-$svc --image=busybox --rm -it -n $NAMESPACE -- \
        wget -qO- --timeout=5 http://$svc.$NAMESPACE.svc.cluster.local 2>&1 || echo "Failed to connect to $svc"
    echo ""
done

# 3. Ingress控制器状态
echo "⚙️ 3. Ingress控制器状态"
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --tail=50

# 4. 端到端测试
echo ""
echo "🔌 4. 端到端连通性测试"
INGRESS_IP=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
if [ ! -z "$INGRESS_IP" ]; then
    for host in $(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].spec.rules[*].host}'); do
        echo "Testing $host -> $INGRESS_IP"
        curl -H "Host: $host" -s -w "HTTP Code: %{http_code}\nTime: %{time_total}s\n" http://$INGRESS_IP/ 2>/dev/null || echo "Failed"
        echo ""
    done
else
    echo "⚠️  No external IP found for Ingress Controller"
fi

# 5. 性能指标检查
echo "📈 5. 性能指标检查"
echo "Service endpoints:"
kubectl get endpoints -n $NAMESPACE
echo ""
echo "Ingress metrics:"
kubectl exec -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx -- \
    curl -s http://localhost:10254/metrics | grep nginx_ingress_controller_requests || echo "Metrics not available"

echo ""
echo "✅ 诊断完成，请根据以上输出检查问题根源"
```

### 2. 常见问题解决方案

#### 问题1：Service无法通过Ingress访问

```yaml
# 诊断和修复步骤
apiVersion: v1
kind: Service
metadata:
  name: fixed-service
  namespace: service-ingress-integration
  annotations:
    # 确保正确的端口映射
    service.alpha.kubernetes.io/tolerate-unready-endpoints: "true"
spec:
  selector:
    app: fixed-app  # 确保标签选择器正确
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080  # 确保目标端口正确
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fixed-ingress
  namespace: service-ingress-integration
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /  # 简化重写规则
spec:
  ingressClassName: nginx
  rules:
    - host: fixed.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: fixed-service  # 确保服务名称正确
                port:
                  number: 80
```

#### 问题2：负载不均衡

```yaml
# 优化负载均衡配置
apiVersion: v1
kind: Service
metadata:
  name: balanced-service
  namespace: service-ingress-integration
  annotations:
    # 启用拓扑感知负载均衡
    service.kubernetes.io/topology-aware-hints: "auto"
spec:
  selector:
    app: balanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  sessionAffinity: None  # 禁用会话亲和性以实现更好负载均衡

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: balanced-ingress
  namespace: service-ingress-integration
  annotations:
    # 负载均衡算法优化
    nginx.ingress.kubernetes.io/upstream-hash-by: "$remote_addr"
    nginx.ingress.kubernetes.io/proxy-next-upstream: "error timeout invalid_header http_500 http_502 http_503 http_504"
spec:
  ingressClassName: nginx
  rules:
    - host: balanced.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: balanced-service
                port:
                  number: 80
```

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes Service文档](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Kubernetes Ingress文档](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Service Mesh集成指南](https://istio.io/latest/docs/setup/addons/)

### 相关案例
- [Service完整体系](../service/service-complete-demo/)
- [Ingress完整体系](../ingress/ingress-complete-demo/)
- [网络策略管理](../../network/)

### 进阶主题
- 多集群Service发现
- 边缘计算网关联动
- AI驱动的流量调度
- 零信任网络架构

---

## 🧪 实践练习

### 练习1：完整链路部署
部署从前端到后端的完整服务链路，配置相应的Ingress路由规则。

### 练习2：安全集成实践
为服务链路配置端到端的安全策略，包括网络策略、认证授权和WAF防护。

### 练习3：智能路由演练
实现基于用户特征的智能路由，包括金丝雀发布和A/B测试。

### 练习4：故障诊断实训
模拟各种故障场景，练习使用诊断工具进行根因分析和问题解决。

---

## 📋 清理资源

```bash
# 删除集成演示命名空间
kubectl delete namespace service-ingress-integration

# 删除相关组件
kubectl delete namespace ingress-nginx
kubectl delete crd virtualservices.networking.istio.io
kubectl delete crd gateways.networking.istio.io
```

---

> **💡 提示**: 本案例展示了Service和Ingress的深度集成模式，建议根据实际业务需求选择合适的集成方案。定期评估和优化集成配置以适应业务发展。