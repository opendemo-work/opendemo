# Iceberg 数据湖演示 - 开放表格式实战

> 使用 Apache Iceberg 与 Spark 构建数据湖，演示时间旅行、分区演进和增量读取等现代数据湖核心特性。

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

- ✅ 理解数据湖与传统数据仓库的区别
- ✅ 解释 Iceberg 的开放表格式核心设计
- ✅ 使用 Spark 创建 Iceberg 表并插入数据
- ✅ 演示 Iceberg 的时间旅行和分区演进能力

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Iceberg 数据湖架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Spark/Flink ──▶ Iceberg Catalog ──▶ 元数据层                  │
│                        │                                        │
│                        ▼                                        │
│              ┌─────────────────────┐                           │
│              │   Metadata Files    │                           │
│              │   (Schema/分区/快照) │                           │
│              └─────────────────────┘                           │
│                        │                                        │
│                        ▼                                        │
│              ┌─────────────────────┐                           │
│              │   Data Files        │                           │
│              │   (Parquet/Avro/ORC)│                           │
│              └─────────────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 Spark-Iceberg 容器 |
| Docker Compose | >= 1.29 | 编排服务 |

### 启动 Spark-Iceberg

```bash
cd bigdata/data-lake/iceberg-data-lake-demo
./scripts/start.sh
sleep 15
./scripts/check.sh
```

---

## 📖 核心概念

### 1. 开放表格式

Iceberg 是一种开放表格式，定义了数据如何在对象存储（S3、HDFS、MinIO）上以表的形式组织。它不绑定特定计算引擎。

### 2. 时间旅行（Time Travel）

Iceberg 每次写入都会产生一个快照（Snapshot），可以查询历史版本数据：

```sql
SELECT * FROM demo.orders VERSION AS OF 1;
```

### 3. 分区演进（Partition Evolution）

可以在不重写数据的情况下修改分区策略，Iceberg 会自动处理新旧分区策略的兼容。

---

## 💻 代码示例

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("IcebergDemo") \
    .config("spark.sql.catalog.demo", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.demo.type", "hadoop") \
    .config("spark.sql.catalog.demo.warehouse", "/data/warehouse") \
    .getOrCreate()

# 创建 Iceberg 表
spark.sql("""
    CREATE TABLE demo.orders (
        id BIGINT,
        amount DOUBLE,
        ts TIMESTAMP
    ) USING iceberg
    PARTITIONED BY (days(ts))
""")

# 插入第一批数据
spark.sql("""
    INSERT INTO demo.orders VALUES
    (1, 100.0, TIMESTAMP '2026-06-01 10:00:00'),
    (2, 200.0, TIMESTAMP '2026-06-01 11:00:00')
""")

# 查询当前数据
spark.sql("SELECT * FROM demo.orders").show()

# 插入第二批数据
spark.sql("""
    INSERT INTO demo.orders VALUES
    (3, 150.0, TIMESTAMP '2026-06-02 09:00:00')
""")

# 时间旅行：查询第一个快照
spark.sql("SELECT * FROM demo.orders VERSION AS OF 1").show()

# 查看快照历史
spark.sql("SELECT * FROM demo.orders.snapshots").show(truncate=False)

spark.stop()
```

---

## 🔧 配置说明

| 配置项 | 说明 |
|--------|------|
| `spark.sql.catalog.demo` | 注册名为 `demo` 的 Iceberg Catalog |
| `spark.sql.catalog.demo.type` | Catalog 类型，本案例使用 Hadoop 文件系统 |
| `spark.sql.catalog.demo.warehouse` | 数据仓库根目录 |

---

## 🧪 验证测试

```bash
# 进入容器运行示例
docker exec spark-iceberg python /home/iceberg/notebooks/iceberg_demo.py

# 查看生成的元数据和数据文件
docker exec spark-iceberg ls -R /data/warehouse/demo.db/orders
```

---

## 📊 运行结果

```
+---+------+-------------------+
| id|amount|                 ts|
+---+------+-------------------+
|  1| 100.0|2026-06-01 10:00:00|
|  2| 200.0|2026-06-01 11:00:00|
|  3| 150.0|2026-06-02 09:00:00|
+---+------+-------------------+
```

---

## 🐛 常见问题

### Q1：Iceberg 表创建失败？

**A**：确认 Spark Session 中 Catalog 配置正确，且仓库目录有写入权限。

### Q2：时间旅行查询无结果？

**A**：检查快照 ID 是否正确，可以通过 `.snapshots` 表查看所有快照。

---

## 📚 扩展学习

- [Spark SQL 批处理分析](../spark/spark-sql-batch-analytics/)
- [ClickHouse OLAP 分析](../clickhouse/clickhouse-olap-analytics/)
- [Apache Iceberg 官方文档](https://iceberg.apache.org/docs/latest/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
