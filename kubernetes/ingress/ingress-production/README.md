# 🏭 Kubernetes Ingress生产环境最佳实践

> 企业级Kubernetes Ingress部署、运维和优化的完整指南，涵盖高可用、性能调优、监控告警等关键生产要素

## 📋 案例概述

本案例汇集了Kubernetes Ingress在生产环境中的最佳实践，帮助您构建稳定、高效、可扩展的外部访问入口。

### 🔧 核心技能点

- **高可用架构**: 多实例部署、故障自愈
- **性能优化**: 负载均衡调优、缓存策略
- **监控告警**: 全方位指标收集、智能告警
- **灾备恢复**: 多集群备份、快速恢复
- **成本优化**: 资源配额管理、成本控制

### 🎯 适用人群

- 企业架构师
- SRE工程师
- 运维团队负责人
- 技术管理者

---

## 🚀 快速开始

### 1. 生产环境准备

```bash
# 创建生产命名空间
kubectl create namespace ingress-production

# 应用生产环境标签
kubectl label namespace ingress-production environment=production tier=critical
```

### 2. 高可用控制器部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ingress-nginx-controller
  namespace: ingress-production
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: ingress-nginx
      app.kubernetes.io/instance: ingress-nginx
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/instance: ingress-nginx
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app.kubernetes.io/name
                  operator: In
                  values:
                  - ingress-nginx
              topologyKey: kubernetes.io/hostname
      containers:
      - name: controller
        image: k8s.gcr.io/ingress-nginx/controller:v1.8.1
        ports:
        - name: http
          containerPort: 80
        - name: https
          containerPort: 443
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        resources:
          requests:
            cpu: "100m"
            memory: "90Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
```

---

## 📚 详细教程

### 1. 高可用配置

#### 1.1 多实例部署

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ingress-nginx-controller
  namespace: ingress-production
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
      targetPort: 80
      protocol: TCP
    - name: https
      port: 443
      targetPort: 443
      protocol: TCP
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
```

#### 1.2 健康检查配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: health-check-ingress
  namespace: ingress-production
  annotations:
    nginx.ingress.kubernetes.io/custom-http-errors: "404,500,502,503"
spec:
  ingressClassName: nginx
  rules:
  - host: health.example.com
    http:
      paths:
      - path: /healthz
        pathType: Prefix
        backend:
          service:
            name: health-service
            port:
              number: 80
```

### 2. 性能优化

#### 2.1 连接优化

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configuration
  namespace: ingress-production
data:
  proxy-connect-timeout: "10"
  proxy-send-timeout: "300"
  proxy-read-timeout: "300"
  proxy-body-size: "50m"
  proxy-buffer-size: "4k"
  proxy-buffers-number: "8"
  enable-brotli: "true"
  brotli-level: "6"
  brotli-types: "text/html text/css application/javascript application/json"
```

#### 2.2 缓存策略

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: caching-ingress
  namespace: ingress-production
  annotations:
    nginx.ingress.kubernetes.io/configuration-snippet: |
      location / {
        proxy_cache static_cache;
        proxy_cache_valid 200 302 1h;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_lock on;
        add_header X-Cache-Status $upstream_cache_status;
      }
spec:
  ingressClassName: nginx
  rules:
  - host: cache.example.com
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

### 练习1：高可用架构部署
配置三实例的Ingress控制器高可用架构。

### 练习2：性能调优实践
对Ingress进行压力测试并实施性能优化措施。

### 练习3：监控告警配置
建立完整的监控告警体系。

---

## 📋 清理资源

```bash
kubectl delete namespace ingress-production
```