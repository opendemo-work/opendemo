#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 抽象基类 (ABC) 完整示例
演示 abc 模块的接口定义和抽象方法
"""

from abc import ABC, abstractmethod, abstractproperty
from typing import List, Dict, Any, Protocol, runtime_checkable
from dataclasses import dataclass


# ============ 1. 基本抽象类 ============
print("=" * 50)
print("1. 基本抽象类")
print("=" * 50)

class Shape(ABC):
    """形状抽象基类"""
    
    @abstractmethod
    def area(self) -> float:
        """计算面积 - 必须实现"""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """计算周长 - 必须实现"""
        pass
    
    def describe(self) -> str:
        """具体方法 - 可选覆盖"""
        return f"{self.__class__.__name__}: 面积={self.area():.2f}, 周长={self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# 使用
circle = Circle(5)
rect = Rectangle(4, 6)

print(circle.describe())
print(rect.describe())

# 不能实例化抽象类
try:
    shape = Shape()
except TypeError as e:
    print(f"实例化抽象类报错: {e}")


# ============ 2. 抽象属性 ============
print("\n" + "=" * 50)
print("2. 抽象属性")
print("=" * 50)

class Animal(ABC):
    """动物抽象类 - 带抽象属性"""
    
    @property
    @abstractmethod
    def species(self) -> str:
        """物种名称"""
        pass
    
    @property
    @abstractmethod
    def sound(self) -> str:
        """叫声"""
        pass
    
    def speak(self) -> str:
        return f"{self.species} says: {self.sound}"

class Dog(Animal):
    @property
    def species(self) -> str:
        return "Dog"
    
    @property
    def sound(self) -> str:
        return "Woof!"

class Cat(Animal):
    @property
    def species(self) -> str:
        return "Cat"
    
    @property
    def sound(self) -> str:
        return "Meow!"

dog = Dog()
cat = Cat()
print(dog.speak())
print(cat.speak())


# ============ 3. 抽象类方法和静态方法 ============
print("\n" + "=" * 50)
print("3. 抽象类方法和静态方法")
print("=" * 50)

class Serializable(ABC):
    """可序列化抽象类"""
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Serializable":
        """从字典创建实例"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        pass
    
    @staticmethod
    @abstractmethod
    def validate(data: Dict[str, Any]) -> bool:
        """验证数据"""
        pass

@dataclass
class User(Serializable):
    name: str
    email: str
    age: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "email": self.email, "age": self.age}
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> bool:
        return all(k in data for k in ["name", "email", "age"])

# 使用
data = {"name": "Alice", "email": "alice@example.com", "age": 25}
if User.validate(data):
    user = User.from_dict(data)
    print(f"创建用户: {user}")
    print(f"转为字典: {user.to_dict()}")


# ============ 4. 接口继承 ============
print("\n" + "=" * 50)
print("4. 多接口继承")
print("=" * 50)

class Printable(ABC):
    @abstractmethod
    def print_content(self) -> str:
        pass

class Saveable(ABC):
    @abstractmethod
    def save(self, path: str) -> bool:
        pass

class Loadable(ABC):
    @classmethod
    @abstractmethod
    def load(cls, path: str) -> "Loadable":
        pass

class Document(Printable, Saveable, Loadable):
    """实现多个接口的文档类"""
    
    def __init__(self, content: str):
        self.content = content
    
    def print_content(self) -> str:
        return f"Document: {self.content[:50]}..."
    
    def save(self, path: str) -> bool:
        print(f"  保存到 {path}")
        return True
    
    @classmethod
    def load(cls, path: str) -> "Document":
        print(f"  从 {path} 加载")
        return cls(f"Content from {path}")

doc = Document("Hello, this is a sample document content.")
print(doc.print_content())
doc.save("document.txt")
loaded_doc = Document.load("document.txt")


# ============ 5. Protocol (结构化子类型) ============
print("\n" + "=" * 50)
print("5. Protocol (鸭子类型接口)")
print("=" * 50)

@runtime_checkable
class Drawable(Protocol):
    """可绘制协议 - 结构化子类型"""
    def draw(self) -> str:
        ...

class Square:
    """正方形 - 没有显式继承但实现了draw"""
    def __init__(self, size: int):
        self.size = size
    
    def draw(self) -> str:
        return f"Drawing square of size {self.size}"

class Text:
    """文本 - 也实现了draw"""
    def __init__(self, content: str):
        self.content = content
    
    def draw(self) -> str:
        return f"Drawing text: {self.content}"

def render(drawable: Drawable) -> None:
    """接受任何实现了draw方法的对象"""
    print(f"  {drawable.draw()}")

# 使用
square = Square(10)
text = Text("Hello")

print("渲染图形:")
render(square)
render(text)

# 运行时检查
print(f"\nSquare 是 Drawable: {isinstance(square, Drawable)}")
print(f"Text 是 Drawable: {isinstance(text, Drawable)}")


# ============ 6. 模板方法模式 ============
print("\n" + "=" * 50)
print("6. 模板方法模式")
print("=" * 50)

class DataProcessor(ABC):
    """数据处理器 - 模板方法模式"""
    
    def process(self, data: Any) -> Any:
        """模板方法 - 定义处理流程"""
        validated = self.validate(data)
        if not validated:
            raise ValueError("数据验证失败")
        
        transformed = self.transform(data)
        result = self.output(transformed)
        return result
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """验证数据 - 子类实现"""
        pass
    
    @abstractmethod
    def transform(self, data: Any) -> Any:
        """转换数据 - 子类实现"""
        pass
    
    def output(self, data: Any) -> Any:
        """输出数据 - 可选覆盖"""
        return data

class JSONProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, dict)
    
    def transform(self, data: Any) -> Any:
        import json
        return json.dumps(data)
    
    def output(self, data: Any) -> Any:
        return f"JSON: {data}"

class CSVProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, list) and all(isinstance(row, dict) for row in data)
    
    def transform(self, data: Any) -> Any:
        if not data:
            return ""
        headers = list(data[0].keys())
        rows = [",".join(str(row.get(h, "")) for h in headers) for row in data]
        return "\n".join([",".join(headers)] + rows)

# 使用
json_proc = JSONProcessor()
result = json_proc.process({"name": "Alice", "age": 25})
print(result)

csv_proc = CSVProcessor()
result = csv_proc.process([
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30}
])
print(f"CSV:\n{result}")


# ============ 7. 注册虚拟子类 ============
print("\n" + "=" * 50)
print("7. 注册虚拟子类")
print("=" * 50)

class Container(ABC):
    @abstractmethod
    def __contains__(self, item) -> bool:
        pass
    
    @abstractmethod
    def __len__(self) -> int:
        pass

# 将现有类注册为虚拟子类
Container.register(list)
Container.register(dict)

# 检查
print(f"list 是 Container 的子类: {issubclass(list, Container)}")
print(f"dict 是 Container 的子类: {issubclass(dict, Container)}")

# 注意：虚拟子类不会强制实现抽象方法


# ============ 8. Mixin 模式 ============
print("\n" + "=" * 50)
print("8. Mixin 模式")
print("=" * 50)

class LoggerMixin:
    """日志混入类"""
    def log(self, message: str):
        print(f"[{self.__class__.__name__}] {message}")

class ValidatorMixin:
    """验证混入类"""
    def validate_not_empty(self, value: str, field: str):
        if not value:
            raise ValueError(f"{field} 不能为空")

class Service(LoggerMixin, ValidatorMixin):
    """使用多个Mixin的服务类"""
    
    def create_user(self, name: str, email: str):
        self.log(f"创建用户: {name}")
        self.validate_not_empty(name, "name")
        self.validate_not_empty(email, "email")
        self.log("用户创建成功")
        return {"name": name, "email": email}

service = Service()
user = service.create_user("Alice", "alice@example.com")
print(f"创建的用户: {user}")


# ============ 9. 工厂模式 ============
print("\n" + "=" * 50)
print("9. 抽象工厂模式")
print("=" * 50)

class Database(ABC):
    @abstractmethod
    def connect(self) -> str:
        pass
    
    @abstractmethod
    def query(self, sql: str) -> List[Dict]:
        pass

class MySQLDatabase(Database):
    def connect(self) -> str:
        return "Connected to MySQL"
    
    def query(self, sql: str) -> List[Dict]:
        return [{"source": "MySQL", "sql": sql}]

class PostgreSQLDatabase(Database):
    def connect(self) -> str:
        return "Connected to PostgreSQL"
    
    def query(self, sql: str) -> List[Dict]:
        return [{"source": "PostgreSQL", "sql": sql}]

class DatabaseFactory:
    """数据库工厂"""
    
    _databases = {
        "mysql": MySQLDatabase,
        "postgresql": PostgreSQLDatabase,
    }
    
    @classmethod
    def create(cls, db_type: str) -> Database:
        db_class = cls._databases.get(db_type.lower())
        if not db_class:
            raise ValueError(f"不支持的数据库类型: {db_type}")
        return db_class()

# 使用工厂
db = DatabaseFactory.create("mysql")
print(db.connect())
print(db.query("SELECT * FROM users"))


# ============ 总结 ============
print("\n" + "=" * 50)
print("抽象基类总结")
print("=" * 50)
print("""
ABC vs Protocol:
- ABC: 显式继承，强制实现
- Protocol: 结构化子类型(鸭子类型)

常用场景:
1. 定义接口/契约
2. 模板方法模式
3. 工厂模式
4. 插件系统

最佳实践:
- 优先使用组合而非继承
- 接口应该小而专注
- 使用Protocol更灵活
- Mixin提供可复用功能
""")
