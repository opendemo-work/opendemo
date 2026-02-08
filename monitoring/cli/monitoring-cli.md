# 📊 Monitoring 命令行速查表 (monitoring-cli.md)

> 监控系统必备的命令行参考手册，涵盖Prometheus、Grafana、ELK等主流监控工具，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [Prometheus管理](#prometheus管理)
- [Grafana管理](#grafana管理)
- [ELK栈管理](#elk栈管理)
- [指标收集](#指标收集)
- [告警配置](#告警配置)
- [日志分析](#日志分析)
- [性能监控](#性能监控)
- [容器监控](#容器监控)
- [故障排查](#故障排查)
- [最佳实践](#最佳实践)

---

## Prometheus管理

### 基础操作
```bash
# 启动Prometheus
prometheus --config.file=prometheus.yml

# 重启Prometheus
kill -HUP $(pgrep prometheus)

# 查看Prometheus状态
curl http://localhost:9090/-/healthy
curl http://localhost:9090/-/ready

# 查看targets状态
curl http://localhost:9090/api/v1/targets
```

### 配置管理
```yaml
# prometheus.yml基础配置
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']
```

### 查询和调试
```bash
# PromQL查询示例
# 当前CPU使用率
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 内存使用率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# 磁盘使用率
100 - ((node_filesystem_avail_bytes * 100) / node_filesystem_size_bytes)

# HTTP请求速率
rate(http_requests_total[5m])

# API查询
curl "http://localhost:9090/api/v1/query?query=up"
curl "http://localhost:9090/api/v1/query_range?query=node_cpu_seconds_total&start=$(date -d '1 hour ago' +%s)&end=$(date +%s)&step=15s"
```

---

## Grafana管理

### 基础管理
```bash
# 启动Grafana
systemctl start grafana-server
# 或
docker run -d -p 3000:3000 grafana/grafana

# 默认登录
# 用户名: admin
# 密码: admin

# 重置管理员密码
grafana-cli admin reset-admin-password newpassword

# 查看Grafana状态
curl http://admin:admin@localhost:3000/api/health
```

### 数据源配置
```bash
# 添加Prometheus数据源
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name":"Prometheus",
    "type":"prometheus",
    "url":"http://localhost:9090",
    "access":"proxy",
    "basicAuth":false
  }' \
  http://admin:admin@localhost:3000/api/datasources

# 添加Elasticsearch数据源
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "name":"Elasticsearch",
    "type":"elasticsearch",
    "url":"http://localhost:9200",
    "access":"proxy",
    "database":"[logstash-]YYYY.MM.DD",
    "jsonData": {
      "esVersion": 70,
      "timeField": "@timestamp"
    }
  }' \
  http://admin:admin@localhost:3000/api/datasources
```

### 仪表板管理
```bash
# 导出仪表板
curl http://admin:admin@localhost:3000/api/dashboards/uid/dashboard-uid > dashboard.json

# 导入仪表板
curl -X POST -H "Content-Type: application/json" \
  -d @dashboard.json \
  http://admin:admin@localhost:3000/api/dashboards/db

# 批量导入
for file in dashboards/*.json; do
    curl -X POST -H "Content-Type: application/json" \
      -d @$file \
      http://admin:admin@localhost:3000/api/dashboards/db
done
```

---

## ELK栈管理

### Elasticsearch管理
```bash
# 启动Elasticsearch
systemctl start elasticsearch
# 或
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.17.0

# 健康检查
curl -X GET "localhost:9200/_cluster/health?pretty"

# 查看节点信息
curl -X GET "localhost:9200/_nodes/stats?pretty"

# 创建索引
curl -X PUT "localhost:9200/my-index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  }
}'

# 查看索引列表
curl -X GET "localhost:9200/_cat/indices?v"
```

### Logstash配置
```bash
# 启动Logstash
logstash -f /etc/logstash/conf.d/logstash.conf

# 基础配置示例 logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
  }
  
  date {
    match => [ "timestamp", "ISO8601" ]
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "application-logs-%{+YYYY.MM.dd}"
  }
  
  stdout { codec => rubydebug }
}
```

### Kibana管理
```bash
# 启动Kibana
systemctl start kibana
# 或
docker run -d -p 5601:5601 kibana:7.17.0

# 配置索引模式
curl -X POST "localhost:5601/api/saved_objects/index-pattern" \
  -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d'
{
  "attributes": {
    "title": "application-logs-*",
    "timeFieldName": "@timestamp"
  }
}'
```

---

## 指标收集

### Node Exporter
```bash
# 启动Node Exporter
./node_exporter --web.listen-address=:9100

# 常用指标
# CPU使用率
node_cpu_seconds_total{mode!="idle"}

# 内存使用
node_memory_MemAvailable_bytes
node_memory_MemTotal_bytes

# 磁盘IO
node_disk_reads_completed_total
node_disk_writes_completed_total

# 网络流量
node_network_receive_bytes_total
node_network_transmit_bytes_total
```

### Process Exporter
```bash
# 启动Process Exporter
./process-exporter -config.path=config.yml

# 配置文件 config.yml
process_names:
  - name: "{{.Comm}}"
    cmdline:
      - '.+'
```

### 自定义Exporter
```python
# simple_exporter.py
from prometheus_client import start_http_server, Gauge
import random
import time

# 创建指标
REQUEST_COUNT = Gauge('app_requests_total', 'Total requests')
REQUEST_LATENCY = Gauge('app_request_duration_seconds', 'Request latency')

def collect_metrics():
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.set(random.uniform(0.1, 1.0))

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        collect_metrics()
        time.sleep(1)
```

---

## 告警配置

### Alertmanager配置
```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@example.com'
  smtp_auth_username: 'alerts@example.com'
  smtp_auth_password: 'password'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'team-mails'

receivers:
  - name: 'team-mails'
    email_configs:
      - to: 'team@example.com'
```

### 告警规则示例
```yaml
# rules/alerts.yml
groups:
  - name: example
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% for more than 5 minutes"

      - alert: LowDiskSpace
        expr: (node_filesystem_free_bytes / node_filesystem_size_bytes) * 100 < 10
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space"
          description: "Disk space is below 10%"
```

---

## 日志分析

### Filebeat配置
```yaml
# filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/*.log
    fields:
      service: myapp
    multiline.pattern: '^\['
    multiline.negate: true
    multiline.match: after

output.elasticsearch:
  hosts: ["localhost:9200"]
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"

processors:
  - add_host_metadata: ~
  - add_cloud_metadata: ~
```

### 日志查询示例
```bash
# Elasticsearch查询
# 搜索特定关键词
curl -X GET "localhost:9200/application-logs-*/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "message": "ERROR"
    }
  },
  "sort": [
    {"@timestamp": {"order": "desc"}}
  ],
  "size": 100
}'

# 聚合分析
curl -X GET "localhost:9200/application-logs-*/_search" -H 'Content-Type: application/json' -d'
{
  "aggs": {
    "error_count": {
      "terms": {
        "field": "level.keyword"
      }
    }
  },
  "size": 0
}'
```

---

## 性能监控

### 应用性能监控(APM)
```bash
# Jaeger配置
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 14250:14250 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.35

# Zipkin配置
docker run -d -p 9411:9411 openzipkin/zipkin
```

### 数据库监控
```bash
# MySQL Exporter
docker run -d \
  -p 9104:9104 \
  -e DATA_SOURCE_NAME="user:password@(localhost:3306)/" \
  prom/mysqld-exporter

# PostgreSQL Exporter
docker run -d \
  -p 9187:9187 \
  -e DATA_SOURCE_NAME="postgresql://user:password@localhost:5432/database?sslmode=disable" \
  wrouesnel/postgres_exporter
```

### Redis监控
```bash
# Redis Exporter
docker run -d \
  -p 9121:9121 \
  -e REDIS_ADDR=redis://localhost:6379 \
  oliver006/redis_exporter

# 常用指标
redis_memory_used_bytes
redis_connected_clients
redis_commands_processed_total
```

---

## 容器监控

### Docker监控
```bash
# cAdvisor
docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  gcr.io/cadvisor/cadvisor:latest

# Dockerd Exporter
docker run -d \
  --name docker-exporter \
  -p 9323:9323 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  quay.io/prometheuscommunity/docker-exporter
```

### Kubernetes监控
```bash
# kube-state-metrics
kubectl apply -f https://github.com/kubernetes/kube-state-metrics/releases/latest/download/kube-state-metrics.yaml

# node-exporter DaemonSet
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/master/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml

# Prometheus Operator
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/master/bundle.yaml
```

---

## 故障排查

### 监控系统诊断
```bash
# Prometheus问题排查
# 检查配置文件
promtool check config prometheus.yml

# 检查规则文件
promtool check rules rules/*.yml

# 查看TSDB状态
curl http://localhost:9090/api/v1/status/tsdb

# Grafana问题排查
# 检查数据源连接
curl -X GET http://admin:admin@localhost:3000/api/datasources

# 查看插件状态
grafana-cli plugins ls

# ELK问题排查
# 检查Elasticsearch健康状态
curl -X GET "localhost:9200/_cluster/health?pretty"

# 查看索引状态
curl -X GET "localhost:9200/_cat/indices?v&health=red"
```

### 性能问题分析
```bash
# 系统资源监控
top -p $(pgrep -f "prometheus|elasticsearch|grafana")
iostat -x 1
vmstat 1

# 网络连接检查
ss -tuln | grep -E "(9090|9093|3000|9200)"
netstat -an | grep ESTABLISHED | wc -l

# 日志分析
tail -f /var/log/prometheus/prometheus.log
tail -f /var/log/elasticsearch/elasticsearch.log
journalctl -u grafana-server -f
```

---

## 最佳实践

### 高可用配置
```yaml
# Prometheus HA配置
# 使用Thanos或Cortex实现全局视图
# prometheus.yml
global:
  external_labels:
    cluster: prod
    replica: $(HOSTNAME)

# Alertmanager集群配置
# alertmanager.yml
cluster:
  peers:
    - alertmanager-1:9094
    - alertmanager-2:9094
    - alertmanager-3:9094
```

### 安全配置
```bash
# Prometheus安全
# 启用认证和TLS
# prometheus.yml
scrape_configs:
  - job_name: 'secure-target'
    scheme: https
    tls_config:
      ca_file: /path/to/ca.crt
    basic_auth:
      username: prometheus
      password: secret

# Grafana安全
# 配置LDAP认证
# grafana.ini
[auth.ldap]
enabled = true
config_file = /etc/grafana/ldap.toml
allow_sign_up = false
```

### 自动化运维脚本
```bash
#!/bin/bash
# monitoring_health_check.sh

# Prometheus健康检查
check_prometheus() {
    curl -s http://localhost:9090/-/healthy > /dev/null
    if [ $? -eq 0 ]; then
        echo "Prometheus: OK"
    else
        echo "Prometheus: DOWN"
        # 发送告警
    fi
}

# Grafana健康检查
check_grafana() {
    curl -s http://admin:admin@localhost:3000/api/health > /dev/null
    if [ $? -eq 0 ]; then
        echo "Grafana: OK"
    else
        echo "Grafana: DOWN"
    fi
}

# Elasticsearch健康检查
check_elasticsearch() {
    curl -s localhost:9200/_cluster/health | grep -q '"status":"green"'
    if [ $? -eq 0 ]; then
        echo "Elasticsearch: OK"
    else
        echo "Elasticsearch: WARNING"
    fi
}

# 执行检查
check_prometheus
check_grafana
check_elasticsearch
```

---