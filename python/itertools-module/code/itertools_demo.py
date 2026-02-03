#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python itertools 模块完整示例
演示迭代器工具函数
"""

from itertools import (
    # 无限迭代器
    count, cycle, repeat,
    # 终止于最短输入的迭代器
    accumulate, chain, compress, dropwhile, takewhile,
    filterfalse, groupby, islice, starmap, zip_longest,
    # 组合迭代器
    product, permutations, combinations, combinations_with_replacement
)
from operator import add, mul
from typing import Iterator


# ============ 1. 无限迭代器 ============
print("=" * 50)
print("1. 无限迭代器")
print("=" * 50)

# count: 无限计数
print("count(10, 2):", list(islice(count(10, 2), 5)))

# cycle: 无限循环
print("cycle('ABC'):", list(islice(cycle('ABC'), 7)))

# repeat: 重复
print("repeat('X', 5):", list(repeat('X', 5)))
print("repeat('Y') * 3:", list(islice(repeat('Y'), 3)))


# ============ 2. accumulate 累积 ============
print("\n" + "=" * 50)
print("2. accumulate 累积")
print("=" * 50)

# 默认累加
data = [1, 2, 3, 4, 5]
print(f"累加 {data}: {list(accumulate(data))}")

# 指定函数
print(f"累乘 {data}: {list(accumulate(data, mul))}")
print(f"累积最大值: {list(accumulate([3, 1, 4, 1, 5, 9, 2], max))}")

# 带初始值 (Python 3.8+)
print(f"带初始值0: {list(accumulate([1, 2, 3], initial=0))}")


# ============ 3. chain 链接 ============
print("\n" + "=" * 50)
print("3. chain 链接")
print("=" * 50)

# 链接多个可迭代对象
print(f"chain([1,2], [3,4], [5]): {list(chain([1, 2], [3, 4], [5]))}")

# 从可迭代对象中链接
iterables = ['ABC', 'DEF']
print(f"chain.from_iterable: {list(chain.from_iterable(iterables))}")


# ============ 4. compress 筛选 ============
print("\n" + "=" * 50)
print("4. compress 按选择器筛选")
print("=" * 50)

data = ['A', 'B', 'C', 'D', 'E']
selectors = [1, 0, 1, 0, 1]
print(f"compress({data}, {selectors}): {list(compress(data, selectors))}")


# ============ 5. dropwhile / takewhile ============
print("\n" + "=" * 50)
print("5. dropwhile / takewhile")
print("=" * 50)

data = [1, 4, 6, 4, 1, 3, 8]

# dropwhile: 丢弃直到条件为False
print(f"dropwhile(x<5, {data}): {list(dropwhile(lambda x: x < 5, data))}")

# takewhile: 获取直到条件为False
print(f"takewhile(x<5, {data}): {list(takewhile(lambda x: x < 5, data))}")


# ============ 6. filterfalse ============
print("\n" + "=" * 50)
print("6. filterfalse 过滤假值")
print("=" * 50)

data = range(10)
print(f"filterfalse(x%2, range(10)): {list(filterfalse(lambda x: x % 2, data))}")


# ============ 7. groupby 分组 ============
print("\n" + "=" * 50)
print("7. groupby 分组")
print("=" * 50)

# 注意：数据必须先排序
data = [('A', 1), ('A', 2), ('B', 3), ('B', 4), ('C', 5)]
print("按首字母分组:")
for key, group in groupby(data, lambda x: x[0]):
    print(f"  {key}: {list(group)}")

# 连续相同元素分组
chars = "AAABBBCCAAB"
print(f"\n连续字符分组 '{chars}':")
for key, group in groupby(chars):
    print(f"  {key}: {list(group)}")


# ============ 8. islice 切片 ============
print("\n" + "=" * 50)
print("8. islice 迭代器切片")
print("=" * 50)

data = range(100)
print(f"islice(range(100), 5): {list(islice(data, 5))}")
print(f"islice(range(100), 5, 10): {list(islice(data, 5, 10))}")
print(f"islice(range(100), 0, 20, 3): {list(islice(data, 0, 20, 3))}")


# ============ 9. starmap 展开参数映射 ============
print("\n" + "=" * 50)
print("9. starmap 展开参数映射")
print("=" * 50)

pairs = [(2, 3), (4, 5), (6, 7)]
print(f"starmap(pow, {pairs}): {list(starmap(pow, pairs))}")

points = [(1, 2), (3, 4), (5, 6)]
print(f"starmap(add, {points}): {list(starmap(add, points))}")


# ============ 10. zip_longest ============
print("\n" + "=" * 50)
print("10. zip_longest 最长拉链")
print("=" * 50)

a = [1, 2, 3, 4, 5]
b = ['a', 'b', 'c']

print(f"zip({a}, {b}): {list(zip(a, b))}")
print(f"zip_longest: {list(zip_longest(a, b, fillvalue='-'))}")


# ============ 11. product 笛卡尔积 ============
print("\n" + "=" * 50)
print("11. product 笛卡尔积")
print("=" * 50)

print(f"product('AB', '12'): {list(product('AB', '12'))}")
print(f"product(range(2), repeat=3): {list(product(range(2), repeat=3))}")


# ============ 12. permutations 排列 ============
print("\n" + "=" * 50)
print("12. permutations 排列")
print("=" * 50)

print(f"permutations('ABC', 2): {list(permutations('ABC', 2))}")
print(f"permutations('AB'): {list(permutations('AB'))}")


# ============ 13. combinations 组合 ============
print("\n" + "=" * 50)
print("13. combinations 组合")
print("=" * 50)

print(f"combinations('ABCD', 2): {list(combinations('ABCD', 2))}")
print(f"combinations([1,2,3], 2): {list(combinations([1, 2, 3], 2))}")


# ============ 14. combinations_with_replacement ============
print("\n" + "=" * 50)
print("14. combinations_with_replacement 可重复组合")
print("=" * 50)

print(f"combinations_with_replacement('AB', 2): {list(combinations_with_replacement('AB', 2))}")


# ============ 15. 实用示例 ============
print("\n" + "=" * 50)
print("15. 实用示例")
print("=" * 50)

# 示例1: 分批处理
def batched(iterable, n):
    """将可迭代对象分批"""
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch

data = range(10)
print(f"分批处理 range(10), batch=3:")
for batch in batched(data, 3):
    print(f"  {batch}")

# 示例2: 滑动窗口
def sliding_window(iterable, n):
    """滑动窗口"""
    it = iter(iterable)
    window = list(islice(it, n))
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window = window[1:] + [x]
        yield tuple(window)

print(f"\n滑动窗口 range(5), size=3:")
for window in sliding_window(range(5), 3):
    print(f"  {window}")

# 示例3: 扁平化嵌套
def flatten(nested):
    """扁平化嵌套可迭代对象"""
    return chain.from_iterable(nested)

nested = [[1, 2], [3, 4, 5], [6]]
print(f"\n扁平化 {nested}: {list(flatten(nested))}")


print("\n" + "=" * 50)
print("所有 itertools 示例完成!")
print("=" * 50)
