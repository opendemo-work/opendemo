"""
Text2SQL Pipeline 单元测试

使用标准库 unittest，无需额外安装 pytest 即可运行。
"""

import sys
import unittest
from pathlib import Path

# 添加 code 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from text2sql_pipeline import SimpleNL2SQL, TableSchema


class TestSimpleNL2SQL(unittest.TestCase):
    """SimpleNL2SQL 测试"""

    def setUp(self):
        self.schemas = [
            TableSchema(
                name="customers",
                columns=["id INTEGER", "name TEXT", "email TEXT"],
                description="客户表",
            ),
            TableSchema(
                name="orders",
                columns=["id INTEGER", "customer_id INTEGER", "amount REAL"],
                description="订单表",
            ),
        ]
        self.pipeline = SimpleNL2SQL(self.schemas)

    def test_build_prompt_contains_schema(self):
        """测试 prompt 包含 Schema"""
        prompt = self.pipeline.build_prompt("List all customers")
        self.assertIn("CREATE TABLE customers", prompt)
        self.assertIn("CREATE TABLE orders", prompt)

    def test_build_prompt_contains_question(self):
        """测试 prompt 包含用户问题"""
        prompt = self.pipeline.build_prompt("How many orders?")
        self.assertIn("How many orders?", prompt)

    def test_generate_sql_select_customers(self):
        """测试生成客户查询 SQL"""
        prompt = self.pipeline.build_prompt("List all customers")
        sql = self.pipeline.generate_sql(prompt)
        self.assertIn("SELECT", sql.upper())
        self.assertIn("customers", sql.lower())

    def test_generate_sql_join_and_aggregate(self):
        """测试生成 JOIN 聚合 SQL"""
        prompt = self.pipeline.build_prompt("Which customer has the highest total order amount?")
        sql = self.pipeline.generate_sql(prompt)
        self.assertIn("JOIN", sql.upper())
        self.assertIn("SUM", sql.upper())

    def test_validate_sql_allows_select(self):
        """测试允许 SELECT 语句"""
        self.assertTrue(self.pipeline.validate_sql("SELECT * FROM customers"))

    def test_validate_sql_rejects_drop(self):
        """测试拒绝 DROP 语句"""
        self.assertFalse(self.pipeline.validate_sql("DROP TABLE customers"))

    def test_validate_sql_rejects_delete(self):
        """测试拒绝 DELETE 语句"""
        self.assertFalse(self.pipeline.validate_sql("DELETE FROM customers"))

    def test_execute_sql_returns_results(self):
        """测试执行 SQL 返回结果"""
        results = self.pipeline.execute_sql("SELECT * FROM customers")
        self.assertGreater(len(results), 0)
        self.assertIn("name", results[0])

    def test_execute_sql_rejects_unsafe(self):
        """测试执行拒绝不安全 SQL"""
        with self.assertRaises(ValueError):
            self.pipeline.execute_sql("DROP TABLE customers")


if __name__ == "__main__":
    unittest.main()
