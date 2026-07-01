# 🚀 CoreDNS 生产级部署配置完整指南

> 企业级 CoreDNS 部署、配置和管理的完整解决方案，满足生产环境高可用、高性能需求

## 📋 案例概述

本案例提供 CoreDNS 的企业级部署和配置方案，涵盖从基础安装到高可用架构的完整实践，确保在生产环境中能够稳定、高效地提供DNS服务。

### 🔧 核心能力覆盖

- **高可用部署**: 多副本架构、滚动更新、故障自愈
- **性能优化**: 缓存策略、并发处理、资源调优
- **配置管理**: Corefile高级配置、插件管理、动态更新
- **安全加固**: 访问控制、TLS加密、日志审计
- **监控告警**: 性能指标、健康检查、故障告警
- **运维管理**: 自动化部署、配置备份、版本管理

### 🎯 适用场景

- 企业级Kubernetes集群DNS服务
- 高并发DNS查询场景
- 多区域部署环境
- 安全合规要求严格的环境
- 需要精细化监控的生产环境

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查集群状态
kubectl cluster-info
kubectl get nodes

# 验证现有CoreDNS状态
kubectl get deployments -n kube-system coredns
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 创建生产环境命名空间
kubectl create namespace coredns-prod
```

### 2. 生产级部署配置

```bash
# 部署高可用CoreDNS
kubectl apply -f coredns-production.yaml -n kube-system

# 验证部署状态
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl describe deployment coredns -n kube-system
```

---

## 📚 核心配置详解

### 1. 高可用部署架构

#### 1.1 多副本部署配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coredns
  namespace: kube-system
  labels:
    k8s-app: kube-dns
spec:
  replicas: 3  # 根据集群规模调整
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
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
      tolerations:
        - key: "CriticalAddonsOnly"
          operator: "Exists"
        - key: "node-role.kubernetes.io/master"
          effect: NoSchedule
        - key: "node-role.kubernetes.io/control-plane"
          effect: NoSchedule
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: k8s-app
                  operator: In
                  values: ["kube-dns"]
              topologyKey: kubernetes.io/hostname
      containers:
      - name: coredns
        image: registry.k8s.io/coredns/coredns:v1.10.1
        imagePullPolicy: IfNotPresent
        args: [ "-conf", "/etc/coredns/Corefile" ]
        volumeMounts:
        - name: config-volume
          mountPath: /etc/coredns
          readOnly: true
        - name: tmp
          mountPath: /tmp
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
          initialDelaySeconds: 30
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3
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
      - name: tmp
        emptyDir: {}
```

#### 1.2 Service配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kube-dns
  namespace: kube-system
  annotations:
    prometheus.io/port: "9153"
    prometheus.io/scrape: "true"
  labels:
    k8s-app: kube-dns
    kubernetes.io/cluster-service: "true"
    kubernetes.io/name: "CoreDNS"
spec:
  selector:
    k8s-app: kube-dns
  ports:
  - name: dns
    port: 53
    protocol: UDP
  - name: dns-tcp
    port: 53
    protocol: TCP
  - name: metrics
    port: 9153
    protocol: TCP
```

### 2. 生产级Corefile配置

#### 2.1 高性能基础配置

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
           expire 30s
           health_check 5s
        }
        cache 30 {
           success 9984
           denial 9984
           prefetch 1 10m 10%
        }
        loop
        reload
        loadbalance
    }
```

#### 2.2 高级缓存优化

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-optimized
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        log . {
           class error
        }
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           endpoint_pod_names
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        # 多上游DNS服务器
        forward . 8.8.8.8 8.8.4.4 1.1.1.1 {
           max_fails 3
           expire 30s
           health_check 5s
           policy sequential
        }
        # 高级缓存配置
        cache 300 {
           success 9984
           denial 9984
           prefetch 1 10m 10%
        }
        # 查询限制防止滥用
        limits {
           requests_per_second 1000
           requests_burst 2000
        }
        loop
        reload
        loadbalance
    }
```

### 3. 资源调优配置

#### 3.1 性能优化参数

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coredns-optimized
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - name: coredns
        env:
        - name: GOGC
          value: "20"  # 垃圾回收优化
        - name: GOMAXPROCS
          value: "2"   # CPU核心数限制
        resources:
          requests:
            cpu: 200m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        # 性能调优挂载点
        volumeMounts:
        - name: coredns-config
          mountPath: /etc/coredns
        - name: tmp
          mountPath: /tmp
```

---

## 🔧 高级配置选项

### 1. 自定义域名解析

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-custom-domains
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        # 自定义域名映射
        hosts {
           10.0.0.10 internal-api.company.com
           10.0.0.11 external-api.company.com
           fallthrough
        }
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```

### 2. 条件转发配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-conditional-forwarding
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        # 内部域名转发到内部DNS
        forward internal.company.com 10.0.0.10:53 {
           max_fails 3
           expire 30s
           health_check 5s
        }
        # 外部域名转发到公共DNS
        forward . 8.8.8.8 8.8.4.4 {
           max_fails 3
           expire 30s
           health_check 5s
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

### 3. 安全增强配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-security-enhanced
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        # 安全日志记录
        log . {
           class error denial
        }
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           endpoint_pod_names
           fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        # 限制查询类型
        any
        # 防止递归查询
        recursion {
           disable
        }
        forward . /etc/resolv.conf {
           max_fails 3
           expire 30s
           health_check 5s
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

---

## 📊 监控和告警

### 1. Prometheus监控配置

```yaml
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

### 2. 告警规则

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: coredns-alerts
  namespace: monitoring
spec:
  groups:
  - name: coredns.rules
    rules:
    - alert: CoreDNSDown
      expr: up{job="coredns"} == 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "CoreDNS is down"
        description: "CoreDNS has disappeared from Prometheus target discovery"
    
    - alert: CoreDNSHighLatency
      expr: histogram_quantile(0.99, rate(coredns_dns_request_duration_seconds_bucket[5m])) > 1
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS high latency"
        description: "CoreDNS 99th percentile latency is higher than 1 second"
    
    - alert: CoreDNSErrorsHigh
      expr: rate(coredns_dns_responses_total{rcode!="NOERROR"}[5m]) > 0.01
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS error rate high"
        description: "CoreDNS error rate is higher than 1%"
```

---

## 🚨 故障排查

### 1. 常见问题诊断

```bash
# 1. 检查CoreDNS状态
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl describe pod -n kube-system -l k8s-app=kube-dns

# 2. 查看日志
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100

# 3. 验证DNS解析
kubectl run dns-test --image=busybox --rm -it -- nslookup kubernetes.default
kubectl run dns-test --image=busybox --rm -it -- nslookup google.com

# 4. 检查配置
kubectl get configmap coredns -n kube-system -o yaml
```

### 2. 性能调优检查

```bash
# 1. 资源使用情况
kubectl top pods -n kube-system -l k8s-app=kube-dns

# 2. 检查DNS查询统计
kubectl port-forward -n kube-system svc/kube-dns 9153:9153
curl http://localhost:9153/metrics | grep coredns_dns

# 3. 网络连通性测试
kubectl exec -it <pod-name> -n <namespace> -- dig @kube-dns.kube-system.svc.cluster.local google.com
```

---

## 🧪 实践练习

### 练习1：高可用部署
部署三副本CoreDNS并验证故障切换能力。

### 练习2：性能调优
调整缓存和并发参数，观察性能变化。

### 练习3：监控配置
配置完整的监控告警体系。

### 练习4：安全加固
实施安全增强配置并验证防护效果。

---

## 📚 扩展阅读

### 官方文档
- [CoreDNS官方文档](https://coredns.io/manual/toc/)
- [Kubernetes DNS配置](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/)

### 相关案例
- [CoreDNS基础入门](../coredns-basics/)
- [CoreDNS高级特性](../coredns-advanced/)
- [网络故障排查](../network-troubleshooting/)

### 进阶主题
- DNS联邦配置
- 自定义插件开发
- 多集群DNS管理
- DNS安全最佳实践

---

## 📋 清理资源

```bash
# 删除测试资源
kubectl delete namespace coredns-prod

# 恢复默认配置
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/master/cluster/addons/dns/coredns/coredns.yaml

# 重置副本数
kubectl scale deployment coredns -n kube-system --replicas=2
```

---

> **💡 提示**: CoreDNS是Kubernetes集群的核心组件，生产环境部署时务必做好充分测试和监控。
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

```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
