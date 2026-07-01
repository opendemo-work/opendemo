<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Spring Cloud Sleuth Demo - 分布式链路追踪演示

## 项目概述

本项目演示了 Spring Cloud Sleuth 在微服务架构中的分布式链路追踪功能。通过模拟一个订单处理流程（Order → Inventory → Payment），展示如何在服务间调用中自动传递 Trace ID 和 Span ID，以及如何集成 Zipkin 进行链路可视化。

## 什么是分布式链路追踪

在微服务架构中，一个用户请求可能需要经过多个服务的处理才能完成。分布式链路追踪（Distributed Tracing）是一种用于监控和排查这些跨服务请求的技术。

### 核心概念

- **Trace（追踪）**：代表一个完整的请求链路，从入口到所有下游服务的调用。每个 Trace 有一个唯一的 Trace ID
- **Span（跨度）**：代表 Trace 中的一个工作单元，例如一次 HTTP 请求或一次数据库查询。每个 Span 有一个唯一的 Span ID
- **Annotation（标注）**：记录 Span 中特定时间点的事件，如 `cs`（Client Send）、`sr`（Server Receive）等
- **Baggage（行李）**：可以跨服务传递的键值对数据，用于在链路中传递上下文信息

### 为什么需要链路追踪

1. **故障定位**：快速找到请求链路中的故障点
2. **性能分析**：识别链路中的性能瓶颈
3. **依赖分析**：了解服务之间的调用关系
4. **请求路径可视化**：直观展示请求的完整调用路径

## 项目结构

```
spring-cloud-sleuth-demo/
├── pom.xml
├── metadata.json
├── README.md
└── src/main/java/com/example/demo/
    ├── SleuthDemoApplication.java
    ├── config/
    │   └── RestTemplateConfig.java
    ├── controller/
    │   ├── OrderController.java       # 订单入口
    │   ├── PaymentController.java     # 支付服务
    │   └── InventoryController.java   # 库存服务
    ├── service/
    │   ├── OrderService.java          # 订单处理（调用下游服务）
    │   ├── PaymentService.java        # 支付服务客户端
    │   └── InventoryService.java      # 库存服务客户端
    └── dto/
        ├── OrderRequest.java
        └── OrderResponse.java
```

## Trace ID 和 Span ID

### 自动注入原理

Spring Cloud Sleuth 通过以下方式自动注入追踪信息：

1. **HTTP 请求拦截器**：Sleuth 自动为 RestTemplate、WebClient、Feign 等添加拦截器，在 HTTP Header 中注入 Trace ID 和 Span ID
2. **日志 MDC 注入**：Sleuth 自动将 Trace ID 和 Span ID 注入到 SLF4J 的 MDC（Mapped Diagnostic Context）中
3. **线程池传播**：Sleuth 确保在异步调用中追踪信息能够正确传播

### 日志格式配置

```yaml
logging:
  pattern:
    level: '%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]'
```

配置后，每条日志将输出如下格式：

```
INFO [sleuth-demo,5e6a8d3f2b1c,7f8a9b0c1d2e] Processing order for product: P001
```

其中：
- `sleuth-demo` = 应用名称
- `5e6a8d3f2b1c` = Trace ID
- `7f8a9b0c1d2e` = Span ID

## Spring Cloud Sleuth 配置

### 基础配置

```yaml
spring:
  sleuth:
    sampler:
      probability: 1.0    # 采样率，1.0 表示全部采样
    web:
      skip-pattern: /actuator.*  # 跳过 Actuator 端点的追踪
```

### 采样策略

在生产环境中，不可能对所有请求都进行追踪（性能开销大）。Sleuth 支持多种采样策略：

```yaml
spring:
  sleuth:
    sampler:
      probability: 0.1    # 10% 的采样率
```

也可以通过自定义 Sampler 实现：

```java
@Bean
public Sampler customSampler() {
    return new ProbabilityBasedSampler(0.1f);
}
```

常见的采样策略：
- **固定比例采样**：按一定比例随机采样（如 10%）
- **基于速率采样**：每秒采样固定数量的请求
- **自定义策略**：根据请求特征（如 URL、Header）决定是否采样

### Baggage 传播

Baggage 允许在服务调用链中传递自定义的上下文信息：

```yaml
spring:
  sleuth:
    baggage:
      remote-fields: user-id,tenant-id       # 在 HTTP Header 中传播的字段
      correlation-fields: user-id,tenant-id   # 同时记录到日志 MDC 的字段
```

使用方式：

```java
// 设置 Baggage
Span.current().context().extra().put("user-id", "user-123");

// 或者使用静态方法
ExtraFieldPropagation.set("user-id", "user-123");
```

## Zipkin 集成

### 什么是 Zipkin

Zipkin 是一个开源的分布式追踪系统，用于收集、存储和展示链路追踪数据。它提供了 Web UI 来可视化和分析请求链路。

### 配置 Zipkin

```yaml
spring:
  zipkin:
    base-url: http://localhost:9411    # Zipkin Server 地址
    sender:
      type: web                         # 使用 HTTP 发送追踪数据
```

### 启动 Zipkin Server

使用 Docker 快速启动：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```

或下载 Zipkin Jar 直接运行：

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
curl -sSL https://zipkin.io/quickstart.sh | bash -s
java -jar zipkin.jar
```

### Zipkin 数据存储

Zipkin 支持多种存储后端：

| 存储类型 | 适用场景 | 配置 |
|---------|---------|------|
| 内存 | 开发测试 | 默认 |
| MySQL | 中小规模生产 | `STORAGE_TYPE=mysql` |
| Elasticsearch | 大规模生产 | `STORAGE_TYPE=elasticsearch` |
| Cassandra | 大规模生产 | `STORAGE_TYPE=cassandra` |

## RestTemplate 与 Sleuth 传播

为了确保追踪信息在服务间调用时正确传播，需要配置带有 Sleuth 拦截器的 RestTemplate：

```java
@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate(LazyTraceClientHttpRequestInterceptor interceptor) {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.setInterceptors(Collections.singletonList(interceptor));
        return restTemplate;
    }
}
```

`LazyTraceClientHttpRequestInterceptor` 会在每次 HTTP 请求时自动添加追踪相关的 HTTP Header：
- `X-B3-TraceId`：Trace ID
- `X-B3-SpanId`：当前 Span ID
- `X-B3-ParentSpanId`：父 Span ID
- `X-B3-Sampled`：是否采样

## 调用链路说明

本 demo 模拟了一个完整的订单处理流程：

```
Client → OrderController → OrderService
                                ├── InventoryService → InventoryController
                                └── PaymentService → PaymentController
```

1. 客户端发送 POST 请求到 `/orders`
2. `OrderController` 接收请求（生成 Trace ID）
3. `OrderService` 调用 `InventoryService`（创建子 Span，继承 Trace ID）
4. `InventoryService` 通过 RestTemplate 调用 `/inventory`（自动传播追踪 Header）
5. `OrderService` 调用 `PaymentService`（创建另一个子 Span）
6. `PaymentService` 通过 RestTemplate 调用 `/payments`（自动传播追踪 Header）

## 运行步骤

### 1. 启动 Zipkin（可选）

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```

### 2. 启动应用

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn spring-boot:run
```

### 3. 发送测试请求

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
curl -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -d '{"productId": "P001", "quantity": 2, "amount": 199.99}'
```

### 4. 查看日志输出

在控制台中可以看到带有 Trace ID 和 Span ID 的日志：

```
INFO [sleuth-demo,abc123,def456] Received order request: productId=P001, quantity=2
INFO [sleuth-demo,abc123,ghi789] Checking inventory for product: P001, quantity: 2
INFO [sleuth-demo,abc123,jkl012] Inventory check completed for product: P001
INFO [sleuth-demo,abc123,mno345] Initiating payment for order: xxx, amount: 199.99
INFO [sleuth-demo,abc123,pqr678] Payment processed for order: xxx
INFO [sleuth-demo,abc123,def456] Order processed: orderId=xxx, status=COMPLETED
```

注意同一个 Trace ID `abc123` 贯穿整个请求链路。

### 5. 查看 Zipkin UI

访问 http://localhost:9411，可以看到请求的完整调用链路和每个 Span 的耗时。

## 日志关联

### 日志格式

通过配置 `logging.pattern.level`，每条日志都会携带追踪信息：

```
%5p [应用名,Trace ID,Span ID]
```

### 日志聚合

在分布式系统中，通常使用 ELK（Elasticsearch + Logstash + Kibana）或类似方案聚合日志。通过 Trace ID，可以在 Kibana 中搜索某个请求的所有日志：

```
traceId: "abc123def456"
```

这样可以快速定位问题，查看一个请求在所有服务中的完整日志。

## 从 Sleuth 迁移到 Micrometer Tracing

Spring Cloud Sleuth 已停止维护，Spring Boot 3.x 推荐使用 Micrometer Tracing。

### 迁移要点

1. **依赖替换**：
   - `spring-cloud-starter-sleuth` → `micrometer-tracing-bridge-brave`
   - `spring-cloud-sleuth-zipkin` → `micrometer-observation-reporting-zipkin`

2. **API 变更**：
   - Sleuth 的 `Tracer` API → Micrometer 的 `Observation` API
   - Baggage 传播 API 有所调整

3. **配置前缀变更**：
   - `spring.sleuth.*` → `management.tracing.*`

4. **Spring Boot 3.x 迁移**：
   - 需要 Java 17+
   - Spring Boot 3.x 原生支持 Micrometer Observation

### Micrometer Tracing 配置示例（Spring Boot 3.x）

```yaml
management:
  tracing:
    sampling:
      probability: 1.0
  zipkin:
    tracing:
      endpoint: http://localhost:9411/api/v2/spans
```

## 最佳实践

1. **合理设置采样率**：开发环境设为 1.0（全量采样），生产环境根据流量设置合适比例
2. **统一日志格式**：所有服务使用相同的日志格式，包含 Trace ID 和 Span ID
3. **配置 Baggage**：传递必要的业务上下文信息（如用户 ID、租户 ID）
4. **跳过健康检查**：避免对 Actuator 端点的追踪造成大量无用数据
5. **关注性能**：追踪会增加少量性能开销，采样率设置需要平衡可观测性和性能
6. **使用专业的追踪后端**：生产环境推荐使用 Zipkin + Elasticsearch 或 Jaeger

## 常见问题

### 1. Trace ID 没有生成

确认 `spring-cloud-starter-sleuth` 依赖已正确添加，且应用启动日志中有 Sleuth 相关信息。

### 2. 下游服务没有收到 Trace ID

确保 RestTemplate 或 WebClient 使用了 Sleuth 的拦截器，不要直接 `new RestTemplate()`。

### 3. Zipkin 中看不到数据

检查 Zipkin Server 是否正常运行，`spring.zipkin.base-url` 配置是否正确，采样率是否为 0。

## 技术栈

- Java 11
- Spring Boot 2.7.12
- Spring Cloud 2021.0.3
- Spring Cloud Sleuth
- Zipkin
- RestTemplate

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```
