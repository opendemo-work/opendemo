# OpenTelemetry

OpenTelemetry可观测性标准演示。

## 什么是OpenTelemetry

云原生可观测性的统一标准，整合Tracing、Metrics、Logging。

## 核心组件

- **OTel SDK**: 应用埋点SDK
- **OTel Collector**: 数据收集代理
- **OTLP**: 传输协议

## 快速集成

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

provider = TracerProvider()
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("operation"):
    # 业务逻辑
    pass
```
