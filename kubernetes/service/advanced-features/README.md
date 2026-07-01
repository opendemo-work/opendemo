# 🚀 Kubernetes Service高级特性实战

> 深入探索Kubernetes Service的高级功能：Session Affinity、多端口配置、健康检查、外部流量策略等企业级特性

## 📋 案例概述

本案例专注于Kubernetes Service的高级配置和企业级特性，帮助您掌握生产环境中Service的精细化管理和优化配置。

### 🔧 核心技能点

- **Session Affinity**: 会话亲和性配置
- **Multi-port Services**: 多端口服务配置
- **Health Checks**: 健康检查和就绪探针
- **Traffic Policies**: 流量策略控制
- **External Traffic Policy**: 外部流量处理策略
- **Topology-aware Routing**: 拓扑感知路由

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
kubectl create namespace service-advanced

# 启用必要的特性门控（如果需要）
kubectl apply -f feature-gates.yaml
```

### 2. 部署测试应用

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 部署多副本应用
kubectl apply -f advanced-deployment.yaml -n service-advanced

# 验证部署
kubectl get pods -n service-advanced
```

---

## 📚 详细教程

### 1. Session Affinity（会话亲和性）

让来自同一客户端的请求始终路由到同一个Pod。

#### 基于客户端IP的会话亲和性

```yaml
apiVersion: v1
kind: Service
metadata:
  name: session-affinity-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3小时超时
```

#### 部署和测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 部署服务
kubectl apply -f session-affinity-service.yaml

# 测试会话亲和性
kubectl run test-client --image=curlimages/curl --rm -it -n service-advanced -- sh

# 在容器内多次请求，观察Pod IP是否一致
for i in {1..10}; do
  curl -s http://session-affinity-service | grep "Pod IP"
done
```

#### 应用场景
- 用户会话保持
- WebSocket连接
- 文件上传下载
- 需要状态保持的应用

### 2. Multi-port Services（多端口服务）

单个Service暴露多个端口，简化服务管理。

#### 多端口配置示例

```yaml
apiVersion: v1
kind: Service
metadata:
  name: multi-port-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: https
      protocol: TCP
      port: 443
      targetPort: 8443
    - name: metrics
      protocol: TCP
      port: 9090
      targetPort: 9090
  type: LoadBalancer
```

#### 使用方式

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 通过服务名访问不同端口
curl http://multi-port-service:80/
curl https://multi-port-service:443/
curl http://multi-port-service:9090/metrics

# 或通过DNS SRV记录
dig SRV _http._tcp.multi-port-service.service-advanced.svc.cluster.local
```

### 3. 健康检查高级配置

精细化的健康检查和就绪探针配置。

#### 完整健康检查配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: health-check-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-check-deployment
  namespace: service-advanced
spec:
  replicas: 3
  selector:
    matchLabels:
      app: advanced-app
  template:
    metadata:
      labels:
        app: advanced-app
    spec:
      containers:
      - name: app
        image: nginx:1.21
        ports:
        - containerPort: 8080
        # 启动探针
        startupProbe:
          httpGet:
            path: /healthz/startup
            port: 8080
          failureThreshold: 30
          periodSeconds: 10
        # 就绪探针
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3
        # 存活探针
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 5
```

#### 监控健康检查状态

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 查看Pod健康状态
kubectl get pods -n service-advanced -o wide

# 查看详细事件
kubectl describe pod <pod-name> -n service-advanced

# 监控探针失败事件
kubectl get events -n service-advanced --field-selector reason=Unhealthy
```

### 4. External Traffic Policy（外部流量策略）

控制外部流量如何路由到Pod。

#### Local策略（推荐用于性能敏感场景）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-local-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
  externalTrafficPolicy: Local
```

#### Cluster策略（默认，更好的负载均衡）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-cluster-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
  externalTrafficPolicy: Cluster
```

#### 性能对比测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 测试Local策略
kubectl apply -f external-local-service.yaml
LOCAL_IP=$(kubectl get svc external-local-service -n service-advanced -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
ab -n 1000 -c 10 http://$LOCAL_IP/

# 测试Cluster策略
kubectl apply -f external-cluster-service.yaml
CLUSTER_IP=$(kubectl get svc external-cluster-service -n service-advanced -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
ab -n 1000 -c 10 http://$CLUSTER_IP/
```

### 5. Internal Traffic Policy（内部流量策略）

控制集群内部流量路由策略。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: internal-traffic-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
  internalTrafficPolicy: Local  # 或 Cluster
```

### 6. Topology-aware Routing（拓扑感知路由）

基于节点拓扑结构优化流量路由。

#### 启用拓扑感知路由

```yaml
apiVersion: v1
kind: Service
metadata:
  name: topology-aware-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  topologyKeys:
    - "kubernetes.io/hostname"
    - "topology.kubernetes.io/zone"
    - "*"
```

#### 验证拓扑路由

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 查看Pod分布
kubectl get pods -n service-advanced -o wide

# 测试同节点访问优先级
kubectl exec -it <pod-name> -n service-advanced -- curl http://topology-aware-service
```

### 7. IP Family配置（IPv4/IPv6双栈）

配置Service的IP族支持。

#### IPv4单栈配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ipv4-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  ipFamilyPolicy: SingleStack
  ipFamilies:
    - IPv4
```

#### IPv6单栈配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ipv6-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  ipFamilyPolicy: SingleStack
  ipFamilies:
    - IPv6
```

#### 双栈配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: dual-stack-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  ipFamilyPolicy: PreferDualStack
  ipFamilies:
    - IPv4
    - IPv6
```

---

## 🔧 实际应用场景

### 场景1：金融交易系统的会话保持

```yaml
apiVersion: v1
kind: Service
metadata:
  name: trading-session-service
  namespace: finance
  annotations:
    service.alpha.kubernetes.io/tolerate-unready-endpoints: "true"
spec:
  selector:
    app: trading-engine
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 86400  # 24小时会话保持
```

### 场景2：微服务的多端口暴露

```yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: microservices
spec:
  selector:
    app: user-service
  ports:
    - name: api
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: grpc
      protocol: TCP
      port: 50051
      targetPort: 50051
    - name: metrics
      protocol: TCP
      port: 9090
      targetPort: 9090
    - name: admin
      protocol: TCP
      port: 8081
      targetPort: 8081
```

### 场景3：CDN边缘节点优化

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cdn-edge-service
  namespace: cdn
spec:
  selector:
    app: edge-node
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
  externalTrafficPolicy: Local
  internalTrafficPolicy: Local
  topologyKeys:
    - "kubernetes.io/hostname"
```

---

## 📊 性能调优

### 1. 负载均衡算法优化

```yaml
apiVersion: v1
kind: Service
metadata:
  name: optimized-service
  namespace: service-advanced
  annotations:
    # AWS NLB配置
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    # GCP配置
    cloud.google.com/neg: '{"ingress": true}'
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

### 2. 连接池优化

```yaml
apiVersion: v1
kind: Service
metadata:
  name: connection-pool-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
  allocateLoadBalancerNodePorts: false  # 减少NodePort分配开销
```

---

## 🔍 监控和告警

### 1. Service指标收集

```yaml
apiVersion: v1
kind: Service
metadata:
  name: monitored-service
  namespace: service-advanced
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: advanced-app
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: metrics
      protocol: TCP
      port: 9090
      targetPort: 9090
```

### 2. 常用监控查询

```promql
# Service连接数
kube_service_status_load_balancer_ingress{service="monitored-service"}

# Endpoint健康状态
kube_endpoint_address_available{service="monitored-service"}

# Service延迟分布
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

## ⚠️ 常见问题和解决方案

### 1. Session Affinity失效

**问题**: 会话亲和性没有按预期工作

**解决方案**:
```yaml
# 检查Service配置
kubectl get svc session-affinity-service -n service-advanced -o yaml

# 验证客户端IP是否变化
kubectl logs -n service-advanced -l app=advanced-app --tail=100 | grep "Client IP"
```

### 2. 多端口服务DNS解析异常

**问题**: SRV记录未正确生成

**解决方案**:
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 验证CoreDNS配置
kubectl get cm coredns -n kube-system -o yaml

# 重启CoreDNS
kubectl rollout restart deployment/coredns -n kube-system
```

### 3. External Traffic Policy性能问题

**问题**: Local策略导致负载不均衡

**解决方案**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: balanced-service
  namespace: service-advanced
spec:
  selector:
    app: advanced-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
  externalTrafficPolicy: Cluster  # 改为Cluster策略
```

---

## 🧪 实践练习

### 练习1：会话亲和性调优
配置不同超时时间的会话亲和性，测试用户体验和资源利用率的平衡。

### 练习2：多端口服务管理
为一个复杂应用配置多端口Service，实现API、管理界面、监控端点的统一暴露。

### 练习3：流量策略对比
在同一环境中部署Local和Cluster策略的服务，对比性能差异和适用场景。

### 练习4：健康检查优化
为不同类型的应用（Web、数据库、消息队列）配置最适合的健康检查策略。

---

## 📋 清理资源

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 删除命名空间和所有资源
kubectl delete namespace service-advanced

# 或单独删除各项资源
kubectl delete svc --all -n service-advanced
kubectl delete deploy --all -n service-advanced
kubectl delete pod --all -n service-advanced
```

---

> **💡 提示**: 高级Service特性需要根据具体业务场景谨慎配置，建议在测试环境中充分验证后再应用到生产环境。
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
