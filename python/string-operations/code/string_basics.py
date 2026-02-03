#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python字符串基础操作演示
展示字符串的创建、索引、切片、常用方法
"""

def demo_string_creation():
    """字符串创建方式"""
    print("=" * 50)
    print("1. 字符串创建方式")
    print("=" * 50)
    
    # 单引号和双引号
    s1 = 'Hello'
    s2 = "World"
    print(f"单引号: {s1}")
    print(f"双引号: {s2}")
    
    # 三引号多行字符串
    s3 = """这是
多行
字符串"""
    print(f"多行字符串:\n{s3}")
    
    # 原始字符串(不转义)
    s4 = r"C:\Users\test\file.txt"
    print(f"原始字符串: {s4}")
    
    # f-string格式化
    name = "Python"
    version = 3.11
    s5 = f"{name} version {version}"
    print(f"f-string: {s5}")


def demo_string_indexing():
    """字符串索引和切片"""
    print("\n" + "=" * 50)
    print("2. 字符串索引和切片")
    print("=" * 50)
    
    s = "Hello Python"
    print(f"原字符串: '{s}'")
    
    # 索引
    print(f"第一个字符 s[0]: '{s[0]}'")
    print(f"最后一个字符 s[-1]: '{s[-1]}'")
    
    # 切片 [start:end:step]
    print(f"前5个字符 s[:5]: '{s[:5]}'")
    print(f"从第6个开始 s[6:]: '{s[6:]}'")
    print(f"中间部分 s[2:8]: '{s[2:8]}'")
    print(f"隔一个取一个 s[::2]: '{s[::2]}'")
    print(f"反转字符串 s[::-1]: '{s[::-1]}'")


def demo_string_methods():
    """字符串常用方法"""
    print("\n" + "=" * 50)
    print("3. 字符串常用方法")
    print("=" * 50)
    
    s = "  Hello World  "
    print(f"原字符串: '{s}'")
    
    # 大小写转换
    print(f"upper(): '{s.upper()}'")
    print(f"lower(): '{s.lower()}'")
    print(f"title(): '{s.title()}'")
    print(f"capitalize(): '{s.capitalize()}'")
    
    # 去除空白
    print(f"strip(): '{s.strip()}'")
    print(f"lstrip(): '{s.lstrip()}'")
    print(f"rstrip(): '{s.rstrip()}'")
    
    # 查找和替换
    s2 = "Hello World"
    print(f"\n查找和替换 ('{s2}'):")
    print(f"find('World'): {s2.find('World')}")
    print(f"find('Python'): {s2.find('Python')}")  # 找不到返回-1
    print(f"replace('World', 'Python'): '{s2.replace('World', 'Python')}'")
    print(f"count('l'): {s2.count('l')}")
    
    # 判断方法
    print(f"\n判断方法:")
    print(f"'Hello'.startswith('He'): {'Hello'.startswith('He')}")
    print(f"'Hello'.endswith('lo'): {'Hello'.endswith('lo')}")
    print(f"'12345'.isdigit(): {'12345'.isdigit()}")
    print(f"'Hello'.isalpha(): {'Hello'.isalpha()}")
    print(f"'Hello123'.isalnum(): {'Hello123'.isalnum()}")


def demo_string_split_join():
    """字符串分割和连接"""
    print("\n" + "=" * 50)
    print("4. 字符串分割和连接")
    print("=" * 50)
    
    # split分割
    s = "apple,banana,orange,grape"
    fruits = s.split(',')
    print(f"原字符串: '{s}'")
    print(f"split(','): {fruits}")
    
    # 限制分割次数
    print(f"split(',', 2): {s.split(',', 2)}")
    
    # splitlines分割行
    text = "line1\nline2\nline3"
    print(f"splitlines(): {text.splitlines()}")
    
    # join连接
    words = ['Hello', 'World', 'Python']
    print(f"\n列表: {words}")
    print(f"' '.join(): '{' '.join(words)}'")
    print(f"'-'.join(): '{'-'.join(words)}'")
    print(f"''.join(): '{''.join(words)}'")


if __name__ == "__main__":
    demo_string_creation()
    demo_string_indexing()
    demo_string_methods()
    demo_string_split_join()
    print("\n[OK] 字符串基础演示完成!")
