#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python SQLite数据库操作演示
展示sqlite3模块的常用功能
"""
import sqlite3
import tempfile
import os


def demo_connection():
    """数据库连接"""
    print("=" * 50)
    print("1. 数据库连接")
    print("=" * 50)
    
    # 内存数据库
    conn = sqlite3.connect(':memory:')
    print(f"内存数据库连接: {conn}")
    conn.close()
    
    # 文件数据库
    temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    temp_db.close()
    
    conn = sqlite3.connect(temp_db.name)
    print(f"文件数据库: {temp_db.name}")
    conn.close()
    
    os.unlink(temp_db.name)
    
    # 使用上下文管理器
    print("\n使用上下文管理器:")
    with sqlite3.connect(':memory:') as conn:
        print(f"  连接有效: {conn is not None}")
    print("  自动关闭连接")


def demo_create_table():
    """创建表"""
    print("\n" + "=" * 50)
    print("2. 创建表")
    print("=" * 50)
    
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX idx_users_email ON users(email)')
    
    print("创建表 users:")
    print("  - id: INTEGER PRIMARY KEY AUTOINCREMENT")
    print("  - name: TEXT NOT NULL")
    print("  - email: TEXT UNIQUE")
    print("  - age: INTEGER")
    print("  - created_at: TIMESTAMP")
    
    conn.close()
    return conn


def demo_crud_operations():
    """CRUD操作"""
    print("\n" + "=" * 50)
    print("3. CRUD操作")
    print("=" * 50)
    
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL,
            quantity INTEGER DEFAULT 0
        )
    ''')
    
    # INSERT - 插入
    print("\nINSERT插入:")
    cursor.execute(
        "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
        ("Apple", 1.5, 100)
    )
    print(f"  插入1条, lastrowid: {cursor.lastrowid}")
    
    # 批量插入
    products = [
        ("Banana", 0.8, 150),
        ("Orange", 2.0, 80),
        ("Grape", 3.5, 50),
    ]
    cursor.executemany(
        "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
        products
    )
    print(f"  批量插入{len(products)}条")
    conn.commit()
    
    # SELECT - 查询
    print("\nSELECT查询:")
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    for row in rows:
        print(f"  {row}")
    
    # 条件查询
    print("\n条件查询 (price > 1.0):")
    cursor.execute("SELECT name, price FROM products WHERE price > ?", (1.0,))
    for row in cursor.fetchall():
        print(f"  {row}")
    
    # UPDATE - 更新
    print("\nUPDATE更新:")
    cursor.execute("UPDATE products SET price = ? WHERE name = ?", (1.8, "Apple"))
    print(f"  更新{cursor.rowcount}条记录")
    conn.commit()
    
    # DELETE - 删除
    print("\nDELETE删除:")
    cursor.execute("DELETE FROM products WHERE quantity < ?", (60,))
    print(f"  删除{cursor.rowcount}条记录")
    conn.commit()
    
    # 验证结果
    print("\n最终数据:")
    cursor.execute("SELECT * FROM products")
    for row in cursor.fetchall():
        print(f"  {row}")
    
    conn.close()


def demo_row_factory():
    """行工厂"""
    print("\n" + "=" * 50)
    print("4. 行工厂")
    print("=" * 50)
    
    conn = sqlite3.connect(':memory:')
    
    # 创建表并插入数据
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT, age INTEGER)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice', 25)")
    conn.execute("INSERT INTO users VALUES (2, 'Bob', 30)")
    
    # 默认返回元组
    print("默认(元组):")
    cursor = conn.execute("SELECT * FROM users")
    for row in cursor:
        print(f"  {row}, 访问: row[1] = {row[1]}")
    
    # 使用Row工厂
    print("\nRow工厂(可按名访问):")
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT * FROM users")
    for row in cursor:
        print(f"  {dict(row)}, 访问: row['name'] = {row['name']}")
    
    conn.close()


def demo_transactions():
    """事务处理"""
    print("\n" + "=" * 50)
    print("5. 事务处理")
    print("=" * 50)
    
    conn = sqlite3.connect(':memory:')
    conn.execute("CREATE TABLE accounts (id INTEGER, balance REAL)")
    conn.execute("INSERT INTO accounts VALUES (1, 1000)")
    conn.execute("INSERT INTO accounts VALUES (2, 500)")
    conn.commit()
    
    def transfer(conn, from_id, to_id, amount):
        """转账操作"""
        try:
            cursor = conn.cursor()
            
            # 检查余额
            cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
            balance = cursor.fetchone()[0]
            
            if balance < amount:
                raise ValueError("余额不足")
            
            # 扣款
            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, from_id)
            )
            
            # 入账
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_id)
            )
            
            conn.commit()
            print(f"  转账成功: {from_id} -> {to_id}, 金额: {amount}")
            
        except Exception as e:
            conn.rollback()
            print(f"  转账失败并回滚: {e}")
    
    print("转账演示:")
    print("  初始余额:", end=" ")
    for row in conn.execute("SELECT * FROM accounts"):
        print(f"账户{row[0]}:{row[1]}", end=" ")
    print()
    
    transfer(conn, 1, 2, 200)  # 成功
    transfer(conn, 1, 2, 2000)  # 失败(余额不足)
    
    print("  最终余额:", end=" ")
    for row in conn.execute("SELECT * FROM accounts"):
        print(f"账户{row[0]}:{row[1]}", end=" ")
    print()
    
    conn.close()


def demo_aggregate_functions():
    """聚合函数"""
    print("\n" + "=" * 50)
    print("6. 聚合函数")
    print("=" * 50)
    
    conn = sqlite3.connect(':memory:')
    conn.execute("CREATE TABLE sales (product TEXT, amount REAL, date TEXT)")
    
    sales_data = [
        ("Apple", 100, "2024-01-01"),
        ("Banana", 80, "2024-01-01"),
        ("Apple", 120, "2024-01-02"),
        ("Orange", 90, "2024-01-02"),
        ("Banana", 110, "2024-01-03"),
    ]
    conn.executemany("INSERT INTO sales VALUES (?, ?, ?)", sales_data)
    
    print("聚合查询:")
    
    # COUNT
    result = conn.execute("SELECT COUNT(*) FROM sales").fetchone()
    print(f"  COUNT: {result[0]}")
    
    # SUM
    result = conn.execute("SELECT SUM(amount) FROM sales").fetchone()
    print(f"  SUM: {result[0]}")
    
    # AVG
    result = conn.execute("SELECT AVG(amount) FROM sales").fetchone()
    print(f"  AVG: {result[0]:.2f}")
    
    # MIN, MAX
    result = conn.execute("SELECT MIN(amount), MAX(amount) FROM sales").fetchone()
    print(f"  MIN: {result[0]}, MAX: {result[1]}")
    
    # GROUP BY
    print("\nGROUP BY产品:")
    cursor = conn.execute("""
        SELECT product, SUM(amount) as total, COUNT(*) as count
        FROM sales
        GROUP BY product
        ORDER BY total DESC
    """)
    for row in cursor:
        print(f"  {row[0]}: 总额={row[1]}, 次数={row[2]}")
    
    conn.close()


def demo_context_manager():
    """实用模式"""
    print("\n" + "=" * 50)
    print("7. 实用模式")
    print("=" * 50)
    
    from contextlib import contextmanager
    
    @contextmanager
    def get_db_connection(db_path=':memory:'):
        """数据库连接上下文管理器"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    print("使用自定义上下文管理器:")
    with get_db_connection() as conn:
        conn.execute("CREATE TABLE test (id INTEGER, value TEXT)")
        conn.execute("INSERT INTO test VALUES (1, 'hello')")
        row = conn.execute("SELECT * FROM test").fetchone()
        print(f"  查询结果: {dict(row)}")
    print("  连接已自动关闭")


if __name__ == "__main__":
    demo_connection()
    demo_create_table()
    demo_crud_operations()
    demo_row_factory()
    demo_transactions()
    demo_aggregate_functions()
    demo_context_manager()
    print("\n[OK] 数据库操作演示完成!")

