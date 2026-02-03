# 🚀 Kubernetes Service Controllers 生产级管理

> 企业级 Service 控制器部署、配置和管理完整指南

## 📋 案例概述

本案例提供 Kubernetes Service 控制器的企业级管理方案，涵盖从基础控制器到高级服务网格的各种部署模式，确保在生产环境中能够稳定、高效地管理服务发现和负载均衡。

### 🔧 核心能力覆盖

- **基础控制器**: kube-proxy、CoreDNS服务发现
- **服务网格**: Istio、Linkerd、Consul Connect
- **云原生服务**: AWS Load Balancer Controller、GKE Service Networking
- **性能优化**: 连接池优化、负载均衡算法、会话保持
- **高可用配置**: 多副本部署、故障转移、健康检查
- **监控告警**: 控制器指标、服务状态监控、性能分析

### 🎯 适用场景

- 企业级微服务架构
- 高可用服务部署
- 多云环境服务管理
- 服务网格集成
- 性能敏感型应用

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查集群状态
kubectl cluster-info
kubectl get nodes

# 验证基础控制器状态
kubectl get daemonsets -n kube-system kube-proxy
kubectl get deployments -n kube-system coredns

# 创建控制器管理命名空间
kubectl create namespace service-controllers
```

### 2. 基础控制器验证

```bash
# 检查 kube-proxy 状态
kubectl get daemonsets -n kube-system kube-proxy
kubectl get pods -n kube-system -l k8s-app=kube-proxy

# 检查 CoreDNS 状态
kubectl get deployments -n kube-system coredns
kubectl get services -n kube-system kube-dns

# 验证服务发现功能
kubectl run debug --image=busybox --rm -it -- nslookup kubernetes.default
```

---

## 📚 核心控制器详解

### 1. kube-proxy 管理

#### 1.1 kube-proxy 模式配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-proxy
  namespace: kube-system
data:
  config.conf: |
    apiVersion: kubeproxy.config.k8s.io/v1alpha1
    kind: KubeProxyConfiguration
    mode: "iptables"  # 或 "ipvs"
    iptables:
      masqueradeAll: false
      masqueradeBit: 14
      minSyncPeriod: 0s
      syncPeriod: 30s
    ipvs:
      excludeCIDRs: null
      minSyncPeriod: 0s
      scheduler: "rr"  # 轮询调度
      syncPeriod: 30s
      strictARP: false
    conntrack:
      maxPerCore: 32768
      min: 131072
      tcpCloseWaitTimeout: 1h0m0s
      tcpEstablishedTimeout: 24h0m0s
```

#### 1.2 kube-proxy 性能优化

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-proxy
  namespace: kube-system
spec:
  selector:
    matchLabels:
      k8s-app: kube-proxy
  template:
    metadata:
      labels:
        k8s-app: kube-proxy
    spec:
      containers:
        - name: kube-proxy
          image: registry.k8s.io/kube-proxy:v1.28.0
          command:
            - /usr/local/bin/kube-proxy
            - --config=/var/lib/kube-proxy/config.conf
            - --v=2
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi
          securityContext:
            privileged: true
          volumeMounts:
            - name: kube-proxy-config
              mountPath: /var/lib/kube-proxy/
            - name: lib-modules
              mountPath: /lib/modules
              readOnly: true
      volumes:
        - name: kube-proxy-config
          configMap:
            name: kube-proxy
        - name: lib-modules
          hostPath:
            path: /lib/modules
```

### 2. CoreDNS 服务发现

#### 2.1 CoreDNS 配置优化

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

#### 2.2 CoreDNS 水平扩展

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coredns
  namespace: kube-system
spec:
  replicas: 3  # 根据集群规模调整
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  selector:
    matchLabels:
      k8s-app: kube-dns
  template:
    metadata:
      labels:
        k8s-app: kube-dns
    spec:
      priorityClassName: system-cluster-critical
      serviceAccountName: coredns
      containers:
        - name: coredns
          image: registry.k8s.io/coredns/coredns:v1.10.1
          args: [ "-conf", "/etc/coredns/Corefile" ]
          volumeMounts:
            - name: config-volume
              mountPath: /etc/coredns
              readOnly: true
          ports:
            - containerPort: 53
              name: dns
              protocol: UDP
            - containerPort: 53
              name: dns-tcp
              protocol: TCP
            - containerPort: 9153
              name: metrics
              protocol: TCP
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
              scheme: HTTP
            initialDelaySeconds: 60
            timeoutSeconds: 5
            successThreshold: 1
            failureThreshold: 5
          readinessProbe:
            httpGet:
              path: /ready
              port: 8181
              scheme: HTTP
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              add:
                - NET_BIND_SERVICE
              drop:
                - all
            readOnlyRootFilesystem: true
      volumes:
        - name: config-volume
          configMap:
            name: coredns
            items:
              - key: Corefile
                path: Corefile
```

### 3. 服务网格控制器

#### 3.1 Istio 服务网格部署

```yaml
# Istio 基础组件
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-controlplane
  namespace: istio-system
spec:
  profile: default
  components:
    pilot:
      enabled: true
      k8s:
        resources:
          requests:
            cpu: 200m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
    ingressGateways:
      - name: istio-ingressgateway
        enabled: true
        k8s:
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 2000m
              memory: 1024Mi
  values:
    global:
      proxy:
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 2000m
            memory: 1024Mi
    pilot:
      autoscaleEnabled: true
      autoscaleMin: 2
      autoscaleMax: 5
```

#### 3.2 Linkerd 服务网格配置

```yaml
# Linkerd 基础安装
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: web-svc.emojivoto.svc.cluster.local
  namespace: emojivoto
spec:
  routes:
    - condition:
        method: GET
        pathRegex: /api/list
      name: list-emojis
      isRetryable: false
    - condition:
        method: POST
        pathRegex: /api/vote
      name: vote-emoji
      isRetryable: true
```

### 4. 云原生服务控制器

#### 4.1 AWS Load Balancer Controller

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aws-load-balancer-controller
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/AWSLoadBalancerControllerIAMRole
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aws-load-balancer-controller
  namespace: kube-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: aws-load-balancer-controller
  template:
    metadata:
      labels:
        app.kubernetes.io/name: aws-load-balancer-controller
    spec:
      serviceAccountName: aws-load-balancer-controller
      containers:
        - name: controller
          image: public.ecr.aws/eks/aws-load-balancer-controller:v2.5.4
          args:
            - --cluster-name=your-cluster-name
            - --ingress-class=alb
            - --enable-waf=false
            - --enable-wafv2=false
            - --enable-shield=false
          ports:
            - containerPort: 8080
              name: webhook
          resources:
            requests:
              cpu: 200m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1024Mi
          livenessProbe:
            httpGet:
              path: /healthz
              port: 61779
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 10
```

---

## 🔧 高级配置选项

### 1. 自定义负载均衡策略

```yaml
apiVersion: v1
kind: Service
metadata:
  name: custom-lb-service
  namespace: production
  annotations:
    # AWS 特定配置
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    service.beta.kubernetes.io/aws-load-balancer-proxy-protocol: "*"
    
    # 健康检查配置
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-protocol: "HTTP"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-port: "8080"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-path: "/health"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-interval: "30"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-timeout: "6"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-healthy-threshold: "2"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-unhealthy-threshold: "2"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

### 2. 会话保持配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: sticky-session-service
  namespace: production
  annotations:
    service.alpha.kubernetes.io/tolerate-unready-endpoints: "true"
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3小时会话保持
```

### 3. 外部服务集成

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-database-service
  namespace: production
spec:
  type: ExternalName
  externalName: database.prod.company.internal
---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-database-service
  namespace: production
subsets:
  - addresses:
      - ip: 10.0.1.100
      - ip: 10.0.1.101
    ports:
      - port: 5432
```

---

## 📊 监控和告警

### 1. 控制器指标收集

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: kube-proxy-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      k8s-app: kube-proxy
  namespaceSelector:
    matchNames:
      - kube-system
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: coredns-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      k8s-app: kube-dns
  namespaceSelector:
    matchNames:
      - kube-system
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
```

### 2. 告警规则配置

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: service-controller-alerts
  namespace: monitoring
spec:
  groups:
    - name: service-controllers.rules
      rules:
        # CoreDNS 告警
        - alert: CoreDNSDown
          expr: up{job="coredns"} == 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "CoreDNS is down"
            description: "CoreDNS has disappeared from Prometheus target discovery"
        
        # kube-proxy 告警
        - alert: KubeProxyDown
          expr: up{job="kube-proxy"} == 0
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "kube-proxy is down"
            description: "kube-proxy has disappeared from Prometheus target discovery"
        
        # Service 端点告警
        - alert: ServiceWithoutEndpoints
          expr: kube_service_spec_type == 1 unless kube_endpoint_address_available > 0
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "Service without endpoints"
            description: "Service {{ $labels.namespace }}/{{ $labels.service }} has no endpoints"
```

---

## 🚨 故障排查

### 1. 常见问题诊断

```bash
# 1. 检查控制器状态
kubectl get daemonsets -n kube-system kube-proxy
kubectl get deployments -n kube-system coredns

# 2. 查看控制器日志
kubectl logs -n kube-system -l k8s-app=kube-proxy --tail=100
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100

# 3. 验证服务发现
kubectl run debug --image=busybox --rm -it -- nslookup kubernetes.default
kubectl run debug --image=busybox --rm -it -- nslookup <service-name>.<namespace>.svc.cluster.local

# 4. 检查网络策略影响
kubectl get networkpolicies --all-namespaces
```

### 2. 性能调优

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-proxy-tuning
  namespace: kube-system
data:
  config.conf: |
    apiVersion: kubeproxy.config.k8s.io/v1alpha1
    kind: KubeProxyConfiguration
    mode: "ipvs"
    ipvs:
      scheduler: "lc"  # 最少连接调度
      syncPeriod: 15s
      minSyncPeriod: 5s
    conntrack:
      maxPerCore: 65536
      min: 262144
      tcpCloseWaitTimeout: 30m
      tcpEstablishedTimeout: 12h
```

---

## 🧪 实践练习

### 练习1：控制器部署优化
部署并优化 kube-proxy 和 CoreDNS 配置，提升服务发现性能。

### 练习2：服务网格集成
配置 Istio 或 Linkerd 服务网格，实现高级流量管理。

### 练习3：云原生服务
部署 AWS Load Balancer Controller 并配置外部负载均衡器。

### 练习4：故障诊断演练
模拟各种控制器故障场景，练习诊断和恢复技能。

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes Service Controllers](https://kubernetes.io/docs/concepts/architecture/control-plane-node-communication/)
- [CoreDNS 官方文档](https://coredns.io/manual/toc/)
- [Istio 服务网格](https://istio.io/latest/docs/)

### 相关案例
- [Service 高级特性](../advanced-features/)
- [Service 监控运维](../monitoring-operations/)
- [Service 安全加固](../security-hardening/)

### 进阶主题
- 多集群服务发现
- 边缘计算服务管理
- AI驱动的服务优化
- 零信任网络架构

---

## 📋 清理资源

```bash
# 删除测试资源
kubectl delete namespace service-controllers

# 重置控制器配置（谨慎操作）
kubectl delete configmap kube-proxy -n kube-system
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/master/cluster/addons/kube-proxy/kube-proxy-ds.yaml
```

---

> **💡 提示**: Service 控制器是 Kubernetes 网络功能的核心组件，合理的配置和监控对集群稳定性至关重要。