#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python变量和数据类型测试文件
验证变量赋值、数据类型、类型转换等功能的正确性
"""

import pytest
from variables_types_demo import *

class TestVariablesTypes:
    """变量和数据类型测试类"""
    
    def test_variable_assignment(self):
        """测试变量赋值"""
        # 基本赋值
        name = "测试"
        age = 25
        height = 175.5
        is_active = True
        
        assert isinstance(name, str)
        assert isinstance(age, int)
        assert isinstance(height, float)
        assert isinstance(is_active, bool)
        
        # 多重赋值
        x = y = z = 10
        assert x == y == z == 10
        
        # 元组解包
        a, b, c = 1, 2, 3
        assert a == 1 and b == 2 and c == 3
        
        # 变量交换
        a, b = b, a
        assert a == 2 and b == 1
    
    def test_numeric_types(self):
        """测试数值类型"""
        # 整数类型
        integer = 42
        negative = -17
        binary = 0b1010  # 10
        octal = 0o755    # 493
        hex_num = 0xFF   # 255
        
        assert isinstance(integer, int)
        assert isinstance(negative, int)
        assert binary == 10
        assert octal == 493
        assert hex_num == 255
        
        # 浮点数类型
        float_num = 3.14159
        scientific = 1.23e-4
        infinity = float('inf')
        
        assert isinstance(float_num, float)
        assert isinstance(scientific, float)
        assert scientific == 0.000123
        
        # 复数类型
        complex_num = 3 + 4j
        assert isinstance(complex_num, complex)
        assert complex_num.real == 3
        assert complex_num.imag == 4
        
        # 布尔类型
        assert isinstance(True, bool)
        assert isinstance(False, bool)
        assert int(True) == 1
        assert int(False) == 0
    
    def test_sequence_types(self):
        """测试序列类型"""
        # 字符串
        string = "Hello World"
        assert isinstance(string, str)
        assert len(string) == 11
        assert string[0] == 'H'
        assert string[-1] == 'd'
        
        # 列表
        list_data = [1, 2, 3, 4, 5]
        assert isinstance(list_data, list)
        assert len(list_data) == 5
        assert list_data[0] == 1
        assert list_data[-1] == 5
        
        # 可变性测试
        list_data.append(6)
        assert len(list_data) == 6
        assert list_data[-1] == 6
        
        # 元组
        tuple_data = (1, 2, 3)
        assert isinstance(tuple_data, tuple)
        assert len(tuple_data) == 3
        assert tuple_data[0] == 1
        
        # 元组不可变性测试
        with pytest.raises(TypeError):
            tuple_data[0] = 10  # 这会抛出TypeError
    
    def test_mapping_types(self):
        """测试映射类型"""
        # 字典
        dict_data = {'name': '张三', 'age': 25}
        assert isinstance(dict_data, dict)
        assert len(dict_data) == 2
        assert dict_data['name'] == '张三'
        assert dict_data['age'] == 25
        
        # 字典操作
        dict_data['city'] = '北京'
        assert len(dict_data) == 3
        assert 'city' in dict_data
        
        del dict_data['age']
        assert len(dict_data) == 2
        assert 'age' not in dict_data
    
    def test_set_types(self):
        """测试集合类型"""
        # 集合
        set_data = {1, 2, 3, 4, 5}
        assert isinstance(set_data, set)
        assert len(set_data) == 5
        
        # 集合去重特性
        duplicate_set = {1, 2, 2, 3, 3, 3}
        assert len(duplicate_set) == 3
        assert duplicate_set == {1, 2, 3}
        
        # 集合操作
        set_a = {1, 2, 3}
        set_b = {3, 4, 5}
        
        assert set_a | set_b == {1, 2, 3, 4, 5}  # 并集
        assert set_a & set_b == {3}              # 交集
        assert set_a - set_b == {1, 2}           # 差集
        assert set_a ^ set_b == {1, 2, 4, 5}     # 对称差集
    
    def test_type_conversion(self):
        """测试类型转换"""
        # 数值转换
        assert int('123') == 123
        assert float('3.14') == 3.14
        assert str(42) == '42'
        
        # 序列转换
        assert list('hello') == ['h', 'e', 'l', 'l', 'o']
        assert tuple([1, 2, 3]) == (1, 2, 3)
        assert set([1, 2, 2, 3]) == {1, 2, 3}
        
        # 布尔转换
        assert bool(0) == False
        assert bool(1) == True
        assert bool('') == False
        assert bool('hello') == True
        assert bool([]) == False
        assert bool([1, 2, 3]) == True
    
    def test_type_checking(self):
        """测试类型检查"""
        # isinstance测试
        assert isinstance(42, int)
        assert isinstance(3.14, (int, float))
        assert isinstance("hello", str)
        assert isinstance([1, 2, 3], list)
        assert isinstance({'key': 'value'}, dict)
        
        # type测试
        assert type(42) == int
        assert type([1, 2, 3]) == list
        assert type({'a': 1}) == dict
    
    def test_memory_management(self):
        """测试内存管理特性"""
        # 引用同一对象
        a = [1, 2, 3]
        b = a
        assert a is b  # 同一对象
        assert id(a) == id(b)
        
        # 创建新对象
        c = [1, 2, 3]
        assert a == c  # 值相等
        assert a is not c  # 不同对象
        assert id(a) != id(c)
        
        # 不可变对象的行为
        x = "hello"
        y = x
        x += " world"
        assert y == "hello"  # 原字符串未改变
        assert x == "hello world"
        
        # 可变对象的行为
        list1 = [1, 2, 3]
        list2 = list1
        list1.append(4)
        assert list2 == [1, 2, 3, 4]  # 同一对象被修改

def run_tests():
    """运行所有测试"""
    pytest.main([__file__, "-v"])

if __name__ == "__main__":
    run_tests()