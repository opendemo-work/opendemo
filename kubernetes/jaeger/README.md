# Jaeger Distributed Tracing

Jaeger分布式链路追踪演示，展示微服务调用链的可视化分析。

## 什么是分布式追踪

```
分布式调用链:
User Request
     │
     ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│   API   │───▶│  Auth   │───▶│  User   │
│ Gateway │    │ Service │    │ Service │
└────┬────┘    └─────────┘    └────┬────┘
     │                              │
     │    ┌─────────┐               │
     └───▶│  Order  │◀──────────────┘
          │ Service │
          └────┬────┘
               │
               ▼
          ┌─────────┐
          │ Payment │
          │ Service │
          └─────────┘

Trace: 完整请求链路
Span: 单个服务调用
Parent-Child: 调用关系
```

## Jaeger架构

```
Jaeger组件:
┌─────────────────────────────────────────────────────┐
│                   Jaeger UI                         │
│              (可视化和查询)                          │
└────────────────────┬────────────────────────────────┘
                     │
              ┌──────┴──────┐
              │   Query      │
              │  (API/查询)  │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Collector  │ │ Collector  │ │ Collector  │
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
              ┌──────┴──────┐
              │   Storage    │
              │ (ES/Cassandra)│
              └───────────────┘
```

## 安装Jaeger

### All-in-One模式 (开发测试)
```bash
# Docker运行
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest

# 访问UI: http://localhost:16686
```

### Kubernetes安装
```bash
# 使用Helm
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm install jaeger jaegertracing/jaeger \
  --namespace observability \
  --create-namespace

# 使用Operator
kubectl apply -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.49.0/jaeger-operator.yaml
```

### Jaeger CRD
```yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: simple-prod
spec:
  strategy: production
  storage:
    type: elasticsearch
    options:
      es:
        server-urls: http://elasticsearch:9200
  ingress:
    enabled: true
```

## 代码集成

### OpenTelemetry SDK

#### Java (Spring Boot)
```java
// pom.xml依赖
// opentelemetry-spring-boot-starter

// 配置application.yml
otel:
  traces:
    exporter: otlp
  exporter:
    otlp:
      endpoint: http://jaeger:4317

// 自动追踪Controller
@RestController
public class OrderController {
    
    @GetMapping("/order/{id}")
    public Order getOrder(@PathVariable String id) {
        // 自动创建Span
        return orderService.findById(id);
    }
}
```

#### Python (FastAPI)
```python
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# 配置Tracer
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="jaeger:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    # 自动追踪
    return {"user_id": user_id}

# 自定义Span
tracer = trace.get_tracer(__name__)

@app.post("/api/orders")
async def create_order():
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("order.type", "premium")
        # 业务逻辑
        return {"status": "created"}
```

#### Go (Gin)
```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/trace"
)

func initTracer() func() {
    ctx := context.Background()
    
    exporter, _ := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("jaeger:4317"),
        otlptracegrpc.WithInsecure(),
    )
    
    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
    )
    otel.SetTracerProvider(tp)
    
    return func() { tp.Shutdown(ctx) }
}

// 使用
func handleRequest(c *gin.Context) {
    tracer := otel.Tracer("my-service")
    ctx, span := tracer.Start(c.Request.Context(), "handle-request")
    defer span.End()
    
    // 业务逻辑
}
```

### 手动创建Span
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def process_payment(order_id):
    with tracer.start_as_current_span("process_payment") as span:
        # 添加属性
        span.set_attribute("order.id", order_id)
        span.set_attribute("payment.method", "credit_card")
        
        # 添加事件
        span.add_event("validation_started")
        validate_payment()
        span.add_event("validation_completed")
        
        # 嵌套Span
        with tracer.start_as_current_span("charge_card") as child_span:
            result = charge_card()
            child_span.set_attribute("charge.amount", 99.99)
        
        return result
```

## 上下文传播

### HTTP传播
```python
from opentelemetry.propagate import inject, extract
import requests

# 客户端 - 注入上下文
def call_service_b():
    headers = {}
    inject(headers)  # 注入trace上下文到headers
    
    response = requests.get(
        "http://service-b/api",
        headers=headers
    )
    return response.json()

# 服务端 - 提取上下文
@app.get("/api")
def handle_request():
    ctx = extract(request.headers)  # 提取trace上下文
    # 继续链路...
```

### gRPC传播
```python
# 客户端
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient

GrpcInstrumentorClient().instrument()

# 服务端
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer

GrpcInstrumentorServer().instrument()
```

## 采样策略

```yaml
# 头部采样 (Probabilistic)
sampling:
  type: probabilistic
  param: 0.1  # 10%采样

# 速率限制采样
sampling:
  type: ratelimiting
  param: 100  # 每秒100个trace
```

## 分析使用

### Jaeger UI功能
1. **Trace搜索**: 按服务、操作、标签筛选
2. **依赖图**: 服务调用拓扑
3. **Trace详情**: 时序图、日志、标签
4. **对比**: 异常vs正常trace对比

### 性能分析
```
Trace分析:
┌─────────────────────────────────────────────────────┐
│ ServiceA: [====Span A====]                          │
│              │                                      │
│ ServiceB:    [===Span B===]                         │
│                 │                                   │
│ ServiceC:       [Span C]                            │
│                                                      │
│ Tags:                                                │
│   - http.method: GET                                 │
│   - http.status_code: 200                            │
│   - db.statement: SELECT * FROM users                │
│                                                      │
│ Logs:                                                │
│   12:00:01  "Query started"                          │
│   12:00:02  "Cache miss"                             │
│   12:00:03  "Query completed"                        │
└─────────────────────────────────────────────────────┘
```

## 学习要点

1. 分布式追踪概念和术语
2. OpenTelemetry标准
3. 自动和手动埋点
4. 上下文传播机制
5. 采样策略和性能优化
