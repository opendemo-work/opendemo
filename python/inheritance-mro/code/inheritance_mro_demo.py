#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 继承与 MRO (方法解析顺序) 完整示例
演示单继承、多继承、super() 和 MRO
"""

from typing import List


# ============ 1. 单继承基础 ============
print("=" * 50)
print("1. 单继承基础")
print("=" * 50)

class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "Some sound"
    
    def info(self):
        return f"{self.name} is an animal"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 调用父类构造函数
        self.breed = breed
    
    def speak(self):  # 方法重写
        return "Woof!"
    
    def fetch(self):  # 新增方法
        return f"{self.name} is fetching"

dog = Dog("Buddy", "Golden Retriever")
print(f"Dog: {dog.name}, {dog.breed}")
print(f"speak(): {dog.speak()}")
print(f"info(): {dog.info()}")  # 继承的方法
print(f"fetch(): {dog.fetch()}")


# ============ 2. 多继承 ============
print("\n" + "=" * 50)
print("2. 多继承")
print("=" * 50)

class Flyable:
    def fly(self):
        return "Flying..."

class Swimmable:
    def swim(self):
        return "Swimming..."

class Duck(Animal, Flyable, Swimmable):
    def speak(self):
        return "Quack!"

duck = Duck("Donald")
print(f"Duck: {duck.name}")
print(f"speak(): {duck.speak()}")
print(f"fly(): {duck.fly()}")
print(f"swim(): {duck.swim()}")


# ============ 3. MRO (方法解析顺序) ============
print("\n" + "=" * 50)
print("3. MRO (方法解析顺序)")
print("=" * 50)

print(f"Dog MRO: {[cls.__name__ for cls in Dog.__mro__]}")
print(f"Duck MRO: {[cls.__name__ for cls in Duck.__mro__]}")

# 使用 mro() 方法
print(f"\nDuck.mro(): {Duck.mro()}")


# ============ 4. 菱形继承问题 ============
print("\n" + "=" * 50)
print("4. 菱形继承问题")
print("=" * 50)

class A:
    def method(self):
        return "A.method"
    
    def __init__(self):
        print("  A.__init__")

class B(A):
    def method(self):
        return "B.method -> " + super().method()
    
    def __init__(self):
        print("  B.__init__")
        super().__init__()

class C(A):
    def method(self):
        return "C.method -> " + super().method()
    
    def __init__(self):
        print("  C.__init__")
        super().__init__()

class D(B, C):
    def method(self):
        return "D.method -> " + super().method()
    
    def __init__(self):
        print("  D.__init__")
        super().__init__()

print("菱形继承 D(B, C), B(A), C(A):")
print(f"D MRO: {[cls.__name__ for cls in D.__mro__]}")
print("\n创建 D 实例:")
d = D()
print(f"\nd.method(): {d.method()}")


# ============ 5. super() 详解 ============
print("\n" + "=" * 50)
print("5. super() 详解")
print("=" * 50)

class Parent:
    class_attr = "Parent's class attr"
    
    def greet(self):
        return "Hello from Parent"

class Child(Parent):
    class_attr = "Child's class attr"
    
    def greet(self):
        # super() 返回一个代理对象
        parent_greeting = super().greet()
        return f"Child says: {parent_greeting}"
    
    def access_parent_attr(self):
        # 访问父类的类属性
        return super().class_attr

child = Child()
print(f"child.greet(): {child.greet()}")
print(f"access_parent_attr(): {child.access_parent_attr()}")

# super() 的两参数形式
print(f"\nsuper(Child, child).greet(): {super(Child, child).greet()}")


# ============ 6. 协作式多重继承 ============
print("\n" + "=" * 50)
print("6. 协作式多重继承")
print("=" * 50)

class Base:
    def __init__(self, **kwargs):
        # 消耗所有剩余参数
        pass

class Logger(Base):
    def __init__(self, log_level="INFO", **kwargs):
        self.log_level = log_level
        print(f"  Logger init: log_level={log_level}")
        super().__init__(**kwargs)
    
    def log(self, message):
        return f"[{self.log_level}] {message}"

class Serializer(Base):
    def __init__(self, format="json", **kwargs):
        self.format = format
        print(f"  Serializer init: format={format}")
        super().__init__(**kwargs)
    
    def serialize(self, data):
        return f"Serialized as {self.format}: {data}"

class LoggingSerializer(Logger, Serializer):
    def __init__(self, name, **kwargs):
        self.name = name
        print(f"  LoggingSerializer init: name={name}")
        super().__init__(**kwargs)

print("创建 LoggingSerializer:")
ls = LoggingSerializer("MySerializer", log_level="DEBUG", format="xml")
print(f"\n结果: {ls.name}, {ls.log_level}, {ls.format}")
print(f"MRO: {[c.__name__ for c in LoggingSerializer.__mro__]}")


# ============ 7. 抽象基类继承 ============
print("\n" + "=" * 50)
print("7. 抽象基类继承")
print("=" * 50)

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

rect = Rectangle(4, 5)
square = Square(4)
print(f"Rectangle: {rect.describe()}")
print(f"Square: {square.describe()}")
print(f"Square MRO: {[c.__name__ for c in Square.__mro__]}")


# ============ 8. Mixin 模式 ============
print("\n" + "=" * 50)
print("8. Mixin 模式")
print("=" * 50)

class JsonMixin:
    """提供 JSON 序列化功能"""
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class ComparableMixin:
    """提供比较功能"""
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __ne__(self, other):
        return not self.__eq__(other)

class Person(JsonMixin, ComparableMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("Alice", 30)
p2 = Person("Alice", 30)
p3 = Person("Bob", 25)

print(f"p1.to_json(): {p1.to_json()}")
print(f"p1 == p2: {p1 == p2}")
print(f"p1 == p3: {p1 == p3}")


# ============ 9. 方法覆盖与扩展 ============
print("\n" + "=" * 50)
print("9. 方法覆盖与扩展")
print("=" * 50)

class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        return self.count

class LoggingCounter(Counter):
    def __init__(self):
        super().__init__()
        self.history = []
    
    def increment(self):
        # 扩展父类方法
        result = super().increment()
        self.history.append(result)
        print(f"  Count: {result}")
        return result

lc = LoggingCounter()
lc.increment()
lc.increment()
lc.increment()
print(f"History: {lc.history}")


# ============ 10. isinstance 与 issubclass ============
print("\n" + "=" * 50)
print("10. isinstance 与 issubclass")
print("=" * 50)

print(f"isinstance(dog, Dog): {isinstance(dog, Dog)}")
print(f"isinstance(dog, Animal): {isinstance(dog, Animal)}")
print(f"isinstance(dog, Flyable): {isinstance(dog, Flyable)}")

print(f"\nissubclass(Dog, Animal): {issubclass(Dog, Animal)}")
print(f"issubclass(Duck, Flyable): {issubclass(Duck, Flyable)}")
print(f"issubclass(Duck, Dog): {issubclass(Duck, Dog)}")


print("\n" + "=" * 50)
print("所有继承与MRO示例完成!")
print("=" * 50)
