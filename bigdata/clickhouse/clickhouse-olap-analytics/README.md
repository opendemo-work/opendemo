# ClickHouse OLAP 分析 - 用户行为实时分析

> 使用 Docker 部署 ClickHouse 列式数据库，导入用户事件数据并执行高并发 OLAP 聚合查询，体验 ClickHouse 在分析场景下的极致性能。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
  - [环境要求](#环境要求)
  - [启动 ClickHouse](#启动-clickhouse)
  - [执行查询](#执行查询)
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

- ✅ 解释列式存储与行式存储的区别及适用场景
- ✅ 使用 Docker 部署单节点 ClickHouse
- ✅ 创建 MergeTree 引擎表并导入数据
- ✅ 编写高效的 GROUP BY 聚合查询
- ✅ 理解 ClickHouse 的分区和排序键设计

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    ClickHouse OLAP 查询流程                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   应用/BI ──▶ ClickHouse Server ──▶ MergeTree 表引擎           │
│                   │                       │                     │
│                   │              ┌────────┴────────┐           │
│                   │              │   列式存储分区   │           │
│                   │              │  按日期排序索引  │           │
│                   │              └─────────────────┘           │
│                   │                                            │
│                   ▼                                            │
│              向量化执行引擎                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 ClickHouse 容器 |
| Docker Compose | >= 1.29 | 编排服务 |
| Python | >= 3.9 | 可选，用于 Python 客户端查询 |

### 启动 ClickHouse

```bash
# 1. 进入案例目录
cd bigdata/clickhouse/clickhouse-olap-analytics

# 2. 启动 ClickHouse
./scripts/start.sh

# 3. 等待服务就绪
sleep 5

# 4. 检查状态
./scripts/check.sh
```

### 执行查询

```bash
# 使用 HTTP 接口执行 SQL
curl -s http://localhost:8123 -d "SELECT event_type, COUNT(*) AS cnt, SUM(amount) AS total FROM demo.events GROUP BY event_type ORDER BY total DESC"

# 或使用 Python 客户端
pip install requests
python code/query.py
```

---

## 📖 核心概念

### 1. 列式存储

传统关系型数据库（如 MySQL）按行存储数据，适合 OLTP 场景。ClickHouse 按列存储数据，同一列的数据物理上连续存放，适合 OLAP 场景：

- **压缩率高**：同列数据类型相同，压缩效果更好
- **查询速度快**：只需读取查询涉及的列，避免全行扫描
- **向量化执行**：利用 SIMD 指令批量处理数据

### 2. MergeTree 引擎

MergeTree 是 ClickHouse 最常用的表引擎，支持：

- 按主键排序和稀疏索引
- 按分区键分区
- 数据自动合并和去重（带 ReplacingMergeTree 等变体）

```sql
CREATE TABLE demo.events (
    event_date Date,
    user_id UInt64,
    event_type String,
    amount Decimal64(2)
) ENGINE = MergeTree()
ORDER BY (event_date, user_id);
```

### 3. 分区与排序键

- **分区键（PARTITION BY）**：决定数据如何物理分区，通常按时间
- **排序键（ORDER BY）**：决定每个分区内数据的排序方式，影响查询性能

---

## 💻 代码示例

### 创建表并导入数据

```sql
CREATE DATABASE IF NOT EXISTS demo;

CREATE TABLE IF NOT EXISTS demo.events (
    event_date Date,
    user_id UInt64,
    event_type String,
    amount Decimal64(2)
) ENGINE = MergeTree()
ORDER BY (event_date, user_id);

INSERT INTO demo.events VALUES
('2026-06-01', 1, 'purchase', 100.00),
('2026-06-01', 2, 'view', 0.00),
('2026-06-02', 1, 'purchase', 250.00),
('2026-06-02', 3, 'purchase', 80.00);
```

### 聚合查询

```sql
SELECT
    event_type,
    COUNT(*) AS event_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
FROM demo.events
GROUP BY event_type
ORDER BY total_amount DESC;
```

### Python 查询示例

```python
import requests

query = """
SELECT event_type, COUNT(*) AS cnt, SUM(amount) AS total
FROM demo.events
GROUP BY event_type
ORDER BY total DESC
"""

resp = requests.post('http://localhost:8123', data=query)
print(resp.text)
```

---

## 🔧 配置说明

### docker-compose.yml

| 服务 | 端口 | 说明 |
|------|------|------|
| clickhouse | 8123 (HTTP), 9000 (Native) | ClickHouse 服务端 |

### 初始化脚本

`init.sql` 在容器首次启动时自动执行，完成建库、建表和初始数据导入。

---

## 🧪 验证测试

```bash
# 1. 检查服务是否可访问
curl -s http://localhost:8123/ping

# 2. 查看数据库列表
curl -s http://localhost:8123 -d "SHOW DATABASES"

# 3. 查看表数据
curl -s http://localhost:8123 -d "SELECT * FROM demo.events"

# 4. 执行聚合查询
curl -s http://localhost:8123 -d "SELECT event_type, COUNT(*), SUM(amount) FROM demo.events GROUP BY event_type"
```

---

## 📊 运行结果

### 表数据

```
2026-06-01      1       purchase        100.00
2026-06-01      2       view            0.00
2026-06-02      1       purchase        250.00
2026-06-02      3       purchase        80.00
```

### 聚合结果

```
purchase        3       430.00
view            1       0.00
```

---

## 🐛 常见问题

### Q1：ClickHouse 启动后无法连接？

**A**：ClickHouse 首次启动需要初始化，请等待 10-20 秒。查看日志：

```bash
docker logs clickhouse-server
```

### Q2：Decimal 类型精度不够？

**A**：根据业务需求调整 `Decimal(P, S)` 中的精度 P 和标度 S。例如 `Decimal64(2)` 表示 18 位有效数字，2 位小数。

### Q3：如何导入大量数据？

**A**：使用 `INSERT INTO ... FORMAT CSV` 或 `clickhouse-client --query="INSERT INTO ... FORMAT CSV" < data.csv`。

---

## 📚 扩展学习

### 相关案例

- [Spark SQL 批处理分析](../spark/spark-sql-batch-analytics/) - 离线批处理
- [Flink 实时 ETL](../flink/flink-real-time-etl/) - 实时流处理

### 推荐资源

- 📖 [ClickHouse 官方文档](https://clickhouse.com/docs/)
- 📖 [ClickHouse 快速入门](https://clickhouse.com/docs/en/getting-started/quick-start)
- 🎥 [ClickHouse 架构解析](https://clickhouse.com/blog/)

### 进阶实验

- [ ] 使用 `PARTITION BY` 按月份分区并对比查询性能
- [ ] 测试 ClickHouse 在 1000 万行数据上的聚合性能
- [ ] 使用 `MATERIALIZED VIEW` 创建预聚合视图
- [ ] 使用 `JOIN` 进行多表关联分析

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
