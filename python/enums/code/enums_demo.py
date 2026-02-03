#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 枚举类型 (Enum) 完整示例
演示 enum 模块的各种用法
"""

from enum import Enum, IntEnum, Flag, IntFlag, auto, unique
from typing import Optional
from dataclasses import dataclass


# ============ 1. 基本枚举 ============
print("=" * 50)
print("1. 基本枚举")
print("=" * 50)

class Color(Enum):
    """颜色枚举"""
    RED = 1
    GREEN = 2
    BLUE = 3

# 访问枚举成员
print(f"Color.RED = {Color.RED}")
print(f"Color.RED.name = {Color.RED.name}")
print(f"Color.RED.value = {Color.RED.value}")

# 通过值获取成员
color = Color(2)
print(f"Color(2) = {color}")

# 通过名称获取成员
color = Color["BLUE"]
print(f"Color['BLUE'] = {color}")

# 遍历枚举
print("\n遍历枚举:")
for c in Color:
    print(f"  {c.name} = {c.value}")


# ============ 2. auto() 自动赋值 ============
print("\n" + "=" * 50)
print("2. auto() 自动赋值")
print("=" * 50)

class Priority(Enum):
    """优先级枚举 - 自动赋值"""
    LOW = auto()      # 1
    MEDIUM = auto()   # 2
    HIGH = auto()     # 3
    CRITICAL = auto() # 4

for p in Priority:
    print(f"  {p.name} = {p.value}")


# ============ 3. 字符串枚举 ============
print("\n" + "=" * 50)
print("3. 字符串枚举")
print("=" * 50)

class Status(Enum):
    """状态枚举 - 字符串值"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"

print(f"Status.PENDING.value = '{Status.PENDING.value}'")

# 实用：JSON序列化
import json
data = {"status": Status.APPROVED.value}
print(f"JSON: {json.dumps(data)}")


# ============ 4. IntEnum - 支持整数比较 ============
print("\n" + "=" * 50)
print("4. IntEnum - 支持整数比较")
print("=" * 50)

class Permission(IntEnum):
    """权限级别"""
    NONE = 0
    READ = 1
    WRITE = 2
    ADMIN = 3

# IntEnum可以直接与整数比较
print(f"Permission.READ == 1: {Permission.READ == 1}")
print(f"Permission.ADMIN > Permission.WRITE: {Permission.ADMIN > Permission.WRITE}")
print(f"Permission.READ + Permission.WRITE = {Permission.READ + Permission.WRITE}")


# ============ 5. Flag - 位标志 ============
print("\n" + "=" * 50)
print("5. Flag - 位标志组合")
print("=" * 50)

class FilePermission(Flag):
    """文件权限标志"""
    NONE = 0
    READ = auto()    # 1
    WRITE = auto()   # 2
    EXECUTE = auto() # 4
    
    # 组合权限
    READ_WRITE = READ | WRITE
    ALL = READ | WRITE | EXECUTE

# 组合权限
user_perm = FilePermission.READ | FilePermission.WRITE
print(f"用户权限: {user_perm}")
print(f"值: {user_perm.value}")

# 检查权限
print(f"有读权限: {FilePermission.READ in user_perm}")
print(f"有执行权限: {FilePermission.EXECUTE in user_perm}")

# 预定义组合
print(f"ALL权限: {FilePermission.ALL}")


# ============ 6. @unique 确保唯一性 ============
print("\n" + "=" * 50)
print("6. @unique 确保值唯一")
print("=" * 50)

@unique
class HttpStatus(Enum):
    """HTTP状态码 - 确保无重复"""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    SERVER_ERROR = 500

print("HttpStatus 成员:")
for status in HttpStatus:
    print(f"  {status.name}: {status.value}")


# ============ 7. 枚举方法 ============
print("\n" + "=" * 50)
print("7. 枚举自定义方法")
print("=" * 50)

class Planet(Enum):
    """行星枚举 - 带方法"""
    MERCURY = (3.303e+23, 2.4397e6)
    VENUS = (4.869e+24, 6.0518e6)
    EARTH = (5.976e+24, 6.37814e6)
    MARS = (6.421e+23, 3.3972e6)
    
    def __init__(self, mass: float, radius: float):
        self.mass = mass      # 质量 (kg)
        self.radius = radius  # 半径 (m)
    
    @property
    def surface_gravity(self) -> float:
        """表面重力加速度"""
        G = 6.67430e-11  # 万有引力常数
        return G * self.mass / (self.radius ** 2)
    
    def weight_on(self, earth_weight: float) -> float:
        """计算在该行星上的重量"""
        return earth_weight * self.surface_gravity / Planet.EARTH.surface_gravity

print("行星表面重力:")
for planet in Planet:
    print(f"  {planet.name}: {planet.surface_gravity:.2f} m/s^2")

print(f"\n地球上70kg在火星上的重量: {Planet.MARS.weight_on(70):.2f} kg")


# ============ 8. 枚举比较和哈希 ============
print("\n" + "=" * 50)
print("8. 枚举比较和哈希")
print("=" * 50)

class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

# 枚举成员是单例
print(f"Weekday.MONDAY is Weekday.MONDAY: {Weekday.MONDAY is Weekday.MONDAY}")
print(f"Weekday.MONDAY == Weekday.MONDAY: {Weekday.MONDAY == Weekday.MONDAY}")

# 可以用作字典键
schedule = {
    Weekday.MONDAY: "会议",
    Weekday.FRIDAY: "代码评审",
}
print(f"周一安排: {schedule.get(Weekday.MONDAY)}")

# 可以用于集合
weekend = {Weekday.SATURDAY, Weekday.SUNDAY}
print(f"周末: {weekend}")


# ============ 9. 枚举与数据类结合 ============
print("\n" + "=" * 50)
print("9. 枚举与数据类结合")
print("=" * 50)

class OrderStatus(Enum):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class Order:
    id: int
    product: str
    status: OrderStatus
    
    def can_cancel(self) -> bool:
        """是否可以取消"""
        return self.status in {OrderStatus.CREATED, OrderStatus.PAID}
    
    def next_status(self) -> Optional[OrderStatus]:
        """下一个状态"""
        transitions = {
            OrderStatus.CREATED: OrderStatus.PAID,
            OrderStatus.PAID: OrderStatus.SHIPPED,
            OrderStatus.SHIPPED: OrderStatus.DELIVERED,
        }
        return transitions.get(self.status)

order = Order(1, "Laptop", OrderStatus.PAID)
print(f"订单: {order}")
print(f"可取消: {order.can_cancel()}")
print(f"下一状态: {order.next_status()}")


# ============ 10. 状态机示例 ============
print("\n" + "=" * 50)
print("10. 状态机示例")
print("=" * 50)

class State(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"

class StateMachine:
    """简单状态机"""
    
    TRANSITIONS = {
        State.IDLE: {State.RUNNING},
        State.RUNNING: {State.PAUSED, State.STOPPED},
        State.PAUSED: {State.RUNNING, State.STOPPED},
        State.STOPPED: {State.IDLE},
    }
    
    def __init__(self):
        self._state = State.IDLE
    
    @property
    def state(self) -> State:
        return self._state
    
    def can_transition_to(self, new_state: State) -> bool:
        allowed = self.TRANSITIONS.get(self._state, set())
        return new_state in allowed
    
    def transition_to(self, new_state: State) -> bool:
        if self.can_transition_to(new_state):
            print(f"  {self._state.value} -> {new_state.value}")
            self._state = new_state
            return True
        print(f"  无法从 {self._state.value} 转换到 {new_state.value}")
        return False

machine = StateMachine()
print(f"初始状态: {machine.state.value}")
machine.transition_to(State.RUNNING)
machine.transition_to(State.PAUSED)
machine.transition_to(State.IDLE)  # 不允许
machine.transition_to(State.STOPPED)


# ============ 11. 枚举序列化 ============
print("\n" + "=" * 50)
print("11. 枚举JSON序列化")
print("=" * 50)

import json

class EnumEncoder(json.JSONEncoder):
    """枚举JSON编码器"""
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

def enum_decoder(enum_class):
    """创建枚举解码器"""
    def decode(value):
        return enum_class(value)
    return decode

# 序列化
data = {
    "status": Status.APPROVED,
    "priority": Priority.HIGH,
}
json_str = json.dumps(data, cls=EnumEncoder)
print(f"序列化: {json_str}")

# 反序列化
parsed = json.loads(json_str)
parsed["status"] = Status(parsed["status"])
parsed["priority"] = Priority(parsed["priority"])
print(f"反序列化: {parsed}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("枚举类型总结")
print("=" * 50)
print("""
枚举类型选择:
- Enum: 通用枚举
- IntEnum: 需要整数比较
- Flag: 位运算组合
- IntFlag: 位运算 + 整数比较

常用技巧:
- auto(): 自动赋值
- @unique: 确保值唯一
- 自定义方法和属性
- __init__: 多值枚举

最佳实践:
1. 使用枚举代替魔法数字/字符串
2. 字符串值便于序列化
3. 组合使用 Flag 处理权限
4. 状态机使用枚举表示状态
""")
