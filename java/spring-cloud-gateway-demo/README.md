# Spring Cloud Gateway - API 网关路由与过滤

> 使用 Spring Cloud Gateway 构建 API 网关，演示路由转发、负载均衡、限流、熔断和自定义过滤器。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 使用 Spring Cloud Gateway 创建 API 网关
- ✅ 配置路由规则和断言（Predicate）
- ✅ 实现全局过滤器和局部过滤器
- ✅ 集成 Sentinel 或 Redis 实现限流

---

## 📐 架构图

```
客户端 ──▶ Spring Cloud Gateway ──┬─▶ /api/users ──▶ user-service
                                  ├─▶ /api/orders ──▶ order-service
                                  └─▶ /api/pay ────▶ pay-service
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 |
|------|----------|
| JDK | >= 17 |
| Maven | >= 3.8 |

### 启动

```bash
cd java/spring-cloud-gateway-demo
mvn spring-boot:run
```

---

## 📖 核心概念

### 1. Route

路由是网关的基本构建块，包含 ID、目标 URI、断言和过滤器。

### 2. Predicate

断言用于匹配请求：

- Path
- Method
- Header
- Query
- After/Before/Between

### 3. Filter

过滤器用于修改请求或响应：

- AddRequestHeader
- StripPrefix
- RewritePath
- RequestRateLimiter
- CircuitBreaker

---

## 💻 代码示例

### application.yml 路由配置

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/users/**
          filters:
            - StripPrefix=1
        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
          filters:
            - StripPrefix=1
```

### 自定义过滤器

```java
@Component
public class LoggingFilter implements GlobalFilter, Ordered {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        System.out.println("Request path: " + exchange.getRequest().getPath());
        return chain.filter(exchange);
    }

    @Override
    public int getOrder() {
        return -1;
    }
}
```

### 限流配置

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: rate-limited-route
          uri: http://localhost:8081
          predicates:
            - Path=/limited/**
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
```

---

## 🧪 验证测试

```bash
# 测试路由
curl http://localhost:8080/api/users/1

# 测试限流
for i in {1..15}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/limited/; done
```

---

## 📚 扩展学习

- [Spring Boot Actuator](../actuator-demo/)
- [Java 并发编程](../concurrent-programming-demo/)
- [Spring Cloud Gateway 文档](https://docs.spring.io/spring-cloud-gateway/docs/current/reference/html/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 核心流程

spring-cloud-gateway-demo 从启动到完成主要包含以下环节：

1. **环境准备**：配置运行所需的依赖、网络和存储资源。
2. **主流程执行**：运行案例的核心逻辑并产出结果。
3. **结果验证**：通过日志、命令输出或测试用例确认正确性。
4. **资源回收**：停止服务并清理临时数据，保证可重复执行。

### 设计要点

| 方面 | 做法 | 说明 |
|------|------|------|
| 部署方式 | 本地容器化 | 减少环境差异，便于复现 |
| 配置管理 | 配置文件 + 环境变量 | 兼顾可读性与灵活性 |
| 可观测性 | 日志 + 健康检查 | 方便定位问题 |
| 扩展方式 | 模块化组织 | 后续可按需增加功能 |

### 需要关注的指标

在生产环境中落地类似方案时，建议留意：

- 关键路径的响应延迟
- CPU、内存、磁盘和网络资源使用
- 并发量与吞吐量变化
- 错误率和异常告警

---

## 🛡️ 安全与最佳实践

### 安全建议

- 生产环境不要使用默认密码、密钥或令牌。
- 定期将依赖升级到稳定的最新版本。
- 敏感配置优先使用密钥管理工具或环境变量注入。
- 通过防火墙、安全组或网络策略限制访问范围。

### 操作建议

- 修改配置前备份现有环境。
- 将配置文件和脚本纳入版本控制。
- 为核心路径补充自动化测试。
- 保留运行日志以便审计和排障。

---

## 🧪 进阶实验

基础流程跑通后，可以尝试：

1. 调整关键参数，观察对结果的影响。
2. 模拟异常场景，验证容错能力。
3. 增加负载，分析系统瓶颈。
4. 与其他组件组合，形成完整链路。

---

## 📚 扩展资源

- 相关技术的官方文档
- [OpenDemo 项目主页](https://github.com/opendemo)
- GitHub Discussions 与技术社区

---

## 🤝 贡献与反馈

如发现内容有误或希望补充，欢迎提交 Issue 或 Pull Request。

---

*本 README 由 OpenDemo 自动生成并持续维护，欢迎根据实际案例补充细节。*
