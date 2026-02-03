# 🚀 Kubernetes Service 高级特性完整指南

> 企业级 Service 高级功能、自定义配置和扩展开发完整解决方案

## 📋 案例概述

本案例提供 Kubernetes Service 高级特性的完整实践体系，涵盖从自定义资源配置到服务网格集成的全方位内容，帮助企业充分利用 Service 的高级功能实现复杂的业务需求。

### 🔧 核心能力覆盖

- **自定义资源配置**: EndpointSlice、Service Topology
- **高级负载均衡**: 自定义算法、会话保持、权重分配
- **服务网格集成**: Istio、Linkerd、Consul Connect
- **多集群服务**: 跨集群服务发现、联邦服务
- **扩展开发**: 自定义控制器、CRD开发、插件机制
- **性能优化**: 连接池、缓存策略、资源调优

### 🎯 适用场景

- 复杂微服务架构
- 多集群环境管理
- 服务网格集成项目
- 高性能服务部署
- 自定义业务需求

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查Kubernetes版本（需要1.21+）
kubectl version

# 验证EndpointSlice API
kubectl get crds | grep endpointslices

# 创建演示命名空间
kubectl create namespace service-advanced
```

### 2. 基础验证

```bash
# 检查现有服务状态
kubectl get services --all-namespaces

# 验证EndpointSlice功能
kubectl get endpointslices --all-namespaces
```

---

## 📚 核心高级特性

### 1. EndpointSlice 高级配置

#### 1.1 自定义EndpointSlice

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: custom-endpoints
  namespace: service-advanced
  labels:
    kubernetes.io/service-name: advanced-service
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 8080
endpoints:
  - addresses:
      - "10.244.1.10"
    conditions:
      ready: true
      serving: true
      terminating: false
    hostname: backend-v1
    nodeName: worker-1
    zone: us-west-1a
    hints:
      forZones:
        - name: us-west-1a
  - addresses:
      - "10.244.2.15"
    conditions:
      ready: true
      serving: true
      terminating: false
    hostname: backend-v2
    nodeName: worker-2
    zone: us-west-1b
    hints:
      forZones:
        - name: us-west-1b
```

#### 1.2 拓扑感知路由

```yaml
apiVersion: v1
kind: Service
metadata:
  name: topology-aware-service
  namespace: service-advanced
  annotations:
    service.kubernetes.io/topology-aware-hints: "auto"
spec:
  selector:
    app: topology-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

### 2. 自定义负载均衡策略

#### 2.1 基于权重的负载均衡

```yaml
apiVersion: v1
kind: Service
metadata:
  name: weighted-service
  namespace: service-advanced
spec:
  selector:
    app: weighted-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
---
# 通过EndpointSlice实现权重分配
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: weighted-endpoints-v1
  namespace: service-advanced
  labels:
    kubernetes.io/service-name: weighted-service
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 8080
endpoints:
  - addresses: ["10.244.1.10"]
    conditions:
      ready: true
    # 通过创建多个相同的endpoint实现权重
---
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: weighted-endpoints-v2
  namespace: service-advanced
  labels:
    kubernetes.io/service-name: weighted-service
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 8080
endpoints:
  - addresses: ["10.244.2.15"]
    conditions:
      ready: true
```

#### 2.2 自定义负载均衡算法

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: custom-lb-config
  namespace: service-advanced
data:
  nginx.conf: |
    upstream backend {
        least_conn;  # 最少连接算法
        server 10.244.1.10:8080;
        server 10.244.2.15:8080;
        keepalive 32;
    }
    
    server {
        listen 80;
        location / {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
        }
    }
```

### 3. 服务网格集成

#### 3.1 Istio 服务网格配置

```yaml
# Istio DestinationRule
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: advanced-service-dr
  namespace: service-advanced
spec:
  host: advanced-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 1000
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 7
      interval: 30s
      baseEjectionTime: 30s

---
# Istio VirtualService
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: advanced-service-vs
  namespace: service-advanced
spec:
  hosts:
    - advanced-service
  http:
    - route:
        - destination:
            host: advanced-service
            subset: v1
          weight: 90
        - destination:
            host: advanced-service
            subset: v2
          weight: 10
```

#### 3.2 Linkerd 服务配置

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: advanced-service.service-advanced.svc.cluster.local
  namespace: service-advanced
spec:
  routes:
    - condition:
        method: GET
        pathRegex: /api/v1/.*
      name: api-v1-routes
      isRetryable: false
    - condition:
        method: POST
        pathRegex: /api/v1/data
      name: data-post
      isRetryable: true
      timeout: 30s
```

### 4. 多集群服务管理

#### 4.1 跨集群服务发现

```yaml
# Cluster 1 配置
apiVersion: v1
kind: Service
metadata:
  name: cross-cluster-service
  namespace: service-advanced
  annotations:
    # 多集群服务标识
    multicluster.kubernetes.io/service-name: cross-cluster-service
spec:
  selector:
    app: cross-cluster-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP

---
# Cluster 2 配置
apiVersion: v1
kind: Service
metadata:
  name: cross-cluster-service
  namespace: service-advanced
  annotations:
    multicluster.kubernetes.io/service-name: cross-cluster-service
spec:
  selector:
    app: cross-cluster-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

#### 4.2 联邦服务配置

```yaml
apiVersion: types.kubefed.io/v1beta1
kind: FederatedService
metadata:
  name: federated-service
  namespace: service-advanced
spec:
  template:
    spec:
      selector:
        app: federated-app
      ports:
        - protocol: TCP
          port: 80
          targetPort: 8080
  placement:
    clusters:
      - name: cluster-1
      - name: cluster-2
      - name: cluster-3
  overrides:
    - clusterName: cluster-1
      clusterOverrides:
        - path: "/spec/ports/0/port"
          value: 8080
    - clusterName: cluster-2
      clusterOverrides:
        - path: "/spec/ports/0/port"
          value: 8081
```

### 5. 自定义控制器开发

#### 5.1 CRD定义

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: advancedservices.networking.example.com
spec:
  group: networking.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                serviceName:
                  type: string
                loadBalancingAlgorithm:
                  type: string
                  enum: ["round_robin", "least_conn", "ip_hash"]
                healthCheck:
                  type: object
                  properties:
                    path:
                      type: string
                    port:
                      type: integer
  scope: Namespaced
  names:
    plural: advancedservices
    singular: advancedservice
    kind: AdvancedService
```

#### 5.2 控制器实现示例

```go
// Go语言控制器示例
func (r *AdvancedServiceReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 获取自定义资源
    advancedService := &networkingv1.AdvancedService{}
    if err := r.Get(ctx, req.NamespacedName, advancedService); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // 创建对应的Service资源
    service := &corev1.Service{
        ObjectMeta: metav1.ObjectMeta{
            Name:      advancedService.Spec.ServiceName,
            Namespace: req.Namespace,
        },
        Spec: corev1.ServiceSpec{
            Selector: map[string]string{"app": advancedService.Spec.ServiceName},
            Ports: []corev1.ServicePort{
                {
                    Protocol: corev1.ProtocolTCP,
                    Port:     80,
                    TargetPort: intstr.IntOrString{
                        Type:   intstr.Int,
                        IntVal: 8080,
                    },
                },
            },
        },
    }

    // 应用自定义负载均衡算法
    switch advancedService.Spec.LoadBalancingAlgorithm {
    case "least_conn":
        service.Annotations = map[string]string{
            "service.beta.kubernetes.io/aws-load-balancer-type": "nlb",
        }
    case "ip_hash":
        // 实现IP哈希逻辑
    }

    return ctrl.Result{}, nil
}
```

---

## 🔧 性能优化配置

### 1. 连接池优化

```yaml
apiVersion: v1
kind: Service
metadata:
  name: optimized-service
  namespace: service-advanced
  annotations:
    # 连接池配置
    service.alpha.kubernetes.io/connection-timeout: "30s"
    service.alpha.kubernetes.io/keepalive-timeout: "600s"
spec:
  selector:
    app: optimized-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

### 2. 资源限制配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: resource-managed-service
  namespace: service-advanced
spec:
  selector:
    app: managed-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
# 配合资源配额
apiVersion: v1
kind: ResourceQuota
metadata:
  name: service-quota
  namespace: service-advanced
spec:
  hard:
    services: "50"
    services.loadbalancers: "10"
    services.nodeports: "20"
```

---

## 📊 监控和指标

### 1. 自定义指标收集

```yaml
apiVersion: v1
kind: Service
metadata:
  name: monitored-service
  namespace: service-advanced
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: monitored-app
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: metrics
      protocol: TCP
      port: 8080
      targetPort: 8080
```

### 2. 服务网格指标

```yaml
# Istio指标配置
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: service-telemetry
  namespace: service-advanced
spec:
  metrics:
    - providers:
        - name: prometheus
      overrides:
        - tagOverrides:
            request_operation:
              value: "request.operation"
            grpc_status_code:
              value: "grpc.status_code"
```

---

## ⚠️ 常见问题和解决方案

### 1. EndpointSlice同步问题

**问题现象**: Service无法正确发现Endpoints

**解决方案**:
```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: fixed-endpoints
  namespace: service-advanced
  labels:
    kubernetes.io/service-name: problematic-service
    endpointslice.kubernetes.io/managed-by: custom-controller
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 8080
endpoints:
  - addresses: ["10.244.1.10"]
    conditions:
      ready: true
      serving: true
      terminating: false
```

### 2. 负载均衡不均匀

**问题现象**: 某些Pod接收过多请求

**解决方案**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: balanced-service
  namespace: service-advanced
  annotations:
    service.kubernetes.io/topology-aware-hints: "auto"
spec:
  selector:
    app: balanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  externalTrafficPolicy: Local  # 本地流量策略
```

---

## 🧪 实践练习

### 练习1：自定义EndpointSlice配置
创建具有特定拓扑提示的EndpointSlice，实现区域感知路由。

### 练习2：服务网格集成
配置Istio或Linkerd，实现高级流量管理和可观测性。

### 练习3：多集群服务
设置跨集群服务发现，实现多集群应用部署。

### 练习4：自定义控制器开发
开发简单的自定义控制器来管理特定的Service行为。

---

## 📚 扩展阅读

### 官方文档
- [EndpointSlice文档](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/)
- [服务网格集成指南](https://istio.io/latest/docs/setup/addons/)
- [多集群服务管理](https://github.com/kubernetes-sigs/kubefed)

### 相关案例
- [Service控制器管理](../controllers/core-controllers/)
- [Service监控运维](../monitoring-operations/)
- [Service安全加固](../security-hardening/)

### 进阶主题
- 自定义CRD开发
- 操作符模式实践
- 边缘计算服务管理
- AI驱动的服务优化

---

## 📋 清理资源

```bash
# 删除演示资源
kubectl delete namespace service-advanced

# 清理CRD（如果创建了自定义资源）
kubectl delete crd advancedservices.networking.example.com

# 重置相关配置
kubectl delete federatedservice --all -n service-advanced
```

---

> **💡 提示**: Service高级特性为复杂场景提供了强大的灵活性，建议在充分测试后应用于生产环境。