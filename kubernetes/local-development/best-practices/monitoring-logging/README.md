# 📊 Kubernetes 本地开发监控和日志最佳实践

> 本地 Kubernetes 环境的监控、日志收集与分析完整指南

## 🎯 监控和日志概述

在本地 Kubernetes 开发环境中建立完善的监控和日志系统，可以帮助开发者快速发现问题、优化性能并提高应用可靠性。

### 📋 核心目标
- **实时监控**：持续监控集群和应用状态
- **日志收集**：集中收集和管理应用日志
- **性能分析**：分析系统性能瓶颈
- **故障诊断**：快速定位和解决问题
- **容量规划**：基于数据进行资源规划

## 🚀 本地监控栈部署

### 1. Prometheus + Grafana 监控栈

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 部署 Prometheus 监控栈
setup_prometheus_monitoring() {
    # 创建监控命名空间
    kubectl create namespace monitoring
    
    # 使用 Prometheus Operator 部署
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    
    # 安装 Prometheus Operator
    helm install prometheus prometheus-community/kube-prometheus-stack \
        --namespace monitoring \
        --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
        --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false
    
    # 等待组件就绪
    kubectl wait --for=condition=available deployment/prometheus-grafana -n monitoring --timeout=300s
    kubectl wait --for=condition=available statefulset/prometheus-prometheus-kube-prometheus-prometheus -n monitoring --timeout=300s
    
    echo "Prometheus 监控栈部署完成"
    echo "Grafana 访问: kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80"
    echo "默认用户名: admin, 密码: prom-operator"
}

# 本地开发友好的 Prometheus 配置
create_local_prometheus_config() {
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-local-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - "alert.rules"
    
    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - alertmanager:9093
    
    scrape_configs:
      - job_name: 'kubernetes-apiservers'
        kubernetes_sd_configs:
        - role: endpoints
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabel_configs:
        - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
          action: keep
          regex: default;kubernetes;https
    
      - job_name: 'kubernetes-nodes'
        kubernetes_sd_configs:
        - role: node
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabel_configs:
        - action: labelmap
          regex: __meta_kubernetes_node_label_(.+)
        - target_label: __address__
          replacement: kubernetes.default.svc:443
        - source_labels: [__meta_kubernetes_node_name]
          regex: (.+)
          target_label: __metrics_path__
          replacement: /api/v1/nodes/\${1}/proxy/metrics
    
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
        - role: pod
        relabel_configs:
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
          action: keep
          regex: true
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
          action: replace
          target_label: __metrics_path__
          regex: (.+)
        - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
          action: replace
          regex: ([^:]+)(?::\d+)?;(\d+)
          replacement: \$1:\$2
          target_label: __address__
        - action: labelmap
          regex: __meta_kubernetes_pod_label_(.+)
        - source_labels: [__meta_kubernetes_namespace]
          action: replace
          target_label: kubernetes_namespace
        - source_labels: [__meta_kubernetes_pod_name]
          action: replace
          target_label: kubernetes_pod_name
EOF
}

# 应用监控配置
setup_application_monitoring() {
    # 为应用添加 Prometheus 注解
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monitored-app
  namespace: development
spec:
  replicas: 2
  selector:
    matchLabels:
      app: monitored-app
  template:
    metadata:
      labels:
        app: monitored-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: monitored-app-service
  namespace: development
  labels:
    app: monitored-app
spec:
  selector:
    app: monitored-app
  ports:
  - port: 80
    targetPort: 8080
EOF
}
```

### 2. Grafana 仪表板配置

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建自定义 Grafana 仪表板
create_grafana_dashboards() {
    # 创建节点监控仪表板
    cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: node-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  node-dashboard.json: |
    {
      "dashboard": {
        "id": null,
        "title": "节点监控",
        "tags": ["nodes"],
        "timezone": "browser",
        "schemaVersion": 16,
        "version": 0,
        "refresh": "10s",
        "panels": [
          {
            "type": "graph",
            "title": "CPU 使用率",
            "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
            "targets": [
              {
                "expr": "100 - (avg(rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
                "legendFormat": "{{instance}}"
              }
            ]
          },
          {
            "type": "graph",
            "title": "内存使用率",
            "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
            "targets": [
              {
                "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100",
                "legendFormat": "{{instance}}"
              }
            ]
          },
          {
            "type": "stat",
            "title": "Pod 数量",
            "gridPos": {"x": 0, "y": 8, "w": 8, "h": 6},
            "targets": [
              {
                "expr": "count(kube_pod_info)",
                "instant": true
              }
            ]
          },
          {
            "type": "stat",
            "title": "节点状态",
            "gridPos": {"x": 8, "y": 8, "w": 8, "h": 6},
            "targets": [
              {
                "expr": "sum(up{job=\"kubernetes-nodes\"})",
                "instant": true
              }
            ]
          }
        ]
      }
    }
EOF

    # 创建应用监控仪表板
    cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  app-dashboard.json: |
    {
      "dashboard": {
        "id": null,
        "title": "应用监控",
        "tags": ["applications"],
        "timezone": "browser",
        "schemaVersion": 16,
        "version": 0,
        "refresh": "10s",
        "panels": [
          {
            "type": "graph",
            "title": "HTTP 请求率",
            "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
            "targets": [
              {
                "expr": "rate(http_requests_total[5m])",
                "legendFormat": "{{handler}}"
              }
            ]
          },
          {
            "type": "graph",
            "title": "请求延迟",
            "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
                "legendFormat": "{{handler}} 95th percentile"
              }
            ]
          },
          {
            "type": "stat",
            "title": "错误率",
            "gridPos": {"x": 0, "y": 8, "w": 8, "h": 6},
            "targets": [
              {
                "expr": "rate(http_requests_total{code=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100",
                "instant": true
              }
            ]
          },
          {
            "type": "stat",
            "title": "在线实例数",
            "gridPos": {"x": 8, "y": 8, "w": 8, "h": 6},
            "targets": [
              {
                "expr": "count(up{job=\"kubernetes-pods\"} == 1)",
                "instant": true
              }
            ]
          }
        ]
      }
    }
EOF
}
```

## 📝 日志收集和分析

### 1. EFK 栈部署 (Elasticsearch + Fluentd + Kibana)

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 部署 EFK 日志栈
setup_efk_stack() {
    # 创建日志命名空间
    kubectl create namespace logging
    
    # 部署 Elasticsearch
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
  namespace: logging
spec:
  serviceName: elasticsearch
  replicas: 1
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
        env:
        - name: discovery.type
          value: single-node
        - name: ES_JAVA_OPTS
          value: "-Xms512m -Xmx512m"
        ports:
        - containerPort: 9200
          name: http
        - containerPort: 9300
          name: transport
        volumeMounts:
        - name: elasticsearch-data
          mountPath: /usr/share/elasticsearch/data
  volumeClaimTemplates:
  - metadata:
      name: elasticsearch-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch
  namespace: logging
spec:
  selector:
    app: elasticsearch
  ports:
  - port: 9200
    targetPort: 9200
EOF

    # 部署 Fluentd
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
  labels:
    app: fluentd
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      serviceAccount: fluentd
      serviceAccountName: fluentd
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1.16.1-debian-elasticsearch7-1.0
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        - name: FLUENT_ELASTICSEARCH_SCHEME
          value: "http"
        - name: FLUENT_UID
          value: "0"
        resources:
          limits:
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: fluentd-config
          mountPath: /fluentd/etc
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: fluentd-config
        configMap:
          name: fluentd-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>
    
    <filter kubernetes.**>
      @type kubernetes_metadata
    </filter>
    
    <match kubernetes.**>
      @type elasticsearch
      host "#{ENV['FLUENT_ELASTICSEARCH_HOST']}"
      port "#{ENV['FLUENT_ELASTICSEARCH_PORT']}"
      scheme "#{ENV['FLUENT_ELASTICSEARCH_SCHEME']}"
      logstash_format true
      logstash_prefix kubernetes
      flush_interval 5s
    </match>
EOF

    # 创建 Fluentd ServiceAccount 和 RBAC
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fluentd
  namespace: logging
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fluentd
rules:
- apiGroups:
  - ""
  resources:
  - pods
  - namespaces
  verbs:
  - get
  - list
  - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: fluentd
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: fluentd
subjects:
- kind: ServiceAccount
  name: fluentd
  namespace: logging
EOF

    # 部署 Kibana
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
  namespace: logging
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kibana
  template:
    metadata:
      labels:
        app: kibana
    spec:
      containers:
      - name: kibana
        image: docker.elastic.co/kibana/kibana:8.11.0
        env:
        - name: ELASTICSEARCH_HOSTS
          value: "http://elasticsearch:9200"
        ports:
        - containerPort: 5601
---
apiVersion: v1
kind: Service
metadata:
  name: kibana
  namespace: logging
spec:
  selector:
    app: kibana
  ports:
  - port: 5601
    targetPort: 5601
EOF

    echo "EFK 日志栈部署完成"
    echo "Kibana 访问: kubectl port-forward svc/kibana -n logging 5601:5601"
}

# 应用日志配置
setup_application_logging() {
    # 为应用配置结构化日志
    cat <<'EOF' | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logging-app
  namespace: development
spec:
  replicas: 2
  selector:
    matchLabels:
      app: logging-app
  template:
    metadata:
      labels:
        app: logging-app
    spec:
      containers:
      - name: app
        image: myapp:latest
        env:
        - name: LOG_FORMAT
          value: "json"
        - name: LOG_LEVEL
          value: "info"
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: log-volume
          mountPath: /var/log/app
      volumes:
      - name: log-volume
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: logging-app-service
  namespace: development
spec:
  selector:
    app: logging-app
  ports:
  - port: 80
    targetPort: 8080
EOF
}
```

### 2. 日志查询和分析

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 日志查询工具
create_log_query_tools() {
    # 创建日志查询脚本
    cat <<'EOF' > log-query.sh
#!/bin/bash
# 日志查询工具

ELASTICSEARCH_URL="http://localhost:9200"
KIBANA_URL="http://localhost:5601"

# 基础日志查询
query_logs() {
    local query=$1
    local index=${2:-"kubernetes-*"}
    
    curl -s -X GET "$ELASTICSEARCH_URL/$index/_search" \
        -H 'Content-Type: application/json' \
        -d "{
            \"query\": {
                \"query_string\": {
                    \"query\": \"$query\"
                }
            },
            \"sort\": [
                {\"@timestamp\": {\"order\": \"desc\"}}
            ],
            \"size\": 50
        }" | jq '.hits.hits[]._source | {timestamp: .@timestamp, message: .log, pod: .kubernetes.pod_name}'
}

# 错误日志查询
query_error_logs() {
    query_logs "level:error OR ERROR OR Exception" "$1"
}

# 特定应用日志查询
query_app_logs() {
    local app_name=$1
    local query=${2:-"*"}
    
    query_logs "kubernetes.container_name:$app_name AND ($query)" "kubernetes-*"
}

# 实时日志跟踪
tail_logs() {
    local app_name=$1
    
    while true; do
        query_app_logs "$app_name" "*" | jq -r '.timestamp + " " + .pod + " " + .message'
        sleep 2
    done
}

# 日志统计分析
log_statistics() {
    local app_name=$1
    local hours=${2:-24}
    
    echo "=== $app_name 最近 $hours 小时日志统计 ==="
    
    # 错误数量统计
    error_count=$(query_error_logs "kubernetes.container_name:$app_name" | jq length)
    echo "错误日志数量: $error_count"
    
    # 日志级别分布
    echo "日志级别分布:"
    curl -s -X GET "$ELASTICSEARCH_URL/kubernetes-*/_search" \
        -H 'Content-Type: application/json' \
        -d "{
            \"query\": {
                \"term\": {
                    \"kubernetes.container_name.keyword\": \"$app_name\"
                }
            },
            \"aggs\": {
                \"log_levels\": {
                    \"terms\": {
                        \"field\": \"level.keyword\"
                    }
                }
            },
            \"size\": 0
        }" | jq '.aggregations.log_levels.buckets[] | "\(.key): \(.doc_count)"'
}

# 主菜单
case "$1" in
    "query")
        query_logs "$2" "$3"
        ;;
    "errors")
        query_error_logs "$2"
        ;;
    "app")
        query_app_logs "$2" "$3"
        ;;
    "tail")
        tail_logs "$2"
        ;;
    "stats")
        log_statistics "$2" "$3"
        ;;
    *)
        echo "用法: $0 {query|errors|app|tail|stats} [参数...]"
        echo "示例:"
        echo "  $0 query 'error'"
        echo "  $0 errors my-app"
        echo "  $0 app my-app 'user login'"
        echo "  $0 tail my-app"
        echo "  $0 stats my-app 24"
        ;;
esac
EOF

    chmod +x log-query.sh
    
    # 创建 Kibana 查询模板
    cat <<'EOF' > kibana-queries.json
{
  "saved_objects": [
    {
      "id": "app-error-logs",
      "type": "search",
      "attributes": {
        "title": "应用错误日志",
        "description": "查询应用错误日志",
        "kibanaSavedObjectMeta": {
          "searchSourceJSON": "{\"index\":\"kubernetes-*\",\"filter\":[],\"query\":{\"query_string\":{\"query\":\"level:error OR ERROR OR Exception\"}}}"
        }
      }
    },
    {
      "id": "slow-requests",
      "type": "search",
      "attributes": {
        "title": "慢请求分析",
        "description": "分析响应时间超过1秒的请求",
        "kibanaSavedObjectMeta": {
          "searchSourceJSON": "{\"index\":\"kubernetes-*\",\"filter\":[],\"query\":{\"query_string\":{\"query\":\"response_time:>1000\"}}}"
        }
      }
    }
  ]
}
EOF
}
```

## 🔔 告警配置

### 1. Alertmanager 配置

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 配置 Alertmanager
setup_alerting() {
    # 创建 Alertmanager 配置
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-config
  namespace: monitoring
data:
  alertmanager.yml: |
    global:
      smtp_smarthost: 'smtp.gmail.com:587'
      smtp_from: 'alerts@example.com'
      smtp_auth_username: 'alerts@example.com'
      smtp_auth_password: 'your-app-password'
    
    route:
      group_by: ['alertname']
      group_wait: 10s
      group_interval: 10s
      repeat_interval: 1h
      receiver: 'slack-notifications'
    
    receivers:
    - name: 'slack-notifications'
      slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        channel: '#alerts'
        send_resolved: true
        title: '{{ template "slack.title" . }}'
        text: '{{ template "slack.text" . }}'
    
    templates:
    - '/etc/alertmanager/template/*.tmpl'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alertmanager
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: alertmanager
  template:
    metadata:
      labels:
        app: alertmanager
    spec:
      containers:
      - name: alertmanager
        image: prom/alertmanager:v0.26.0
        args:
        - '--config.file=/etc/alertmanager/alertmanager.yml'
        - '--storage.path=/alertmanager'
        ports:
        - containerPort: 9093
        volumeMounts:
        - name: config-volume
          mountPath: /etc/alertmanager
        - name: storage-volume
          mountPath: /alertmanager
      volumes:
      - name: config-volume
        configMap:
          name: alertmanager-config
      - name: storage-volume
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: alertmanager
  namespace: monitoring
spec:
  selector:
    app: alertmanager
  ports:
  - port: 9093
    targetPort: 9093
EOF

    # 创建告警规则
    cat <<EOF | kubectl apply -f -
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: alert-rules
  namespace: monitoring
spec:
  groups:
  - name: kubernetes-alerts
    rules:
    - alert: HighCPUUsage
      expr: 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High CPU usage detected"
        description: "CPU usage is above 80% for more than 5 minutes"

    - alert: HighMemoryUsage
      expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High memory usage detected"
        description: "Memory usage is above 85% for more than 5 minutes"

    - alert: PodCrashLooping
      expr: rate(kube_pod_container_status_restarts_total[5m]) * 60 * 5 > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Pod crash looping detected"
        description: "Pod {{ \$labels.pod }} is crash looping"

    - alert: ServiceDown
      expr: up == 0
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: "Service is down"
        description: "Service {{ \$labels.job }} is down"
EOF
}
```

### 2. 本地告警测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 告警测试工具
create_alert_test_tools() {
    # 创建告警测试脚本
    cat <<'EOF' > alert-test.sh
#!/bin/bash
# 告警测试工具

PROMETHEUS_URL="http://localhost:9090"
ALERTMANAGER_URL="http://localhost:9093"

# 触发测试告警
trigger_test_alert() {
    local alert_name=${1:-"TestAlert"}
    local severity=${2:-"warning"}
    
    echo "触发测试告警: $alert_name (严重程度: $severity)"
    
    # 创建测试告警规则
    cat <<TEST_RULE | curl -X POST -H "Content-Type: application/yaml" \
        --data-binary @- "$PROMETHEUS_URL/api/v1/rules"
groups:
- name: test-alerts
  rules:
  - alert: $alert_name
    expr: vector(1)
    labels:
      severity: $severity
    annotations:
      summary: "Test alert"
      description: "This is a test alert triggered at $(date)"
TEST_RULE
}

# 查看当前告警
view_active_alerts() {
    echo "=== 当前活跃告警 ==="
    curl -s "$ALERTMANAGER_URL/api/v2/alerts" | jq '.[] | {
        name: .labels.alertname,
        severity: .labels.severity,
        status: .status.state,
        startsAt: .startsAt,
        summary: .annotations.summary
    }'
}

# 查看告警历史
view_alert_history() {
    echo "=== 告警历史 ==="
    curl -s "$ALERTMANAGER_URL/api/v2/alerts?active=false" | jq '.[] | {
        name: .labels.alertname,
        status: .status.state,
        startsAt: .startsAt,
        endsAt: .endsAt,
        summary: .annotations.summary
    }'
}

# 测试通知渠道
test_notification_channels() {
    echo "测试通知渠道..."
    
    # 测试 Slack 通知
    curl -X POST -H 'Content-Type: application/json' \
        --data '{"text":"🔔 这是一个测试通知"}' \
        https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK 2>/dev/null && \
        echo "✅ Slack 通知测试成功" || echo "❌ Slack 通知测试失败"
    
    # 测试邮件通知（需要配置 SMTP）
    echo "📧 邮件通知测试需要手动验证"
}

# 清理测试告警
cleanup_test_alerts() {
    echo "清理测试告警..."
    curl -X DELETE "$PROMETHEUS_URL/api/v1/rules/test-alerts"
    echo "测试告警已清理"
}

# 主菜单
case "$1" in
    "trigger")
        trigger_test_alert "$2" "$3"
        ;;
    "view")
        view_active_alerts
        ;;
    "history")
        view_alert_history
        ;;
    "test-notifications")
        test_notification_channels
        ;;
    "cleanup")
        cleanup_test_alerts
        ;;
    *)
        echo "用法: $0 {trigger|view|history|test-notifications|cleanup} [参数...]"
        echo "示例:"
        echo "  $0 trigger TestCPUAlert warning"
        echo "  $0 view"
        echo "  $0 history"
        echo "  $0 test-notifications"
        echo "  $0 cleanup"
        ;;
esac
EOF

    chmod +x alert-test.sh
}
```

## 📈 性能指标收集

### 1. 应用性能监控

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 应用性能监控配置
setup_app_performance_monitoring() {
    # 创建应用性能监控配置
    cat <<'EOF' | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: perf-monitored-app
  namespace: development
spec:
  replicas: 2
  selector:
    matchLabels:
      app: perf-monitored-app
  template:
    metadata:
      labels:
        app: perf-monitored-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: ENABLE_PROFILING
          value: "true"
        - name: METRICS_ENDPOINT
          value: "/metrics"
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: perf-monitored-app-service
  namespace: development
  labels:
    app: perf-monitored-app
spec:
  selector:
    app: perf-monitored-app
  ports:
  - port: 80
    targetPort: 8080
EOF

    # 创建自定义指标收集器
    cat <<'EOF' > app-metrics-collector.py
#!/usr/bin/env python3
"""
应用性能指标收集器
"""

import time
import psutil
import requests
from prometheus_client import start_http_server, Gauge, Counter, Histogram

# 定义指标
cpu_percent = Gauge('app_cpu_percent', 'CPU使用百分比')
memory_percent = Gauge('app_memory_percent', '内存使用百分比')
request_count = Counter('app_requests_total', '总请求数')
request_duration = Histogram('app_request_duration_seconds', '请求处理时间')

def collect_system_metrics():
    """收集系统指标"""
    cpu_percent.set(psutil.cpu_percent())
    memory_percent.set(psutil.virtual_memory().percent)

def monitor_requests():
    """监控HTTP请求"""
    try:
        start_time = time.time()
        response = requests.get('http://localhost:8080/health', timeout=5)
        duration = time.time() - start_time
        
        request_count.inc()
        request_duration.observe(duration)
        
        return response.status_code == 200
    except Exception as e:
        print(f"请求监控错误: {e}")
        return False

def main():
    # 启动Prometheus指标服务器
    start_http_server(8080)
    print("指标收集器已启动，监听端口 8080")
    
    # 定期收集指标
    while True:
        collect_system_metrics()
        monitor_requests()
        time.sleep(10)

if __name__ == "__main__":
    main()
EOF
}
```

### 2. 性能测试和基准

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 性能测试工具
create_performance_benchmarks() {
    # 创建性能测试脚本
    cat <<'EOF' > performance-benchmark.sh
#!/bin/bash
# 性能基准测试工具

TEST_DURATION=${1:-60}  # 测试持续时间（秒）
CONCURRENT_USERS=${2:-10}  # 并发用户数

echo "=== 性能基准测试 ==="
echo "测试持续时间: ${TEST_DURATION}秒"
echo "并发用户数: ${CONCURRENT_USERS}"

# CPU 基准测试
test_cpu_performance() {
    echo "1. CPU 性能测试..."
    sysbench --test=cpu --cpu-max-prime=20000 run | grep "total time\|events per second"
}

# 内存基准测试
test_memory_performance() {
    echo "2. 内存性能测试..."
    sysbench --test=memory --memory-block-size=1K --memory-total-size=100G run | grep "transferred\|throughput"
}

# 磁盘 I/O 测试
test_disk_performance() {
    echo "3. 磁盘 I/O 性能测试..."
    sysbench --test=fileio --file-total-size=1G prepare
    sysbench --test=fileio --file-total-size=1G --file-test-mode=rndrw --time=${TEST_DURATION} run | grep "read\|written\|requests"
    sysbench --test=fileio --file-total-size=1G cleanup
}

# 网络性能测试
test_network_performance() {
    echo "4. 网络性能测试..."
    
    # 创建测试 Pod
    kubectl run network-test --image=nicolaka/netshoot --rm -it --restart=Never -- \
        iperf3 -s -D &  # 启动服务器
    
    sleep 5
    
    # 运行客户端测试
    kubectl run network-client --image=nicolaka/netshoot --rm -it --restart=Never -- \
        iperf3 -c network-test -t ${TEST_DURATION} -P ${CONCURRENT_USERS}
}

# 应用响应时间测试
test_app_response_time() {
    echo "5. 应用响应时间测试..."
    
    SERVICE_URL=${SERVICE_URL:-"http://perf-monitored-app-service.development.svc.cluster.local"}
    
    for i in $(seq 1 ${TEST_DURATION}); do
        start_time=$(date +%s%N)
        curl -s -o /dev/null -w "%{http_code}" ${SERVICE_URL}/health
        end_time=$(date +%s%N)
        duration=$((($end_time - $start_time) / 1000000))  # 转换为毫秒
        echo "请求 $i: ${duration}ms"
        sleep 1
    done
}

# 运行所有测试
run_all_tests() {
    test_cpu_performance
    test_memory_performance
    test_disk_performance
    test_network_performance
    test_app_response_time
    
    echo "性能测试完成"
    echo "结果已保存到 performance-results-$(date +%Y%m%d-%H%M%S).txt"
}

# 主程序
run_all_tests | tee performance-results-$(date +%Y%m%d-%H%M%S).txt
EOF

    chmod +x performance-benchmark.sh
    
    # 创建持续性能监控
    cat <<'EOF' > continuous-monitoring.sh
#!/bin/bash
# 持续性能监控脚本

INTERVAL=${1:-30}  # 监控间隔（秒）

echo "开始持续性能监控，间隔: ${INTERVAL}秒"

while true; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] === 性能快照 ==="
    
    # 收集关键指标
    echo "CPU 使用率: $(kubectl top nodes | awk 'NR>1 {print $2}' | head -1)"
    echo "内存使用率: $(kubectl top nodes | awk 'NR>1 {print $4}' | head -1)"
    echo "Pod 数量: $(kubectl get pods --all-namespaces --no-headers | wc -l)"
    echo "运行中的 Pod: $(kubectl get pods --field-selector=status.phase=Running --all-namespaces --no-headers | wc -l)"
    
    # 检查应用健康状态
    app_status=$(kubectl get pods -n development -l app=perf-monitored-app -o jsonpath='{.items[*].status.phase}' 2>/dev/null)
    echo "应用状态: $app_status"
    
    sleep $INTERVAL
done
EOF

    chmod +x continuous-monitoring.sh
}
```

## 🎯 监控和日志最佳实践总结

### 实施建议
1. **分层监控**：从基础设施到应用层的全方位监控
2. **结构化日志**：使用统一的日志格式便于分析
3. **告警分级**：合理设置告警级别和阈值
4. **性能基线**：建立正常的性能基准用于比较
5. **定期审查**：定期审查监控配置和告警规则

### 关键成功因素
- 选择合适的工具组合
- 设计清晰的监控策略
- 建立有效的告警机制
- 培养数据驱动的文化
- 持续优化和改进

---

> **💡 提示**: 监控和日志系统应该随着应用的发展而演进，始终保持其有效性和实用性。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/apply.sh
```

### 检查状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/check.sh
```

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
