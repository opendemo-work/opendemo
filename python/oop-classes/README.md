# Python OOP Classes Demo

Python面向对象编程(OOP)演示项目，全面展示类、对象、继承、多态等核心概念。

## 技术栈

- Python 3.8+
- 面向对象编程(OOP)

## 核心概念

### 类与对象

```python
class Person:
    """人员基类"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"我是{self.name}，今年{self.age}岁"

# 创建对象
person = Person("张三", 25)
print(person.introduce())
```

### 继承

```python
class Student(Person):
    """学生类，继承Person"""
    
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
    
    def study(self):
        return f"{self.name}正在学习"

student = Student("李四", 20, "S001")
print(student.introduce())  # 继承父类方法
print(student.study())      # 子类特有方法
```

### 多态

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪"

class Cat(Animal):
    def speak(self):
        return "喵喵"

# 多态调用
def animal_sound(animal):
    print(animal.speak())

animal_sound(Dog())  # 汪汪
animal_sound(Cat())  # 喵喵
```

### 封装

```python
class BankAccount:
    """银行账户类"""
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # 私有属性
    
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        """取款"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self):
        """获取余额"""
        return self.__balance

account = BankAccount("王五", 1000)
account.deposit(500)
print(account.get_balance())  # 1500
```

### 类方法与静态方法

```python
class MathUtils:
    """数学工具类"""
    
    count = 0  # 类属性
    
    def __init__(self):
        MathUtils.count += 1
    
    @classmethod
    def get_count(cls):
        """类方法"""
        return cls.count
    
    @staticmethod
    def add(x, y):
        """静态方法"""
        return x + y

print(MathUtils.add(1, 2))  # 3
```

### 属性装饰器

```python
class Circle:
    """圆形类"""
    
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """获取半径"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """设置半径"""
        if value > 0:
            self._radius = value
        else:
            raise ValueError("半径必须大于0")
    
    @property
    def area(self):
        """计算面积"""
        import math
        return math.pi * self._radius ** 2

circle = Circle(5)
print(circle.area)  # 78.54...
circle.radius = 10
print(circle.area)  # 314.15...
```

## 高级特性

### 抽象基类

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """抽象基类"""
    
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
```

### 单例模式

```python
class Singleton:
    """单例模式实现"""
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True
```

## 快速开始

```bash
# 运行示例
python oop_basics.py
python inheritance_demo.py
python polymorphism_demo.py

# 运行测试
python -m pytest test_oop.py -v
```

## 学习要点

1. 类与对象的关系
2. 继承的类型：单继承、多继承
3. 方法解析顺序(MRO)
4. 访问控制：public、protected、private
5. 设计模式基础：单例、工厂、策略模式

## 参考

- [Python官方文档 - 类](https://docs.python.org/3/tutorial/classes.html)
- 《Python Cookbook》
