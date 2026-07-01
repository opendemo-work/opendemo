<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# ActiveMQ JMS Demo - Spring Boot 集成 ActiveMQ 消息队列演示

## 项目概述

本项目演示了 Spring Boot 集成 Apache ActiveMQ 实现基于 JMS（Java Message Service）的消息队列功能。通过本 demo，你将学习 Queue（点对点）和 Topic（发布/订阅）两种消息模型，以及 Spring JMS 提供的 `JmsTemplate` 和 `@JmsListener` 等核心组件的使用方式。

## 什么是 JMS

JMS（Java Message Service）是 Java 平台中面向消息中间件（MOM）的 API 标准，用于在两个应用程序之间或分布式系统中发送消息，进行异步通信。

### JMS 核心概念

- **Provider**：JMS 提供者，即消息中间件的实现（如 ActiveMQ、RabbitMQ 等）
- **Client**：JMS 客户端，生产或消费消息的应用程序
- **Producer**：消息生产者，创建并发送消息的客户端
- **Consumer**：消息消费者，接收并处理消息的客户端
- **Message**：消息对象，包含头部（Header）、属性（Properties）和消息体（Body）
- **Destination**：消息目标，消息发送的目的地，分为 Queue 和 Topic 两种

### JMS 消息类型

| 消息类型 | 说明 |
|---------|------|
| TextMessage | 文本消息（字符串） |
| ObjectMessage | Java 对象消息（可序列化对象） |
| MapMessage | 键值对消息 |
| BytesMessage | 二进制字节流消息 |
| StreamMessage | 流消息 |

## Queue vs Topic

### Queue（点对点模型）

```
Producer → [Queue] → Consumer A
                    → Consumer B（同一个 Queue 只有一个消费者会收到消息）
```

特点：
- 每条消息只能被一个消费者消费
- 消息在队列中按 FIFO（先进先出）顺序处理
- 消费者不需要在消息发送时在线，离线消息会被保留
- 适用于任务分发、负载均衡场景

### Topic（发布/订阅模型）

```
Producer → [Topic] → Subscriber A（收到消息）
                    → Subscriber B（收到消息）
                    → Subscriber C（收到消息）
```

特点：
- 每条消息会被所有订阅者消费
- 只有活跃的订阅者才能收到消息（非持久订阅）
- 支持持久订阅，离线订阅者可以在重新上线后收到离线期间的消息
- 适用于事件广播、通知推送场景

### 对比总结

| 特性 | Queue | Topic |
|------|-------|-------|
| 消息消费 | 一条消息只被一个消费者消费 | 一条消息被所有订阅者消费 |
| 消息保留 | 未消费的消息会保留 | 非持久订阅消息不保留 |
| 消费者依赖 | 无需消费者在线 | 通常需要订阅者在线 |
| 典型场景 | 任务分发、异步处理 | 事件通知、数据广播 |
| 负载均衡 | 天然支持（多消费者竞争） | 不支持（每个消费者都处理） |

## 项目结构

```
activemq-jms-demo/
├── pom.xml
├── metadata.json
├── README.md
└── src/main/java/com/example/demo/
    ├── ActiveMqJmsDemoApplication.java
    ├── config/
    │   └── JmsConfig.java              # JMS 配置（ConnectionFactory、JmsTemplate、Listener Factory）
    ├── producer/
    │   └── MessageProducer.java         # 消息生产者
    ├── consumer/
    │   ├── MessageConsumer.java         # Queue 消费者
    │   └── TopicMessageConsumer.java    # Topic 消费者（多个订阅者）
    ├── controller/
    │   └── MessageController.java       # REST API 控制器
    ├── model/
    │   └── EmailMessage.java            # 消息体对象
    └── service/
        └── NotificationService.java     # 消息处理服务
```

## Spring JMS 集成

### ConnectionFactory 配置

Spring Boot 通过 `spring-boot-starter-activemq` 自动配置 ActiveMQ 连接工厂。本 demo 使用嵌入式 Broker：

```yaml
spring:
  activemq:
    broker-url: vm://localhost?broker.persistent=false
    user: admin
    password: admin
    in-memory: true
```

`vm://localhost` 表示使用嵌入式 ActiveMQ Broker（JVM 内部通信），`broker.persistent=false` 表示不持久化消息到磁盘。

### JmsTemplate 使用

`JmsTemplate` 是 Spring 提供的 JMS 操作模板类，简化了消息的发送和接收：

```java
// 发送消息到 Queue
jmsTemplate.convertAndSend("queue-name", message);

// 发送消息到 Topic（需设置 pubSubDomain=true）
jmsTemplate.convertAndSend("topic-name", message);

// 接收消息
Object message = jmsTemplate.receiveAndConvert("queue-name");
```

本 demo 中配置了两个 JmsTemplate：
- `jmsTemplate`：用于 Queue（点对点）
- `topicJmsTemplate`：用于 Topic（发布/订阅），设置 `pubSubDomain = true`

### @JmsListener 注解

`@JmsListener` 是 Spring JMS 提供的消息监听注解，用于异步接收消息：

```java
@JmsListener(destination = "email-queue", containerFactory = "queueListenerFactory")
public void receiveEmailMessage(EmailMessage message) {
    // 处理消息
}
```

关键属性：
- `destination`：监听的目标（Queue 或 Topic 名称）
- `containerFactory`：使用的监听器容器工厂
- `subscription`：持久订阅的名称（用于 Topic）
- `selector`：消息选择器（SQL 语法过滤消息）

### DefaultJmsListenerContainerFactory

为 Queue 和 Topic 分别配置不同的监听器容器工厂：

```java
// Queue 监听器工厂
@Bean
public DefaultJmsListenerContainerFactory queueListenerFactory(ConnectionFactory cf) {
    DefaultJmsListenerContainerFactory factory = new DefaultJmsListenerContainerFactory();
    factory.setConnectionFactory(cf);
    factory.setSessionTransacted(true);
    factory.setConcurrency("1-5");
    return factory;
}

// Topic 监听器工厂
@Bean
public DefaultJmsListenerContainerFactory topicListenerFactory(ConnectionFactory cf) {
    DefaultJmsListenerContainerFactory factory = new DefaultJmsListenerContainerFactory();
    factory.setConnectionFactory(cf);
    factory.setPubSubDomain(true);    // 关键：设置为 Topic 模式
    factory.setConcurrency("1-5");
    return factory;
}
```

## 消息转换

Spring JMS 默认使用 `SimpleMessageConverter` 进行消息转换：

| Java 类型 | JMS 消息类型 |
|----------|-------------|
| String | TextMessage |
| Serializable | ObjectMessage |
| Map | MapMessage |
| byte[] | BytesMessage |

本 demo 中的 `EmailMessage` 实现了 `Serializable` 接口，会被自动转换为 `ObjectMessage`。

### 自定义 MessageConverter

可以自定义消息转换器，例如使用 JSON 格式：

```java
@Bean
public MessageConverter jacksonJmsMessageConverter() {
    MappingJackson2MessageConverter converter = new MappingJackson2MessageConverter();
    converter.setTargetType(TextMessage.class);
    converter.setTypeIdPropertyName("_type");
    return converter;
}
```

## 事务管理

### JMS 事务

在 `JmsConfig` 中配置了事务支持：

```java
factory.setSessionTransacted(true);
```

事务模式下：
- 消息消费失败时会自动回滚，消息重新入队
- 可以结合 `@Transactional` 实现与数据库事务的统一管理
- 避免消息丢失或重复处理

### 本地事务 vs 分布式事务

- **本地事务**：JMS Session 级别的事务，仅保证消息操作的原子性
- **JTA 事务**：使用 JTA（Java Transaction API）实现跨资源的事务管理

## ActiveMQ 配置说明

### 嵌入式 Broker

本 demo 使用嵌入式 ActiveMQ Broker，无需额外安装：

```yaml
spring:
  activemq:
    broker-url: vm://localhost?broker.persistent=false
    in-memory: true
```

优点：
- 零额外部署，适合开发和测试
- 启动速度快
- 无需管理外部服务

缺点：
- 不适合生产环境
- 无法持久化消息（本 demo 配置）
- 性能受限

### 外部 ActiveMQ Broker

生产环境使用外部 ActiveMQ 服务器：

```yaml
spring:
  activemq:
    broker-url: tcp://localhost:61616
    user: admin
    password: admin
    pool:
      enabled: true
      max-connections: 50
```

使用连接池提高性能：

```xml
<dependency>
    <groupId>org.apache.activemq</groupId>
    <artifactId>activemq-pool</artifactId>
</dependency>
```

### ActiveMQ 协议

| 协议 | URL 格式 | 说明 |
|------|---------|------|
| VM | `vm://localhost` | JVM 内部通信（嵌入式） |
| TCP | `tcp://host:port` | 默认协议，远程通信 |
| NIO | `nio://host:port` | 高性能 TCP 变体 |
| SSL | `ssl://host:port` | 加密通信 |
| WebSocket | `ws://host:port` | Web 客户端支持 |

## 运行步骤

### 1. 启动应用

```bash
mvn spring-boot:run
```

应用启动后会自动创建嵌入式 ActiveMQ Broker。

### 2. 发送 Queue 消息（邮件）

```bash
curl -X POST http://localhost:8080/api/messages/queue/email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "Welcome",
    "body": "Hello, welcome to our platform!",
    "from": "noreply@example.com"
  }'
```

观察控制台日志，`MessageConsumer` 会异步接收并处理邮件消息。

### 3. 发送 Queue 消息（通知）

```bash
curl -X POST http://localhost:8080/api/messages/queue/notification \
  -H "Content-Type: application/json" \
  -d '{"message": "New order received!"}'
```

### 4. 发送 Topic 消息（广播）

```bash
curl -X POST http://localhost:8080/api/messages/topic/broadcast \
  -H "Content-Type: application/json" \
  -d '{
    "to": "all-users@example.com",
    "subject": "System Maintenance",
    "body": "System will be down for maintenance at midnight.",
    "from": "admin@example.com"
  }'
```

观察控制台日志，两个订阅者（`subscriber-one` 和 `subscriber-two`）都会收到消息。

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/messages/queue/email` | POST | 发送邮件到 Queue |
| `/api/messages/queue/notification` | POST | 发送通知到 Queue |
| `/api/messages/topic/broadcast` | POST | 广播消息到 Topic |

## 消息处理流程

### Queue 模式

```
HTTP POST → MessageController → MessageProducer → [email-queue] → MessageConsumer → NotificationService
```

1. REST API 接收请求
2. `MessageProducer` 使用 `JmsTemplate` 发送消息到 Queue
3. `MessageConsumer` 通过 `@JmsListener` 异步接收消息
4. `NotificationService` 处理具体的业务逻辑

### Topic 模式

```
HTTP POST → MessageController → MessageProducer → [broadcast-topic] → Subscriber One → NotificationService
                                                                               → Subscriber Two → NotificationService
```

1. REST API 接收请求
2. `MessageProducer` 使用 Topic JmsTemplate 发布消息
3. 所有订阅者（`subscriber-one`、`subscriber-two`）都会收到消息
4. 各订阅者分别处理消息

## 最佳实践

1. **消息对象设计**：消息体应保持简单，避免传递大对象；实现 `Serializable` 接口
2. **异常处理**：在消费者中妥善处理异常，避免消息无限重试
3. **幂等消费**：消费者应设计为幂等操作，防止消息重复消费导致数据不一致
4. **连接池配置**：生产环境务必使用连接池，提高性能和稳定性
5. **消息持久化**：重要的业务消息应配置持久化，防止 Broker 故障导致消息丢失
6. **合理设置并发**：根据业务需求和系统资源设置监听器并发数
7. **消息选择器**：使用 JMS Selector 过滤消息，减少不必要的消息传输

## 常见问题

### 1. 消息对象序列化失败

确保消息对象实现了 `Serializable` 接口，并在 ConnectionFactory 中配置 `trustAllPackages=true`。

### 2. Topic 订阅者收不到消息

确保监听器容器工厂设置了 `pubSubDomain=true`，且订阅者在消息发送前已启动。

### 3. 嵌入式 Broker 启动失败

检查端口是否被占用，或切换到外部 ActiveMQ Broker。

### 4. 消息消费顺序问题

JMS 只保证单个消费者内的消息顺序。多个消费者并行消费时，无法保证全局顺序。

## 技术栈

- Java 11
- Spring Boot 2.7.12
- Spring JMS
- Apache ActiveMQ（嵌入式）
- Spring Web

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

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

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
