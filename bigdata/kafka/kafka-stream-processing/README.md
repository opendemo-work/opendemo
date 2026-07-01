# Kafka 流处理实战演示 - 生产者与消费者模式

> 使用 Docker Compose 启动单节点 Kafka，通过 Python 编写生产者和消费者，演示事件流的基础发布-订阅、分区消费和简单统计。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 使用 Docker Compose 在本地启动 Zookeeper + Kafka
- ✅ 使用 Python 编写 Kafka 生产者，发送 JSON 事件到指定 topic
- ✅ 使用 Python 编写 Kafka 消费者，按消费者组消费并统计事件类型
- ✅ 理解 topic、partition、offset、consumer group 等核心概念
- ✅ 为 Kafka 应用编写基础单元测试

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kafka 发布-订阅架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐                                               │
│   │  Producer   │──┐                                            │
│   │ (producer.py)│  │                                            │
│   └─────────────┘  │                                            │
│                    │   send("user-events")                       │
│                    ▼                                            │
│   ┌─────────────────────────────────────┐                       │
│   │           Kafka Broker              │                       │
│   │  ┌─────────────────────────────┐   │                       │
│   │  │  Topic: user-events         │   │                       │
│   │  │  Partition 0                │   │                       │
│   │  │  ┌───┬───┬───┬───┬───┐     │   │                       │
│   │  │  │ 0 │ 1 │ 2 │ 3 │...│     │   │                       │
│   │  │  └───┴───┴───┴───┴───┘     │   │                       │
│   │  └─────────────────────────────┘   │                       │
│   └─────────────────────────────────────┘                       │
│                    │                                            │
│                    │ pull                                        │
│        ┌───────────┼───────────┐                                │
│        ▼           ▼           ▼                                │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐                        │
│   │Consumer │  │Consumer │  │Consumer │                        │
│   │  (A)    │  │  (B)    │  │  (C)    │                        │
│   └─────────┘  └─────────┘  └─────────┘                        │
│        │            │            │                              │
│        └────────────┴────────────┘                              │
│              Consumer Group                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 Kafka 容器 |
| Docker Compose | >= 1.29 | 编排 Zookeeper + Kafka |
| Python | >= 3.9 | 运行生产者和消费者 |

### 安装与运行

```bash
# 1. 进入案例目录
cd bigdata/kafka/kafka-stream-processing

# 2. 安装 Python 依赖
pip install -r requirements.txt

# 3. 启动 Kafka 环境
./scripts/start_kafka.sh

# 4. 一键运行演示（启动消费者 + 生产者）
./scripts/run_demo.sh

# 5. 停止环境
./scripts/stop_kafka.sh
```

### 分别运行生产者和消费者

```bash
# 终端 1：启动消费者
python code/consumer.py

# 终端 2：运行生产者
python code/producer.py
```

---

## 📖 核心概念

### 1. Topic

Topic 是 Kafka 中消息的分类名。生产者向 topic 发送消息，消费者从 topic 订阅消息。本案例使用 `user-events` topic 存储用户行为事件。

### 2. Partition

Partition 是 topic 的物理分片，允许水平扩展和并行消费。单节点环境下通常只有 1 个 partition。

### 3. Offset

Offset 是消息在 partition 中的唯一序号。消费者通过 offset 追踪已消费的位置。

### 4. Consumer Group

Consumer Group 是一组共同消费同一个 topic 的消费者。Kafka 会确保同一条消息只被组内一个消费者处理，实现负载均衡。

### 5. Key

发送消息时可以指定 key，Kafka 根据 key 的哈希值决定消息进入哪个 partition，保证相同 key 的消息顺序。

---

## 💻 代码示例

### 示例 1：发送事件（producer.py）

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

event = {
    "user_id": "user_0001",
    "event_type": "click",
    "page": "/home",
    "timestamp": "2026-06-26T12:00:00Z",
    "value": 12.5,
}

future = producer.send("user-events", key="user_0001", value=event)
record_metadata = future.get(timeout=10)
print(f"已发送: partition={record_metadata.partition}, offset={record_metadata.offset}")
producer.close()
```

### 示例 2：消费事件（consumer.py）

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "user-events",
    group_id="event-processor",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

for message in consumer:
    print(f"收到: {message.value}")
```

---

## 🔧 配置说明

### docker-compose.yml 关键配置

| 配置项 | 说明 |
|--------|------|
| `KAFKA_ADVERTISED_LISTENERS` | 客户端连接地址，本地使用 `PLAINTEXT://localhost:9092` |
| `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR` | 单节点设置为 1 |
| `KAFKA_AUTO_CREATE_TOPICS_ENABLE` | 自动创建不存在的 topic |

### 生产者关键参数

| 参数 | 说明 |
|------|------|
| `bootstrap_servers` | Kafka broker 地址 |
| `value_serializer` | 消息值序列化函数 |
| `key_serializer` | 消息 key 序列化函数 |

### 消费者关键参数

| 参数 | 说明 |
|------|------|
| `group_id` | 消费者组 ID |
| `auto_offset_reset` | 无提交 offset 时从最早/最新开始消费 |
| `enable_auto_commit` | 是否自动提交消费位置 |

---

## 🧪 验证测试

```bash
# 运行单元测试
python -m pytest tests/test_kafka.py -v
```

### 手动验证

```bash
# 1. 启动环境
./scripts/start_kafka.sh

# 2. 创建 topic
docker exec kafka-broker kafka-topics \
  --bootstrap-server localhost:9092 \
  --create --topic user-events --partitions 1 --replication-factor 1 --if-not-exists

# 3. 查看 topic 列表
docker exec kafka-broker kafka-topics --bootstrap-server localhost:9092 --list

# 4. 运行生产者和消费者
python code/producer.py
python code/consumer.py
```

---

## 📊 运行结果

### 生产者预期输出

```
开始向 topic 'user-events' 发送消息...
✅ 已发送: partition=0, offset=0, event=click
✅ 已发送: partition=0, offset=1, event=view
...
✅ 已发送: partition=0, offset=19, event=purchase
生产者已关闭
```

### 消费者预期输出

```
开始消费 topic 'user-events'...
📩 partition=0, offset=0, key=user_0000, event_type=click
📩 partition=0, offset=1, key=user_0001, event_type=view
...

消费统计:
  click: 7
  purchase: 3
  view: 10
消费者已关闭
```

---

## 🐛 常见问题

### Q1：连接 Kafka 时报错 `NoBrokersAvailable`？

**A**：确认 Kafka 容器已启动并健康：

```bash
docker ps
docker logs kafka-broker
```

### Q2：消费者收不到消息？

**A**：检查消费者组是否已有 offset 提交。可以更换 `group_id` 或设置 `auto_offset_reset="earliest"`。

### Q3：如何清空 topic 中的数据？

**A**：

```bash
docker exec kafka-broker kafka-topics \
  --bootstrap-server localhost:9092 \
  --delete --topic user-events
```

---

## 📚 扩展学习

### 相关案例

- [Apache Kafka 官方示例](https://github.com/apache/kafka/tree/trunk/examples) - Kafka 官方 Java/Scala 示例
- [Confluent Kafka Tutorials](https://developer.confluent.io/tutorials/) - Confluent 官方 Kafka 教程

### 推荐资源

- 📖 [Apache Kafka 官方文档](https://kafka.apache.org/documentation/)
- 📖 [Kafka Python 客户端文档](https://kafka-python.readthedocs.io/)
- 🎥 [Kafka 101](https://kafka.apache.org/intro)

### 进阶主题

- [ ] Kafka Connect 数据集成
- [ ] Kafka Streams 有状态流处理
- [ ] Kafka 多分区与消费者再均衡
- [ ] Schema Registry 与 Avro/Protobuf
- [ ] Kafka 生产者幂等性与事务

---

*最后更新：2026-06-26*  
*版本：1.0.0*  
*维护者：OpenDemo Team*
