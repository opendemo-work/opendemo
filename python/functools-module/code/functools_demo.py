#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python functools 模块完整示例
演示函数式编程工具
"""

from functools import (
    reduce, partial, partialmethod, wraps,
    lru_cache, cache, cached_property,
    total_ordering, singledispatch, singledispatchmethod,
    cmp_to_key
)
from typing import Callable, Any
import time


# ============ 1. reduce 归约 ============
print("=" * 50)
print("1. reduce 归约")
print("=" * 50)

# 累加
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)
print(f"累加 {numbers}: {total}")

# 累乘
product = reduce(lambda x, y: x * y, numbers)
print(f"累乘 {numbers}: {product}")

# 带初始值
total_with_init = reduce(lambda x, y: x + y, numbers, 100)
print(f"带初始值累加: {total_with_init}")

# 找最大值
max_val = reduce(lambda x, y: x if x > y else y, [3, 1, 4, 1, 5, 9])
print(f"找最大值: {max_val}")

# 扁平化嵌套列表
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda x, y: x + y, nested)
print(f"扁平化 {nested}: {flat}")


# ============ 2. partial 偏函数 ============
print("\n" + "=" * 50)
print("2. partial 偏函数")
print("=" * 50)

def power(base, exponent):
    return base ** exponent

# 固定指数
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(f"square(5) = {square(5)}")
print(f"cube(5) = {cube(5)}")

# 固定基数
power_of_2 = partial(power, 2)
print(f"power_of_2(10) = {power_of_2(10)}")

# 格式化函数
def format_string(template, **kwargs):
    return template.format(**kwargs)

greeting = partial(format_string, "Hello, {name}! You are {age} years old.")
print(f"greeting: {greeting(name='Alice', age=25)}")


# ============ 3. partialmethod 偏方法 ============
print("\n" + "=" * 50)
print("3. partialmethod 偏方法")
print("=" * 50)

class Cell:
    def __init__(self):
        self._alive = False
    
    def set_state(self, state):
        self._alive = state
    
    # 使用 partialmethod 创建快捷方法
    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)
    
    def __repr__(self):
        return f"Cell(alive={self._alive})"

cell = Cell()
print(f"初始: {cell}")
cell.set_alive()
print(f"set_alive(): {cell}")
cell.set_dead()
print(f"set_dead(): {cell}")


# ============ 4. wraps 装饰器 ============
print("\n" + "=" * 50)
print("4. wraps 保留函数元信息")
print("=" * 50)

def timer(func):
    """计时装饰器"""
    @wraps(func)  # 保留原函数信息
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"  {func.__name__} 耗时: {(end-start)*1000:.3f}ms")
        return result
    return wrapper

@timer
def slow_add(a: int, b: int) -> int:
    """带延迟的加法"""
    time.sleep(0.01)
    return a + b

result = slow_add(1, 2)
print(f"函数名: {slow_add.__name__}")
print(f"文档: {slow_add.__doc__}")


# ============ 5. lru_cache 缓存 ============
print("\n" + "=" * 50)
print("5. lru_cache 缓存")
print("=" * 50)

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"fibonacci(30) = {fibonacci(30)}")
print(f"缓存信息: {fibonacci.cache_info()}")

# Python 3.9+ cache (无限缓存)
@cache
def factorial(n):
    return n * factorial(n - 1) if n else 1

print(f"factorial(10) = {factorial(10)}")


# ============ 6. cached_property ============
print("\n" + "=" * 50)
print("6. cached_property 缓存属性")
print("=" * 50)

class DataAnalyzer:
    def __init__(self, data):
        self.data = data
    
    @cached_property
    def statistics(self):
        """计算统计信息 (只计算一次)"""
        print("  计算统计信息...")
        return {
            'sum': sum(self.data),
            'mean': sum(self.data) / len(self.data),
            'min': min(self.data),
            'max': max(self.data)
        }

analyzer = DataAnalyzer([1, 2, 3, 4, 5])
print(f"第一次访问: {analyzer.statistics}")
print(f"第二次访问: {analyzer.statistics}")  # 不会重新计算


# ============ 7. total_ordering ============
print("\n" + "=" * 50)
print("7. total_ordering 完整比较")
print("=" * 50)

@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __eq__(self, other):
        return self.grade == other.grade
    
    def __lt__(self, other):
        return self.grade < other.grade
    
    def __repr__(self):
        return f"Student({self.name}, {self.grade})"

s1 = Student("Alice", 85)
s2 = Student("Bob", 90)
s3 = Student("Charlie", 85)

print(f"s1 < s2: {s1 < s2}")
print(f"s1 <= s2: {s1 <= s2}")
print(f"s1 > s2: {s1 > s2}")
print(f"s1 >= s2: {s1 >= s2}")
print(f"s1 == s3: {s1 == s3}")


# ============ 8. singledispatch 单分派 ============
print("\n" + "=" * 50)
print("8. singledispatch 单分派泛函数")
print("=" * 50)

@singledispatch
def process(arg):
    """默认处理"""
    return f"默认处理: {arg}"

@process.register(int)
def _(arg):
    return f"处理整数: {arg * 2}"

@process.register(str)
def _(arg):
    return f"处理字符串: {arg.upper()}"

@process.register(list)
def _(arg):
    return f"处理列表: {len(arg)} 个元素"

print(process(10))
print(process("hello"))
print(process([1, 2, 3]))
print(process(3.14))


# ============ 9. singledispatchmethod ============
print("\n" + "=" * 50)
print("9. singledispatchmethod 方法分派")
print("=" * 50)

class Formatter:
    @singledispatchmethod
    def format(self, arg):
        return str(arg)
    
    @format.register(int)
    def _(self, arg):
        return f"整数: {arg:,}"
    
    @format.register(float)
    def _(self, arg):
        return f"浮点: {arg:.2f}"
    
    @format.register(list)
    def _(self, arg):
        return f"列表[{len(arg)}]: {arg}"

fmt = Formatter()
print(fmt.format(1000000))
print(fmt.format(3.14159))
print(fmt.format([1, 2, 3]))
print(fmt.format("hello"))


# ============ 10. cmp_to_key ============
print("\n" + "=" * 50)
print("10. cmp_to_key 比较函数转换")
print("=" * 50)

def compare_length(a, b):
    """比较字符串长度"""
    return len(a) - len(b)

words = ["apple", "pie", "strawberry", "cat"]
sorted_words = sorted(words, key=cmp_to_key(compare_length))
print(f"按长度排序: {sorted_words}")

# 复杂比较
def compare_complex(a, b):
    """先按长度，再按字母"""
    if len(a) != len(b):
        return len(a) - len(b)
    if a < b:
        return -1
    elif a > b:
        return 1
    return 0

words2 = ["cat", "bat", "apple", "ant", "bear"]
sorted_words2 = sorted(words2, key=cmp_to_key(compare_complex))
print(f"复杂排序: {sorted_words2}")


print("\n" + "=" * 50)
print("所有 functools 示例完成!")
print("=" * 50)
