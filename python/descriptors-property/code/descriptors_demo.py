#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 描述符与属性 (Descriptors & Property) 完整示例
演示 Python 的描述符协议和 property 装饰器
"""

from typing import Any, Optional, Type
from weakref import WeakKeyDictionary


# ============ 1. Property 基础 ============
print("=" * 50)
print("1. Property 基础")
print("=" * 50)

class Circle:
    """使用 property 的圆形类"""
    
    def __init__(self, radius: float):
        self._radius = radius
    
    @property
    def radius(self) -> float:
        """半径 - getter"""
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        """半径 - setter (带验证)"""
        if value <= 0:
            raise ValueError("半径必须为正数")
        self._radius = value
    
    @radius.deleter
    def radius(self):
        """半径 - deleter"""
        print("删除半径")
        del self._radius
    
    @property
    def diameter(self) -> float:
        """直径 - 只读计算属性"""
        return self._radius * 2
    
    @property
    def area(self) -> float:
        """面积 - 只读计算属性"""
        import math
        return math.pi * self._radius ** 2

circle = Circle(5)
print(f"半径: {circle.radius}")
print(f"直径: {circle.diameter}")
print(f"面积: {circle.area:.2f}")

circle.radius = 10  # 使用 setter
print(f"新半径: {circle.radius}")

try:
    circle.radius = -1  # 触发验证
except ValueError as e:
    print(f"验证错误: {e}")


# ============ 2. Property 函数式用法 ============
print("\n" + "=" * 50)
print("2. Property 函数式用法")
print("=" * 50)

class Person:
    def __init__(self, first_name: str, last_name: str):
        self._first_name = first_name
        self._last_name = last_name
    
    def get_full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"
    
    def set_full_name(self, value: str):
        parts = value.split(" ", 1)
        self._first_name = parts[0]
        self._last_name = parts[1] if len(parts) > 1 else ""
    
    # 函数式 property
    full_name = property(get_full_name, set_full_name)

person = Person("John", "Doe")
print(f"全名: {person.full_name}")
person.full_name = "Jane Smith"
print(f"新全名: {person.full_name}")


# ============ 3. 描述符协议 ============
print("\n" + "=" * 50)
print("3. 描述符协议")
print("=" * 50)

class TypedProperty:
    """类型检查描述符"""
    
    def __init__(self, name: str, expected_type: type):
        self.name = name
        self.expected_type = expected_type
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} 必须是 {self.expected_type.__name__} 类型")
        obj.__dict__[self.name] = value
    
    def __delete__(self, obj):
        del obj.__dict__[self.name]

class Product:
    name = TypedProperty("name", str)
    price = TypedProperty("price", (int, float))
    quantity = TypedProperty("quantity", int)
    
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

product = Product("Laptop", 999.99, 10)
print(f"产品: {product.name}, 价格: {product.price}, 数量: {product.quantity}")

try:
    product.price = "免费"  # 类型错误
except TypeError as e:
    print(f"类型错误: {e}")


# ============ 4. 数据验证描述符 ============
print("\n" + "=" * 50)
print("4. 数据验证描述符")
print("=" * 50)

class Validator:
    """验证描述符基类"""
    
    def __init__(self, name: str = None):
        self.name = name
        self.storage_name = None
    
    def __set_name__(self, owner, name):
        """Python 3.6+ 自动设置属性名"""
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name, None)
    
    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.storage_name, value)
    
    def validate(self, value):
        """子类实现具体验证"""
        pass

class PositiveNumber(Validator):
    """正数验证"""
    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} 必须是数字")
        if value <= 0:
            raise ValueError(f"{self.name} 必须为正数")

class NonEmptyString(Validator):
    """非空字符串验证"""
    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} 必须是字符串")
        if not value.strip():
            raise ValueError(f"{self.name} 不能为空")

class RangeNumber(Validator):
    """范围数字验证"""
    def __init__(self, min_val: float = None, max_val: float = None):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
    
    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} 必须是数字")
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} 不能小于 {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} 不能大于 {self.max_val}")

class Order:
    customer = NonEmptyString()
    quantity = PositiveNumber()
    discount = RangeNumber(min_val=0, max_val=1)
    
    def __init__(self, customer: str, quantity: int, discount: float = 0):
        self.customer = customer
        self.quantity = quantity
        self.discount = discount

order = Order("Alice", 5, 0.1)
print(f"订单: 客户={order.customer}, 数量={order.quantity}, 折扣={order.discount}")

try:
    order.discount = 1.5
except ValueError as e:
    print(f"验证错误: {e}")


# ============ 5. 惰性属性描述符 ============
print("\n" + "=" * 50)
print("5. 惰性属性描述符")
print("=" * 50)

class LazyProperty:
    """惰性计算属性 - 只计算一次"""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # 计算值并存储到实例字典中
        value = self.func(obj)
        obj.__dict__[self.name] = value
        return value

class DataAnalyzer:
    def __init__(self, data: list):
        self.data = data
    
    @LazyProperty
    def statistics(self) -> dict:
        """复杂计算 - 只执行一次"""
        print("  计算统计信息...")
        import time
        time.sleep(0.1)  # 模拟耗时计算
        return {
            "count": len(self.data),
            "sum": sum(self.data),
            "avg": sum(self.data) / len(self.data) if self.data else 0,
            "min": min(self.data) if self.data else None,
            "max": max(self.data) if self.data else None,
        }

analyzer = DataAnalyzer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("第一次访问 statistics:")
print(f"  结果: {analyzer.statistics}")
print("第二次访问 statistics (使用缓存):")
print(f"  结果: {analyzer.statistics}")


# ============ 6. 使用 WeakKeyDictionary 的描述符 ============
print("\n" + "=" * 50)
print("6. 使用 WeakKeyDictionary 的描述符")
print("=" * 50)

class WeakTypedProperty:
    """使用弱引用存储的类型检查描述符"""
    
    def __init__(self, expected_type: type):
        self.expected_type = expected_type
        self.data = WeakKeyDictionary()
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.data.get(obj)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} 必须是 {self.expected_type.__name__}")
        self.data[obj] = value

class Account:
    balance = WeakTypedProperty((int, float))
    owner = WeakTypedProperty(str)
    
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance

account = Account("Bob", 1000.0)
print(f"账户: {account.owner}, 余额: {account.balance}")


# ============ 7. 只读描述符 ============
print("\n" + "=" * 50)
print("7. 只读描述符")
print("=" * 50)

class ReadOnly:
    """只读描述符"""
    
    def __init__(self, value):
        self.value = value
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        return self.value
    
    def __set__(self, obj, value):
        raise AttributeError(f"{self.name} 是只读属性")

class Constants:
    PI = ReadOnly(3.14159)
    E = ReadOnly(2.71828)
    
const = Constants()
print(f"PI = {const.PI}")
print(f"E = {const.E}")

try:
    const.PI = 3.14
except AttributeError as e:
    print(f"只读错误: {e}")


# ============ 8. 属性委托 ============
print("\n" + "=" * 50)
print("8. 属性委托")
print("=" * 50)

class Delegate:
    """将属性访问委托给另一个对象"""
    
    def __init__(self, attr_name: str, delegate_attr: str):
        self.attr_name = attr_name
        self.delegate_attr = delegate_attr
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        delegate = getattr(obj, self.delegate_attr)
        return getattr(delegate, self.attr_name)
    
    def __set__(self, obj, value):
        delegate = getattr(obj, self.delegate_attr)
        setattr(delegate, self.attr_name, value)

class Engine:
    def __init__(self):
        self.horsepower = 200
        self.fuel_type = "gasoline"

class Car:
    # 委托到 engine 对象
    horsepower = Delegate("horsepower", "_engine")
    fuel_type = Delegate("fuel_type", "_engine")
    
    def __init__(self):
        self._engine = Engine()
        self.brand = "Toyota"

car = Car()
print(f"汽车品牌: {car.brand}")
print(f"马力(委托): {car.horsepower}")
print(f"燃料(委托): {car.fuel_type}")

car.horsepower = 250
print(f"新马力: {car.horsepower}")


# ============ 9. 描述符与类属性 ============
print("\n" + "=" * 50)
print("9. 描述符与类属性访问")
print("=" * 50)

class ClassLevelDescriptor:
    """同时处理类级别和实例级别访问"""
    
    def __init__(self, default=None):
        self.default = default
        self.data = WeakKeyDictionary()
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            # 类级别访问
            return f"<{self.name}: 类属性, 默认值={self.default}>"
        return self.data.get(obj, self.default)
    
    def __set__(self, obj, value):
        self.data[obj] = value

class Config:
    debug = ClassLevelDescriptor(default=False)
    version = ClassLevelDescriptor(default="1.0.0")

print(f"类级别访问 Config.debug: {Config.debug}")
print(f"类级别访问 Config.version: {Config.version}")

config = Config()
print(f"实例访问 config.debug: {config.debug}")
config.debug = True
print(f"修改后 config.debug: {config.debug}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("描述符与属性总结")
print("=" * 50)
print("""
描述符协议:
- __get__(self, obj, objtype): 获取属性
- __set__(self, obj, value): 设置属性
- __delete__(self, obj): 删除属性
- __set_name__(self, owner, name): 获取属性名

数据描述符 vs 非数据描述符:
- 数据描述符: 实现 __get__ 和 __set__
- 非数据描述符: 只实现 __get__

属性查找顺序:
1. 数据描述符
2. 实例 __dict__
3. 非数据描述符
4. 类 __dict__
5. __getattr__

常用场景:
- 属性验证
- 类型检查
- 惰性计算
- 属性委托
- 只读属性
""")
