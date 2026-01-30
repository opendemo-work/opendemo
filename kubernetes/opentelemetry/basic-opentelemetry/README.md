# Kubernetes OpenTelemetry Collector 基础案例

## 什么是 OpenTelemetry？

OpenTelemetry 是一个开源的可观测性框架，提供了一组工具、API 和 SDK，用于生成、收集和导出遥测数据（指标、追踪和日志）。它的目标是统一可观测性领域，提供 vendor-agnostic 的解决方案。

## 本案例包含的内容

- **otel-collector.yaml**: OpenTelemetry Collector 部署配置

## 快速开始

### 1. 部署 OpenTelemetry Collector

```bash
kubectl apply -f otel-collector.yaml
```

### 2. 验证 OpenTelemetry Collector 部署

```bash
# 检查 OpenTelemetry Collector Pod 状态
kubectl get pods -n opentelemetry -l app=otel-collector

# 等待 OpenTelemetry Collector 就绪
kubectl wait --for=condition=ready pod -l app=otel-collector -n opentelemetry --timeout=300s
```

### 3. 查看 OpenTelemetry Collector 日志

```bash
kubectl logs -f deployment/otel-collector -n opentelemetry
```

### 4. 访问 OpenTelemetry Collector 指标

#### 4.1 使用 NodePort 访问

```bash
# 获取 Node IP（根据你的 Kubernetes 环境调整）
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 访问 Prometheus 指标
echo "http://$NODE_IP:30089/metrics"
```

#### 4.2 使用 Port Forward 访问

```bash
# 端口转发 Prometheus 指标端口
kubectl port-forward svc/otel-collector 8889:8889 -n opentelemetry

# 访问指标
curl http://localhost:8889/metrics
```

## 基本使用

### 1. 向 OpenTelemetry Collector 发送数据

OpenTelemetry Collector 支持多种协议接收数据：

#### 1.1 使用 OTLP 协议（推荐）

```
# gRPC 端口: 4317
# HTTP 端口: 4318
```

#### 1.2 使用其他协议

OpenTelemetry Collector 还支持多种其他协议，如 Prometheus、Jaeger、Zipkin 等，可以通过添加相应的接收器来支持。

### 2. 示例应用

以下是一个简单的 Python 应用，使用 OpenTelemetry 向 OpenTelemetry Collector 发送数据：

```python
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# 设置资源
resource = Resource(attributes={
    "service.name": "my-service",
    "service.version": "1.0.0",
    "telemetry.sdk.name": "opentelemetry",
    "telemetry.sdk.language": "python",
    "telemetry.sdk.version": "1.15.0"
})

# 配置追踪器
trace_provider = TracerProvider(resource=resource)
trace_exporter = OTLPSpanExporter(endpoint="http://otel-collector.opentelemetry:4317", insecure=True)
trace_processor = BatchSpanProcessor(trace_exporter)
trace_provider.add_span_processor(trace_processor)
trace.set_tracer_provider(trace_provider)

# 配置指标器
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://otel-collector.opentelemetry:4317", insecure=True)
)
metric_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(metric_provider)

# 获取追踪器和指标器
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# 创建一个计数器
counter = meter.create_counter(
    "my_counter",
    description="A simple counter"
)

# 创建一个 span
with tracer.start_as_current_span("hello"):
    print("Hello, OpenTelemetry!")
    # 增加计数器
    counter.add(1, {"attribute": "value"})
```

## 清理资源

```bash
kubectl delete -f otel-collector.yaml
```

## OpenTelemetry Collector 架构

OpenTelemetry Collector 由三个主要组件组成：

1. **Receivers**: 接收来自不同来源的遥测数据
2. **Processors**: 处理数据（如批处理、采样、过滤等）
3. **Exporters**: 将处理后的数据导出到不同的后端

## 扩展建议

1. **添加更多接收器**: 配置其他接收器，如 Jaeger、Zipkin 等
2. **添加更多导出器**: 配置将数据导出到 Prometheus、Jaeger、Elasticsearch 等后端
3. **配置采样策略**: 根据需求调整采样策略，减少数据量
4. **部署多个实例**: 为了高可用性，部署多个 OpenTelemetry Collector 实例
5. **使用 DaemonSet 部署**: 对于日志收集，考虑使用 DaemonSet 部署

## 相关链接

- [OpenTelemetry 官方文档](https://opentelemetry.io/docs/)
- [OpenTelemetry Collector 文档](https://opentelemetry.io/docs/collector/)
- [OpenTelemetry GitHub 仓库](https://github.com/open-telemetry/opentelemetry-collector)
- [Kubernetes 可观测性最佳实践](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
