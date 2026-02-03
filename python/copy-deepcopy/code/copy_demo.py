#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 浅拷贝与深拷贝 (Copy & Deepcopy) 完整示例
演示对象复制的陷阱和正确用法
"""

import copy
from typing import List, Dict, Any


# ============ 1. 赋值 vs 拷贝 ============
print("=" * 50)
print("1. 赋值 vs 拷贝")
print("=" * 50)

# 赋值只是创建引用
original = [1, 2, 3]
assigned = original  # 不是拷贝!

print(f"original: {original}")
print(f"assigned: {assigned}")
print(f"是同一对象: {original is assigned}")

# 修改会影响双方
assigned.append(4)
print(f"修改assigned后:")
print(f"  original: {original}")
print(f"  assigned: {assigned}")


# ============ 2. 浅拷贝 (Shallow Copy) ============
print("\n" + "=" * 50)
print("2. 浅拷贝")
print("=" * 50)

# 方式1: copy()方法
original = [1, 2, 3]
shallow1 = original.copy()
print(f"list.copy(): {shallow1}")

# 方式2: 切片
shallow2 = original[:]
print(f"切片[:]: {shallow2}")

# 方式3: list()构造器
shallow3 = list(original)
print(f"list(): {shallow3}")

# 方式4: copy模块
shallow4 = copy.copy(original)
print(f"copy.copy(): {shallow4}")

# 验证是不同对象
print(f"\n是同一对象: {original is shallow1}")
print(f"内容相等: {original == shallow1}")

# 修改不影响原对象
shallow1.append(4)
print(f"修改shallow1后:")
print(f"  original: {original}")
print(f"  shallow1: {shallow1}")


# ============ 3. 浅拷贝的陷阱 ============
print("\n" + "=" * 50)
print("3. 浅拷贝的陷阱 (嵌套对象)")
print("=" * 50)

# 嵌套列表
original = [[1, 2], [3, 4], [5, 6]]
shallow = original.copy()

print(f"original: {original}")
print(f"shallow: {shallow}")
print(f"外层是不同对象: {original is not shallow}")
print(f"内层是同一对象: {original[0] is shallow[0]}")

# 修改内层会影响原对象!
shallow[0].append(999)
print(f"\n修改shallow[0]后:")
print(f"  original: {original}")  # 也被修改了!
print(f"  shallow: {shallow}")

# 修改外层不影响
shallow.append([7, 8])
print(f"\n添加新元素到shallow后:")
print(f"  original: {original}")
print(f"  shallow: {shallow}")


# ============ 4. 深拷贝 (Deep Copy) ============
print("\n" + "=" * 50)
print("4. 深拷贝")
print("=" * 50)

original = [[1, 2], [3, 4], {"key": "value"}]
deep = copy.deepcopy(original)

print(f"original: {original}")
print(f"deep: {deep}")
print(f"外层不同: {original is not deep}")
print(f"内层也不同: {original[0] is not deep[0]}")
print(f"字典也不同: {original[2] is not deep[2]}")

# 修改任何层级都不影响原对象
deep[0].append(999)
deep[2]["new"] = "data"
print(f"\n修改deep后:")
print(f"  original: {original}")
print(f"  deep: {deep}")


# ============ 5. 字典的拷贝 ============
print("\n" + "=" * 50)
print("5. 字典的拷贝")
print("=" * 50)

# 浅拷贝
original = {"a": 1, "b": [1, 2, 3], "c": {"nested": True}}
shallow = original.copy()  # 或 dict(original)

print(f"original: {original}")
print(f"shallow: {shallow}")

# 修改嵌套对象
shallow["b"].append(4)
print(f"\n修改shallow['b']后:")
print(f"  original: {original}")  # 也被修改!
print(f"  shallow: {shallow}")

# 深拷贝
original = {"a": 1, "b": [1, 2, 3], "c": {"nested": True}}
deep = copy.deepcopy(original)
deep["b"].append(4)
deep["c"]["new"] = "value"
print(f"\n深拷贝后修改:")
print(f"  original: {original}")  # 不受影响
print(f"  deep: {deep}")


# ============ 6. 自定义类的拷贝 ============
print("\n" + "=" * 50)
print("6. 自定义类的拷贝")
print("=" * 50)

class Person:
    def __init__(self, name: str, friends: List[str]):
        self.name = name
        self.friends = friends
    
    def __repr__(self):
        return f"Person({self.name!r}, friends={self.friends})"

person1 = Person("Alice", ["Bob", "Charlie"])

# 浅拷贝
person2 = copy.copy(person1)
print(f"person1: {person1}")
print(f"person2: {person2}")
print(f"friends是同一对象: {person1.friends is person2.friends}")

# 修改friends会影响两者
person2.friends.append("David")
print(f"\n修改person2.friends后:")
print(f"  person1: {person1}")
print(f"  person2: {person2}")

# 深拷贝
person3 = copy.deepcopy(person1)
person3.friends.append("Eve")
print(f"\n深拷贝后修改:")
print(f"  person1: {person1}")
print(f"  person3: {person3}")


# ============ 7. 自定义拷贝行为 ============
print("\n" + "=" * 50)
print("7. 自定义拷贝行为 (__copy__/__deepcopy__)")
print("=" * 50)

class SmartObject:
    """自定义拷贝行为的类"""
    
    def __init__(self, value: int, cache: dict = None):
        self.value = value
        self.cache = cache or {}
        self._computed = None  # 不需要拷贝的临时数据
    
    def __copy__(self):
        """浅拷贝时调用"""
        print("  调用 __copy__")
        new_obj = SmartObject(self.value)
        new_obj.cache = self.cache  # 浅拷贝cache
        # 不拷贝 _computed
        return new_obj
    
    def __deepcopy__(self, memo):
        """深拷贝时调用"""
        print("  调用 __deepcopy__")
        new_obj = SmartObject(self.value)
        new_obj.cache = copy.deepcopy(self.cache, memo)
        # 不拷贝 _computed
        return new_obj
    
    def __repr__(self):
        return f"SmartObject(value={self.value}, cache={self.cache})"

obj = SmartObject(42, {"key": [1, 2, 3]})
obj._computed = "临时数据"

print("浅拷贝:")
shallow = copy.copy(obj)
print(f"  original._computed: {obj._computed}")
print(f"  shallow._computed: {shallow._computed}")

print("\n深拷贝:")
deep = copy.deepcopy(obj)
deep.cache["key"].append(4)
print(f"  original.cache: {obj.cache}")
print(f"  deep.cache: {deep.cache}")


# ============ 8. 循环引用 ============
print("\n" + "=" * 50)
print("8. 循环引用处理")
print("=" * 50)

# 创建循环引用
a = [1, 2]
b = [3, 4]
a.append(b)
b.append(a)

print(f"a: {a}")  # 会显示 [...] 表示循环
print(f"b: {b}")
print(f"a[2] is b: {a[2] is b}")
print(f"b[2] is a: {b[2] is a}")

# deepcopy 正确处理循环引用
a_copy = copy.deepcopy(a)
print(f"\n深拷贝后:")
print(f"a_copy[2] is a_copy: {a_copy[2][2] is a_copy}")  # 循环引用被保持


# ============ 9. 不可变对象 ============
print("\n" + "=" * 50)
print("9. 不可变对象的拷贝")
print("=" * 50)

# 不可变对象(int, str, tuple)拷贝时返回同一对象
num = 42
num_copy = copy.copy(num)
print(f"int: {num is num_copy}")  # True

text = "hello"
text_copy = copy.copy(text)
print(f"str: {text is text_copy}")  # True

tup = (1, 2, 3)
tup_copy = copy.copy(tup)
print(f"tuple: {tup is tup_copy}")  # True

# 但包含可变元素的元组
tup_with_list = (1, [2, 3], 4)
tup_copy = copy.deepcopy(tup_with_list)
print(f"\n元组内的列表:")
print(f"  浅拷贝后列表相同: {copy.copy(tup_with_list)[1] is tup_with_list[1]}")
print(f"  深拷贝后列表不同: {tup_copy[1] is not tup_with_list[1]}")


# ============ 10. 实用函数 ============
print("\n" + "=" * 50)
print("10. 实用函数")
print("=" * 50)

def safe_update(original: Dict, updates: Dict) -> Dict:
    """安全更新字典(不修改原字典)"""
    result = copy.deepcopy(original)
    result.update(updates)
    return result

def clone_with_override(obj: Any, **overrides) -> Any:
    """克隆对象并覆盖属性"""
    cloned = copy.deepcopy(obj)
    for key, value in overrides.items():
        setattr(cloned, key, value)
    return cloned

# 使用示例
config = {"debug": False, "settings": {"timeout": 30}}
new_config = safe_update(config, {"debug": True})
print(f"original config: {config}")
print(f"new config: {new_config}")

person = Person("Alice", ["Bob"])
person2 = clone_with_override(person, name="Charlie")
print(f"original person: {person}")
print(f"cloned person: {person2}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("拷贝总结")
print("=" * 50)
print("""
三种"复制"方式:
1. 赋值 (=): 只创建引用,共享同一对象
2. 浅拷贝: 创建新对象,但内部引用相同
3. 深拷贝: 完全独立的副本

浅拷贝方法:
- list.copy(), dict.copy()
- 切片 [:]
- 构造器 list(), dict()
- copy.copy()

深拷贝方法:
- copy.deepcopy()

使用建议:
- 简单对象 -> 浅拷贝
- 嵌套对象 -> 深拷贝
- 性能敏感 -> 谨慎使用深拷贝
- 自定义类 -> 实现__copy__/__deepcopy__
""")
