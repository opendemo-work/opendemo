"""
Text2SQL Pipeline 原型

本脚本演示一个端到端的自然语言转 SQL 工作流，包括：
- Schema 理解
- Prompt 构建
- SQL 生成（模拟）
- SQL 安全校验
- 在 SQLite 内存数据库中执行

注意：本示例仅使用标准库，便于在无网络环境下运行。
生产环境可将 generate_sql 替换为真实 LLM API 调用。
"""

import sqlite3
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TableSchema:
    """表结构定义

    Attributes:
        name: 表名
        columns: 列定义列表，如 ["id INTEGER", "name TEXT"]
        description: 表中文描述
    """

    name: str
    columns: List[str]
    description: str = ""


class SimpleNL2SQL:
    """简化版 Text2SQL Pipeline"""

    def __init__(
        self,
        schemas: List[TableSchema],
        examples: Optional[List[Dict[str, str]]] = None,
    ):
        """
        初始化 Text2SQL Pipeline

        Args:
            schemas: 数据库表结构列表
            examples: Few-shot 示例列表
        """
        self.schemas = schemas
        self.examples = examples or []

    def build_prompt(self, question: str) -> str:
        """构建 Text2SQL Prompt

        Args:
            question: 自然语言问题

        Returns:
            完整的 prompt 字符串
        """
        prompt = (
            "You are an expert SQL assistant. "
            "Convert the user's question into a valid SQLite SQL query.\n\n"
        )
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
        """模拟 SQL 生成

        生产环境中应替换为真实 LLM 调用。
        """
        # 从 prompt 中提取用户问题
        question_part = prompt.split("Q:")[-1].replace("SQL:", "").strip().lower()

        # 基于关键词的简单规则生成
        if "customer" in question_part and "order" in question_part:
            if "total" in question_part or "amount" in question_part or "销售额" in question_part:
                return """SELECT c.name, SUM(o.amount) as total
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total DESC"""
            if "count" in question_part or "多少" in question_part:
                return """SELECT c.name, COUNT(o.id) as order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY order_count DESC"""

        if "list all" in question_part or "所有" in question_part:
            return "SELECT * FROM customers LIMIT 10"

        return "SELECT * FROM customers LIMIT 10"

    def validate_sql(self, sql: str) -> bool:
        """SQL 安全校验：仅允许 SELECT

        Args:
            sql: 待校验的 SQL 字符串

        Returns:
            是否通过安全校验
        """
        sql_upper = sql.strip().upper()
        forbidden = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "ALTER",
            "CREATE",
            "TRUNCATE",
        ]
        return sql_upper.startswith("SELECT") and not any(
            f" {f}" in f" {sql_upper} " for f in forbidden
        )

    def execute_sql(self, sql: str, db_path: str = ":memory:") -> List[Dict[str, any]]:
        """执行 SQL 并返回结果

        Args:
            sql: 已通过校验的 SELECT 语句
            db_path: SQLite 数据库路径，默认内存数据库

        Returns:
            查询结果字典列表
        """
        if not self.validate_sql(sql):
            raise ValueError("仅支持 SELECT 查询")

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 创建示例表和数据
        cursor.executescript(
            """
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
                (2, 'Bob', 'bob@example.com', 'South'),
                (3, 'Carol', 'carol@example.com', 'East');
            INSERT INTO orders (id, customer_id, amount, order_date) VALUES
                (1, 1, 150.0, '2023-01-15'),
                (2, 1, 230.0, '2023-02-20'),
                (3, 2, 90.0, '2023-03-10'),
                (4, 3, 120.0, '2023-04-05');
        """
        )

        cursor.execute(sql)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()
        return results


def main():
    """主函数：演示 Text2SQL Pipeline"""
    schemas = [
        TableSchema(
            name="customers",
            columns=["id INTEGER", "name TEXT", "email TEXT", "region TEXT"],
            description="客户信息表",
        ),
        TableSchema(
            name="orders",
            columns=[
                "id INTEGER",
                "customer_id INTEGER",
                "amount REAL",
                "order_date TEXT",
            ],
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
        print("\nResults:")
        for row in results:
            print(row)
    else:
        print("Generated SQL failed security validation.")


if __name__ == "__main__":
    main()
