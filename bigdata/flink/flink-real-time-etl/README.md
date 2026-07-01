# Flink 实时 ETL 处理 - Kafka 流数据清洗转换

> 使用 Docker Compose 部署 Apache Flink，从 Kafka 读取用户行为事件流，进行实时过滤、转换和聚合，将结果输出到下游。

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

- ✅ 理解 Flink 的 DataStream API 和 Table API
- ✅ 使用 Docker Compose 部署 Flink JobManager + TaskManager
- ✅ 编写 Flink SQL 实现实时 ETL
- ✅ 理解事件时间（Event Time）和水印（Watermark）概念
- ✅ 在 Flink UI 中监控作业运行状态

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flink 实时 ETL 架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Kafka Topic ──▶ Flink JobManager ──▶ TaskManager             │
│   user-events          │                    │                   │
│                        │                    ▼                   │
│                        │              实时聚合/转换              │
│                        │                    │                   │
│                        │                    ▼                   │
│                        │              下游存储（MySQL/Redis）    │
│                        ▼                                        │
│                   Flink Web UI:8081                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 Flink 容器 |
| Docker Compose | >= 1.29 | 编排服务 |

### 启动 Flink

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 进入案例目录
cd bigdata/flink/flink-real-time-etl

# 2. 启动 Flink
./scripts/start.sh

# 3. 检查状态
./scripts/check.sh
```

### 访问 Flink UI

```
http://localhost:8081
```

---

## 📖 核心概念

### 1. 流处理 vs 批处理

- **批处理**：处理有界数据集，如 HDFS 上的历史数据
- **流处理**：处理无界数据流，如 Kafka 实时事件

Flink 统一了流处理和批处理，底层都以流的方式执行。

### 2. Event Time 与 Watermark

- **Event Time**：事件实际发生的时间
- **Processing Time**：数据被处理的时间
- **Watermark**：允许迟到数据的时间边界

### 3. Checkpoint 与状态

Flink 通过 Checkpoint 实现容错，定期将算子状态持久化到外部存储（如 HDFS、RocksDB）。

---

## 💻 代码示例

### Flink SQL 实时聚合

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

# 定义 Kafka 源表
t_env.execute_sql('''
    CREATE TABLE user_events (
        user_id STRING,
        event_type STRING,
        event_time TIMESTAMP(3),
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'user-events',
        'properties.bootstrap.servers' = 'kafka:9092',
        'format' = 'json'
    )
''')

# 定义结果表
t_env.execute_sql('''
    CREATE TABLE event_stats (
        event_type STRING,
        event_count BIGINT,
        window_start TIMESTAMP(3)
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:mysql://mysql:3306/demo',
        'table-name' = 'event_stats',
        'username' = 'root',
        'password' = 'rootpass'
    )
''')

# 5 秒滚动窗口聚合
t_env.execute_sql('''
    INSERT INTO event_stats
    SELECT
        event_type,
        COUNT(*) AS event_count,
        TUMBLE_START(event_time, INTERVAL '5' SECOND) AS window_start
    FROM user_events
    GROUP BY
        event_type,
        TUMBLE(event_time, INTERVAL '5' SECOND)
''')
```

---

## 🔧 配置说明

| 服务 | 端口 | 作用 |
|------|------|------|
| jobmanager | 8081 | 作业调度和协调 |
| taskmanager | 随机 | 执行具体 Task |

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 检查 Flink 集群
curl -s http://localhost:8081/overview | python3 -m json.tool

# 提交测试作业（需安装 flink 连接器依赖）
# docker exec jobmanager flink run /data/code/etl_job.py
```

---

## 📊 运行结果

Flink UI 显示：
- JobManager 和 TaskManager 正常运行
- 提交的作业状态为 RUNNING
- 输出到下游的聚合结果随时间更新

---

## 🐛 常见问题

### Q1：TaskManager 无法注册到 JobManager？

**A**：检查 `JOB_MANAGER_RPC_ADDRESS` 环境变量是否设置为 `jobmanager`。

### Q2：Kafka 连接器类找不到？

**A**：Flink 容器需要额外安装 Kafka connector JAR，实际生产环境需将依赖放入 `lib` 目录。

---

## 📚 扩展学习

- [Spark SQL 批处理分析](../spark/spark-sql-batch-analytics/)
- [Kafka 流处理演示](../../kafka/kafka-stream-processing/)
- [Apache Flink 官方文档](https://nightlies.apache.org/flink/flink-docs-stable/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
