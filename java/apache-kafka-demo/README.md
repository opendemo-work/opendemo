# Apache Kafka Demo

Apache Kafka消息流处理演示项目，演示Spring Kafka的Producer和Consumer使用。

## 技术栈

- Spring Boot 2.7
- Spring Kafka
- Apache Kafka

## 项目结构

```
apache-kafka-demo/
├── src/main/java/com/example/demo/
│   ├── KafkaDemoApplication.java          # 应用入口
│   ├── config/
│   │   └── KafkaConfig.java               # Kafka配置
│   ├── controller/
│   │   └── KafkaController.java           # REST控制器
│   ├── consumer/
│   │   └── KafkaMessageConsumer.java      # 消息消费者
│   ├── model/
│   │   └── KafkaMessage.java              # 消息实体
│   └── producer/
│       └── KafkaMessageProducer.java      # 消息生产者
├── src/main/resources/
│   └── application.yml                    # 应用配置
├── pom.xml
└── README.md
```

## 核心概念

### Kafka架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Producer   │────▶│    Topic    │────▶│  Consumer   │
└─────────────┘     │  (Partition)│     └─────────────┘
                    └─────────────┘
                           │
                    ┌──────┴──────┐
                    │   Broker    │
                    └─────────────┘
```

- **Producer**: 消息生产者
- **Consumer**: 消息消费者
- **Topic**: 消息主题
- **Partition**: 分区，实现并行处理
- **Broker**: Kafka服务器节点
- **Consumer Group**: 消费者组，组内消费不重复

### Spring Kafka核心注解

#### @EnableKafka
启用Kafka功能。

```java
@Configuration
@EnableKafka
public class KafkaConfig { ... }
```

#### @KafkaListener
标注消息监听方法。

```java
@KafkaListener(topics = "demo-topic", groupId = "demo-group")
public void consume(String message) { ... }
```

## 快速开始

### 1. 启动Kafka

使用Docker Compose启动Kafka：

```yaml
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.0.1
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.0.1
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

```bash
docker-compose up -d
```

### 2. 启动应用

```bash
mvn spring-boot:run
```

### 3. 发送消息

```bash
# 发送简单消息
curl -X POST "http://localhost:8080/api/kafka/send?topic=demo-topic&message=HelloKafka"

# 发送JSON消息
curl -X POST http://localhost:8080/api/kafka/send/json \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello Kafka","topic":"demo-topic"}'

# 批量发送
curl -X POST "http://localhost:8080/api/kafka/send/batch?topic=demo-topic&count=5"

# 发送带Key的消息（保证分区顺序）
curl -X POST "http://localhost:8080/api/kafka/send/keyed?topic=order-topic&key=user-1&message=Order1"

# 快速测试
curl http://localhost:8080/api/kafka/test/demo-topic
```

### 4. 查看消费日志

应用控制台会显示消费者接收到的消息：

```
[Consumer-1] 收到消息: HelloKafka
[Consumer-2] 收到消息: HelloKafka, partition=0, offset=0, key=xxx
```

## 配置详解

### Producer配置

```java
@Bean
public ProducerFactory<String, String> producerFactory() {
    Map<String, Object> configProps = new HashMap<>();
    configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
    configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
    // 可靠性配置
    configProps.put(ProducerConfig.ACKS_CONFIG, "all");  // 所有副本确认
    configProps.put(ProducerConfig.RETRIES_CONFIG, 3);   // 重试次数
    configProps.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);  // 幂等性
    return new DefaultKafkaProducerFactory<>(configProps);
}
```

### Consumer配置

```java
@Bean
public ConsumerFactory<String, String> consumerFactory() {
    Map<String, Object> props = new HashMap<>();
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    props.put(ConsumerConfig.GROUP_ID_CONFIG, "demo-group");
    props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    return new DefaultKafkaConsumerFactory<>(props);
}
```

### Topic定义

```java
@Bean
public NewTopic demoTopic() {
    return new NewTopic("demo-topic", 3, (short) 1);
    // 参数：topic名称, 分区数, 副本数
}
```

## 消费模式

### 1. 基础消费

```java
@KafkaListener(topics = "demo-topic", groupId = "demo-group")
public void consume(String message) {
    System.out.println("收到消息: " + message);
}
```

### 2. 带元数据消费

```java
@KafkaListener(topics = "demo-topic", groupId = "demo-group")
public void consume(
        @Payload String message,
        @Header(KafkaHeaders.RECEIVED_PARTITION_ID) int partition,
        @Header(KafkaHeaders.OFFSET) long offset) {
    System.out.println("消息: " + message + ", 分区: " + partition + ", 偏移量: " + offset);
}
```

### 3. 多Topic监听

```java
@KafkaListener(topics = {"topic1", "topic2"}, groupId = "group")
public void consumeMultiple(String message) { ... }
```

## 消息发送方式

### 1. 异步发送

```java
ListenableFuture<SendResult<String, String>> future = 
    kafkaTemplate.send(topic, key, message);

future.addCallback(
    result -> System.out.println("发送成功"),
    ex -> System.err.println("发送失败: " + ex.getMessage())
);
```

### 2. 同步发送

```java
SendResult<String, String> result = 
    kafkaTemplate.send(topic, message).get();
```

### 3. 带Key发送（保证分区顺序）

```java
// 相同Key的消息会发送到同一个分区
kafkaTemplate.send("order-topic", "user-1", "order-data");
kafkaTemplate.send("order-topic", "user-1", "order-data-2");
```

## 消费者组

### 组内消费（不重复消费）

```
Topic: demo-topic (3 partitions)

Consumer Group: group-A
├─ Consumer-1 → Partition 0
├─ Consumer-2 → Partition 1
└─ Consumer-3 → Partition 2
```

### 广播消费（多个组）

```
Topic: demo-topic
├─ Consumer Group A (所有消息)
└─ Consumer Group B (所有消息)
```

## Kafka命令行工具

```bash
# 查看Topic列表
kafka-topics.sh --bootstrap-server localhost:9092 --list

# 创建Topic
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic my-topic --partitions 3 --replication-factor 1

# 查看Topic详情
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic my-topic

# 发送消息
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic demo-topic

# 消费消息
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic demo-topic --from-beginning

# 查看消费者组
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# 查看消费进度
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group demo-group
```

## 生产环境建议

### 1. 分区数设置
- 根据并发需求设置分区数
- 分区数决定最大消费者数

### 2. 消费者配置
```properties
# 自动提交偏移量
spring.kafka.consumer.enable-auto-commit=true
spring.kafka.consumer.auto-commit-interval=5000

# 批量消费
spring.kafka.listener.type=batch
spring.kafka.consumer.max-poll-records=500
```

### 3. 幂等性保障
- 生产者启用幂等性: `enable.idempotence=true`
- 消费者处理幂等（业务层去重）

### 4. 异常处理
```java
@KafkaListener(topics = "demo-topic", errorHandler = "myErrorHandler")
public void consume(String message) { ... }
```

## 学习要点

1. Kafka核心概念和架构设计
2. Producer的发送模式和可靠性保障
3. Consumer的消费模式和偏移量管理
4. 消费者组的负载均衡机制
5. 分区策略和顺序保证
6. 消息可靠性（ACK、重试、幂等性）
7. Spring Kafka的抽象和封装
