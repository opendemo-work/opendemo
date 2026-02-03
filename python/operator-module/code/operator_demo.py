#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python operator 模块完整示例
演示运算符函数和操作符重载
"""

import operator
from functools import reduce
from typing import List, Any


# ============ 1. 算术运算符函数 ============
print("=" * 50)
print("1. 算术运算符函数")
print("=" * 50)

print(f"add(5, 3)      = {operator.add(5, 3)}")
print(f"sub(5, 3)      = {operator.sub(5, 3)}")
print(f"mul(5, 3)      = {operator.mul(5, 3)}")
print(f"truediv(5, 3)  = {operator.truediv(5, 3):.4f}")
print(f"floordiv(5, 3) = {operator.floordiv(5, 3)}")
print(f"mod(5, 3)      = {operator.mod(5, 3)}")
print(f"pow(5, 3)      = {operator.pow(5, 3)}")
print(f"neg(-5)        = {operator.neg(-5)}")
print(f"pos(-5)        = {operator.pos(-5)}")
print(f"abs(-5)        = {operator.abs(-5)}")


# ============ 2. 比较运算符函数 ============
print("\n" + "=" * 50)
print("2. 比较运算符函数")
print("=" * 50)

a, b = 5, 3
print(f"a={a}, b={b}")
print(f"lt(a, b) (a < b)  = {operator.lt(a, b)}")
print(f"le(a, b) (a <= b) = {operator.le(a, b)}")
print(f"eq(a, b) (a == b) = {operator.eq(a, b)}")
print(f"ne(a, b) (a != b) = {operator.ne(a, b)}")
print(f"gt(a, b) (a > b)  = {operator.gt(a, b)}")
print(f"ge(a, b) (a >= b) = {operator.ge(a, b)}")


# ============ 3. 位运算符函数 ============
print("\n" + "=" * 50)
print("3. 位运算符函数")
print("=" * 50)

x, y = 0b1100, 0b1010
print(f"x={x} (0b{x:04b}), y={y} (0b{y:04b})")
print(f"and_(x, y) = {operator.and_(x, y)} (0b{operator.and_(x, y):04b})")
print(f"or_(x, y)  = {operator.or_(x, y)} (0b{operator.or_(x, y):04b})")
print(f"xor(x, y)  = {operator.xor(x, y)} (0b{operator.xor(x, y):04b})")
print(f"invert(x)  = {operator.invert(x)}")
print(f"lshift(x, 2) = {operator.lshift(x, 2)}")
print(f"rshift(x, 2) = {operator.rshift(x, 2)}")


# ============ 4. 逻辑运算符函数 ============
print("\n" + "=" * 50)
print("4. 逻辑运算符函数")
print("=" * 50)

print(f"not_(True)     = {operator.not_(True)}")
print(f"not_(0)        = {operator.not_(0)}")
print(f"truth([])      = {operator.truth([])}")
print(f"truth([1,2,3]) = {operator.truth([1, 2, 3])}")
print(f"is_(5, 5)      = {operator.is_(5, 5)}")
print(f"is_not(5, 5)   = {operator.is_not(5, 5)}")


# ============ 5. 序列操作函数 ============
print("\n" + "=" * 50)
print("5. 序列操作函数")
print("=" * 50)

lst = [1, 2, 3, 4, 5]
print(f"列表: {lst}")
print(f"getitem(lst, 2)       = {operator.getitem(lst, 2)}")
print(f"getitem(lst, slice(1,4)) = {operator.getitem(lst, slice(1, 4))}")
print(f"contains(lst, 3)      = {operator.contains(lst, 3)}")
print(f"contains(lst, 10)     = {operator.contains(lst, 10)}")
print(f"countOf(lst, 2)       = {operator.countOf(lst, 2)}")
print(f"indexOf(lst, 3)       = {operator.indexOf(lst, 3)}")

# concat
print(f"\nconcat([1,2], [3,4]) = {operator.concat([1, 2], [3, 4])}")

# setitem / delitem (修改列表)
test_lst = [1, 2, 3]
operator.setitem(test_lst, 1, 20)
print(f"setitem后: {test_lst}")
operator.delitem(test_lst, 0)
print(f"delitem后: {test_lst}")


# ============ 6. itemgetter 获取项 ============
print("\n" + "=" * 50)
print("6. itemgetter 获取项")
print("=" * 50)

# 从元组/列表获取
get_first = operator.itemgetter(0)
get_last = operator.itemgetter(-1)
get_multi = operator.itemgetter(0, 2, 4)

data = ['a', 'b', 'c', 'd', 'e']
print(f"数据: {data}")
print(f"itemgetter(0): {get_first(data)}")
print(f"itemgetter(-1): {get_last(data)}")
print(f"itemgetter(0, 2, 4): {get_multi(data)}")

# 从字典获取
person = {'name': 'Alice', 'age': 30, 'city': 'NYC'}
get_name = operator.itemgetter('name')
get_info = operator.itemgetter('name', 'age')

print(f"\n字典: {person}")
print(f"itemgetter('name'): {get_name(person)}")
print(f"itemgetter('name', 'age'): {get_info(person)}")

# 用于排序
students = [
    ('Alice', 85, 22),
    ('Bob', 90, 20),
    ('Charlie', 85, 21),
]
print(f"\n排序前: {students}")
# 按成绩(索引1)排序
by_grade = sorted(students, key=operator.itemgetter(1), reverse=True)
print(f"按成绩排序: {by_grade}")
# 按成绩和年龄排序
by_grade_age = sorted(students, key=operator.itemgetter(1, 2))
print(f"按成绩和年龄: {by_grade_age}")


# ============ 7. attrgetter 获取属性 ============
print("\n" + "=" * 50)
print("7. attrgetter 获取属性")
print("=" * 50)

class Person:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city
    
    def __repr__(self):
        return f"Person({self.name}, {self.age})"

people = [
    Person('Alice', 30, 'NYC'),
    Person('Bob', 25, 'LA'),
    Person('Charlie', 35, 'Chicago'),
]

get_name = operator.attrgetter('name')
get_age = operator.attrgetter('age')
get_multi = operator.attrgetter('name', 'age')

print(f"people[0]: {people[0]}")
print(f"attrgetter('name'): {get_name(people[0])}")
print(f"attrgetter('age'): {get_age(people[0])}")
print(f"attrgetter('name', 'age'): {get_multi(people[0])}")

# 用于排序
sorted_by_age = sorted(people, key=operator.attrgetter('age'))
print(f"\n按年龄排序: {sorted_by_age}")

# 嵌套属性
class Address:
    def __init__(self, city):
        self.city = city

class Employee:
    def __init__(self, name, address):
        self.name = name
        self.address = address

emp = Employee('Dave', Address('Boston'))
get_city = operator.attrgetter('address.city')
print(f"\n嵌套属性 address.city: {get_city(emp)}")


# ============ 8. methodcaller 调用方法 ============
print("\n" + "=" * 50)
print("8. methodcaller 调用方法")
print("=" * 50)

# 调用字符串方法
upper_caller = operator.methodcaller('upper')
replace_caller = operator.methodcaller('replace', 'o', '0')

text = "hello world"
print(f"text: '{text}'")
print(f"methodcaller('upper'): '{upper_caller(text)}'")
print(f"methodcaller('replace', 'o', '0'): '{replace_caller(text)}'")

# 用于列表处理
strings = ['hello', 'world', 'python']
uppercased = list(map(operator.methodcaller('upper'), strings))
print(f"\n批量转大写: {uppercased}")


# ============ 9. 原地操作函数 ============
print("\n" + "=" * 50)
print("9. 原地操作函数 (iadd, isub, etc.)")
print("=" * 50)

# 注意: 原地操作返回结果，不一定修改原对象
lst = [1, 2, 3]
result = operator.iadd(lst, [4, 5])  # 等同于 lst += [4, 5]
print(f"iadd([1,2,3], [4,5]) = {result}")
print(f"原列表被修改: {lst}")

num = 10
result = operator.iadd(num, 5)  # 数值是不可变的
print(f"\niadd(10, 5) = {result}")


# ============ 10. 实用示例 ============
print("\n" + "=" * 50)
print("10. 实用示例")
print("=" * 50)

# 示例1: reduce + operator
numbers = [1, 2, 3, 4, 5]
total = reduce(operator.add, numbers)
product = reduce(operator.mul, numbers)
print(f"列表 {numbers}")
print(f"  求和: {total}")
print(f"  求积: {product}")

# 示例2: 用于max/min的key
data = [
    {'name': 'A', 'value': 10},
    {'name': 'B', 'value': 30},
    {'name': 'C', 'value': 20},
]
max_item = max(data, key=operator.itemgetter('value'))
print(f"\n数据: {data}")
print(f"value最大的项: {max_item}")

# 示例3: 条件过滤
values = [5, 10, 15, 20, 25]
gt_10 = list(filter(lambda x: operator.gt(x, 10), values))
print(f"\n{values} 中大于10的: {gt_10}")

# 示例4: 函数式编程组合
from functools import partial

# 创建特定的加法函数
add_10 = partial(operator.add, 10)
print(f"\nadd_10(5) = {add_10(5)}")

# 创建特定的比较函数
is_positive = partial(operator.gt, 0)  # 注意参数顺序
# is_positive(x) 等同于 operator.gt(0, x) 即 0 > x
# 需要反过来
is_positive = lambda x: operator.gt(x, 0)
print(f"is_positive(5) = {is_positive(5)}")
print(f"is_positive(-5) = {is_positive(-5)}")


print("\n" + "=" * 50)
print("所有 operator 模块示例完成!")
print("=" * 50)
