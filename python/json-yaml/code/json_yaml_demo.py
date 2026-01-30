#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python JSON和YAML处理演示
展示json模块和yaml库的常用功能
"""
import json
import tempfile
import os
from datetime import datetime, date
from dataclasses import dataclass, asdict


def demo_json_basics():
    """JSON基础"""
    print("=" * 50)
    print("1. JSON基础操作")
    print("=" * 50)
    
    # Python对象转JSON字符串
    data = {
        "name": "Alice",
        "age": 25,
        "skills": ["Python", "Java", "SQL"],
        "is_active": True,
        "score": 95.5,
        "address": None
    }
    
    json_str = json.dumps(data)
    print(f"dumps():\n  {json_str}")
    
    # 格式化输出
    json_pretty = json.dumps(data, indent=2, ensure_ascii=False)
    print(f"\ndumps(indent=2):\n{json_pretty}")
    
    # JSON字符串转Python对象
    parsed = json.loads(json_str)
    print(f"\nloads():")
    print(f"  类型: {type(parsed)}")
    print(f"  name: {parsed['name']}")
    print(f"  skills: {parsed['skills']}")


def demo_json_file():
    """JSON文件操作"""
    print("\n" + "=" * 50)
    print("2. JSON文件操作")
    print("=" * 50)
    
    data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
        ],
        "total": 2
    }
    
    temp_file = tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False, encoding='utf-8'
    )
    temp_file.close()
    
    # 写入JSON文件
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"写入文件: {temp_file.name}")
    
    # 读取JSON文件
    with open(temp_file.name, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    print(f"读取内容: {loaded}")
    
    os.unlink(temp_file.name)


def demo_json_custom_encoder():
    """自定义JSON编码器"""
    print("\n" + "=" * 50)
    print("3. 自定义JSON编码器")
    print("=" * 50)
    
    # 默认无法序列化datetime
    data = {
        "event": "会议",
        "date": datetime.now(),
        "deadline": date.today()
    }
    
    print("datetime默认无法序列化,需要自定义编码器:")
    
    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            return super().default(obj)
    
    json_str = json.dumps(data, cls=CustomEncoder, indent=2)
    print(f"使用CustomEncoder:\n{json_str}")
    
    # 使用default参数(简化版)
    def json_serializer(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    json_str2 = json.dumps(data, default=json_serializer, indent=2)
    print(f"\n使用default函数:\n{json_str2}")


def demo_json_with_dataclass():
    """JSON与dataclass"""
    print("\n" + "=" * 50)
    print("4. JSON与dataclass")
    print("=" * 50)
    
    @dataclass
    class User:
        id: int
        name: str
        email: str
        is_active: bool = True
    
    # dataclass转JSON
    user = User(1, "Alice", "alice@example.com")
    json_str = json.dumps(asdict(user), indent=2)
    print(f"dataclass -> JSON:\n{json_str}")
    
    # JSON转dataclass
    json_data = '{"id": 2, "name": "Bob", "email": "bob@example.com", "is_active": false}'
    data = json.loads(json_data)
    user2 = User(**data)
    print(f"\nJSON -> dataclass: {user2}")


def demo_yaml_basics():
    """YAML基础"""
    print("\n" + "=" * 50)
    print("5. YAML基础 (需要 pip install pyyaml)")
    print("=" * 50)
    
    try:
        import yaml
        
        # Python对象转YAML
        data = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "myapp"
            },
            "features": ["auth", "logging", "cache"],
            "debug": True
        }
        
        yaml_str = yaml.dump(data, allow_unicode=True, default_flow_style=False)
        print(f"dump():\n{yaml_str}")
        
        # YAML字符串转Python对象
        yaml_text = """
server:
  host: 0.0.0.0
  port: 8080
  
logging:
  level: INFO
  format: "%(asctime)s - %(message)s"
  
features:
  - authentication
  - rate_limiting
  - caching
"""
        parsed = yaml.safe_load(yaml_text)
        print(f"safe_load():")
        print(f"  server: {parsed['server']}")
        print(f"  features: {parsed['features']}")
        
    except ImportError:
        print("  PyYAML未安装,显示示例代码:")
        yaml_example = '''
# 安装: pip install pyyaml
import yaml

# 读取YAML文件
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 写入YAML文件
with open('output.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, allow_unicode=True)
'''
        print(yaml_example)


def demo_yaml_file():
    """YAML文件操作"""
    print("\n" + "=" * 50)
    print("6. YAML文件操作")
    print("=" * 50)
    
    try:
        import yaml
        
        config = {
            "app": {
                "name": "MyApp",
                "version": "1.0.0",
                "debug": False
            },
            "database": {
                "host": "localhost",
                "port": 3306,
                "name": "myapp_db",
                "pool_size": 10
            },
            "redis": {
                "host": "localhost",
                "port": 6379
            }
        }
        
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        )
        temp_file.close()
        
        # 写入YAML
        with open(temp_file.name, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        print(f"写入文件: {temp_file.name}")
        
        # 读取YAML
        with open(temp_file.name, 'r', encoding='utf-8') as f:
            loaded = yaml.safe_load(f)
        print(f"读取内容:")
        print(f"  app.name: {loaded['app']['name']}")
        print(f"  database.host: {loaded['database']['host']}")
        
        os.unlink(temp_file.name)
        
    except ImportError:
        print("  PyYAML未安装,跳过文件操作演示")


def demo_json_yaml_conversion():
    """JSON和YAML互转"""
    print("\n" + "=" * 50)
    print("7. JSON和YAML互转")
    print("=" * 50)
    
    try:
        import yaml
        
        # JSON转YAML
        json_str = '{"name": "Alice", "skills": ["Python", "Java"], "active": true}'
        data = json.loads(json_str)
        yaml_str = yaml.dump(data, allow_unicode=True)
        print(f"JSON:\n  {json_str}")
        print(f"\n转换为YAML:\n{yaml_str}")
        
        # YAML转JSON
        yaml_text = """
user:
  name: Bob
  age: 30
  hobbies:
    - reading
    - coding
"""
        data = yaml.safe_load(yaml_text)
        json_str = json.dumps(data, indent=2)
        print(f"YAML转JSON:\n{json_str}")
        
    except ImportError:
        print("  PyYAML未安装,显示转换原理:")
        print("  JSON -> dict -> YAML: yaml.dump(json.loads(json_str))")
        print("  YAML -> dict -> JSON: json.dumps(yaml.safe_load(yaml_str))")


if __name__ == "__main__":
    demo_json_basics()
    demo_json_file()
    demo_json_custom_encoder()
    demo_json_with_dataclass()
    demo_yaml_basics()
    demo_yaml_file()
    demo_json_yaml_conversion()
    print("\n[OK] JSON/YAML处理演示完成!")
