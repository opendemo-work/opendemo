# Spring RSocket 演示

## 学习目标

1. 掌握 RSocket 核心协议
2. 理解响应式消息交互模型
3. 学会实现 Request/Response、Fire-and-Forget
4. 掌握 RSocket 与 Spring Boot 集成

## 环境要求

- JDK 17+
- Maven 3.9+

## 交互模型

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| Request/Response | 请求-响应 | RPC 调用 |
| Request/Stream | 请求-流响应 | 列表查询 |
| Fire-and-Forget | 发送即忘 | 事件通知 |
| Channel | 双向流 | 实时通信 |

## 快速开始

```bash
cd spring-rsocket-demo
mvn spring-boot:run
```

## 客户端示例

```java
RSocketRequester requester;

requester.route("greeting")
    .data("World")
    .retrieveMono(String.class);
```

---

**技术栈**: Spring Boot 3.2 | RSocket | Reactor

**版本**: 1.0.0