# 📊 Kubernetes Service 监控运维完整指南

> 企业级 Service 监控、告警、日志和运维管理完整解决方案

## 📋 案例概述

本案例提供 Kubernetes Service 的企业级监控运维体系，涵盖从基础指标收集到智能告警的全方位内容，确保在生产环境中能够及时发现问题并快速响应。

### 🔧 核心能力覆盖

- **指标收集**: Service指标、端点状态、连接统计
- **日志管理**: 访问日志、错误日志、调试日志
- **告警策略**: 异常检测、阈值告警、预测性告警
- **可视化展示**: Grafana仪表板、自定义视图
- **自动化运维**: 自愈机制、容量规划、性能优化
- **故障排查**: 诊断工具、根因分析、修复建议

### 🎯 适用场景

- 生产环境监控
- 性能瓶颈分析
- 故障预警和自愈
- 容量规划和优化
- 合规审计和报告

---

## 🚀 快速开始

### 1. 环境准备

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 检查监控组件状态
kubectl get pods -n monitoring

# 验证Prometheus和Grafana部署
kubectl get svc -n monitoring prometheus-k8s grafana

# 创建监控专用命名空间
kubectl create namespace service-monitoring
```

### 2. 基础监控配置

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 部署Service监控配置
kubectl apply -f service-monitor.yaml -n monitoring

# 验证监控目标发现
kubectl port-forward svc/prometheus-k8s -n monitoring 9090:9090
# 访问 http://localhost:9090/targets
```

---

## 📊 核心监控体系

### 1. Service指标收集

#### 1.1 基础指标配置

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: kubernetes-services
  namespace: monitoring
spec:
  selector:
    matchLabels:
      k8s-app: kubelet
  namespaceSelector:
    matchNames:
      - default
      - production
  endpoints:
    - port: https-metrics
      scheme: https
      interval: 30s
      tlsConfig:
        caFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        insecureSkipVerify: true
      bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabelings:
        - sourceLabels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
          action: keep
          regex: true
        - sourceLabels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
          action: replace
          targetLabel: __address__
          regex: ([^:]+)(?::\d+)?;(\d+)
          replacement: $1:$2
```

#### 1.2 自定义Service监控

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: application-services
  namespace: monitoring
spec:
  selector:
    matchExpressions:
      - key: app
        operator: Exists
  namespaceSelector:
    any: true
  endpoints:
    - port: http-metrics
      path: /metrics
      interval: 15s
      scrapeTimeout: 10s
      metricRelabelings:
        # 过滤掉不必要的指标
        - sourceLabels: [__name__]
          action: drop
          regex: go_.*
        - sourceLabels: [__name__]
          action: drop
          regex: process_.*
```

### 2. 关键指标定义

#### 2.1 Service健康指标

```yaml
# Prometheus告警规则
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: service-health-rules
  namespace: monitoring
spec:
  groups:
    - name: service.health.rules
      rules:
        # Service可用性监控
        - alert: ServiceDown
          expr: kube_service_spec_type > 0 unless kube_endpoint_address_available > 0
          for: 2m
          labels:
            severity: critical
          annotations:
            summary: "Service {{ $labels.namespace }}/{{ $labels.service }} is down"
            description: "Service has no available endpoints for more than 2 minutes"
        
        # 端点健康检查
        - alert: EndpointUnhealthy
          expr: kube_pod_status_ready{condition="true"} == 0
          for: 1m
          labels:
            severity: warning
          annotations:
            summary: "Endpoint {{ $labels.pod }} is unhealthy"
            description: "Pod is not ready for service {{ $labels.service }}"
        
        # 连接数异常
        - alert: HighConnectionCount
          expr: rate(kube_service_connection_total[5m]) > 1000
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High connection count for service {{ $labels.service }}"
            description: "Service is handling more than 1000 connections per second"
```

#### 2.2 性能指标

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: service-performance-rules
  namespace: monitoring
spec:
  groups:
    - name: service.performance.rules
      rules:
        # 响应时间监控
        - alert: HighResponseTime
          expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High response time for service {{ $labels.service }}"
            description: "95th percentile response time exceeds 2 seconds"
        
        # 错误率监控
        - alert: HighErrorRate
          expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
          for: 2m
          labels:
            severity: critical
          annotations:
            summary: "High error rate for service {{ $labels.service }}"
            description: "Error rate exceeds 5% in the last 5 minutes"
        
        # CPU使用率
        - alert: HighCPUUsage
          expr: rate(container_cpu_usage_seconds_total[5m]) > 0.8
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "High CPU usage for service {{ $labels.service }}"
            description: "CPU usage exceeds 80% for more than 10 minutes"
```

### 3. 日志收集配置

#### 3.1 Fluentd配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*_service-*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_key time
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>
    
    <filter kubernetes.**>
      @type kubernetes_metadata
    </filter>
    
    <match kubernetes.var.log.containers.**service**.log>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      logstash_format true
      logstash_prefix service-logs
      <buffer>
        @type file
        path /var/log/fluentd-buffers/kubernetes.system.buffer
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
  name: loki-config
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
    "title": "Kubernetes Services Overview",
    "timezone": "browser",
    "panels": [
      {
        "type": "graph",
        "title": "Service Request Rate",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "type": "singlestat",
        "title": "Total Services",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "count(kube_service_created)"
          }
        ]
      },
      {
        "type": "table",
        "title": "Service Health Status",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "kube_service_status_load_balancer_ingress > 0",
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
  name: grafana-dashboard-service-overview
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  service-overview.json: |
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
              "expr": "sum(rate(container_cpu_usage_seconds_total{container!=\"POD\",container!=\"\"}[5m])) by (pod)",
              "format": "time_series",
              "intervalFactor": 2,
              "legendFormat": "{{pod}}",
              "refId": "A"
            }
          ],
          "thresholds": [],
          "timeFrom": null,
          "timeShift": null,
          "title": "CPU Usage by Pod",
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
      "tags": [],
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
      "title": "Service Overview",
      "uid": "service-overview",
      "version": 1
    }
```

---

## 🤖 自动化运维

### 1. 自愈机制

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: service-autoscaler
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: service-deployment
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
```

### 2. 容量规划脚本

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 容量规划分析脚本

echo "📊 Service Capacity Planning Analysis"
echo "====================================="

# 收集历史数据
echo "1. 收集历史资源使用数据..."
kubectl top pods -n production | grep service

# 分析趋势
echo "2. 分析资源使用趋势..."
prometheus_query="
  avg_over_time(
    rate(container_cpu_usage_seconds_total{namespace='production'}[1h])
  [7d:])
"

# 预测需求
echo "3. 预测未来资源需求..."
# 这里可以集成机器学习模型进行预测

# 生成建议
echo "4. 生成容量规划建议..."
echo "建议增加节点数量: 2"
echo "建议调整HPA阈值: CPU 65%, Memory 75%"
```

---

## 🚨 故障排查工具

### 1. 诊断脚本

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# Service健康检查脚本

echo "🔧 Service Health Check"
echo "======================"

# 1. Service状态检查
echo "📋 Service状态检查:"
kubectl get services -n production -o wide

# 2. Endpoint状态检查
echo ""
echo "🔌 Endpoint状态检查:"
kubectl get endpoints -n production

# 3. Pod就绪状态检查
echo ""
echo "🏃 Pod就绪状态检查:"
kubectl get pods -n production -l app=service -o wide

# 4. 网络连通性检查
echo ""
echo "🌐 网络连通性检查:"
for pod in $(kubectl get pods -n production -l app=service -o jsonpath='{.items[*].metadata.name}'); do
    echo "检查Pod: $pod"
    kubectl exec $pod -n production -- nc -zv service.production.svc.cluster.local 80 2>&1 || echo "  连接失败"
done

# 5. 日志分析
echo ""
echo "📝 最近错误日志:"
kubectl logs -n production -l app=service --tail=50 | grep -i error

echo ""
echo "✅ 健康检查完成"
```

### 2. 性能分析工具

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: service-performance-test
  namespace: monitoring
spec:
  template:
    spec:
      containers:
        - name: performance-test
          image: busybox
          command:
            - sh
            - -c
            - |
              echo "开始性能测试..."
              for i in $(seq 1 1000); do
                wget -qO- http://service.production.svc.cluster.local:80/health
              done
              echo "性能测试完成"
      restartPolicy: Never
```

---

## 📚 扩展阅读

### 官方文档
- [Prometheus监控指南](https://prometheus.io/docs/guides/kubernetes/)
- [Grafana仪表板](https://grafana.com/docs/grafana/latest/)
- [Fluentd日志收集](https://docs.fluentd.org/)

### 相关案例
- [Service控制器管理](../controllers/core-controllers/)
- [Service高级特性](../advanced-features/custom-resources/)
- [Service安全加固](../security-hardening/)

### 进阶主题
- AI驱动的异常检测
- 预测性维护
- 智能容量规划
- 自动化故障恢复

---

## 📋 清理资源

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 删除监控配置
kubectl delete -f service-monitor.yaml -n monitoring

# 删除测试Job
kubectl delete job service-performance-test -n monitoring

# 清理临时资源
kubectl delete namespace service-monitoring
```

---

> **💡 提示**: 完善的监控体系是保障Service稳定运行的关键，建议结合业务特点定制监控策略。
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
