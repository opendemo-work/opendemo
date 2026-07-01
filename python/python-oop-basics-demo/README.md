<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Python面向对象编程基础

## 🎯 案例概述

这是一个全面展示Python面向对象编程核心概念的示例，涵盖类定义、继承、多态、封装、抽象类、特殊方法等OOP重要特性。

## 📚 学习目标

通过本示例你将掌握：
- Python类的定义和实例化
- 继承机制和方法重写
- 多态性的实现和应用
- 封装原则和访问控制
- 抽象类和接口的概念
- 特殊方法的使用
- 面向对象设计原则

## 🔧 核心知识点

### 1. 基本类定义
- 类的声明和构造方法
- 实例属性和类属性
- 方法定义和调用
- self参数的作用

### 2. 继承和多态
- 单继承和方法重写
- super()函数的使用
- 多态行为的实现
- isinstance()和issubclass()检查

### 3. 封装特性
- 公有、受保护、私有成员
- 属性装饰器(@property)
- getter和setter方法
- 名称改编机制

### 4. 抽象类
- ABC抽象基类
- @abstractmethod装饰器
- 抽象方法的强制实现
- 接口契约的定义

### 5. 特殊方法
- __init__构造方法
- __str__和__repr__字符串表示
- __eq__相等比较
- 类方法和静态方法

## 🚀 运行示例

```bash
# 运行主程序
python oop_basics_demo.py

# 运行测试
python -m pytest test_oop_basics.py -v
```

## 📖 代码详解

### 主要类结构演示

```python
class Animal:           # 基础类演示
class Dog(Animal):      # 继承演示
class Cat(Animal):      # 多态演示
class Shape(ABC):       # 抽象类演示
class Rectangle(Shape): # 抽象方法实现
class Circle(Shape):    # 另一种实现
class BankAccount:      # 封装演示
```

### 关键技术点演示

#### 1. 基本类定义
```python
class Animal:
    species_count = 0  # 类变量
    
    def __init__(self, name: str, age: int):
        self._name = name    # 受保护属性
        self._age = age      # 受保护属性
        self.__id = Animal.species_count  # 私有属性
        Animal.species_count += 1
    
    def speak(self) -> str:
        return "动物发出声音"
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not value:
            raise ValueError("名字不能为空")
        self._name = value
```

#### 2. 继承和多态
```python
class Dog(Animal):
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)  # 调用父类构造方法
        self.breed = breed
    
    def speak(self) -> str:  # 重写父类方法
        return f"{self._name}汪汪叫"
    
    def info(self) -> str:   # 扩展父类方法
        base_info = super().info()
        return f"{base_info}，品种是{self.breed}"

# 多态使用
animals = [Dog("旺财", 3, "金毛"), Cat("咪咪", 2, "橘色")]
for animal in animals:
    print(animal.speak())  # 不同的实现
```

#### 3. 抽象类实现
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:      # 必须实现抽象方法
        return self.width * self.height
    
    def perimeter(self) -> float: # 必须实现抽象方法
        return 2 * (self.width + self.height)
```

#### 4. 特殊方法使用
```python
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:      # str()调用
        return f"Point({self.x}, {self.y})"
    
    def __repr__(self) -> str:     # repr()调用
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other) -> bool:  # == 操作符
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    @classmethod
    def origin(cls):              # 类方法
        return cls(0, 0)
    
    @staticmethod
    def distance(p1, p2) -> float: # 静态方法
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5
```

#### 5. 封装和数据安全
```python
class BankAccount:
    def __init__(self, account_holder: str, initial_balance: float = 0):
        self._account_holder = account_holder  # 受保护
        self._balance = initial_balance        # 受保护
        self._transaction_history = []         # 私有数据
    
    @property
    def balance(self) -> float:    # 只读属性
        return self._balance
    
    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self._balance += amount
        self._log_transaction("存款", amount)
        return True
    
    def _log_transaction(self, transaction_type: str, amount: float):
        # 私有方法，内部使用
        import datetime
        timestamp = datetime.datetime.now()
        self._transaction_history.append({
            'time': timestamp,
            'type': transaction_type,
            'amount': amount
        })
```

## 🧪 测试覆盖

测试文件 `test_oop_basics.py` 包含以下测试：

✅ 基本类创建测试  
✅ 属性装饰器测试  
✅ 继承机制测试  
✅ 多态行为测试  
✅ 封装特性测试  
✅ 抽象类测试  
✅ 特殊方法测试  
✅ 类方法测试  
✅ 静态方法测试  
✅ 银行账户封装测试  
✅ 交易历史测试  

## 🎯 实际应用场景

### 1. 游戏角色系统
```python
class Character:
    def __init__(self, name: str, health: int):
        self.name = name
        self.health = health
    
    def take_damage(self, damage: int):
        self.health = max(0, self.health - damage)

class Warrior(Character):
    def __init__(self, name: str):
        super().__init__(name, 100)
        self.weapon = "剑"
    
    def attack(self):
        return f"{self.name}用{self.weapon}攻击!"

class Mage(Character):
    def __init__(self, name: str):
        super().__init__(name, 80)
        self.spell = "火球术"
    
    def cast_spell(self):
        return f"{self.name}施展{self.spell}!"
```

### 2. 数据处理管道
```python
class DataProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass

class CSVProcessor(DataProcessor):
    def process(self, data):
        # CSV处理逻辑
        return processed_csv_data

class JSONProcessor(DataProcessor):
    def process(self, data):
        # JSON处理逻辑
        return processed_json_data

class DataPipeline:
    def __init__(self):
        self.processors = []
    
    def add_processor(self, processor: DataProcessor):
        self.processors.append(processor)
    
    def process_data(self, data):
        result = data
        for processor in self.processors:
            result = processor.process(result)
        return result
```

### 3. 插件系统
```python
class Plugin(ABC):
    @abstractmethod
    def activate(self):
        pass
    
    @abstractmethod
    def deactivate(self):
        pass

class LoggingPlugin(Plugin):
    def activate(self):
        print("日志插件已激活")
    
    def deactivate(self):
        print("日志插件已停用")

class SecurityPlugin(Plugin):
    def activate(self):
        print("安全插件已激活")
    
    def deactivate(self):
        print("安全插件已停用")

class Application:
    def __init__(self):
        self.plugins = []
    
    def register_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)
    
    def start(self):
        for plugin in self.plugins:
            plugin.activate()
```

## ⚡ 最佳实践建议

### 1. 类设计原则
- 遵循单一职责原则
- 合理使用继承层次
- 优先组合而非继承
- 接口隔离原则

### 2. 封装建议
- 私有属性使用双下划线前缀
- 受保护属性使用单下划线前缀
- 公有接口保持简洁稳定
- 内部实现细节对外隐藏

### 3. 继承使用
- 继承用于"is-a"关系
- 组合用于"has-a"关系
- 避免过深的继承层次
- 优先使用抽象基类

## 🔍 常见问题和解决方案

### 1. 多重继承菱形问题
```python
# 问题：多重继承可能导致方法解析顺序混乱
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()

class C(A):
    def method(self):
        print("C")
        super().method()

class D(B, C):
    def method(self):
        print("D")
        super().method()

# 解决：使用MRO(Method Resolution Order)
print(D.__mro__)  # 查看方法解析顺序
```

### 2. 抽象方法未实现
```python
# 问题：子类没有实现抽象方法
from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def required_method(self):
        pass

# class Concrete(Base):  # 这会导致TypeError
#     pass

# 解决：确保实现所有抽象方法
class Concrete(Base):
    def required_method(self):
        return "已实现"
```

### 3. 私有属性访问
```python
# 问题：试图访问私有属性
class Test:
    def __init__(self):
        self.__private = "私有"

obj = Test()
# print(obj.__private)  # AttributeError

# 解决：使用名称改编或提供公共接口
print(obj._Test__private)  # 通过名称改编访问
# 或者提供属性方法
```

## 📚 扩展学习资源

### 官方文档
- [Python数据模型](https://docs.python.org/3/reference/datamodel.html)
- [abc模块](https://docs.python.org/3/library/abc.html)

### 推荐书籍
- 《Python Tricks》
- 《Effective Python》
- 《设计模式：可复用面向对象软件的基础》

### 相关主题
- 设计模式在Python中的应用
- 元类和描述符
- 数据类(dataclasses)
- 类型提示

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含完整的OOP基础演示

---
**注意**: 面向对象编程是Python的核心特性之一，深入理解和熟练运用这些概念对编写高质量Python代码至关重要。
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
