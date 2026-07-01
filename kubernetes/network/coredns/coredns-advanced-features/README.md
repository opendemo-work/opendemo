# 🌐 CoreDNS 高级特性与自定义配置

> 企业级 CoreDNS 高级功能、插件开发和自定义配置完整指南

## 📋 案例概述

本案例深入探讨 CoreDNS 的高级特性和自定义配置能力，涵盖插件开发、联邦DNS、条件转发等企业级功能，帮助企业构建灵活、安全的DNS服务体系。

### 🔧 核心能力覆盖

- **插件开发**: 自定义插件编写、插件管理、性能优化
- **联邦DNS**: 多集群DNS联合、跨域解析、全局服务发现
- **条件转发**: 基于域名的智能转发、地理位置路由
- **安全增强**: DNSSEC支持、访问控制、查询过滤
- **性能优化**: 高级缓存策略、并发处理、资源管理
- **监控分析**: 详细指标收集、性能分析、故障诊断

### 🎯 适用场景

- 复杂企业网络环境
- 多集群联合部署
- 需要自定义DNS逻辑的场景
- 安全合规要求严格的环境
- 高性能DNS服务需求

---

## 🚀 快速开始

### 1. 环境准备

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 检查CoreDNS版本
kubectl get pods -n kube-system -l k8s-app=kube-dns -o jsonpath='{.items[0].spec.containers[0].image}'

# 创建测试环境
kubectl create namespace coredns-advanced

# 部署测试应用
kubectl apply -f test-applications.yaml -n coredns-advanced
```

### 2. 高级配置验证

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 验证插件加载
kubectl exec -it <coredns-pod> -n kube-system -- coredns -plugins

# 测试自定义配置
kubectl apply -f advanced-corefile.yaml -n kube-system
```

---

## 📚 核心高级特性

### 1. 自定义插件开发

#### 1.1 插件基础结构

```go
// Go语言插件示例
package example

import (
    "context"
    "github.com/coredns/coredns/plugin"
    "github.com/coredns/coredns/request"
    "github.com/miekg/dns"
)

type Example struct {
    Next plugin.Handler
    // 自定义配置字段
    config map[string]string
}

func (e Example) ServeDNS(ctx context.Context, w dns.ResponseWriter, r *dns.Msg) (int, error) {
    state := request.Request{W: w, Req: r}
    
    // 自定义处理逻辑
    if state.QType() == dns.TypeA && state.Name() == "special.example.com." {
        m := new(dns.Msg)
        m.SetReply(r)
        rr, err := dns.NewRR("special.example.com. 300 IN A 10.0.0.10")
        if err != nil {
            return dns.RcodeServerFailure, err
        }
        m.Answer = append(m.Answer, rr)
        w.WriteMsg(m)
        return dns.RcodeSuccess, nil
    }
    
    // 传递给下一个插件
    return plugin.NextOrFailure(e.Name(), e.Next, ctx, w, r)
}

func (e Example) Name() string { return "example" }
```

#### 1.2 插件注册和配置

```go
// 插件注册
func init() {
    plugin.Register("example", setup)
}

func setup(c *caddy.Controller) error {
    e := Example{}
    
    // 解析配置
    for c.Next() {
        if c.NextBlock() {
            switch c.Val() {
            case "config":
                if !c.NextArg() {
                    return c.ArgErr()
                }
                e.config[c.Val()] = c.RemainingArgs()[0]
            }
        }
    }
    
    // 注册插件
    dnsserver.GetConfig(c).AddPlugin(func(next plugin.Handler) plugin.Handler {
        e.Next = next
        return e
    })
    
    return nil
}
```

### 2. 联邦DNS配置

#### 2.1 多集群DNS联合

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-federation
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        # 本地集群DNS
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        
        # 联邦DNS配置
        federation cluster.local {
           prod prod-clusters.example.com
           staging staging-clusters.example.com
           dev dev-clusters.example.com
        }
        
        # 条件转发到不同集群
        forward prod-clusters.example.com 10.10.0.10:53 {
           max_fails 3
           expire 30s
           health_check 5s
        }
        
        forward staging-clusters.example.com 10.20.0.10:53 {
           max_fails 3
           expire 30s
           health_check 5s
        }
        
        forward dev-clusters.example.com 10.30.0.10:53 {
           max_fails 3
           expire 30s
           health_check 5s
        }
        
        prometheus :9153
        cache 30
        loop
        reload
        loadbalance
    }
```

#### 2.2 跨集群服务发现

```yaml
apiVersion: v1
kind: Service
metadata:
  name: global-service
  namespace: federation
  annotations:
    # 联邦服务标识
    federation.kubernetes.io/service-name: global-service
spec:
  selector:
    app: global-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
---
# 不同集群中的相同服务
apiVersion: v1
kind: Service
metadata:
  name: global-service
  namespace: federation
  annotations:
    federation.kubernetes.io/cluster-name: prod-us-east
spec:
  selector:
    app: global-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

### 3. 条件转发和智能路由

#### 3.1 基于地理位置的转发

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-geo-routing
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        
        # 地理位置智能路由
        template IN A geo-route.example.com {
           match ^(?P<region>[^.]+)\.geo-route\.example\.com$
           answer "{{ .Name }} 60 IN A {{ .Group.region }}"
           fallthrough
        }
        
        # 北美地区转发
        forward us.geo-route.example.com 10.0.1.10:53 {
           max_fails 3
           expire 30s
           health_check 5s
        }
        
        # 欧洲地区转发
        forward eu.geo-route.example.com 10.0.2.10:53 {
           max_fails 3
           expire 30s
           health_check 5s
        }
        
        # 亚洲地区转发
        forward asia.geo-route.example.com 10.0.3.10:53 {
           max_fails 3
           expire 30s
           health_check 5s
        }
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        
        prometheus :9153
        cache 300
        loop
        reload
        loadbalance
    }
```

#### 3.2 基于客户端IP的路由

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-client-routing
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        
        # 客户端IP分段路由
        acl {
           allow net 10.0.0.0/8
           allow net 172.16.0.0/12
           allow net 192.168.0.0/16
           block
        }
        
        # 内网客户端转发到内网DNS
        forward internal.example.com 10.0.0.10:53 {
           max_fails 3
           expire 30s
           health_check 5s
           except 10.0.0.0/8
        }
        
        # 外网客户端转发到公网DNS
        forward internal.example.com 8.8.8.8:53 {
           max_fails 3
           expire 30s
           health_check 5s
        }
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        
        prometheus :9153
        cache 30
        loop
        reload
        loadbalance
    }
```

### 4. 安全增强配置

#### 4.1 DNSSEC支持

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-dnssec
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        log . {
           class error denial
        }
        
        # DNSSEC验证
        dnssec {
           key-directory /etc/coredns/keys
           cache 3600
        }
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           endpoint_pod_names
           fallthrough in-addr.arpa ip6.arpa
        }
        
        # 查询过滤防止滥用
        filter {
           block query type AXFR
           block query type IXFR
           rate_limit 1000 60
        }
        
        # 访问控制
        acl {
           allow net 10.0.0.0/8
           allow net 172.16.0.0/12
           allow net 192.168.0.0/16
           block
        }
        
        forward . /etc/resolv.conf {
           max_fails 3
           expire 30s
           health_check 5s
        }
        
        cache 300 {
           success 9984
           denial 9984
           prefetch 1 10m 10%
        }
        
        loop
        reload
        loadbalance
    }
```

#### 4.2 查询审计和日志

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-audit
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        
        # 详细日志记录
        log . {
           class all
           format json
        }
        
        # 安全日志
        log security {
           class error denial
           format combined
        }
        
        # 查询审计
        whoami
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        
        forward . /etc/resolv.conf
        
        cache 30
        
        loop
        reload
        loadbalance
    }
```

---

## 🔧 性能优化配置

### 1. 高级缓存策略

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-advanced-cache
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
        
        # 高级缓存配置
        cache {
           # 成功响应缓存
           success 9984 300 {
              prefetch 1 10m 10%
           }
           # 否定响应缓存
           denial 9984 60 {
              prefetch 1 5m 20%
           }
           # 缓存预热
           serve_stale 30s
        }
        
        # 并发处理优化
        limits {
           requests_per_second 5000
           requests_burst 10000
           clients_per_second 1000
           clients_burst 2000
        }
        
        forward . /etc/resolv.conf {
           max_concurrent 2000
           expire 30s
           health_check 5s
        }
        
        prometheus :9153
        loop
        reload
        loadbalance
    }
```

### 2. 资源优化配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coredns-optimized
  namespace: kube-system
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: coredns
        image: registry.k8s.io/coredns/coredns:v1.10.1
        env:
        # Go运行时优化
        - name: GOGC
          value: "20"
        - name: GOMAXPROCS
          value: "2"
        # 网络优化
        - name: COREDNS_BUF_SIZE
          value: "1232"
        resources:
          requests:
            cpu: 300m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        # 性能调优参数
        securityContext:
          capabilities:
            add:
            - NET_BIND_SERVICE
            drop:
            - all
```

---

## 📊 监控和指标

### 1. 自定义指标收集

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: coredns-advanced-monitoring
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
    interval: 15s
    path: /metrics
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'coredns_(dns|cache|forward)_.*'
      action: keep
```

### 2. 高级告警规则

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: coredns-advanced-alerts
  namespace: monitoring
spec:
  groups:
  - name: coredns.advanced.rules
    rules:
    - alert: CoreDNSCacheHitRateLow
      expr: rate(coredns_cache_hits_total[5m]) / rate(coredns_dns_requests_total[5m]) < 0.8
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS cache hit rate low"
        description: "Cache hit rate is below 80%, consider adjusting cache settings"
    
    - alert: CoreDNSForwardErrorsHigh
      expr: rate(coredns_forward_errors_total[5m]) > 0.05
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "CoreDNS forward errors high"
        description: "Forward error rate exceeds 5%"
    
    - alert: CoreDNSACLBlocksHigh
      expr: rate(coredns_acl_blocks_total[5m]) > 100
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS ACL blocks high"
        description: "High number of blocked queries detected"
```

---

## 🚨 故障排查和调试

### 1. 高级诊断工具

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 1. 插件调试
kubectl exec -it <coredns-pod> -n kube-system -- coredns -plugins

# 2. 配置验证
kubectl exec -it <coredns-pod> -n kube-system -- coredns -conf /etc/coredns/Corefile -check

# 3. 性能分析
kubectl exec -it <coredns-pod> -n kube-system -- sh -c "pprof -http=:6060 http://localhost:6060/debug/pprof/profile"

# 4. 详细日志
kubectl logs -n kube-system -l k8s-app=kube-dns -f --since=1h
```

### 2. 调试配置示例

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-debug
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        # 调试模式
        debug
        
        # 详细日志
        log . {
           class all
           format json
        }
        
        errors
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        
        # 调试转发
        forward . 8.8.8.8 {
           force_tcp
           prefer_udp
           expire 300s
           max_fails 1
        }
        
        cache 5
        loop
        reload
        loadbalance
    }
```

---

## 🧪 实践练习

### 练习1：插件开发
开发一个简单的自定义插件并集成到CoreDNS中。

### 练习2：联邦DNS配置
配置多集群DNS联合解析环境。

### 练习3：智能路由实现
基于客户端特征实现智能DNS路由。

### 练习4：安全加固
实施完整的DNS安全防护方案。

---

## 📚 扩展阅读

### 官方文档
- [CoreDNS插件开发](https://coredns.io/manual/plugins/)
- [联邦DNS指南](https://github.com/kubernetes/federation/blob/master/docs/dns.md)
- [CoreDNS安全配置](https://coredns.io/manual/security/)

### 相关案例
- [CoreDNS生产部署](../coredns-deployment/)
- [CoreDNS监控运维](../monitoring-operations/)
- [CoreDNS安全加固](../security-hardening/)

### 进阶主题
- 自定义协议支持
- 机器学习驱动的DNS优化
- 边缘计算DNS架构
- 量子安全DNS

---

## 📋 清理资源

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 删除测试环境
kubectl delete namespace coredns-advanced

# 恢复默认配置
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/master/cluster/addons/dns/coredns/coredns.yaml

# 清理自定义插件
kubectl delete configmap coredns-custom -n kube-system
```

---

> **💡 提示**: CoreDNS高级特性提供了强大的自定义能力，但需要谨慎使用以确保稳定性和安全性。
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
