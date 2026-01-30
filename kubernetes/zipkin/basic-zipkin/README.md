# Kubernetes Zipkin 分布式追踪基础案例

## 什么是 Zipkin？

Zipkin 是一个开源的分布式追踪系统，用于收集、存储和展示分布式系统中的时序数据。它帮助开发者理解系统中的服务依赖关系，排查性能瓶颈和故障。

## 本案例包含的内容

- **zipkin.yaml**: Zipkin 部署配置

## 快速开始

### 1. 部署 Zipkin

```bash
kubectl apply -f zipkin.yaml
```

### 2. 验证 Zipkin 部署

```bash
# 检查 Zipkin Pod 状态
kubectl get pods -n zipkin -l app=zipkin

# 等待 Zipkin 就绪
kubectl wait --for=condition=ready pod -l app=zipkin -n zipkin --timeout=300s
```

### 3. 访问 Zipkin UI

#### 3.1 使用 NodePort 访问

```bash
# 获取 Node IP（根据你的 Kubernetes 环境调整）
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 访问 Zipkin UI
echo "http://$NODE_IP:30069"
```

#### 3.2 使用 Port Forward 访问

```bash
kubectl port-forward svc/zipkin 9411:9411 -n zipkin
```

然后访问：http://localhost:9411

## 基本使用

### 1. 在 Zipkin UI 中查看追踪数据

1. 登录 Zipkin UI
2. 在 **Service Name** 下拉菜单中选择一个服务
3. 在 **Span Name** 下拉菜单中选择一个操作
4. 点击 **Find Traces**
5. 选择一个追踪查看详细信息

### 2. 向 Zipkin 发送追踪数据

Zipkin 支持多种协议接收追踪数据：

#### 2.1 使用 HTTP API

```
# HTTP 端口: 9411
# API 端点: /api/v2/spans
```

#### 2.2 使用 gRPC API

```
# gRPC 端口: 9411 (通过 gRPC-Web)
```

### 3. 示例应用

以下是一个简单的 Python 应用，使用 OpenTelemetry 向 Zipkin 发送追踪数据：

```python
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
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
exporter = ZipkinExporter(endpoint="http://zipkin.zipkin:9411/api/v2/spans")
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# 获取追踪器
tracer = trace.get_tracer(__name__)

# 创建一个 span
with tracer.start_as_current_span("hello"):
    print("Hello, Zipkin!")
```

## 清理资源

```bash
kubectl delete -f zipkin.yaml
```

## Zipkin vs Jaeger

| 特性 | Zipkin | Jaeger |
|------|--------|--------|
| 架构 | 简单，单节点部署方便 | 更复杂，支持分布式部署 |
| 存储支持 | 内存、MySQL、Cassandra、Elasticsearch | 内存、Cassandra、Elasticsearch |
| UI | 简洁 | 更丰富，支持更多可视化 |
| 性能 | 良好 | 优秀，特别是在大规模环境下 |
| 社区 | 成熟 | 活跃，由 CNCF 托管 |
| 集成 | 广泛支持 | 良好支持，特别是与 Kubernetes 集成 |

## 扩展建议

1. **使用持久化存储**: 将 Zipkin 的存储从内存改为 MySQL、Cassandra 或 Elasticsearch
2. **部署生产环境配置**: 配置 Zipkin 集群，提高可用性
3. **与其他系统集成**: 与 Prometheus、Grafana 等集成，实现可观测性统一
4. **配置采样策略**: 根据需求调整采样策略，平衡性能和追踪数据完整性
5. **使用 OpenTelemetry**: 采用 OpenTelemetry 作为统一的可观测性框架

## 相关链接

- [Zipkin 官方文档](https://zipkin.io/docs/)
- [OpenTelemetry 官方文档](https://opentelemetry.io/docs/)
- [Kubernetes 可观测性最佳实践](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
