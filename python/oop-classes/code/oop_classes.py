#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python面向对象编程演示
展示类定义、继承、多态、特殊方法、属性装饰器等
"""
from abc import ABC, abstractmethod


def demo_class_basics():
    """类基础"""
    print("=" * 50)
    print("1. 类基础")
    print("=" * 50)
    
    class Person:
        """人员类"""
        # 类属性
        species = "Human"
        
        def __init__(self, name, age):
            """构造方法"""
            self.name = name  # 实例属性
            self.age = age
        
        def introduce(self):
            """实例方法"""
            return f"我是{self.name}, {self.age}岁"
        
        @classmethod
        def get_species(cls):
            """类方法"""
            return cls.species
        
        @staticmethod
        def is_adult(age):
            """静态方法"""
            return age >= 18
    
    # 创建实例
    p1 = Person("Alice", 25)
    p2 = Person("Bob", 17)
    
    print(f"p1.introduce(): {p1.introduce()}")
    print(f"p2.introduce(): {p2.introduce()}")
    print(f"类属性: Person.species = {Person.species}")
    print(f"类方法: Person.get_species() = {Person.get_species()}")
    print(f"静态方法: Person.is_adult(25) = {Person.is_adult(25)}")
    print(f"静态方法: Person.is_adult(17) = {Person.is_adult(17)}")


def demo_inheritance():
    """继承"""
    print("\n" + "=" * 50)
    print("2. 继承")
    print("=" * 50)
    
    class Animal:
        def __init__(self, name):
            self.name = name
        
        def speak(self):
            return "Some sound"
    
    class Dog(Animal):
        def __init__(self, name, breed):
            super().__init__(name)  # 调用父类构造
            self.breed = breed
        
        def speak(self):  # 方法重写
            return "Woof!"
    
    class Cat(Animal):
        def speak(self):
            return "Meow!"
    
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers")
    
    print(f"dog.name: {dog.name}, breed: {dog.breed}")
    print(f"dog.speak(): {dog.speak()}")
    print(f"cat.speak(): {cat.speak()}")
    print(f"isinstance(dog, Animal): {isinstance(dog, Animal)}")
    print(f"issubclass(Dog, Animal): {issubclass(Dog, Animal)}")


def demo_multiple_inheritance():
    """多重继承"""
    print("\n" + "=" * 50)
    print("3. 多重继承与MRO")
    print("=" * 50)
    
    class A:
        def method(self):
            return "A"
    
    class B(A):
        def method(self):
            return "B"
    
    class C(A):
        def method(self):
            return "C"
    
    class D(B, C):
        pass
    
    d = D()
    print(f"D().method(): {d.method()}")
    print(f"D的MRO: {[c.__name__ for c in D.__mro__]}")


def demo_special_methods():
    """特殊方法(魔术方法)"""
    print("\n" + "=" * 50)
    print("4. 特殊方法")
    print("=" * 50)
    
    class Vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        
        def __repr__(self):
            return f"Vector({self.x}, {self.y})"
        
        def __str__(self):
            return f"({self.x}, {self.y})"
        
        def __add__(self, other):
            return Vector(self.x + other.x, self.y + other.y)
        
        def __mul__(self, scalar):
            return Vector(self.x * scalar, self.y * scalar)
        
        def __eq__(self, other):
            return self.x == other.x and self.y == other.y
        
        def __len__(self):
            return int((self.x**2 + self.y**2)**0.5)
    
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    
    print(f"v1: {v1}")
    print(f"repr(v1): {repr(v1)}")
    print(f"v1 + v2: {v1 + v2}")
    print(f"v1 * 2: {v1 * 2}")
    print(f"v1 == Vector(3, 4): {v1 == Vector(3, 4)}")
    print(f"len(v1): {len(v1)}")


def demo_property():
    """属性装饰器"""
    print("\n" + "=" * 50)
    print("5. 属性装饰器 @property")
    print("=" * 50)
    
    class Circle:
        def __init__(self, radius):
            self._radius = radius
        
        @property
        def radius(self):
            """获取半径"""
            return self._radius
        
        @radius.setter
        def radius(self, value):
            """设置半径"""
            if value < 0:
                raise ValueError("半径不能为负")
            self._radius = value
        
        @property
        def area(self):
            """计算面积(只读属性)"""
            return 3.14159 * self._radius ** 2
    
    c = Circle(5)
    print(f"初始半径: {c.radius}")
    print(f"面积: {c.area:.2f}")
    
    c.radius = 10
    print(f"修改后半径: {c.radius}")
    print(f"新面积: {c.area:.2f}")


def demo_abstract_class():
    """抽象类"""
    print("\n" + "=" * 50)
    print("6. 抽象类")
    print("=" * 50)
    
    class Shape(ABC):
        @abstractmethod
        def area(self):
            pass
        
        @abstractmethod
        def perimeter(self):
            pass
    
    class Rectangle(Shape):
        def __init__(self, width, height):
            self.width = width
            self.height = height
        
        def area(self):
            return self.width * self.height
        
        def perimeter(self):
            return 2 * (self.width + self.height)
    
    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius
        
        def area(self):
            return 3.14159 * self.radius ** 2
        
        def perimeter(self):
            return 2 * 3.14159 * self.radius
    
    shapes = [Rectangle(4, 5), Circle(3)]
    for shape in shapes:
        print(f"{shape.__class__.__name__}: 面积={shape.area():.2f}, 周长={shape.perimeter():.2f}")


def demo_dataclass():
    """数据类 (Python 3.7+)"""
    print("\n" + "=" * 50)
    print("7. 数据类 @dataclass")
    print("=" * 50)
    
    from dataclasses import dataclass, field
    
    @dataclass
    class Product:
        name: str
        price: float
        quantity: int = 0
        tags: list = field(default_factory=list)
        
        def total_value(self):
            return self.price * self.quantity
    
    p1 = Product("Apple", 1.5, 100)
    p2 = Product("Banana", 0.8, 50, ["fruit", "yellow"])
    
    print(f"p1: {p1}")
    print(f"p2: {p2}")
    print(f"p1.total_value(): {p1.total_value()}")
    print(f"p1 == Product('Apple', 1.5, 100): {p1 == Product('Apple', 1.5, 100)}")


if __name__ == "__main__":
    demo_class_basics()
    demo_inheritance()
    demo_multiple_inheritance()
    demo_special_methods()
    demo_property()
    demo_abstract_class()
    demo_dataclass()
    print("\n[OK] 面向对象编程演示完成!")
