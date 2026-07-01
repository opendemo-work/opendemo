# 📊 CoreDNS 监控运维完整体系

> 企业级 CoreDNS 监控、告警、日志和运维管理完整解决方案

## 📋 案例概述

本案例提供 CoreDNS 的企业级监控运维体系，涵盖从基础指标收集到智能告警的全方位内容，确保在生产环境中能够及时发现问题并快速响应。

### 🔧 核心能力覆盖

- **指标收集**: DNS查询统计、缓存命中率、转发性能
- **日志管理**: 查询日志、错误日志、安全审计日志
- **告警策略**: 性能异常、服务中断、安全威胁告警
- **可视化展示**: Grafana仪表板、自定义监控视图
- **自动化运维**: 自愈机制、容量规划、性能优化
- **故障排查**: 诊断工具、根因分析、修复建议

### 🎯 适用场景

- 生产环境DNS监控
- 性能瓶颈分析
- 安全威胁检测
- 容量规划和优化
- 合规审计和报告

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查监控组件状态
kubectl get pods -n monitoring

# 验证Prometheus和Grafana部署
kubectl get svc -n monitoring prometheus-k8s grafana

# 创建监控专用命名空间
kubectl create namespace coredns-monitoring
```

### 2. 基础监控配置

```bash
# 部署CoreDNS监控配置
kubectl apply -f coredns-monitor.yaml -n monitoring

# 验证监控目标发现
kubectl port-forward svc/prometheus-k8s -n monitoring 9090:9090
# 访问 http://localhost:9090/targets
```

---

## 📊 核心监控体系

### 1. 指标收集配置

#### 1.1 ServiceMonitor配置

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
    interval: 15s
    path: /metrics
    relabelings:
    - sourceLabels: [__meta_kubernetes_pod_name]
      targetLabel: pod
    - sourceLabels: [__meta_kubernetes_pod_node_name]
      targetLabel: node
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'coredns_(dns|cache|forward)_.*'
      action: keep
```

#### 1.2 自定义指标收集

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-custom-metrics
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
        }
        prometheus :9153 {
           # 自定义指标标签
           metrics_labels {
              cluster="production"
              region="us-west"
           }
        }
        forward . /etc/resolv.conf {
           max_concurrent 1000
           expire 30s
           health_check 5s
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

### 2. 关键指标定义

#### 2.1 性能指标

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: coredns-performance-rules
  namespace: monitoring
spec:
  groups:
  - name: coredns.performance.rules
    rules:
    # 查询延迟监控
    - alert: CoreDNSHighLatency
      expr: histogram_quantile(0.95, rate(coredns_dns_request_duration_seconds_bucket[5m])) > 0.5
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS high latency"
        description: "95th percentile DNS query latency exceeds 500ms"
    
    # 查询成功率监控
    - alert: CoreDNSLowSuccessRate
      expr: rate(coredns_dns_responses_total{rcode="NOERROR"}[5m]) / rate(coredns_dns_responses_total[5m]) < 0.95
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "CoreDNS low success rate"
        description: "DNS query success rate below 95%"
    
    # 吞吐量监控
    - alert: CoreDNSHighQueryRate
      expr: rate(coredns_dns_requests_total[5m]) > 10000
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS high query rate"
        description: "DNS query rate exceeds 10,000 QPS"
```

#### 2.2 缓存指标

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: coredns-cache-rules
  namespace: monitoring
spec:
  groups:
  - name: coredns.cache.rules
    rules:
    # 缓存命中率监控
    - alert: CoreDNSLowCacheHitRate
      expr: rate(coredns_cache_hits_total[5m]) / rate(coredns_dns_requests_total[5m]) < 0.7
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS low cache hit rate"
        description: "DNS cache hit rate below 70%"
    
    # 缓存大小监控
    - alert: CoreDNSCacheSizeHigh
      expr: coredns_cache_entries > 100000
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS cache size high"
        description: "DNS cache entries exceed 100,000"
```

#### 2.3 转发指标

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: coredns-forward-rules
  namespace: monitoring
spec:
  groups:
  - name: coredns.forward.rules
    rules:
    # 转发错误率监控
    - alert: CoreDNSForwardErrorsHigh
      expr: rate(coredns_forward_errors_total[5m]) > 0.01
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "CoreDNS forward errors high"
        description: "DNS forward error rate exceeds 1%"
    
    # 上游DNS响应时间监控
    - alert: CoreDNSUpstreamSlow
      expr: histogram_quantile(0.95, rate(coredns_forward_request_duration_seconds_bucket[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "CoreDNS upstream slow"
        description: "Upstream DNS 95th percentile response time exceeds 1 second"
```

### 3. 日志收集配置

#### 3.1 Fluentd配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-coredns-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*coredns*.log
      pos_file /var/log/fluentd-coredns.log.pos
      tag kubernetes.coredns.*
      read_from_head true
      <parse>
        @type json
        time_key time
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>
    
    <filter kubernetes.coredns.**>
      @type kubernetes_metadata
    </filter>
    
    <match kubernetes.coredns.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      logstash_format true
      logstash_prefix coredns-logs
      <buffer>
        @type file
        path /var/log/fluentd-buffers/coredns.buffer
        flush_mode interval
        retry_type exponential_backoff
        flush_thread_count 2
        flush_interval 5s
        retry_forever
        retry_max_interval 30
        chunk_limit_size 2M
        queue_limit_length 8
        overflow_action block
      </buffer>
    </match>
```

#### 3.2 Loki日志配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: loki-coredns-config
  namespace: logging
data:
  loki.yaml: |
    auth_enabled: false
    
    server:
      http_listen_port: 3100
      
    ingester:
      lifecycler:
        address: 127.0.0.1
        ring:
          kvstore:
            store: inmemory
          replication_factor: 1
        final_sleep: 0s
      chunk_idle_period: 5m
      chunk_retain_period: 30s
      
    schema_config:
      configs:
        - from: 2020-05-15
          store: boltdb
          object_store: filesystem
          schema: v11
          index:
            prefix: index_
            period: 168h
            
    storage_config:
      boltdb:
        directory: /tmp/loki/index
      filesystem:
        directory: /tmp/loki/chunks
        
    limits_config:
      enforce_metric_name: false
      reject_old_samples: true
      reject_old_samples_max_age: 168h
```

---

## 📈 可视化仪表板

### 1. Grafana仪表板配置

```json
{
  "dashboard": {
    "id": null,
    "title": "CoreDNS Monitoring Dashboard",
    "timezone": "browser",
    "panels": [
      {
        "type": "graph",
        "title": "DNS Query Rate",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(coredns_dns_requests_total[5m])",
            "legendFormat": "Queries per second"
          }
        ]
      },
      {
        "type": "singlestat",
        "title": "Cache Hit Rate",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(coredns_cache_hits_total[5m]) / rate(coredns_dns_requests_total[5m]) * 100",
            "legendFormat": "Cache Hit Rate %"
          }
        ]
      },
      {
        "type": "graph",
        "title": "Query Latency (95th percentile)",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(coredns_dns_request_duration_seconds_bucket[5m]))",
            "legendFormat": "Latency (seconds)"
          }
        ]
      },
      {
        "type": "table",
        "title": "Top Queried Domains",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "topk(10, sum by (zone) (rate(coredns_dns_requests_total[5m])))",
            "format": "table"
          }
        ]
      }
    ]
  }
}
```

### 2. 自定义监控面板

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-coredns-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  coredns-dashboard.json: |
    {
      "annotations": {
        "list": [
          {
            "builtIn": 1,
            "datasource": "-- Grafana --",
            "enable": true,
            "hide": true,
            "iconColor": "rgba(0, 211, 255, 1)",
            "name": "Annotations & Alerts",
            "type": "dashboard"
          }
        ]
      },
      "editable": true,
      "gnetId": null,
      "graphTooltip": 0,
      "id": null,
      "links": [],
      "panels": [
        {
          "aliasColors": {},
          "bars": false,
          "dashLength": 10,
          "dashes": false,
          "datasource": "Prometheus",
          "fill": 1,
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 0
          },
          "id": 2,
          "legend": {
            "avg": false,
            "current": false,
            "max": false,
            "min": false,
            "show": true,
            "total": false,
            "values": false
          },
          "lines": true,
          "linewidth": 1,
          "links": [],
          "nullPointMode": "null",
          "percentage": false,
          "pointradius": 5,
          "points": false,
          "renderer": "flot",
          "seriesOverrides": [],
          "spaceLength": 10,
          "stack": false,
          "steppedLine": false,
          "targets": [
            {
              "expr": "rate(coredns_dns_requests_total[5m])",
              "format": "time_series",
              "intervalFactor": 2,
              "legendFormat": "Total Queries",
              "refId": "A"
            },
            {
              "expr": "rate(coredns_cache_hits_total[5m])",
              "format": "time_series",
              "intervalFactor": 2,
              "legendFormat": "Cache Hits",
              "refId": "B"
            }
          ],
          "thresholds": [],
          "timeFrom": null,
          "timeShift": null,
          "title": "DNS Query Statistics",
          "tooltip": {
            "shared": true,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "buckets": null,
            "mode": "time",
            "name": null,
            "show": true,
            "values": []
          },
          "yaxes": [
            {
              "format": "short",
              "label": null,
              "logBase": 1,
              "max": null,
              "min": null,
              "show": true
            },
            {
              "format": "short",
              "label": null,
              "logBase": 1,
              "max": null,
              "min": null,
              "show": true
            }
          ],
          "yaxis": {
            "align": false,
            "alignLevel": null
          }
        }
      ],
      "refresh": "10s",
      "schemaVersion": 16,
      "style": "dark",
      "tags": ["coredns", "dns", "kubernetes"],
      "templating": {
        "list": []
      },
      "time": {
        "from": "now-6h",
        "to": "now"
      },
      "timepicker": {
        "refresh_intervals": [
          "5s",
          "10s",
          "30s",
          "1m",
          "5m",
          "15m",
          "30m",
          "1h",
          "2h",
          "1d"
        ],
        "time_options": [
          "5m",
          "15m",
          "1h",
          "6h",
          "12h",
          "24h",
          "2d",
          "7d",
          "30d"
        ]
      },
      "timezone": "",
      "title": "CoreDNS Monitoring",
      "uid": "coredns-monitoring",
      "version": 1
    }
```

---

## 🤖 自动化运维

### 1. 自愈机制

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coredns-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: coredns-autoscaler
  template:
    metadata:
      labels:
        app: coredns-autoscaler
    spec:
      containers:
      - name: autoscaler
        image: k8s.gcr.io/cluster-proportional-autoscaler-amd64:1.8.5
        resources:
          requests:
            cpu: "20m"
            memory: "10Mi"
        command:
          - /cluster-proportional-autoscaler
          - --namespace=kube-system
          - --configmap=coredns-autoscaler
          - --target=Deployment/coredns
          - --default-params={"linear":{"coresPerReplica":256,"nodesPerReplica":16,"min":2,"max":10}}
          - --logtostderr=true
          - --v=2
```

### 2. 容量规划脚本

```bash
#!/bin/bash
# CoreDNS容量规划分析脚本

echo "📊 CoreDNS Capacity Planning Analysis"
echo "====================================="

# 收集历史数据
echo "1. 收集历史查询量数据..."
kubectl get --raw /api/v1/namespaces/monitoring/services/prometheus-k8s:9090/proxy/api/v1/query?query=rate(coredns_dns_requests_total[1h]) | jq '.data.result[].value[1]' > query_data.txt

# 分析趋势
echo "2. 分析查询量趋势..."
awk '{sum+=$1; count++} END {print "Average queries per second:", sum/count}' query_data.txt

# 预测需求
echo "3. 预测未来资源需求..."
# 基于历史增长率预测
growth_rate=$(awk 'NR==1{prev=$1} {curr=$1; if(NR>1) growth=(curr-prev)/prev; prev=curr; sum+=growth; count++} END {print (sum/count)*100}' query_data.txt)
echo "Predicted growth rate: ${growth_rate}%"

# 生成建议
echo "4. 生成容量规划建议..."
current_replicas=$(kubectl get deployment coredns -n kube-system -o jsonpath='{.spec.replicas}')
recommended_replicas=$((current_replicas + (current_replicas * growth_rate / 100)))
echo "Recommended replica count: $recommended_replicas"
```

---

## 🚨 故障排查工具

### 1. 诊断脚本

```bash
#!/bin/bash
# CoreDNS健康检查脚本

echo "🔧 CoreDNS Health Check"
echo "======================"

# 1. CoreDNS状态检查
echo "📋 CoreDNS状态检查:"
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide

# 2. 指标收集检查
echo ""
echo "📊 指标收集检查:"
kubectl port-forward svc/kube-dns -n kube-system 9153:9153 &
sleep 2
curl -s http://localhost:9153/metrics | head -20
kill %1

# 3. DNS解析测试
echo ""
echo "🌐 DNS解析测试:"
for domain in kubernetes.default google.com github.com; do
    echo "测试解析 $domain:"
    kubectl run dns-test --image=busybox --rm -it -- nslookup $domain 2>&1 | head -5
done

# 4. 日志分析
echo ""
echo "📝 最近错误日志:"
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=50 | grep -i error

# 5. 资源使用检查
echo ""
echo "💾 资源使用情况:"
kubectl top pods -n kube-system -l k8s-app=kube-dns

echo ""
echo "✅ 健康检查完成"
```

### 2. 性能分析工具

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: coredns-performance-test
  namespace: monitoring
spec:
  template:
    spec:
      containers:
      - name: dnsperf
        image: quay.io/ssro/dnsperf:latest
        command:
          - sh
          - -c
          - |
            echo "开始DNS性能测试..."
            # 生成测试查询文件
            echo "google.com A" > queries.txt
            echo "github.com A" >> queries.txt
            echo "kubernetes.default A" >> queries.txt
            
            # 执行性能测试
            dnsperf -s kube-dns.kube-system.svc.cluster.local -d queries.txt -l 60
            
            echo "性能测试完成"
      restartPolicy: Never
```

---

## 📚 扩展阅读

### 官方文档
- [CoreDNS监控指南](https://coredns.io/manual/metrics/)
- [Prometheus监控](https://prometheus.io/docs/guides/coredns/)
- [Grafana仪表板](https://grafana.com/docs/grafana/latest/)

### 相关案例
- [CoreDNS生产部署](../coredns-deployment/)
- [CoreDNS高级特性](../coredns-advanced-features/)
- [CoreDNS安全加固](../security-hardening/)

### 进阶主题
- AI驱动的异常检测
- 预测性维护
- 智能容量规划
- 自动化故障恢复

---

## 📋 清理资源

```bash
# 删除监控配置
kubectl delete -f coredns-monitor.yaml -n monitoring

# 删除测试Job
kubectl delete job coredns-performance-test -n monitoring

# 清理临时资源
kubectl delete namespace coredns-monitoring
```

---

> **💡 提示**: 完善的监控体系是保障CoreDNS稳定运行的关键，建议结合业务特点定制监控策略。
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
