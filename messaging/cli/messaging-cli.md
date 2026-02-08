# 📨 Messaging 命令行速查表 (messaging-cli.md)

> 消息队列和事件驱动架构必备的命令行参考手册，涵盖RocketMQ、Kafka、RabbitMQ等主流消息中间件，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [RocketMQ管理](#rocketmq管理)
- [Kafka管理](#kafka管理)
- [RabbitMQ管理](#rabbitmq管理)
- [消息生产消费](#消息生产消费)
- [集群管理](#集群管理)
- [监控告警](#监控告警)
- [性能调优](#性能调优)
- [故障排查](#故障排查)
- [最佳实践](#最佳实践)

---

## RocketMQ管理

### 基础管理命令
```bash
# 启动NameServer
nohup sh mqnamesrv &

# 启动Broker
nohup sh mqbroker -n localhost:9876 &

# 关闭服务
sh mqshutdown broker
sh mqshutdown namesrv

# 查看集群状态
sh mqadmin clusterList -n localhost:9876
```

### Topic管理
```bash
# 创建Topic
sh mqadmin updateTopic -n localhost:9876 -t MyTopic -c DefaultCluster

# 查看Topic列表
sh mqadmin topicList -n localhost:9876

# 查看Topic详情
sh mqadmin topicStatus -n localhost:9876 -t MyTopic

# 删除Topic
sh mqadmin deleteTopic -n localhost:9876 -t MyTopic -c DefaultCluster
```

### 消费者组管理
```bash
# 查看消费者组
sh mqadmin consumerProgress -n localhost:9876 -g MyConsumerGroup

# 重置消费位点
sh mqadmin resetOffsetByTime -n localhost:9876 -g MyConsumerGroup -t MyTopic -s "2024-01-01 00:00:00"

# 删除消费者组
sh mqadmin deleteSubGroup -n localhost:9876 -g MyConsumerGroup -c DefaultCluster
```

---

## Kafka管理

### Kafka基础操作
```bash
# 启动ZooKeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# 启动Kafka
bin/kafka-server-start.sh config/server.properties

# 创建Topic
bin/kafka-topics.sh --create --topic my-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

# 查看Topic列表
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# 查看Topic详情
bin/kafka-topics.sh --describe --topic my-topic --bootstrap-server localhost:9092
```

### 生产消费测试
```bash
# 生产消息
bin/kafka-console-producer.sh --topic my-topic --bootstrap-server localhost:9092

# 消费消息
bin/kafka-console-consumer.sh --topic my-topic --bootstrap-server localhost:9092 --from-beginning

# 消费特定消费者组
bin/kafka-console-consumer.sh --topic my-topic --bootstrap-server localhost:9092 --group my-group
```

### 消费者组管理
```bash
# 查看消费者组列表
bin/kafka-consumer-groups.sh --list --bootstrap-server localhost:9092

# 查看消费者组详情
bin/kafka-consumer-groups.sh --describe --group my-group --bootstrap-server localhost:9092

# 重置消费位点
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --reset-offsets --to-earliest --execute --topic my-topic
```

---

## RabbitMQ管理

### 基础管理
```bash
# 启动RabbitMQ
rabbitmq-server

# 启用管理插件
rabbitmq-plugins enable rabbitmq_management

# 查看节点状态
rabbitmqctl status

# 查看队列列表
rabbitmqctl list_queues

# 查看交换机列表
rabbitmqctl list_exchanges
```

### 用户和权限管理
```bash
# 添加用户
rabbitmqctl add_user myuser mypassword

# 设置用户角色
rabbitmqctl set_user_tags myuser administrator

# 设置权限
rabbitmqctl set_permissions -p / myuser ".*" ".*" ".*"

# 删除用户
rabbitmqctl delete_user myuser
```

### 队列管理
```bash
# 声明队列
rabbitmqadmin declare queue name=my-queue durable=true

# 查看队列详情
rabbitmqctl list_queues name messages consumers

# 清空队列
rabbitmqctl purge_queue my-queue

# 删除队列
rabbitmqadmin delete queue name=my-queue
```

---

## 消息生产消费

### RocketMQ客户端
```bash
# 生产消息
sh tools.sh org.apache.rocketmq.example.quickstart.Producer

# 消费消息
sh tools.sh org.apache.rocketmq.example.quickstart.Consumer

# 顺序消息生产
sh tools.sh org.apache.rocketmq.example.ordermessage.Producer

# 顺序消息消费
sh tools.sh org.apache.rocketmq.example.ordermessage.Consumer
```

### Kafka客户端
```bash
# 高级生产者
bin/kafka-verifiable-producer.sh --topic test-topic --max-messages 100 --bootstrap-server localhost:9092

# 高级消费者
bin/kafka-verifiable-consumer.sh --topic test-topic --bootstrap-server localhost:9092 --group-id test-group

# 性能测试
bin/kafka-producer-perf-test.sh --topic perf-test --num-records 100000 --record-size 1000 --throughput -1 --producer-props bootstrap.servers=localhost:9092

bin/kafka-consumer-perf-test.sh --topic perf-test --messages 100000 --broker-list localhost:9092 --group perf-group
```

### RabbitMQ客户端
```bash
# 发布消息
rabbitmqadmin publish exchange=amq.direct routing_key=test payload="Hello World"

# 消费消息
rabbitmqadmin get queue=my-queue ackmode=ack_requeue_false

# 批量操作
for i in {1..100}; do
    rabbitmqadmin publish exchange=amq.direct routing_key=test payload="Message $i"
done
```

---

## 集群管理

### RocketMQ集群
```bash
# 查看集群信息
sh mqadmin clusterList -n localhost:9876

# 添加Broker到集群
# 修改broker.conf配置文件
brokerClusterName = DefaultCluster
brokerName = broker-a
brokerId = 0
namesrvAddr = localhost:9876

# 同步双写配置
flushDiskType = SYNC_FLUSH
sendMessageWithVIPChannel = false
```

### Kafka集群
```bash
# 集群配置 server.properties
broker.id=0
listeners=PLAINTEXT://:9092
log.dirs=/tmp/kafka-logs
zookeeper.connect=localhost:2181
num.partitions=3
default.replication.factor=2

# 查看集群元数据
bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092

# Rebalance操作
bin/kafka-preferred-replica-election.sh --bootstrap-server localhost:9092
```

### RabbitMQ集群
```bash
# 集群配置
# 节点1
rabbitmq-server -detached

# 节点2
rabbitmq-server -detached
rabbitmqctl stop_app
rabbitmqctl join_cluster rabbit@node1
rabbitmqctl start_app

# 查看集群状态
rabbitmqctl cluster_status
```

---

## 监控告警

### RocketMQ监控
```bash
# 启用监控
# 修改broker.conf
autoCreateTopicEnable=true
autoCreateSubscriptionGroup=true

# 监控指标收集
curl "http://localhost:9876/api/stat.do?msgType=cluster"
curl "http://localhost:9876/api/stat.do?msgType=broker&brokerAddr=localhost:10911"

# 自定义监控脚本
#!/bin/bash
CLUSTER_INFO=$(curl -s "http://localhost:9876/api/stat.do?msgType=cluster")
echo $CLUSTER_INFO | jq '.data.brokerStats'
```

### Kafka监控
```bash
# JMX监控配置
export JMX_PORT=9999
bin/kafka-server-start.sh config/server.properties

# 监控脚本
#!/bin/bash
TOPIC_NAME="my-topic"
BOOTSTRAP_SERVERS="localhost:9092"

# 获取lag信息
bin/kafka-consumer-groups.sh --bootstrap-server $BOOTSTRAP_SERVERS --describe --group my-group | grep $TOPIC_NAME

# 监控生产速率
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list $BOOTSTRAP_SERVERS --topic $TOPIC_NAME --time -1
```

### RabbitMQ监控
```bash
# 启用监控插件
rabbitmq-plugins enable rabbitmq_prometheus

# 监控端点
curl http://localhost:15692/metrics

# 自定义监控
#!/bin/bash
QUEUE_NAME="my-queue"
RABBITMQ_ADMIN="http://guest:guest@localhost:15672"

# 获取队列消息数
curl -s "$RABBITMQ_ADMIN/api/queues/%2F/$QUEUE_NAME" | jq '.messages'

# 获取消费者数量
curl -s "$RABBITMQ_ADMIN/api/queues/%2F/$QUEUE_NAME" | jq '.consumers'
```

---

## 性能调优

### RocketMQ调优
```bash
# Broker配置优化 broker.conf
# 内存配置
-Xms4g -Xmx4g -Xmn2g

# 存储配置
storePathRootDir=/data/rocketmq/store
storePathCommitLog=/data/rocketmq/commitlog

# 性能参数
sendMessageThreadPoolNums=16
pullMessageThreadPoolNums=64
queryMessageThreadPoolNums=8
```

### Kafka调优
```bash
# 服务端调优 server.properties
# 网络配置
num.network.threads=8
num.io.threads=16

# 日志配置
log.flush.interval.messages=10000
log.flush.interval.ms=1000

# 副本配置
replica.fetch.max.bytes=1048576
replica.lag.time.max.ms=30000

# 客户端调优 producer.properties
batch.size=16384
linger.ms=5
compression.type=lz4
```

### RabbitMQ调优
```bash
# 内存水位配置
vm_memory_high_watermark.relative = 0.6
vm_memory_high_watermark_paging_ratio = 0.8

# 磁盘空间配置
disk_free_limit.absolute = 1GB

# 连接配置
tcp_listen_options.backlog = 128
tcp_listen_options.nodelay = true
```

---

## 故障排查

### 常见问题诊断
```bash
# RocketMQ问题排查
# 查看NameServer日志
tail -f ~/logs/rocketmqlogs/namesrv.log

# 查看Broker日志
tail -f ~/logs/rocketmqlogs/broker.log

# 检查端口占用
netstat -tuln | grep -E "(9876|10911)"

# Kafka问题排查
# 查看ZooKeeper状态
echo stat | nc localhost 2181

# 查看Kafka日志
tail -f logs/server.log

# 检查分区leader
bin/kafka-topics.sh --describe --topic my-topic --bootstrap-server localhost:9092

# RabbitMQ问题排查
# 查看错误日志
tail -f /var/log/rabbitmq/rabbit@hostname.log

# 检查Erlang进程
rabbitmqctl eval 'erlang:processes().'

# 查看内存使用
rabbitmqctl eval 'rabbit_diagnostics:maybe_stuck().'
```

### 性能瓶颈分析
```bash
# 系统资源监控
iostat -x 1
vmstat 1
top -p $(pgrep -f "rocketmq|kafka|rabbitmq")

# 网络监控
iftop -i eth0
ss -tuln | grep -E "(9876|9092|5672)"

# 磁盘IO分析
iotop
iostat -x 1 10
```

---

## 最佳实践

### 高可用配置
```bash
# RocketMQ高可用
# NameServer集群
namesrvAddr=node1:9876;node2:9876;node3:9876

# Broker主从配置
brokerRole=SYNC_MASTER
flushDiskType=SYNC_FLUSH

# Kafka高可用
# 多副本配置
default.replication.factor=3
min.insync.replicas=2

# 分区策略
num.partitions=6

# RabbitMQ高可用
# 镜像队列配置
rabbitmqctl set_policy ha-all "^ha\." '{"ha-mode":"all"}'
```

### 安全配置
```bash
# RocketMQ安全
# ACL配置
aclEnable=true
globalWhiteRemoteAddresses=192.168.1.*

# Kafka安全
# SASL配置
sasl.enabled.mechanisms=PLAIN
security.inter.broker.protocol=SASL_PLAINTEXT

# RabbitMQ安全
# 用户权限控制
rabbitmqctl add_user admin admin123
rabbitmqctl set_user_tags admin administrator
rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
```

### 运维脚本
```bash
#!/bin/bash
# messaging_monitor.sh

# RocketMQ监控
check_rocketmq() {
    curl -s "http://localhost:9876/api/stat.do?msgType=cluster" | jq '.data.brokerStats' > /dev/null
    if [ $? -eq 0 ]; then
        echo "RocketMQ OK"
    else
        echo "RocketMQ DOWN"
    fi
}

# Kafka监控
check_kafka() {
    bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Kafka OK"
    else
        echo "Kafka DOWN"
    fi
}

# RabbitMQ监控
check_rabbitmq() {
    curl -s "http://localhost:15672/api/overview" > /dev/null
    if [ $? -eq 0 ]; then
        echo "RabbitMQ OK"
    else
        echo "RabbitMQ DOWN"
    fi
}

# 执行检查
check_rocketmq
check_kafka
check_rabbitmq
```

---