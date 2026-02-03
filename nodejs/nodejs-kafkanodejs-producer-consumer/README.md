# Kafka生产者消费者Node.js演示

本项目提供了一个基于Node.js的Kafka生产者和消费者的完整示例，帮助开发者理解如何使用Kafka进行异步消息通信。

## 学习目标

- 理解Kafka的基本概念：主题（Topic）、生产者（Producer）、消费者（Consumer）
- 掌握使用 `kafkajs` 库在Node.js中实现消息的发送与接收
- 实践跨平台的消息队列应用开发流程

## 环境要求

- Node.js 版本：v14.x 或更高（推荐 v16+）
- Kafka 服务：本地或远程运行的 Kafka 实例（默认连接 localhost:9092）
- 操作系统：Windows、Linux、macOS 均支持

> 提示：可使用 Docker 快速启动 Kafka 环境（见扩展学习建议）

## 安装依赖的详细步骤

1. 克隆项目或创建项目目录
2. 打开终端并进入项目根目录
3. 运行以下命令安装依赖：

```bash
npm init -y
npm install kafkajs
```

## 文件说明

- `producer.js`：Kafka 生产者，向指定主题发送消息
- `consumer.js`：Kafka 消费者，订阅主题并处理接收到的消息
- `package.json`：依赖声明文件

## 逐步实操指南

### 第一步：启动 Kafka 服务

确保你的 Kafka 服务正在运行。例如使用 Docker 启动单节点 Kafka：

```bash
docker run -d --name kafka-stack \n  -p 9092:9092 \n  -e KAFKA_BROKER_ID=1 \n  -e KAFKA_ZOOKEEPER_CONNECT=localhost:2181 \n  -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \n  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \n  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \n  confluentinc/cp-kafka:latest
```

等待几秒让服务启动。

### 第二步：运行消费者

打开终端窗口，运行：

```bash
node consumer.js
```

预期输出：
```
✅ 消费者已连接
✅ 消费者已订阅主题 hello-kafka
🚀 等待接收消息...
```

### 第三步：运行生产者

另开一个终端窗口，运行：

```bash
node producer.js
```

预期输出：
```
✅ 生产者已连接
📤 消息已发送：Hello Kafka! (时间戳)
✅ 消息发送成功
✨ 断开生产者连接
```

回到消费者终端，应看到：
```
📨 收到消息：Hello Kafka! (时间戳)
内容: { key: null, value: 'Hello Kafka! (时间戳)' }
```

## 代码解析

### producer.js 关键逻辑

- 创建 Kafka 实例并连接生产者
- 使用 `producer.send()` 发送消息到 `hello-kafka` 主题
- 消息包含时间戳以区分每次运行

### consumer.js 关键逻辑

- 创建消费者并订阅 `hello-kafka` 主题
- 使用 `eachMessage` 处理每一条消息
- 输出消息内容到控制台

## 预期输出示例

**Producer 输出**：
```
✅ 生产者已连接
📤 消息已发送：Hello Kafka! (2025-04-05T10:00:00Z)
✅ 消息发送成功
✨ 断开生产者连接
```

**Consumer 输出**：
```
✅ 消费者已连接
✅ 消费者已订阅主题 hello-kafka
🚀 等待接收消息...
📨 收到消息：Hello Kafka! (2025-04-05T10:00:00Z)
内容: { key: null, value: 'Hello Kafka! (2025-04-05T10:00:00Z)' }
```

## 常见问题解答

**Q1：连接失败？**
A：检查 Kafka 是否运行，并确认 broker 地址为 `localhost:9092`。防火墙或网络配置可能阻止连接。

**Q2：消费者收不到消息？**
A：确保消费者先运行或使用 `fromBeginning: true` 选项读取历史消息。

**Q3：报错 `Cannot find module 'kafkajs'`？**
A：运行 `npm install kafkajs` 安装依赖。

## 扩展学习建议

- 使用 Docker Compose 启动 ZooKeeper + Kafka 环境
- 实现多个消费者组成消费者组实现负载均衡
- 添加错误重试机制和日志记录
- 使用 Schema Registry 管理消息格式（如 Avro）

> 参考 `docker-compose.yml` 示例：
>
> ```yaml
> version: '3'
> services:
>   zookeeper:
>     image: confluentinc/cp-zookeeper:latest
>     environment:
>       ZOOKEEPER_CLIENT_PORT: 2181
>   kafka:
>     image: confluentinc/cp-kafka:latest
>     depends_on:
>       - zookeeper
>     ports:
>       - "9092:9092"
>     environment:
>       KAFKA_BROKER_ID: 1
>       KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
>       KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
>       KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
>       KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
> ```