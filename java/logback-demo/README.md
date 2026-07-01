<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Logback 日志配置演示

> 深入理解 Logback 日志框架，掌握 logback-spring.xml 配置、MDC、Profile 分环境和 Rolling Policy

## 🎯 学习目标

- ✅ 理解 SLF4J + Logback 的日志架构
- ✅ 掌握 logback-spring.xml 的详细配置
- ✅ 学会使用 MDC（Mapped Diagnostic Context）
- ✅ 了解日志滚动策略和日志分级存储
- ✅ 掌握 Spring Profile 与日志配置的结合

---

## 📚 核心概念

| 概念 | 说明 |
|------|------|
| **SLF4J** | 日志门面（Simple Logging Facade） |
| **Logback** | SLF4J 的实现，Spring Boot 默认日志框架 |
| **Appender** | 日志输出目的地（控制台、文件等） |
| **Layout/Encoder** | 日志格式化器 |
| **MDC** | 映射诊断上下文，线程级别的键值对 |
| **Rolling Policy** | 日志滚动/归档策略 |

---

## 🛠️ 日志级别

```
┌──────────────────────────────────────────┐
│         日志级别 (从低到高)                │
├──────────────────────────────────────────┤
│  TRACE ◀ 最详细的调试信息                  │
│    ↓                                     │
│  DEBUG ◀ 调试信息                         │
│    ↓                                     │
│  INFO  ◀ 一般运行信息 (默认级别)            │
│    ↓                                     │
│  WARN  ◀ 警告信息                         │
│    ↓                                     │
│  ERROR ◀ 错误信息                         │
└──────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. logback-spring.xml 配置

```xml
<configuration>
    <!-- 控制台输出 -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <!-- 滚动文件输出 -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>./logs/application.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>./logs/application.%d{yyyy-MM-dd}.log</fileNamePattern>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
    </appender>

    <!-- 按Profile区分配置 -->
    <springProfile name="dev">
        <root level="DEBUG">
            <appender-ref ref="CONSOLE"/>
        </root>
    </springProfile>

    <springProfile name="prod">
        <root level="INFO">
            <appender-ref ref="FILE"/>
        </root>
    </springProfile>
</configuration>
```

### 2. LoggingService - MDC 使用

```java
@Service
public class LoggingService {

    public void logWithMdc(String userId, String action) {
        MDC.put("requestId", UUID.randomUUID().toString());
        MDC.put("userId", userId);

        try {
            logger.info("用户操作: {}", action);
        } finally {
            MDC.clear();
        }
    }
}
```

### 3. 参数化日志

```java
logger.info("用户: {}, 年龄: {}", user, age);
logger.error("操作失败: {}", e.getMessage(), e);

// 条件日志 - 避免不必要的计算
if (logger.isDebugEnabled()) {
    logger.debug("耗时结果: {}", expensiveComputation());
}
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/logback-demo
mvn spring-boot:run
```

### 2. 查看日志输出

```
2026-04-30 10:30:00.123 [main] INFO  c.e.d.LogbackApplication - === Logback 日志演示 ===
2026-04-30 10:30:00.124 [main] TRACE c.e.d.service.LoggingService - TRACE级别
2026-04-30 10:30:00.124 [main] DEBUG c.e.d.service.LoggingService - DEBUG级别
2026-04-30 10:30:00.124 [main] INFO  c.e.d.service.LoggingService - INFO级别
2026-04-30 10:30:00.124 [main] WARN  c.e.d.service.LoggingService - WARN级别
2026-04-30 10:30:00.124 [main] ERROR c.e.d.service.LoggingService - ERROR级别
```

### 3. 切换 Profile

```bash
# 生产环境 - 日志写入文件
mvn spring-boot:run -Dspring-boot.run.profiles=prod

# 测试环境
mvn spring-boot:run -Dspring-boot.run.profiles=test
```

---

## 📁 项目结构

```
logback-demo/
├── src/main/java/com/example/demo/
│   ├── LogbackApplication.java              # 应用入口
│   └── service/
│       └── LoggingService.java              # 日志服务（MDC、分级日志）
├── src/main/resources/
│   ├── application.yml                      # 应用配置
│   └── logback-spring.xml                   # Logback配置
├── src/test/java/com/example/demo/
│   └── LogbackDemoTest.java                 # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 logback-spring.xml 配置要素

| 元素 | 说明 |
|------|------|
| `<appender>` | 定义日志输出目的地 |
| `<encoder>` | 日志格式编码器 |
| `<rollingPolicy>` | 日志滚动策略 |
| `<filter>` | 日志级别过滤器 |
| `<logger>` | 包级别日志配置 |
| `<root>` | 根日志级别配置 |
| `<springProfile>` | Spring Profile 条件配置 |

---

## 🔧 日志格式占位符

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `%d` | 日期时间 | `2026-04-30 10:30:00.123` |
| `%thread` | 线程名 | `main` |
| `%-5level` | 日志级别 | `INFO ` |
| `%logger{36}` | Logger 名称 | `c.e.d.service.LoggingService` |
| `%msg` | 日志消息 | `用户登录成功` |
| `%n` | 换行 | |
| `%X{key}` | MDC 值 | `%X{requestId}` |

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Actuator Demo](../actuator-demo/) - 应用监控
- [AOP Logging](../aop-logging-demo/) - AOP 日志切面

---

*最后更新：2026年4月*

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
