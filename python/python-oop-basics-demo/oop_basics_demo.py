#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python面向对象编程基础演示程序
展示类定义、继承、多态、封装、特殊方法等OOP核心概念
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import inspect

def print_header(title: str) -> None:
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

class Animal:
    """动物基类 - 演示基本类定义和封装"""
    
    # 类变量
    species_count = 0
    
    def __init__(self, name: str, age: int):
        """构造方法"""
        self._name = name  # 受保护属性
        self._age = age    # 受保护属性
        self.__id = Animal.species_count  # 私有属性
        Animal.species_count += 1
    
    # 属性装饰器 - getter
    @property
    def name(self) -> str:
        """获取名字"""
        return self._name
    
    # 属性装饰器 - setter
    @name.setter
    def name(self, value: str) -> None:
        """设置名字"""
        if not value:
            raise ValueError("名字不能为空")
        self._name = value
    
    @property
    def age(self) -> int:
        """获取年龄"""
        return self._age
    
    @age.setter
    def age(self, value: int) -> None:
        """设置年龄"""
        if value < 0:
            raise ValueError("年龄不能为负数")
        self._age = value
    
    def speak(self) -> str:
        """发声方法 - 将被子类重写"""
        return "动物发出声音"
    
    def info(self) -> str:
        """基本信息"""
        return f"我是{self._name}，今年{self._age}岁"
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.__class__.__name__}(name='{self._name}', age={self._age})"
    
    def __repr__(self) -> str:
        """开发者表示"""
        return f"{self.__class__.__name__}('{self._name}', {self._age})"
    
    @classmethod
    def get_species_count(cls) -> int:
        """类方法 - 获取物种计数"""
        return cls.species_count
    
    @staticmethod
    def is_adult(age: int) -> bool:
        """静态方法 - 判断是否成年"""
        return age >= 2

class Dog(Animal):
    """狗类 - 演示继承和多态"""
    
    def __init__(self, name: str, age: int, breed: str):
        """构造方法"""
        super().__init__(name, age)  # 调用父类构造方法
        self.breed = breed
        self._tricks = []  # 狗会的技巧
    
    def speak(self) -> str:
        """重写父类方法 - 多态体现"""
        return f"{self._name}汪汪叫"
    
    def add_trick(self, trick: str) -> None:
        """添加技巧"""
        self._tricks.append(trick)
    
    def list_tricks(self) -> List[str]:
        """列出所有技巧"""
        return self._tricks.copy()
    
    def info(self) -> str:
        """重写并扩展父类方法"""
        base_info = super().info()
        return f"{base_info}，品种是{self.breed}"
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"{super().__str__()[:-1]}, breed='{self.breed}')"
    
    def __eq__(self, other) -> bool:
        """相等比较"""
        if not isinstance(other, Dog):
            return False
        return (self._name == other._name and 
                self._age == other._age and 
                self.breed == other.breed)

class Cat(Animal):
    """猫类 - 演示另一种继承"""
    
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age)
        self.color = color
        self._lives = 9  # 猫有九条命
    
    def speak(self) -> str:
        """重写父类方法"""
        return f"{self._name}喵喵叫"
    
    def info(self) -> str:
        """重写父类方法"""
        base_info = super().info()
        return f"{base_info}，毛色是{self.color}"
    
    @property
    def lives(self) -> int:
        """剩余生命"""
        return self._lives
    
    def lose_life(self) -> bool:
        """失去一条命"""
        if self._lives > 0:
            self._lives -= 1
            return True
        return False

class Shape(ABC):
    """抽象形状类 - 演示抽象基类"""
    
    @abstractmethod
    def area(self) -> float:
        """计算面积 - 抽象方法"""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """计算周长 - 抽象方法"""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

class Rectangle(Shape):
    """矩形类"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        """实现抽象方法"""
        return self.width * self.height
    
    def perimeter(self) -> float:
        """实现抽象方法"""
        return 2 * (self.width + self.height)
    
    def __str__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"

class Circle(Shape):
    """圆形类"""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        """实现抽象方法"""
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        """实现抽象方法"""
        return 2 * 3.14159 * self.radius
    
    def __str__(self) -> str:
        return f"Circle(radius={self.radius})"

class BankAccount:
    """银行账户类 - 演示封装和数据安全"""
    
    def __init__(self, account_holder: str, initial_balance: float = 0):
        self._account_holder = account_holder
        self._balance = initial_balance
        self._transaction_history = []
        self._log_transaction("开户", initial_balance)
    
    @property
    def balance(self) -> float:
        """只读属性 - 余额"""
        return self._balance
    
    @property
    def account_holder(self) -> str:
        """账户持有人"""
        return self._account_holder
    
    def deposit(self, amount: float) -> bool:
        """存款"""
        if amount <= 0:
            print("存款金额必须大于0")
            return False
        
        self._balance += amount
        self._log_transaction("存款", amount)
        print(f"存款成功: ¥{amount:.2f}")
        return True
    
    def withdraw(self, amount: float) -> bool:
        """取款"""
        if amount <= 0:
            print("取款金额必须大于0")
            return False
        
        if amount > self._balance:
            print("余额不足")
            return False
        
        self._balance -= amount
        self._log_transaction("取款", -amount)
        print(f"取款成功: ¥{amount:.2f}")
        return True
    
    def _log_transaction(self, transaction_type: str, amount: float) -> None:
        """私有方法 - 记录交易"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._transaction_history.append({
            'time': timestamp,
            'type': transaction_type,
            'amount': amount,
            'balance': self._balance
        })
    
    def get_transaction_history(self) -> List[Dict]:
        """获取交易历史"""
        return self._transaction_history.copy()
    
    def __str__(self) -> str:
        return f"BankAccount(holder='{self._account_holder}', balance=¥{self._balance:.2f})"

def demonstrate_basic_classes() -> None:
    """演示基本类的使用"""
    print_header("基本类定义和使用演示")
    
    # 创建动物实例
    dog = Dog("旺财", 3, "金毛")
    cat = Cat("咪咪", 2, "橘色")
    
    print("1. 对象创建和基本属性访问:")
    print(f"   {dog}")
    print(f"   {cat}")
    print(f"   狗的名字: {dog.name}")
    print(f"   猫的年龄: {cat.age}")
    
    print("\n2. 方法调用和多态:")
    animals = [dog, cat]
    for animal in animals:
        print(f"   {animal.speak()}")
        print(f"   {animal.info()}")

def demonstrate_inheritance_polymorphism() -> None:
    """演示继承和多态"""
    print_header("继承和多态演示")
    
    # 创建不同类型的动物
    animals = [
        Dog("小白", 2, "哈士奇"),
        Cat("小黑", 1, "黑色"),
        Dog("小黄", 4, "柴犬")
    ]
    
    print("1. 多态行为演示:")
    for animal in animals:
        print(f"   {animal.info()}")
        print(f"   声音: {animal.speak()}")
        print(f"   是否成年: {Animal.is_adult(animal.age)}")
        print()

def demonstrate_encapsulation() -> None:
    """演示封装特性"""
    print_header("封装特性演示")
    
    # 创建银行账户
    account = BankAccount("张三", 1000)
    
    print("1. 封装保护演示:")
    print(f"   账户信息: {account}")
    print(f"   账户持有人: {account.account_holder}")
    print(f"   当前余额: ¥{account.balance:.2f}")
    
    print("\n2. 受控访问演示:")
    account.deposit(500)
    account.withdraw(200)
    account.withdraw(2000)  # 余额不足
    account.deposit(-100)   # 无效金额
    
    print(f"\n   最终余额: ¥{account.balance:.2f}")
    
    print("\n3. 交易历史:")
    history = account.get_transaction_history()
    for transaction in history[-3:]:  # 显示最近3笔交易
        print(f"   {transaction['time']} {transaction['type']}: ¥{transaction['amount']:.2f}, 余额: ¥{transaction['balance']:.2f}")

def demonstrate_abstract_classes() -> None:
    """演示抽象类"""
    print_header("抽象类演示")
    
    # 创建具体形状
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Rectangle(2, 8)
    ]
    
    print("1. 抽象类使用:")
    for shape in shapes:
        print(f"   {shape}")
        print(f"     面积: {shape.area():.2f}")
        print(f"     周长: {shape.perimeter():.2f}")
        print()

def demonstrate_special_methods() -> None:
    """演示特殊方法"""
    print_header("特殊方法演示")
    
    # 比较操作
    dog1 = Dog("旺财", 3, "金毛")
    dog2 = Dog("旺财", 3, "金毛")
    dog3 = Dog("小白", 2, "哈士奇")
    
    print("1. 比较操作:")
    print(f"   dog1 == dog2: {dog1 == dog2}")
    print(f"   dog1 == dog3: {dog1 == dog3}")
    
    # 字符串表示
    print(f"\n2. 字符串表示:")
    print(f"   str(dog1): {str(dog1)}")
    print(f"   repr(dog1): {repr(dog1)}")
    
    # 类方法和静态方法
    print(f"\n3. 类方法和静态方法:")
    print(f"   物种总数: {Animal.get_species_count()}")
    print(f"   1岁是否成年: {Animal.is_adult(1)}")
    print(f"   3岁是否成年: {Animal.is_adult(3)}")

def demonstrate_advanced_features() -> None:
    """演示高级特性"""
    print_header("高级特性演示")
    
    # 属性装饰器
    print("1. 属性装饰器:")
    dog = Dog("测试狗", 2, "测试品种")
    print(f"   原名: {dog.name}")
    
    try:
        dog.name = ""  # 这会引发异常
    except ValueError as e:
        print(f"   设置空名失败: {e}")
    
    dog.name = "新名字"
    print(f"   新名: {dog.name}")
    
    # 私有成员访问
    print(f"\n2. 私有成员:")
    print(f"   公有属性可访问: {dog.breed}")
    print(f"   受保护属性可通过约定访问: {dog._name}")
    print(f"   私有属性名称改编: {dog._Animal__id}")

def main() -> None:
    """主函数"""
    print("🐍 Python面向对象编程基础演示")
    print("=" * 60)
    
    try:
        demonstrate_basic_classes()
        demonstrate_inheritance_polymorphism()
        demonstrate_encapsulation()
        demonstrate_abstract_classes()
        demonstrate_special_methods()
        demonstrate_advanced_features()
        
        print("\n🎉 所有面向对象编程演示完成!")
        print("=" * 60)
        print(f"总共创建了 {Animal.get_species_count()} 个动物对象")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        raise

if __name__ == "__main__":
    main()