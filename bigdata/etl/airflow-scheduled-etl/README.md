# Airflow 定时 ETL 调度 - 数据管道编排实战

> 使用 Docker Compose 部署 Apache Airflow，编写 DAG 实现从数据抽取、转换到加载的定时 ETL 流程，学习任务依赖编排与调度监控。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
  - [环境要求](#环境要求)
  - [启动 Airflow](#启动-airflow)
  - [触发 DAG](#触发-dag)
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

- ✅ 理解 Airflow 的核心概念：DAG、Operator、Task、Schedule
- ✅ 使用 Docker Compose 部署 Airflow（Webserver + Scheduler + Metadata DB）
- ✅ 编写包含依赖关系的 Python DAG
- ✅ 在 Airflow UI 中手动触发和监控 DAG 运行
- ✅ 设计简单的 ETL 数据管道

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Airflow 架构                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐         ┌──────────────┐                    │
│   │   Webserver  │◀───────▶│   Scheduler  │                    │
│   │   (UI/API)   │         │  (解析/调度)  │                    │
│   └──────────────┘         └──────┬───────┘                    │
│                                   │                             │
│                                   ▼                             │
│                          ┌─────────────────┐                   │
│                          │   PostgreSQL    │                   │
│                          │  (Metadata DB)  │                   │
│                          └─────────────────┘                   │
│                                                                 │
│   DAG 文件 ──▶ /opt/airflow/dags ──▶ Scheduler 解析并执行      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 Airflow 容器 |
| Docker Compose | >= 1.29 | 编排服务 |
| 内存 | >= 4GB | Airflow 需要约 2GB 内存 |

### 启动 Airflow

```bash
# 1. 进入案例目录
cd bigdata/etl/airflow-scheduled-etl

# 2. 启动 Airflow（包含首次初始化）
./scripts/start.sh

# 3. 等待初始化完成（约 30-60 秒）
sleep 45

# 4. 检查状态
./scripts/check.sh
```

### 访问 Airflow UI

```
URL: http://localhost:8080
用户名: admin
密码: admin
```

### 触发 DAG

1. 在 UI 中找到 `etl_demo` DAG
2. 点击 DAG 名称进入详情页
3. 点击右上角的开关启用 DAG
4. 点击 "Trigger DAG" 手动触发
5. 在 Graph View 中查看任务执行状态

---

## 📖 核心概念

### 1. DAG（有向无环图）

DAG 是 Airflow 的核心，定义了一组任务及其执行顺序。DAG 本身不执行任务，只描述任务间的依赖关系。

### 2. Operator

Operator 定义了任务的类型，常见的有：

- `PythonOperator`：执行 Python 函数
- `BashOperator`：执行 Bash 命令
- `DockerOperator`：在 Docker 容器中执行任务
- `PostgresOperator`：执行 PostgreSQL 语句

### 3. Task 依赖

使用 `>>` 和 `<<` 定义任务依赖：

```python
t1 >> t2 >> t3  # t1 完成后执行 t2，t2 完成后执行 t3
```

### 4. Schedule Interval

`schedule_interval` 定义 DAG 的运行频率：

- `timedelta(hours=1)`：每小时运行一次
- `"0 9 * * *"`：每天上午 9 点运行
- `@daily`：每天运行一次

---

## 💻 代码示例

### DAG 定义（dags/etl_demo.py）

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def extract():
    """从数据源抽取原始数据"""
    print("Extracting data from source...")
    # 实际场景：读取数据库、API、文件等
    return {"raw_data": [1, 2, 3, 4, 5]}


def transform(**context):
    """清洗和转换数据"""
    raw_data = context['ti'].xcom_pull(task_ids='extract')
    print(f"Transforming data: {raw_data}")
    # 实际场景：数据清洗、格式转换、聚合计算
    transformed = [x * 2 for x in raw_data['raw_data']]
    return {"transformed_data": transformed}


def load(**context):
    """加载数据到目标存储"""
    transformed = context['ti'].xcom_pull(task_ids='transform')
    print(f"Loading data: {transformed}")
    # 实际场景：写入数据仓库、数据库、文件系统等


with DAG(
    dag_id='etl_demo',
    default_args={
        'owner': 'opendemo',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='OpenDemo ETL pipeline with Airflow',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2026, 6, 1),
    catchup=False,
    tags=['etl', 'demo'],
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    
    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    
    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )
    
    extract_task >> transform_task >> load_task
```

---

## 🔧 配置说明

### 服务组成

| 服务 | 作用 |
|------|------|
| `postgres` | Airflow 元数据库 |
| `airflow-init` | 初始化数据库和 admin 用户 |
| `airflow-webserver` | Web UI 和 REST API |
| `airflow-scheduler` | DAG 解析和任务调度 |

### 关键环境变量

| 变量 | 说明 |
|------|------|
| `AIRFLOW__CORE__EXECUTOR` | 执行器类型，本案例使用 LocalExecutor |
| `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` | 元数据库连接字符串 |

---

## 🧪 验证测试

```bash
# 1. 检查容器状态
docker ps --filter name=airflow

# 2. 查看 DAG 是否正确加载
docker exec airflow-webserver airflow dags list

# 3. 测试 DAG 任务
docker exec airflow-webserver airflow tasks test etl_demo extract 2026-06-01

# 4. 查看任务日志
docker exec airflow-webserver airflow tasks test etl_demo load 2026-06-01
```

---

## 📊 运行结果

DAG 成功运行后，在 Airflow UI 中可以看到：

- `extract` 任务状态：success
- `transform` 任务状态：success
- `load` 任务状态：success

任务日志中会输出：

```
Extracting data from source...
Transforming data: {'raw_data': [1, 2, 3, 4, 5]}
Loading data: {'transformed_data': [2, 4, 6, 8, 10]}
```

---

## 🐛 常见问题

### Q1：Airflow 初始化失败？

**A**：PostgreSQL 启动需要一定时间，请等待后重新运行 `./scripts/start.sh`。查看日志：

```bash
docker logs airflow-init
```

### Q2：DAG 没有出现在 UI 中？

**A**：检查 DAG 文件是否已挂载到 `/opt/airflow/dags`，并确认 DAG 代码无语法错误：

```bash
docker exec airflow-webserver python -m py_compile dags/etl_demo.py
```

### Q3：任务执行失败如何重试？

**A**：在 Airflow UI 中点击失败的任务，选择 "Clear" 清除状态后重新运行。

---

## 📚 扩展学习

### 相关案例

- [Spark SQL 批处理分析](../spark/spark-sql-batch-analytics/) - 离线数据处理
- [Flink 实时 ETL](../flink/flink-real-time-etl/) - 实时流处理

### 推荐资源

- 📖 [Apache Airflow 官方文档](https://airflow.apache.org/docs/)
- 📖 [Airflow DAG 编写最佳实践](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- 🎥 [Airflow 官方教程](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)

### 进阶实验

- [ ] 使用 `BashOperator` 执行 Shell 脚本
- [ ] 使用 `PostgresOperator` 写入数据库
- [ ] 配置邮件/Slack 告警通知
- [ ] 使用 Airflow Variables 和 Connections 管理配置

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
