#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 类型注解 (Type Hints) 完整示例
演示 Python 3.5+ 引入的类型提示系统
"""

from typing import (
    List, Dict, Set, Tuple, Optional, Union, Any,
    Callable, TypeVar, Generic, Literal, Final,
    Iterator, Iterable, Sequence, Mapping
)
from dataclasses import dataclass
from abc import ABC, abstractmethod


# ============ 1. 基本类型注解 ============
print("=" * 50)
print("1. 基本类型注解")
print("=" * 50)

def greet(name: str) -> str:
    """基本的参数和返回值类型注解"""
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    """数值类型注解"""
    return a + b

def is_valid(value: float) -> bool:
    """布尔返回类型"""
    return value > 0

# 变量类型注解
age: int = 25
price: float = 19.99
name: str = "Python"
is_active: bool = True

print(f"greet('World') = {greet('World')}")
print(f"add(10, 20) = {add(10, 20)}")
print(f"is_valid(3.14) = {is_valid(3.14)}")


# ============ 2. 容器类型注解 ============
print("\n" + "=" * 50)
print("2. 容器类型注解")
print("=" * 50)

def process_names(names: List[str]) -> List[str]:
    """列表类型注解"""
    return [name.upper() for name in names]

def get_user_ages(users: Dict[str, int]) -> List[int]:
    """字典类型注解"""
    return list(users.values())

def unique_numbers(nums: List[int]) -> Set[int]:
    """集合类型注解"""
    return set(nums)

def get_coordinates() -> Tuple[float, float, float]:
    """元组类型注解（固定长度和类型）"""
    return (1.0, 2.5, 3.7)

# Python 3.9+ 可以直接使用内置类型
# def process_names(names: list[str]) -> list[str]:

names = ["alice", "bob", "charlie"]
users = {"alice": 25, "bob": 30, "charlie": 35}

print(f"process_names({names}) = {process_names(names)}")
print(f"get_user_ages({users}) = {get_user_ages(users)}")
print(f"unique_numbers([1,2,2,3,3,3]) = {unique_numbers([1,2,2,3,3,3])}")
print(f"get_coordinates() = {get_coordinates()}")


# ============ 3. Optional 和 Union 类型 ============
print("\n" + "=" * 50)
print("3. Optional 和 Union 类型")
print("=" * 50)

def find_user(user_id: int) -> Optional[str]:
    """Optional[X] 等价于 Union[X, None]"""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

def parse_value(value: Union[str, int, float]) -> str:
    """Union 类型：可以是多种类型之一"""
    return str(value)

# Python 3.10+ 可以使用 | 语法
# def parse_value(value: str | int | float) -> str:

print(f"find_user(1) = {find_user(1)}")
print(f"find_user(99) = {find_user(99)}")
print(f"parse_value(42) = {parse_value(42)}")
print(f"parse_value('hello') = {parse_value('hello')}")


# ============ 4. Callable 类型 ============
print("\n" + "=" * 50)
print("4. Callable 类型（函数类型）")
print("=" * 50)

def apply_operation(
    x: int, 
    y: int, 
    operation: Callable[[int, int], int]
) -> int:
    """Callable[[参数类型], 返回类型]"""
    return operation(x, y)

def multiply(a: int, b: int) -> int:
    return a * b

def power(a: int, b: int) -> int:
    return a ** b

print(f"apply_operation(3, 4, multiply) = {apply_operation(3, 4, multiply)}")
print(f"apply_operation(2, 5, power) = {apply_operation(2, 5, power)}")


# ============ 5. TypeVar 泛型 ============
print("\n" + "=" * 50)
print("5. TypeVar 泛型")
print("=" * 50)

T = TypeVar('T')  # 任意类型
N = TypeVar('N', int, float)  # 受限类型

def first_element(items: List[T]) -> Optional[T]:
    """泛型函数：保持类型一致性"""
    return items[0] if items else None

def double(value: N) -> N:
    """受限泛型：只接受 int 或 float"""
    return value * 2

print(f"first_element([1, 2, 3]) = {first_element([1, 2, 3])}")
print(f"first_element(['a', 'b']) = {first_element(['a', 'b'])}")
print(f"double(5) = {double(5)}")
print(f"double(3.14) = {double(3.14)}")


# ============ 6. Generic 泛型类 ============
print("\n" + "=" * 50)
print("6. Generic 泛型类")
print("=" * 50)

T = TypeVar('T')

class Stack(Generic[T]):
    """泛型栈实现"""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        return self._items.pop() if self._items else None
    
    def peek(self) -> Optional[T]:
        return self._items[-1] if self._items else None
    
    def __len__(self) -> int:
        return len(self._items)

# 使用泛型类
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
int_stack.push(3)

str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")

print(f"int_stack.pop() = {int_stack.pop()}")
print(f"str_stack.pop() = {str_stack.pop()}")


# ============ 7. Literal 和 Final 类型 ============
print("\n" + "=" * 50)
print("7. Literal 和 Final 类型")
print("=" * 50)

def set_mode(mode: Literal["read", "write", "append"]) -> str:
    """Literal：限制参数只能是特定值"""
    return f"Mode set to: {mode}"

MAX_SIZE: Final[int] = 100  # Final: 常量，不可修改
APP_NAME: Final = "MyApp"   # 类型可推断

print(f"set_mode('read') = {set_mode('read')}")
print(f"MAX_SIZE = {MAX_SIZE}")
print(f"APP_NAME = {APP_NAME}")


# ============ 8. 类方法类型注解 ============
print("\n" + "=" * 50)
print("8. 类方法类型注解")
print("=" * 50)

class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def get_info(self) -> str:
        return f"{self.name} ({self.age})"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """类方法返回类实例"""
        return cls(data["name"], data["age"])
    
    @staticmethod
    def validate_age(age: int) -> bool:
        """静态方法"""
        return 0 <= age <= 150

user = User("Alice", 25)
user2 = User.from_dict({"name": "Bob", "age": 30})
print(f"user.get_info() = {user.get_info()}")
print(f"user2.get_info() = {user2.get_info()}")
print(f"User.validate_age(25) = {User.validate_age(25)}")


# ============ 9. 协议和抽象类型 ============
print("\n" + "=" * 50)
print("9. 抽象类型注解")
print("=" * 50)

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        """抽象方法必须被实现"""
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

def make_speak(animal: Animal) -> str:
    """接受抽象基类类型"""
    return animal.speak()

dog = Dog()
cat = Cat()
print(f"make_speak(dog) = {make_speak(dog)}")
print(f"make_speak(cat) = {make_speak(cat)}")


# ============ 10. 实际应用示例 ============
print("\n" + "=" * 50)
print("10. 实际应用示例：API响应处理")
print("=" * 50)

from typing import TypedDict

class UserResponse(TypedDict):
    """TypedDict：定义字典结构"""
    id: int
    name: str
    email: str
    is_active: bool

def process_api_response(response: UserResponse) -> str:
    """处理API响应"""
    if response["is_active"]:
        return f"Active user: {response['name']} ({response['email']})"
    return f"Inactive user: {response['name']}"

api_response: UserResponse = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "is_active": True
}

print(f"处理结果: {process_api_response(api_response)}")


# ============ 类型检查提示 ============
print("\n" + "=" * 50)
print("类型检查工具使用提示")
print("=" * 50)
print("""
常用类型检查工具:
1. mypy: pip install mypy && mypy your_script.py
2. pyright: pip install pyright && pyright your_script.py
3. IDE集成: PyCharm/VSCode 内置类型检查

运行时类型检查:
- pydantic: 数据验证库
- beartype: 运行时类型检查装饰器

最佳实践:
1. 公共API应该添加类型注解
2. 复杂类型使用类型别名
3. 使用 TypedDict 代替复杂字典
4. 善用 Optional 处理可能为 None 的值
""")
