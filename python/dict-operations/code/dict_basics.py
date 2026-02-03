#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python字典操作演示
展示字典的创建、访问、修改、常用方法和字典推导式
"""

def demo_dict_creation():
    """字典创建方式"""
    print("=" * 50)
    print("1. 字典创建方式")
    print("=" * 50)
    
    # 直接创建
    dict1 = {'name': 'Alice', 'age': 25, 'city': 'Beijing'}
    print(f"直接创建: {dict1}")
    
    # dict()构造函数
    dict2 = dict(name='Bob', age=30, city='Shanghai')
    print(f"dict()构造: {dict2}")
    
    # 从键值对列表创建
    dict3 = dict([('a', 1), ('b', 2), ('c', 3)])
    print(f"从键值对列表: {dict3}")
    
    # fromkeys创建
    dict4 = dict.fromkeys(['x', 'y', 'z'], 0)
    print(f"fromkeys: {dict4}")
    
    # 字典推导式
    dict5 = {x: x**2 for x in range(1, 6)}
    print(f"字典推导式: {dict5}")
    
    # 空字典
    dict6 = {}
    print(f"空字典: {dict6}")


def demo_dict_access():
    """字典访问"""
    print("\n" + "=" * 50)
    print("2. 字典访问")
    print("=" * 50)
    
    person = {'name': 'Alice', 'age': 25, 'city': 'Beijing', 'skills': ['Python', 'Java']}
    print(f"原字典: {person}")
    
    # 直接访问
    print(f"person['name']: {person['name']}")
    
    # get方法(安全访问)
    print(f"person.get('age'): {person.get('age')}")
    print(f"person.get('salary', 0): {person.get('salary', 0)}")  # 默认值
    
    # 获取所有键、值、键值对
    print(f"keys(): {list(person.keys())}")
    print(f"values(): {list(person.values())}")
    print(f"items(): {list(person.items())}")
    
    # 检查键是否存在
    print(f"'name' in person: {'name' in person}")
    print(f"'salary' in person: {'salary' in person}")
    
    # 嵌套字典访问
    data = {'user': {'info': {'name': 'Alice', 'age': 25}}}
    print(f"\n嵌套字典: {data}")
    print(f"data['user']['info']['name']: {data['user']['info']['name']}")


def demo_dict_modify():
    """字典修改"""
    print("\n" + "=" * 50)
    print("3. 字典修改")
    print("=" * 50)
    
    person = {'name': 'Alice', 'age': 25}
    print(f"原字典: {person}")
    
    # 添加/修改
    person['city'] = 'Beijing'
    print(f"添加 city: {person}")
    
    person['age'] = 26
    print(f"修改 age: {person}")
    
    # update批量更新
    person.update({'email': 'alice@example.com', 'age': 27})
    print(f"update: {person}")
    
    # setdefault
    person.setdefault('country', 'China')
    print(f"setdefault country: {person}")
    person.setdefault('name', 'Bob')  # 已存在不会更新
    print(f"setdefault name (已存在): {person}")
    
    # 删除
    del person['email']
    print(f"del email: {person}")
    
    popped = person.pop('country')
    print(f"pop country: 弹出 {popped}, 剩余 {person}")
    
    # popitem删除最后一项
    item = person.popitem()
    print(f"popitem: 弹出 {item}, 剩余 {person}")
    
    # 清空
    person_copy = person.copy()
    person_copy.clear()
    print(f"clear: {person_copy}")


def demo_dict_iteration():
    """字典遍历"""
    print("\n" + "=" * 50)
    print("4. 字典遍历")
    print("=" * 50)
    
    scores = {'Alice': 95, 'Bob': 87, 'Charlie': 92}
    print(f"原字典: {scores}")
    
    # 遍历键
    print("\n遍历键:")
    for key in scores:
        print(f"  {key}")
    
    # 遍历值
    print("\n遍历值:")
    for value in scores.values():
        print(f"  {value}")
    
    # 遍历键值对
    print("\n遍历键值对:")
    for key, value in scores.items():
        print(f"  {key}: {value}")


def demo_dict_comprehension():
    """字典推导式"""
    print("\n" + "=" * 50)
    print("5. 字典推导式")
    print("=" * 50)
    
    # 基本推导式
    squares = {x: x**2 for x in range(1, 6)}
    print(f"平方字典: {squares}")
    
    # 带条件的推导式
    even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
    print(f"偶数平方: {even_squares}")
    
    # 交换键值
    original = {'a': 1, 'b': 2, 'c': 3}
    swapped = {v: k for k, v in original.items()}
    print(f"交换键值: {original} -> {swapped}")
    
    # 从列表创建字典
    words = ['apple', 'banana', 'cherry']
    word_lengths = {word: len(word) for word in words}
    print(f"单词长度: {word_lengths}")


if __name__ == "__main__":
    demo_dict_creation()
    demo_dict_access()
    demo_dict_modify()
    demo_dict_iteration()
    demo_dict_comprehension()
    print("\n[OK] 字典操作演示完成!")
