#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 数据类 (dataclasses) 完整示例
演示 Python 3.7+ 引入的 dataclass 装饰器
"""

from dataclasses import dataclass, field, asdict, astuple, replace, fields
from typing import List, Optional, ClassVar
from datetime import datetime
import json


# ============ 1. 基本数据类 ============
print("=" * 50)
print("1. 基本数据类定义")
print("=" * 50)

@dataclass
class Point:
    """简单的二维点"""
    x: float
    y: float

@dataclass
class Person:
    """包含多种类型字段的数据类"""
    name: str
    age: int
    email: str

# 自动生成 __init__, __repr__, __eq__
p1 = Point(3.0, 4.0)
p2 = Point(3.0, 4.0)
person = Person("Alice", 25, "alice@example.com")

print(f"Point(3.0, 4.0) = {p1}")
print(f"p1 == p2: {p1 == p2}")  # 自动生成的 __eq__
print(f"Person: {person}")


# ============ 2. 默认值和默认工厂 ============
print("\n" + "=" * 50)
print("2. 默认值和默认工厂")
print("=" * 50)

@dataclass
class Config:
    """带默认值的配置类"""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    # 可变默认值必须使用 field(default_factory=...)
    allowed_hosts: List[str] = field(default_factory=list)
    
    # 带有默认工厂的时间戳
    created_at: datetime = field(default_factory=datetime.now)

config1 = Config()
config2 = Config(host="0.0.0.0", port=80, debug=True)
config2.allowed_hosts.append("example.com")

print(f"默认配置: {config1}")
print(f"自定义配置: {config2}")
print(f"config1.allowed_hosts is config2.allowed_hosts: {config1.allowed_hosts is config2.allowed_hosts}")


# ============ 3. 字段选项 ============
print("\n" + "=" * 50)
print("3. 字段选项 (field)")
print("=" * 50)

@dataclass
class Product:
    """展示各种字段选项"""
    name: str
    price: float
    
    # repr=False: 不在 repr 中显示
    internal_id: str = field(repr=False)
    
    # compare=False: 不参与比较
    description: str = field(default="", compare=False)
    
    # init=False: 不在 __init__ 中包含
    created_at: datetime = field(init=False, default_factory=datetime.now)
    
    # 类变量（不是实例字段）
    category: ClassVar[str] = "General"

product = Product("Laptop", 999.99, "SKU-12345", "A great laptop")
print(f"Product: {product}")
print(f"internal_id: {product.internal_id}")
print(f"created_at: {product.created_at}")
print(f"类变量 category: {Product.category}")


# ============ 4. 不可变数据类 (frozen) ============
print("\n" + "=" * 50)
print("4. 不可变数据类 (frozen)")
print("=" * 50)

@dataclass(frozen=True)
class Coordinate:
    """不可变坐标 - 创建后无法修改"""
    latitude: float
    longitude: float
    
    def distance_from_origin(self) -> float:
        """可以定义方法"""
        return (self.latitude ** 2 + self.longitude ** 2) ** 0.5

coord = Coordinate(40.7128, -74.0060)
print(f"坐标: {coord}")
print(f"距原点距离: {coord.distance_from_origin():.2f}")

# 尝试修改会抛出异常
try:
    coord.latitude = 0  # type: ignore
except Exception as e:
    print(f"修改frozen数据类时报错: {type(e).__name__}")

# frozen数据类可以作为字典键或集合元素
coord_set = {coord, Coordinate(34.0522, -118.2437)}
print(f"坐标集合大小: {len(coord_set)}")


# ============ 5. 排序支持 (order) ============
print("\n" + "=" * 50)
print("5. 排序支持 (order)")
print("=" * 50)

@dataclass(order=True)
class Version:
    """支持比较和排序的版本号"""
    major: int
    minor: int
    patch: int
    
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

versions = [
    Version(2, 0, 0),
    Version(1, 9, 5),
    Version(1, 10, 0),
    Version(2, 1, 3),
]

print("原始版本列表:")
for v in versions:
    print(f"  {v}")

print("\n排序后:")
for v in sorted(versions):
    print(f"  {v}")

print(f"\n最新版本: {max(versions)}")


# ============ 6. 后处理 (__post_init__) ============
print("\n" + "=" * 50)
print("6. 后处理 (__post_init__)")
print("=" * 50)

@dataclass
class Rectangle:
    """带后处理的矩形类"""
    width: float
    height: float
    area: float = field(init=False)
    perimeter: float = field(init=False)
    
    def __post_init__(self):
        """在 __init__ 之后自动调用"""
        self.area = self.width * self.height
        self.perimeter = 2 * (self.width + self.height)
        
        # 验证
        if self.width <= 0 or self.height <= 0:
            raise ValueError("宽度和高度必须为正数")

rect = Rectangle(5.0, 3.0)
print(f"矩形: {rect}")
print(f"面积: {rect.area}, 周长: {rect.perimeter}")


# ============ 7. 继承 ============
print("\n" + "=" * 50)
print("7. 数据类继承")
print("=" * 50)

@dataclass
class Animal:
    """动物基类"""
    name: str
    age: int

@dataclass
class Dog(Animal):
    """狗类 - 继承自动物"""
    breed: str
    is_trained: bool = False

@dataclass
class Cat(Animal):
    """猫类 - 继承自动物"""
    color: str
    indoor: bool = True

dog = Dog("Buddy", 3, "Golden Retriever", True)
cat = Cat("Whiskers", 2, "Orange")

print(f"Dog: {dog}")
print(f"Cat: {cat}")


# ============ 8. 工具函数 ============
print("\n" + "=" * 50)
print("8. 工具函数: asdict, astuple, replace, fields")
print("=" * 50)

@dataclass
class User:
    name: str
    email: str
    age: int

user = User("Bob", "bob@example.com", 30)

# asdict: 转换为字典
user_dict = asdict(user)
print(f"asdict(user) = {user_dict}")

# astuple: 转换为元组
user_tuple = astuple(user)
print(f"astuple(user) = {user_tuple}")

# replace: 创建修改后的副本
new_user = replace(user, name="Robert", age=31)
print(f"replace(user, name='Robert') = {new_user}")
print(f"原user不变: {user}")

# fields: 获取字段信息
print("\n字段信息:")
for f in fields(user):
    print(f"  {f.name}: {f.type.__name__}, default={f.default}")


# ============ 9. JSON 序列化 ============
print("\n" + "=" * 50)
print("9. JSON 序列化")
print("=" * 50)

@dataclass
class Order:
    """订单数据类"""
    order_id: str
    customer: str
    items: List[str]
    total: float
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "Order":
        """从JSON字符串创建"""
        data = json.loads(json_str)
        return cls(**data)

order = Order("ORD-001", "Alice", ["Item1", "Item2", "Item3"], 150.50)
json_str = order.to_json()
print(f"订单JSON:\n{json_str}")

# 反序列化
restored_order = Order.from_json(json_str)
print(f"\n反序列化: {restored_order}")
print(f"与原对象相等: {order == restored_order}")


# ============ 10. 实际应用示例 ============
print("\n" + "=" * 50)
print("10. 实际应用: API请求/响应模型")
print("=" * 50)

@dataclass
class APIRequest:
    """API请求模型"""
    endpoint: str
    method: str = "GET"
    headers: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    body: Optional[dict] = None
    timeout: int = 30

@dataclass
class APIResponse:
    """API响应模型"""
    status_code: int
    data: dict
    headers: dict = field(default_factory=dict)
    elapsed_ms: float = 0.0
    
    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300
    
    @property
    def is_error(self) -> bool:
        return self.status_code >= 400

# 模拟API调用
request = APIRequest(
    endpoint="/api/users",
    method="POST",
    headers={"Content-Type": "application/json"},
    body={"name": "Alice", "email": "alice@example.com"}
)

response = APIResponse(
    status_code=201,
    data={"id": 1, "name": "Alice", "email": "alice@example.com"},
    elapsed_ms=45.2
)

print(f"请求: {request}")
print(f"响应: {response}")
print(f"请求成功: {response.is_success}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("dataclass 使用总结")
print("=" * 50)
print("""
主要特性:
1. 自动生成 __init__, __repr__, __eq__ 等方法
2. 支持默认值和默认工厂
3. frozen=True 创建不可变对象
4. order=True 支持比较排序
5. __post_init__ 进行后处理

常用装饰器参数:
- frozen: 不可变
- order: 支持排序
- eq: 生成 __eq__
- repr: 生成 __repr__
- init: 生成 __init__

工具函数:
- asdict(): 转为字典
- astuple(): 转为元组
- replace(): 创建修改副本
- fields(): 获取字段信息

最佳实践:
- DTO/值对象使用 dataclass
- 可变默认值用 field(default_factory=...)
- 需要哈希时使用 frozen=True
""")
