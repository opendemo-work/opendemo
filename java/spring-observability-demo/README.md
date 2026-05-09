# Spring Boot 可观测性深度集成演示

## 学习目标

1. 掌握 Micrometer 进行应用指标采集
2. 理解 OpenTelemetry (OTLP) 集成
3. 学会配置健康检查和探活端点
4. 实现分布式追踪

## 环境要求

- JDK 17+
- Maven 3.9+
- Prometheus + Grafana (可选，用于可视化)

## 项目结构

```
spring-observability-demo/
├── code/
│   └── main/java/com/opendemo/observability/
│       ├── ObservabilityApplication.java
│       ├── controller/
│       │   └── MetricsController.java
│       ├── service/
│       │   └── BusinessService.java
│       └── config/
│           ├── MicrometerConfig.java
│           └── OpenTelemetryConfig.java
├── pom.xml
└── README.md
```

## 核心概念

### 可观测性三要素

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Metrics   │     │    Logs     │     │   Traces    │
│   (指标)    │     │   (日志)    │     │   (追踪)    │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ Prometheus  │     │   ELK       │     │   Jaeger    │
│ Micrometer   │     │   Loki     │     │   Zipkin    │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 快速开始

### 1. 启动应用

```bash
cd spring-observability-demo
mvn spring-boot:run
```

### 2. 访问端点

```bash
# 健康检查
curl http://localhost:8080/actuator/health

# 查看指标
curl http://localhost:8080/actuator/metrics

# 查看特定指标
curl http://localhost:8080/actuator/metrics/http.server.requests

# 查看追踪
curl http://localhost:8080/actuator/traces
```

## 核心功能详解

### 1. Micrometer 指标采集

Micrometer 是 Spring Boot 3.x 的指标抽象层，支持多种监控系统。

**内置指标：**
- `jvm.memory.used` - JVM 内存使用
- `http.server.requests` - HTTP 请求统计
- `process.cpu.usage` - CPU 使用率
- `hikaricp.connections` - 数据库连接池

**自定义指标：**

```java
// 计数器
Counter totalRequests = MeterRegistry.counter("app.requests.total");

// 计时器
Timer requestLatency = MeterRegistry.timer("app.request.latency");

//  Gauge
Gauge.builder("app.active.users", this, Service::getActiveUsers)
    .register(registry);
```

### 2. OpenTelemetry 集成

OTLP (OpenTelemetry Protocol) 是标准的可观测性数据传输协议。

**配置 OTLP 导出器：**

```yaml
management:
  otlp:
    tracing:
      endpoint: http://localhost:4317
  exporter:
    otlp:
      endpoint: http://localhost:4317
```

### 3. 健康检查

Spring Boot Actuator 提供完整的健康检查端点。

**自定义健康指示器：**

```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        // 检查数据库连接
        if (isDatabaseHealthy()) {
            return Health.up().withDetail("database", "OK").build();
        }
        return Health.down().withDetail("database", "FAILED").build();
    }
}
```

## 代码解析

### BusinessService.java

```java
@Service
public class BusinessService {

    private final Counter requestCounter;
    private final Timer operationTimer;

    public BusinessService(MeterRegistry registry) {
        this.requestCounter = Counter.builder("app.business.requests")
            .description("业务请求总数")
            .register(registry);

        this.operationTimer = Timer.builder("app.business.duration")
            .description("业务操作耗时")
            .register(registry);
    }

    public String processOrder(String orderId) {
        return operationTimer.record(() -> {
            requestCounter.increment();
            // 业务逻辑
            return "Order " + orderId + " processed";
        });
    }
}
```

### MetricsController.java

```java
@RestController
@RequestMapping("/api/metrics")
public class MetricsController {

    private final MeterRegistry registry;

    public MetricsController(MeterRegistry registry) {
        this.registry = registry;
    }

    @GetMapping("/custom")
    public Map<String, Object> getCustomMetrics() {
        Map<String, Object> metrics = new HashMap<>();

        // 获取当前指标值
        registry.find("app.business.requests").counter()
            .ifPresent(c -> metrics.put("totalRequests", c.count()));

        return metrics;
    }
}
```

## 扩展配置

### Prometheus 集成

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: always
  prometheus:
    metrics:
      export:
        enabled: true
```

### Grafana Dashboard

推荐 Grafana Dashboard ID: `4701` (JVM/Micrometer 仪表板)

## 常见问题

### Q1: 如何添加自定义指标？

```java
@Service
public class CustomMetricsService {
    private final MeterRegistry registry;

    public CustomMetricsService(MeterRegistry registry) {
        // 方式1: 直接创建
        Counter counter = Counter.builder("app.custom.counter")
            .description("自定义计数器")
            .register(registry);

        // 方式2: 使用 @Timed 注解
    }

    @Timed(value = "app.method.duration", description = "方法耗时")
    public void trackedMethod() {
        // 方法自动计时
    }
}
```

### Q2: 如何禁用特定指标？

```yaml
management:
  metrics:
    enable:
      jvm: false  # 禁用 JVM 指标
      process: false  # 禁用进程指标
```

---

**技术栈**: Spring Boot 3.2 | Micrometer | OpenTelemetry | Prometheus

**维护者**: OpenDemo Team

**版本**: 1.0.0