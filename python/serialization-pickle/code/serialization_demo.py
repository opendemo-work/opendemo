#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 序列化 (Serialization) 完整示例
演示 pickle、json 和其他序列化方法
"""

import pickle
import json
import shelve
import tempfile
import os
from dataclasses import dataclass, asdict
from typing import Any, Dict, List
from datetime import datetime, date
import struct


# ============ 1. Pickle 基础 ============
print("=" * 50)
print("1. Pickle 基础")
print("=" * 50)

# 序列化基本类型
data = {
    "name": "Alice",
    "age": 25,
    "scores": [85, 90, 88],
    "active": True,
    "metadata": {"role": "admin"},
}

# 序列化为字节
pickled = pickle.dumps(data)
print(f"序列化后大小: {len(pickled)} 字节")
print(f"前50字节: {pickled[:50]}")

# 反序列化
restored = pickle.loads(pickled)
print(f"反序列化: {restored}")
print(f"数据相等: {data == restored}")


# ============ 2. Pickle 文件操作 ============
print("\n" + "=" * 50)
print("2. Pickle 文件操作")
print("=" * 50)

# 创建临时文件
with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as f:
    pickle.dump(data, f)
    temp_path = f.name

print(f"保存到: {temp_path}")

# 读取
with open(temp_path, 'rb') as f:
    loaded = pickle.load(f)
print(f"加载的数据: {loaded}")

# 清理
os.unlink(temp_path)


# ============ 3. 序列化自定义类 ============
print("\n" + "=" * 50)
print("3. 序列化自定义类")
print("=" * 50)

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.created_at = datetime.now()
    
    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age})"
    
    def greet(self):
        return f"Hello, I'm {self.name}"

person = Person("Bob", 30)
print(f"原始对象: {person}")

# 序列化
pickled_person = pickle.dumps(person)
print(f"序列化大小: {len(pickled_person)} 字节")

# 反序列化
restored_person = pickle.loads(pickled_person)
print(f"恢复对象: {restored_person}")
print(f"方法调用: {restored_person.greet()}")


# ============ 4. 自定义序列化行为 ============
print("\n" + "=" * 50)
print("4. 自定义序列化行为 (__getstate__/__setstate__)")
print("=" * 50)

class DatabaseConnection:
    """不可序列化的资源需要特殊处理"""
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._connection = self._connect()
    
    def _connect(self):
        """模拟连接"""
        return f"Connection to {self.host}:{self.port}"
    
    def __getstate__(self):
        """序列化时排除连接"""
        state = self.__dict__.copy()
        del state["_connection"]  # 不序列化连接
        return state
    
    def __setstate__(self, state):
        """反序列化时重建连接"""
        self.__dict__.update(state)
        self._connection = self._connect()  # 重新连接
    
    def __repr__(self):
        return f"DB({self.host}:{self.port}, connected={bool(self._connection)})"

db = DatabaseConnection("localhost", 5432)
print(f"原始: {db}")
print(f"连接: {db._connection}")

pickled_db = pickle.dumps(db)
restored_db = pickle.loads(pickled_db)
print(f"恢复: {restored_db}")
print(f"重建连接: {restored_db._connection}")


# ============ 5. __reduce__ 方法 ============
print("\n" + "=" * 50)
print("5. __reduce__ 高级控制")
print("=" * 50)

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __reduce__(self):
        """返回重建对象所需的信息"""
        return (self.__class__, (self.x, self.y))
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

point = Point(3.0, 4.0)
pickled_point = pickle.dumps(point)
restored_point = pickle.loads(pickled_point)
print(f"原始: {point}")
print(f"恢复: {restored_point}")


# ============ 6. JSON 序列化 ============
print("\n" + "=" * 50)
print("6. JSON 序列化")
print("=" * 50)

# 基本JSON操作
json_data = {
    "name": "Alice",
    "age": 25,
    "emails": ["alice@example.com"],
}

json_str = json.dumps(json_data, indent=2)
print(f"JSON字符串:\n{json_str}")

# 反序列化
parsed = json.loads(json_str)
print(f"解析结果: {parsed}")


# ============ 7. 自定义JSON编码器 ============
print("\n" + "=" * 50)
print("7. 自定义JSON编码器/解码器")
print("=" * 50)

class CustomEncoder(json.JSONEncoder):
    """处理特殊类型的JSON编码器"""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return {"__datetime__": obj.isoformat()}
        if isinstance(obj, date):
            return {"__date__": obj.isoformat()}
        if isinstance(obj, set):
            return {"__set__": list(obj)}
        if isinstance(obj, bytes):
            return {"__bytes__": obj.hex()}
        if hasattr(obj, "__dict__"):
            return {"__class__": obj.__class__.__name__, **obj.__dict__}
        return super().default(obj)

def custom_decoder(obj):
    """自定义解码器钩子"""
    if "__datetime__" in obj:
        return datetime.fromisoformat(obj["__datetime__"])
    if "__date__" in obj:
        return date.fromisoformat(obj["__date__"])
    if "__set__" in obj:
        return set(obj["__set__"])
    if "__bytes__" in obj:
        return bytes.fromhex(obj["__bytes__"])
    return obj

# 测试
complex_data = {
    "created": datetime.now(),
    "tags": {"python", "demo"},
    "binary": b"hello",
}

encoded = json.dumps(complex_data, cls=CustomEncoder, indent=2)
print(f"编码后:\n{encoded}")

decoded = json.loads(encoded, object_hook=custom_decoder)
print(f"解码后: {decoded}")
print(f"类型检查: datetime={type(decoded['created'])}, set={type(decoded['tags'])}")


# ============ 8. Dataclass 序列化 ============
print("\n" + "=" * 50)
print("8. Dataclass 序列化")
print("=" * 50)

@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, json_str: str) -> "User":
        return cls(**json.loads(json_str))
    
    def to_pickle(self) -> bytes:
        return pickle.dumps(self)
    
    @classmethod
    def from_pickle(cls, data: bytes) -> "User":
        return pickle.loads(data)

user = User(1, "Alice", "alice@example.com")
print(f"原始: {user}")

# JSON
json_str = user.to_json()
print(f"JSON: {json_str}")
restored_user = User.from_json(json_str)
print(f"从JSON恢复: {restored_user}")

# Pickle
pickled = user.to_pickle()
print(f"Pickle大小: {len(pickled)} 字节")


# ============ 9. Shelve 持久化字典 ============
print("\n" + "=" * 50)
print("9. Shelve 持久化字典")
print("=" * 50)

# 创建临时shelve文件
shelf_path = tempfile.mktemp()

with shelve.open(shelf_path) as db:
    db["user1"] = {"name": "Alice", "age": 25}
    db["user2"] = {"name": "Bob", "age": 30}
    db["config"] = {"debug": True, "version": "1.0"}
    print(f"写入 {len(db)} 个键")

with shelve.open(shelf_path) as db:
    print(f"读取 user1: {db['user1']}")
    print(f"所有键: {list(db.keys())}")

# 清理
for ext in ["", ".db", ".dir", ".bak", ".dat"]:
    try:
        os.unlink(shelf_path + ext)
    except FileNotFoundError:
        pass


# ============ 10. 二进制序列化 (struct) ============
print("\n" + "=" * 50)
print("10. 二进制序列化 (struct)")
print("=" * 50)

# 定义数据结构
# < = 小端序, i = int, f = float, 10s = 10字节字符串
format_str = "<if10s"

# 打包数据
data = (42, 3.14, b"hello")
packed = struct.pack(format_str, *data)
print(f"打包后: {packed.hex()}")
print(f"大小: {len(packed)} 字节")

# 解包数据
unpacked = struct.unpack(format_str, packed)
print(f"解包后: {unpacked}")


# ============ 11. Pickle 安全注意事项 ============
print("\n" + "=" * 50)
print("11. Pickle 安全注意事项")
print("=" * 50)

print("""
Pickle 安全风险:
- pickle.loads() 会执行任意代码
- 不要反序列化不信任的数据
- 恶意pickle可执行系统命令

安全建议:
1. 只反序列化可信来源的数据
2. 考虑使用 JSON 代替 pickle
3. 使用 hmac 验证数据完整性
4. 限制 pickle 协议版本

安全示例:
""")

import hmac
import hashlib

def secure_dumps(obj, key: bytes) -> tuple:
    """安全序列化(带签名)"""
    data = pickle.dumps(obj)
    signature = hmac.new(key, data, hashlib.sha256).digest()
    return data, signature

def secure_loads(data: bytes, signature: bytes, key: bytes):
    """安全反序列化(验证签名)"""
    expected_sig = hmac.new(key, data, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected_sig):
        raise ValueError("签名验证失败")
    return pickle.loads(data)

# 使用
secret_key = b"my-secret-key"
data, sig = secure_dumps({"user": "alice"}, secret_key)
print(f"数据大小: {len(data)}, 签名大小: {len(sig)}")

restored = secure_loads(data, sig, secret_key)
print(f"验证并恢复: {restored}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("序列化方法对比")
print("=" * 50)
print("""
| 方法    | 可读性 | 性能  | 类型支持 | 安全性 |
|---------|--------|-------|----------|--------|
| JSON    | 高     | 中    | 有限     | 高     |
| Pickle  | 无     | 高    | 全部     | 低     |
| Shelve  | 无     | 高    | 全部     | 低     |
| struct  | 无     | 极高  | 基本类型 | 高     |

使用建议:
- API通信: JSON
- 内部缓存: Pickle
- 持久化存储: Shelve/数据库
- 网络协议: struct
""")
