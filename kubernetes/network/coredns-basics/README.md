# 🧠 CoreDNS基础入门实战

> 全面掌握Kubernetes DNS服务核心组件：从基础配置到高级服务发现的完整实践指南

## 📋 案例概述

本案例详细介绍CoreDNS的基础知识和实践操作，帮助用户理解和掌握Kubernetes服务发现和DNS解析的核心技能。

### 🔧 核心技能点

- **CoreDNS基本概念**: 理解Kubernetes DNS服务架构和工作原理
- **基础配置管理**: Corefile配置、插件使用、服务发现配置
- **服务发现机制**: Service DNS解析、Pod DNS解析、Endpoints管理
- **性能调优优化**: 缓存配置、查询优化、资源限制调整
- **监控告警体系**: DNS指标采集、性能监控、故障告警
- **安全配置管理**: 访问控制、DNS安全、日志审计

### 🎯 适用人群

- Kubernetes系统管理员
- DevOps工程师
- 网络工程师
- 云平台运维人员

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查集群DNS状态
kubectl cluster-info
kubectl get pods -n kube-system | grep coredns

# 创建测试命名空间
kubectl create namespace coredns-demo

# 验证DNS功能
kubectl run debug-pod --image=busybox --rm -it -- sh
nslookup kubernetes.default
```

### 2. CoreDNS基础配置

```bash
# 查看当前CoreDNS配置
kubectl get configmap coredns -n kube-system -o yaml

# 备份原始配置
kubectl get configmap coredns -n kube-system -o yaml > coredns-backup.yaml
```

---

## 📚 详细教程

### 1. CoreDNS核心概念

#### 1.1 什么是CoreDNS

CoreDNS是Kubernetes的默认DNS服务器，负责集群内的服务发现和DNS解析。

**核心特性**：
- 基于Caddy服务器构建
- 插件化架构设计
- 支持多种DNS协议
- 高性能DNS解析能力

#### 1.2 DNS解析架构

```
Pod → CoreDNS → Service Discovery → Endpoints → Target Pods
```

### 2. 基础配置管理

#### 2.1 Corefile基础配置

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

#### 2.2 自定义DNS配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: custom-dns
  namespace: coredns-demo
data:
  Corefile: |
    .:53 {
        errors
        log
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods verified
            upstream
            fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . 8.8.8.8 8.8.4.4 {
            max_fails 3
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

### 3. 服务发现配置

#### 3.1 Service DNS解析

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: coredns-demo
spec:
  selector:
    app: web
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
  namespace: coredns-demo
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx:1.21
        ports:
        - containerPort: 8080
```

#### 3.2 Headless Service配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: headless-service
  namespace: coredns-demo
spec:
  clusterIP: None
  selector:
    app: database
  ports:
  - port: 3306
    targetPort: 3306
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database-sts
  namespace: coredns-demo
spec:
  serviceName: headless-service
  replicas: 3
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "password123"
```

### 4. 性能调优配置

#### 4.1 缓存优化配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-performance
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            upstream
            fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . /etc/resolv.conf {
            max_concurrent 2000
            health_check 5s
        }
        # 性能优化缓存配置
        cache 60 {
            success 9984
            denial 9984
            prefetch 1 10m 10%
        }
        # 负载均衡优化
        loadbalance round_robin
        # 自动重载配置
        reload 30s
    }
```

#### 4.2 资源限制配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coredns
  namespace: kube-system
spec:
  replicas: 2
  selector:
    matchLabels:
      k8s-app: kube-dns
  template:
    metadata:
      labels:
        k8s-app: kube-dns
    spec:
      priorityClassName: system-cluster-critical
      containers:
      - name: coredns
        image: k8s.gcr.io/coredns/coredns:v1.8.6
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
            memory: "70Mi"
            cpu: "100m"
          limits:
            memory: "170Mi"
            cpu: "200m"
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

### 5. 监控告警配置

#### 5.1 Prometheus监控配置

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: coredns
  namespace: monitoring
  labels:
    app: coredns
spec:
  jobLabel: k8s-app
  selector:
    matchLabels:
      k8s-app: kube-dns
  namespaceSelector:
    matchNames:
    - kube-system
  endpoints:
  - port: metrics
    interval: 15s
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-alerts
  namespace: monitoring
data:
  coredns-alerts.yaml: |
    groups:
    - name: coredns.alerts
      rules:
      - alert: CoreDNSDown
        expr: up{job="coredns"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "CoreDNS服务宕机"
          description: "CoreDNS服务不可用超过5分钟"
          
      - alert: CoreDNSHighErrorRate
        expr: rate(coredns_dns_responses_total{rcode!="NOERROR"}[5m]) > 0.01
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "CoreDNS错误率过高"
          description: "DNS错误率超过1%: {{ $value }}"
          
      - alert: CoreDNSHighLatency
        expr: histogram_quantile(0.99, rate(coredns_dns_request_duration_seconds_bucket[5m])) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "CoreDNS响应延迟过高"
          description: "99%的DNS查询响应时间超过1秒: {{ $value }}s"
```

---

## 🔧 实践操作

### 1. CoreDNS部署验证

```bash
# 1. 检查CoreDNS Pod状态
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 2. 验证DNS解析功能
kubectl run dns-test --image=busybox --rm -it -- sh
nslookup kubernetes.default
nslookup web-service.coredns-demo.svc.cluster.local

# 3. 测试服务发现
dig web-service.coredns-demo.svc.cluster.local

# 4. 验证Pod DNS解析
kubectl get pods -n coredns-demo -o wide
nslookup 10-244-1-10.coredns-demo.pod.cluster.local
```

### 2. 性能测试

```bash
# 1. 部署DNS性能测试工具
kubectl apply -f dnsperf.yaml

# 2. 执行DNS查询测试
kubectl exec -it dnsperf-pod -- dnsperf -s coredns.kube-system.svc.cluster.local -d queries.txt

# 3. 监控性能指标
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# 访问 http://localhost:9090 查看DNS相关指标
```

### 3. 故障排查

```bash
# 1. 查看CoreDNS日志
kubectl logs -n kube-system -l k8s-app=kube-dns

# 2. 检查配置状态
kubectl get configmap coredns -n kube-system -o yaml

# 3. 验证网络连通性
kubectl exec -it <pod-name> -n coredns-demo -- nc -z coredns.kube-system.svc.cluster.local 53

# 4. 测试外部DNS解析
kubectl exec -it <pod-name> -n coredns-demo -- nslookup google.com
```

---

## 📊 监控指标

### 1. 关键性能指标

```bash
# DNS查询成功率
rate(coredns_dns_responses_total{rcode="NOERROR"}[5m]) / rate(coredns_dns_responses_total[5m])

# 平均响应时间
rate(coredns_dns_request_duration_seconds_sum[5m]) / rate(coredns_dns_request_duration_seconds_count[5m])

# QPS统计
rate(coredns_dns_requests_total[5m])

# 缓存命中率
rate(coredns_cache_hits_total[5m]) / (rate(coredns_cache_hits_total[5m]) + rate(coredns_cache_misses_total[5m]))
```

### 2. 告警规则配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-rules
  namespace: monitoring
data:
  rules.yaml: |
    groups:
    - name: coredns.rules
      rules:
      - record: coredns:query_success_rate
        expr: rate(coredns_dns_responses_total{rcode="NOERROR"}[5m]) / rate(coredns_dns_responses_total[5m])
        
      - record: coredns:average_response_time
        expr: rate(coredns_dns_request_duration_seconds_sum[5m]) / rate(coredns_dns_request_duration_seconds_count[5m])
        
      - record: coredns:qps
        expr: rate(coredns_dns_requests_total[5m])
```

---

## ⚠️ 常见问题和解决方案

### 1. DNS解析失败

**问题现象**: Pod无法解析服务名称或外部域名

**可能原因**:
- CoreDNS Pod异常
- 网络策略阻止DNS流量
- 配置文件语法错误
- Service Account权限问题

**解决步骤**:
```bash
# 1. 检查CoreDNS状态
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl describe pod -n kube-system <coredns-pod-name>

# 2. 验证网络策略
kubectl get networkpolicies --all-namespaces

# 3. 检查配置语法
kubectl get configmap coredns -n kube-system -o yaml | yq eval

# 4. 测试DNS连通性
kubectl run debug-pod --image=busybox --rm -it -- sh
nslookup kubernetes.default
```

### 2. DNS响应慢

**问题现象**: DNS查询响应时间过长

**解决步骤**:
```bash
# 1. 检查CoreDNS资源使用
kubectl top pods -n kube-system -l k8s-app=kube-dns

# 2. 调整缓存配置
kubectl patch configmap coredns -n kube-system -p '{"data":{"Corefile":".:53 {\n    cache 120\n    ...\n}"}}'

# 3. 增加副本数
kubectl scale deployment coredns -n kube-system --replicas=3

# 4. 优化上游DNS
kubectl patch configmap coredns -n kube-system -p '{"data":{"Corefile":"forward . 8.8.8.8 1.1.1.1"}}'
```

### 3. 内存泄漏问题

**问题现象**: CoreDNS Pod内存使用持续增长

**解决步骤**:
```bash
# 1. 监控内存使用
kubectl top pods -n kube-system -l k8s-app=kube-dns

# 2. 检查缓存配置
kubectl get configmap coredns -n kube-system -o yaml

# 3. 重启CoreDNS Pod
kubectl delete pod -n kube-system -l k8s-app=kube-dns

# 4. 调整资源限制
kubectl patch deployment coredns -n kube-system -p '{"spec":{"template":{"spec":{"containers":[{"name":"coredns","resources":{"limits":{"memory":"256Mi"}}}]}}}}'
```

---

## 🧪 实践练习

### 练习1：基础DNS配置
配置自定义CoreDNS配置并验证服务发现功能。

### 练习2：性能调优实践
优化CoreDNS缓存和资源配置以提升查询性能。

### 练习3：监控告警配置
部署完整的DNS监控和告警体系。

### 练习4：故障排查演练
模拟各种DNS故障场景并练习排查技能。

---

## 📚 扩展阅读

### 官方文档
- [CoreDNS官方文档](https://coredns.io/manual/toc/)
- [Kubernetes DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [CoreDNS插件文档](https://coredns.io/plugins/)

### 相关案例
- [Terway网络插件](../terway-basics/)
- [CSI Plugin存储](../csi-plugin-basics/)
- [网络组件生产实践](../network-production/)

### 进阶主题
- DNS联邦配置
- 自定义DNS插件开发
- 多集群DNS解决方案
- DNS安全加固

---

## 📋 清理资源

```bash
# 删除测试资源
kubectl delete namespace coredns-demo

# 恢复原始配置
kubectl apply -f coredns-backup.yaml

# 删除监控配置
kubectl delete servicemonitor coredns -n monitoring
kubectl delete configmap coredns-alerts -n monitoring

# 重置CoreDNS副本数
kubectl scale deployment coredns -n kube-system --replicas=2
```

---

> **💡 提示**: CoreDNS是Kubernetes集群的关键组件，建议在修改配置前做好备份。在生产环境中使用时要注意性能监控和资源管理。
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
