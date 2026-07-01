# Kubernetes Zipkin 分布式追踪基础案例

## 什么是 Zipkin？

Zipkin 是一个开源的分布式追踪系统，用于收集、存储和展示分布式系统中的时序数据。它帮助开发者理解系统中的服务依赖关系，排查性能瓶颈和故障。

## 本案例包含的内容

- **zipkin.yaml**: Zipkin 部署配置

## 快速开始

### 1. 部署 Zipkin

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f zipkin.yaml
```

### 2. 验证 Zipkin 部署

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查 Zipkin Pod 状态
kubectl get pods -n zipkin -l app=zipkin

# 等待 Zipkin 就绪
kubectl wait --for=condition=ready pod -l app=zipkin -n zipkin --timeout=300s
```

### 3. 访问 Zipkin UI

#### 3.1 使用 NodePort 访问

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 获取 Node IP（根据你的 Kubernetes 环境调整）
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 访问 Zipkin UI
echo "http://$NODE_IP:30069"
```

#### 3.2 使用 Port Forward 访问

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
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
