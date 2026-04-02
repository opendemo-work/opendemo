# Spring Cloud Hystrix Demo

Spring Cloud Hystrix熔断器演示项目，演示微服务架构中的熔断降级模式。

## 技术栈

- Spring Boot 2.7
- Spring Cloud Netflix Hystrix
- Spring Boot Actuator (监控)

## 项目结构

```
spring-cloud-hystrix-demo/
├── src/main/java/com/example/demo/
│   ├── HystrixDemoApplication.java        # 应用入口
│   ├── controller/
│   │   └── HystrixController.java         # 测试控制器
│   └── service/
│       └── HystrixService.java            # 熔断器服务
├── src/main/resources/
│   └── application.yml                    # 应用配置
├── pom.xml
└── README.md
```

## 核心概念

### 什么是熔断器模式

熔断器模式(Circuit Breaker)是一种防止故障传播的设计模式，类似电路中的保险丝。当服务故障达到一定阈值时，熔断器打开，后续请求直接走降级逻辑，避免雪崩效应。

### Hystrix三种状态

```
CLOSED (关闭)  →  服务正常，请求通过
    ↓ 失败率超过阈值
OPEN (打开)    →  熔断状态，请求走降级
    ↓ 等待sleepWindow时间
HALF-OPEN (半开) → 允许部分请求测试服务恢复
    ↓ 服务恢复
CLOSED (关闭)
```

## 核心注解说明

### @EnableCircuitBreaker
在主类上启用熔断器功能。

```java
@SpringBootApplication
@EnableCircuitBreaker
public class HystrixDemoApplication { ... }
```

### @HystrixCommand
标注需要熔断保护的方法。

```java
@HystrixCommand(
    fallbackMethod = "fallbackMethod",
    commandProperties = {
        @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "3000"),
        @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "10"),
        @HystrixProperty(name = "circuitBreaker.errorThresholdPercentage", value = "50"),
        @HystrixProperty(name = "circuitBreaker.sleepWindowInMilliseconds", value = "10000")
    }
)
public String myService() { ... }
```

## 配置参数详解

| 参数 | 说明 | 默认值 |
|------|------|--------|
| execution.isolation.thread.timeoutInMilliseconds | 执行超时时间 | 1000ms |
| circuitBreaker.requestVolumeThreshold | 熔断触发的最小请求数 | 20 |
| circuitBreaker.errorThresholdPercentage | 错误率阈值 | 50% |
| circuitBreaker.sleepWindowInMilliseconds | 熔断后休眠时间 | 5000ms |
| metrics.rollingStats.timeInMilliseconds | 统计窗口时间 | 10000ms |

## 快速开始

### 1. 启动应用

```bash
mvn spring-boot:run
```

### 2. 测试接口

```bash
# 正常服务
curl http://localhost:8080/api/normal

# 慢服务（可能超时触发降级）
curl http://localhost:8080/api/slow

# 不稳定服务（随机失败）
curl http://localhost:8080/api/unstable

# 异常服务（快速触发熔断）
curl http://localhost:8080/api/error

# 批量测试
curl http://localhost:8080/api/batch-test
```

### 3. 监控端点

```bash
# Hystrix Stream (用于Hystrix Dashboard)
curl http://localhost:8080/actuator/hystrix.stream

# 健康检查
curl http://localhost:8080/actuator/health
```

## 熔断器行为验证

### 1. 超时降级测试

连续调用慢服务接口：

```bash
for i in {1..10}; do curl http://localhost:8080/api/slow; echo; done
```

观察输出：
- 延迟<2000ms时返回正常结果
- 延迟>2000ms时返回降级响应

### 2. 熔断触发测试

连续调用异常服务接口：

```bash
for i in {1..10}; do curl http://localhost:8080/api/error; echo; done
```

观察输出：
- 前3次：执行方法并抛出异常，走降级
- 第4-10次：熔断器打开，直接走降级（不执行方法）
- 等待5秒后：进入半开状态，尝试恢复

### 3. 不稳定服务测试

```bash
for i in {1..20}; do curl http://localhost:8080/api/unstable; echo; done
```

观察输出：
- 部分成功，部分失败走降级
- 当失败率超过50%时触发熔断
- 熔断期间所有请求直接走降级

## Fallback降级方法

```java
@HystrixCommand(fallbackMethod = "fallbackMethod")
public String myService() { ... }

public String fallbackMethod() {
    return "服务降级，返回默认值";
}

// 带异常信息的降级
public String fallbackMethod(Throwable throwable) {
    return "服务异常: " + throwable.getMessage();
}
```

注意事项：
1. 降级方法参数必须与原始方法一致
2. 降级方法可以额外加一个Throwable参数
3. 降级方法返回类型必须与原始方法一致

## Hystrix Dashboard

### 启动Dashboard

```bash
# 添加依赖后启动
docker run -d -p 7979:7979 --name hystrix-dashboard \
  mantisio/hystrix-dashboard
```

### 配置监控

1. 访问 http://localhost:7979/hystrix
2. 输入Stream URL: `http://localhost:8080/actuator/hystrix.stream`
3. 点击"Monitor Stream"

## 生产环境建议

### 1. 线程池隔离

```java
@HystrixCommand(
    threadPoolKey = "myThreadPool",
    threadPoolProperties = {
        @HystrixProperty(name = "coreSize", value = "20"),
        @HystrixProperty(name = "maxQueueSize", value = "100")
    }
)
```

### 2. 信号量隔离（适用于高并发）

```java
@HystrixCommand(
    commandProperties = {
        @HystrixProperty(name = "execution.isolation.strategy", value = "SEMAPHORE"),
        @HystrixProperty(name = "execution.isolation.semaphore.maxConcurrentRequests", value = "100")
    }
)
```

### 3. 缓存请求结果

```java
@CacheResult(cacheKeyMethod = "getCacheKey")
@HystrixCommand
public String getUser(@CacheKey Long id) { ... }
```

## 学习要点

1. 熔断器模式的设计原理
2. Hystrix三种状态的转换机制
3. 线程隔离与信号量隔离的区别
4. 降级策略的设计
5. 熔断参数的调优方法
6. 与Spring Cloud其他组件的集成
