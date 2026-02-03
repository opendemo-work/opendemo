#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python函数与装饰器演示
展示函数定义、参数、lambda、闭包、装饰器等
"""
import functools
import time


def demo_function_basics():
    """函数基础"""
    print("=" * 50)
    print("1. 函数基础")
    print("=" * 50)
    
    # 基本函数
    def greet(name):
        """问候函数"""
        return f"Hello, {name}!"
    
    print(f"greet('Alice'): {greet('Alice')}")
    print(f"函数文档: {greet.__doc__}")
    
    # 多返回值
    def get_stats(numbers):
        return min(numbers), max(numbers), sum(numbers) / len(numbers)
    
    nums = [1, 2, 3, 4, 5]
    min_val, max_val, avg_val = get_stats(nums)
    print(f"get_stats({nums}): 最小={min_val}, 最大={max_val}, 平均={avg_val}")


def demo_function_parameters():
    """函数参数类型"""
    print("\n" + "=" * 50)
    print("2. 函数参数类型")
    print("=" * 50)
    
    # 默认参数
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"
    
    print(f"默认参数: {greet('Alice')}")
    print(f"指定参数: {greet('Bob', 'Hi')}")
    
    # 关键字参数
    def person_info(name, age, city):
        return f"{name}, {age}岁, 来自{city}"
    
    print(f"关键字参数: {person_info(age=25, city='Beijing', name='Alice')}")
    
    # *args可变位置参数
    def sum_all(*args):
        return sum(args)
    
    print(f"*args: sum_all(1,2,3,4,5) = {sum_all(1, 2, 3, 4, 5)}")
    
    # **kwargs可变关键字参数
    def print_info(**kwargs):
        return ", ".join(f"{k}={v}" for k, v in kwargs.items())
    
    print(f"**kwargs: {print_info(name='Alice', age=25, city='Beijing')}")
    
    # 混合使用
    def mixed_params(a, b, *args, name="default", **kwargs):
        return f"a={a}, b={b}, args={args}, name={name}, kwargs={kwargs}"
    
    result = mixed_params(1, 2, 3, 4, name="test", x=10, y=20)
    print(f"混合参数: {result}")


def demo_lambda():
    """Lambda表达式"""
    print("\n" + "=" * 50)
    print("3. Lambda表达式")
    print("=" * 50)
    
    # 基本lambda
    square = lambda x: x ** 2
    print(f"square(5): {square(5)}")
    
    add = lambda x, y: x + y
    print(f"add(3, 4): {add(3, 4)}")
    
    # 配合内置函数使用
    nums = [1, 2, 3, 4, 5]
    squared = list(map(lambda x: x**2, nums))
    print(f"map(lambda x: x**2, {nums}): {squared}")
    
    evens = list(filter(lambda x: x % 2 == 0, nums))
    print(f"filter偶数: {evens}")
    
    # 排序
    students = [('Alice', 85), ('Bob', 92), ('Charlie', 78)]
    sorted_students = sorted(students, key=lambda x: x[1], reverse=True)
    print(f"按分数排序: {sorted_students}")


def demo_closure():
    """闭包"""
    print("\n" + "=" * 50)
    print("4. 闭包")
    print("=" * 50)
    
    # 计数器闭包
    def make_counter():
        count = 0
        def counter():
            nonlocal count
            count += 1
            return count
        return counter
    
    counter1 = make_counter()
    counter2 = make_counter()
    print(f"counter1: {counter1()}, {counter1()}, {counter1()}")
    print(f"counter2: {counter2()}, {counter2()}")
    
    # 乘法器闭包
    def make_multiplier(n):
        def multiplier(x):
            return x * n
        return multiplier
    
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"double(5): {double(5)}")
    print(f"triple(5): {triple(5)}")


def demo_decorators():
    """装饰器"""
    print("\n" + "=" * 50)
    print("5. 装饰器")
    print("=" * 50)
    
    # 基本装饰器
    def log_call(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  调用 {func.__name__}({args}, {kwargs})")
            result = func(*args, **kwargs)
            print(f"  返回 {result}")
            return result
        return wrapper
    
    @log_call
    def add(a, b):
        return a + b
    
    print("基本装饰器:")
    add(3, 5)
    
    # 计时装饰器
    def timer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"  {func.__name__} 执行时间: {end - start:.6f}秒")
            return result
        return wrapper
    
    @timer
    def slow_function():
        time.sleep(0.1)
        return "done"
    
    print("\n计时装饰器:")
    slow_function()
    
    # 带参数的装饰器
    def repeat(times):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for _ in range(times):
                    result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator
    
    @repeat(3)
    def say_hello():
        print("  Hello!")
        return "done"
    
    print("\n带参数装饰器 @repeat(3):")
    say_hello()


def demo_higher_order():
    """高阶函数"""
    print("\n" + "=" * 50)
    print("6. 高阶函数")
    print("=" * 50)
    
    nums = [1, 2, 3, 4, 5]
    
    # map
    squared = list(map(lambda x: x**2, nums))
    print(f"map: {nums} -> {squared}")
    
    # filter
    evens = list(filter(lambda x: x % 2 == 0, nums))
    print(f"filter偶数: {nums} -> {evens}")
    
    # reduce
    from functools import reduce
    product = reduce(lambda x, y: x * y, nums)
    print(f"reduce乘积: {nums} -> {product}")
    
    # sorted
    words = ['banana', 'apple', 'cherry', 'date']
    sorted_by_len = sorted(words, key=len)
    print(f"sorted按长度: {words} -> {sorted_by_len}")


if __name__ == "__main__":
    demo_function_basics()
    demo_function_parameters()
    demo_lambda()
    demo_closure()
    demo_decorators()
    demo_higher_order()
    print("\n[OK] 函数与装饰器演示完成!")
