#!/usr/bin/env python3
"""批量生成Python案例README文件"""

import os
import json

# 案例定义
CASES = {
    # 基础语法类
    "control-flow": {
        "title": "Control Flow Demo",
        "desc": "Python控制流演示，if/else/for/while/break/continue",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "functions-decorators": {
        "title": "Functions and Decorators Demo",
        "desc": "Python函数与装饰器演示，高阶函数、闭包、装饰器",
        "category": "python-core",
        "difficulty": "intermediate"
    },
    "lambda-expressions": {
        "title": "Lambda Expressions Demo",
        "desc": "Python Lambda表达式演示，匿名函数、高阶函数",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "list-operations": {
        "title": "List Operations Demo",
        "desc": "Python列表操作演示，切片、推导式、常用方法",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "dict-operations": {
        "title": "Dictionary Operations Demo",
        "desc": "Python字典操作演示，CRUD、遍历、字典方法",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "set-operations": {
        "title": "Set Operations Demo",
        "desc": "Python集合操作演示，集合运算、去重、 frozenset",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "string-operations": {
        "title": "String Operations Demo",
        "desc": "Python字符串操作演示，格式化、正则、编码",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "file-operations": {
        "title": "File Operations Demo",
        "desc": "Python文件操作演示，读写、上下文管理器、路径处理",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "exception-handling": {
        "title": "Exception Handling Demo",
        "desc": "Python异常处理演示，try/except/finally、自定义异常",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "comprehensions": {
        "title": "Comprehensions Demo",
        "desc": "Python推导式演示，列表/字典/集合推导式",
        "category": "python-core",
        "difficulty": "beginner"
    },
    # 高级特性类
    "iterators-generators": {
        "title": "Iterators and Generators Demo",
        "desc": "Python迭代器和生成器演示，yield、生成器表达式",
        "category": "python-core",
        "difficulty": "intermediate"
    },
    "context-managers": {
        "title": "Context Managers Demo",
        "desc": "Python上下文管理器演示，with语句、__enter__/__exit__",
        "category": "python-core",
        "difficulty": "intermediate"
    },
    "decorators-advanced": {
        "title": "Decorators Advanced Demo",
        "desc": "Python装饰器高级演示，类装饰器、参数装饰器、wraps",
        "category": "python-core",
        "difficulty": "advanced"
    },
    "metaclasses": {
        "title": "Metaclasses Demo",
        "desc": "Python元类演示，type、元类编程",
        "category": "python-core",
        "difficulty": "advanced"
    },
    "descriptors-property": {
        "title": "Descriptors and Property Demo",
        "desc": "Python描述符和property演示，__get__/__set__、属性装饰器",
        "category": "python-core",
        "difficulty": "advanced"
    },
    "magic-methods": {
        "title": "Magic Methods Demo",
        "desc": "Python魔术方法演示，__str__、__repr__、__eq__等",
        "category": "python-core",
        "difficulty": "intermediate"
    },
    "inheritance-mro": {
        "title": "Inheritance and MRO Demo",
        "desc": "Python继承和MRO演示，多重继承、方法解析顺序",
        "category": "python-core",
        "difficulty": "intermediate"
    },
    "scope-closures": {
        "title": "Scope and Closures Demo",
        "desc": "Python作用域和闭包演示，LEGB规则、nonlocal、闭包",
        "category": "python-core",
        "difficulty": "intermediate"
    },
    # 标准库类
    "collections-module": {
        "title": "Collections Module Demo",
        "desc": "Python Collections模块演示，Counter、defaultdict、OrderedDict",
        "category": "python-standard-library",
        "difficulty": "intermediate"
    },
    "itertools-module": {
        "title": "Itertools Module Demo",
        "desc": "Python Itertools模块演示，迭代器工具、组合、排列",
        "category": "python-standard-library",
        "difficulty": "intermediate"
    },
    "functools-module": {
        "title": "Functools Module Demo",
        "desc": "Python Functools模块演示，lru_cache、partial、reduce",
        "category": "python-standard-library",
        "difficulty": "intermediate"
    },
    "operator-module": {
        "title": "Operator Module Demo",
        "desc": "Python Operator模块演示，函数式操作符",
        "category": "python-standard-library",
        "difficulty": "beginner"
    },
    "datetime": {
        "title": "DateTime Module Demo",
        "desc": "Python日期时间处理演示，datetime、timezone、timedelta",
        "category": "python-standard-library",
        "difficulty": "beginner"
    },
    "json-yaml": {
        "title": "JSON and YAML Processing Demo",
        "desc": "Python JSON和YAML处理演示，序列化、反序列化",
        "category": "python-standard-library",
        "difficulty": "beginner"
    },
    "regex": {
        "title": "Regular Expressions Demo",
        "desc": "Python正则表达式演示，re模块、模式匹配",
        "category": "python-standard-library",
        "difficulty": "intermediate"
    },
    "logging": {
        "title": "Logging Module Demo",
        "desc": "Python日志处理演示，logging配置、级别、处理器",
        "category": "python-standard-library",
        "difficulty": "intermediate"
    },
    "config-management": {
        "title": "Config Management Demo",
        "desc": "Python配置管理演示，ini、yaml、env配置",
        "category": "python-standard-library",
        "difficulty": "beginner"
    },
    "pathlib-os": {
        "title": "Pathlib and OS Module Demo",
        "desc": "Python路径和系统操作演示，pathlib、os、shutil",
        "category": "python-standard-library",
        "difficulty": "beginner"
    },
    "environment-variables": {
        "title": "Environment Variables Demo",
        "desc": "Python环境变量演示，os.environ、python-dotenv",
        "category": "python-standard-library",
        "difficulty": "beginner"
    },
    "serialization-pickle": {
        "title": "Serialization and Pickle Demo",
        "desc": "Python序列化演示，pickle、json、marshal",
        "category": "python-standard-library",
        "difficulty": "intermediate"
    },
    # 并发编程类
    "multiprocessing": {
        "title": "Multiprocessing Demo",
        "desc": "Python多进程编程演示，Process、Pool、Queue",
        "category": "python-concurrency",
        "difficulty": "intermediate"
    },
    "threading-synchronization": {
        "title": "Threading Synchronization Demo",
        "desc": "Python线程同步演示，Lock、RLock、Condition、Semaphore",
        "category": "python-concurrency",
        "difficulty": "advanced"
    },
    # 数据库类
    "database-sqlite": {
        "title": "SQLite Database Demo",
        "desc": "Python SQLite数据库演示，CRUD、事务、连接池",
        "category": "python-database",
        "difficulty": "beginner"
    },
    # 网络类
    "socket-networking": {
        "title": "Socket Networking Demo",
        "desc": "Python Socket网络编程演示，TCP/UDP、客户端/服务器",
        "category": "python-networking",
        "difficulty": "intermediate"
    },
    "http-requests": {
        "title": "HTTP Requests Demo",
        "desc": "Python HTTP请求演示，requests库、API调用",
        "category": "python-networking",
        "difficulty": "beginner"
    },
    # 数据处理类
    "caching": {
        "title": "Caching Demo",
        "desc": "Python缓存演示，functools.lru_cache、cachetools",
        "category": "python-performance",
        "difficulty": "intermediate"
    },
    "profiling-optimization": {
        "title": "Profiling and Optimization Demo",
        "desc": "Python性能分析演示，cProfile、line_profiler、优化技巧",
        "category": "python-performance",
        "difficulty": "advanced"
    },
    "copy-deepcopy": {
        "title": "Copy and Deepcopy Demo",
        "desc": "Python拷贝演示，浅拷贝、深拷贝、对象复制",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "numbers-math": {
        "title": "Numbers and Math Demo",
        "desc": "Python数值和数学演示，math、random、decimal",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "bitwise-operations": {
        "title": "Bitwise Operations Demo",
        "desc": "Python位运算演示，位操作、掩码、标志位",
        "category": "python-core",
        "difficulty": "intermediate"
    },
    "enums": {
        "title": "Enums Demo",
        "desc": "Python枚举演示，Enum、IntEnum、自动值",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "dataclasses": {
        "title": "Dataclasses Demo",
        "desc": "Python数据类演示，@dataclass、字段、默认值",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "abc-interfaces": {
        "title": "ABC and Interfaces Demo",
        "desc": "Python抽象基类演示，ABC、抽象方法、接口",
        "category": "python-core",
        "difficulty": "intermediate"
    },
    "modules-packages": {
        "title": "Modules and Packages Demo",
        "desc": "Python模块和包演示，导入、__init__.py、命名空间",
        "category": "python-core",
        "difficulty": "beginner"
    },
    "type-hints": {
        "title": "Type Hints Demo",
        "desc": "Python类型提示演示，typing、类型检查、mypy",
        "category": "python-core",
        "difficulty": "intermediate"
    },
    "debugging": {
        "title": "Debugging Demo",
        "desc": "Python调试演示，pdb、断点、调试技巧",
        "category": "python-development",
        "difficulty": "beginner"
    }
}

def generate_readme(dir_name, info):
    """生成README.md文件"""
    content = f"""# {info['title']}

{info['desc']}。

## 技术栈

- Python 3.8+
- {info['category'].replace('python-', '').title()}

## 核心概念

### 主要特性

- 特性1
- 特性2
- 特性3

## 快速开始

```bash
# 运行示例
python {dir_name.replace('-', '_')}.py

# 运行测试
python -m pytest test_{dir_name.replace('-', '_')}.py -v
```

## 学习要点

1. 核心概念1
2. 核心概念2
3. 核心概念3

## 参考

- [Python官方文档](https://docs.python.org/3/)
"""
    
    readme_path = os.path.join(dir_name, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 创建 {readme_path}")

def generate_metadata(dir_name, info):
    """生成metadata.json文件"""
    metadata = {
        "name": info['title'],
        "category": info['category'],
        "tech_stack": ["Python"],
        "description": info['desc'],
        "difficulty": info['difficulty'],
        "dependencies": []
    }
    
    metadata_path = os.path.join(dir_name, "metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"✅ 创建 {metadata_path}")

def main():
    """主函数"""
    count = 0
    for dir_name, info in CASES.items():
        if os.path.isdir(dir_name):
            # 检查是否已存在README
            readme_path = os.path.join(dir_name, "README.md")
            if not os.path.exists(readme_path):
                try:
                    generate_readme(dir_name, info)
                    generate_metadata(dir_name, info)
                    count += 1
                except Exception as e:
                    print(f"❌ 错误 {dir_name}: {e}")
        else:
            print(f"⚠️ 目录不存在: {dir_name}")
    
    print(f"\n🎉 共生成 {count} 个案例的文档")

if __name__ == '__main__':
    main()
