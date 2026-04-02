# Spring Cloud Alibaba Sentinel Demo

Spring Cloud Alibaba Sentinel流量控制、熔断降级演示项目。

## 什么是Sentinel

Sentinel是阿里巴巴开源的分布式系统的流量防卫兵，提供：
- **流量控制**：限流、热点参数限流
- **熔断降级**：异常比例/异常数降级、慢调用比例降级
- **系统保护**：负载保护、自适应限流
- **热点防护**：热点参数自动识别与控制

## 与Hystrix对比

| 特性 | Sentinel | Hystrix |
|------|----------|---------|
| 限流能力 | 丰富（QPS、线程数、热点） | 弱 |
| 熔断策略 | 异常比例/异常数/慢调用 | 异常/超时 |
| 控制台 | 完善的Dashboard | 无原生Dashboard |
| 扩展性 | SPI扩展 | 有限 |
| 社区活跃度 | 高（阿里巴巴维护） | 低（已停更） |

## 技术栈

- Spring Boot 2.7
- Spring Cloud Alibaba Sentinel
- Sentinel Dashboard 1.8+

## 项目结构

```
spring-cloud-alibaba-sentinel-demo/
├── src/main/java/com/example/demo/
│   ├── SentinelDemoApplication.java      # 应用入口
│   └── controller/
│       └── HelloController.java          # 演示控制器
├── src/main/resources/
│   └── application.yml                   # 应用配置
├── pom.xml
└── README.md
```

## 快速开始

### 1. 启动Sentinel Dashboard

```bash
# 下载Sentinel Dashboard
curl -O https://github.com/alibaba/Sentinel/releases/download/1.8.6/sentinel-dashboard-1.8.6.jar

# 启动控制台
java -Dserver.port=8858 -jar sentinel-dashboard-1.8.6.jar

# 访问控制台
open http://localhost:8858
# 默认账号密码: sentinel/sentinel
```

### 2. 启动应用

```bash
mvn spring-boot:run
```

### 3. 初始化监控

**重要**：首次需要访问接口，Sentinel才能识别资源

```bash
# 访问几次接口，触发Sentinel监控
curl http://localhost:8080/hello
curl http://localhost:8080/rate-limit
curl http://localhost:8080/circuit-breaker
```

### 4. 配置限流规则

1. 登录Sentinel控制台
2. 找到 `sentinel-demo` 应用
3. 进入 **簇点链路**
4. 找到 `/rate-limit` 资源
5. 点击 **流控** 按钮
6. 配置：
   - 资源名: `rateLimit`
   - 单机阈值: 1（QPS）
   - 流控模式: 直接
   - 流控效果: 快速失败

### 5. 测试限流

```bash
# 快速请求两次
for i in {1..3}; do curl http://localhost:8080/rate-limit; echo; done

# 第一次成功
{"message":"请求成功","count":1}

# 第二次被限流
{"message":"请求被限流","error":"Too many requests"}
```

### 6. 配置熔断规则

1. 控制台进入 **熔断规则**
2. 点击 **新增熔断规则**
3. 配置：
   - 资源名: `circuitBreaker`
   - 熔断策略: 异常比例
   - 异常比例阈值: 0.5
   - 熔断时长: 10秒

### 7. 测试熔断

```bash
# 多次触发异常
for i in {1..10}; do curl "http://localhost:8080/circuit-breaker?error=true"; echo; done

# 触发熔断后，正常请求也会失败
curl http://localhost:8080/circuit-breaker
{"message":"请求被熔断","error":"Circuit breaker is open"}
```

## 核心注解

### @SentinelResource

```java
@SentinelResource(
    value = "resourceName",      // 资源名
    blockHandler = "handler",    // 限流/降级处理方法
    fallback = "fallback"        // 业务异常降级方法
)
```

## 流量控制策略

### 1. 直接限流
```
QPS > 阈值 → 直接拒绝
```

### 2. 关联限流
```
资源A的限流由资源B的流量决定
例如: 读操作限流受写操作流量影响
```

### 3. 链路限流
```
从入口资源进来的流量进行限流
```

## 熔断降级策略

### 1. 慢调用比例
```
响应时间 > 慢调用RT → 统计为慢调用
慢调用比例 > 阈值 → 触发熔断
```

### 2. 异常比例
```
异常比例 > 阈值 → 触发熔断
```

### 3. 异常数
```
异常数 > 阈值 → 触发熔断
```

## 系统保护规则

保护系统负载，支持：
- Load 自适应
- CPU使用率
- 平均RT
- 并发线程数
- 入口QPS

## 学习要点

1. Sentinel的滑动窗口限流算法
2. 熔断器的状态转换（CLOSED/OPEN/HALF_OPEN）
3. 热点参数限流原理
4. 系统自适应保护算法
5. 与网关（Gateway/Spring Cloud Gateway）的集成

## 参考

- [Sentinel官方文档](https://sentinelguard.io/zh-cn/)
- [Spring Cloud Alibaba](https://github.com/alibaba/spring-cloud-alibaba)
