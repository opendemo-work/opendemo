<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Spring 条件装配演示

> 深入理解 @Conditional、@Profile、@ConditionalOnProperty 等条件装配注解

## 🎯 学习目标

- ✅ 理解 Spring 条件装配的核心注解
- ✅ 掌握 @ConditionalOnProperty 根据配置动态加载 Bean
- ✅ 学会使用 @Profile 实现多环境配置
- ✅ 了解 Feature Toggle（功能开关）模式

---

## 📚 核心注解

| 注解 | 说明 |
|------|------|
| **@Profile** | 根据 Spring Profile 条件加载 |
| **@ConditionalOnProperty** | 根据配置属性条件加载 |
| **@ConditionalOnBean** | 容器中存在指定 Bean 时加载 |
| **@ConditionalOnClass** | 类路径中存在指定类时加载 |
| **@ConditionalOnMissingBean** | 容器中不存在指定 Bean 时加载 |
| **@ConditionalOnExpression** | SpEL 表达式为 true 时加载 |

---

## 🛠️ 条件装配流程

```
┌──────────────────────────────────────────────┐
│           条件装配决策流程                     │
├──────────────────────────────────────────────┤
│                                              │
│  @Profile("dev")                             │
│       ↓                                      │
│  当前Profile == "dev" ?  ──→ 是 → 注册Bean   │
│                          └──→ 否 → 跳过      │
│                                              │
│  @ConditionalOnProperty("feature.xx")        │
│       ↓                                      │
│  配置项 == true ?  ──→ 是 → 注册Bean         │
│                    └──→ 否 → 跳过            │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. @ConditionalOnProperty 条件配置

```java
@Configuration
public class ConditionalConfig {

    @Bean
    @ConditionalOnProperty(name = "feature.swagger.enabled", havingValue = "true")
    public String swaggerConfig() {
        return "swagger-enabled";
    }

    @Bean
    @ConditionalOnProperty(name = "feature.cache.type", havingValue = "redis")
    public String redisCacheConfig() {
        return "redis-cache";
    }

    @Bean
    @ConditionalOnProperty(name = "feature.cache.type", havingValue = "local",
                           matchIfMissing = true)
    public String localCacheConfig() {
        return "local-cache";
    }
}
```

### 2. @Profile 多环境配置

```java
@Configuration
public class ProfileConfig {

    @Bean
    @Profile("dev")
    public String devDataSource() {
        return "h2-datasource";
    }

    @Bean
    @Profile("prod")
    public String prodDataSource() {
        return "mysql-datasource";
    }

    @Bean
    @Profile({"dev", "test"})
    public String debugToolConfig() {
        return "debug-tools-enabled";
    }
}
```

### 3. Feature Toggle 服务

```java
@Service
public class FeatureToggleService {

    @Value("${feature.swagger.enabled:false}")
    private boolean swaggerEnabled;

    @Value("${feature.cache.type:local}")
    private String cacheType;

    public Map<String, Object> getFeatureStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("swaggerEnabled", swaggerEnabled);
        status.put("cacheType", cacheType);
        return status;
    }
}
```

---

## 🚀 快速开始

### 1. 启动应用（开发环境）

```bash
cd java/conditional-demo
mvn spring-boot:run
```

### 2. 切换 Profile 启动

```bash
# 生产环境
mvn spring-boot:run -Dspring-boot.run.profiles=prod

# 测试环境
mvn spring-boot:run -Dspring-boot.run.profiles=test
```

### 3. 开启功能开关

```bash
mvn spring-boot:run -Dspring-boot.run.arguments="--feature.swagger.enabled=true --feature.cache.type=redis"
```

---

## 📁 项目结构

```
conditional-demo/
├── src/main/java/com/example/demo/
│   ├── ConditionalApplication.java        # 应用入口
│   ├── DevConfig.java                     # 开发环境配置 (@Profile)
│   ├── config/
│   │   ├── ConditionalConfig.java         # 条件配置 (@ConditionalOnProperty)
│   │   └── ProfileConfig.java             # 多环境配置 (@Profile)
│   └── service/
│       └── FeatureToggleService.java      # 功能开关服务
├── src/main/resources/
│   └── application.yml                    # 应用配置
├── src/test/java/com/example/demo/
│   └── ConditionalDemoTest.java           # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 application.yml 配置

```yaml
feature:
  swagger:
    enabled: false        # Swagger开关
  rate-limit:
    enabled: true         # 限流开关
  cache:
    type: local           # 缓存类型: local/redis

spring:
  profiles:
    active: dev           # 激活的环境
```

---

## 🔧 常见使用场景

| 场景 | 推荐注解 |
|------|---------|
| 多环境数据源 | `@Profile` |
| 功能开关 | `@ConditionalOnProperty` |
| 自动配置 | `@ConditionalOnClass` |
| 防止重复 Bean | `@ConditionalOnMissingBean` |

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Profiles Demo](../profiles-demo/) - 环境配置详解
- [Spring Boot Autoconfiguration](../spring-boot-autoconfig-demo/) - 自动配置原理

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
