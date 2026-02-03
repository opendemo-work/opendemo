# Kafka生产者消费者Go示例

## 简介
本项目提供一个完整的、可执行的Go语言示例，演示如何使用Sarama库与Apache Kafka进行交互，包括消息的生产与消费。适用于学习分布式系统中的异步通信机制。

## 学习目标
- 理解Kafka的基本架构（Producer/Consumer/Broker/Topic）
- 掌握使用Go语言编写Kafka生产者和消费者
- 学会配置Sarama客户端并处理常见错误
- 实践Go中并发模型在消息处理中的应用

## 环境要求
- Go 1.19 或更高版本
- Apache Kafka 2.8+（本地或远程）
- Docker（可选，用于快速启动Kafka环境）

## 安装依赖步骤

1. 克隆本项目：
```bash
git clone https://github.com/example/kafka-go-demo.git
cd kafka-go-demo
```

2. 下载依赖库：
```bash
go mod tidy
```

## 文件说明
- `producer.go`：Kafka消息生产者，发送模拟日志消息到指定主题
- `consumer.go`：Kafka消息消费者，订阅主题并打印接收到的消息
- `go.mod`：Go模块依赖声明文件

## 逐步实操指南

### 第一步：启动Kafka环境（使用Docker示例）
```bash
docker-compose -f docker-compose-kafka.yml up -d
```
> 如果没有docker-compose-kafka.yml，可参考官方Kafka镜像文档启动单节点集群。

### 第二步：运行消费者（先启动）
```bash
go run consumer.go
```
预期输出：
```
✅ 正在连接Kafka...
✅ 成功连接！等待消息...
```

### 第三步：运行生产者
打开另一个终端窗口，执行：
```bash
go run producer.go
```
预期输出：
```
✅ 消息已发送：Hello Kafka! [序号: 1]
✅ 消息已发送：Hello Kafka! [序号: 2]
...（共10条）
```

### 第四步：查看消费者输出
消费者应显示：
```
📩 收到消息: Hello Kafka! [序号: 1] (来自分区: 0, 偏移量: 0)
📩 收到消息: Hello Kafka! [序号: 2] (来自分区: 0, 偏移量: 1)
```

## 代码解析

### `producer.go` 关键点
- 使用`sarama.NewSyncProducer`创建同步生产者，确保每条消息发送成功
- 设置`config.Producer.Return.Successes = true`以获取确认
- 使用循环发送10条测试消息

### `consumer.go` 关键点
- 使用`sarama.NewConsumerGroup`实现消费者组，支持负载均衡和容错
- 实现`setup`, `cleanup`, `ConsumeClaim`方法满足`sarama.ConsumerGroupHandler`接口
- 使用Goroutine并发处理多个分区的消息

## 预期输出示例
**生产者输出：**
```
✅ 消息已发送：Hello Kafka! [序号: 5]
```

**消费者输出：**
```
📩 收到消息: Hello Kafka! [序号: 5] (来自分区: 0, 偏移量: 4)
```

## 常见问题解答

**Q: 连接被拒绝？**
A: 确保Kafka服务正在运行且`localhost:9092`可访问。检查防火墙设置。

**Q: 消费者收不到消息？**
A: 确保消费者组ID不同或重置偏移量（可通过修改group ID实现）

**Q: 如何处理JSON消息？**
A: 使用`json.Marshal`发送，`json.Unmarshal`接收，保持消息格式一致即可。

## 扩展学习建议
- 尝试添加TLS/SCRAM认证连接安全Kafka集群
- 实现Exactly-Once语义（通过事务生产者）
- 集成Prometheus监控指标
- 使用`kafka-go`替代Sarama，比较API设计差异
- 构建Web API触发消息发送