# Spring Cloud Gateway Advanced Demo

Spring Cloud Gateway高级特性演示项目，包含限流、熔断、鉴权、灰度发布等企业级功能。

## 技术栈

- Spring Boot 2.7
- Spring Cloud Gateway
- Redis (限流)
- Resilience4j (熔断)
- Eureka (服务发现)

## 核心功能

### 1. 动态路由
```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true  # 自动从Eureka发现服务
```

### 2. 限流 (Rate Limiting)
基于Redis的令牌桶算法限流：
```yaml
filters:
  - name: RequestRateLimiter
    args:
      redis-rate-limiter.replenishRate: 10  # 每秒10个请求
      redis-rate-limiter.burstCapacity: 20  # 突发20个请求
      key-resolver: "#{@ipKeyResolver}"      # 按IP限流
```

### 3. 熔断 (Circuit Breaker)
使用Resilience4j实现熔断：
```yaml
filters:
  - name: CircuitBreaker
    args:
      name: userServiceCircuitBreaker
      fallbackUri: forward:/fallback/users
```

### 4. 灰度发布
基于权重的流量分配：
```yaml
# 80%流量到V1
- Weight=product-service, 80
# 20%流量到V2  
- Weight=product-service, 20
```

### 5. 路径重写
```yaml
filters:
  - RewritePath=/api/old/(?<segment>.*), /api/new/$\\{segment}
```

## 快速开始

### 1. 启动依赖服务

```bash
# 启动Redis (限流用)
docker run -d -p 6379:6379 redis:latest

# 启动Eureka
# (参考spring-cloud-eureka-demo)
```

### 2. 启动网关

```bash
mvn spring-boot:run
```

### 3. 测试限流

```bash
# 快速请求10次，部分会被限流
for i in {1..15}; do 
    curl http://localhost:8080/api/users/info
done
```

### 4. 测试熔断

```bash
# 当后端服务异常时，自动触发熔断
curl http://localhost:8080/api/orders/list
```

## 限流策略

### 按IP限流
```java
@Bean
public KeyResolver ipKeyResolver() {
    return exchange -> Mono.just(
        exchange.getRequest().getRemoteAddress().getAddress().getHostAddress()
    );
}
```

### 按用户限流
```java
@Bean
public KeyResolver userKeyResolver() {
    return exchange -> Mono.just(
        exchange.getRequest().getHeaders().getFirst("userId")
    );
}
```

### 按API限流
```java
@Bean
public KeyResolver apiKeyResolver() {
    return exchange -> Mono.just(
        exchange.getRequest().getPath().value()
    );
}
```

## 熔断配置

```yaml
resilience4j:
  circuitbreaker:
    configs:
      default:
        slidingWindowSize: 10        # 滑动窗口大小
        failureRateThreshold: 50      # 失败率阈值50%
        waitDurationInOpenState: 10000  # 熔断10秒
        permittedNumberOfCallsInHalfOpenState: 3  # 半开允许3次调用
```

## 熔断器状态

```
CLOSED (关闭)  →  正常处理请求
    ↓ 失败率超过阈值
OPEN (打开)    →  快速失败，走fallback
    ↓ 等待时间结束
HALF_OPEN (半开) → 允许部分请求测试
    ↓ 成功
CLOSED (关闭)
```

## 高级过滤器

### 鉴权过滤器 (JWT)
```java
@Component
public class AuthFilter extends AbstractGatewayFilterFactory<Config> {
    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            String token = exchange.getRequest().getHeaders().getFirst("Authorization");
            if (token == null || !validateToken(token)) {
                exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
                return exchange.getResponse().setComplete();
            }
            return chain.filter(exchange);
        };
    }
}
```

### 日志过滤器
```java
@Component
public class LoggingFilter extends AbstractGatewayFilterFactory<Config> {
    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            log.info("Request: {} {}", 
                exchange.getRequest().getMethod(),
                exchange.getRequest().getURI()
            );
            return chain.filter(exchange);
        };
    }
}
```

## 性能优化

### 连接池配置
```yaml
spring:
  cloud:
    gateway:
      httpclient:
        pool:
          type: elastic
          max-connections: 1000
          max-idle-time: 10000
```

### 响应缓存
```yaml
spring:
  cloud:
    gateway:
      routes:
        - filters:
            - name: LocalResponseCache
              args:
                cacheName: myCache
                ttl: 5m
```

## 监控端点

```bash
# 查看路由列表
curl http://localhost:8080/actuator/gateway/routes

# 查看网关指标
curl http://localhost:8080/actuator/metrics

# 刷新路由
curl -X POST http://localhost:8080/actuator/gateway/refresh
```

## 生产建议

1. **限流策略**：根据业务特点选择IP/用户/API限流
2. **熔断参数**：根据服务SLA设置合理的阈值
3. **超时设置**：配置合理的连接和响应超时
4. **监控告警**：接入Prometheus+Grafana监控
5. **日志追踪**：集成SkyWalking/Zipkin链路追踪

## 学习要点

1. Gateway的响应式编程模型
2. 令牌桶限流算法原理
3. 熔断器状态机设计
4. 灰度发布的实现策略
5. 网关层安全防护

## 参考

- [Spring Cloud Gateway文档](https://docs.spring.io/spring-cloud-gateway/docs/current/reference/html/)
- [Resilience4j文档](https://resilience4j.readme.io/)
