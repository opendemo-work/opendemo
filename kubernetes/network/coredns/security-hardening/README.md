# 🛡️ CoreDNS 安全加固完整指南

> 企业级 CoreDNS 安全配置、访问控制和防护策略完整解决方案

## 📋 案例概述

本案例提供 CoreDNS 的企业级安全加固方案，涵盖从基础安全配置到高级防护策略的完整内容，确保在生产环境中能够抵御各种安全威胁。

### 🔧 核心能力覆盖

- **访问控制**: 网络策略、ACL配置、身份认证
- **数据加密**: TLS/SSL配置、DNSSEC支持、传输加密
- **安全监控**: 安全日志、威胁检测、异常行为分析
- **防护策略**: DDoS防护、查询过滤、速率限制
- **合规审计**: 安全审计、合规检查、报告生成
- **漏洞管理**: 安全更新、漏洞扫描、风险评估

### 🎯 适用场景

- 金融行业DNS服务
- 政府机构网络环境
- 医疗健康信息系统
- 电商平台DNS基础设施
- 需要合规认证的企业环境

---

## 🚀 快速开始

### 1. 安全环境准备

```bash
# 检查集群安全状态
kubectl get networkpolicies --all-namespaces
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 创建安全测试环境
kubectl create namespace coredns-security

# 验证安全组件
kubectl get secrets -n kube-system | grep coredns
```

### 2. 基础安全配置

```bash
# 应用安全配置
kubectl apply -f coredns-security.yaml -n kube-system

# 验证安全设置
kubectl describe deployment coredns -n kube-system
```

---

## 📚 核心安全配置

### 1. 网络访问控制

#### 1.1 NetworkPolicy配置

```yaml
apiVersion: batch/v1
kind: NetworkPolicy
metadata:
  name: coredns-network-policy
  namespace: kube-system
spec:
  podSelector:
    matchLabels:
      k8s-app: kube-dns
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # 允许集群内部访问
  - from:
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
    - protocol: TCP
      port: 9153
  # 允许监控组件访问
  - from:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 9153
  egress:
  # 允许访问上游DNS服务器
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 10.0.0.0/8
        - 172.16.0.0/12
        - 192.168.0.0/16
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

#### 1.2 高级ACL配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-acl-config
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        
        # 网络访问控制
        acl {
           # 允许内部网络
           allow net 10.0.0.0/8
           allow net 172.16.0.0/12
           allow net 192.168.0.0/16
           
           # 允许特定IP段
           allow net 100.64.0.0/10  # RFC6598 CGNAT
           
           # 拒绝所有其他访问
           block
        }
        
        # 安全日志记录
        log security {
           class error denial
           format combined
        }
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           endpoint_pod_names
           fallthrough in-addr.arpa ip6.arpa
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

### 2. 数据传输加密

#### 2.1 TLS配置

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: coredns-tls
  namespace: kube-system
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t...
  tls.key: LS0tLS1CRUdJTiBSU0EgUFJJV...
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-tls-config
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        
        # TLS加密配置
        tls {
           cert /etc/coredns/tls/tls.crt
           key /etc/coredns/tls/tls.key
        }
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           endpoint_pod_names
           fallthrough in-addr.arpa ip6.arpa
        }
        
        forward . /etc/resolv.conf
        
        cache 30
        loop
        reload
        loadbalance
    }
```

#### 2.2 DNSSEC配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-dnssec-config
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        
        # DNSSEC验证
        dnssec {
           key-directory /etc/coredns/dnssec-keys
           cache 3600
        }
        
        # 安全日志
        log dnssec {
           class error denial
           format json
        }
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           endpoint_pod_names
           fallthrough in-addr.arpa ip6.arpa
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

### 3. 查询防护策略

#### 3.1 DDoS防护配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-ddos-protection
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        
        # 查询速率限制
        ratelimit {
           requests_per_second 1000
           requests_burst 2000
           clients_per_second 100
           clients_burst 200
        }
        
        # 查询过滤
        filter {
           # 阻止危险查询类型
           block query type AXFR
           block query type IXFR
           block query type ANY
           
           # 阻止递归查询攻击
           block recursion
           
           # 阻止过长域名
           block name length > 255
        }
        
        # 查询大小限制
        bufsize 1232
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           endpoint_pod_names
           fallthrough in-addr.arpa ip6.arpa
        }
        
        forward . /etc/resolv.conf
        
        cache 30
        loop
        reload
        loadbalance
    }
```

#### 3.2 智能防护配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-smart-protection
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        
        # 智能威胁检测
        threat-detection {
           # 异常查询模式检测
           anomaly_detection threshold=0.9
           
           # 已知恶意域名阻止
           blocklist /etc/coredns/blocklist.txt
           
           # 地理位置过滤
           geo_filter countries=CN,RU,KP
        }
        
        # 动态ACL
        dynamic-acl {
           # 基于行为的访问控制
           reputation_based
           rate_based
           pattern_based
        }
        
        # 查询日志分析
        log analytics {
           class all
           format json
           output /var/log/coredns/analytics.log
        }
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           endpoint_pod_names
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

## 🔧 安全监控和告警

### 1. 安全指标收集

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: coredns-security-monitor
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
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'coredns_(acl|filter|ratelimit|threat)_.*'
      action: keep
```

### 2. 安全告警规则

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: coredns-security-alerts
  namespace: monitoring
spec:
  groups:
  - name: coredns.security.rules
    rules:
    # ACL阻止事件告警
    - alert: CoreDNSACLBlocksHigh
      expr: rate(coredns_acl_blocks_total[5m]) > 50
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS ACL blocks high"
        description: "High number of blocked DNS queries detected: {{ $value }}"
    
    # DDoS攻击告警
    - alert: CoreDNSDDoSAttack
      expr: rate(coredns_ratelimit_drops_total[5m]) > 100
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "CoreDNS DDoS attack detected"
        description: "Rate limiting dropping {{ $value }} queries per second"
    
    # 异常查询模式告警
    - alert: CoreDNSAnomalousQueries
      expr: coredns_threat_anomalies_detected > 0
      for: 1m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS anomalous queries detected"
        description: "Unusual DNS query patterns detected: {{ $value }} anomalies"
    
    # DNSSEC验证失败告警
    - alert: CoreDNSDNSSECValidationFailed
      expr: rate(coredns_dnssec_validation_failures_total[5m]) > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "CoreDNS DNSSEC validation failed"
        description: "DNSSEC validation failures detected"
```

---

## 📊 安全审计和合规

### 1. 审计日志配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-audit-config
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        
        # 完整审计日志
        log audit {
           class all
           format json
           output /var/log/coredns/audit.log
        }
        
        # 安全事件日志
        log security {
           class error denial
           format syslog
           output /var/log/coredns/security.log
        }
        
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods verified
           endpoint_pod_names
           fallthrough in-addr.arpa ip6.arpa
        }
        
        forward . /etc/resolv.conf
        
        cache 30
        loop
        reload
        loadbalance
    }
```

### 2. 合规检查脚本

```bash
#!/bin/bash
# CoreDNS安全合规检查脚本

echo "🛡️ CoreDNS Security Compliance Check"
echo "==================================="

# 1. 配置安全检查
echo "📋 1. 配置安全检查"
echo "检查ACL配置:"
kubectl get configmap coredns -n kube-system -o yaml | grep -A 10 "acl:" || echo "  ❌ ACL未配置"

echo "检查查询过滤:"
kubectl get configmap coredns -n kube-system -o yaml | grep -A 5 "filter:" || echo "  ❌ 查询过滤未配置"

echo "检查速率限制:"
kubectl get configmap coredns -n kube-system -o yaml | grep -A 5 "ratelimit:" || echo "  ❌ 速率限制未配置"

# 2. 网络安全检查
echo ""
echo "🌐 2. 网络安全检查"
echo "检查NetworkPolicy:"
kubectl get networkpolicy -n kube-system coredns-network-policy 2>/dev/null && echo "  ✅ NetworkPolicy已配置" || echo "  ❌ NetworkPolicy未配置"

# 3. 加密配置检查
echo ""
echo "🔐 3. 加密配置检查"
echo "检查TLS证书:"
kubectl get secret coredns-tls -n kube-system 2>/dev/null && echo "  ✅ TLS证书已配置" || echo "  ❌ TLS证书未配置"

echo "检查DNSSEC:"
kubectl get configmap coredns -n kube-system -o yaml | grep -A 5 "dnssec:" || echo "  ❌ DNSSEC未配置"

# 4. 监控告警检查
echo ""
echo "📊 4. 监控告警检查"
echo "检查安全监控:"
kubectl get servicemonitor -n monitoring coredns-security-monitor 2>/dev/null && echo "  ✅ 安全监控已配置" || echo "  ❌ 安全监控未配置"

echo "检查安全告警:"
kubectl get prometheusrule -n monitoring coredns-security-alerts 2>/dev/null && echo "  ✅ 安全告警已配置" || echo "  ❌ 安全告警未配置"

echo ""
echo "✅ 安全合规检查完成"
```

---

## 🚨 威胁响应和处置

### 1. 自动化响应机制

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coredns-security-response
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: security-response
  template:
    metadata:
      labels:
        app: security-response
    spec:
      containers:
      - name: responder
        image: security/coredns-responder:latest
        env:
        - name: ALERTMANAGER_URL
          value: "http://alertmanager.monitoring.svc:9093"
        - name: SLACK_WEBHOOK_URL
          valueFrom:
            secretKeyRef:
              name: slack-webhook
              key: url
        volumeMounts:
        - name: config
          mountPath: /etc/responder
        resources:
          requests:
            cpu: 50m
            memory: 128Mi
          limits:
            cpu: 100m
            memory: 256Mi
      volumes:
      - name: config
        configMap:
          name: security-responder-config
```

### 2. 应急响应流程

```bash
#!/bin/bash
# CoreDNS安全应急响应脚本

echo "🚨 CoreDNS Security Incident Response"
echo "===================================="

INCIDENT_ID=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/var/log/coredns/incidents/$INCIDENT_ID"

mkdir -p $LOG_DIR

# 1. 收集证据
echo "1. 收集安全证据..."
kubectl logs -n kube-system -l k8s-app=kube-dns --since=1h > $LOG_DIR/coredns_logs.txt
kubectl get events --field-selector involvedObject.namespace=kube-system > $LOG_DIR/events.txt

# 2. 隔离受影响组件
echo "2. 隔离受影响组件..."
kubectl scale deployment coredns -n kube-system --replicas=0

# 3. 应用紧急安全配置
echo "3. 应用紧急安全配置..."
kubectl apply -f emergency-security-config.yaml -n kube-system

# 4. 恢复服务
echo "4. 恢复服务..."
kubectl scale deployment coredns -n kube-system --replicas=2

# 5. 验证恢复
echo "5. 验证服务恢复..."
kubectl get pods -n kube-system -l k8s-app=kube-dns

echo " incident evidence collected in $LOG_DIR"
```

---

## 🧪 安全实践练习

### 练习1：访问控制配置
配置完整的网络访问控制和ACL策略。

### 练习2：加密传输实现
实施TLS和DNSSEC安全传输配置。

### 练习3：威胁防护测试
模拟各种攻击场景并验证防护效果。

### 练习4：合规审计演练
执行完整的安全合规检查流程。

---

## 📚 扩展阅读

### 官方文档
- [CoreDNS安全配置](https://coredns.io/manual/security/)
- [Kubernetes网络安全](https://kubernetes.io/docs/concepts/security/)
- [DNSSEC官方指南](https://www.icann.org/resources/pages/dnssec-what-is-it-why-important-2019-03-05-en)

### 相关案例
- [CoreDNS生产部署](../coredns-deployment/)
- [CoreDNS监控运维](../monitoring-operations/)
- [CoreDNS高级特性](../coredns-advanced-features/)

### 进阶主题
- 零信任网络架构
- AI驱动的威胁检测
- 量子安全DNS
- 区块链DNS解决方案

---

## 📋 清理资源

```bash
# 删除安全测试环境
kubectl delete namespace coredns-security

# 移除安全配置
kubectl delete -f coredns-security.yaml -n kube-system

# 清理安全监控
kubectl delete servicemonitor coredns-security-monitor -n monitoring
kubectl delete prometheusrule coredns-security-alerts -n monitoring

# 恢复默认配置
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/master/cluster/addons/dns/coredns/coredns.yaml
```

---

> **💡 提示**: CoreDNS安全加固需要平衡安全性和性能，在实施严格安全措施时要注意对DNS服务性能的影响。