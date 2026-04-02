# Prometheus and Grafana

Prometheus监控与Grafana可视化集成演示。

## 架构概览

```
Prometheus架构:
┌─────────────────────────────────────────────────────────┐
│                   Prometheus Server                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   TSDB      │  │  Retriever  │  │    HTTP     │     │
│  │  (存储)      │  │  (抓取)      │  │   Server    │     │
│  └─────────────┘  └──────┬──────┘  └─────────────┘     │
└──────────────────────────┼──────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────┴────┐        ┌────┴────┐       ┌────┴────┐
   │ Exporter│        │ Exporter│       │ Exporter│
   │(Node)   │        │(MySQL)  │       │(Custom) │
   └─────────┘        └─────────┘       └─────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
              ┌────────────┴────────────┐
              │       Alertmanager      │
              └────────────┬────────────┘
                           │
              ┌────────────┴────────────┐
              │       Grafana           │
              │     (可视化)             │
              └─────────────────────────┘
```

## 安装Prometheus

### 使用Helm
```bash
# 添加仓库
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 安装Prometheus
helm install prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --create-namespace

# 安装kube-prometheus-stack (推荐)
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### 基础配置
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

## PromQL查询

### 基础查询
```promql
# CPU使用率
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance) * 100)

# 内存使用率
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# 磁盘使用率
100 - ((node_filesystem_avail_bytes{mountpoint="/"} * 100) / node_filesystem_size_bytes{mountpoint="/"})

# 网络流量
rate(node_network_receive_bytes_total[5m])
```

### 聚合操作
```promql
# 按实例分组统计CPU
avg by (instance) (rate(node_cpu_seconds_total[5m]))

# 百分位数
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# 增长预测
predict_linear(node_filesystem_avail_bytes[1h], 3600 * 4)
```

## 告警规则

```yaml
# prometheus-rules.yml
groups:
  - name: node-alerts
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 80% (current value: {{ $value }}%)"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is above 85% (current value: {{ $value }}%)"

      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Disk space is below 10% (current value: {{ $value }}%)"
```

## Alertmanager配置

```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alert@example.com'

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 12h
  receiver: 'email'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'

receivers:
  - name: 'email'
    email_configs:
      - to: 'ops@example.com'
        headers:
          Subject: 'Prometheus Alert: {{ .GroupLabels.alertname }}'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<pagerduty-key>'
```

## Grafana安装配置

### 安装
```bash
# Helm安装
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set persistence.enabled=true

# 获取密码
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

### 数据源配置
```yaml
# grafana-datasource.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

### 常用Dashboard

#### Node Exporter Full
- ID: 1860
- 全面的节点监控仪表板

#### Kubernetes Cluster
- ID: 7249
- K8s集群整体视图

#### MySQL Overview
- ID: 7362
- MySQL数据库监控

#### Nginx Ingress Controller
- ID: 9614
- Ingress流量分析

## 自定义Exporter

### Python示例
```python
from prometheus_client import start_http_server, Gauge
import random
import time

# 创建指标
REQUEST_TIME = Gauge('app_request_time_seconds', 'Request processing time')
ACTIVE_CONNECTIONS = Gauge('app_active_connections', 'Active connections')

def process_request():
    REQUEST_TIME.set(random.random())
    ACTIVE_CONNECTIONS.set(random.randint(0, 100))

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        process_request()
        time.sleep(1)
```

### 部署到K8s
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: custom-exporter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: exporter
  template:
    metadata:
      labels:
        app: exporter
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
    spec:
      containers:
      - name: exporter
        image: my-exporter:latest
        ports:
        - containerPort: 8000
```

## 常用Exporter

| Exporter | 用途 | 端口 |
|---------|------|------|
| node-exporter | 主机指标 | 9100 |
| kube-state-metrics | K8s资源状态 | 8080 |
| mysqld-exporter | MySQL指标 | 9104 |
| redis-exporter | Redis指标 | 9121 |
| blackbox-exporter | 黑盒探测 | 9115 |
| nginx-exporter | Nginx指标 | 9113 |

## 学习要点

1. 数据模型和时序数据库
2. PromQL查询语言
3. 告警规则配置
4. Grafana仪表板设计
5. 自定义指标暴露
