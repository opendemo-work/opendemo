#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 性能分析与优化完整示例
演示代码性能分析和优化技巧
"""

import time
import cProfile
import pstats
import io
from functools import lru_cache
import timeit
from typing import List
import sys


# ============ 1. 基本计时 ============
print("=" * 50)
print("1. 基本计时方法")
print("=" * 50)

def measure_time(func):
    """计时装饰器"""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"  {func.__name__}: {(end - start) * 1000:.3f} ms")
        return result
    return wrapper

@measure_time
def slow_function():
    time.sleep(0.1)
    return sum(range(10000))

result = slow_function()
print(f"  结果: {result}")


# ============ 2. timeit 模块 ============
print("\n" + "=" * 50)
print("2. timeit 精确计时")
print("=" * 50)

# 比较列表创建方式
list_comp_time = timeit.timeit(
    "[i**2 for i in range(1000)]",
    number=1000
)
map_time = timeit.timeit(
    "list(map(lambda x: x**2, range(1000)))",
    number=1000
)
loop_time = timeit.timeit(
    """
result = []
for i in range(1000):
    result.append(i**2)
""",
    number=1000
)

print(f"列表推导式: {list_comp_time:.4f}s")
print(f"map + lambda: {map_time:.4f}s")
print(f"for 循环: {loop_time:.4f}s")


# ============ 3. cProfile 性能分析 ============
print("\n" + "=" * 50)
print("3. cProfile 性能分析")
print("=" * 50)

def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def run_fibonacci():
    return fibonacci(25)

# 使用 cProfile
profiler = cProfile.Profile()
profiler.enable()
result = run_fibonacci()
profiler.disable()

# 输出统计
stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream)
stats.sort_stats('cumulative')
stats.print_stats(10)

print(f"fibonacci(25) = {result}")
print("性能分析(前10行):")
output = stream.getvalue()
for line in output.split('\n')[:15]:
    if line.strip():
        print(f"  {line}")


# ============ 4. 优化对比 ============
print("\n" + "=" * 50)
print("4. 优化对比: 斐波那契")
print("=" * 50)

# 原始递归
def fib_recursive(n: int) -> int:
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

# 缓存优化
@lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

# 迭代优化
def fib_iterative(n: int) -> int:
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# 比较性能
n = 30

start = time.perf_counter()
result1 = fib_recursive(n)
time1 = time.perf_counter() - start

fib_cached.cache_clear()
start = time.perf_counter()
result2 = fib_cached(n)
time2 = time.perf_counter() - start

start = time.perf_counter()
result3 = fib_iterative(n)
time3 = time.perf_counter() - start

print(f"n = {n}")
print(f"递归: {time1:.6f}s (结果: {result1})")
print(f"缓存: {time2:.6f}s (结果: {result2})")
print(f"迭代: {time3:.6f}s (结果: {result3})")
print(f"缓存比递归快: {time1/time2:.0f}x")


# ============ 5. 内存分析 ============
print("\n" + "=" * 50)
print("5. 内存使用分析")
print("=" * 50)

def get_size(obj, seen=None):
    """递归计算对象大小"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

# 比较不同数据结构
list_data = list(range(1000))
tuple_data = tuple(range(1000))
set_data = set(range(1000))
dict_data = {i: i for i in range(1000)}

print(f"list (1000元素): {sys.getsizeof(list_data):,} bytes")
print(f"tuple (1000元素): {sys.getsizeof(tuple_data):,} bytes")
print(f"set (1000元素): {sys.getsizeof(set_data):,} bytes")
print(f"dict (1000元素): {sys.getsizeof(dict_data):,} bytes")


# ============ 6. 生成器节省内存 ============
print("\n" + "=" * 50)
print("6. 生成器 vs 列表内存对比")
print("=" * 50)

# 列表
list_squares = [x**2 for x in range(10000)]
list_size = sys.getsizeof(list_squares)

# 生成器
gen_squares = (x**2 for x in range(10000))
gen_size = sys.getsizeof(gen_squares)

print(f"列表大小: {list_size:,} bytes")
print(f"生成器大小: {gen_size:,} bytes")
print(f"内存节省: {list_size/gen_size:.0f}x")


# ============ 7. 字符串操作优化 ============
print("\n" + "=" * 50)
print("7. 字符串操作优化")
print("=" * 50)

n = 10000

# 字符串拼接 (慢)
start = time.perf_counter()
s = ""
for i in range(n):
    s += str(i)
concat_time = time.perf_counter() - start

# join (快)
start = time.perf_counter()
s = "".join(str(i) for i in range(n))
join_time = time.perf_counter() - start

print(f"字符串拼接: {concat_time:.4f}s")
print(f"join方法: {join_time:.4f}s")
print(f"join 快: {concat_time/join_time:.1f}x")


# ============ 8. 查找优化 ============
print("\n" + "=" * 50)
print("8. 查找操作优化")
print("=" * 50)

n = 100000
data_list = list(range(n))
data_set = set(range(n))
data_dict = {i: i for i in range(n)}

search_values = [n-1, n//2, n+1]  # 最后,中间,不存在

print("查找100000个元素中的值:")
for val in search_values:
    # list
    start = time.perf_counter()
    _ = val in data_list
    list_time = time.perf_counter() - start
    
    # set
    start = time.perf_counter()
    _ = val in data_set
    set_time = time.perf_counter() - start
    
    # dict
    start = time.perf_counter()
    _ = val in data_dict
    dict_time = time.perf_counter() - start
    
    print(f"  {val}: list={list_time*1000:.3f}ms, set={set_time*1000:.6f}ms, dict={dict_time*1000:.6f}ms")


# ============ 9. 局部变量优化 ============
print("\n" + "=" * 50)
print("9. 局部变量优化")
print("=" * 50)

import math

def global_access():
    result = 0
    for i in range(10000):
        result += math.sqrt(i)  # 每次访问全局
    return result

def local_access():
    sqrt = math.sqrt  # 局部变量
    result = 0
    for i in range(10000):
        result += sqrt(i)
    return result

global_time = timeit.timeit(global_access, number=100)
local_time = timeit.timeit(local_access, number=100)

print(f"全局访问: {global_time:.4f}s")
print(f"局部变量: {local_time:.4f}s")
print(f"优化效果: {(1 - local_time/global_time) * 100:.1f}%")


# ============ 10. 实用优化技巧 ============
print("\n" + "=" * 50)
print("10. 优化技巧总结")
print("=" * 50)

print("""
数据结构选择:
- 查找多 -> set/dict (O(1))
- 有序遍历 -> list
- 不可变 -> tuple
- 去重 -> set

代码优化:
- 字符串拼接用 join()
- 全局变量改局部变量
- 列表推导式优于循环
- 使用 @lru_cache 缓存

内存优化:
- 大数据用生成器
- 使用 __slots__
- 及时释放大对象

分析工具:
- timeit: 微基准测试
- cProfile: CPU分析
- memory_profiler: 内存分析
- line_profiler: 逐行分析
- py-spy: 采样分析器

常见陷阱:
- 过早优化
- 优化错误的地方
- 牺牲可读性
- 忽略算法复杂度
""")


# ============ 11. slots 优化 ============
print("\n" + "=" * 50)
print("11. __slots__ 内存优化")
print("=" * 50)

class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

regular = RegularPoint(1, 2)
slotted = SlottedPoint(1, 2)

print(f"普通类实例大小: {sys.getsizeof(regular) + sys.getsizeof(regular.__dict__)} bytes")
print(f"__slots__类实例大小: {sys.getsizeof(slotted)} bytes")

# 创建大量对象比较
import gc
gc.collect()

regular_list = [RegularPoint(i, i) for i in range(10000)]
regular_mem = sum(sys.getsizeof(p) + sys.getsizeof(p.__dict__) for p in regular_list)

slotted_list = [SlottedPoint(i, i) for i in range(10000)]
slotted_mem = sum(sys.getsizeof(p) for p in slotted_list)

print(f"10000个普通对象: {regular_mem:,} bytes")
print(f"10000个slots对象: {slotted_mem:,} bytes")
print(f"内存节省: {(1 - slotted_mem/regular_mem) * 100:.1f}%")
