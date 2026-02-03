# RocketMQ 消息队列演示

## 🎯 概述

本演示展示了Apache RocketMQ分布式消息中间件的核心功能，包括生产者消费者模式、消息过滤、事务消息、延迟消息等企业级特性。

## 🏗️ 技术架构

### 核心组件
- **主要技术**: RocketMQ 5.0+
- **适用场景**: 异步处理、应用解耦、流量削峰、消息通讯
- **难度等级**: 🔴 高级

### 技术栈
```yaml
components:
  - rocketmq: "5.0"
  - openjdk: "11"
  - docker: "20.10+"
  - spring-boot: "2.7"

features:
  - message production/consumption
  - message filtering
  - transactional messages
  - delayed messages
  - message tracing
  - cluster deployment
```

## 🚀 快速开始

### 环境部署
```bash
# 进入消息队列目录
cd messaging/rocketmq-producer-consumer

# 启动RocketMQ集群
docker-compose up -d

# 验证服务状态
docker-compose exec namesrv mqadmin clusterList -n namesrv:9876
```

### 基本使用
```bash
# 发送测试消息
docker-compose exec producer java -jar producer.jar "Hello RocketMQ"

# 查看消费结果
docker-compose logs consumer
```

## 🔧 核心功能演示

### 1. 基础生产者消费者
```java
// Producer示例
public class SimpleProducer {
    public static void main(String[] args) throws Exception {
        DefaultMQProducer producer = new DefaultMQProducer("simple_producer_group");
        producer.setNamesrvAddr("namesrv:9876");
        producer.start();
        
        for (int i = 0; i < 10; i++) {
            Message msg = new Message("SimpleTopic", 
                "TagA", 
                ("Hello RocketMQ " + i).getBytes(RemotingHelper.DEFAULT_CHARSET));
            SendResult sendResult = producer.send(msg);
            System.out.printf("%s%n", sendResult);
        }
        
        producer.shutdown();
    }
}

// Consumer示例
public class SimpleConsumer {
    public static void main(String[] args) throws Exception {
        DefaultMQPushConsumer consumer = new DefaultMQPushConsumer("simple_consumer_group");
        consumer.setNamesrvAddr("namesrv:9876");
        consumer.subscribe("SimpleTopic", "*");
        
        consumer.registerMessageListener(new MessageListenerConcurrently() {
            @Override
            public ConsumeConcurrentlyStatus consumeMessage(
                    List<MessageExt> msgs, ConsumeConcurrentlyContext context) {
                for (MessageExt msg : msgs) {
                    try {
                        String body = new String(msg.getBody(), RemotingHelper.DEFAULT_CHARSET);
                        System.out.println("Received: " + body);
                    } catch (Exception e) {
                        e.printStackTrace();
                        return ConsumeConcurrentlyStatus.RECONSUME_LATER;
                    }
                }
                return ConsumeConcurrentlyStatus.CONSUME_SUCCESS;
            }
        });
        
        consumer.start();
        System.out.println("Consumer Started.");
    }
}
```

### 2. 消息过滤
```java
// SQL92过滤示例
public class FilterProducer {
    public static void main(String[] args) throws Exception {
        DefaultMQProducer producer = new DefaultMQProducer("filter_producer_group");
        producer.setNamesrvAddr("namesrv:9876");
        producer.start();
        
        for (int i = 0; i < 10; i++) {
            Message msg = new Message("FilterTopic", 
                "TagA", 
                ("Order Message " + i).getBytes(RemotingHelper.DEFAULT_CHARSET));
            
            // 设置过滤属性
            msg.putUserProperty("orderId", String.valueOf(i));
            msg.putUserProperty("amount", String.valueOf(i * 100));
            
            producer.send(msg);
        }
        
        producer.shutdown();
    }
}

// 消费者过滤
consumer.subscribe("FilterTopic", MessageSelector.bySql("orderId > 5 AND amount >= 300"));
```

### 3. 事务消息
```java
public class TransactionProducer {
    public static void main(String[] args) throws MQClientException {
        TransactionMQProducer producer = new TransactionMQProducer("transaction_producer_group");
        producer.setNamesrvAddr("namesrv:9876");
        
        // 设置事务监听器
        producer.setTransactionListener(new TransactionListener() {
            @Override
            public LocalTransactionState executeLocalTransaction(Message msg, Object arg) {
                // 执行本地事务
                String orderId = (String) arg;
                System.out.println("Executing local transaction for order: " + orderId);
                
                // 模拟业务处理
                try {
                    // 这里执行数据库操作
                    Thread.sleep(1000);
                    return LocalTransactionState.COMMIT_MESSAGE;
                } catch (Exception e) {
                    return LocalTransactionState.ROLLBACK_MESSAGE;
                }
            }
            
            @Override
            public LocalTransactionState checkLocalTransaction(MessageExt msg) {
                // 事务状态回查
                String orderId = msg.getUserProperty("orderId");
                System.out.println("Checking transaction status for order: " + orderId);
                return LocalTransactionState.COMMIT_MESSAGE;
            }
        });
        
        producer.start();
        
        // 发送事务消息
        Message msg = new Message("TransactionTopic", 
            "TransactionTag", 
            "Transaction Message".getBytes());
        msg.putUserProperty("orderId", "ORDER_001");
        
        SendResult sendResult = producer.sendMessageInTransaction(msg, "ORDER_001");
        System.out.println("Send transaction message: " + sendResult);
        
        producer.shutdown();
    }
}
```

### 4. 延迟消息
```java
public class DelayProducer {
    public static void main(String[] args) throws Exception {
        DefaultMQProducer producer = new DefaultMQProducer("delay_producer_group");
        producer.setNamesrvAddr("namesrv:9876");
        producer.start();
        
        Message msg = new Message("DelayTopic", 
            "DelayTag", 
            "Delayed Message Content".getBytes());
        
        // 设置延迟等级 (1-18级，对应不同延迟时间)
        // 1s 5s 10s 30s 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 20m 30m 1h 2h
        msg.setDelayTimeLevel(3); // 延迟10秒
        
        SendResult result = producer.send(msg);
        System.out.println("Send delay message: " + result);
        
        producer.shutdown();
    }
}
```

## 📊 使用示例

### Spring Boot集成
```java
@SpringBootApplication
public class RocketMQApplication {
    public static void main(String[] args) {
        SpringApplication.run(RocketMQApplication.class, args);
    }
}

@Component
@RocketMQMessageListener(topic = "spring-topic", consumerGroup = "spring-consumer-group")
public class SpringConsumer implements RocketMQListener<String> {
    @Override
    public void onMessage(String message) {
        System.out.println("Received message: " + message);
    }
}

@Service
public class SpringProducer {
    @Autowired
    private RocketMQTemplate rocketMQTemplate;
    
    public void sendMessage(String message) {
        rocketMQTemplate.convertAndSend("spring-topic", message);
    }
    
    public void sendAsyncMessage(String message) {
        rocketMQTemplate.asyncSend("spring-topic", message, new SendCallback() {
            @Override
            public void onSuccess(SendResult sendResult) {
                System.out.println("Async send success: " + sendResult);
            }
            
            @Override
            public void onException(Throwable throwable) {
                System.err.println("Async send failed: " + throwable.getMessage());
            }
        });
    }
}
```

## ⚙️ 集群配置

### docker-compose.yml
```yaml
version: '3.8'
services:
  namesrv:
    image: apache/rocketmq:5.0.0
    container_name: rmqnamesrv
    ports:
      - "9876:9876"
    environment:
      JAVA_OPT_EXT: "-server -Xms512m -Xmx512m"
    command: ["sh", "mqnamesrv"]

  broker:
    image: apache/rocketmq:5.0.0
    container_name: rmqbroker
    ports:
      - "10911:10911"
      - "10909:10909"
    environment:
      NAMESRV_ADDR: "namesrv:9876"
      JAVA_OPT_EXT: "-server -Xms1g -Xmx1g"
    volumes:
      - ./broker.conf:/home/rocketmq/rocketmq-5.0.0/conf/broker.conf
    command: ["sh", "mqbroker", "-c", "/home/rocketmq/rocketmq-5.0.0/conf/broker.conf"]
    depends_on:
      - namesrv

  console:
    image: apacherocketmq/rocketmq-console:2.0.0
    container_name: rocketmq-console
    ports:
      - "8080:8080"
    environment:
      JAVA_OPTS: "-Drocketmq.namesrv.addr=namesrv:9876"
    depends_on:
      - namesrv
```

### broker.conf配置
```properties
brokerClusterName = DefaultCluster
brokerName = broker-a
brokerId = 0
deleteWhen = 04
fileReservedTime = 48
brokerRole = ASYNC_MASTER
flushDiskType = ASYNC_FLUSH
autoCreateTopicEnable=true
autoCreateSubscriptionGroup=true
```

## 🔍 监控和管理

### 管理命令
```bash
# 查看集群状态
docker-compose exec namesrv mqadmin clusterList -n namesrv:9876

# 查看Topic信息
docker-compose exec namesrv mqadmin topicList -n namesrv:9876

# 查看Consumer Group状态
docker-compose exec namesrv mqadmin consumerProgress -n namesrv:9876 -g consumer_group_name

# 发送测试消息
docker-compose exec namesrv mqadmin sendMessage -n namesrv:9876 -t TestTopic -p "Hello World"

# 重置Consumer Offset
docker-compose exec namesrv mqadmin resetOffsetByTime -n namesrv:9876 -g consumer_group_name -t topic_name -s "2023-01-01 00:00:00:000"
```

## 🧪 性能测试

### 基准测试脚本
```bash
#!/bin/bash
# rocketmq-benchmark.sh

echo "Starting RocketMQ Performance Test..."

# 启动生产者测试
echo "Testing message production..."
docker-compose exec producer java -jar benchmark-producer.jar \
  --topic BenchmarkTopic \
  --message-size 1024 \
  --message-count 10000 \
  --thread-count 10

# 启动消费者测试
echo "Testing message consumption..."
docker-compose exec consumer java -jar benchmark-consumer.jar \
  --topic BenchmarkTopic \
  --group BenchmarkGroup \
  --thread-count 5

# 查看测试结果
echo "Test Results:"
docker-compose exec namesrv mqadmin statsAll -n namesrv:9876
```

## 📈 性能优化

### 生产者优化
```java
// 批量发送
List<Message> messages = new ArrayList<>();
for (int i = 0; i < 32; i++) {
    messages.add(new Message("BatchTopic", "Tag", ("Msg" + i).getBytes()));
}
producer.send(messages);

// 异步发送
producer.send(msg, new SendCallback() {
    @Override
    public void onSuccess(SendResult sendResult) {
        // 处理成功
    }
    
    @Override
    public void onException(Throwable e) {
        // 处理失败
    }
});
```

### 消费者优化
```java
// 批量消费
consumer.setConsumeMessageBatchMaxSize(32);
consumer.setPullBatchSize(32);

// 并发消费
consumer.setConsumeThreadMin(20);
consumer.setConsumeThreadMax(64);

// 顺序消费
consumer.setMessageModel(MessageModel.CLUSTERING);
consumer.setConsumeFromWhere(ConsumeFromWhere.CONSUME_FROM_FIRST_OFFSET);
```

## 🚀 生产环境部署

### 高可用配置
```yaml
# 三主三从集群配置
version: '3.8'
services:
  namesrv1:
    # Namesrv节点1配置
    
  namesrv2:
    # Namesrv节点2配置
    
  broker-master1:
    # Broker主节点1
    
  broker-slave1:
    # Broker从节点1
    
  broker-master2:
    # Broker主节点2
    
  broker-slave2:
    # Broker从节点2
```

## 📚 相关资源

### 官方文档
- [RocketMQ官方文档](https://rocketmq.apache.org/docs/)
- [RocketMQ最佳实践](https://rocketmq.apache.org/docs/best-practice/)

### 学习资源
- 《RocketMQ技术内幕》
- 分布式消息系统架构设计

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境
```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up

# 运行单元测试
mvn test

# 构建镜像
docker build -t rocketmq-demo .
```

## 📄 许可证

本项目采用 Apache 2.0 许可证

---
*最后更新: 2026年2月3日*