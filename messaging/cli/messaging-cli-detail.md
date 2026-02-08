# Messaging CLI命令详解

本文档详细解释消息队列常用CLI命令的用途、输出示例、内容解析、注意事项以及在生产环境中执行的安全风险。

## 1. RocketMQ管理命令

### 用途
Apache RocketMQ是阿里巴巴开源的分布式消息中间件，提供高性能、高可用、高可靠的消息传递服务。其管理命令用于集群管理、Topic管理、消费者组管理等操作。

### 输出示例
```bash
# 启动NameServer
$ nohup sh mqnamesrv &
Java HotSpot(TM) 64-Bit Server VM warning: If the number of processors is expected to increase from one, then you should configure the number of parallel GC threads appropriately using -XX:ParallelGCThreads=N
The Name Server boot success. serializeType=JSON

# 启动Broker
$ nohup sh mqbroker -n localhost:9876 &
Java HotSpot(TM) 64-Bit Server VM warning: If the number of processors is expected to increase from one, then you should configure the number of parallel GC threads appropriately using -XX:ParallelGCThreads=N
The broker[broker-a, 192.168.1.100:10911] boot success. serializeType=JSON and name server is localhost:9876

# 查看集群状态
$ sh mqadmin clusterList -n localhost:9876
#Cluster Name     #Broker Name            #BID  #Addr                  #Version                #InTPS      #OutTPS       #PCWaitMillisecond #Hour #SPACE
DefaultCluster    broker-a                0     192.168.1.100:10911    V4_9_4                   0.00        0.00                    0 149745.92 0.4378

# 创建Topic
$ sh mqadmin updateTopic -n localhost:9876 -t MyTestTopic -c DefaultCluster
create topic to 192.168.1.100:10911 success.
TopicConfig [topicName=MyTestTopic, readQueueNums=4, writeQueueNums=4, perm=RW-, topicFilterType=SINGLE_TAG, topicSysFlag=0, order=false]

# 查看Topic列表
$ sh mqadmin topicList -n localhost:9876
MyTestTopic
OFFSET_MOVED_EVENT
TBW102

# 查看Topic详情
$ sh mqadmin topicStatus -n localhost:9876 -t MyTestTopic
#Topic                #Consumer Group       #Client IP          #Diff  #LastTime
MyTestTopic           MyConsumerGroup       192.168.1.100       0      2024-01-15 10:30:45

# 查看消费者组进度
$ sh mqadmin consumerProgress -n localhost:9876 -g MyConsumerGroup
#Topic                #Broker Name         #QID  #Broker Offset      #Consumer Offset    #Diff   #LastTime
MyTestTopic           broker-a             0     100                 95                  5       2024-01-15 10:30:45
MyTestTopic           broker-a             1     85                  85                  0       2024-01-15 10:30:45
MyTestTopic           broker-a             2     120                 118                 2       2024-01-15 10:30:45
MyTestTopic           broker-a             3     90                  90                  0       2024-01-15 10:30:45
```

### 内容解析
- **集群信息**: 显示集群名称、Broker名称、Broker ID、地址、版本等
- **性能指标**: InTPS(输入TPS)、OutTPS(输出TPS)、PCWaitMillisecond(等待时间)
- **Topic状态**: 显示Topic的读写队列数、权限、过滤类型等配置
- **消费进度**: 显示每个队列的Broker偏移量、消费者偏移量和差值
- **时间戳**: 显示最后消费时间

### 常用参数详解
- `-n NAMESRV_ADDR`: 指定NameServer地址
- `-t TOPIC`: 指定Topic名称
- `-c CLUSTER`: 指定集群名称
- `-g GROUP`: 指定消费者组名称
- `-b BROKER`: 指定Broker地址

### 注意事项
- NameServer和Broker需要分别启动
- Topic名称应遵循命名规范
- 生产环境应配置多个NameServer实现高可用
- 定期监控消费积压情况

### 生产安全风险
- ⚠️ 默认端口可能存在安全风险
- ⚠️ 未配置ACL可能导致未授权访问
- ⚠️ 日志文件可能包含敏感信息
- ✅ 建议启用ACL和SSL加密

---

## 2. Kafka管理命令

### 用途
Apache Kafka是LinkedIn开源的分布式流处理平台，广泛用于构建实时数据管道和流应用。其CLI工具提供Topic管理、生产消费测试、消费者组管理等功能。

### 输出示例
```bash
# 启动ZooKeeper
$ bin/zookeeper-server-start.sh config/zookeeper.properties
[2024-01-15 10:30:45,123] INFO Reading configuration from: config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
[2024-01-15 10:30:45,125] INFO Starting server (org.apache.zookeeper.server.ZooKeeperServerMain)
[2024-01-15 10:30:45,234] INFO binding to port 0.0.0.0/0.0.0.0:2181 (org.apache.zookeeper.server.NIOServerCnxnFactory)

# 启动Kafka
$ bin/kafka-server-start.sh config/server.properties
[2024-01-15 10:30:46,456] INFO KafkaConfig values: 
	advertised.listeners = PLAINTEXT://localhost:9092
	auto.create.topics.enable = true
	background.threads = 10
	broker.id = 0
	compression.type = producer
[2024-01-15 10:30:47,123] INFO [KafkaServer id=0] started (kafka.server.KafkaServer)

# 创建Topic
$ bin/kafka-topics.sh --create --topic my-test-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
Created topic my-test-topic.

# 查看Topic列表
$ bin/kafka-topics.sh --list --bootstrap-server localhost:9092
__consumer_offsets
my-test-topic

# 查看Topic详情
$ bin/kafka-topics.sh --describe --topic my-test-topic --bootstrap-server localhost:9092
Topic: my-test-topic	TopicId: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx	PartitionCount: 3	ReplicationFactor: 1	Configs: 
	Topic: my-test-topic	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
	Topic: my-test-topic	Partition: 1	Leader: 0	Replicas: 0	Isr: 0
	Topic: my-test-topic	Partition: 2	Leader: 0	Replicas: 0	Isr: 0

# 生产消息
$ bin/kafka-console-producer.sh --topic my-test-topic --bootstrap-server localhost:9092
>Hello World
>This is a test message
>Another message

# 消费消息
$ bin/kafka-console-consumer.sh --topic my-test-topic --bootstrap-server localhost:9092 --from-beginning
Hello World
This is a test message
Another message

# 查看消费者组列表
$ bin/kafka-consumer-groups.sh --list --bootstrap-server localhost:9092
console-consumer-12345
my-test-group

# 查看消费者组详情
$ bin/kafka-consumer-groups.sh --describe --group my-test-group --bootstrap-server localhost:9092
GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                  HOST            CLIENT-ID
my-test-group   my-test-topic   0          3               3               0               consumer-1-xxxxx /192.168.1.100         consumer-1
my-test-group   my-test-topic   1          2               2               0               consumer-1-xxxxx /192.168.1.100         consumer-1
my-test-group   my-test-topic   2          4               4               0               consumer-1-xxxxx /192.168.1.100         consumer-1

# 重置消费位点
$ bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-test-group --reset-offsets --to-earliest --execute --topic my-test-topic
GROUP                          TOPIC                          PARTITION  NEW-OFFSET     
my-test-group                  my-test-topic                  0          0              
my-test-group                  my-test-topic                  1          0              
my-test-group                  my-test-topic                  2          0              
```

### 内容解析
- **服务器启动**: 显示配置加载和启动过程
- **Topic信息**: 包括分区数、副本因子、Leader分布
- **ISR列表**: In-Sync Replicas(同步副本)列表
- **消费组状态**: 显示当前偏移量、日志末尾偏移量、滞后量
- **消费者信息**: 消费者ID、主机地址、客户端ID

### 常用参数详解
- `--bootstrap-server HOST:PORT`: 指定Kafka服务器地址
- `--topic TOPIC_NAME`: 指定Topic名称
- `--partitions NUM`: 指定分区数量
- `--replication-factor NUM`: 指定副本因子
- `--group GROUP_NAME`: 指定消费者组名称
- `--from-beginning`: 从最早的消息开始消费
- `--reset-offsets`: 重置消费位点

### 注意事项
- ZooKeeper和Kafka需要按顺序启动
- 生产环境应配置多个Broker实现集群
- 合理设置分区数和副本因子
- 定期清理过期的消费者组

### 生产安全风险
- ⚠️ 默认配置可能存在安全漏洞
- ⚠️ 未启用认证和授权机制
- ⚠️ 网络传输未加密
- ✅ 建议启用SASL认证和SSL加密

---

## 3. RabbitMQ管理命令

### 用途
RabbitMQ是基于Erlang开发的开源消息代理软件，实现了AMQP(高级消息队列协议)，提供可靠的消息传递、灵活的路由、集群和故障转移等功能。

### 输出示例
```bash
# 启动RabbitMQ
$ rabbitmq-server
Starting rabbitmq-server: SUCCESS
rabbitmq-server.

# 启用管理插件
$ rabbitmq-plugins enable rabbitmq_management
Enabling plugins on node rabbit@localhost:
rabbitmq_management
The following plugins have been configured:
  rabbitmq_management
  rabbitmq_management_agent
  rabbitmq_web_dispatch
Applying plugin configuration to rabbit@localhost...
The following plugins are already enabled:
  rabbitmq_management
  rabbitmq_management_agent
  rabbitmq_web_dispatch

# 查看节点状态
$ rabbitmqctl status
Status of node rabbit@localhost ...
Runtime

OS PID: 12345
OS Thread Priorities
[{cpu_sup,<0.33.0>,0},
 {inet_gethost_native,<0.34.0>,0}]

Memory
   allocated: 78901234
   reserved_unallocated: 1234567
   strategy: rss
   total: [{connection_readers,123456},
           {connection_writers,789012},
           {connection_channels,345678},
           {connection_other,901234},
           {queue_procs,567890},
           {queue_slave_procs,123456},
           {plugins,789012}]

# 查看队列列表
$ rabbitmqctl list_queues
Timeout: 60.0 seconds ...
Listing queues for vhost '/' ...
name	messages
my-test-queue	5
another-queue	0

# 查看交换机列表
$ rabbitmqctl list_exchanges
Listing exchanges for vhost '/' ...
name	type
	direct
amq.direct	direct
amq.fanout	fanout
amq.headers	headers
amq.match	headers
amq.rabbitmq.log	topic
amq.rabbitmq.trace	topic
amq.topic	topic
my-test-exchange	topic

# 添加用户
$ rabbitmqctl add_user testuser testpassword
Adding user "testuser" ...

# 设置用户权限
$ rabbitmqctl set_permissions -p / testuser ".*" ".*" ".*"
Setting permissions for user "testuser" in vhost "/" ...

# 查看队列详情
$ rabbitmqctl list_queues name messages consumers memory
Timeout: 60.0 seconds ...
Listing queues for vhost '/' ...
name	messages	consumers	memory
my-test-queue	5	1	34567
another-queue	0	0	12345

# 清空队列
$ rabbitmqctl purge_queue my-test-queue
Purging queue 'my-test-queue' in vhost '/' ...
3 messages purged.

# 查看集群状态
$ rabbitmqctl cluster_status
Cluster status of node rabbit@node1 ...
Basics

Cluster name: rabbit@node1

Disk Nodes

rabbit@node1
rabbit@node2
rabbit@node3

Running Nodes

rabbit@node1
rabbit@node2
rabbit@node3

Versions

rabbit@node1: RabbitMQ 3.12.0 on Erlang 25.3.2.6
rabbit@node2: RabbitMQ 3.12.0 on Erlang 25.3.2.6
rabbit@node3: RabbitMQ 3.12.0 on Erlang 25.3.2.6
```

### 内容解析
- **内存使用**: 显示不同类型进程的内存分配情况
- **队列统计**: 消息数量、消费者数量、内存使用
- **交换机类型**: direct、fanout、topic、headers等
- **集群信息**: 磁盘节点、运行节点、版本信息
- **权限配置**: 配置模式、写入模式、读取模式

### 常用参数详解
- `list_queues`: 列出队列信息
- `list_exchanges`: 列出交换机信息
- `list_bindings`: 列出绑定关系
- `add_user USER PASSWORD`: 添加用户
- `set_permissions`: 设置用户权限
- `purge_queue QUEUE`: 清空队列
- `cluster_status`: 查看集群状态

### 注意事项
- Erlang和RabbitMQ版本需要兼容
- 生产环境建议使用集群部署
- 定期监控队列积压情况
- 合理配置内存和磁盘水位

### 生产安全风险
- ⚠️ 默认guest用户只能本地访问
- ⚠️ 未配置TLS加密传输
- ⚠️ 管理界面可能存在未授权访问
- ✅ 建议启用TLS、配置防火墙规则

---

## 4. 消息生产消费命令

### 用途
用于测试和验证消息队列的基本功能，包括消息的发送、接收、确认等操作。

### 输出示例
```bash
# RocketMQ生产消息
$ sh tools.sh org.apache.rocketmq.example.quickstart.Producer
SendResult [sendStatus=SEND_OK, msgId=AC100A6400002A9F0000000000000001, offsetMsgId=AC100A64000000000000000000000001, messageQueue=MessageQueue [topic=TEST_TOPIC, brokerName=broker-a, queueId=0], queueOffset=0]

# RocketMQ消费消息
$ sh tools.sh org.apache.rocketmq.example.quickstart.Consumer
Consumer Started.
Receive New Messages: [MessageExt [queueId=0, storeSize=179, queueOffset=0, sysFlag=0, bornTimestamp=1705315845123, bornHost=/192.168.1.100:56789, storeTimestamp=1705315845123, storeHost=/192.168.1.100:10911, msgId=AC100A64000000000000000000000001, commitLogOffset=0, bodyCRC=1234567890, reconsumeTimes=0, preparedTransactionOffset=0, toString()=Message{topic='TEST_TOPIC', flag=0, properties={MIN_OFFSET=0, MAX_OFFSET=1, CONSUME_START_TIME=1705315845123, UNIQ_KEY=AC100A6400002A9F0000000000000001, WAIT=true}, body=[72, 101, 108, 108, 111, 32, 82, 111, 99, 107, 101, 116, 77, 81], transactionId='null'}]]

# Kafka性能测试生产者
$ bin/kafka-producer-perf-test.sh --topic perf-test --num-records 100000 --record-size 1000 --throughput -1 --producer-props bootstrap.servers=localhost:9092
100000 records sent, 89285.714286 records/sec (85.15 MB/sec), 123.45 ms avg latency, 456.78 ms max latency, 98 ms 50th, 234 ms 95th, 345 ms 99th, 456 ms 99.9th.

# Kafka性能测试消费者
$ bin/kafka-consumer-perf-test.sh --topic perf-test --messages 100000 --broker-list localhost:9092 --group perf-group
start.time, end.time, data.consumed.in.MB, MB.sec, data.consumed.in.nMsg, nMsg.sec, rebalance.time.ms, fetch.time.ms, fetch.MB.sec, fetch.nMsg.sec
2024-01-15 10:30:45:123, 2024-01-15 10:30:47:456, 95.37, 42.1567, 100000, 44285.7143, 123, 2210, 43.1567, 45248.8688

# RabbitMQ发布消息
$ rabbitmqadmin publish exchange=amq.direct routing_key=test payload="Hello RabbitMQ"
Message published

# RabbitMQ消费消息
$ rabbitmqadmin get queue=my-test-queue ackmode=ack_requeue_false
+-------------+----------+---------------+---------+---------------+------------------+-------------+
| routing_key | exchange | message_count | payload | payload_bytes | message_timestamp | redelivered |
+-------------+----------+---------------+---------+---------------+------------------+-------------+
| test        | amq.direct | 4             | Hello RabbitMQ | 13            | 1705315845        | False       |
+-------------+----------+---------------+---------+---------------+------------------+-------------+
```

### 内容解析
- **发送结果**: 包括发送状态、消息ID、队列信息等
- **消费结果**: 显示接收到的消息内容和元数据
- **性能指标**: 吞吐量、延迟、百分位数等
- **消息属性**: 路由键、交换机、消息体等

### 常用参数详解
- `--num-records`: 发送消息数量
- `--record-size`: 消息大小(字节)
- `--throughput`: 吞吐量限制(-1表示不限制)
- `--messages`: 消费消息数量
- `ackmode`: 确认模式(auto_ack、ack_requeue_true、ack_requeue_false)

### 注意事项
- 性能测试应在专用环境中进行
- 注意消息大小对性能的影响
- 合理设置批处理大小
- 监控系统资源使用情况

### 生产安全风险
- ⚠️ 测试数据可能包含敏感信息
- ⚠️ 性能测试可能影响生产环境
- ✅ 建议在隔离环境中进行测试

---

## 5. 集群管理命令

### 用途
用于管理消息队列集群，包括节点加入、状态查看、故障恢复等操作。

### 输出示例
```bash
# RocketMQ集群信息
$ sh mqadmin clusterList -n localhost:9876
#Cluster Name     #Broker Name            #BID  #Addr                  #Version                #InTPS      #OutTPS       #PCWaitMillisecond #Hour #SPACE
DefaultCluster    broker-a                0     192.168.1.100:10911    V4_9_4                   0.00        0.00                    0 149745.92 0.4378
DefaultCluster    broker-b                0     192.168.1.101:10911    V4_9_4                   0.00        0.00                    0 149745.92 0.4378
DefaultCluster    broker-c                0     192.168.1.102:10911    V4_9_4                   0.00        0.00                    0 149745.92 0.4378

# Kafka集群元数据
$ bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092
Broker 0 supports versions 0 to 12 for API key 0 (Produce)
Broker 0 supports versions 0 to 12 for API key 1 (Fetch)
Broker 0 supports versions 0 to 7 for API key 2 (ListOffsets)
# ... 更多API版本信息

# RabbitMQ集群状态
$ rabbitmqctl cluster_status
Cluster status of node rabbit@node1 ...
Basics

Cluster name: rabbit@node1

Disk Nodes

rabbit@node1
rabbit@node2
rabbit@node3

Running Nodes

rabbit@node1
rabbit@node2
rabbit@node3

Partitions

Currently there are no network partitions.

Alarms

Currently there are no alarms on any nodes.

Network Partitions

Currently there are no network partitions.

Listeners

Interface: [::], port: 25672, protocol: clustering, purpose: inter-node and CLI tool communication
Interface: [::], port: 5672, protocol: amqp, purpose: AMQP 0-9-1 and AMQP 1.0
Interface: [::], port: 15672, protocol: http, purpose: HTTP API
```

### 内容解析
- **节点信息**: 显示集群中所有节点的状态
- **API版本**: Kafka支持的API版本信息
- **分区状态**: RabbitMQ集群分区情况
- **监听端口**: 各种协议的监听端口信息

### 常用参数详解
- `clusterList`: 查看RocketMQ集群列表
- `broker-api-versions`: 查看Kafka Broker支持的API版本
- `cluster_status`: 查看RabbitMQ集群状态
- `join_cluster`: 加入RabbitMQ集群

### 注意事项
- 集群部署需要规划网络拓扑
- 定期检查集群健康状态
- 配置适当的故障恢复策略
- 监控节点间的网络连接

### 生产安全风险
- ⚠️ 集群配置错误可能导致数据丢失
- ⚠️ 网络分区可能影响服务可用性
- ✅ 建议配置监控告警和自动故障恢复

---

**总结**: 以上是消息队列常用的CLI工具详解。在生产环境中使用这些工具时，务必注意网络安全、访问控制和监控告警，确保消息系统的稳定性和可靠性。