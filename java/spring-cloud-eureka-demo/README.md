# Spring Cloud Eureka 服务注册发现演示

> 微服务架构核心组件：服务注册、发现、心跳、自我保护机制完整实战

## 目录

- [核心概念](#核心概念)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [Eureka 架构详解](#eureka-架构详解)
- [Eureka Server 配置](#eureka-server-配置)
- [Eureka Client 配置](#eureka-client-配置)
- [服务注册流程](#服务注册流程)
- [服务发现流程](#服务发现流程)
- [心跳与健康检查](#心跳与健康检查)
- [自我保护机制](#自我保护机制)
- [Eureka Dashboard](#eureka-dashboard)
- [测试接口](#测试接口)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

## 核心概念

### 什么是服务注册与发现？

在微服务架构中，服务实例的地址（IP + 端口）是动态变化的。服务注册与发现解决了以下问题：

- **服务如何知道彼此的存在？** → 服务注册
- **服务如何找到其他服务的地址？** → 服务发现
- **服务挂了如何感知？** → 心跳检测

### Eureka 简介

Netflix Eureka 是一个基于 REST 的服务注册发现组件，分为 Eureka Server（注册中心）和 Eureka Client（服务提供者/消费者）。

### 核心角色

```
┌─────────────────────────────────────────────────┐
│                   Eureka Server                  │
│               （服务注册中心）                      │
│                                                  │
│  ┌─────────────── 服务注册表 ────────────────┐    │
│  │  user-service: 192.168.1.10:8080          │    │
│  │  order-service: 192.168.1.11:8081         │    │
│  │  product-service: 192.168.1.12:8082       │    │
│  └───────────────────────────────────────────┘    │
└──────────┬───────────────────┬───────────────────┘
           │                   │
     注册 + 心跳          查询服务列表
           │                   │
    ┌──────▼──────┐    ┌──────▼──────┐
    │  Service A  │    │  Service B  │
    │  (Provider) │    │  (Consumer) │
    └─────────────┘    └─────────────┘
```

### Eureka vs 其他注册中心

| 特性 | Eureka | Nacos | Consul | Zookeeper |
|------|--------|-------|--------|-----------|
| 一致性模型 | AP | AP/CP | CP | CP |
| 健康检查 | 心跳 | 心跳+TCP | TCP+HTTP | 会话保持 |
| 自我保护 | 有 | 有 | 无 | 无 |
| 配置中心 | 无 | 有 | 有 | 无 |
| Spring Cloud 集成 | 原生 | Alibaba | 原生 | 原生 |

> Eureka 采用 AP 模型（可用性优先），在网络分区时仍可提供服务发现功能。

## 技术栈

- Java 11+
- Spring Boot 2.7.0
- Spring Cloud 2021.0.3 (Jubilee)
- Spring Cloud Netflix Eureka

## 项目结构

```
spring-cloud-eureka-demo/
├── pom.xml                           # 父 POM（模块聚合）
├── README.md
├── metadata.json
├── eureka-server/                    # 注册中心模块
│   ├── pom.xml
│   └── src/main/
│       ├── java/com/example/demo/
│       │   └── EurekaServerApplication.java
│       └── resources/
│           └── application.yml
└── eureka-client/                    # 服务提供者模块
    ├── pom.xml
    └── src/main/
        ├── java/com/example/demo/
        │   ├── EurekaClientApplication.java
        │   └── controller/UserController.java
        └── resources/
            └── application.yml
```

## 快速开始

### 前置条件

- JDK 11+
- Maven 3.6+

### 步骤一：启动 Eureka Server

```bash
cd eureka-server
mvn spring-boot:run
```

等待启动完成后访问 Eureka Dashboard：`http://localhost:8761`

### 步骤二：启动 Eureka Client

```bash
cd eureka-client
mvn spring-boot:run
```

### 步骤三：验证服务注册

1. 访问 `http://localhost:8761`，在 Instances 注册列表中看到 `USER-SERVICE`
2. 调用客户端接口验证：`curl http://localhost:8080/users`

## Eureka 架构详解

### 整体架构

```
         注册(POST /eureka/apps/{serviceName})
         ─────────────────────────────────────▶
    Eureka Client                                    Eureka Server
         ◀─────────────────────────────────────     (注册中心)
         获取服务列表(GET /eureka/apps)
         续约(PUT /eureka/apps/{serviceName}/{instanceId})

         ◀─────────────────────────────────────▶
              下线(DELETE /eureka/apps/{serviceName}/{instanceId})
```

### REST API

| 操作 | HTTP 方法 | 路径 |
|------|----------|------|
| 注册服务 | POST | `/eureka/apps/{appName}` |
| 服务续约 | PUT | `/eureka/apps/{appName}/{id}` |
| 取消注册 | DELETE | `/eureka/apps/{appName}/{id}` |
| 获取服务列表 | GET | `/eureka/apps` |
| 增量获取 | GET | `/eureka/apps/delta` |

## Eureka Server 配置

### 关键配置项

```yaml
server:
  port: 8761                          # Eureka Server 端口

eureka:
  instance:
    hostname: localhost               # 实例主机名
  client:
    register-with-eureka: false       # 不向自己注册
    fetch-registry: false             # 不拉取服务列表
    service-url:
      defaultZone: http://localhost:8761/eureka/
  server:
    enable-self-preservation: false   # 关闭自我保护（开发环境）
    eviction-interval-timer-in-ms: 5000  # 清理间隔
```

### 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `register-with-eureka` | 是否将自己注册到 Eureka | true |
| `fetch-registry` | 是否拉取服务注册表 | true |
| `enable-self-preservation` | 是否启用自我保护 | true |
| `eviction-interval-timer-in-ms` | 清理过期实例的间隔 | 60000ms |

## Eureka Client 配置

### 关键配置项

```yaml
server:
  port: 8080

spring:
  application:
    name: user-service                # 服务名称（注册到 Eureka 的名称）

eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
    register-with-eureka: true        # 注册到 Eureka
    fetch-registry: true              # 拉取服务列表
  instance:
    prefer-ip-address: true           # 使用 IP 注册
    instance-id: ${spring.application.name}:${server.port}
    lease-renewal-interval-in-seconds: 30     # 心跳间隔
    lease-expiration-duration-in-seconds: 90  # 过期时间
```

### 实例配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `prefer-ip-address` | 使用 IP 而非主机名 | false |
| `instance-id` | 实例唯一标识 | 主机名:应用名:端口 |
| `lease-renewal-interval-in-seconds` | 心跳发送间隔 | 30s |
| `lease-expiration-duration-in-seconds` | 多久未心跳视为过期 | 90s |

## 服务注册流程

```
Client 启动
    ↓
读取 eureka.client.service-url 配置
    ↓
POST /eureka/apps/{serviceName}
请求体包含: 实例ID、IP、端口、健康检查URL
    ↓
Server 将实例信息写入注册表
    ↓
Client 启动心跳线程（默认30秒一次）
```

### 注册信息

```json
{
    "instance": {
        "instanceId": "user-service:8080",
        "hostName": "192.168.1.10",
        "ipAddr": "192.168.1.10",
        "status": "UP",
        "port": {"$": 8080, "@enabled": true},
        "app": "USER-SERVICE",
        "healthCheckUrl": "http://192.168.1.10:8080/actuator/health"
    }
}
```

## 服务发现流程

```
Client 启动
    ↓
GET /eureka/apps （全量拉取）
    ↓
缓存到本地注册表
    ↓
定时增量拉取（默认30秒）
    ↓
消费者从本地缓存获取服务地址
    ↓
通过 Ribbon/LoadBalancer 进行客户端负载均衡
```

### 缓存层级

Eureka Client 有多级缓存：

1. **ReadOnlyCacheMap**：只读缓存（默认30秒更新）
2. **ReadWriteCacheMap**：读写缓存（默认180秒过期）
3. **注册表**：实际数据存储

> 这意味着服务下线后，消费者最长可能需要 30 + 180 = 210 秒才能感知。

## 心跳与健康检查

### 心跳机制

```
Client                              Server
  │                                   │
  │─── PUT /eureka/apps/{app}/{id} ──▶│  (每30秒)
  │◀──────── 200 OK ─────────────────│
  │                                   │
  │─── PUT /eureka/apps/{app}/{id} ──▶│  (再30秒)
  │◀──────── 200 OK ─────────────────│
  │                                   │
  │   (90秒未收到心跳)                  │
  │                                   │
  │                              标记实例为 DOWN
  │                              从注册表中移除
```

### 心跳参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `lease-renewal-interval-in-seconds` | 心跳发送间隔 | 30s |
| `lease-expiration-duration-in-seconds` | 心跳超时时间 | 90s |

> 生产环境建议心跳间隔 10s，超时时间 30s，以更快感知服务变化。

## 自我保护机制

### 什么是自我保护？

当 Eureka Server 在短时间内丢失大量心跳时（超过 85% 的实例未发送心跳），会进入自我保护模式。此时 Eureka Server 不再移除过期实例。

### 为什么需要自我保护？

网络分区是常见问题，并非所有心跳丢失都意味着服务真的挂了。自我保护防止在网络抖动时错误地将健康实例剔除。

### 自我保护触发条件

```
期望心跳数 = 注册实例数 × (60 / 心跳间隔)
实际心跳数 = 最近一分钟收到的续约次数

如果 实际心跳数 < 期望心跳数 × 0.85 → 触发自我保护
```

### 开发/生产环境建议

- **开发环境**：关闭自我保护 `enable-self-preservation: false`，便于快速调试
- **生产环境**：开启自我保护 `enable-self-preservation: true`，保证可用性

## Eureka Dashboard

访问 `http://localhost:8761` 可以看到 Eureka 的管理界面：

- **System Status**：Eureka Server 状态信息
- **DS Replicas**：副本节点列表
- **Instances currently registered with Eureka**：已注册的服务实例
- **General Info**：系统信息（内存、CPU）

### Dashboard 关键信息

| 字段 | 说明 |
|------|------|
| Environment | 运行环境（默认 test） |
| Data Center | 数据中心（默认 MyOwn） |
| Current Time | Server 当前时间 |
| Uptime | 运行时长 |
| Lease expiration enabled | 是否启用过期剔除 |
| Renews threshold | 续约阈值 |
| Renews (last min) | 最近一分钟续约数 |

## 测试接口

```bash
# 查看 Eureka 注册的服务列表
curl http://localhost:8761/eureka/apps

# 查看特定服务实例
curl http://localhost:8761/eureka/apps/USER-SERVICE

# 调用客户端接口
curl http://localhost:8080/users

# 健康检查
curl http://localhost:8080/users/health
```

## 最佳实践

### 1. 生产环境配置

```yaml
eureka:
  server:
    enable-self-preservation: true
    eviction-interval-timer-in-ms: 60000
  instance:
    lease-renewal-interval-in-seconds: 10
    lease-expiration-duration-in-seconds: 30
```

### 2. 高可用部署

Eureka Server 支持集群部署，多个节点互相注册：

```yaml
# Server 1
eureka:
  client:
    service-url:
      defaultZone: http://server2:8761/eureka/,http://server3:8761/eureka/

# Server 2
eureka:
  client:
    service-url:
      defaultZone: http://server1:8761/eureka/,http://server3:8761/eureka/
```

### 3. 优雅停机

在客户端停机时主动发送下线请求：

```java
@PreDestroy
public void unregister() {
    // Eureka Client 会自动处理
}
```

或配置 `endpoints.shutdown.enabled=true` 触发优雅停机。

### 4. 安全配置

为 Eureka Server 添加认证：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable()
            .authorizeRequests()
            .anyRequest().authenticated()
            .and()
            .httpBasic();
    }
}
```

## 常见问题

### Q: Eureka 和 Nacos 该选哪个？

- **新项目推荐 Nacos**：功能更全（配置中心 + 注册中心），性能更好
- **维护旧项目用 Eureka**：Spring Cloud Netflix 生态成熟，社区资料多
- Eureka 2.x 已停止维护，但 1.x 仍然稳定可用

### Q: 服务注册后多久能被发现？

默认情况下，客户端需要 30 秒拉取一次增量更新。加上缓存，最长可能需要约 3 分钟。

### Q: 如何强制下线一个实例？

调用 Eureka REST API：
```bash
curl -X PUT http://localhost:8761/eureka/apps/{appName}/{instanceId}/status?value=OUT_OF_SERVICE
```

### Q: Eureka Server 挂了怎么办？

Eureka Client 本地缓存了服务列表，可以继续工作。但不支持新的服务注册和发现。

### Q: 多个 Eureka Server 如何同步？

Eureka 采用 Peer-to-Peer 复制模型，节点之间通过 `service-url` 互相注册，自动同步注册表。

## 扩展阅读

- [Spring Cloud Netflix Eureka 官方文档](https://docs.spring.io/spring-cloud-netflix/docs/current/reference/html/)
- [Netflix Eureka Wiki](https://github.com/Netflix/eureka/wiki)
- [Spring Cloud 服务注册发现对比](https://spring.io/blog/2020/03/25/spring-cloud-2020-0-0-m1-aka-ilford-available-now)
