# 数据仓库分层设计 - ODS/DWD/DWS/ADS 实战

> 使用 MySQL 演示数据仓库经典四层架构：ODS 贴源层、DWD 明细层、DWS 汇总层、ADS 应用层，理解每层职责和 ETL 加工逻辑。

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

- ✅ 理解数据仓库四层的职责划分
- ✅ 使用 SQL 实现从 ODS 到 ADS 的逐层加工
- ✅ 区分贴源存储、明细清洗、维度汇总和指标应用
- ✅ 设计简单的分层 ETL 流程

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    数据仓库分层架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   业务系统 ──▶ ODS 贴源层 ──▶ DWD 明细层                       │
│   (MySQL/     (原始数据)      (清洗/标准化)                     │
│    API)                                                         │
│                                │                                │
│                                ▼                                │
│                         DWS 汇总层                              │
│                      (按主题/时间聚合)                          │
│                                │                                │
│                                ▼                                │
│                          ADS 应用层                             │
│                       (面向业务指标)                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 MySQL 容器 |
| Docker Compose | >= 1.29 | 编排服务 |

### 启动并初始化

```bash
cd bigdata/data-warehouse/dwd-dws-ads-layer-design
./scripts/start.sh
sleep 20

# 按顺序执行分层 SQL
mysql -h127.0.0.1 -uroot -prootpass demo_dw < sql/01_ods.sql
mysql -h127.0.0.1 -uroot -prootpass demo_dw < sql/02_dwd.sql
mysql -h127.0.0.1 -uroot -prootpass demo_dw < sql/03_dws.sql
mysql -h127.0.0.1 -uroot -prootpass demo_dw < sql/04_ads.sql
```

---

## 📖 核心概念

### 1. ODS（Operational Data Store）贴源层

- 直接同步业务系统数据
- 结构与源系统保持一致
- 保留原始数据，不做清洗

### 2. DWD（Data Warehouse Detail）明细层

- 对 ODS 数据进行清洗、脱敏、标准化
- 统一编码、字段格式
- 形成主题明细表

### 3. DWS（Data Warehouse Summary）汇总层

- 按主题、时间维度进行轻度/重度汇总
- 生成日报、周报、月报等汇总表
- 为 ADS 层提供预聚合数据

### 4. ADS（Application Data Store）应用层

- 面向具体业务场景
- 提供可直接使用的指标数据
- 支撑报表、BI、算法等应用

---

## 💻 代码示例

### ODS 层：原始订单表

```sql
CREATE TABLE IF NOT EXISTS ods_orders (
    order_id BIGINT,
    user_id BIGINT,
    order_time DATETIME,
    amount DECIMAL(10,2),
    status VARCHAR(50)
);

INSERT INTO ods_orders VALUES
(1, 1001, '2026-06-01 10:00:00', 120.00, 'completed'),
(2, 1002, '2026-06-01 11:00:00', 300.00, 'completed'),
(3, 1001, '2026-06-02 09:00:00', 80.00, 'pending');
```

### DWD 层：清洗后订单明细

```sql
CREATE TABLE IF NOT EXISTS dwd_orders AS
SELECT
    order_id,
    user_id,
    DATE(order_time) AS order_date,
    amount,
    LOWER(TRIM(status)) AS status
FROM ods_orders
WHERE status = 'completed';
```

### DWS 层：用户日汇总

```sql
CREATE TABLE IF NOT EXISTS dws_user_daily AS
SELECT
    user_id,
    order_date,
    COUNT(order_id) AS order_cnt,
    SUM(amount) AS total_amount
FROM dwd_orders
GROUP BY user_id, order_date;
```

### ADS 层：用户消费总览

```sql
CREATE TABLE IF NOT EXISTS ads_user_summary AS
SELECT
    user_id,
    SUM(order_cnt) AS total_orders,
    SUM(total_amount) AS total_amount,
    ROUND(SUM(total_amount) / SUM(order_cnt), 2) AS avg_order_amount
FROM dws_user_daily
GROUP BY user_id;
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `sql/01_ods.sql` | 创建贴源表并导入原始数据 |
| `sql/02_dwd.sql` | 明细层清洗转换 |
| `sql/03_dws.sql` | 汇总层聚合计算 |
| `sql/04_ads.sql` | 应用层指标输出 |
| `docker-compose.yml` | MySQL 服务部署 |

---

## 🧪 验证测试

```bash
# 查看各层数据
mysql -h127.0.0.1 -uroot -prootpass demo_dw -e "SELECT * FROM ods_orders"
mysql -h127.0.0.1 -uroot -prootpass demo_dw -e "SELECT * FROM dwd_orders"
mysql -h127.0.0.1 -uroot -prootpass demo_dw -e "SELECT * FROM dws_user_daily"
mysql -h127.0.0.1 -uroot -prootpass demo_dw -e "SELECT * FROM ads_user_summary"
```

---

## 📊 运行结果

### ads_user_summary 输出

```
+---------+--------------+-------------+------------------+
| user_id | total_orders | total_amount | avg_order_amount |
+---------+--------------+-------------+------------------+
|    1001 |            1 |      120.00 |           120.00 |
|    1002 |            1 |      300.00 |           300.00 |
+---------+--------------+-------------+------------------+
```

---

## 🐛 常见问题

### Q1：MySQL 连接被拒绝？

**A**：等待 MySQL 初始化完成，或检查密码是否为 `rootpass`。

### Q2：DWD 层数据为空？

**A**：检查 ODS 数据中的 `status` 值是否包含 `completed`。

---

## 📚 扩展学习

- [Spark SQL 批处理分析](../spark/spark-sql-batch-analytics/)
- [Airflow 定时 ETL 调度](../etl/airflow-scheduled-etl/)
- [ClickHouse OLAP 分析](../clickhouse/clickhouse-olap-analytics/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
