# Prometheus 指标收集演示

## 🎯 概述

本演示展示了如何使用Prometheus进行全面的系统和服务监控，包括自定义指标收集、服务发现、告警规则配置和联邦集群设置。

## 🏗️ 技术架构

### 核心组件
- **主要技术**: Prometheus 2.40+, Alertmanager, Node Exporter
- **适用场景**: 系统监控、应用性能监控、告警管理
- **难度等级**: 🔴 高级

### 技术栈
```yaml
monitoring_stack:
  - prometheus: "2.40"
  - alertmanager: "0.25"
  - node_exporter: "1.5"
  - blackbox_exporter: "0.24"
  - grafana: "9.3"

exporters:
  - node_exporter: "系统指标"
  - cadvisor: "容器指标"
  - blackbox_exporter: "黑盒监控"
  - custom_exporter: "自定义指标"
```

## 🚀 快速开始

### 环境部署
```bash
# 进入监控目录
cd monitoring/prometheus-metrics-collection

# 启动完整监控栈
docker-compose up -d

# 验证服务状态
docker-compose ps
```

### 访问监控界面
- **Prometheus**: http://localhost:9090
- **Alertmanager**: http://localhost:9093
- **Grafana**: http://localhost:3000 (admin/admin)

## 🔧 核心功能演示

### 1. 自定义指标收集
```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # 应用指标收集
  - job_name: 'application-metrics'
    static_configs:
      - targets: ['app-exporter:8080']
    metrics_path: '/metrics'
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
      - source_labels: [__meta_docker_container_name]
        target_label: container

  # 黑盒监控
  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
        - http://example.com
        - https://api.example.com
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115
```

### 2. 告警规则配置
```yaml
# rules/application_alerts.yml
groups:
- name: application.rules
  rules:
  - alert: HighRequestLatency
    expr: job:request_latency_seconds:mean5m{job="myapp"} > 0.5
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High request latency detected"
      description: "{{ $labels.instance }} has latency > 0.5s for 10 minutes"

  - alert: ApplicationDown
    expr: up{job="myapp"} == 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Application is down"
      description: "{{ $labels.instance }} has been down for 5 minutes"
```

### 3. 服务发现配置
```yaml
# 使用文件服务发现
- job_name: 'file-sd'
  file_sd_configs:
  - files:
    - /etc/prometheus/file_sd/*.json
    refresh_interval: 5m

# JSON格式的服务发现文件
[
  {
    "targets": ["10.1.2.3:9100", "10.1.2.4:9100"],
    "labels": {
      "job": "node",
      "region": "us-west",
      "env": "production"
    }
  }
]
```

## 📊 自定义Exporter开发

### Go语言Exporter示例
```go
package main

import (
    "log"
    "net/http"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    httpRequestTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )
    
    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
)

func init() {
    prometheus.MustRegister(httpRequestTotal)
    prometheus.MustRegister(httpRequestDuration)
}

func main() {
    http.HandleFunc("/api/users", func(w http.ResponseWriter, r *http.Request) {
        timer := prometheus.NewTimer(httpRequestDuration.WithLabelValues(r.Method, "/api/users"))
        defer timer.ObserveDuration()
        
        // 处理业务逻辑
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("OK"))
        
        httpRequestTotal.WithLabelValues(r.Method, "/api/users", "200").Inc()
    })
    
    http.Handle("/metrics", promhttp.Handler())
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

## 🔍 查询示例

### 常用PromQL查询
```promql
# 系统CPU使用率
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 内存使用率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# 磁盘IO利用率
irate(node_disk_io_time_seconds_total[5m]) * 100

# HTTP请求速率
rate(http_requests_total[5m])

# 95百分位响应时间
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# 容器内存使用
container_memory_usage_bytes{container!="POD", container!=""}

# 服务可用性
up == 0
```

## 🚨 告警配置

### Alertmanager配置
```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@example.com'
  smtp_auth_username: 'alerts@example.com'
  smtp_auth_password: 'your-password'

route:
  group_by: ['alertname', 'cluster']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 3h
  receiver: 'team-mails'

receivers:
- name: 'team-mails'
  email_configs:
  - to: 'team@example.com'
    send_resolved: true
  
  webhook_configs:
  - url: 'http://webhook.example.com/alerts'
    send_resolved: true

  slack_configs:
  - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
    channel: '#alerts'
    send_resolved: true
```

## 🧪 测试验证

### 监控测试脚本
```bash
#!/bin/bash
# test-monitoring.sh

echo "Testing Prometheus Monitoring Setup..."

# 检查Prometheus是否运行
if curl -s http://localhost:9090/-/healthy | grep "Prometheus"; then
    echo "✓ Prometheus is running"
else
    echo "✗ Prometheus is not accessible"
    exit 1
fi

# 检查指标收集
targets=$(curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets | length')
echo "Active targets: $targets"

# 测试告警规则
rules=$(curl -s http://localhost:9090/api/v1/rules | jq '.data.groups | length')
echo "Alert rule groups: $rules"

# 检查是否有告警触发
alerts=$(curl -s http://localhost:9090/api/v1/alerts | jq '.data.alerts | length')
echo "Active alerts: $alerts"

echo "Monitoring tests completed!"
```

## 📈 性能优化

### Prometheus配置优化
```yaml
# prometheus.yml 性能优化
global:
  scrape_interval: 30s  # 根据需要调整
  scrape_timeout: 10s
  evaluation_interval: 30s

storage:
  tsdb:
    retention.time: 15d
    wal-compression: true

query:
  max-concurrency: 20
  timeout: 2m

# 启用远程写入
remote_write:
  - url: "http://remote-storage:9090/api/v1/write"
    queue_config:
      capacity: 10000
      max_shards: 50
      max_samples_per_send: 1000
```

## 🚀 生产部署

### Kubernetes部署配置
```yaml
# k8s/prometheus-deployment.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: prometheus
spec:
  serviceName: prometheus
  replicas: 2
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:v2.40.0
        args:
          - '--config.file=/etc/prometheus/prometheus.yml'
          - '--storage.tsdb.path=/prometheus'
          - '--web.console.libraries=/etc/prometheus/console_libraries'
          - '--web.console.templates=/etc/prometheus/consoles'
          - '--storage.tsdb.retention.time=30d'
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config-volume
          mountPath: /etc/prometheus
        - name: storage-volume
          mountPath: /prometheus
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
```

## 📚 相关资源

### 官方文档
- [Prometheus官方文档](https://prometheus.io/docs/)
- [PromQL查询指南](https://prometheus.io/docs/prometheus/latest/querying/basics/)

### 学习资源
- 《Prometheus监控实战》
- 监控系统设计最佳实践

---
*最后更新: 2026年2月3日*