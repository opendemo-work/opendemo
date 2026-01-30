#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Lambda表达式与函数式编程完整示例
演示匿名函数、高阶函数和函数式编程技巧
"""

from functools import reduce, partial, wraps
from typing import List, Callable, Any
from operator import add, mul, itemgetter, attrgetter


# ============ 1. Lambda基础 ============
print("=" * 50)
print("1. Lambda基础语法")
print("=" * 50)

# 基本语法: lambda 参数: 表达式
square = lambda x: x ** 2
add_two = lambda x, y: x + y
greet = lambda name: f"Hello, {name}!"

print(f"square(5) = {square(5)}")
print(f"add_two(3, 4) = {add_two(3, 4)}")
print(f"greet('Python') = {greet('Python')}")

# 无参数lambda
get_pi = lambda: 3.14159
print(f"get_pi() = {get_pi()}")

# 带默认参数
power = lambda x, n=2: x ** n
print(f"power(3) = {power(3)}")
print(f"power(3, 3) = {power(3, 3)}")


# ============ 2. Lambda与内置函数 ============
print("\n" + "=" * 50)
print("2. Lambda与内置函数结合")
print("=" * 50)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map: 对每个元素应用函数
squares = list(map(lambda x: x ** 2, numbers))
print(f"平方: {squares}")

# filter: 筛选满足条件的元素
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数: {evens}")

# reduce: 累积操作
from functools import reduce
total = reduce(lambda acc, x: acc + x, numbers, 0)
product = reduce(lambda acc, x: acc * x, numbers, 1)
print(f"总和: {total}")
print(f"乘积: {product}")

# sorted: 自定义排序
words = ["apple", "Banana", "cherry", "Date"]
sorted_words = sorted(words, key=lambda s: s.lower())
print(f"忽略大小写排序: {sorted_words}")


# ============ 3. 复杂排序场景 ============
print("\n" + "=" * 50)
print("3. 复杂排序场景")
print("=" * 50)

students = [
    {"name": "Alice", "age": 22, "score": 85},
    {"name": "Bob", "age": 20, "score": 92},
    {"name": "Charlie", "age": 21, "score": 85},
    {"name": "David", "age": 20, "score": 78},
]

# 按单个字段排序
by_score = sorted(students, key=lambda s: s["score"], reverse=True)
print("按分数降序:")
for s in by_score:
    print(f"  {s['name']}: {s['score']}")

# 按多个字段排序（先分数降序，再年龄升序）
by_multi = sorted(students, key=lambda s: (-s["score"], s["age"]))
print("\n按分数降序，年龄升序:")
for s in by_multi:
    print(f"  {s['name']}: score={s['score']}, age={s['age']}")

# 使用operator模块更高效
from operator import itemgetter
by_name = sorted(students, key=itemgetter("name"))
print(f"\n按姓名排序: {[s['name'] for s in by_name]}")


# ============ 4. 列表推导式 vs map/filter ============
print("\n" + "=" * 50)
print("4. 列表推导式 vs map/filter")
print("=" * 50)

nums = range(1, 11)

# map + lambda
result1 = list(map(lambda x: x ** 2, nums))
# 列表推导式（更Pythonic）
result2 = [x ** 2 for x in nums]
print(f"map结果: {result1}")
print(f"推导式结果: {result2}")

# filter + lambda
result3 = list(filter(lambda x: x > 5, nums))
# 列表推导式
result4 = [x for x in nums if x > 5]
print(f"filter结果: {result3}")
print(f"推导式结果: {result4}")

# 组合操作
result5 = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, nums)))
result6 = [x ** 2 for x in nums if x % 2 == 0]
print(f"组合map+filter: {result5}")
print(f"组合推导式: {result6}")


# ============ 5. 闭包与Lambda ============
print("\n" + "=" * 50)
print("5. 闭包与Lambda")
print("=" * 50)

def make_multiplier(n: int) -> Callable[[int], int]:
    """创建一个乘法器"""
    return lambda x: x * n

double = make_multiplier(2)
triple = make_multiplier(3)
print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")

# 常见陷阱：循环中的lambda
print("\n循环中的lambda陷阱:")
funcs_wrong = [lambda x: x * i for i in range(3)]
print(f"错误方式: {[f(2) for f in funcs_wrong]}")  # 全是4!

# 正确方式：使用默认参数捕获值
funcs_right = [lambda x, i=i: x * i for i in range(3)]
print(f"正确方式: {[f(2) for f in funcs_right]}")  # [0, 2, 4]


# ============ 6. 高阶函数 ============
print("\n" + "=" * 50)
print("6. 高阶函数")
print("=" * 50)

def compose(*funcs: Callable) -> Callable:
    """组合多个函数"""
    def composed(x):
        for f in reversed(funcs):
            x = f(x)
        return x
    return composed

def apply_twice(f: Callable[[int], int]) -> Callable[[int], int]:
    """应用函数两次"""
    return lambda x: f(f(x))

# 函数组合
add_one = lambda x: x + 1
double = lambda x: x * 2
composed = compose(double, add_one)  # 先+1再*2
print(f"compose(double, add_one)(5) = {composed(5)}")

# 应用两次
double_twice = apply_twice(double)
print(f"apply_twice(double)(3) = {double_twice(3)}")


# ============ 7. Partial函数 ============
print("\n" + "=" * 50)
print("7. Partial函数（偏函数）")
print("=" * 50)

from functools import partial

def power(base: int, exponent: int) -> int:
    return base ** exponent

# 创建特定的幂函数
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(f"square(5) = {square(5)}")
print(f"cube(3) = {cube(3)}")

# 实际应用：固定日志前缀
def log_message(level: str, message: str):
    print(f"[{level}] {message}")

log_info = partial(log_message, "INFO")
log_error = partial(log_message, "ERROR")

log_info("Application started")
log_error("Something went wrong")


# ============ 8. 条件表达式Lambda ============
print("\n" + "=" * 50)
print("8. 条件表达式Lambda")
print("=" * 50)

# 三元表达式
abs_value = lambda x: x if x >= 0 else -x
max_val = lambda a, b: a if a > b else b
clamp = lambda x, low, high: max(low, min(x, high))

print(f"abs_value(-5) = {abs_value(-5)}")
print(f"max_val(3, 7) = {max_val(3, 7)}")
print(f"clamp(15, 0, 10) = {clamp(15, 0, 10)}")

# 分类函数
classify = lambda n: "positive" if n > 0 else ("negative" if n < 0 else "zero")
print(f"classify(5) = {classify(5)}")
print(f"classify(-3) = {classify(-3)}")
print(f"classify(0) = {classify(0)}")


# ============ 9. 实际应用场景 ============
print("\n" + "=" * 50)
print("9. 实际应用场景")
print("=" * 50)

# 9.1 数据转换管道
data = ["  hello  ", "  WORLD  ", "  Python  "]
pipeline = [
    lambda s: s.strip(),
    lambda s: s.lower(),
    lambda s: s.capitalize(),
]

def process_pipeline(data: List[str], funcs: List[Callable]) -> List[str]:
    result = data
    for func in funcs:
        result = list(map(func, result))
    return result

processed = process_pipeline(data, pipeline)
print(f"数据处理管道: {data} -> {processed}")

# 9.2 回调函数
def fetch_data(callback: Callable[[dict], None]):
    """模拟异步数据获取"""
    data = {"status": "success", "value": 42}
    callback(data)

fetch_data(lambda d: print(f"收到数据: {d}"))

# 9.3 字典操作
users = {
    "alice": {"age": 25, "city": "NYC"},
    "bob": {"age": 30, "city": "LA"},
    "charlie": {"age": 35, "city": "NYC"},
}

# 筛选NYC用户
nyc_users = {k: v for k, v in users.items() if v["city"] == "NYC"}
print(f"NYC用户: {list(nyc_users.keys())}")

# 按年龄排序
sorted_users = dict(sorted(users.items(), key=lambda x: x[1]["age"]))
print(f"按年龄排序: {list(sorted_users.keys())}")


# ============ 10. Lambda vs def ============
print("\n" + "=" * 50)
print("10. Lambda vs def 对比")
print("=" * 50)

print("""
Lambda优点:
- 简洁，适合简单的一次性函数
- 可直接作为参数传递
- 适合排序key、map、filter等场景

Lambda缺点:
- 只能包含单个表达式
- 没有函数名，调试困难
- 不支持类型注解
- 复杂逻辑难以阅读

使用建议:
1. 简单操作(一行) -> 使用lambda
2. 复杂逻辑 -> 使用def
3. 需要复用 -> 使用def
4. 排序key -> lambda或operator模块
5. 列表转换 -> 优先使用列表推导式
""")

# 对比示例
# Lambda方式
result_lambda = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, range(10))))

# 推导式方式（更Pythonic）
result_comp = [x ** 2 for x in range(10) if x % 2 == 0]

# def方式（更清晰）
def square_even_numbers(n: int) -> List[int]:
    """返回0到n-1中偶数的平方"""
    return [x ** 2 for x in range(n) if x % 2 == 0]

print(f"Lambda: {result_lambda}")
print(f"推导式: {result_comp}")
print(f"函数: {square_even_numbers(10)}")
