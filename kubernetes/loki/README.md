# Loki Log Aggregation

Loki日志聚合系统演示，展示轻量级、云原生的日志收集方案。

## Loki vs ELK

```
架构对比:

ELK Stack:                          Loki Stack:
┌──────────┐                       ┌──────────┐
│ Logstash │  (处理)               │ Promtail │  (收集)
│  (重)    │                       │  (轻量)  │
└────┬─────┘                       └────┬─────┘
     │                                  │
┌────┴─────┐                       ┌────┴─────┐
│Elasticsearch│ (索引)              │  Loki    │  (存储)
│  (全文索引) │                      │  (标签索引)│
└────┬─────┘                       └────┬─────┘
     │                                  │
┌────┴─────┐                       ┌────┴─────┐
│  Kibana  │  (可视化)              │ Grafana  │  (可视化)
└──────────┘                       └──────────┘

特点:
- 索引大小: 1GB日志→500MB索引    1GB日志→<1MB索引
- 资源占用: 高                     低
- 查询: 全文搜索                    标签+grep
- 成本: 高                          低
```

## Loki架构

```
Loki组件:
┌─────────────────────────────────────────────────────┐
│                   Grafana UI                        │
│              (查询和可视化)                          │
└────────────────────┬────────────────────────────────┘
                     │
              ┌──────┴──────┐
              │  Loki Query  │
              │  Frontend    │
              └──────┬──────┘
                     │
              ┌──────┴──────┐
              │    Loki      │
              │   (Querier)  │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│  Ingester  │ │  Ingester  │ │  Ingester  │
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
              ┌──────┴──────┐
              │   Storage    │
              │ (S3/GCS/本地) │
              └───────────────┘
                     ▲
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│  Promtail  │ │  Promtail  │ │  Promtail  │
│ (日志收集) │ │ (日志收集) │ │ (日志收集) │
└────────────┘ └────────────┘ └────────────┘
```

## 安装部署

### Docker Compose
```yaml
version: "3"
services:
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./loki-config.yml:/etc/loki/local-config.yaml
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail:latest
    volumes:
      - ./promtail-config.yml:/etc/promtail/config.yml
      - /var/log:/var/log
    command: -config.file=/etc/promtail/config.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
```

### Loki配置
```yaml
# loki-config.yml
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
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /tmp/loki/boltdb-shipper
    cache_location: /tmp/loki/boltdb-shipper-cache
  filesystem:
    directory: /tmp/loki/chunks

limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h
```

### Promtail配置
```yaml
# promtail-config.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log

  - job_name: application
    static_configs:
      - targets:
          - localhost
        labels:
          job: myapp
          env: production
          __path__: /var/log/myapp/*.log

  # Kubernetes Pod日志
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels:
          - __meta_kubernetes_pod_name
        target_label: pod
      - source_labels:
          - __meta_kubernetes_namespace
        target_label: namespace
```

### Kubernetes部署
```bash
# 使用Helm
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm upgrade --install loki grafana/loki-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.enabled=true

# 获取Grafana密码
kubectl get secret --namespace monitoring loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

## LogQL查询语言

### 基础查询
```logql
# 选择标签
{job="varlogs"}

# 多标签匹配
{job="myapp", env="production"}

# 正则匹配
{job=~"myapp.*"}

# 排除标签
{job!="debug"}
```

### 过滤操作
```logql
# 包含字符串
{job="myapp"} |= "error"

# 不包含
{job="myapp"} != "debug"

# 正则匹配
{job="myapp"} |~ "err.*"

# 组合过滤
{job="myapp"} 
  |= "error" 
  != "timeout" 
  |~ "level=(error|fatal)"
```

### 解析JSON
```logql
# 解析JSON日志
{job="myapp"} 
  | json
  | level="error"
  | line_format "{{.message}}"

# 提取特定字段
{job="myapp"} 
  | json level="level", msg="message", user_id="userId"
  | level="error"
```

### 解析日志格式
```logql
# 解析Apache日志
{job="apache"} 
  | regexp "^(?P<ip>\S+) (?P<ident>\S+) (?P<user>\S+) \[(?P<timestamp>[\w:/]+\s[+\-]\d{4})\] \"(?P<action>\S+)\s?(?P<path>\S+)?\s?(?P<protocol>\S+)?\" (?P<status>\d{3}|-)"
  | status = "500"

# 解析结构化日志
{job="app"} 
  | pattern "<_> level=<level> msg=<msg> user=<user> <_>"
```

### 聚合查询
```logql
# 统计错误率
sum(rate({job="myapp"} |= "error" [1m]))

# TopK错误
sum by (pod) (rate({job="myapp"} |= "error" [5m]))

# 直方图
sum by (le) (histogram_quantile(0.95, 
  sum(rate({job="myapp"} | json | unwrap duration [5m])) by (le)
))
```

## Grafana集成

### 数据源配置
```yaml
# provisioning/datasources/loki.yml
apiVersion: 1
datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    jsonData:
      maxLines: 1000
```

### 创建日志面板
```json
{
  "targets": [
    {
      "expr": "{job=\"myapp\"} |= \"error\"",
      "refId": "A"
    }
  ],
  "type": "logs",
  "title": "Error Logs"
}
```

## 告警配置

```yaml
# 使用Loki Ruler
ruler:
  alertmanager_url: http://alertmanager:9093
  
  storage:
    type: local
    local:
      directory: /etc/loki/rules
      
  rule_path: /tmp/loki/rules
  
  ring:
    kvstore:
      store: inmemory
```

```yaml
# /etc/loki/rules/fake/rules.yml
groups:
  - name: error_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate({job="myapp"} |= "error" [5m])) by (namespace) > 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate in {{ $labels.namespace }}"
          description: "Error rate: {{ $value }} errors/second"
```

## 学习要点

1. Loki与ELK的架构差异
2. LogQL查询语法
3. 标签设计和索引优化
4. 日志解析和结构化
5. 告警规则配置
