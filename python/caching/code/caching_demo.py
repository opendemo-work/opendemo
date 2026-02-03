#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 缓存机制完整示例
演示 functools.lru_cache、自定义缓存和缓存策略
"""

import time
from functools import lru_cache, cache, cached_property, wraps
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from collections import OrderedDict
import threading
import hashlib


# ============ 1. lru_cache 基础 ============
print("=" * 50)
print("1. lru_cache 基础")
print("=" * 50)

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """使用缓存的斐波那契数列"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 测试性能
start = time.time()
result = fibonacci(35)
cached_time = time.time() - start

print(f"fibonacci(35) = {result}")
print(f"缓存后耗时: {cached_time:.6f}秒")

# 查看缓存信息
info = fibonacci.cache_info()
print(f"缓存信息: hits={info.hits}, misses={info.misses}, size={info.currsize}")

# 清除缓存
fibonacci.cache_clear()
print("缓存已清除")


# ============ 2. cache 装饰器 (Python 3.9+) ============
print("\n" + "=" * 50)
print("2. cache 装饰器 (无限缓存)")
print("=" * 50)

@cache  # 等价于 @lru_cache(maxsize=None)
def factorial(n: int) -> int:
    """计算阶乘"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(f"factorial(10) = {factorial(10)}")
print(f"factorial(20) = {factorial(20)}")
print(f"缓存信息: {factorial.cache_info()}")


# ============ 3. 带超时的缓存 ============
print("\n" + "=" * 50)
print("3. 带超时的缓存 (TTL Cache)")
print("=" * 50)

def ttl_cache(seconds: int = 60, maxsize: int = 128):
    """带过期时间的缓存装饰器"""
    def decorator(func: Callable):
        cache_data: Dict[tuple, tuple] = {}  # key -> (value, timestamp)
        lock = threading.Lock()
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = (args, tuple(sorted(kwargs.items())))
            current_time = time.time()
            
            with lock:
                # 检查缓存
                if key in cache_data:
                    value, timestamp = cache_data[key]
                    if current_time - timestamp < seconds:
                        return value
                    else:
                        del cache_data[key]  # 过期删除
                
                # 限制大小
                while len(cache_data) >= maxsize:
                    oldest_key = next(iter(cache_data))
                    del cache_data[oldest_key]
                
                # 计算并缓存
                result = func(*args, **kwargs)
                cache_data[key] = (result, current_time)
                return result
        
        wrapper.cache_clear = lambda: cache_data.clear()
        wrapper.cache_info = lambda: {"size": len(cache_data), "maxsize": maxsize, "ttl": seconds}
        return wrapper
    return decorator

@ttl_cache(seconds=2, maxsize=10)
def get_data(key: str) -> str:
    """模拟耗时操作"""
    time.sleep(0.1)
    return f"data_{key}_{time.time():.2f}"

# 测试
print(f"第一次调用: {get_data('test')}")
print(f"第二次调用(缓存): {get_data('test')}")
print(f"缓存信息: {get_data.cache_info()}")

time.sleep(2.1)  # 等待过期
print(f"过期后调用: {get_data('test')}")


# ============ 4. cached_property ============
print("\n" + "=" * 50)
print("4. cached_property (惰性求值)")
print("=" * 50)

class DataProcessor:
    def __init__(self, data: list):
        self.data = data
        self._process_count = 0
    
    @cached_property
    def processed_data(self) -> list:
        """只计算一次的属性"""
        self._process_count += 1
        print(f"  处理数据... (第{self._process_count}次)")
        time.sleep(0.1)  # 模拟耗时处理
        return [x * 2 for x in self.data]
    
    @cached_property
    def statistics(self) -> dict:
        """统计信息"""
        data = self.processed_data
        return {
            "count": len(data),
            "sum": sum(data),
            "avg": sum(data) / len(data) if data else 0
        }

processor = DataProcessor([1, 2, 3, 4, 5])
print("第一次访问 processed_data:")
print(f"  结果: {processor.processed_data}")
print("第二次访问 processed_data:")
print(f"  结果: {processor.processed_data}")
print(f"统计信息: {processor.statistics}")


# ============ 5. LRU 缓存实现 ============
print("\n" + "=" * 50)
print("5. 手动实现 LRU 缓存")
print("=" * 50)

class LRUCache:
    """最近最少使用缓存"""
    
    def __init__(self, maxsize: int = 128):
        self.maxsize = maxsize
        self.cache: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def get(self, key: Any) -> Optional[Any]:
        if key in self.cache:
            # 移到末尾表示最近使用
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        # 超出容量时删除最旧的
        while len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
    
    def __contains__(self, key: Any) -> bool:
        return key in self.cache
    
    def info(self) -> dict:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "size": len(self.cache),
            "maxsize": self.maxsize
        }

# 使用示例
lru = LRUCache(maxsize=3)
lru.put("a", 1)
lru.put("b", 2)
lru.put("c", 3)
print(f"初始状态: {list(lru.cache.items())}")

lru.get("a")  # 访问a,使其变成最近使用
print(f"访问a后: {list(lru.cache.items())}")

lru.put("d", 4)  # 添加d,应该淘汰b
print(f"添加d后: {list(lru.cache.items())}")
print(f"缓存信息: {lru.info()}")


# ============ 6. 基于内容的缓存键 ============
print("\n" + "=" * 50)
print("6. 基于内容的缓存键")
print("=" * 50)

def make_hashable(obj: Any) -> str:
    """将任意对象转换为可哈希的字符串"""
    import json
    if isinstance(obj, (list, dict)):
        return hashlib.md5(json.dumps(obj, sort_keys=True).encode()).hexdigest()
    return str(obj)

def content_cache(func: Callable):
    """基于参数内容的缓存"""
    cache_data = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 创建基于内容的键
        key_parts = [make_hashable(arg) for arg in args]
        key_parts.extend(f"{k}={make_hashable(v)}" for k, v in sorted(kwargs.items()))
        key = ":".join(key_parts)
        
        if key not in cache_data:
            cache_data[key] = func(*args, **kwargs)
        return cache_data[key]
    
    return wrapper

@content_cache
def process_config(config: dict) -> str:
    """处理配置(字典参数通常不可哈希)"""
    print(f"  处理配置: {config}")
    return f"processed_{len(config)}_items"

config1 = {"a": 1, "b": 2}
config2 = {"a": 1, "b": 2}  # 相同内容

print("第一次调用:")
print(f"  结果: {process_config(config1)}")
print("第二次调用(相同内容):")
print(f"  结果: {process_config(config2)}")


# ============ 7. 多级缓存 ============
print("\n" + "=" * 50)
print("7. 多级缓存")
print("=" * 50)

class MultiLevelCache:
    """多级缓存: L1(内存) -> L2(持久化)"""
    
    def __init__(self, l1_size: int = 100):
        self.l1 = LRUCache(l1_size)  # 快速内存缓存
        self.l2: Dict[str, Any] = {}  # 模拟持久化存储
    
    def get(self, key: str) -> Optional[Any]:
        # 先查L1
        value = self.l1.get(key)
        if value is not None:
            print(f"  L1 命中: {key}")
            return value
        
        # 查L2
        if key in self.l2:
            print(f"  L2 命中: {key}")
            value = self.l2[key]
            self.l1.put(key, value)  # 提升到L1
            return value
        
        print(f"  缓存未命中: {key}")
        return None
    
    def put(self, key: str, value: Any) -> None:
        self.l1.put(key, value)
        self.l2[key] = value

cache = MultiLevelCache(l1_size=2)
cache.put("user:1", {"name": "Alice"})
cache.put("user:2", {"name": "Bob"})
cache.put("user:3", {"name": "Charlie"})  # L1中user:1被淘汰

print("查询 user:1 (在L2中):")
cache.get("user:1")
print("再次查询 user:1 (已提升到L1):")
cache.get("user:1")


# ============ 8. 缓存装饰器工厂 ============
print("\n" + "=" * 50)
print("8. 缓存装饰器工厂")
print("=" * 50)

def memoize(key_func: Optional[Callable] = None):
    """
    灵活的记忆化装饰器
    key_func: 自定义缓存键生成函数
    """
    def decorator(func: Callable):
        cache_data = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = (args, tuple(sorted(kwargs.items())))
            
            if key not in cache_data:
                cache_data[key] = func(*args, **kwargs)
            return cache_data[key]
        
        wrapper.cache = cache_data
        wrapper.cache_clear = cache_data.clear
        return wrapper
    return decorator

# 自定义缓存键
@memoize(key_func=lambda user_id, **kwargs: user_id)
def get_user(user_id: int, include_details: bool = False) -> dict:
    """只根据user_id缓存,忽略其他参数"""
    print(f"  查询用户 {user_id}")
    return {"id": user_id, "name": f"User_{user_id}"}

print("查询用户1(include_details=False):")
print(f"  {get_user(1, include_details=False)}")
print("查询用户1(include_details=True) - 使用缓存:")
print(f"  {get_user(1, include_details=True)}")


# ============ 9. 缓存失效策略 ============
print("\n" + "=" * 50)
print("9. 缓存失效策略")
print("=" * 50)

class CacheWithInvalidation:
    """支持主动失效的缓存"""
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.tags: Dict[str, set] = {}  # tag -> keys
    
    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key)
    
    def put(self, key: str, value: Any, tags: list = None) -> None:
        self.cache[key] = value
        for tag in (tags or []):
            if tag not in self.tags:
                self.tags[tag] = set()
            self.tags[tag].add(key)
    
    def invalidate_by_key(self, key: str) -> None:
        """按键失效"""
        self.cache.pop(key, None)
    
    def invalidate_by_tag(self, tag: str) -> int:
        """按标签失效"""
        keys = self.tags.get(tag, set())
        for key in keys:
            self.cache.pop(key, None)
        self.tags.pop(tag, None)
        return len(keys)

cache = CacheWithInvalidation()
cache.put("user:1", {"name": "Alice"}, tags=["users"])
cache.put("user:2", {"name": "Bob"}, tags=["users"])
cache.put("product:1", {"name": "Laptop"}, tags=["products"])

print(f"初始缓存: {list(cache.cache.keys())}")

# 失效所有用户缓存
count = cache.invalidate_by_tag("users")
print(f"失效 {count} 个用户缓存")
print(f"剩余缓存: {list(cache.cache.keys())}")


# ============ 10. 最佳实践 ============
print("\n" + "=" * 50)
print("10. 缓存最佳实践")
print("=" * 50)
print("""
1. 选择合适的缓存策略:
   - 纯函数 -> @lru_cache/@cache
   - 需要过期 -> TTL缓存
   - 类属性 -> @cached_property

2. 缓存键设计:
   - 确保唯一性
   - 考虑参数可哈希性
   - 适当的粒度

3. 缓存失效:
   - 主动失效(写入时)
   - 被动失效(TTL过期)
   - 标签失效(批量)

4. 注意事项:
   - 缓存不是银弹
   - 考虑内存占用
   - 线程安全
   - 避免缓存穿透

5. 推荐工具:
   - functools.lru_cache (标准库)
   - cachetools (更多策略)
   - redis/memcached (分布式缓存)
""")
