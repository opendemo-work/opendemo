#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python面向对象编程基础测试文件
验证类定义、继承、多态、封装等OOP特性的正确性
"""

import pytest
from oop_basics_demo import *

class TestOOPBasics:
    """面向对象编程基础测试类"""
    
    def test_basic_class_creation(self):
        """测试基本类创建"""
        # 创建动物实例
        animal = Animal("测试动物", 5)
        
        # 验证属性
        assert animal.name == "测试动物"
        assert animal.age == 5
        assert isinstance(animal, Animal)
    
    def test_property_decorators(self):
        """测试属性装饰器"""
        animal = Animal("测试", 3)
        
        # 测试getter
        assert animal.name == "测试"
        assert animal.age == 3
        
        # 测试setter
        animal.name = "新名字"
        assert animal.name == "新名字"
        
        animal.age = 5
        assert animal.age == 5
        
        # 测试setter验证
        with pytest.raises(ValueError):
            animal.name = ""  # 空名字应该抛出异常
        
        with pytest.raises(ValueError):
            animal.age = -1  # 负年龄应该抛出异常
    
    def test_inheritance(self):
        """测试继承"""
        # 创建狗实例
        dog = Dog("旺财", 3, "金毛")
        
        # 验证继承关系
        assert isinstance(dog, Dog)
        assert isinstance(dog, Animal)
        assert hasattr(dog, 'speak')
        assert hasattr(dog, 'breed')
    
    def test_polymorphism(self):
        """测试多态"""
        dog = Dog("旺财", 2, "金毛")
        cat = Cat("咪咪", 1, "橘色")
        
        # 验证方法重写
        assert dog.speak() == "旺财汪汪叫"
        assert cat.speak() == "咪咪喵喵叫"
        
        # 验证多态行为
        animals = [dog, cat]
        sounds = [animal.speak() for animal in animals]
        assert len(sounds) == 2
        assert "汪汪叫" in sounds[0]
        assert "喵喵叫" in sounds[1]
    
    def test_encapsulation(self):
        """测试封装"""
        # 测试受保护属性
        animal = Animal("测试", 5)
        assert animal._name == "测试"
        assert animal._age == 5
        
        # 测试私有属性名称改编
        assert hasattr(animal, '_Animal__id')
        
        # 测试属性访问控制
        with pytest.raises(AttributeError):
            animal.__id  # 私有属性无法直接访问
    
    def test_abstract_classes(self):
        """测试抽象类"""
        # 抽象类不能实例化
        with pytest.raises(TypeError):
            Shape()
        
        # 具体类可以实例化
        rectangle = Rectangle(5, 3)
        circle = Circle(4)
        
        # 验证抽象方法实现
        assert rectangle.area() == 15
        assert rectangle.perimeter() == 16
        assert abs(circle.area() - 50.265) < 0.01
        assert abs(circle.perimeter() - 25.133) < 0.01
    
    def test_special_methods(self):
        """测试特殊方法"""
        dog1 = Dog("旺财", 3, "金毛")
        dog2 = Dog("旺财", 3, "金毛")
        dog3 = Dog("小白", 2, "哈士奇")
        
        # 测试__eq__方法
        assert dog1 == dog2
        assert dog1 != dog3
        
        # 测试__str__和__repr__方法
        str_repr = str(dog1)
        repr_repr = repr(dog1)
        assert "Dog" in str_repr
        assert "旺财" in str_repr
        assert "Dog" in repr_repr
    
    def test_class_methods(self):
        """测试类方法"""
        # 重置计数器进行测试
        Animal.species_count = 0
        
        animal1 = Animal("动物1", 1)
        animal2 = Animal("动物2", 2)
        
        # 测试类方法
        assert Animal.get_species_count() == 2
        assert animal1.get_species_count() == 2
        assert animal2.get_species_count() == 2
    
    def test_static_methods(self):
        """测试静态方法"""
        # 测试静态方法
        assert Animal.is_adult(0) == False
        assert Animal.is_adult(1) == False
        assert Animal.is_adult(2) == True
        assert Animal.is_adult(10) == True
    
    def test_bank_account_encapsulation(self):
        """测试银行账户封装"""
        account = BankAccount("张三", 1000)
        
        # 测试只读属性
        assert account.account_holder == "张三"
        initial_balance = account.balance
        assert initial_balance == 1000
        
        # 测试存款
        assert account.deposit(500) == True
        assert account.balance == 1500
        
        # 测试取款
        assert account.withdraw(200) == True
        assert account.balance == 1300
        
        # 测试无效操作
        assert account.withdraw(2000) == False  # 余额不足
        assert account.deposit(-100) == False   # 无效金额
        assert account.balance == 1300  # 余额不变
    
    def test_transaction_history(self):
        """测试交易历史"""
        account = BankAccount("测试用户", 0)
        
        # 执行一些交易
        account.deposit(1000)
        account.withdraw(200)
        account.deposit(500)
        
        # 检查交易历史
        history = account.get_transaction_history()
        assert len(history) == 4  # 开户 + 3笔交易
        assert history[0]['type'] == "开户"
        assert history[1]['type'] == "存款"
        assert history[2]['type'] == "取款"
        assert history[3]['type'] == "存款"
        
        # 验证余额计算正确
        final_balance = history[-1]['balance']
        assert final_balance == account.balance

def run_tests():
    """运行所有测试"""
    pytest.main([__file__, "-v"])

if __name__ == "__main__":
    run_tests()