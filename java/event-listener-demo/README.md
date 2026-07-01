<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Spring Events 事件监听演示

> 深入理解 Spring 事件机制，掌握 ApplicationEvent、@EventListener、异步事件和条件事件

## 🎯 学习目标

- ✅ 理解 Spring 事件发布/订阅模型
- ✅ 掌握自定义 ApplicationEvent 的创建
- ✅ 学会使用 @EventListener 监听事件
- ✅ 了解 @Async 异步事件处理
- ✅ 掌握条件事件监听（SpEL 表达式过滤）

---

## 📚 核心概念

| 概念 | 说明 |
|------|------|
| **ApplicationEvent** | Spring 事件基类 |
| **ApplicationEventPublisher** | 事件发布器接口 |
| **@EventListener** | 事件监听注解 |
| **@Async** | 异步执行事件处理 |
| **@TransactionalEventListener** | 事务绑定的事件监听 |

---

## 🛠️ 事件传播流程

```
┌────────────────────────────────────────────────────┐
│              Spring Events 传播流程                  │
├────────────────────────────────────────────────────┤
│                                                    │
│  EventPublisher.publishEvent(event)                │
│       ↓                                            │
│  ┌──────────────┐                                  │
│  │ Spring 容器   │                                  │
│  └──────┬───────┘                                  │
│         │                                          │
│    ┌────┼────┬────────────┐                        │
│    ↓    ↓    ↓            ↓                        │
│  邮件  短信  订单处理    高价值订单                   │
│  监听  监听  监听器      监听器                       │
│  (同步) (异步) (同步)    (条件>1000)                  │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. 自定义事件

```java
public class UserRegisteredEvent extends ApplicationEvent {
    private final String username;
    private final String email;

    public UserRegisteredEvent(Object source, String username, String email) {
        super(source);
        this.username = username;
        this.email = email;
    }
}
```

### 2. 事件发布器

```java
@Service
public class EventPublisherService {

    private final ApplicationEventPublisher eventPublisher;

    public void publishUserRegistered(String username, String email) {
        eventPublisher.publishEvent(
            new UserRegisteredEvent(this, username, email));
    }
}
```

### 3. 事件监听器

```java
@Component
public class EmailNotificationListener {

    @EventListener
    public void handleUserRegistered(UserRegisteredEvent event) {
        logger.info("[邮件通知] 发送欢迎邮件给: {}", event.getUsername());
    }
}

@Component
public class SmsNotificationListener {

    @Async
    @EventListener
    public void handleUserRegistered(UserRegisteredEvent event) {
        logger.info("[短信通知] 发送注册成功短信给: {}", event.getUsername());
    }
}
```

### 4. 条件事件监听

```java
@Component
public class OrderEventListener {

    @EventListener(condition = "#event.amount > 1000")
    public void handleHighValueOrder(OrderCreatedEvent event) {
        logger.info("[VIP订单] 高价值订单通知: {}", event.getOrderId());
    }
}
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/event-listener-demo
mvn spring-boot:run
```

### 2. 观察日志输出

```
=== Spring Events 演示 ===
[邮件通知] 发送欢迎邮件给: 张三 (zhangsan@test.com)
[短信通知] 发送注册成功短信给: 张三
[订单处理] 订单创建: orderId=ORD001, user=张三, amount=500.0
[订单处理] 订单创建: orderId=ORD002, user=李四, amount=2000.0
[VIP订单] 高价值订单通知: orderId=ORD002, amount=2000.0
[短信通知] 短信发送完成: 张三
```

---

## 📁 项目结构

```
event-listener-demo/
├── src/main/java/com/example/demo/
│   ├── EventListenerApplication.java         # 应用入口
│   ├── event/
│   │   ├── UserRegisteredEvent.java          # 用户注册事件
│   │   └── OrderCreatedEvent.java            # 订单创建事件
│   ├── listener/
│   │   ├── EmailNotificationListener.java    # 邮件通知监听器
│   │   ├── SmsNotificationListener.java      # 短信通知监听器(异步)
│   │   └── OrderEventListener.java           # 订单事件监听器(条件)
│   └── service/
│       └── EventPublisherService.java        # 事件发布服务
├── src/test/java/com/example/demo/
│   └── EventListenerDemoTest.java            # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 @EventListener 高级用法

| 特性 | 示例 |
|------|------|
| 条件过滤 | `@EventListener(condition = "#event.amount > 100")` |
| 异步处理 | `@Async @EventListener` |
| 事务绑定 | `@TransactionalEventListener(phase = AFTER_COMMIT)` |
| SpEL 表达式 | `#event.username.contains('admin')` |

---

## 🔧 注意事项

- 同步事件按注册顺序执行，注意性能影响
- 异步事件需要 `@EnableAsync` 配置
- 事件处理器中避免抛出异常（会影响其他监听器）
- 事件对象应设计为不可变
- 同步事件在发布者线程中执行

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Spring Core IoC](../spring-core-ioc-demo/) - IoC 容器
- [AOP Logging](../aop-logging-demo/) - AOP 切面编程

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
