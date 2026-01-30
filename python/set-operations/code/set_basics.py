#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python集合操作演示
展示集合的创建、操作、集合运算
"""

def demo_set_creation():
    """集合创建方式"""
    print("=" * 50)
    print("1. 集合创建方式")
    print("=" * 50)
    
    # 直接创建
    set1 = {1, 2, 3, 4, 5}
    print(f"直接创建: {set1}")
    
    # set()构造函数
    set2 = set([1, 2, 2, 3, 3, 3])  # 自动去重
    print(f"set()从列表创建(自动去重): {set2}")
    
    set3 = set("hello")  # 从字符串创建
    print(f"set('hello'): {set3}")
    
    # 集合推导式
    set4 = {x**2 for x in range(1, 6)}
    print(f"集合推导式: {set4}")
    
    # 空集合(注意: {}是空字典)
    set5 = set()
    print(f"空集合: {set5}, 类型: {type(set5)}")
    print(f"{{}}的类型: {type({})}")  # 这是空字典


def demo_set_basic_operations():
    """集合基本操作"""
    print("\n" + "=" * 50)
    print("2. 集合基本操作")
    print("=" * 50)
    
    s = {1, 2, 3}
    print(f"原集合: {s}")
    
    # 添加元素
    s.add(4)
    print(f"add(4): {s}")
    
    # 添加多个元素
    s.update([5, 6, 7])
    print(f"update([5, 6, 7]): {s}")
    
    # 删除元素
    s.remove(7)  # 不存在会报错
    print(f"remove(7): {s}")
    
    s.discard(10)  # 不存在不会报错
    print(f"discard(10): {s}")
    
    popped = s.pop()  # 随机删除一个
    print(f"pop(): 弹出 {popped}, 剩余 {s}")
    
    # 检查成员
    print(f"3 in s: {3 in s}")
    print(f"10 in s: {10 in s}")
    
    # 长度
    print(f"len(s): {len(s)}")


def demo_set_operations():
    """集合运算"""
    print("\n" + "=" * 50)
    print("3. 集合运算")
    print("=" * 50)
    
    A = {1, 2, 3, 4, 5}
    B = {4, 5, 6, 7, 8}
    print(f"集合A: {A}")
    print(f"集合B: {B}")
    
    # 并集
    print(f"\n并集 A | B: {A | B}")
    print(f"并集 A.union(B): {A.union(B)}")
    
    # 交集
    print(f"\n交集 A & B: {A & B}")
    print(f"交集 A.intersection(B): {A.intersection(B)}")
    
    # 差集
    print(f"\n差集 A - B: {A - B}")
    print(f"差集 A.difference(B): {A.difference(B)}")
    print(f"差集 B - A: {B - A}")
    
    # 对称差集(只在一个集合中的元素)
    print(f"\n对称差集 A ^ B: {A ^ B}")
    print(f"对称差集 A.symmetric_difference(B): {A.symmetric_difference(B)}")


def demo_set_comparison():
    """集合比较"""
    print("\n" + "=" * 50)
    print("4. 集合比较")
    print("=" * 50)
    
    A = {1, 2, 3}
    B = {1, 2, 3, 4, 5}
    C = {1, 2, 3}
    D = {6, 7, 8}
    
    print(f"A = {A}")
    print(f"B = {B}")
    print(f"C = {C}")
    print(f"D = {D}")
    
    # 子集
    print(f"\nA.issubset(B): {A.issubset(B)}")
    print(f"A <= B: {A <= B}")
    print(f"A < B (真子集): {A < B}")
    
    # 超集
    print(f"\nB.issuperset(A): {B.issuperset(A)}")
    print(f"B >= A: {B >= A}")
    
    # 相等
    print(f"\nA == C: {A == C}")
    
    # 不相交
    print(f"\nA.isdisjoint(D): {A.isdisjoint(D)}")


def demo_frozenset():
    """不可变集合"""
    print("\n" + "=" * 50)
    print("5. 不可变集合 frozenset")
    print("=" * 50)
    
    # 创建frozenset
    fs = frozenset([1, 2, 3, 4, 5])
    print(f"frozenset: {fs}")
    print(f"类型: {type(fs)}")
    
    # frozenset可以作为字典的键
    data = {frozenset([1, 2]): "one-two", frozenset([3, 4]): "three-four"}
    print(f"\nfrozenset作为字典键: {data}")
    
    # frozenset可以作为集合的元素
    s = {frozenset([1, 2]), frozenset([3, 4])}
    print(f"frozenset作为集合元素: {s}")
    
    # frozenset支持集合运算
    fs1 = frozenset([1, 2, 3])
    fs2 = frozenset([2, 3, 4])
    print(f"\nfrozenset并集: {fs1 | fs2}")
    print(f"frozenset交集: {fs1 & fs2}")


if __name__ == "__main__":
    demo_set_creation()
    demo_set_basic_operations()
    demo_set_operations()
    demo_set_comparison()
    demo_frozenset()
    print("\n[OK] 集合操作演示完成!")
