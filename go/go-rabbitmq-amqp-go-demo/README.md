# RabbitMQ AMQP Go Demo

## 简介
本项目是一个基于Go语言的RabbitMQ AMQP协议实战演示程序，展示了如何使用Go构建高效的消息生产者与消费者。通过本Demo，开发者可以快速掌握在分布式系统中使用消息队列进行解耦和异步处理的核心技术。

## 学习目标
- 掌握Go中使用amqp库连接RabbitMQ的基本方法
- 理解消息生产者与消费者的实现模式
- 学会使用工作队列（Work Queue）分发任务
- 熟悉AMQP核心概念：Exchange、Queue、Binding、Routing Key

## 环境要求
- Go 1.19 或更高版本
- RabbitMQ 3.8+（可通过Docker运行）
- 支持curl或浏览器用于验证服务状态

## 安装依赖的详细步骤

1. 安装Go（如未安装）
   ```bash
   # macOS
   brew install go

   # Ubuntu
   sudo apt-get update && sudo apt-get install golang

   # 验证安装
   go version
   ```

2. 启动RabbitMQ服务（推荐使用Docker）
   ```bash
   docker run -d --hostname my-rabbit --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

   访问 http://localhost:15672，登录账号密码默认为 `guest/guest`

3. 初始化Go模块并安装依赖
   ```bash
   go mod init rabbitmq-demo
   go get github.com/streadway/amqp
   ```

## 文件说明
- `producer.go`：消息生产者，向RabbitMQ发送消息
- `consumer.go`：消息消费者，从队列接收并处理消息
- `work_consumer.go`：工作队列消费者，模拟多个工作者竞争消费任务

## 逐步实操指南

### 第一步：启动消费者
```bash
go run consumer.go
```
**预期输出**：
```
[*] Waiting for messages. To exit press CTRL+C
```

### 第二步：发送消息
打开另一个终端，运行：
```bash
go run producer.go
```
**预期输出**：
```
[+] Sent 'Hello World!'
```

回到消费者终端，应看到：
```
[+] Received Hello World!
```

### 第三步：测试工作队列
启动两个工作消费者：
```bash
go run work_consumer.go
# 在另一个终端重复执行一次
```
然后多次运行生产者：
```bash
go run producer.go
```
观察两个消费者交替处理消息，体现负载均衡。

## 代码解析

### producer.go
- 使用`amqp.Dial`建立与RabbitMQ的连接
- 创建channel用于通信
- 声明一个持久化队列（确保重启后消息不丢失）
- 使用`channel.Publish`发送消息到默认交换机

### consumer.go
- 使用`channel.Consume`订阅队列
- 处理接收到的消息，并在处理完成后手动发送ACK确认
- 使用goroutine并发处理多条消息

### work_consumer.go
- 设置`Qos`为1，确保一次只处理一条消息（公平分发）
- 模拟耗时操作（如sleep），体现工作队列的负载分配能力

## 预期输出示例
### 生产者
```
[+] Sent 'Hello World!'
```

### 消费者
```
[*] Waiting for messages. To exit press CTRL+C
[+] Received Hello World!
```

## 常见问题解答

**Q: 连接被拒绝？**
A: 确保RabbitMQ正在运行且端口5672已暴露。使用`docker ps`检查容器状态。

**Q: 消息未被消费？**
A: 检查队列名称是否一致，确保生产者和消费者使用相同队列名。

**Q: 如何启用SSL连接？**
A: 修改连接字符串为`amqps://user:pass@host:port/`，并配置证书。

## 扩展学习建议
- 实现Fanout/Topic/Direct Exchange路由模式
- 添加消息持久化与重试机制
- 结合context实现优雅关闭
- 使用Sarama或其它库对比Kafka与RabbitMQ差异