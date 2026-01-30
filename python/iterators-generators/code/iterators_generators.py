#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python迭代器与生成器演示
展示迭代协议、生成器函数、生成器表达式等
"""
import itertools


def demo_iterator_basics():
    """迭代器基础"""
    print("=" * 50)
    print("1. 迭代器基础")
    print("=" * 50)
    
    # 可迭代对象和迭代器
    my_list = [1, 2, 3]
    iterator = iter(my_list)
    
    print(f"列表: {my_list}")
    print(f"迭代器: {iterator}")
    print(f"next(): {next(iterator)}")
    print(f"next(): {next(iterator)}")
    print(f"next(): {next(iterator)}")
    
    # 自定义迭代器
    class CountDown:
        def __init__(self, start):
            self.start = start
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.start <= 0:
                raise StopIteration
            self.start -= 1
            return self.start + 1
    
    print(f"\n自定义迭代器 CountDown(5):")
    for num in CountDown(5):
        print(f"  {num}", end=" ")
    print()


def demo_generator_function():
    """生成器函数"""
    print("\n" + "=" * 50)
    print("2. 生成器函数")
    print("=" * 50)
    
    # 基本生成器
    def countdown(n):
        print("  倒计时开始")
        while n > 0:
            yield n
            n -= 1
        print("  倒计时结束")
    
    print("countdown(5):")
    for num in countdown(5):
        print(f"  {num}", end=" ")
    print()
    
    # 生成器是惰性求值
    def infinite_sequence():
        num = 0
        while True:
            yield num
            num += 1
    
    print("\n无限序列(取前10个):")
    gen = infinite_sequence()
    for _ in range(10):
        print(f"  {next(gen)}", end=" ")
    print()
    
    # 斐波那契数列生成器
    def fibonacci(limit):
        a, b = 0, 1
        while a < limit:
            yield a
            a, b = b, a + b
    
    print(f"\n斐波那契数列(< 100): {list(fibonacci(100))}")


def demo_generator_expression():
    """生成器表达式"""
    print("\n" + "=" * 50)
    print("3. 生成器表达式")
    print("=" * 50)
    
    # 列表推导式 vs 生成器表达式
    list_comp = [x**2 for x in range(10)]
    gen_exp = (x**2 for x in range(10))
    
    print(f"列表推导式: {list_comp}")
    print(f"生成器表达式: {gen_exp}")
    print(f"生成器转列表: {list(gen_exp)}")
    
    # 内存效率对比
    import sys
    list_size = sys.getsizeof([x**2 for x in range(1000)])
    gen_size = sys.getsizeof((x**2 for x in range(1000)))
    print(f"\n内存占用对比:")
    print(f"  列表(1000元素): {list_size} bytes")
    print(f"  生成器(1000元素): {gen_size} bytes")


def demo_yield_from():
    """yield from语法"""
    print("\n" + "=" * 50)
    print("4. yield from语法")
    print("=" * 50)
    
    def chain(*iterables):
        for iterable in iterables:
            yield from iterable
    
    result = list(chain([1, 2, 3], "abc", (4, 5, 6)))
    print(f"chain([1,2,3], 'abc', (4,5,6)): {result}")
    
    # 嵌套生成器
    def flatten(nested):
        for item in nested:
            if isinstance(item, (list, tuple)):
                yield from flatten(item)
            else:
                yield item
    
    nested = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
    print(f"\nflatten({nested}):")
    print(f"  {list(flatten(nested))}")


def demo_send_and_close():
    """生成器的send和close"""
    print("\n" + "=" * 50)
    print("5. 生成器的send和close")
    print("=" * 50)
    
    def accumulator():
        total = 0
        while True:
            value = yield total
            if value is None:
                break
            total += value
    
    acc = accumulator()
    print(f"初始化: {next(acc)}")  # 启动生成器
    print(f"send(10): {acc.send(10)}")
    print(f"send(20): {acc.send(20)}")
    print(f"send(30): {acc.send(30)}")


def demo_itertools():
    """itertools模块"""
    print("\n" + "=" * 50)
    print("6. itertools模块")
    print("=" * 50)
    
    # count - 无限计数器
    print("count(10, 2) 前5个:")
    counter = itertools.count(10, 2)
    print(f"  {[next(counter) for _ in range(5)]}")
    
    # cycle - 循环迭代
    print("\ncycle('ABC') 前8个:")
    cycler = itertools.cycle('ABC')
    print(f"  {[next(cycler) for _ in range(8)]}")
    
    # repeat - 重复
    print(f"\nrepeat('X', 5): {list(itertools.repeat('X', 5))}")
    
    # chain - 连接迭代器
    print(f"\nchain([1,2], [3,4], [5,6]): {list(itertools.chain([1,2], [3,4], [5,6]))}")
    
    # islice - 切片
    print(f"\nislice(range(100), 5, 10): {list(itertools.islice(range(100), 5, 10))}")
    
    # combinations - 组合
    print(f"\ncombinations('ABC', 2): {list(itertools.combinations('ABC', 2))}")
    
    # permutations - 排列
    print(f"\npermutations('AB', 2): {list(itertools.permutations('AB', 2))}")
    
    # groupby - 分组
    data = [('A', 1), ('A', 2), ('B', 3), ('B', 4), ('A', 5)]
    print(f"\ngroupby分组 (需先排序):")
    sorted_data = sorted(data, key=lambda x: x[0])
    for key, group in itertools.groupby(sorted_data, key=lambda x: x[0]):
        print(f"  {key}: {list(group)}")


if __name__ == "__main__":
    demo_iterator_basics()
    demo_generator_function()
    demo_generator_expression()
    demo_yield_from()
    demo_send_and_close()
    demo_itertools()
    print("\n[OK] 迭代器与生成器演示完成!")
