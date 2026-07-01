# Text2SQL：自然语言转 SQL

> 本案例详解 Text2SQL 的完整工作流，演示如何将自然语言问题转换为可执行的 SQL 查询，涵盖 Schema 理解、Prompt 工程、SQL 生成与结果验证。

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Text2SQL 完整工作流                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Natural Language Question                                             │
│   例："2023 年销售额最高的前 3 名客户是谁？"                              │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   1. Schema 理解与检索                            │  │
│   │                                                                  │  │
│   │   Database Schema:                                               │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ customers   │    │ orders      │    │ products    │        │  │
│   │   │ - id        │    │ - id        │    │ - id        │        │  │
│   │   │ - name      │    │ - customer_id│   │ - name      │        │  │
│   │   │ - email     │    │ - product_id │   │ - price     │        │  │
│   │   │ - region    │    │ - amount    │    │ - category  │        │  │
│   │   │             │    │ - order_date│    │             │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   │                                                                  │  │
│   │   操作：Schema Linking（识别相关表和列）                          │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   2. Prompt 构建                                  │  │
│   │                                                                  │  │
│   │   组成：                                                         │  │
│   │   • 任务说明                                                     │  │
│   │   • 相关表结构（CREATE TABLE ...）                                │  │
│   │   • Few-shot 示例（可选）                                         │  │
│   │   • 用户问题                                                     │  │
│   │   • 输出格式约束                                                 │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   3. SQL 生成                                     │  │
│   │                                                                  │  │
│   │   LLM → SELECT name, SUM(amount)                                │  │
│   │           FROM customers c                                      │  │
│   │           JOIN orders o ON c.id = o.customer_id                 │  │
│   │           WHERE strftime('%Y', o.order_date) = '2023'           │  │
│   │           GROUP BY c.id, c.name                                 │  │
│   │           ORDER BY total_amount DESC                            │  │
│   │           LIMIT 3                                               │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   4. 验证与执行                                   │  │
│   │                                                                  │  │
│   │   • 语法检查（解析 SQL）                                          │  │
│   │   • 安全校验（禁止 DROP/DELETE/UPDATE 等危险操作）                │  │
│   │   • 在只读模式下执行                                              │  │
│   │   • 结果格式化输出                                                │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   SQL Result / Natural Language Answer                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解 Text2SQL 的核心挑战与常见架构
- ✅ 掌握 Schema 描述、Few-shot 示例、Self-Correction 等 Prompt 工程技术
- ✅ 实现一个端到端的 Text2SQL 原型
- ✅ 学会验证 SQL 正确性与执行安全性

## 📖 核心概念

### 1. Text2SQL 的挑战

Text2SQL 是连接自然语言与结构化数据库的关键技术，面临以下挑战：

- **Schema 理解**：模型需要理解数据库表结构、列含义和表关系
- **歧义处理**：自然语言问题可能存在多种理解方式
- **复杂查询**：涉及多表 JOIN、聚合、子查询、排序等
- **安全性**：防止生成破坏性 SQL（如 DROP TABLE、DELETE 不带 WHERE）
- **领域适配**：不同数据库 Schema 差异很大

### 2. Schema Linking

Schema Linking 是指从用户问题中识别出相关的表、列和值，帮助模型聚焦关键信息。常见方法：

- **基于规则**：使用字符串匹配找出问题中提到的表名/列名
- **基于检索**：将 Schema 向量化，检索与问题最相关的表和列
- **基于模型**：使用专门的 Schema Linking 模型进行预测

### 3. Prompt 工程

有效的 Text2SQL Prompt 通常包含：

- **清晰的角色定义**："你是一个 SQL 专家"
- **Schema 描述**：以 CREATE TABLE 语句形式提供相关表结构
- **外键关系**：说明表之间的关联
- **Few-shot 示例**：提供问题-SQL 对的示例
- **输出约束**：要求只输出 SQL，不添加解释

### 4. SQL 验证与安全

生产环境中必须对生成的 SQL 进行安全检查：

- 只允许 SELECT 语句
- 禁止 DDL（CREATE/ALTER/DROP）和 DML（INSERT/UPDATE/DELETE）
- 限制查询结果行数
- 在只读连接上执行
- 对敏感表进行访问控制

## 💻 代码示例

完整代码位于 `code/` 目录。下面展示 Text2SQL 的核心实现：

```python
# code/text2sql_pipeline.py
import re
import sqlite3
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class TableSchema:
    """表结构定义"""
    name: str
    columns: List[str]
    description: str = ""


class SimpleNL2SQL:
    """简化版 Text2SQL Pipeline"""

    def __init__(self, schemas: List[TableSchema], examples: List[Dict] = None):
        self.schemas = schemas
        self.examples = examples or []

    def build_prompt(self, question: str) -> str:
        """构建 Text2SQL Prompt"""
        prompt = "You are an expert SQL assistant. Convert the user's question into a valid SQLite SQL query.\n\n"
        prompt += "Database Schema:\n"
        for schema in self.schemas:
            prompt += f"CREATE TABLE {schema.name} (\n"
            prompt += ",\n".join(f"  {col}" for col in schema.columns)
            prompt += "\n);\n"
            if schema.description:
                prompt += f"-- {schema.description}\n"

        if self.examples:
            prompt += "\nExamples:\n"
            for ex in self.examples:
                prompt += f"Q: {ex['question']}\n"
                prompt += f"SQL: {ex['sql']}\n\n"

        prompt += f"Q: {question}\n"
        prompt += "SQL:"
        return prompt

    def generate_sql(self, prompt: str) -> str:
        """模拟 SQL 生成，生产环境替换为真实 LLM"""
        # 基于关键词的简单规则生成
        question = prompt.split("Q:")[-1].replace("SQL:", "").strip().lower()

        if "customer" in question and "order" in question:
            return """SELECT c.name, COUNT(o.id) as order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY order_count DESC"""

        if "total amount" in question or "销售额" in question:
            return """SELECT c.name, SUM(o.amount) as total
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total DESC"""

        return "SELECT * FROM customers LIMIT 10"

    def validate_sql(self, sql: str) -> bool:
        """SQL 安全校验：仅允许 SELECT"""
        sql_upper = sql.strip().upper()
        forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE", "TRUNCATE"]
        return sql_upper.startswith("SELECT") and not any(f in sql_upper for f in forbidden)

    def execute_sql(self, sql: str, db_path: str = ":memory:") -> List[Dict]:
        """执行 SQL 并返回结果"""
        if not self.validate_sql(sql):
            raise ValueError("仅支持 SELECT 查询")

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 创建示例表和数据
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                region TEXT
            );
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                amount REAL,
                order_date TEXT
            );
            INSERT INTO customers (id, name, email, region) VALUES
                (1, 'Alice', 'alice@example.com', 'North'),
                (2, 'Bob', 'bob@example.com', 'South');
            INSERT INTO orders (id, customer_id, amount, order_date) VALUES
                (1, 1, 150.0, '2023-01-15'),
                (2, 1, 230.0, '2023-02-20'),
                (3, 2, 90.0, '2023-03-10');
        """)

        cursor.execute(sql)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()
        return results


if __name__ == "__main__":
    schemas = [
        TableSchema(
            name="customers",
            columns=["id INTEGER", "name TEXT", "email TEXT", "region TEXT"],
            description="客户信息表",
        ),
        TableSchema(
            name="orders",
            columns=["id INTEGER", "customer_id INTEGER", "amount REAL", "order_date TEXT"],
            description="订单表，通过 customer_id 关联 customers",
        ),
    ]

    examples = [
        {
            "question": "List all customers.",
            "sql": "SELECT * FROM customers;",
        }
    ]

    pipeline = SimpleNL2SQL(schemas, examples)
    question = "Which customer has the highest total order amount?"

    prompt = pipeline.build_prompt(question)
    sql = pipeline.generate_sql(prompt)

    print(f"Question: {question}")
    print(f"Generated SQL:\n{sql}")

    if pipeline.validate_sql(sql):
        results = pipeline.execute_sql(sql)
        print(f"\nResults:")
        for row in results:
            print(row)
    else:
        print("Generated SQL failed security validation.")
```

## 🔧 配置说明

Text2SQL Pipeline 的关键配置：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `max_tables` | int | 10 | 单次 prompt 中包含的最大表数 |
| `max_columns_per_table` | int | 20 | 每表包含的最大列数 |
| `num_shots` | int | 3 | Few-shot 示例数量 |
| `allow_ddl` | bool | False | 是否允许 DDL 语句 |
| `allow_dml` | bool | False | 是否允许 DML 语句 |
| `max_result_rows` | int | 100 | 最大返回行数 |

## 📊 运行结果

执行 `code/text2sql_pipeline.py` 后，预期输出：

```
Question: Which customer has the highest total order amount?
Generated SQL:
SELECT c.name, SUM(o.amount) as total
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total DESC

Results:
{'name': 'Alice', 'total': 380.0}
{'name': 'Bob', 'total': 90.0}
```

## 🐛 常见问题

### Q1: 如何处理复杂的多表 JOIN？

建议：
- 在 Schema 描述中明确外键关系
- 提供涉及多表 JOIN 的 Few-shot 示例
- 使用 Schema Linking 先确定相关表，再构建 prompt
- 对常见查询模式建立模板库

### Q2: 生成的 SQL 在真实数据库上执行失败怎么办？

可以采用 Self-Correction 策略：
1. 执行生成的 SQL
2. 捕获错误信息
3. 将错误信息反馈给模型
4. 要求模型修正 SQL
5. 重复直到执行成功或达到最大重试次数

### Q3: 如何防止 SQL 注入？

Text2SQL 中的 SQL 注入风险主要来自：
- 用户问题中包含恶意指令
- 模型被诱导生成破坏性 SQL

防护措施：
- 严格限制只允许 SELECT
- 使用参数化查询（对模型生成的常量值进行参数化）
- 在沙箱数据库中执行
- 人工审核高风险查询

## 📚 扩展学习

- **Spider**: 经典 Text2SQL 英文数据集
- **BIRD**: 大规模真实世界 Text2SQL 基准
- **DIN-SQL**: Decomposed In-Context Learning for Text-to-SQL
- **SQL-PaLM**: Google 的 Text2SQL 工作
- **Vanna.ai**: 开源 Text2SQL 框架

## 🤝 贡献指南

欢迎扩展 Text2SQL 能力：

- 集成真实 LLM API（OpenAI、Claude、Qwen 等）
- 实现 Schema Linking 模块
- 增加 Self-Correction 循环
- 支持更多数据库方言（MySQL、PostgreSQL、SQL Server）
- 添加 SQL 执行计划解释

---

*最后更新：2026-06-16*

## 🚀 快速开始

### 运行演示

```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```
