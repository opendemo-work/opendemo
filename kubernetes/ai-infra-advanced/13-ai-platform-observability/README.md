# AI平台可观测性

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **工具**: Prometheus, Grafana, Jaeger

---

## 概述

AI平台可观测性涵盖GPU监控、训练任务监控、推理服务监控、数据管道监控等全方位的可观测性体系。

---

## 监控架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI平台可观测性架构                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ GPU监控    │  │ 训练监控   │  │ 推理监控   │               │
│  │ DCGM       │  │ MLflow     │  │ vLLM       │               │
│  └────────────┘  └────────────┘  └────────────┘               │
│                              │                                  │
│                              v                                  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   Prometheus                             │  │
│  │              (指标采集与存储)                            │  │
│  └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              v                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ Grafana    │  │ Alertmgr   │  │ Jaeger     │               │
│  │ (可视化)   │  │ (告警)     │  │ (追踪)     │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 训练任务监控

### Prometheus监控配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'gpu-metrics'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            target_label: __address__
            regex: (.+)
            replacement: $1:9400
      
      - job_name: 'mlflow'
        static_configs:
          - targets: ['mlflow.mlops.svc.cluster.local:5000']
      
      - job_name: 'vllm-metrics'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - llm-serving
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            action: keep
            regex: vllm.*
```

### 训练指标采集

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: training-metrics-exporter
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: training-metrics-exporter
  template:
    metadata:
      labels:
        app: training-metrics-exporter
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
    spec:
      containers:
        - name: exporter
          image: prom/statsd-exporter:latest
          ports:
            - containerPort: 8000
          args:
            - --statsd.listen-address=:9125
            - --web.listen-address=:8000
```

---

## 推理服务监控

### vLLM指标配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-with-metrics
  namespace: llm-serving
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm
  template:
    metadata:
      labels:
        app: vllm
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
    spec:
      containers:
        - name: vllm
          image: vllm/vllm-openai:latest
          args:
            - --model
            - /models/llama-2-7b-hf
            - --enable-metrics
          ports:
            - containerPort: 8000
```

### 推理监控Dashboard

```json
{
  "dashboard": {
    "title": "LLM Inference Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(vllm_request_total[5m])"
          }
        ]
      },
      {
        "title": "Latency P99",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(vllm_request_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "Token Throughput",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(vllm_tokens_generated_total[5m])"
          }
        ]
      },
      {
        "title": "KV Cache Usage",
        "type": "gauge",
        "targets": [
          {
            "expr": "vllm_kv_cache_usage_ratio"
          }
        ]
      }
    ]
  }
}
```

---

## 分布式追踪

### Jaeger部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
  namespace: observability
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
        - name: jaeger
          image: jaegertracing/all-in-one:latest
          ports:
            - containerPort: 16686
              name: ui
            - containerPort: 14268
              name: collector
          env:
            - name: COLLECTOR_OTLP_ENABLED
              value: "true"
```

### OpenTelemetry集成

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-config
  namespace: observability
data:
  config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
    processors:
      batch:
        timeout: 1s
    exporters:
      jaeger:
        endpoint: jaeger.observability.svc.cluster.local:14250
        tls:
          insecure: true
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch]
          exporters: [jaeger]
```

---

## 告警规则

### AI平台告警

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ai-platform-alerts
  namespace: monitoring
spec:
  groups:
    - name: training-alerts
      rules:
        - alert: TrainingJobStuck
          expr: increase(kubeflow_training_job_running[1h]) == 0 and kubeflow_training_job_running > 0
          for: 30m
          labels:
            severity: warning
          annotations:
            summary: "Training job appears stuck"
        
        - alert: TrainingJobFailed
          expr: increase(kubeflow_training_job_failed[5m]) > 0
          labels:
            severity: critical
          annotations:
            summary: "Training job failed"
    
    - name: inference-alerts
      rules:
        - alert: HighInferenceLatency
          expr: histogram_quantile(0.99, rate(vllm_request_duration_seconds_bucket[5m])) > 5
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Inference latency P99 > 5s"
        
        - alert: InferenceErrorRate
          expr: rate(vllm_request_errors_total[5m]) / rate(vllm_request_total[5m]) > 0.01
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Inference error rate > 1%"
```

---

## 相关案例

- [GPU监控DCGM](../04-gpu-monitoring-dcgm/) - GPU监控
- [LLM可观测性](../25-llm-observability/) - LLM监控
- [故障排查性能](../14-troubleshooting-performance/) - 性能诊断

---

**维护者**: OpenDemo Team | **许可证**: MIT
