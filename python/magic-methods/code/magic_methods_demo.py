#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 魔法方法 (Magic Methods / Dunder Methods) 完整示例
演示特殊方法的使用
"""

from functools import total_ordering
from typing import Any


# ============ 1. 对象创建与初始化 ============
print("=" * 50)
print("1. 对象创建与初始化")
print("=" * 50)

class MyClass:
    def __new__(cls, *args, **kwargs):
        """创建实例 (在__init__之前)"""
        print(f"  __new__ 创建实例")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, value):
        """初始化实例"""
        print(f"  __init__ 初始化, value={value}")
        self.value = value
    
    def __del__(self):
        """销毁实例 (垃圾回收时)"""
        print(f"  __del__ 销毁实例")

print("创建对象:")
obj = MyClass(42)
print(f"obj.value = {obj.value}")


# ============ 2. 字符串表示 ============
print("\n" + "=" * 50)
print("2. 字符串表示")
print("=" * 50)

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __str__(self):
        """用户友好的字符串 (print, str())"""
        return f"{self.name}, {self.age}岁"
    
    def __repr__(self):
        """开发者字符串 (调试, repr())"""
        return f"Person(name={self.name!r}, age={self.age})"

person = Person("Alice", 25)
print(f"str(): {str(person)}")
print(f"repr(): {repr(person)}")
print(f"print: {person}")


# ============ 3. 比较运算符 ============
print("\n" + "=" * 50)
print("3. 比较运算符")
print("=" * 50)

@total_ordering  # 自动生成其他比较方法
class Version:
    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch
    
    def __eq__(self, other):
        """=="""
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) == \
               (other.major, other.minor, other.patch)
    
    def __lt__(self, other):
        """<"""
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) < \
               (other.major, other.minor, other.patch)
    
    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

v1 = Version(1, 0, 0)
v2 = Version(1, 2, 0)
v3 = Version(2, 0, 0)

print(f"v1={v1}, v2={v2}, v3={v3}")
print(f"v1 == v2: {v1 == v2}")
print(f"v1 < v2: {v1 < v2}")
print(f"v2 <= v3: {v2 <= v3}")  # 自动生成


# ============ 4. 算术运算符 ============
print("\n" + "=" * 50)
print("4. 算术运算符")
print("=" * 50)

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """+"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        """-"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar):
        """* (标量乘法)"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __rmul__(self, scalar):
        """反向乘法 (scalar * vector)"""
        return self.__mul__(scalar)
    
    def __neg__(self):
        """一元负号"""
        return Vector(-self.x, -self.y)
    
    def __abs__(self):
        """abs()"""
        return (self.x**2 + self.y**2) ** 0.5
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 - v2 = {v1 - v2}")
print(f"v1 * 2 = {v1 * 2}")
print(f"3 * v2 = {3 * v2}")
print(f"-v1 = {-v1}")
print(f"abs(v1) = {abs(v1)}")


# ============ 5. 容器相关 ============
print("\n" + "=" * 50)
print("5. 容器相关魔法方法")
print("=" * 50)

class MyList:
    def __init__(self, data):
        self._data = list(data)
    
    def __len__(self):
        """len()"""
        return len(self._data)
    
    def __getitem__(self, key):
        """self[key]"""
        return self._data[key]
    
    def __setitem__(self, key, value):
        """self[key] = value"""
        self._data[key] = value
    
    def __delitem__(self, key):
        """del self[key]"""
        del self._data[key]
    
    def __contains__(self, item):
        """item in self"""
        return item in self._data
    
    def __iter__(self):
        """iter()"""
        return iter(self._data)
    
    def __reversed__(self):
        """reversed()"""
        return reversed(self._data)
    
    def __repr__(self):
        return f"MyList({self._data})"

ml = MyList([1, 2, 3, 4, 5])
print(f"len: {len(ml)}")
print(f"ml[2]: {ml[2]}")
print(f"3 in ml: {3 in ml}")
print(f"遍历: {[x for x in ml]}")
print(f"反转: {list(reversed(ml))}")

ml[0] = 100
print(f"修改后: {ml}")


# ============ 6. 可调用对象 ============
print("\n" + "=" * 50)
print("6. 可调用对象 (__call__)")
print("=" * 50)

class Multiplier:
    def __init__(self, factor: int):
        self.factor = factor
    
    def __call__(self, value):
        """使对象可调用"""
        return value * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")
print(f"callable(double): {callable(double)}")


class Counter:
    def __init__(self):
        self.count = 0
    
    def __call__(self):
        self.count += 1
        return self.count

counter = Counter()
print(f"counter(): {counter()}, {counter()}, {counter()}")


# ============ 7. 上下文管理器 ============
print("\n" + "=" * 50)
print("7. 上下文管理器")
print("=" * 50)

class Timer:
    def __init__(self, name: str):
        self.name = name
    
    def __enter__(self):
        """进入with块"""
        import time
        print(f"  开始计时: {self.name}")
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出with块"""
        import time
        elapsed = time.time() - self.start
        print(f"  结束计时: {self.name}, 耗时: {elapsed:.4f}s")
        return False  # 不抑制异常

with Timer("测试操作"):
    sum(range(100000))


# ============ 8. 属性访问 ============
print("\n" + "=" * 50)
print("8. 属性访问控制")
print("=" * 50)

class DynamicObject:
    def __init__(self):
        self._data = {}
    
    def __getattr__(self, name):
        """访问不存在的属性时调用"""
        return self._data.get(name, f"属性'{name}'不存在")
    
    def __setattr__(self, name, value):
        """设置属性时调用"""
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
    
    def __delattr__(self, name):
        """删除属性时调用"""
        if name in self._data:
            del self._data[name]

obj = DynamicObject()
obj.name = "Alice"
obj.age = 25
print(f"name: {obj.name}")
print(f"age: {obj.age}")
print(f"unknown: {obj.unknown}")


# ============ 9. 哈希与布尔 ============
print("\n" + "=" * 50)
print("9. 哈希与布尔")
print("=" * 50)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        """使对象可哈希(可作为字典键/集合元素)"""
        return hash((self.x, self.y))
    
    def __bool__(self):
        """bool()转换"""
        return self.x != 0 or self.y != 0
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p1 = Point(3, 4)
p2 = Point(3, 4)
p0 = Point(0, 0)

print(f"p1 == p2: {p1 == p2}")
print(f"hash(p1) == hash(p2): {hash(p1) == hash(p2)}")

# 可用作字典键
points = {p1: "first", p2: "second"}
print(f"字典: {points}")  # p1和p2相等,所以只有一个

print(f"bool(p1): {bool(p1)}")
print(f"bool(p0): {bool(p0)}")


# ============ 10. 类型转换 ============
print("\n" + "=" * 50)
print("10. 类型转换")
print("=" * 50)

class Money:
    def __init__(self, amount: float):
        self.amount = amount
    
    def __int__(self):
        return int(self.amount)
    
    def __float__(self):
        return float(self.amount)
    
    def __str__(self):
        return f"${self.amount:.2f}"
    
    def __format__(self, format_spec):
        """format()和f-string"""
        if format_spec == "":
            return str(self)
        return format(self.amount, format_spec)

money = Money(123.456)
print(f"int(): {int(money)}")
print(f"float(): {float(money)}")
print(f"str(): {str(money)}")
print(f"format .2f: {money:.2f}")
print(f"f-string: {money}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("魔法方法总结")
print("=" * 50)
print("""
常用魔法方法:
创建/销毁: __new__, __init__, __del__
字符串: __str__, __repr__, __format__
比较: __eq__, __lt__, __le__, __gt__, __ge__, __ne__
算术: __add__, __sub__, __mul__, __truediv__, __neg__, __abs__
容器: __len__, __getitem__, __setitem__, __contains__, __iter__
属性: __getattr__, __setattr__, __delattr__
调用: __call__
上下文: __enter__, __exit__
其他: __hash__, __bool__, __int__, __float__

设计原则:
1. 返回NotImplemented表示不支持该操作
2. __eq__改变时考虑__hash__
3. 使用@total_ordering简化比较方法
4. __repr__返回可重建对象的字符串
""")
