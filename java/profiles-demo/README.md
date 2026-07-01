<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Profiles Demo - Spring Boot 多环境配置

> Spring Profiles 多环境配置实战：开发、测试、生产环境的配置隔离与动态切换

## 目录

- [核心概念](#核心概念)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [Profile 配置文件](#profile-配置文件)
- [激活 Profile 的方式](#激活-profile-的方式)
- [@Profile 注解详解](#profile-注解详解)
- [ProfileConfig 配置类](#profileconfig-配置类)
- [运行时切换](#运行时切换)
- [测试接口](#测试接口)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

## 核心概念

### 什么是 Spring Profiles？

Spring Profiles 是 Spring 框架提供的环境隔离机制，允许根据不同的运行环境（开发、测试、生产）注册不同的 Bean、加载不同的配置。

### 为什么需要多环境配置？

在实际开发中，不同环境的配置差异很大：

| 配置项 | 开发环境 (dev) | 生产环境 (prod) |
|--------|---------------|----------------|
| 数据库连接 | localhost:3306 | prod-db.internal:3306 |
| 日志级别 | DEBUG | WARN |
| 端口 | 8080 | 80 |
| 缓存 | 禁用 | 启用 |
| Swagger | 启用 | 禁用 |

使用 Profiles 可以避免手动修改配置文件带来的错误，实现一次打包、多处运行。

### 配置加载优先级

```
application.yml (基础配置)
    ↓ 覆盖
application-{profile}.yml (Profile 配置)
    ↓ 覆盖
命令行参数 / 环境变量
```

Profile 配置中的属性会覆盖基础配置中的同名属性。

## 技术栈

- Java 11+
- Spring Boot 2.7.14
- Spring Web (spring-boot-starter-web)
- JUnit 5 + Spring Boot Test

## 项目结构

```
profiles-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/main/
    ├── java/com/example/demo/
    │   ├── ProfilesApplication.java            # 启动类
    │   ├── config/
    │   │   └── ProfileConfig.java              # Profile 条件配置
    │   └── controller/
    │       └── ProfileController.java          # Profile 信息接口
    └── resources/
        ├── application.yml                     # 基础配置
        ├── application-dev.yml                 # 开发环境配置
        └── application-prod.yml                # 生产环境配置
```

## 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用默认 profile (dev) 启动
mvn spring-boot:run

# 指定生产环境启动
mvn spring-boot:run -Dspring-boot.run.profiles=prod

# 打包并运行
mvn clean package
java -jar target/profiles-demo-1.0-SNAPSHOT.jar --spring.profiles.active=prod

# 运行测试
mvn test
```

## Profile 配置文件

### application.yml (基础配置)

基础配置定义所有环境共享的属性：

```yaml
spring:
  profiles:
    active: dev

app:
  name: DemoApp
  env: default
```

### application-dev.yml (开发环境)

```yaml
app:
  env: development

server:
  port: 8080
```

### application-prod.yml (生产环境)

```yaml
app:
  env: production

server:
  port: 80
```

### 命名规则

配置文件命名格式为 `application-{profile}.yml`，其中 `{profile}` 是 Profile 名称。

支持的格式：
- `application-{profile}.yml`
- `application-{profile}.yaml`
- `application-{profile}.properties`

## 激活 Profile 的方式

### 方式一：配置文件

在 `application.yml` 中指定默认激活的 Profile：

```yaml
spring:
  profiles:
    active: dev
```

### 方式二：命令行参数

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
java -jar app.jar --spring.profiles.active=prod
```

或使用 Maven：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn spring-boot:run -Dspring-boot.run.profiles=prod
```

### 方式三：环境变量

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
export SPRING_PROFILES_ACTIVE=prod
java -jar app.jar
```

Spring Boot 会自动将环境变量中的 `SPRING_PROFILES_ACTIVE` 映射为 `spring.profiles.active`。

### 方式四：JVM 参数

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
java -Dspring.profiles.active=prod -jar app.jar
```

### 方式五：代码中指定

```java
SpringApplication app = new SpringApplication(App.class);
app.setAdditionalProfiles("prod");
app.run(args);
```

### 优先级（从高到低）

1. 命令行参数 `--spring.profiles.active`
2. JVM 系统属性 `-Dspring.profiles.active`
3. 环境变量 `SPRING_PROFILES_ACTIVE`
4. `application.yml` 中的 `spring.profiles.active`
5. 默认 `default` Profile

## @Profile 注解详解

`@Profile` 注解用于限制 Bean 的注册条件，只在指定 Profile 激活时才创建该 Bean。

### 用在 @Configuration 类上

```java
@Configuration
@Profile("dev")
public class DevConfig {
    // 只在 dev 环境生效
}
```

### 用在 @Bean 方法上

```java
@Configuration
public class ProfileConfig {

    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        // 开发环境数据源
    }

    @Bean
    @Profile("prod")
    public DataSource prodDataSource() {
        // 生产环境数据源
    }
}
```

### 用在 @Component 类上

```java
@Component
@Profile("prod")
public class ProdOnlyService {
    // 只在 prod 环境被注册
}
```

### 取反匹配

```java
@Profile("!prod")   // 非 prod 环境生效
@Profile("dev | test")  // dev 或 test 环境生效
```

## ProfileConfig 配置类

本项目通过 `ProfileConfig` 演示 @Profile 条件注入：

```java
@Configuration
public class ProfileConfig {

    @Bean
    @Profile("dev")
    public String devMessage() {
        return "开发环境配置已加载";
    }

    @Bean
    @Profile("prod")
    public String prodMessage() {
        return "生产环境配置已加载";
    }
}
```

## 运行时切换

### 查看当前 Profile

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
curl http://localhost:8080/info
```

响应示例（dev 环境）：
```json
{
    "appName": "DemoApp",
    "env": "development",
    "activeProfile": "dev",
    "message": "开发环境配置已加载"
}
```

### 切换到生产环境

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 停止应用，使用 prod profile 重启
mvn spring-boot:run -Dspring-boot.run.profiles=prod
```

再次请求 `/info`：
```json
{
    "appName": "DemoApp",
    "env": "production",
    "activeProfile": "prod",
    "message": "生产环境配置已加载"
}
```

## 测试接口

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查看 Profile 信息
curl http://localhost:8080/info

# 查看所有 Bean 信息
curl http://localhost:8080/info/beans
```

## 最佳实践

1. **基础配置放公共属性**：`application.yml` 放所有环境共享的配置
2. **Profile 配置只写差异**：`application-{profile}.yml` 只写该环境特有的配置
3. **默认使用开发环境**：设置 `spring.profiles.active=dev` 作为默认值
4. **敏感信息不放代码**：数据库密码等使用环境变量或配置中心
5. **生产环境禁用调试功能**：如 Swagger、Actuator 的敏感端点
6. **测试使用专用 Profile**：创建 `application-test.yml` 用于单元测试

### 推荐的 Profile 划分

| Profile | 用途 | 说明 |
|---------|------|------|
| `dev` | 本地开发 | 使用内嵌数据库、DEBUG 日志 |
| `test` | 自动化测试 | 使用内存数据库、Mock 服务 |
| `staging` | 预发布 | 与生产配置一致，连接预发布环境 |
| `prod` | 生产 | 优化配置、安全设置、WARN 日志 |

## 常见问题

### Q: 可以同时激活多个 Profile 吗？

可以。使用逗号分隔多个 Profile：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
java -jar app.jar --spring.profiles.active=dev,debug
```

### Q: Profile 配置和基础配置冲突时以谁为准？

Profile 配置优先级更高，会覆盖基础配置中的同名属性。

### Q: @Profile 和 @Conditional 有什么区别？

`@Profile` 是 `@Conditional` 的特化版本。`@Profile("dev")` 等价于 `@Conditional(ProfileCondition.class)`。`@Conditional` 更灵活，可以自定义条件逻辑。

### Q: 如何在测试中指定 Profile？

使用 `@ActiveProfiles` 注解：
```java
@SpringBootTest
@ActiveProfiles("test")
class MyTest {}
```

### Q: 不指定 Profile 时默认是什么？

默认 Profile 是 `default`。可以通过 `spring.profiles.default` 修改。

## 扩展阅读

- [Spring Boot Profiles 官方文档](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.profiles)
- [Externalized Configuration](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config)
- [Spring @Profile 注解](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Profile.html)

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
