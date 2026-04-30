# Environment Demo

> Spring Environment 抽象演示项目 - 涵盖 Environment API、@Value 注入、Profile 多环境配置管理

## 📚 学习目标

完成本案例后，您将能够：
- ✅ 理解 Spring Environment 抽象体系的核心概念
- ✅ 掌握通过 `Environment` 接口读取配置属性
- ✅ 学会使用 `@Value` 注解注入配置值
- ✅ 理解 Spring Profile 多环境配置机制
- ✅ 掌握 `application.yml` 多环境配置文件的编写
- ✅ 能够在代码中动态获取当前运行环境信息

## 🛠️ 环境准备

### 系统要求
- **JDK版本**: OpenJDK 11+
- **构建工具**: Maven 3.6+
- **IDE推荐**: IntelliJ IDEA / Eclipse / VS Code
- **操作系统**: Windows/Linux/macOS

### 依赖安装
```bash
mvn clean install
```

## 📁 项目结构

```
environment-demo/
├── src/
│   ├── main/
│   │   ├── java/com/example/demo/
│   │   │   ├── EnvironmentDemoApplication.java  # 启动类
│   │   │   ├── config/
│   │   │   │   └── AppConfig.java                # 配置类（Environment + @Value）
│   │   │   ├── service/
│   │   │   │   └── PropertyService.java          # 属性服务
│   │   │   └── controller/
│   │   │       └── EnvironmentController.java    # REST控制器
│   │   └── resources/
│   │       ├── application.yml                   # 主配置
│   │       ├── application-dev.yml               # 开发环境配置
│   │       └── application-prod.yml              # 生产环境配置
│   └── test/
│       └── java/com/example/demo/
│           └── EnvironmentDemoApplicationTest.java
├── pom.xml
├── README.md
└── metadata.json
```

## 🚀 快速开始

### 步骤1：启动项目
```bash
cd environment-demo
mvn spring-boot:run
```

### 步骤2：测试环境信息接口
```bash
# 获取应用配置属性
curl http://localhost:8081/api/env/app-properties

# 获取系统和环境信息
curl http://localhost:8081/api/env/system-info

# 按key查询配置属性
curl http://localhost:8081/api/env/property?key=java.version

# 按key查询（带默认值）
curl http://localhost:8081/api/env/property?key=custom.key&defaultValue=fallback

# 检查属性是否存在
curl http://localhost:8081/api/env/has-property?key=app.name
```

### 步骤3：切换 Profile
```bash
# 使用开发环境
mvn spring-boot:run -Dspring-boot.run.profiles=dev

# 使用生产环境
mvn spring-boot:run -Dspring-boot.run.profiles=prod
```

### 步骤4：运行测试
```bash
mvn test
```

## 🔍 核心代码解析

### 1. Environment 接口核心方法
`AppConfig.java` 通过构造器注入 `Environment`，展示了以下常用方法：

| 方法 | 作用 | 示例 |
|------|------|------|
| `getProperty(key)` | 获取属性值 | `environment.getProperty("java.version")` |
| `getProperty(key, default)` | 获取属性值（带默认值） | `environment.getProperty("server.port", "8080")` |
| `getActiveProfiles()` | 获取激活的Profile | 返回 `String[]` |
| `getDefaultProfiles()` | 获取默认Profile | 返回 `String[]` |
| `containsProperty(key)` | 判断属性是否存在 | 返回 `boolean` |

### 2. @Value 注入配置
```java
@Value("${app.name:default-app}")
private String appName;
```
语法格式：`${property.key:default-value}`，冒号后为默认值。

### 3. Profile 多环境配置

**配置文件命名规则**：
- `application.yml` - 公共配置（所有环境生效）
- `application-dev.yml` - 开发环境配置（`profiles=dev` 时生效）
- `application-prod.yml` - 生产环境配置（`profiles=prod` 时生效）

**Profile 切换方式**：
1. `application.yml` 中 `spring.profiles.active: dev`
2. 命令行参数 `--spring.profiles.active=prod`
3. 环境变量 `SPRING_PROFILES_ACTIVE=prod`
4. JVM 参数 `-Dspring.profiles.active=prod`

### 4. Environment 属性源优先级

Spring Boot 的属性源优先级从高到低：
1. 命令行参数
2. JVM 系统属性 (`System.getProperties()`)
3. 操作系统环境变量
4. `application-{profile}.yml`
5. `application.yml`
6. `@PropertySource` 注解指定的属性文件

### 关键技术点
1. **Environment 与 @Value 的关系**: `@Value` 底层通过 `Environment` 解析属性值
2. **类型安全**: `Environment.getProperty()` 返回 `String`，需手动转换；`@Value` 支持自动类型转换
3. **属性占位符**: `${app.name}` 支持嵌套引用，如 `${app.name:${app.fallback:default}}`
4. **Profile 激活**: 多个 Profile 可同时激活，后面的覆盖前面的属性

## ⚠️ 常见问题与解决方案

### Q1: 配置文件中的属性读取不到？
**问题描述**: `@Value` 注入失败或 `Environment.getProperty()` 返回 null
**解决方案**: 检查属性 key 是否正确拼写、yml 缩进是否正确、配置文件是否在 `src/main/resources` 下

### Q2: Profile 切换不生效？
**问题描述**: 指定了 Profile 但仍然使用默认配置
**解决方案**: 确认配置文件命名正确（`application-{profile}.yml`），确认 `spring.profiles.active` 已正确设置

### Q3: 如何在非 Spring 管理的类中使用 Environment？
**问题描述**: 工具类或静态方法中需要获取配置属性
**解决方案**: 创建一个 `ApplicationContextAware` 实现类，缓存 `ApplicationContext` 引用，通过 `getBean(Environment.class)` 获取

### Q4: yml 和 properties 配置文件哪个优先级高？
**问题描述**: 同时存在 `.yml` 和 `.properties` 文件时的加载顺序
**解决方案**: `.properties` 优先级高于 `.yml`，实际项目中建议统一使用一种格式

## 📚 扩展学习

### 相关技术文档
- [Spring Environment 官方文档](https://docs.spring.io/spring-framework/reference/core/beans/environment.html)
- [Spring Boot Externalized Configuration](https://docs.spring.io/spring-boot/docs/2.7.x/reference/html/features.html#features.external-config)
- [Spring Profile 文档](https://docs.spring.io/spring-boot/docs/2.7.x/reference/html/features.html#features.profiles)

### 进阶学习路径
1. `@ConfigurationProperties` 类型安全的属性绑定
2. `@PropertySource` 加载自定义配置文件
3. Spring Cloud Config 分布式配置中心
4. 配置属性变更监听与热更新

### 企业级应用场景
- **多环境部署**: 开发/测试/预发/生产环境切换
- **配置中心集成**: 与 Nacos、Apollo 等配置中心集成
- **动态配置**: 运行时动态调整配置参数
- **安全配置**: 敏感信息加密存储与解密读取

---
> **💡 提示**: Spring Environment 是 Spring 框架的核心抽象之一，理解其属性解析机制对于排查配置问题至关重要。Profile 机制是实现多环境部署的基础。
