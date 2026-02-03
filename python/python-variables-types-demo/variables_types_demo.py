#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python变量和数据类型基础演示程序
展示Python变量声明、内置数据类型、类型转换等核心概念
"""

import sys
from typing import Any, List, Dict, Tuple
import json

def print_header(title: str) -> None:
    """打印章节标题"""
    print(f"\n{'='*50}")
    print(f"🎯 {title}")
    print(f"{'='*50}")

def demonstrate_variable_assignment() -> None:
    """演示变量赋值和命名规则"""
    print_header("变量赋值和命名规则演示")
    
    # 1. 基本变量赋值
    print("1. 基本变量赋值:")
    name = "张三"
    age = 25
    height = 175.5
    is_student = True
    
    print(f"   姓名: {name} (类型: {type(name).__name__})")
    print(f"   年龄: {age} (类型: {type(age).__name__})")
    print(f"   身高: {height} (类型: {type(height).__name__})")
    print(f"   学生身份: {is_student} (类型: {type(is_student).__name__})")
    
    # 2. 多重赋值
    print("\n2. 多重赋值:")
    x = y = z = 10
    print(f"   x = y = z = 10: x={x}, y={y}, z={z}")
    
    a, b, c = 1, 2, 3
    print(f"   a, b, c = 1, 2, 3: a={a}, b={b}, c={c}")
    
    # 3. 变量交换
    print("\n3. 变量交换:")
    a, b = b, a
    print(f"   交换后: a={a}, b={b}")
    
    # 4. 命名约定
    print("\n4. Python命名约定:")
    snake_case_variable = "蛇形命名法"
    UPPER_CASE_CONSTANT = "常量命名法"
    _private_variable = "私有变量命名法"
    Class_Name = "类名命名法"
    
    print(f"   蛇形命名: {snake_case_variable}")
    print(f"   常量命名: {UPPER_CASE_CONSTANT}")
    print(f"   私有变量: {_private_variable}")
    print(f"   类名命名: {Class_Name}")

def demonstrate_numeric_types() -> None:
    """演示数值类型"""
    print_header("数值类型演示")
    
    # 1. 整数类型
    print("1. 整数类型 (int):")
    integer_examples = [
        42,           # 普通整数
        -17,          # 负整数
        0,            # 零
        0b1010,       # 二进制 (10)
        0o755,        # 八进制 (493)
        0xFF,         # 十六进制 (255)
        1_000_000,    # 数字分隔符 (1000000)
    ]
    
    for num in integer_examples:
        print(f"   {num} (类型: {type(num).__name__})")
    
    # 2. 浮点数类型
    print("\n2. 浮点数类型 (float):")
    float_examples = [
        3.14159,      # 普通浮点数
        -2.5,         # 负浮点数
        0.0,          # 零浮点数
        1.23e-4,      # 科学计数法
        float('inf'), # 正无穷
        float('-inf'),# 负无穷
        float('nan'), # 非数字
    ]
    
    for num in float_examples:
        print(f"   {num} (类型: {type(num).__name__})")
    
    # 3. 复数类型
    print("\n3. 复数类型 (complex):")
    complex_examples = [
        3 + 4j,       # 普通复数
        5j,           # 纯虚数
        complex(2, 3),# 构造函数创建
    ]
    
    for num in complex_examples:
        print(f"   {num} (实部: {num.real}, 虚部: {num.imag})")
    
    # 4. 布尔类型
    print("\n4. 布尔类型 (bool):")
    bool_examples = [True, False]
    for boolean in bool_examples:
        print(f"   {boolean} (类型: {type(boolean).__name__}, 数值: {int(boolean)})")
    
    # 5. 数值运算演示
    print("\n5. 数值运算演示:")
    a, b = 10, 3
    print(f"   {a} + {b} = {a + b}")
    print(f"   {a} - {b} = {a - b}")
    print(f"   {a} * {b} = {a * b}")
    print(f"   {a} / {b} = {a / b}")
    print(f"   {a} // {b} = {a // b} (整除)")
    print(f"   {a} % {b} = {a % b} (取余)")
    print(f"   {a} ** {b} = {a ** b} (幂运算)")

def demonstrate_sequence_types() -> None:
    """演示序列类型"""
    print_header("序列类型演示")
    
    # 1. 字符串类型
    print("1. 字符串类型 (str):")
    string_examples = [
        "Hello World",           # 双引号
        'Python编程',            # 单引号
        """多行
字符串
演示""",                     # 三重引号
        "包含'单引号'的字符串",
        '包含"双引号"的字符串',
        f"格式化字符串: {42}",   # f-string
    ]
    
    for s in string_examples:
        print(f"   '{s}' (长度: {len(s)}, 类型: {type(s).__name__})")
    
    # 2. 列表类型
    print("\n2. 列表类型 (list):")
    list_examples = [
        [1, 2, 3, 4, 5],                    # 数字列表
        ['apple', 'banana', 'orange'],      # 字符串列表
        [1, 'hello', 3.14, True],           # 混合类型列表
        list(range(5)),                     # range转列表
        [],                                 # 空列表
    ]
    
    for lst in list_examples:
        print(f"   {lst} (长度: {len(lst)}, 类型: {type(lst).__name__})")
    
    # 3. 元组类型
    print("\n3. 元组类型 (tuple):")
    tuple_examples = [
        (1, 2, 3),                          # 数字元组
        ('a', 'b', 'c'),                    # 字符元组
        (1, 'hello', 3.14),                 # 混合元组
        tuple([1, 2, 3]),                   # 列表转元组
        (42,),                              # 单元素元组
        (),                                 # 空元组
    ]
    
    for tup in tuple_examples:
        print(f"   {tup} (长度: {len(tup)}, 类型: {type(tup).__name__})")
    
    # 4. 字节类型
    print("\n4. 字节类型:")
    byte_string = b"Hello"
    byte_array = bytearray(b"World")
    print(f"   bytes: {byte_string} (类型: {type(byte_string).__name__})")
    print(f"   bytearray: {byte_array} (类型: {type(byte_array).__name__})")

def demonstrate_mapping_types() -> None:
    """演示映射类型"""
    print_header("映射类型演示")
    
    # 1. 字典类型
    print("1. 字典类型 (dict):")
    dict_examples = [
        {'name': '张三', 'age': 25, 'city': '北京'},
        {1: 'one', 2: 'two', 3: 'three'},
        {'numbers': [1, 2, 3], 'nested': {'key': 'value'}},
        dict(name='李四', age=30),
        {},
    ]
    
    for d in dict_examples:
        print(f"   {d} (键数: {len(d)}, 类型: {type(d).__name__})")
    
    # 2. 字典操作演示
    print("\n2. 字典操作演示:")
    student = {'name': '王五', 'age': 22, 'grades': [85, 92, 78]}
    print(f"   原始字典: {student}")
    print(f"   获取值: student['name'] = {student['name']}")
    student['major'] = '计算机科学'
    print(f"   添加键值对: {student}")
    del student['age']
    print(f"   删除键值对: {student}")

def demonstrate_set_types() -> None:
    """演示集合类型"""
    print_header("集合类型演示")
    
    # 1. 集合类型
    print("1. 集合类型 (set):")
    set_examples = [
        {1, 2, 3, 4, 5},
        {'apple', 'banana', 'orange'},
        set([1, 2, 2, 3, 3, 4]),  # 去重
        set(),
    ]
    
    for s in set_examples:
        print(f"   {s} (元素数: {len(s)}, 类型: {type(s).__name__})")
    
    # 2. 冰冻集合
    print("\n2. 冰冻集合 (frozenset):")
    frozen_examples = [
        frozenset([1, 2, 3]),
        frozenset({'a', 'b', 'c'}),
        frozenset(),
    ]
    
    for fs in frozen_examples:
        print(f"   {fs} (类型: {type(fs).__name__})")
    
    # 3. 集合运算演示
    print("\n3. 集合运算演示:")
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}
    print(f"   集合A: {set_a}")
    print(f"   集合B: {set_b}")
    print(f"   并集: {set_a | set_b}")
    print(f"   交集: {set_a & set_b}")
    print(f"   差集: {set_a - set_b}")
    print(f"   对称差集: {set_a ^ set_b}")

def demonstrate_type_conversion() -> None:
    """演示类型转换"""
    print_header("类型转换演示")
    
    # 1. 显式类型转换
    print("1. 显式类型转换:")
    conversions = [
        ("str(42)", str(42)),
        ("int('123')", int('123')),
        ("float('3.14')", float('3.14')),
        ("bool(0)", bool(0)),
        ("bool(1)", bool(1)),
        ("list('hello')", list('hello')),
        ("tuple([1, 2, 3])", tuple([1, 2, 3])),
        ("set([1, 2, 2, 3])", set([1, 2, 2, 3])),
        ("dict([('a', 1), ('b', 2)])", dict([('a', 1), ('b', 2)])),
    ]
    
    for conversion, result in conversions:
        print(f"   {conversion} = {result} (类型: {type(result).__name__})")
    
    # 2. 隐式类型转换演示
    print("\n2. 隐式类型转换:")
    print(f"   5 + 3.14 = {5 + 3.14} (int + float -> float)")
    print(f"   True + 1 = {True + 1} (bool + int -> int)")
    print(f"   'Hello ' + 'World' = {'Hello ' + 'World'} (str + str -> str)")

def demonstrate_type_checking() -> None:
    """演示类型检查"""
    print_header("类型检查演示")
    
    # 1. isinstance检查
    print("1. isinstance()检查:")
    test_objects = [42, 3.14, "hello", [1, 2, 3], {'key': 'value'}, True]
    
    for obj in test_objects:
        checks = [
            isinstance(obj, int),
            isinstance(obj, float),
            isinstance(obj, str),
            isinstance(obj, list),
            isinstance(obj, dict),
            isinstance(obj, bool),
        ]
        check_results = [str(check) for check in checks]
        print(f"   {obj} ({type(obj).__name__}): int={checks[0]}, float={checks[1]}, str={checks[2]}, list={checks[3]}, dict={checks[4]}, bool={checks[5]}")
    
    # 2. type()检查
    print("\n2. type()检查:")
    for obj in test_objects:
        print(f"   type({obj}) = {type(obj)}")
    
    # 3. 类型比较
    print("\n3. 类型比较:")
    print(f"   type(42) == int: {type(42) == int}")
    print(f"   type([1, 2]) == list: {type([1, 2]) == list}")
    print(f"   isinstance(42, (int, float)): {isinstance(42, (int, float))}")

def demonstrate_memory_management() -> None:
    """演示内存管理"""
    print_header("内存管理演示")
    
    # 1. 对象引用计数
    print("1. 对象引用计数:")
    import sys
    
    a = [1, 2, 3]
    b = a
    c = [1, 2, 3]  # 新对象，虽然内容相同
    
    print(f"   列表a: {a} (引用计数: {sys.getrefcount(a)})")
    print(f"   列表b: {b} (引用计数: {sys.getrefcount(b)})")
    print(f"   列表c: {c} (引用计数: {sys.getrefcount(c)})")
    print(f"   a is b: {a is b} (同一对象)")
    print(f"   a is c: {a is c} (不同对象)")
    
    # 2. 可变与不可变对象
    print("\n2. 可变与不可变对象:")
    
    # 不可变对象
    immutable_types = [42, 3.14, "hello", (1, 2, 3), frozenset([1, 2, 3])]
    print("   不可变对象:")
    for obj in immutable_types:
        try:
            original_id = id(obj)
            # 尝试修改对象
            if isinstance(obj, str):
                obj += " modified"
            elif isinstance(obj, tuple):
                obj = obj + (4,)
            new_id = id(obj)
            print(f"     {obj} (ID: {original_id} -> {new_id})")
        except:
            print(f"     {obj} (无法修改)")
    
    # 可变对象
    mutable_obj = [1, 2, 3]
    print("   可变对象:")
    print(f"     原始列表: {mutable_obj} (ID: {id(mutable_obj)})")
    mutable_obj.append(4)
    print(f"     修改后: {mutable_obj} (ID: {id(mutable_obj)})")

def main() -> None:
    """主函数"""
    print("🐍 Python变量和数据类型基础演示")
    print("=" * 50)
    
    try:
        demonstrate_variable_assignment()
        demonstrate_numeric_types()
        demonstrate_sequence_types()
        demonstrate_mapping_types()
        demonstrate_set_types()
        demonstrate_type_conversion()
        demonstrate_type_checking()
        demonstrate_memory_management()
        
        print("\n🎉 所有演示完成!")
        print("=" * 50)
        print(f"Python版本: {sys.version}")
        print(f"平台: {sys.platform}")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        raise

if __name__ == "__main__":
    main()