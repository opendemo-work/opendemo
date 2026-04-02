# RabbitMQ 生产者消费者演示

> 消息队列异步通信基础

## 🎯 学习目标

- ✅ 理解消息队列概念
- ✅ 掌握RabbitMQ核心概念
- ✅ 实现生产者发送消息
- ✅ 实现消费者接收消息

---

## 📚 核心概念

### 消息队列模型

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Producer │───▶│  Queue   │───▶│ Consumer │
│ (生产者)  │    │  (队列)   │    │ (消费者)  │
└──────────┘    └──────────┘    └──────────┘
       │                              │
       └────────▶ Exchange ◀─────────┘
                  (交换机)
```

---

## 💻 核心代码

### 生产者
```java
@Component
public class MessageProducer {
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    public void sendMessage(String message) {
        rabbitTemplate.convertAndSend(
            "exchange", "routingKey", message);
    }
}
```

### 消费者
```java
@Component
public class MessageConsumer {
    @RabbitListener(queues = "demo.queue")
    public void receiveMessage(String message) {
        System.out.println("接收: " + message);
    }
}
```

---

*最后更新：2026年4月*
