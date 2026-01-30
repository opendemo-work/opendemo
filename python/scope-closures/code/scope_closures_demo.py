#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 作用域与闭包完整示例
演示 LEGB 作用域规则和闭包机制
"""


# ============ 1. LEGB 作用域规则 ============
print("=" * 50)
print("1. LEGB 作用域规则")
print("=" * 50)

# L - Local (局部作用域)
# E - Enclosing (嵌套作用域)
# G - Global (全局作用域)
# B - Built-in (内置作用域)

# 全局变量
global_var = "我是全局变量"

def outer_function():
    # 嵌套作用域变量
    enclosing_var = "我是嵌套作用域变量"
    
    def inner_function():
        # 局部变量
        local_var = "我是局部变量"
        # 内置作用域
        builtin_example = len([1, 2, 3])
        
        print(f"  Local: {local_var}")
        print(f"  Enclosing: {enclosing_var}")
        print(f"  Global: {global_var}")
        print(f"  Built-in (len): {builtin_example}")
    
    inner_function()

outer_function()


# ============ 2. global 关键字 ============
print("\n" + "=" * 50)
print("2. global 关键字")
print("=" * 50)

counter = 0

def increment_wrong():
    """错误方式 - 创建新的局部变量"""
    # counter = counter + 1  # UnboundLocalError
    pass

def increment_correct():
    """正确方式 - 使用 global"""
    global counter
    counter += 1

print(f"初始 counter: {counter}")
increment_correct()
increment_correct()
print(f"调用两次后: {counter}")


# ============ 3. nonlocal 关键字 ============
print("\n" + "=" * 50)
print("3. nonlocal 关键字")
print("=" * 50)

def make_counter():
    """闭包计数器"""
    count = 0
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    return increment

counter1 = make_counter()
counter2 = make_counter()

print(f"counter1: {counter1()}, {counter1()}, {counter1()}")
print(f"counter2: {counter2()}, {counter2()}")
print(f"counter1 独立: {counter1()}")


# ============ 4. 闭包基础 ============
print("\n" + "=" * 50)
print("4. 闭包基础")
print("=" * 50)

def make_multiplier(factor):
    """创建乘法器闭包"""
    def multiplier(x):
        return x * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")

# 查看闭包变量
print(f"double 的闭包变量: {double.__closure__}")
print(f"闭包中的值: {double.__closure__[0].cell_contents}")


# ============ 5. 闭包实用示例 ============
print("\n" + "=" * 50)
print("5. 闭包实用示例")
print("=" * 50)

# 示例1: 带记忆的函数
def make_averager():
    """移动平均计算器"""
    values = []
    
    def averager(new_value):
        values.append(new_value)
        return sum(values) / len(values)
    
    return averager

avg = make_averager()
print(f"平均值: {avg(10):.2f}")
print(f"平均值: {avg(20):.2f}")
print(f"平均值: {avg(30):.2f}")

# 示例2: 配置工厂
def make_formatter(prefix, suffix=""):
    """格式化器工厂"""
    def formatter(text):
        return f"{prefix}{text}{suffix}"
    return formatter

html_bold = make_formatter("<b>", "</b>")
markdown_code = make_formatter("`", "`")

print(f"HTML: {html_bold('Hello')}")
print(f"Markdown: {markdown_code('code')}")


# ============ 6. 闭包陷阱 ============
print("\n" + "=" * 50)
print("6. 闭包陷阱与解决")
print("=" * 50)

# 陷阱: 循环中的闭包
print("陷阱 - 所有函数共享最后的值:")
functions_wrong = []
for i in range(3):
    functions_wrong.append(lambda: i)

print(f"  [f() for f in functions_wrong] = {[f() for f in functions_wrong]}")

# 解决方案1: 默认参数
print("\n解决方案1 - 默认参数:")
functions_fixed1 = []
for i in range(3):
    functions_fixed1.append(lambda x=i: x)

print(f"  [f() for f in functions_fixed1] = {[f() for f in functions_fixed1]}")

# 解决方案2: 使用工厂函数
print("\n解决方案2 - 工厂函数:")
def make_printer(value):
    return lambda: value

functions_fixed2 = [make_printer(i) for i in range(3)]
print(f"  [f() for f in functions_fixed2] = {[f() for f in functions_fixed2]}")


# ============ 7. 变量查找顺序 ============
print("\n" + "=" * 50)
print("7. 变量查找顺序演示")
print("=" * 50)

x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(f"  inner: x = {x}")
    
    def inner_no_local():
        print(f"  inner_no_local: x = {x}")
    
    inner()
    inner_no_local()
    print(f"  outer: x = {x}")

outer()
print(f"global: x = {x}")


# ============ 8. 自由变量检测 ============
print("\n" + "=" * 50)
print("8. 自由变量检测")
print("=" * 50)

def make_adder(n):
    def adder(x):
        return x + n
    return adder

add_5 = make_adder(5)

print(f"函数名: {add_5.__name__}")
print(f"自由变量: {add_5.__code__.co_freevars}")
print(f"闭包: {add_5.__closure__}")
print(f"闭包值: {[cell.cell_contents for cell in add_5.__closure__]}")


# ============ 9. 装饰器与闭包 ============
print("\n" + "=" * 50)
print("9. 装饰器与闭包")
print("=" * 50)

from functools import wraps

def trace(func):
    """跟踪装饰器 - 利用闭包保存函数"""
    call_count = 0
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        print(f"  调用 {func.__name__}, 第 {call_count} 次")
        return func(*args, **kwargs)
    
    wrapper.get_count = lambda: call_count
    return wrapper

@trace
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
print(greet("Bob"))
print(f"总调用次数: {greet.get_count()}")


# ============ 10. 实际应用: 缓存闭包 ============
print("\n" + "=" * 50)
print("10. 实际应用: 缓存闭包")
print("=" * 50)

def memoize(func):
    """记忆化装饰器"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
            print(f"  计算 {func.__name__}{args}")
        else:
            print(f"  缓存 {func.__name__}{args}")
        return cache[args]
    
    wrapper.cache = cache
    wrapper.clear_cache = lambda: cache.clear()
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"fibonacci(5) = {fibonacci(5)}")
print(f"fibonacci(3) = {fibonacci(3)}")  # 使用缓存
print(f"缓存内容: {fibonacci.cache}")


print("\n" + "=" * 50)
print("所有作用域与闭包示例完成!")
print("=" * 50)
