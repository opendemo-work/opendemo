# Kubernetes Jaeger 分布式追踪基础案例

## 什么是 Jaeger？

Jaeger 是一个开源的分布式追踪系统，用于监控和排查微服务架构中的问题。它实现了 OpenTracing 标准，并提供了丰富的可视化界面来查看分布式系统中的请求流。

## 本案例包含的内容

- **jaeger.yaml**: Jaeger all-in-one 部署配置

## 快速开始

### 1. 部署 Jaeger

```bash
kubectl apply -f jaeger.yaml
```

### 2. 验证 Jaeger 部署

```bash
# 检查 Jaeger Pod 状态
kubectl get pods -n jaeger -l app=jaeger

# 等待 Jaeger 就绪
kubectl wait --for=condition=ready pod -l app=jaeger -n jaeger --timeout=300s
```

### 3. 访问 Jaeger UI

#### 3.1 使用 NodePort 访问

```bash
# 获取 Node IP（根据你的 Kubernetes 环境调整）
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 访问 Jaeger UI
echo "http://$NODE_IP:30068"
```

#### 3.2 使用 Port Forward 访问

```bash
kubectl port-forward svc/jaeger 16686:16686 -n jaeger
```

然后访问：http://localhost:16686

## 基本使用

### 1. 在 Jaeger UI 中查看追踪数据

1. 登录 Jaeger UI
2. 在 **Service** 下拉菜单中选择一个服务
3. 在 **Operation** 下拉菜单中选择一个操作
4. 点击 **Find Traces**
5. 选择一个追踪查看详细信息

### 2. 向 Jaeger 发送追踪数据

Jaeger 支持多种协议接收追踪数据：

#### 2.1 使用 OTLP 协议（推荐）

```
# gRPC 端口: 4317
# HTTP 端口: 4318
```

#### 2.2 使用 Jaeger 原生协议

```
# gRPC 端口: 14250
# HTTP 端口: 14268
```

#### 2.3 使用 Zipkin 兼容协议

```
# HTTP 端口: 9411
```

### 3. 示例应用

以下是一个简单的 Python 应用，使用 OpenTelemetry 向 Jaeger 发送追踪数据：

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# 设置资源
resource = Resource(attributes={
    "service.name": "my-service",
    "service.version": "1.0.0",
    "telemetry.sdk.name": "opentelemetry",
    "telemetry.sdk.language": "python",
    "telemetry.sdk.version": "1.15.0"
})

# 配置追踪器
provider = TracerProvider(resource=resource)
exporter = OTLPSpanExporter(endpoint="http://jaeger.jaeger:4317", insecure=True)
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# 获取追踪器
tracer = trace.get_tracer(__name__)

# 创建一个 span
with tracer.start_as_current_span("hello"):
    print("Hello, Jaeger!")
```

## 清理资源

```bash
kubectl delete -f jaeger.yaml
```

## 扩展建议

1. **使用持久化存储**: 配置 Jaeger 使用持久化存储，如 Cassandra 或 Elasticsearch
2. **部署生产环境配置**: 使用 Jaeger 生产环境部署方案，分离收集器、查询器和存储
3. **配置采样策略**: 根据需求调整采样策略，平衡性能和追踪数据完整性
4. **与 Prometheus 集成**: 将 Jaeger 指标导出到 Prometheus，实现可观测性统一
5. **使用 Istio 集成**: 如果使用 Istio，可以配置自动注入追踪头

## 相关链接

- [Jaeger 官方文档](https://www.jaegertracing.io/docs/)
- [OpenTelemetry 官方文档](https://opentelemetry.io/docs/)
- [OpenTracing 官方文档](https://opentracing.io/docs/)
- [Kubernetes 可观测性最佳实践](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
