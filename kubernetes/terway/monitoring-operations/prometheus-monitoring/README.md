# 📊 Terway 监控运维完整体系

> 企业级阿里云Terway网络插件监控、告警、日志和运维管理完整解决方案

## 📋 案例概述

本案例提供阿里云Terway网络插件的企业级监控运维体系，涵盖从基础指标收集到智能告警的全方位内容，确保在生产环境中能够及时发现问题并快速响应。

### 🔧 核心能力覆盖

- **指标收集**: ENI状态、网络性能、QoS指标
- **日志管理**: 网络日志、错误日志、安全审计日志
- **告警策略**: 性能异常、服务中断、安全威胁告警
- **可视化展示**: Grafana仪表板、自定义监控视图
- **自动化运维**: 自愈机制、容量规划、性能优化
- **故障排查**: 诊断工具、根因分析、修复建议

### 🎯 适用场景

- 生产环境网络监控
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
kubectl create namespace terway-monitoring
```

### 2. 基础监控配置

```bash
# 部署Terway监控配置
kubectl apply -f terway-monitor.yaml -n monitoring

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
  name: terway-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: terway
  namespaceSelector:
    matchNames:
      - kube-system
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
    relabelings:
    - sourceLabels: [__meta_kubernetes_pod_node_name]
      targetLabel: node
    - sourceLabels: [__meta_kubernetes_pod_name]
      targetLabel: pod
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'terway_(eni|network|qos|security)_.*'
      action: keep
```

#### 1.2 自定义指标收集

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-custom-metrics
  namespace: kube-system
data:
  metrics_config: |
    {
      "custom_metrics": [
        {
          "name": "terway_eni_utilization_ratio",
          "help": "ENI utilization ratio",
          "type": "gauge",
          "labels": ["node", "eni_id"],
          "query": "terway_eni_allocated_ips / terway_eni_total_ips"
        },
        {
          "name": "terway_network_packet_loss_rate",
          "help": "Network packet loss rate",
          "type": "gauge",
          "labels": ["node", "interface"],
          "query": "rate(terway_network_packets_dropped_total[5m]) / rate(terway_network_packets_total[5m])"
        },
        {
          "name": "terway_qos_violation_count",
          "help": "QoS violation count",
          "type": "counter",
          "labels": ["node", "priority_class"],
          "query": "terway_qos_violations_total"
        }
      ]
    }
```

### 2. 关键指标定义

#### 2.1 性能指标

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: terway-performance-rules
  namespace: monitoring
spec:
  groups:
  - name: terway.performance.rules
    rules:
    # 网络延迟监控
    - alert: TerwayHighLatency
      expr: histogram_quantile(0.95, rate(terway_network_latency_seconds_bucket[5m])) > 0.05
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Terway high latency"
        description: "95th percentile network latency exceeds 50ms"
    
    # 网络吞吐量监控
    - alert: TerwayHighThroughput
      expr: rate(terway_network_bytes_total[5m]) > 1e9
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: "Terway high throughput"
        description: "Network throughput exceeds 1GB/s"
    
    # ENI利用率监控
    - alert: TerwayHighENIUtilization
      expr: terway_eni_allocated_ips / terway_eni_total_ips > 0.8
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Terway high ENI utilization"
        description: "ENI IP allocation ratio exceeds 80%"
```

#### 2.2 QoS指标

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: terway-qos-rules
  namespace: monitoring
spec:
  groups:
  - name: terway.qos.rules
    rules:
    # QoS违规监控
    - alert: TerwayQoSViolations
      expr: rate(terway_qos_violations_total[5m]) > 10
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Terway QoS violations"
        description: "QoS violations exceed 10 per minute"
    
    # 带宽超限监控
    - alert: TerwayBandwidthExceeded
      expr: terway_network_current_bandwidth_bytes > terway_network_allocated_bandwidth_bytes * 1.1
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: "Terway bandwidth exceeded"
        description: "Current bandwidth usage exceeds allocated bandwidth by 10%"
```

#### 2.3 安全指标

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: terway-security-rules
  namespace: monitoring
spec:
  groups:
  - name: terway.security.rules
    rules:
    # 网络隔离违规监控
    - alert: TerwayNetworkIsolationBreach
      expr: terway_network_isolation_violations_total > 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Terway network isolation breach"
        description: "Network isolation policy violations detected"
    
    # 安全组同步失败监控
    - alert: TerwaySecurityGroupSyncFailure
      expr: rate(terway_security_group_sync_failures_total[5m]) > 0.1
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Terway security group sync failure"
        description: "Security group synchronization failure rate exceeds 10%"
```

### 3. 日志收集配置

#### 3.1 Fluentd配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-terway-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/terway/*.log
      pos_file /var/log/fluentd-terway.log.pos
      tag kubernetes.terway.*
      read_from_head true
      <parse>
        @type json
        time_key time
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>
    
    <filter kubernetes.terway.**>
      @type kubernetes_metadata
    </filter>
    
    <match kubernetes.terway.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      logstash_format true
      logstash_prefix terway-logs
      <buffer>
        @type file
        path /var/log/fluentd-buffers/terway.buffer
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
  name: loki-terway-config
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
    "title": "Terway Monitoring Dashboard",
    "timezone": "browser",
    "panels": [
      {
        "type": "graph",
        "title": "Network Throughput",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(terway_network_bytes_total[5m])",
            "legendFormat": "Bytes per second"
          }
        ]
      },
      {
        "type": "singlestat",
        "title": "ENI Utilization",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "terway_eni_allocated_ips / terway_eni_total_ips * 100",
            "legendFormat": "ENI Utilization %"
          }
        ]
      },
      {
        "type": "graph",
        "title": "Network Latency (95th percentile)",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(terway_network_latency_seconds_bucket[5m]))",
            "legendFormat": "Latency (seconds)"
          }
        ]
      },
      {
        "type": "table",
        "title": "Top Network Consumers",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "topk(10, sum by (pod, namespace) (rate(terway_network_bytes_total[5m])))",
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
  name: grafana-terway-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  terway-dashboard.json: |
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
              "expr": "rate(terway_network_bytes_total[5m])",
              "format": "time_series",
              "intervalFactor": 2,
              "legendFormat": "Network Throughput",
              "refId": "A"
            }
          ],
          "thresholds": [],
          "timeFrom": null,
          "timeShift": null,
          "title": "Network Performance Metrics",
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
              "format": "Bps",
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
      "tags": ["terway", "network", "kubernetes"],
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
      "title": "Terway Monitoring",
      "uid": "terway-monitoring",
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
  name: terway-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: terway-autoscaler
  template:
    metadata:
      labels:
        app: terway-autoscaler
    spec:
      containers:
      - name: autoscaler
        image: terway/autoscaler:latest
        env:
        - name: MIN_ENI_COUNT
          value: "2"
        - name: MAX_ENI_COUNT
          value: "10"
        - name: SCALE_UP_THRESHOLD
          value: "0.8"
        - name: SCALE_DOWN_THRESHOLD
          value: "0.3"
        volumeMounts:
        - name: config
          mountPath: /etc/autoscaler
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
          name: terway-autoscaler-config
```

### 2. 容量规划脚本

```bash
#!/bin/bash
# Terway容量规划分析脚本

echo "📊 Terway Capacity Planning Analysis"
echo "==================================="

# 收集历史数据
echo "1. 收集历史网络使用数据..."
kubectl get --raw /api/v1/namespaces/monitoring/services/prometheus-k8s:9090/proxy/api/v1/query?query=rate(terway_network_bytes_total[1h]) | jq '.data.result[].value[1]' > network_data.txt

# 分析趋势
echo "2. 分析网络使用趋势..."
awk '{sum+=$1; count++} END {print "Average network throughput:", sum/count/1024/1024 " MB/s"}' network_data.txt

# 预测需求
echo "3. 预测未来资源需求..."
growth_rate=$(awk 'NR==1{prev=$1} {curr=$1; if(NR>1) growth=(curr-prev)/prev; prev=curr; sum+=growth; count++} END {print (sum/count)*100}' network_data.txt)
echo "Predicted growth rate: ${growth_rate}%"

# 生成建议
echo "4. 生成容量规划建议..."
current_nodes=$(kubectl get nodes --no-headers | wc -l)
recommended_enis=$((current_nodes * 3))
echo "Recommended ENI count: $recommended_enis"
```

---

## 🚨 故障排查工具

### 1. 诊断脚本

```bash
#!/bin/bash
# Terway健康检查脚本

echo "🔧 Terway Health Check"
echo "====================="

# 1. Terway状态检查
echo "📋 Terway状态检查:"
kubectl get pods -n kube-system -l app=terway -o wide

# 2. 指标收集检查
echo ""
echo "📊 指标收集检查:"
kubectl port-forward svc/terway-metrics -n kube-system 9100:9100 &
sleep 2
curl -s http://localhost:9100/metrics | head -20
kill %1

# 3. 网络连通性测试
echo ""
echo "🌐 网络连通性测试:"
for pod in $(kubectl get pods -n terway-monitoring -o jsonpath='{.items[*].metadata.name}'); do
    echo "测试Pod: $pod"
    kubectl exec $pod -n terway-monitoring -- ping -c 3 8.8.8.8 2>&1 | head -5
done

# 4. 日志分析
echo ""
echo "📝 最近错误日志:"
kubectl logs -n kube-system -l app=terway --tail=50 | grep -i error

# 5. 资源使用检查
echo ""
echo "💾 资源使用情况:"
kubectl top pods -n kube-system -l app=terway

echo ""
echo "✅ 健康检查完成"
```

### 2. 性能分析工具

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: terway-performance-test
  namespace: monitoring
spec:
  template:
    spec:
      containers:
      - name: network-perf
        image: networkstatic/iperf3:latest
        command:
          - sh
          - -c
          - |
            echo "开始网络性能测试..."
            
            # 执行iperf3测试
            iperf3 -c terway-server.terway-monitoring.svc.cluster.local -t 60 -P 4
            
            # 执行ping测试
            ping -c 100 terway-server.terway-monitoring.svc.cluster.local
            
            echo "性能测试完成"
      restartPolicy: Never
```

---

## 📚 扩展阅读

### 官方文档
- [Terway监控指南](https://github.com/AliyunContainerService/terway/tree/master/docs)
- [Prometheus监控](https://prometheus.io/docs/guides/terway/)
- [Grafana仪表板](https://grafana.com/docs/grafana/latest/)

### 相关案例
- [Terway生产部署](../deployment/terway-deployment/)
- [Terway高级特性](../advanced-features/custom-networking/)
- [Terway安全加固](../security-hardening/)

### 进阶主题
- AI驱动的异常检测
- 预测性维护
- 智能容量规划
- 自动化故障恢复

---

## 📋 清理资源

```bash
# 删除监控配置
kubectl delete -f terway-monitor.yaml -n monitoring

# 删除测试Job
kubectl delete job terway-performance-test -n monitoring

# 清理临时资源
kubectl delete namespace terway-monitoring
```

---

> **💡 提示**: 完善的监控体系是保障Terway稳定运行的关键，建议结合业务特点定制监控策略。
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
