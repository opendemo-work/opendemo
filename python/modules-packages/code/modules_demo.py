#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 模块与包 (Modules & Packages) 完整示例
演示 Python 的模块系统、导入机制和包组织
"""

import sys
import os
from importlib import import_module, reload
from types import ModuleType
from typing import List


# ============ 1. 模块基础 ============
print("=" * 50)
print("1. 模块基础")
print("=" * 50)

# 当前文件就是一个模块
print(f"当前模块名: {__name__}")
print(f"当前文件: {__file__}")

# 查看模块属性
import math
import json as json_mod
print(f"\njson模块路径: {json_mod.__file__}")
print(f"math模块名: {math.__name__}")
print(f"math.pi = {math.pi}")
print(f"math.sqrt(16) = {math.sqrt(16)}")


# ============ 2. 导入方式 ============
print("\n" + "=" * 50)
print("2. 各种导入方式")
print("=" * 50)

# 方式1: import module
import json
print(f"1. import json: {json.dumps({'a': 1})}")

# 方式2: from module import name
from datetime import datetime, timedelta
print(f"2. from datetime import: {datetime.now()}")

# 方式3: from module import * (不推荐)
# from math import *

# 方式4: import as (别名)
import collections as col
from functools import reduce as red
print(f"3. import as: {col.Counter('hello')}")

# 方式5: 导入子模块
from os import path
print(f"4. from os import path: {path.exists('.')}")

# 方式6: 相对导入 (只能在包内使用)
# from . import sibling_module
# from .. import parent_module
# from ..sibling_package import some_module


# ============ 3. 模块搜索路径 ============
print("\n" + "=" * 50)
print("3. 模块搜索路径 (sys.path)")
print("=" * 50)

print("Python模块搜索路径:")
for i, p in enumerate(sys.path[:5]):  # 只显示前5个
    print(f"  {i}: {p}")
print(f"  ... (共{len(sys.path)}个路径)")

# 添加自定义路径
custom_path = os.path.dirname(__file__)
if custom_path not in sys.path:
    sys.path.insert(0, custom_path)
    print(f"\n已添加自定义路径: {custom_path}")


# ============ 4. __name__ 与 __main__ ============
print("\n" + "=" * 50)
print("4. __name__ 与 __main__")
print("=" * 50)

def main():
    """程序入口点"""
    print("这是main函数")

# 模块被直接运行时 __name__ == "__main__"
# 模块被导入时 __name__ == 模块名
print(f"__name__ = {__name__}")

if __name__ == "__main__":
    print("模块被直接运行")
else:
    print("模块被导入")


# ============ 5. 动态导入 ============
print("\n" + "=" * 50)
print("5. 动态导入")
print("=" * 50)

# 使用 importlib.import_module
module_name = "os"
os_module = import_module(module_name)
print(f"动态导入 {module_name}: {os_module.getcwd()}")

# 导入子模块
urllib_parse = import_module("urllib.parse")
print(f"动态导入子模块: {urllib_parse.quote('hello world')}")

# 使用 __import__ (底层函数)
re_module = __import__("re")
pattern = r'\d+'
print(f"__import__: {re_module.match(pattern, '123')}")


# ============ 6. 重新加载模块 ============
print("\n" + "=" * 50)
print("6. 重新加载模块 (reload)")
print("=" * 50)

# 注意：reload 用于开发调试，生产环境谨慎使用
import random
original_id = id(random)

# 重新加载模块
reloaded_random = reload(random)
print(f"原始模块ID: {original_id}")
print(f"重载后ID: {id(reloaded_random)}")
print(f"是否同一对象: {original_id == id(reloaded_random)}")


# ============ 7. 模块属性 ============
print("\n" + "=" * 50)
print("7. 模块特殊属性")
print("=" * 50)

import collections

print(f"__name__: {collections.__name__}")
print(f"__doc__: {collections.__doc__[:50]}...")
print(f"__file__: {collections.__file__}")
print(f"__package__: {collections.__package__}")

# 查看模块中的公共名称
public_names = [n for n in dir(collections) if not n.startswith('_')]
print(f"\n公共名称(前10个): {public_names[:10]}")


# ============ 8. 包结构示例 ============
print("\n" + "=" * 50)
print("8. 包结构示例")
print("=" * 50)

package_structure = """
典型的包结构:

my_package/
    __init__.py          # 包初始化文件(必需)
    module_a.py          # 模块A
    module_b.py          # 模块B
    subpackage/          # 子包
        __init__.py
        module_c.py
    utils/               # 工具子包
        __init__.py
        helpers.py
        validators.py

__init__.py 的作用:
1. 标识目录为Python包
2. 包初始化代码
3. 定义 __all__ 控制 from package import *
4. 暴露子模块的API

__init__.py 示例:
```python
# my_package/__init__.py
from .module_a import ClassA, function_a
from .module_b import ClassB

__all__ = ['ClassA', 'ClassB', 'function_a']
__version__ = '1.0.0'
```
"""
print(package_structure)


# ============ 9. __all__ 控制导出 ============
print("\n" + "=" * 50)
print("9. __all__ 控制导出")
print("=" * 50)

# 模拟一个模块
class DemoModule:
    """演示 __all__ 的作用"""
    __all__ = ['public_func', 'PublicClass']
    
    @staticmethod
    def public_func():
        return "公开函数"
    
    class PublicClass:
        pass
    
    @staticmethod
    def _private_func():
        return "私有函数"
    
    @staticmethod
    def internal_func():
        """不在__all__中，from x import * 不会导入"""
        return "内部函数"

print("__all__ = ['public_func', 'PublicClass']")
print("from module import * 只会导入 __all__ 中列出的名称")
print(f"公开: {DemoModule.__all__}")


# ============ 10. 常用标准库模块 ============
print("\n" + "=" * 50)
print("10. 常用标准库模块")
print("=" * 50)

stdlib_modules = {
    "os": "操作系统接口",
    "sys": "Python运行时",
    "pathlib": "面向对象的路径操作",
    "json": "JSON编解码",
    "re": "正则表达式",
    "datetime": "日期时间",
    "collections": "高级容器",
    "itertools": "迭代器工具",
    "functools": "高阶函数",
    "typing": "类型注解",
    "logging": "日志记录",
    "unittest": "单元测试",
    "threading": "多线程",
    "multiprocessing": "多进程",
    "asyncio": "异步IO",
    "subprocess": "子进程管理",
    "socket": "网络编程",
    "http": "HTTP协议",
    "sqlite3": "SQLite数据库",
    "pickle": "对象序列化",
}

print("常用标准库:")
for module, desc in list(stdlib_modules.items())[:10]:
    print(f"  {module:15} - {desc}")
print(f"  ... (共{len(stdlib_modules)}个)")


# ============ 11. 条件导入 ============
print("\n" + "=" * 50)
print("11. 条件导入与兼容性")
print("=" * 50)

# Python版本检查
print(f"Python版本: {sys.version_info.major}.{sys.version_info.minor}")

# 条件导入示例
try:
    import tomllib  # Python 3.11+
    print("使用 tomllib (Python 3.11+)")
except ImportError:
    try:
        import tomli as tomllib  # 第三方库
        print("使用 tomli 兼容库")
    except ImportError:
        tomllib = None
        print("TOML解析不可用")

# 可选依赖
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

print(f"NumPy可用: {HAS_NUMPY}")


# ============ 12. 模块缓存 ============
print("\n" + "=" * 50)
print("12. 模块缓存 (sys.modules)")
print("=" * 50)

print(f"已加载模块数量: {len(sys.modules)}")

# 查看部分已加载模块
loaded = [m for m in sys.modules.keys() if not m.startswith('_')][:15]
print(f"部分已加载模块: {loaded}")

# 检查模块是否已加载
print(f"\n'os' 已加载: {'os' in sys.modules}")
print(f"'numpy' 已加载: {'numpy' in sys.modules}")


# ============ 13. 创建简单模块示例 ============
print("\n" + "=" * 50)
print("13. 动态创建模块")
print("=" * 50)

# 动态创建模块
dynamic_module = ModuleType("dynamic_module")
dynamic_module.greeting = "Hello from dynamic module!"
dynamic_module.add = lambda x, y: x + y

# 注册到 sys.modules
sys.modules["dynamic_module"] = dynamic_module

# 现在可以导入了
import dynamic_module
print(f"动态模块: {dynamic_module.greeting}")
print(f"动态函数: {dynamic_module.add(3, 4)}")

# 清理
del sys.modules["dynamic_module"]


# ============ 总结 ============
print("\n" + "=" * 50)
print("模块与包使用总结")
print("=" * 50)
print("""
导入最佳实践:
1. 标准库 -> 第三方库 -> 本地模块 (分组导入)
2. 避免 from module import *
3. 使用绝对导入优于相对导入
4. 循环导入时重构代码

包组织原则:
1. 每个包必须有 __init__.py
2. 使用 __all__ 明确公共API
3. 私有模块以 _ 开头
4. 相关模块组织在同一包中

性能考虑:
1. 导入是有开销的，避免重复导入
2. 延迟导入大型模块
3. 使用 importlib 进行动态导入
""")
