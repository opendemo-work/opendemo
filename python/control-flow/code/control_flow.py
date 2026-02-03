#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python控制流演示
展示条件语句、循环语句、推导式等控制流结构
"""

def demo_if_else():
    """条件语句"""
    print("=" * 50)
    print("1. 条件语句 if-elif-else")
    print("=" * 50)
    
    # 基本if-else
    age = 18
    if age >= 18:
        print(f"年龄{age}: 成年人")
    else:
        print(f"年龄{age}: 未成年")
    
    # if-elif-else
    score = 85
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'
    print(f"分数{score}: 等级{grade}")
    
    # 三元表达式
    x = 10
    result = "正数" if x > 0 else ("零" if x == 0 else "负数")
    print(f"x={x}: {result}")
    
    # 条件表达式
    a, b = 5, 10
    max_val = a if a > b else b
    print(f"a={a}, b={b}, 较大值: {max_val}")


def demo_for_loop():
    """for循环"""
    print("\n" + "=" * 50)
    print("2. for循环")
    print("=" * 50)
    
    # 遍历列表
    fruits = ['apple', 'banana', 'cherry']
    print("遍历列表:")
    for fruit in fruits:
        print(f"  {fruit}")
    
    # 遍历字符串
    print("\n遍历字符串 'Python':")
    for char in "Python":
        print(f"  {char}", end=" ")
    print()
    
    # range()
    print("\nrange(5):")
    for i in range(5):
        print(f"  {i}", end=" ")
    print()
    
    print("\nrange(2, 8, 2):")
    for i in range(2, 8, 2):
        print(f"  {i}", end=" ")
    print()
    
    # enumerate
    print("\nenumerate遍历:")
    for index, fruit in enumerate(fruits):
        print(f"  {index}: {fruit}")
    
    # zip同时遍历多个
    names = ['Alice', 'Bob', 'Charlie']
    ages = [25, 30, 35]
    print("\nzip遍历:")
    for name, age in zip(names, ages):
        print(f"  {name}: {age}岁")


def demo_while_loop():
    """while循环"""
    print("\n" + "=" * 50)
    print("3. while循环")
    print("=" * 50)
    
    # 基本while
    print("基本while (计数到5):")
    count = 1
    while count <= 5:
        print(f"  count = {count}")
        count += 1
    
    # while-else
    print("\nwhile-else (正常结束):")
    n = 3
    while n > 0:
        print(f"  n = {n}")
        n -= 1
    else:
        print("  循环正常结束!")


def demo_break_continue():
    """break和continue"""
    print("\n" + "=" * 50)
    print("4. break和continue")
    print("=" * 50)
    
    # break
    print("break (找到5就停止):")
    for i in range(10):
        if i == 5:
            print(f"  找到{i}, 停止!")
            break
        print(f"  {i}", end=" ")
    print()
    
    # continue
    print("\ncontinue (跳过偶数):")
    for i in range(10):
        if i % 2 == 0:
            continue
        print(f"  {i}", end=" ")
    print()
    
    # for-else (没有break时执行else)
    print("\nfor-else (查找元素):")
    nums = [1, 3, 5, 7, 9]
    target = 4
    for num in nums:
        if num == target:
            print(f"  找到{target}!")
            break
    else:
        print(f"  未找到{target}")


def demo_nested_loops():
    """嵌套循环"""
    print("\n" + "=" * 50)
    print("5. 嵌套循环")
    print("=" * 50)
    
    # 九九乘法表
    print("九九乘法表:")
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f"{j}x{i}={i*j:2}", end=" ")
        print()
    
    # 遍历嵌套列表
    print("\n遍历嵌套列表:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for row in matrix:
        for item in row:
            print(f"  {item}", end=" ")
        print()


def demo_match_case():
    """match-case (Python 3.10+)"""
    print("\n" + "=" * 50)
    print("6. match-case (Python 3.10+)")
    print("=" * 50)
    
    def get_day_type(day):
        match day:
            case "Saturday" | "Sunday":
                return "周末"
            case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
                return "工作日"
            case _:
                return "无效日期"
    
    days = ["Monday", "Saturday", "Unknown"]
    for day in days:
        print(f"  {day}: {get_day_type(day)}")
    
    # 模式匹配
    def process_command(command):
        match command.split():
            case ["quit"]:
                return "退出程序"
            case ["hello", name]:
                return f"你好, {name}!"
            case ["add", x, y]:
                return f"结果: {int(x) + int(y)}"
            case _:
                return "未知命令"
    
    commands = ["quit", "hello Alice", "add 3 5", "unknown"]
    print("\n模式匹配命令:")
    for cmd in commands:
        print(f"  '{cmd}' -> {process_command(cmd)}")


if __name__ == "__main__":
    demo_if_else()
    demo_for_loop()
    demo_while_loop()
    demo_break_continue()
    demo_nested_loops()
    demo_match_case()
    print("\n[OK] 控制流演示完成!")
