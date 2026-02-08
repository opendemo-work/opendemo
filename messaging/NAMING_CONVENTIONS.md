# Messaging 技术栈命名大全

本文件定义了消息队列和事件驱动架构中各类组件、主题、队列等的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、消息队列命名规范

### 1.1 队列命名
```bash
# 核心业务队列命名
queues/
├── user.registration.queue              # 用户-注册-队列
├── order.processing.queue               # 订单-处理-队列
├── payment.notification.queue           # 支付-通知-队列
├── email.delivery.queue                 # 邮件-投递-队列
└── sms.notification.queue               # 短信-通知-队列

# 死信队列命名
queues/
├── user.registration.dlq                # 用户-注册-死信队列
├── order.processing.dlq                 # 订单-处理-死信队列
├── payment.notification.dlq             # 支付-通知-死信队列

# 重试队列命名
queues/
├── user.registration.retry              # 用户-注册-重试队列
├── order.processing.retry               # 订单-处理-重试队列
└── payment.notification.retry           # 支付-通知-重试队列
```

### 1.2 主题命名
```bash
# 事件主题命名
topics/
├── user.created                         # 用户-创建事件
├── user.updated                         # 用户-更新事件
├── user.deleted                         # 用户-删除事件
├── order.created                        # 订单-创建事件
├── order.status.changed                 # 订单-状态-变更事件
├── payment.completed                    # 支付-完成事件
├── payment.failed                       # 支付-失败事件
└── inventory.updated                    # 库存-更新事件

# 业务域主题
topics/
├── user-management.user.registered      # 用户管理-用户-注册
├── order-management.order.placed        # 订单管理-订单-下单
├── payment-processing.payment.authorized # 支付处理-支付-授权
├── inventory-management.stock.changed   # 库存管理-库存-变更
└── notification-service.email.sent      # 通知服务-邮件-发送
```

### 1.3 Exchange命名
```bash
# RabbitMQ Exchange命名
exchanges/
├── user.events.exchange                 # 用户-事件-交换机
├── order.events.exchange                # 订单-事件-交换机
├── payment.events.exchange              # 支付-事件-交换机
├── notification.events.exchange         # 通知-事件-交换机
└── system.management.exchange           # 系统-管理-交换机

# Kafka Topic命名
topics/
├── user-service.user-events             # 用户服务-用户事件
├── order-service.order-events           # 订单服务-订单事件
├── payment-service.payment-events       # 支付服务-支付事件
├── notification-service.notification-events # 通知服务-通知事件
└── audit-service.audit-events           # 审计服务-审计事件
```

## 二、消息格式命名规范

### 2.1 消息头命名
```json
{
  "headers": {
    "message.id": "uuid-generated-message-id",
    "message.type": "user.registration",
    "message.timestamp": "2023-12-01T10:30:00Z",
    "correlation.id": "correlation-uuid",
    "reply.to": "user.registration.response.queue",
    "content.type": "application/json",
    "priority": "high",
    "expiration": "60000",
    "delivery.mode": 2,
    
    "source.service": "user-service",
    "target.service": "notification-service",
    "business.domain": "user-management",
    "event.version": "1.0",
    
    "retry.count": 0,
    "max.retries": 3,
    "dead.letter.reason": "",
    
    "trace.id": "trace-uuid",
    "span.id": "span-uuid",
    "parent.span.id": "parent-span-uuid"
  }
}
```

### 2.2 消息体结构
```json
{
  "message": {
    "id": "msg-uuid-12345",
    "type": "user.registration",
    "version": "1.0",
    "timestamp": "2023-12-01T10:30:00Z",
    "source": "user-service",
    "destination": "notification-service"
  },
  
  "payload": {
    "userId": 12345,
    "username": "john_doe",
    "email": "john@example.com",
    "registrationTime": "2023-12-01T10:30:00Z",
    "profile": {
      "firstName": "John",
      "lastName": "Doe",
      "phoneNumber": "+1234567890"
    }
  },
  
  "metadata": {
    "correlationId": "corr-uuid-67890",
    "sessionId": "session-uuid-11111",
    "clientId": "web-client-22222",
    "userId": 12345,
    "tenantId": "tenant-33333"
  },
  
  "context": {
    "traceId": "trace-uuid-44444",
    "spanId": "span-uuid-55555",
    "parentId": "parent-uuid-66666",
    "sampled": true
  }
}
```

## 三、消费者和生产者命名规范

### 3.1 消费者命名
```java
// Java消费者类命名
public class UserRegistrationConsumer {
    // 处理用户注册消息
}

public class OrderProcessingConsumer {
    // 处理订单处理消息
}

public class PaymentNotificationConsumer {
    // 处理支付通知消息
}

public class EmailDeliveryConsumer {
    // 处理邮件投递消息
}

// 消费者组命名
consumer.groups/
├── user-service.group                   # 用户服务-消费组
├── order-service.group                  # 订单服务-消费组
├── payment-service.group                # 支付服务-消费组
└── notification-service.group           # 通知服务-消费组
```

### 3.2 生产者命名
```java
// Java生产者类命名
public class UserEventProducer {
    // 发送用户相关事件
}

public class OrderEventProducer {
    // 发送订单相关事件
}

public class PaymentEventProducer {
    // 发送支付相关事件
}

public class NotificationEventProducer {
    // 发送通知相关事件
}

// 生产者配置
producer.configs/
├── user-events-producer.config          # 用户事件-生产者-配置
├── order-events-producer.config         # 订单事件-生产者-配置
├── payment-events-producer.config       # 支付事件-生产者-配置
└── notification-events-producer.config  # 通知事件-生产者-配置
```

## 四、路由键命名规范

### 4.1 RabbitMQ路由键
```bash
# 路由键命名模式
routing.keys/
├── user.registration                    # 用户.注册
├── user.profile.updated                 # 用户.档案.更新
├── order.created                        # 订单.创建
├── order.status.pending                 # 订单.状态.待处理
├── order.status.processing              # 订单.状态.处理中
├── order.status.completed               # 订单.状态.已完成
├── payment.authorized                   # 支付.已授权
├── payment.captured                     # 支付.已捕获
├── payment.refunded                     # 支付.已退款
└── notification.email.sent              # 通知.邮件.已发送

# 通配符路由键
routing.patterns/
├── user.*                               # 用户相关所有事件
├── order.#                              # 订单相关所有事件（包括子事件）
├── payment.authorized.*                 # 支付授权相关事件
└── notification.#                       # 通知相关所有事件
```

### 4.2 Kafka分区键
```java
// 分区键策略
partition.keys/
├── userId                               # 按用户ID分区
├── orderId                              # 按订单ID分区
├── tenantId                             # 按租户ID分区
├── eventType                            # 按事件类型分区
└── geographicRegion                     # 按地理区域分区

// 分区键生成示例
public class MessagePartitioner {
    public String generatePartitionKey(Message message) {
        switch (message.getType()) {
            case "user.event":
                return String.valueOf(message.getUserId());
            case "order.event":
                return String.valueOf(message.getOrderId());
            case "payment.event":
                return message.getTenantId();
            default:
                return "default";
        }
    }
}
```

## 五、配置和环境命名规范

### 5.1 配置文件命名
```properties
# application-messaging.properties
# 消息队列配置
messaging.rabbitmq.host=localhost
messaging.rabbitmq.port=5672
messaging.rabbitmq.username=guest
messaging.rabbitmq.password=guest
messaging.rabbitmq.virtual-host=/

# 队列配置
messaging.queues.user.registration.name=user.registration.queue
messaging.queues.user.registration.durable=true
messaging.queues.user.registration.auto-delete=false

messaging.queues.order.processing.name=order.processing.queue
messaging.queues.order.processing.durable=true
messaging.queues.order.processing.auto-delete=false

# 交换机配置
messaging.exchanges.user.events.name=user.events.exchange
messaging.exchanges.user.events.type=topic
messaging.exchanges.user.events.durable=true

# 消费者配置
messaging.consumers.user.registration.threads=5
messaging.consumers.user.registration.prefetch=10
messaging.consumers.user.registration.retry-attempts=3
messaging.consumers.user.registration.dead-letter-exchange=user.events.dlx

# 生产者配置
messaging.producers.user.events.batch-size=100
messaging.producers.user.events.linger-ms=5
messaging.producers.user.events.compression-type=gzip
```

### 5.2 环境变量命名
```bash
# 消息队列环境变量
export RABBITMQ_HOST=rabbitmq.prod.company.com
export RABBITMQ_PORT=5672
export RABBITMQ_USERNAME=messaging_user
export RABBITMQ_PASSWORD=secure_password
export RABBITMQ_VIRTUAL_HOST=production

# 队列配置环境变量
export USER_REGISTRATION_QUEUE_NAME=user.registration.queue
export ORDER_PROCESSING_QUEUE_NAME=order.processing.queue
export PAYMENT_NOTIFICATION_QUEUE_NAME=payment.notification.queue

# 交换机配置环境变量
export USER_EVENTS_EXCHANGE_NAME=user.events.exchange
export ORDER_EVENTS_EXCHANGE_NAME=order.events.exchange
export PAYMENT_EVENTS_EXCHANGE_NAME=payment.events.exchange

# 消费者配置环境变量
export USER_REGISTRATION_CONSUMER_THREADS=10
export ORDER_PROCESSING_CONSUMER_THREADS=15
export PAYMENT_NOTIFICATION_CONSUMER_THREADS=5

# 重试配置环境变量
export MESSAGE_RETRY_MAX_ATTEMPTS=3
export MESSAGE_RETRY_BACKOFF_MS=1000
export MESSAGE_RETRY_MULTIPLIER=2.0
```

## 六、监控和告警命名规范

### 6.1 监控指标命名
```java
// Prometheus指标
metrics/
├── messaging_queue_size{queue="user.registration.queue"}  # 队列大小
├── messaging_consumer_lag{consumer_group="user-service.group"}  # 消费者滞后
├── messaging_message_rate{queue="order.processing.queue"}  # 消息速率
├── messaging_processing_time_seconds{operation="consume"}  # 处理时间
├── messaging_error_rate{queue="payment.notification.queue"}  # 错误率
├── messaging_dead_letter_count{queue="user.registration.dlq"}  # 死信数量
└── messaging_retry_count{queue="order.processing.retry"}  # 重试次数

// 自定义监控指标
public class MessagingMetrics {
    private static final Counter messagesPublished = Counter.build()
            .name("messaging_messages_published_total")
            .help("Total number of messages published")
            .labelNames("queue", "message_type")
            .register();
            
    private static final Counter messagesConsumed = Counter.build()
            .name("messaging_messages_consumed_total")
            .help("Total number of messages consumed")
            .labelNames("queue", "message_type", "status")
            .register();
            
    private static final Histogram messageProcessingTime = Histogram.build()
            .name("messaging_message_processing_seconds")
            .help("Message processing time in seconds")
            .labelNames("queue", "message_type")
            .register();
}
```

### 6.2 告警规则命名
```yaml
# Prometheus告警规则
groups:
- name: messaging.alerts
  rules:
  - alert: HighQueueSize
    expr: messaging_queue_size > 10000
    for: 5m
    labels:
      severity: warning
      team: messaging
    annotations:
      summary: "High queue size detected"
      description: "Queue {{ $labels.queue }} has {{ $value }} messages"

  - alert: ConsumerLagTooHigh
    expr: messaging_consumer_lag > 1000
    for: 2m
    labels:
      severity: critical
      team: messaging
    annotations:
      summary: "Consumer lag too high"
      description: "Consumer group {{ $labels.consumer_group }} lag is {{ $value }}"

  - alert: HighErrorRate
    expr: rate(messaging_error_rate[5m]) > 0.05
    for: 1m
    labels:
      severity: warning
      team: messaging
    annotations:
      summary: "High error rate in messaging"
      description: "Error rate is {{ $value }} for queue {{ $labels.queue }}"
```

## 七、故障排查命名规范

### 7.1 调试队列命名
```bash
# 调试和测试队列
debug.queues/
├── test.user.registration.queue         # 测试-用户-注册-队列
├── debug.order.processing.queue         # 调试-订单-处理-队列
├── temp.payment.notification.queue      # 临时-支付-通知-队列
└── sandbox.email.delivery.queue         # 沙盒-邮件-投递-队列

# 影子队列（用于影子测试）
shadow.queues/
├── shadow.user.registration.queue       # 影子-用户-注册-队列
├── shadow.order.processing.queue        # 影子-订单-处理-队列
└── shadow.payment.notification.queue    # 影子-支付-通知-队列
```

### 7.2 问题诊断消息
```json
{
  "diagnostic": {
    "message.id": "diag-msg-001",
    "message.type": "diagnostic.test.message",
    "timestamp": "2023-12-01T10:30:00Z",
    "source": "diagnostic-tool",
    "destination": "debug.queue"
  },
  
  "test.data": {
    "test.id": "test-12345",
    "test.type": "connectivity",
    "target.queue": "user.registration.queue",
    "expected.response": "pong",
    "timeout.ms": 5000
  },
  
  "results": {
    "sent.at": "2023-12-01T10:30:00Z",
    "received.at": "2023-12-01T10:30:01Z",
    "response.time.ms": 1000,
    "status": "success",
    "error.message": ""
  }
}
```

## 八、安全和权限命名规范

### 8.1 用户权限命名
```bash
# 消息队列用户命名
users/
├── messaging.admin                      # 消息-管理员
├── user.service.user                    # 用户-服务-用户
├── order.service.user                   # 订单-服务-用户
├── payment.service.user                 # 支付-服务-用户
└── monitoring.service.user              # 监控-服务-用户

# 权限组命名
permission.groups/
├── messaging.administrators             # 消息-管理员组
├── service.owners                       # 服务-拥有者组
├── readonly.consumers                   # 只读-消费者组
└── restricted.producers                 # 受限-生产者组
```

### 8.2 安全配置
```properties
# 安全配置
messaging.security.enabled=true
messaging.security.authentication=oauth2
messaging.security.authorization.enabled=true

# SSL/TLS配置
messaging.ssl.enabled=true
messaging.ssl.keystore.location=/etc/messaging/keystore.jks
messaging.ssl.keystore.password=keystore_password
messaging.ssl.truststore.location=/etc/messaging/truststore.jks
messaging.ssl.truststore.password=truststore_password

# 网络安全
messaging.network.whitelist.enabled=true
messaging.network.allowed.ips=192.168.1.0/24,10.0.0.0/8
messaging.network.max.connections.per.ip=100
```

## 九、最佳实践示例

### 9.1 消息生产者实现
```java
@Component
public class ReliableMessageProducer {
    
    private static final Logger logger = LoggerFactory.getLogger(ReliableMessageProducer.class);
    
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    @Autowired
    private MeterRegistry meterRegistry;
    
    private final Counter messagesPublished;
    private final Counter publishErrors;
    private final Timer publishTimer;
    
    public ReliableMessageProducer(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.messagesPublished = Counter.builder("messaging.messages.published")
                .description("Total messages published")
                .tags("component", "producer")
                .register(meterRegistry);
        this.publishErrors = Counter.builder("messaging.publish.errors")
                .description("Publish errors")
                .tags("component", "producer")
                .register(meterRegistry);
        this.publishTimer = Timer.builder("messaging.publish.duration")
                .description("Message publish duration")
                .tags("component", "producer")
                .register(meterRegistry);
    }
    
    public void publishUserRegistration(UserRegistrationEvent event) {
        String routingKey = "user.registration";
        String exchange = "user.events.exchange";
        
        MessageWrapper wrapper = MessageWrapper.builder()
                .id(UUID.randomUUID().toString())
                .type("user.registration")
                .timestamp(Instant.now())
                .source("user-service")
                .payload(event)
                .build();
        
        try {
            Timer.Sample sample = Timer.start(meterRegistry);
            
            rabbitTemplate.convertAndSend(exchange, routingKey, wrapper, message -> {
                message.getMessageProperties().setHeader("message.id", wrapper.getId());
                message.getMessageProperties().setHeader("message.type", wrapper.getType());
                message.getMessageProperties().setHeader("correlation.id", 
                    MDC.get("correlationId"));
                return message;
            });
            
            sample.stop(publishTimer);
            messagesPublished.increment();
            
            logger.info("Published user registration event: userId={}", event.getUserId());
            
        } catch (Exception e) {
            publishErrors.increment();
            logger.error("Failed to publish user registration event", e);
            throw new MessagePublishException("Failed to publish message", e);
        }
    }
    
    public void publishWithRetry(Object message, String exchange, String routingKey, 
                                int maxRetries) {
        int attempts = 0;
        while (attempts < maxRetries) {
            try {
                rabbitTemplate.convertAndSend(exchange, routingKey, message);
                return;
            } catch (Exception e) {
                attempts++;
                if (attempts >= maxRetries) {
                    logger.error("Failed to publish message after {} attempts", maxRetries, e);
                    throw e;
                }
                
                long delay = (long) (Math.pow(2, attempts) * 1000); // 指数退避
                try {
                    Thread.sleep(delay);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new MessagePublishException("Interrupted during retry", ie);
                }
                
                logger.warn("Retrying message publish, attempt {}/{}", attempts, maxRetries);
            }
        }
    }
}
```

### 9.2 消息消费者实现
```java
@Component
public class RobustMessageConsumer {
    
    private static final Logger logger = LoggerFactory.getLogger(RobustMessageConsumer.class);
    
    @RabbitListener(queues = "${messaging.queues.user.registration.name}")
    public void handleUserRegistration(MessageWrapper wrapper, 
                                     @Header("amqp_deliveryTag") long deliveryTag,
                                     Channel channel) {
        
        String messageId = wrapper.getId();
        MDC.put("messageId", messageId);
        MDC.put("correlationId", getCorrelationId(wrapper));
        
        try {
            logger.info("Processing user registration event: userId={}", 
                       ((UserRegistrationEvent) wrapper.getPayload()).getUserId());
            
            // 业务逻辑处理
            processUserRegistration((UserRegistrationEvent) wrapper.getPayload());
            
            // 手动确认消息
            channel.basicAck(deliveryTag, false);
            
            logger.info("Successfully processed user registration event");
            
        } catch (BusinessException e) {
            logger.warn("Business error processing message: {}", e.getMessage());
            // 将消息放入死信队列
            channel.basicNack(deliveryTag, false, false);
            
        } catch (TransientException e) {
            logger.warn("Transient error, requeuing message: {}", e.getMessage());
            // 重新入队，让其他消费者处理
            channel.basicNack(deliveryTag, false, true);
            
        } catch (Exception e) {
            logger.error("Unexpected error processing message", e);
            // 记录到监控系统并拒绝消息
            recordErrorMetric(wrapper, e);
            channel.basicNack(deliveryTag, false, false);
        } finally {
            MDC.clear();
        }
    }
    
    @Scheduled(fixedDelay = 30000) // 每30秒检查一次
    public void monitorConsumerHealth() {
        try {
            // 检查消费者连接状态
            checkConnectionHealth();
            
            // 检查未确认消息数量
            checkUnackedMessages();
            
            // 检查队列积压情况
            checkQueueBacklog();
            
        } catch (Exception e) {
            logger.error("Consumer health check failed", e);
        }
    }
    
    private void processUserRegistration(UserRegistrationEvent event) {
        // 实际的业务逻辑处理
        validateEventData(event);
        createUserAccount(event);
        sendWelcomeEmail(event);
        updateAnalytics(event);
    }
    
    private String getCorrelationId(MessageWrapper wrapper) {
        // 从消息头中提取关联ID
        return wrapper.getHeaders().get("correlation.id", String.class);
    }
    
    private void recordErrorMetric(MessageWrapper wrapper, Exception e) {
        // 记录错误指标到监控系统
        meterRegistry.counter("messaging.consumer.errors",
                "queue", "user.registration.queue",
                "error.type", e.getClass().getSimpleName())
                .increment();
    }
}
```

### 9.3 死信队列处理
```java
@Component
public class DeadLetterHandler {
    
    private static final Logger logger = LoggerFactory.getLogger(DeadLetterHandler.class);
    
    @RabbitListener(queues = "user.registration.dlq")
    public void handleDeadLetter(MessageWrapper wrapper,
                               @Header("x-death") List<Map<String, Object>> deathHeaders) {
        
        logger.warn("Processing dead letter message: messageId={}", wrapper.getId());
        
        // 分析死亡原因
        DeathInfo deathInfo = analyzeDeathReason(deathHeaders);
        
        // 根据不同原因采取不同处理策略
        switch (deathInfo.getReason()) {
            case "rejected":
                handleRejectedMessage(wrapper, deathInfo);
                break;
            case "expired":
                handleExpiredMessage(wrapper, deathInfo);
                break;
            case "maxlen":
                handleMaxLengthExceeded(wrapper, deathInfo);
                break;
            default:
                handleUnknownReason(wrapper, deathInfo);
        }
        
        // 发送告警
        sendAlert(wrapper, deathInfo);
        
        // 记录到专门的死信日志
        logDeadLetter(wrapper, deathInfo);
    }
    
    private DeathInfo analyzeDeathReason(List<Map<String, Object>> deathHeaders) {
        if (deathHeaders == null || deathHeaders.isEmpty()) {
            return new DeathInfo("unknown", 0, Instant.now());
        }
        
        Map<String, Object> latestDeath = deathHeaders.get(0);
        return new DeathInfo(
                (String) latestDeath.get("reason"),
                (Integer) latestDeath.get("count"),
                Instant.ofEpochMilli((Long) latestDeath.get("time"))
        );
    }
    
    private void handleRejectedMessage(MessageWrapper wrapper, DeathInfo deathInfo) {
        logger.info("Handling rejected message: {}", wrapper.getId());
        
        // 记录到人工审核队列
        routeToManualReview(wrapper);
        
        // 更新业务状态
        updateBusinessStatus(wrapper, "REJECTED");
    }
    
    private void sendAlert(MessageWrapper wrapper, DeathInfo deathInfo) {
        Alert alert = Alert.builder()
                .level(AlertLevel.CRITICAL)
                .title("Dead Letter Detected")
                .message(String.format("Message %s died due to %s after %d attempts",
                        wrapper.getId(), deathInfo.getReason(), deathInfo.getCount()))
                .timestamp(Instant.now())
                .tags(Map.of(
                        "queue", "user.registration.queue",
                        "messageId", wrapper.getId(),
                        "reason", deathInfo.getReason()
                ))
                .build();
                
        alertService.sendAlert(alert);
    }
}
```

---

**注意事项：**
1. 消息命名应该清晰表达业务含义，避免使用技术术语
2. 队列和主题应该按照业务域进行组织和命名
3. 生产环境中必须实施适当的消息持久化和确认机制
4. 监控告警应该能够快速定位和解决问题
5. 安全配置必须严格控制访问权限和网络访问