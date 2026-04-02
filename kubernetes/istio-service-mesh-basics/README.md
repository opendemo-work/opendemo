# Istio Service Mesh Basics

Istio服务网格基础演示，展示流量管理、安全、可观测性等核心功能。

## 什么是Istio

Istio是一个开源的服务网格，它透明地分层到现有的分布式应用程序上。Istio强大的功能提供了一种统一和更有效的方式来保护、连接和监视服务。

```
服务网格架构:
┌─────────────────────────────────────────────────────────┐
│                      应用层                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │Service A│  │Service B│  │Service C│  │Service D│   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
├───────┼────────────┼────────────┼────────────┼─────────┤
│       │            │            │            │         │
│  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐   │
│  │ Envoy   │  │ Envoy   │  │ Envoy   │  │ Envoy   │   │
│  │ (Sidecar)│  │ (Sidecar)│  │ (Sidecar)│  │ (Sidecar)│   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
├───────┼────────────┼────────────┼────────────┼─────────┤
│       └────────────┴────────────┴────────────┘         │
│                    Istio Control Plane                   │
│              ┌─────────────────────────┐                │
│              │  Pilot  │  Citadel     │                │
│              │  Mixer  │  Galley      │                │
│              └─────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
```

## 核心组件

### 数据平面 (Data Plane)
- **Envoy Sidecar**: 代理所有服务间通信
- 处理流量管理、安全、遥测

### 控制平面 (Control Plane)
- **istiod**: 集成了Pilot、Citadel、Galley
  - Pilot: 服务发现和流量管理
  - Citadel: 证书和密钥管理
  - Galley: 配置验证和分发

## 快速开始

### 1. 安装Istio

```bash
# 下载Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.20.0

# 添加到PATH
export PATH=$PWD/bin:$PATH

# 安装Istio (demo配置，包含所有功能)
istioctl install --set profile=demo -y

# 启用自动Sidecar注入
kubectl label namespace default istio-injection=enabled
```

### 2. 部署示例应用

```bash
# 部署Bookinfo示例
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml

# 检查服务
kubectl get services
kubectl get pods

# 查看应用
kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"
```

### 3. 配置网关

```bash
# 部署网关
kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml

# 获取访问地址
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export INGRESS_HOST=$(minikube ip)
export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT

echo "访问地址: http://$GATEWAY_URL/productpage"
```

## 流量管理

### 虚拟服务 (VirtualService)
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        end-user:
          exact: jason
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
```

### 目标规则 (DestinationRule)
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
  - name: v3
    labels:
      version: v3
```

### 灰度发布
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
    - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 80  # 80%流量到v1
    - destination:
        host: reviews
        subset: v2
      weight: 20  # 20%流量到v2
```

### 熔断器
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: httpbin
spec:
  host: httpbin
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 1
      http:
        http1MaxPendingRequests: 1
        maxRequestsPerConnection: 1
    outlierDetection:
      consecutiveErrors: 1
      interval: 1s
      baseEjectionTime: 3m
      maxEjectionPercent: 100
```

## 安全

### 双向TLS (mTLS)
```yaml
# 启用全局mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

### 授权策略
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: productpage
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/bookinfo-productpage"]
  - to:
    - operation:
        methods: ["GET"]
```

## 可观测性

### Kiali (服务拓扑)
```bash
# 安装Kiali
kubectl apply -f samples/addons/kiali.yaml

# 访问Kiali
istioctl dashboard kiali
```

### Grafana (监控)
```bash
# 访问Grafana
istioctl dashboard grafana
```

### Jaeger (分布式追踪)
```bash
# 访问Jaeger
istioctl dashboard jaeger
```

## 常用命令

```bash
# 查看代理配置
istioctl proxy-config cluster <pod-name>
istioctl proxy-config listener <pod-name>
istioctl proxy-config route <pod-name>

# 调试流量
istioctl proxy-config log <pod-name> --level debug

# 分析配置
istioctl analyze

# 生成性能报告
istioctl experimental profile --duration 30s
```

## 学习要点

1. Sidecar代理模式的设计原理
2. Envoy代理的配置和调优
3. 金丝雀发布和A/B测试实现
4. 零信任网络安全模型
5. 服务网格的性能开销分析

## 参考

- [Istio官方文档](https://istio.io/latest/docs/)
- [Istio实践指南](https://istio.io/latest/docs/examples/)
