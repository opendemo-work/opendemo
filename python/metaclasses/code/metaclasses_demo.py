#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 元类 (Metaclasses) 完整示例
演示元类的概念和高级用法
"""

from typing import Dict, Any, Callable, Type


# ============ 1. 类也是对象 ============
print("=" * 50)
print("1. 类也是对象")
print("=" * 50)

class MyClass:
    pass

# 类是 type 的实例
print(f"MyClass 是对象: {isinstance(MyClass, type)}")
print(f"MyClass 的类型: {type(MyClass)}")
print(f"MyClass 的类型的类型: {type(type(MyClass))}")

# 动态创建类
DynamicClass = type("DynamicClass", (), {"value": 42, "greet": lambda self: "Hello!"})
obj = DynamicClass()
print(f"动态类实例: {obj.value}, {obj.greet()}")


# ============ 2. type 创建类 ============
print("\n" + "=" * 50)
print("2. 使用 type 动态创建类")
print("=" * 50)

def init(self, name):
    self.name = name

def say_hello(self):
    return f"Hello, {self.name}!"

# type(name, bases, dict)
Person = type(
    "Person",           # 类名
    (),                 # 基类元组
    {                   # 属性和方法字典
        "__init__": init,
        "say_hello": say_hello,
        "species": "Human"
    }
)

person = Person("Alice")
print(f"动态创建的Person类: {person.say_hello()}")
print(f"类属性: {Person.species}")


# ============ 3. 基本元类 ============
print("\n" + "=" * 50)
print("3. 基本元类定义")
print("=" * 50)

class SimpleMeta(type):
    """简单元类 - 拦截类的创建"""
    
    def __new__(mcs, name, bases, namespace):
        print(f"  [元类] 创建类: {name}")
        # 在类创建之前可以修改 namespace
        namespace["created_by"] = "SimpleMeta"
        return super().__new__(mcs, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace):
        print(f"  [元类] 初始化类: {name}")
        super().__init__(name, bases, namespace)

class MyClass(metaclass=SimpleMeta):
    def method(self):
        return "Hello"

print(f"created_by: {MyClass.created_by}")
print(f"MyClass 的元类: {type(MyClass)}")


# ============ 4. 单例元类 ============
print("\n" + "=" * 50)
print("4. 单例模式元类")
print("=" * 50)

class SingletonMeta(type):
    """单例元类 - 确保只有一个实例"""
    _instances: Dict[type, Any] = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected"
        print("  数据库初始化")

db1 = Database()
db2 = Database()
print(f"db1 is db2: {db1 is db2}")
print(f"连接状态: {db1.connection}")


# ============ 5. 注册元类 ============
print("\n" + "=" * 50)
print("5. 注册模式元类")
print("=" * 50)

class PluginMeta(type):
    """插件注册元类"""
    registry: Dict[str, type] = {}
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # 注册非基类
        if name != "Plugin":
            mcs.registry[name] = cls
        return cls
    
    @classmethod
    def get_plugin(mcs, name: str):
        return mcs.registry.get(name)
    
    @classmethod
    def list_plugins(mcs):
        return list(mcs.registry.keys())

class Plugin(metaclass=PluginMeta):
    """插件基类"""
    pass

class JSONPlugin(Plugin):
    def process(self, data):
        return f"JSON处理: {data}"

class XMLPlugin(Plugin):
    def process(self, data):
        return f"XML处理: {data}"

class CSVPlugin(Plugin):
    def process(self, data):
        return f"CSV处理: {data}"

print(f"已注册插件: {PluginMeta.list_plugins()}")

# 动态获取并使用插件
plugin_cls = PluginMeta.get_plugin("JSONPlugin")
if plugin_cls:
    plugin = plugin_cls()
    print(plugin.process({"key": "value"}))


# ============ 6. 验证元类 ============
print("\n" + "=" * 50)
print("6. 验证元类")
print("=" * 50)

class ValidatedMeta(type):
    """验证类定义的元类"""
    
    required_methods = ["save", "load"]
    
    def __new__(mcs, name, bases, namespace):
        # 跳过基类验证
        if name == "Persistable":
            return super().__new__(mcs, name, bases, namespace)
        
        # 验证必需方法
        for method in mcs.required_methods:
            if method not in namespace:
                raise TypeError(f"类 {name} 必须实现 {method} 方法")
        
        return super().__new__(mcs, name, bases, namespace)

class Persistable(metaclass=ValidatedMeta):
    """可持久化基类"""
    pass

class UserModel(Persistable):
    def save(self):
        return "保存用户"
    
    def load(self):
        return "加载用户"

print(f"UserModel 验证通过: {UserModel().save()}")

# 缺少方法会报错
try:
    class InvalidModel(Persistable):
        def save(self):
            pass
        # 缺少 load 方法
except TypeError as e:
    print(f"验证失败: {e}")


# ============ 7. 属性自动添加元类 ============
print("\n" + "=" * 50)
print("7. 自动属性元类")
print("=" * 50)

class AutoPropertyMeta(type):
    """自动为私有属性创建 property"""
    
    def __new__(mcs, name, bases, namespace):
        # 找出所有带下划线的属性
        private_attrs = [
            attr for attr in namespace.get("__annotations__", {})
            if attr.startswith("_") and not attr.startswith("__")
        ]
        
        for attr in private_attrs:
            public_name = attr[1:]  # 去掉下划线
            
            # 创建 getter
            def getter(self, attr=attr):
                return getattr(self, attr)
            
            # 创建 setter
            def setter(self, value, attr=attr):
                setattr(self, attr, value)
            
            namespace[public_name] = property(getter, setter)
        
        return super().__new__(mcs, name, bases, namespace)

class AutoPerson(metaclass=AutoPropertyMeta):
    _name: str
    _age: int
    
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

person = AutoPerson("Bob", 30)
print(f"name (通过property): {person.name}")
print(f"age (通过property): {person.age}")
person.name = "Robert"
print(f"修改后: {person.name}")


# ============ 8. ORM 元类示例 ============
print("\n" + "=" * 50)
print("8. 简单 ORM 元类")
print("=" * 50)

class Field:
    """字段描述符"""
    def __init__(self, column_type: str, primary_key: bool = False):
        self.column_type = column_type
        self.primary_key = primary_key
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name

class ModelMeta(type):
    """ORM 模型元类"""
    
    def __new__(mcs, name, bases, namespace):
        # 跳过基类
        if name == "Model":
            return super().__new__(mcs, name, bases, namespace)
        
        # 收集字段
        fields = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                fields[key] = value
        
        namespace["_fields"] = fields
        namespace["_table_name"] = name.lower() + "s"
        
        return super().__new__(mcs, name, bases, namespace)

class Model(metaclass=ModelMeta):
    """ORM 基类"""
    
    @classmethod
    def create_table_sql(cls) -> str:
        columns = []
        for name, field in cls._fields.items():
            col = f"{name} {field.column_type}"
            if field.primary_key:
                col += " PRIMARY KEY"
            columns.append(col)
        return f"CREATE TABLE {cls._table_name} ({', '.join(columns)})"

class User(Model):
    id = Field("INTEGER", primary_key=True)
    name = Field("VARCHAR(100)")
    email = Field("VARCHAR(200)")

print(f"表名: {User._table_name}")
print(f"字段: {list(User._fields.keys())}")
print(f"建表SQL: {User.create_table_sql()}")


# ============ 9. __init_subclass__ 替代方案 ============
print("\n" + "=" * 50)
print("9. __init_subclass__ (Python 3.6+)")
print("=" * 50)

class PluginBase:
    """使用 __init_subclass__ 的插件基类"""
    plugins: Dict[str, type] = {}
    
    def __init_subclass__(cls, plugin_name: str = None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        cls.plugins[name] = cls
        print(f"  注册插件: {name}")

class AudioPlugin(PluginBase, plugin_name="audio"):
    def play(self):
        return "播放音频"

class VideoPlugin(PluginBase, plugin_name="video"):
    def play(self):
        return "播放视频"

print(f"已注册插件: {list(PluginBase.plugins.keys())}")


# ============ 10. 元类与继承 ============
print("\n" + "=" * 50)
print("10. 元类继承规则")
print("=" * 50)

class MetaA(type):
    pass

class MetaB(MetaA):
    pass

class A(metaclass=MetaA):
    pass

class B(A, metaclass=MetaB):
    """子类可以使用父类元类的子类"""
    pass

print(f"A 的元类: {type(A).__name__}")
print(f"B 的元类: {type(B).__name__}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("元类总结")
print("=" * 50)
print("""
元类关键点:
- 元类是类的类
- type 是默认元类
- metaclass=xxx 指定元类

元类方法:
- __new__: 创建类对象
- __init__: 初始化类对象
- __call__: 创建实例时调用

常用场景:
1. 单例模式
2. 类注册/插件系统
3. ORM/数据验证
4. API框架
5. 抽象基类

替代方案:
- __init_subclass__: 简单的子类钩子
- 类装饰器: 修改类定义
- 描述符: 属性控制

建议:
- 优先使用简单方案
- 元类增加复杂度
- 仅在必要时使用
""")
