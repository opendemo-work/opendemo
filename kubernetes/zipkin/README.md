# Zipkin Distributed Tracing

Zipkin分布式链路追踪系统演示。

## 架构概览

```
Zipkin架构:
┌─────────────────────────────────────────────────────────┐
│                   Zipkin UI                             │
│              (查询与可视化)                              │
└────────────────────┬────────────────────────────────────┘
                     │
              ┌──────┴──────┐
              │   Query      │
              │  Service     │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│  Collector │ │  Collector │ │  Collector │
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
              ┌──────┴──────┐
              │   Storage    │
              │ (ES/MySQL)   │
              └───────────────┘
```

## 快速部署

```bash
# Docker部署
docker run -d -p 9411:9411 openzipkin/zipkin

# Kubernetes部署
kubectl apply -f https://raw.githubusercontent.com/openzipkin/zipkin/master/zipkin-server/kubernetes/zipkin.yaml
```

## 客户端集成

### Java (Brave)
```java
// Maven依赖
// zipkin-reporter-brave, brave-instrumentation-spring-web

@Bean
public HttpTracing httpTracing() {
    AsyncReporter<Span> reporter = AsyncReporter.create(
        OkHttpSender.create("http://zipkin:9411/api/v2/spans")
    );
    
    BraveTracing braveTracing = BraveTracing.newBuilder()
        .localServiceName("my-service")
        .spanReporter(reporter)
        .build();
    
    return braveTracing.httpTracing();
}
```

### Go
```go
import (
    "github.com/openzipkin/zipkin-go"
    "github.com/openzipkin/zipkin-go/reporter/http"
)

reporter := http.NewReporter("http://zipkin:9411/api/v2/spans")
defer reporter.Close()

endpoint, _ := zipkin.NewEndpoint("my-service", "localhost:8080")
tracer, _ := zipkin.NewTracer(reporter, zipkin.WithLocalEndpoint(endpoint))

span := tracer.StartSpan("operation")
defer span.Finish()
```

## 学习要点

1. Span数据模型
2. 采样策略配置
3. 存储后端选择
4. 链路分析技巧
