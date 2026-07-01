<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Spring Boot Actuator 监控演示

> 深入理解 Spring Boot Actuator 的健康检查、指标监控、自定义端点等核心功能

## 🎯 学习目标

- ✅ 理解 Actuator 的作用和核心端点
- ✅ 掌握健康检查（Health Check）的配置与自定义
- ✅ 学会创建自定义 Actuator 端点
- ✅ 了解指标监控（Metrics）的使用方式
- ✅ 掌握 Actuator 安全配置与端点暴露策略

---

## 📚 核心概念

| 概念 | 说明 |
|------|------|
| **Actuator** | Spring Boot 提供的生产级监控和管理模块 |
| **Endpoint** | 监控端点，暴露应用的内部信息 |
| **Health Indicator** | 健康指示器，用于检查特定组件状态 |
| **Metrics** | 运行时指标，如内存使用、HTTP请求统计等 |
| **Info** | 应用静态信息，如版本号、描述等 |

---

## 🛠️ 内置端点一览

| 端点 | 路径 | 说明 |
|------|------|------|
| health | /actuator/health | 应用健康状态 |
| info | /actuator/info | 应用基本信息 |
| metrics | /actuator/metrics | 运行时指标 |
| env | /actuator/env | 环境变量信息 |
| beans | /actuator/beans | Spring Bean 列表 |
| loggers | /actuator/loggers | 日志配置 |
| mappings | /actuator/mappings | 请求映射列表 |
| threaddump | /actuator/threaddump | 线程转储 |
| heapdump | /actuator/heapdump | 堆转储下载 |

---

## 💻 核心代码

### 1. 自定义健康指示器

```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {
        boolean connected = checkConnection();
        if (!connected) {
            return Health.down()
                    .withDetail("database", "MySQL")
                    .withDetail("error", "连接超时")
                    .build();
        }
        return Health.up()
                .withDetail("database", "MySQL")
                .withDetail("activeConnections", 5)
                .build();
    }
}
```

### 2. 自定义 Actuator 端点

```java
@Endpoint(id = "appstatus")
@Component
public class CustomActuatorEndpoint {

    @ReadOperation
    public Map<String, Object> appStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("application", "Actuator Demo");
        status.put("version", "1.0.0");
        status.put("status", "RUNNING");
        return status;
    }

    @WriteOperation
    public void resetCounter() {
        // 重置计数器
    }
}
```

### 3. application.yml 配置

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,env,beans,loggers,appstatus
  endpoint:
    health:
      show-details: always
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/actuator-demo
mvn spring-boot:run
```

### 2. 访问健康检查

```bash
# 基本健康检查
curl http://localhost:8080/actuator/health

# 查看详细信息（含自定义指示器）
curl http://localhost:8080/actuator/health | jq
```

### 3. 访问应用信息

```bash
curl http://localhost:8080/actuator/info
```

### 4. 查看指标

```bash
# 列出所有指标名
curl http://localhost:8080/actuator/metrics

# 查看具体指标
curl http://localhost:8080/actuator/metrics/jvm.memory.used
curl http://localhost:8080/actuator/metrics/http.server.requests
```

### 5. 访问自定义端点

```bash
curl http://localhost:8080/actuator/appstatus
```

---

## 📁 项目结构

```
actuator-demo/
├── src/main/java/com/example/demo/
│   ├── ActuatorApplication.java              # 应用入口
│   ├── health/
│   │   ├── CustomHealthIndicator.java        # 自定义健康指示器
│   │   └── DatabaseHealthIndicator.java      # 数据库健康指示器
│   └── endpoint/
│       └── CustomActuatorEndpoint.java       # 自定义监控端点
├── src/main/resources/
│   └── application.yml                       # 应用配置
├── src/test/java/com/example/demo/
│   └── ActuatorDemoTest.java                 # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 端点安全说明

在生产环境中，应注意以下几点：

- 默认只暴露 `health` 和 `info` 端点
- 使用 `management.endpoints.web.exposure.include` 控制暴露范围
- `show-details` 设为 `never` 可隐藏健康检查详情
- 建议配合 Spring Security 保护敏感端点

```yaml
# 生产环境推荐配置
management:
  endpoints:
    web:
      exposure:
        include: health,info
  endpoint:
    health:
      show-details: when-authorized
```

---

## 🔧 健康状态说明

| 状态 | 说明 |
|------|------|
| **UP** | 服务正常 |
| **DOWN** | 服务不可用 |
| **OUT_OF_SERVICE** | 服务暂停 |
| **UNKNOWN** | 状态未知 |

---

## 📊 常用 Metrics 指标

| 指标 | 说明 |
|------|------|
| `jvm.memory.used` | JVM 已用内存 |
| `jvm.memory.max` | JVM 最大内存 |
| `jvm.gc.pause` | GC 暂停时间 |
| `process.cpu.usage` | 进程 CPU 使用率 |
| `http.server.requests` | HTTP 请求统计 |
| `disk.total` | 磁盘总空间 |
| `disk.free` | 磁盘可用空间 |

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Spring Boot 官方文档 - Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)
- [Spring Boot Admin](https://github.com/codecentric/spring-boot-admin) - 可视化监控面板
- [Micrometer](https://micrometer.io/) - 指标门面库

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
