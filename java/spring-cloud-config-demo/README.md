# Spring Cloud Config Demo - 配置中心演示

## 项目概述

本项目演示了 Spring Cloud Config 的完整使用方式，包含一个 Config Server（配置服务端）和一个 Config Client（配置客户端）。通过本 demo，你将学习如何在微服务架构中实现集中式配置管理，包括配置的存储、分发、刷新和版本控制。

## 什么是 Spring Cloud Config

Spring Cloud Config 是 Spring Cloud 体系中的配置管理组件，它为分布式系统中的外部化配置提供了服务器端和客户端的支持。使用 Config Server，你可以在所有环境中集中管理应用程序的外部属性。

### 核心概念

- **Config Server**：集中式配置服务器，从后端存储（Git 仓库、本地文件系统、数据库等）读取配置文件，并以 REST API 的形式提供给客户端
- **Config Client**：需要获取配置的微服务应用，在启动时从 Config Server 拉取配置
- **Environment**：一个配置的环境由三个维度组成：`{application}`、`{profile}` 和 `{label}`
- **Repository**：配置文件的存储后端，通常使用 Git 仓库

## 项目结构

```
spring-cloud-config-demo/
├── pom.xml                          # 父级 POM（packaging=pom）
├── metadata.json                    # 项目元数据
├── README.md                        # 项目文档
├── config-server/                   # 配置服务器模块
│   ├── pom.xml
│   └── src/main/
│       ├── java/com/example/configserver/
│       │   └── ConfigServerApplication.java
│       └── resources/
│           ├── application.yml      # 服务端配置
│           └── configs/             # 示例配置文件（native 模式）
│               ├── application.yml
│               ├── order-service.yml
│               └── order-service-dev.yml
└── config-client/                   # 配置客户端模块
    ├── pom.xml
    └── src/main/
        ├── java/com/example/configclient/
        │   ├── ConfigClientApplication.java
        │   ├── controller/
        │   │   └── ConfigClientController.java
        │   └── service/
        │       └── ConfigService.java
        └── resources/
            └── bootstrap.yml       # 客户端引导配置
```

## Spring Cloud Config 架构

### 整体架构

在微服务架构中，每个服务都有各自的配置需求。Spring Cloud Config 提供了一种中心化的解决方案：

1. 所有配置文件存储在统一的位置（Git 仓库或本地文件系统）
2. Config Server 作为配置的统一入口，负责读取和分发配置
3. 各个微服务（Config Client）在启动时从 Config Server 获取自己的配置
4. 配置变更可以通过 `/actuator/refresh` 端点动态刷新，无需重启服务

### 配置文件命名规则

Config Server 支持以下 URL 格式来获取配置：

```
/{application}/{profile}[/{label}]
/{application}-{profile}.yml
/{label}/{application}-{profile}.yml
/{application}-{profile}.properties
/{label}/{application}-{profile}.properties
```

其中：
- `{application}` = `spring.application.name`
- `{profile}` = `spring.profiles.active`
- `{label}` = Git 分支或标签（可选）

## Config Server 配置

### Native 模式

本 demo 使用 native 模式，配置文件直接从 classpath 读取：

```yaml
server:
  port: 8888

spring:
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/configs
```

### Git 后端模式

在生产环境中，推荐使用 Git 仓库存储配置：

```yaml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/your-org/config-repo
          search-paths: '{application}'
          default-label: main
          username: your-username
          password: your-password
          clone-on-start: true
```

Git 后端的优势：
- 天然支持版本控制，可以追溯配置的变更历史
- 支持分支和标签，方便管理不同环境的配置
- 支持钩子（Webhook），配置变更时自动通知
- 支持多人协作编辑配置

## Config Client 配置

客户端使用 `bootstrap.yml`（而非 `application.yml`）来配置 Config Server 连接信息：

```yaml
spring:
  application:
    name: order-service        # 用于匹配配置文件名
  profiles:
    active: dev                # 激活的 profile
  cloud:
    config:
      uri: http://localhost:8888   # Config Server 地址
      fail-fast: true              # 启动时连接失败则快速失败
      retry:
        max-attempts: 6            # 重试次数
        initial-interval: 1000     # 初始重试间隔（毫秒）
        multiplier: 1.1            # 间隔乘数
        max-interval: 2000         # 最大重试间隔
```

### 为什么使用 bootstrap.yml

Spring Cloud 应用的引导上下文（Bootstrap Context）在主应用上下文之前加载，负责从 Config Server 获取配置。`bootstrap.yml` 中的配置会在 `application.yml` 之前被读取，确保从远程获取的配置能够参与到主应用上下文的构建中。

## Profile 配置管理

Spring Cloud Config 完美支持 Spring Profile 机制，可以实现不同环境的配置隔离。

### 配置文件加载顺序

以 `order-service` 应用、`dev` profile 为例：

1. `application.yml` - 所有应用共享的基础配置
2. `application-dev.yml` - 所有应用在 dev 环境的共享配置
3. `order-service.yml` - order-service 的专属配置
4. `order-service-dev.yml` - order-service 在 dev 环境的专属配置（优先级最高）

后面的配置会覆盖前面的同名属性。

### 本 demo 中的 Profile 示例

**order-service.yml（通用配置）：**
```yaml
server:
  port: 8081
order:
  max-items: 100
  timeout-seconds: 30
  default-currency: CNY
database:
  host: localhost
  port: 3306
  name: order_db
```

**order-service-dev.yml（dev 环境配置）：**
```yaml
order:
  max-items: 500
  timeout-seconds: 60
database:
  name: order_db_dev
logging:
  level:
    root: DEBUG
```

在 dev 环境下，`max-items` 的最终值为 `500`（dev 配置覆盖了通用配置）。

## 配置加密与解密

Spring Cloud Config 支持对敏感配置进行加密存储。

### 对称加密配置

在 Config Server 的 `application.yml` 中配置加密密钥：

```yaml
encrypt:
  key: my-secret-key
```

使用 Config Server 的加密端点：

```bash
# 加密
curl http://localhost:8888/encrypt -d 'my-db-password'

# 解密
curl http://localhost:8888/decrypt -d 'encrypted-value'
```

在配置文件中使用加密值：

```yaml
database:
  password: '{cipher}AQA...encrypted-value...'
```

### 非对称加密

生产环境推荐使用 RSA 密钥对：

```yaml
encrypt:
  key-store:
    location: classpath:/server.jks
    password: keystore-password
    alias: config-server-key
    secret: key-password
```

## 配置动态刷新

### @RefreshScope 注解

在 Config Client 中，使用 `@RefreshScope` 注解标记需要动态刷新配置的 Bean：

```java
@RestController
@RefreshScope
public class ConfigClientController {
    @Value("${order.max-items:50}")
    private int maxItems;
}
```

### 手动触发刷新

修改配置文件后，发送 POST 请求到客户端的刷新端点：

```bash
curl -X POST http://localhost:8081/actuator/refresh
```

### 批量刷新（Spring Cloud Bus）

在大型微服务系统中，手动逐个刷新效率很低。可以集成 Spring Cloud Bus 实现批量刷新：

1. 添加依赖：`spring-cloud-starter-bus-amqp`
2. 配置消息中间件（如 RabbitMQ）
3. 向 Config Server 发送刷新请求，自动广播到所有客户端

```bash
curl -X POST http://localhost:8888/actuator/busrefresh
```

## 运行步骤

### 1. 启动 Config Server

```bash
cd config-server
mvn spring-boot:run
```

验证服务是否正常：

```bash
curl http://localhost:8888/order-service/dev
```

返回的 JSON 中应包含配置信息。

### 2. 启动 Config Client

```bash
cd config-client
mvn spring-boot:run
```

### 3. 验证配置获取

```bash
# 获取全部配置
curl http://localhost:8081/config

# 获取订单相关配置
curl http://localhost:8081/config/order
```

### 4. 测试配置刷新

1. 修改 `config-server/src/main/resources/configs/order-service-dev.yml` 中的某个值
2. 触发刷新：

```bash
curl -X POST http://localhost:8081/actuator/refresh
```

3. 再次访问配置端点，观察值是否已更新

## 关键 API 端点

### Config Server 端点

| 端点 | 说明 |
|------|------|
| `GET /{app}/{profile}` | 获取应用的配置（JSON 格式） |
| `GET /{app}/{profile}/{label}` | 获取指定 label 的配置 |
| `GET /{app}-{profile}.yml` | 获取 YAML 格式的配置 |
| `GET /{app}-{profile}.properties` | 获取 Properties 格式的配置 |
| `POST /encrypt` | 加密明文 |
| `POST /decrypt` | 解密密文 |

### Config Client 端点

| 端点 | 说明 |
|------|------|
| `GET /config` | 获取当前应用配置 |
| `GET /config/order` | 获取订单模块配置 |
| `POST /actuator/refresh` | 刷新配置 |

## Native 后端 vs Git 后端

| 特性 | Native | Git |
|------|--------|-----|
| 适用场景 | 开发测试 | 生产环境 |
| 版本控制 | 不支持 | 原生支持 |
| 配置变更历史 | 无法追溯 | 完整的 Git 历史 |
| 多环境管理 | 手动管理文件 | 使用分支管理 |
| 协作能力 | 弱 | 强（Git 工作流） |
| 部署复杂度 | 低 | 需要额外 Git 仓库 |

## 最佳实践

1. **配置分类管理**：将共享配置放在 `application.yml`，服务专属配置放在 `{service-name}.yml`
2. **环境隔离**：使用 Profile 区分 dev、staging、production 配置
3. **敏感信息加密**：数据库密码、API Key 等必须使用加密功能
4. **快速失败**：开启 `fail-fast: true`，确保配置获取失败时服务不会以错误配置启动
5. **重试机制**：配置 `retry` 参数，增强服务启动时的容错能力
6. **使用 Git 后端**：生产环境务必使用 Git 后端，利用版本控制能力
7. **合理使用 @RefreshScope**：仅在需要动态刷新的 Bean 上添加，避免过度使用

## 常见问题

### 1. 配置客户端无法连接服务端

检查 Config Server 是否正常运行，`spring.cloud.config.uri` 配置是否正确。

### 2. 配置未生效

确认 `bootstrap.yml` 中 `spring.application.name` 与配置文件名匹配，profile 设置正确。

### 3. 刷新不生效

确保需要刷新配置的 Bean 上添加了 `@RefreshScope` 注解，且 Actuator 的 refresh 端点已暴露。

## 技术栈

- Java 11
- Spring Boot 2.7.12
- Spring Cloud 2021.0.3
- Spring Cloud Config Server
- Spring Cloud Config Client
- Spring Boot Actuator
