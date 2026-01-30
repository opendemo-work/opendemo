#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 推导式 (Comprehensions) 完整示例
演示列表/字典/集合/生成器推导式
"""


# ============ 1. 列表推导式基础 ============
print("=" * 50)
print("1. 列表推导式基础")
print("=" * 50)

# 基本语法: [表达式 for 变量 in 可迭代对象]
squares = [x**2 for x in range(10)]
print(f"平方数: {squares}")

# 带条件: [表达式 for 变量 in 可迭代对象 if 条件]
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(f"偶数平方: {even_squares}")

# 等价于传统循环
result = []
for x in range(10):
    if x % 2 == 0:
        result.append(x**2)
print(f"传统方式: {result}")


# ============ 2. 带表达式转换 ============
print("\n" + "=" * 50)
print("2. 表达式转换")
print("=" * 50)

# 字符串处理
words = ["hello", "WORLD", "Python"]
lower_words = [w.lower() for w in words]
upper_words = [w.upper() for w in words]
print(f"小写: {lower_words}")
print(f"大写: {upper_words}")

# 条件表达式 (三元运算)
nums = [1, -2, 3, -4, 5]
abs_nums = [x if x >= 0 else -x for x in nums]
print(f"绝对值: {abs_nums}")

# 标记正负
signs = ["正" if x > 0 else ("负" if x < 0 else "零") for x in nums]
print(f"符号: {signs}")


# ============ 3. 嵌套推导式 ============
print("\n" + "=" * 50)
print("3. 嵌套推导式")
print("=" * 50)

# 扁平化二维列表
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(f"原矩阵: {matrix}")
print(f"扁平化: {flat}")

# 矩阵转置
transposed = [[row[i] for row in matrix] for i in range(3)]
print(f"转置: {transposed}")

# 笛卡尔积
colors = ["红", "蓝"]
sizes = ["S", "M", "L"]
products = [(c, s) for c in colors for s in sizes]
print(f"笛卡尔积: {products}")


# ============ 4. 复杂条件 ============
print("\n" + "=" * 50)
print("4. 复杂条件筛选")
print("=" * 50)

# 多条件
nums = range(1, 21)
filtered = [x for x in nums if x % 2 == 0 if x % 3 == 0]  # 同时满足
print(f"能被2和3整除: {filtered}")

# 或条件 (在if中使用or)
filtered2 = [x for x in nums if x % 2 == 0 or x % 5 == 0]
print(f"能被2或5整除: {filtered2}")

# 带函数调用
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [x for x in range(2, 30) if is_prime(x)]
print(f"质数: {primes}")


# ============ 5. 字典推导式 ============
print("\n" + "=" * 50)
print("5. 字典推导式")
print("=" * 50)

# 基本语法: {键表达式: 值表达式 for 变量 in 可迭代对象}
squares_dict = {x: x**2 for x in range(6)}
print(f"平方字典: {squares_dict}")

# 从两个列表创建字典
keys = ["a", "b", "c"]
values = [1, 2, 3]
combined = {k: v for k, v in zip(keys, values)}
print(f"组合字典: {combined}")

# 反转字典
original = {"apple": 1, "banana": 2, "cherry": 3}
reversed_dict = {v: k for k, v in original.items()}
print(f"反转字典: {reversed_dict}")

# 带条件
scores = {"Alice": 85, "Bob": 72, "Charlie": 90, "David": 65}
passed = {name: score for name, score in scores.items() if score >= 75}
print(f"及格学生: {passed}")

# 转换值
grades = {name: ("A" if score >= 90 else "B" if score >= 75 else "C") 
          for name, score in scores.items()}
print(f"成绩等级: {grades}")


# ============ 6. 集合推导式 ============
print("\n" + "=" * 50)
print("6. 集合推导式")
print("=" * 50)

# 基本语法: {表达式 for 变量 in 可迭代对象}
nums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x**2 for x in nums}
print(f"唯一平方值: {unique_squares}")

# 字符串处理
text = "hello world"
unique_chars = {c for c in text if c.isalpha()}
print(f"唯一字母: {unique_chars}")

# 带条件
even_set = {x for x in range(20) if x % 2 == 0}
print(f"偶数集合: {even_set}")


# ============ 7. 生成器表达式 ============
print("\n" + "=" * 50)
print("7. 生成器表达式")
print("=" * 50)

# 语法: (表达式 for 变量 in 可迭代对象) - 圆括号!
gen = (x**2 for x in range(10))
print(f"生成器对象: {gen}")
print(f"生成器类型: {type(gen)}")

# 惰性求值 - 节省内存
import sys
list_size = sys.getsizeof([x**2 for x in range(1000)])
gen_size = sys.getsizeof((x**2 for x in range(1000)))
print(f"列表大小: {list_size} bytes")
print(f"生成器大小: {gen_size} bytes")

# 迭代生成器
gen = (x**2 for x in range(5))
print("迭代生成器:")
for val in gen:
    print(f"  {val}")

# 作为函数参数 (可省略括号)
total = sum(x**2 for x in range(10))
print(f"平方和: {total}")

max_square = max(x**2 for x in range(10))
print(f"最大平方: {max_square}")


# ============ 8. 实际应用示例 ============
print("\n" + "=" * 50)
print("8. 实际应用示例")
print("=" * 50)

# 8.1 数据清洗
raw_data = ["  Alice  ", "BOB", "  charlie", "DAVID  "]
cleaned = [name.strip().title() for name in raw_data]
print(f"清洗后: {cleaned}")

# 8.2 文件路径过滤
files = ["doc.txt", "image.png", "script.py", "data.csv", "test.py"]
python_files = [f for f in files if f.endswith(".py")]
print(f"Python文件: {python_files}")

# 8.3 JSON数据转换
users = [
    {"name": "Alice", "age": 25, "active": True},
    {"name": "Bob", "age": 30, "active": False},
    {"name": "Charlie", "age": 35, "active": True},
]
active_names = [u["name"] for u in users if u["active"]]
print(f"活跃用户: {active_names}")

# 8.4 矩阵操作
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
doubled = [[cell * 2 for cell in row] for row in matrix]
print(f"矩阵翻倍: {doubled}")

# 8.5 词频统计
text = "the quick brown fox jumps over the lazy dog"
word_lengths = {word: len(word) for word in text.split()}
print(f"词长: {word_lengths}")


# ============ 9. 性能对比 ============
print("\n" + "=" * 50)
print("9. 性能对比")
print("=" * 50)

import timeit

# 列表推导式 vs for循环
list_comp_time = timeit.timeit(
    "[x**2 for x in range(1000)]",
    number=1000
)

loop_code = """
result = []
for x in range(1000):
    result.append(x**2)
"""
loop_time = timeit.timeit(loop_code, number=1000)

map_time = timeit.timeit(
    "list(map(lambda x: x**2, range(1000)))",
    number=1000
)

print(f"列表推导式: {list_comp_time:.4f}s")
print(f"for循环: {loop_time:.4f}s")
print(f"map+lambda: {map_time:.4f}s")
print(f"推导式更快: {loop_time/list_comp_time:.2f}x")


# ============ 10. 最佳实践 ============
print("\n" + "=" * 50)
print("10. 最佳实践")
print("=" * 50)
print("""
推荐使用推导式:
- 简单的映射和过滤
- 一行可以清晰表达的逻辑
- 需要创建新列表/字典/集合

不推荐使用:
- 逻辑复杂需要多行
- 需要副作用(如print)
- 超过2层嵌套

可读性优先:
# 好
squares = [x**2 for x in range(10) if x % 2 == 0]

# 不好 - 太复杂
result = [f(x) for x in data if g(x) for y in h(x) if i(y)]

# 应该拆分
filtered = [x for x in data if g(x)]
result = [f(x) for x in filtered for y in h(x) if i(y)]
""")
