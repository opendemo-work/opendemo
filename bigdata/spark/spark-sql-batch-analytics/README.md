# Spark SQL 批处理分析 - 电商订单聚合实战

> 使用 Docker Compose 部署 Apache Spark 3.5 集群，通过 Spark SQL 读取 CSV 订单数据，按商品类别进行销售额和订单量聚合分析。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
  - [环境要求](#环境要求)
  - [启动 Spark 集群](#启动-spark-集群)
  - [运行分析任务](#运行分析任务)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
  - [DataFrame API 版本](#dataframe-api-版本)
  - [SQL 版本](#sql-版本)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 解释 Spark SQL 与 DataFrame API 的关系
- ✅ 使用 Docker Compose 启动 Spark Standalone 集群
- ✅ 通过 `spark-submit` 提交 Python 作业
- ✅ 使用 Spark SQL 进行分组聚合（GROUP BY + SUM/AVG/COUNT）
- ✅ 理解 Spark 的惰性求值和物理执行计划

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Spark Standalone 架构                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐    submit     ┌─────────────┐                │
│   │  客户端     │──────────────▶│ Spark Master │                │
│   │ (analytics.py)│              │  (调度器)    │                │
│   └─────────────┘               └──────┬──────┘                │
│                                        │                        │
│                              ┌─────────┴─────────┐              │
│                              ▼                   ▼              │
│                        ┌──────────┐        ┌──────────┐        │
│                        │ Worker 1 │        │ Worker 2 │        │
│                        │ (Executor)│        │ (Executor)│       │
│                        └────┬─────┘        └────┬─────┘        │
│                             │                   │               │
│                             └────────┬──────────┘               │
│                                      ▼                          │
│                            ┌─────────────────┐                  │
│                            │   CSV 数据源     │                  │
│                            │   sales.csv     │                  │
│                            └─────────────────┘                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 Spark 容器 |
| Docker Compose | >= 1.29 | 编排 Master + Worker |
| 内存 | >= 4GB | Spark 容器需要约 2GB 内存 |

### 启动 Spark 集群

```bash
# 1. 进入案例目录
cd bigdata/spark/spark-sql-batch-analytics

# 2. 启动 Spark Master 和 Worker
./scripts/start.sh

# 3. 等待集群就绪（约 10-15 秒）
sleep 15

# 4. 检查集群状态
./scripts/check.sh
```

启动后可通过浏览器访问 Spark UI：

- **Spark Master UI**: http://localhost:8080
- **Spark Application UI**: 提交作业后动态分配

### 运行分析任务

```bash
# 将分析脚本复制到 Spark Master 容器并提交
docker cp code/analytics.py spark-master:/tmp/analytics.py
docker cp data/sales.csv spark-master:/tmp/sales.csv

docker exec spark-master \
  spark-submit \
  --master spark://spark-master:7077 \
  --name "OpenDemo Spark SQL Analytics" \
  /tmp/analytics.py
```

---

## 📖 核心概念

### 1. Spark SQL

Spark SQL 是 Apache Spark 的模块之一，用于处理结构化数据。它将 SQL 查询与 Spark 程序无缝集成，支持：

- 通过 SQL 语句查询数据
- 通过 DataFrame/Dataset API 以编程方式处理数据
- 与 Hive、JDBC、Parquet、JSON、CSV 等多种数据源交互

### 2. DataFrame

DataFrame 是分布式的行集合，带有模式（Schema）。它类似于 pandas DataFrame，但数据分布在集群中，可以处理 TB 级数据。

```python
df = spark.read.option("header", True).csv("/tmp/sales.csv")
df.show()
```

### 3. 惰性求值（Lazy Evaluation）

Spark 的转换操作（Transformation）不会立即执行，只有在遇到行动操作（Action，如 `show()`、`collect()`、`write()`）时才会触发计算。Spark 会自动优化执行计划。

### 4. Spark Standalone

Spark Standalone 是 Spark 自带的资源管理器，不依赖 YARN 或 Kubernetes。它由 Master 和 Worker 组成，适合本地开发和测试。

---

## 💻 代码示例

### DataFrame API 版本

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, count

spark = SparkSession.builder \
    .appName("OpenDemo Spark SQL") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# 读取 CSV
df = spark.read.option("header", True) \
    .option("inferSchema", True) \
    .csv("/tmp/sales.csv")

# DataFrame API 聚合
result = df.groupBy("category") \
    .agg(
        sum("amount").alias("total_sales"),
        avg("amount").alias("avg_sales"),
        count("order_id").alias("order_count")
    ) \
    .orderBy("total_sales", ascending=False)

result.show()
spark.stop()
```

### SQL 版本

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("OpenDemo Spark SQL") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

df = spark.read.option("header", True) \
    .option("inferSchema", True) \
    .csv("/tmp/sales.csv")

# 注册临时视图
df.createOrReplaceTempView("sales")

result = spark.sql("""
    SELECT
        category,
        SUM(amount) AS total_sales,
        AVG(amount) AS avg_sales,
        COUNT(order_id) AS order_count
    FROM sales
    GROUP BY category
    ORDER BY total_sales DESC
""")

result.show()
spark.stop()
```

---

## 🔧 配置说明

### docker-compose.yml 关键配置

| 服务 | 作用 | 端口 |
|------|------|------|
| `spark-master` | Spark 主节点，负责任务调度 | 8080 (UI), 7077 (Spark 端口) |
| `spark-worker` | Spark 工作节点，负责执行 Task | 随机端口 |

### Spark 参数

| 参数 | 说明 |
|------|------|
| `--master spark://spark-master:7077` | 指定 Spark Standalone Master 地址 |
| `--name` | 应用名称，显示在 Spark UI 上 |
| `--executor-memory` | 每个 Executor 的内存大小 |
| `--num-executors` | Executor 数量 |

---

## 🧪 验证测试

### 1. 检查集群状态

访问 http://localhost:8080，确认：
- Master 状态为 ALIVE
- 至少 1 个 Worker 状态为 ALIVE

### 2. 检查 Worker 日志

```bash
docker logs spark-worker
```

### 3. 检查作业输出

运行 `analytics.py` 后，应输出类似以下内容：

```
+-----------+-----------+---------+-----------+
|   category|total_sales|avg_sales|order_count|
+-----------+-----------+---------+-----------+
|Electronics|     2000.0|   1000.0|          2|
|   Clothing|      750.0|    375.0|          2|
|       Food|      150.0|    150.0|          1|
+-----------+-----------+---------+-----------+
```

---

## 📊 运行结果

### 输入数据（data/sales.csv）

```csv
order_id,category,amount
1,Electronics,1200
2,Clothing,300
3,Electronics,800
4,Food,150
5,Clothing,450
```

### 预期输出

```
+-----------+-----------+---------+-----------+
|   category|total_sales|avg_sales|order_count|
+-----------+-----------+---------+-----------+
|Electronics|     2000.0|   1000.0|          2|
|   Clothing|      750.0|    375.0|          2|
|       Food|      150.0|    150.0|          1|
+-----------+-----------+---------+-----------+
```

---

## 🐛 常见问题

### Q1：Spark Worker 无法连接到 Master？

**A**：检查 `SPARK_MASTER_URL` 环境变量是否正确设置为 `spark://spark-master:7077`，并确认容器在同一 Docker 网络中。

### Q2：提交作业时提示 `Connection refused`？

**A**：Master 启动需要几秒钟时间，请等待 10-15 秒后再提交。可以通过 `docker logs spark-master` 查看启动日志。

### Q3：CSV 文件找不到？

**A**：确保已将 `sales.csv` 复制到 Spark Master 容器内的 `/tmp/sales.csv`，或者修改代码中的路径为容器内实际路径。

### Q4：内存不足导致任务失败？

**A**：增加 Docker 容器内存限制，或在 `spark-submit` 中添加 `--executor-memory 512m`。

---

## 📚 扩展学习

### 相关案例

- [Flink 实时 ETL 处理](../flink/flink-real-time-etl/) - 学习流式数据处理
- [Kafka 流处理演示](../../kafka/kafka-stream-processing/) - 学习消息队列与流处理

### 推荐资源

- 📖 [Spark SQL 官方文档](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- 📖 [PySpark API 文档](https://spark.apache.org/docs/latest/api/python/)
- 🎥 [Spark 官方教程](https://spark.apache.org/docs/latest/quick-start.html)

### 进阶实验

- [ ] 将分析结果写入 Parquet 文件
- [ ] 使用 Spark SQL 进行多表 JOIN 分析
- [ ] 对比 DataFrame API 与 SQL 的性能差异
- [ ] 将 Spark 部署到 Kubernetes 上运行

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
