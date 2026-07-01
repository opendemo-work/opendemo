<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

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
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*


---

## 📖 深入理解

### 工作原理

RabbitMQ_AMQP_Go_Demo 的核心机制可以概括为以下几个步骤：

1. **初始化阶段**：准备运行环境，加载必要的配置和依赖。
2. **执行阶段**：按照预定的流程执行主要逻辑，处理输入并生成输出。
3. **验证阶段**：检查结果是否符合预期，记录关键指标和日志。
4. **清理阶段**：释放资源，确保环境可以重复运行。

### 关键设计决策

| 决策点 | 方案 | 理由 |
|--------|------|------|
| 部署方式 | 本地容器化 | 降低环境依赖，便于复现 |
| 配置管理 | 环境变量 + 配置文件 | 灵活且安全 |
| 可观测性 | 日志 + 指标 | 便于排查和优化 |
| 扩展性 | 模块化设计 | 方便后续添加新功能 |

### 性能考量

在实际生产环境中使用本案例时，建议关注以下性能指标：

- **响应时间**：确保核心操作在可接受范围内完成。
- **资源占用**：监控 CPU、内存、磁盘和网络使用情况。
- **吞吐量**：根据业务需求评估并发处理能力。
- **错误率**：建立告警机制，及时发现异常。

---

## 🛡️ 安全与最佳实践

### 安全建议

- 不要在生产环境中使用默认密码或密钥。
- 定期更新依赖组件到最新稳定版本。
- 对敏感配置使用密钥管理工具（如 Kubernetes Secrets、Vault）。
- 限制网络暴露面，使用防火墙或安全组控制访问。

### 最佳实践

- 在修改配置前备份现有环境。
- 使用版本控制管理所有配置文件和脚本。
- 编写自动化测试覆盖核心路径。
- 记录运行日志，便于审计和故障排查。

---

## 🧪 进阶实验

完成基础演示后，可以尝试以下进阶实验：

1. **参数调优**：修改关键配置参数，观察对结果的影响。
2. **故障注入**：故意制造错误，验证系统的容错能力。
3. **压力测试**：增加负载，评估系统瓶颈。
4. **集成测试**：将本案例与其他组件组合，构建完整链路。

---

## 📚 扩展资源

### 官方文档

- [相关技术官方文档](https://example.com)
- [OpenDemo 项目主页](https://github.com/opendemo)

### 推荐书籍

- 《相关技术权威指南》
- 《云原生架构实践》

### 社区与论坛

- Stack Overflow 相关标签
- GitHub Discussions
- 技术博客与公众号

---

## 🤝 贡献与反馈

如果你发现本案例有任何问题，或希望补充更多内容，欢迎提交 Issue 或 Pull Request。

---

*本 README 为 OpenDemo 五星案例标准模板，请根据实际案例内容持续完善。*
