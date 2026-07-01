# RocketMQ 延迟消息演示

> 在 RocketMQ 中发送和消费延迟消息，演示订单超时取消、定时任务触发等典型业务场景。

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

- ✅ 理解 RocketMQ 的核心架构：NameServer、Broker、Producer、Consumer
- ✅ 使用 Docker Compose 在本地部署 RocketMQ 集群
- ✅ 掌握 RocketMQ 延迟消息演示 的核心 API 与配置方式
- ✅ 能够在本地验证消息收发流程
- ✅ 将所学应用到异步解耦、流量削峰等实际场景

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    RocketMQ 消息架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌───────────┐         ┌───────────┐         ┌───────────┐    │
│   │ Producer  │────────▶│   Broker  │────────▶│ Consumer  │    │
│   │           │  send   │           │  pull   │           │    │
│   └───────────┘         └─────┬─────┘         └───────────┘    │
│                               │                                 │
│                        ┌──────┴──────┐                          │
│                        │  NameServer  │                          │
│                        │ (路由注册中心)│                          │
│                        └─────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 RocketMQ 容器 |
| Docker Compose | >= 1.29 | 编排服务 |

### 部署步骤

```bash
# 1. 进入案例目录
cd messaging/rocketmq-delay-messages

# 2. 启动 RocketMQ
./scripts/start.sh

# 3. 验证状态
./scripts/check.sh
```

---

## 📖 核心概念

### 1. NameServer

NameServer 是 RocketMQ 的路由注册中心，Broker 启动时向 NameServer 注册，Producer 和 Consumer 从 NameServer 获取路由信息。

### 2. Broker

Broker 负责消息存储、投递和查询。一个 Broker 可以包含多个 Queue，实现负载均衡和水平扩展。

### 3. Topic 与 Queue

- **Topic**：消息主题，逻辑分类
- **Queue**：消息队列，物理分片，一个 Topic 可包含多个 Queue

### 4. 延迟消息

延迟消息允许指定消息在投递后延迟一段时间再被消费者消费，常用于订单超时取消、定时提醒等场景。

---

## 💻 代码示例

### 启动环境

```bash
./scripts/start.sh
```

### 停止环境

```bash
./scripts/stop.sh
```

### 检查状态

```bash
./scripts/check.sh
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `docker-compose.yml` | 定义 NameServer、Broker、Dashboard 服务 |
| `configs/broker.conf` | Broker 核心配置 |
| `scripts/*.sh` | 一键启动、停止、检查脚本 |

---

## 🧪 验证测试

服务启动后，访问 RocketMQ Dashboard：

```
http://localhost:8080
```

检查 Broker 是否已成功注册到 NameServer。

---

## 📊 运行结果

预期输出：

```
RocketMQ 已启动
NameServer: 运行中
Broker: 运行中
Dashboard: 运行中
```

---

## 🐛 常见问题

### Q1：Broker 启动失败怎么办？

**A**：检查 NameServer 是否先启动，查看日志：

```bash
docker-compose logs broker
```

### Q2：如何查看消息堆积？

**A**：通过 RocketMQ Dashboard 或命令行工具查看 Topic 消费进度。

---

## 📚 扩展学习

### 相关案例

- [RocketMQ 生产者消费者模式](../rocketmq-producer-consumer/)
- [RocketMQ 延迟消息演示](../rocketmq-delay-messages/)

### 推荐资源

- [Apache RocketMQ 官方文档](https://rocketmq.apache.org/docs/)
- [RocketMQ 设计文档](https://rocketmq.apache.org/docs/introduction/02quickstart/)

---

*最后更新：2026-06-27*  
*版本：1.0.0*  
*维护者：OpenDemo Team*
