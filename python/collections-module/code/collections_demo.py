#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python collections 模块完整示例
演示高级容器数据类型
"""

from collections import (
    namedtuple, deque, ChainMap, Counter,
    OrderedDict, defaultdict, UserDict, UserList, UserString
)
from typing import List, Dict


# ============ 1. namedtuple 命名元组 ============
print("=" * 50)
print("1. namedtuple 命名元组")
print("=" * 50)

# 创建命名元组类
Point = namedtuple("Point", ["x", "y"])
Person = namedtuple("Person", "name age email")

# 使用
p = Point(3, 4)
person = Person("Alice", 25, "alice@example.com")

print(f"Point: {p}")
print(f"x={p.x}, y={p.y}")
print(f"通过索引: {p[0]}, {p[1]}")
print(f"Person: {person}")
print(f"name={person.name}")

# 转换
print(f"转为字典: {p._asdict()}")
print(f"替换值: {p._replace(x=10)}")

# 带默认值 (Python 3.7+)
Point3D = namedtuple("Point3D", ["x", "y", "z"], defaults=[0])
p3 = Point3D(1, 2)
print(f"带默认值: {p3}")


# ============ 2. deque 双端队列 ============
print("\n" + "=" * 50)
print("2. deque 双端队列")
print("=" * 50)

# 创建 deque
d = deque([1, 2, 3, 4, 5])
print(f"初始: {d}")

# 两端操作
d.append(6)        # 右端添加
d.appendleft(0)    # 左端添加
print(f"添加后: {d}")

d.pop()            # 右端弹出
d.popleft()        # 左端弹出
print(f"弹出后: {d}")

# 旋转
d.rotate(2)        # 右旋转2位
print(f"右旋转2: {d}")
d.rotate(-2)       # 左旋转2位
print(f"左旋转2: {d}")

# 扩展
d.extend([6, 7, 8])
d.extendleft([-1, -2])  # 注意：会反转顺序
print(f"扩展后: {d}")

# 固定大小队列
fixed = deque(maxlen=3)
for i in range(5):
    fixed.append(i)
    print(f"  添加{i}: {list(fixed)}")


# ============ 3. Counter 计数器 ============
print("\n" + "=" * 50)
print("3. Counter 计数器")
print("=" * 50)

# 创建计数器
text = "abracadabra"
counter = Counter(text)
print(f"字符计数: {counter}")
print(f"最常见3个: {counter.most_common(3)}")

# 计数操作
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_count = Counter(words)
print(f"单词计数: {word_count}")

# 算术操作
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(f"c1 + c2: {c1 + c2}")
print(f"c1 - c2: {c1 - c2}")  # 只保留正数
print(f"c1 & c2 (交集): {c1 & c2}")
print(f"c1 | c2 (并集): {c1 | c2}")

# 更新
counter.update("xyz")
print(f"更新后: {counter}")

# 元素迭代
print(f"所有元素: {list(counter.elements())[:10]}...")


# ============ 4. defaultdict 默认字典 ============
print("\n" + "=" * 50)
print("4. defaultdict 默认字典")
print("=" * 50)

# 默认值工厂
int_dict = defaultdict(int)
list_dict = defaultdict(list)
set_dict = defaultdict(set)

# 自动创建默认值
int_dict["count"] += 1
int_dict["count"] += 1
print(f"int默认值: {dict(int_dict)}")

# 分组数据
students = [
    ("Alice", "Math"),
    ("Bob", "English"),
    ("Alice", "Science"),
    ("Bob", "Math"),
    ("Charlie", "Math"),
]

by_student = defaultdict(list)
for name, subject in students:
    by_student[name].append(subject)
print(f"按学生分组: {dict(by_student)}")

by_subject = defaultdict(set)
for name, subject in students:
    by_subject[subject].add(name)
print(f"按科目分组: {dict(by_subject)}")

# 自定义默认值
def default_value():
    return {"count": 0, "items": []}

custom_dict = defaultdict(default_value)
custom_dict["user"]["count"] += 1
custom_dict["user"]["items"].append("item1")
print(f"自定义默认值: {dict(custom_dict)}")


# ============ 5. OrderedDict 有序字典 ============
print("\n" + "=" * 50)
print("5. OrderedDict 有序字典")
print("=" * 50)

# 注意: Python 3.7+ 普通 dict 也保持插入顺序
# OrderedDict 提供额外功能

od = OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3

print(f"OrderedDict: {od}")

# 移动到末尾
od.move_to_end("a")
print(f"移动a到末尾: {od}")

# 移动到开头
od.move_to_end("c", last=False)
print(f"移动c到开头: {od}")

# 弹出最后/第一个
od.popitem(last=True)   # 弹出最后
print(f"弹出最后: {od}")

# 比较顺序（与普通dict的区别）
d1 = OrderedDict([("a", 1), ("b", 2)])
d2 = OrderedDict([("b", 2), ("a", 1)])
print(f"OrderedDict比较顺序: {d1 == d2}")  # False

d3 = {"a": 1, "b": 2}
d4 = {"b": 2, "a": 1}
print(f"普通dict比较: {d3 == d4}")  # True


# ============ 6. ChainMap 链式映射 ============
print("\n" + "=" * 50)
print("6. ChainMap 链式映射")
print("=" * 50)

# 多个字典的逻辑视图
defaults = {"theme": "light", "language": "en", "debug": False}
user_config = {"theme": "dark"}
env_config = {"debug": True}

config = ChainMap(env_config, user_config, defaults)

print(f"theme: {config['theme']}")      # 从user_config
print(f"debug: {config['debug']}")      # 从env_config
print(f"language: {config['language']}") # 从defaults

# 修改只影响第一个字典
config["new_key"] = "value"
print(f"env_config被修改: {env_config}")

# 获取所有键
print(f"所有键: {list(config.keys())}")

# 子链
child = config.new_child({"debug": False})
print(f"子链 debug: {child['debug']}")
print(f"父链 debug: {config['debug']}")


# ============ 7. UserDict/UserList/UserString ============
print("\n" + "=" * 50)
print("7. 自定义容器基类")
print("=" * 50)

class ValidatedDict(UserDict):
    """验证字典 - 只接受字符串键"""
    
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("键必须是字符串")
        super().__setitem__(key, value)

class HistoryList(UserList):
    """历史列表 - 记录所有添加的元素"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []
    
    def append(self, item):
        self.history.append(("append", item))
        super().append(item)
    
    def extend(self, items):
        self.history.append(("extend", list(items)))
        super().extend(items)

class CaseInsensitiveString(UserString):
    """不区分大小写的字符串比较"""
    
    def __eq__(self, other):
        return self.data.lower() == str(other).lower()
    
    def __hash__(self):
        return hash(self.data.lower())

# 使用
vd = ValidatedDict()
vd["name"] = "Alice"
try:
    vd[123] = "value"
except TypeError as e:
    print(f"验证错误: {e}")

hl = HistoryList([1, 2])
hl.append(3)
hl.extend([4, 5])
print(f"HistoryList: {hl.data}")
print(f"历史记录: {hl.history}")

s1 = CaseInsensitiveString("Hello")
print(f"'Hello' == 'hello': {s1 == 'hello'}")


# ============ 8. 实际应用示例 ============
print("\n" + "=" * 50)
print("8. 实际应用示例")
print("=" * 50)

# 8.1 LRU缓存 (使用OrderedDict)
class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

cache = LRUCache(3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
cache.get("a")  # 访问a
cache.put("d", 4)  # 淘汰b
print(f"LRU缓存: {list(cache.cache.keys())}")


# 8.2 词频统计
def word_frequency(text: str) -> Dict[str, int]:
    words = text.lower().split()
    return dict(Counter(words))

sample_text = "the quick brown fox jumps over the lazy dog the fox"
freq = word_frequency(sample_text)
print(f"词频: {freq}")


# 8.3 滑动窗口最大值
def sliding_window_max(nums: List[int], k: int) -> List[int]:
    if not nums or k <= 0:
        return []
    
    result = []
    window = deque()  # 存储索引
    
    for i, num in enumerate(nums):
        # 移除超出窗口的元素
        while window and window[0] < i - k + 1:
            window.popleft()
        
        # 保持单调递减
        while window and nums[window[-1]] < num:
            window.pop()
        
        window.append(i)
        
        if i >= k - 1:
            result.append(nums[window[0]])
    
    return result

nums = [1, 3, -1, -3, 5, 3, 6, 7]
print(f"滑动窗口最大值 (k=3): {sliding_window_max(nums, 3)}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("collections 模块总结")
print("=" * 50)
print("""
容器类型:
- namedtuple: 带名称的元组
- deque: 双端队列 (O(1)两端操作)
- Counter: 计数器
- defaultdict: 带默认值的字典
- OrderedDict: 有序字典
- ChainMap: 多字典视图

自定义基类:
- UserDict: 自定义字典
- UserList: 自定义列表
- UserString: 自定义字符串

使用场景:
- namedtuple: 简单数据类
- deque: 队列/滑动窗口
- Counter: 计数/统计
- defaultdict: 分组/聚合
- OrderedDict: LRU缓存
- ChainMap: 配置层级
""")
