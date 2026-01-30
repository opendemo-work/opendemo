#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 位运算完整示例
演示位运算符和位操作技巧
"""


# ============ 1. 位运算符基础 ============
print("=" * 50)
print("1. 位运算符基础")
print("=" * 50)

a = 0b1100  # 12
b = 0b1010  # 10

print(f"a = {a} (0b{a:04b})")
print(f"b = {b} (0b{b:04b})")
print()

# AND: 两位都为1才为1
print(f"a & b  = {a & b:2} (0b{a & b:04b}) - 按位与 AND")

# OR: 任一位为1就为1
print(f"a | b  = {a | b:2} (0b{a | b:04b}) - 按位或 OR")

# XOR: 两位不同为1
print(f"a ^ b  = {a ^ b:2} (0b{a ^ b:04b}) - 按位异或 XOR")

# NOT: 取反 (结果为 -(n+1))
print(f"~a     = {~a:2}         - 按位取反 NOT")

# 左移: 乘以 2^n
print(f"a << 2 = {a << 2:2} (0b{a << 2:06b}) - 左移2位")

# 右移: 除以 2^n
print(f"a >> 2 = {a >> 2:2} (0b{a >> 2:02b})   - 右移2位")


# ============ 2. 二进制表示 ============
print("\n" + "=" * 50)
print("2. 二进制表示")
print("=" * 50)

num = 42
print(f"十进制: {num}")
print(f"二进制: {bin(num)}")
print(f"八进制: {oct(num)}")
print(f"十六进制: {hex(num)}")

# 格式化二进制
print(f"格式化(8位): {num:08b}")
print(f"格式化(带前缀): {num:#010b}")

# 位数
print(f"位数 bit_length(): {num.bit_length()}")


# ============ 3. 位操作技巧 ============
print("\n" + "=" * 50)
print("3. 位操作技巧")
print("=" * 50)

# 检查奇偶
def is_odd(n):
    return n & 1 == 1

print(f"5 是奇数: {is_odd(5)}")
print(f"6 是奇数: {is_odd(6)}")

# 乘除2的幂
x = 10
print(f"\n10 * 2 = {x << 1} (左移1位)")
print(f"10 * 4 = {x << 2} (左移2位)")
print(f"10 // 2 = {x >> 1} (右移1位)")
print(f"10 // 4 = {x >> 2} (右移2位)")

# 交换两个数 (不用临时变量)
a, b = 5, 9
print(f"\n交换前: a={a}, b={b}")
a ^= b
b ^= a
a ^= b
print(f"交换后: a={a}, b={b}")


# ============ 4. 位掩码操作 ============
print("\n" + "=" * 50)
print("4. 位掩码操作")
print("=" * 50)

# 权限系统示例
READ    = 0b001  # 1
WRITE   = 0b010  # 2
EXECUTE = 0b100  # 4

print(f"READ    = {READ:03b} ({READ})")
print(f"WRITE   = {WRITE:03b} ({WRITE})")
print(f"EXECUTE = {EXECUTE:03b} ({EXECUTE})")

# 设置权限
permission = READ | WRITE
print(f"\n设置读写权限: {permission:03b} ({permission})")

# 检查权限
has_read = permission & READ
has_execute = permission & EXECUTE
print(f"有读权限: {bool(has_read)}")
print(f"有执行权限: {bool(has_execute)}")

# 添加权限
permission |= EXECUTE
print(f"添加执行权限: {permission:03b} ({permission})")

# 移除权限
permission &= ~WRITE
print(f"移除写权限: {permission:03b} ({permission})")

# 切换权限
permission ^= READ
print(f"切换读权限: {permission:03b} ({permission})")


# ============ 5. 位操作函数 ============
print("\n" + "=" * 50)
print("5. 位操作函数")
print("=" * 50)

def get_bit(n, pos):
    """获取第 pos 位的值"""
    return (n >> pos) & 1

def set_bit(n, pos):
    """将第 pos 位设为 1"""
    return n | (1 << pos)

def clear_bit(n, pos):
    """将第 pos 位设为 0"""
    return n & ~(1 << pos)

def toggle_bit(n, pos):
    """切换第 pos 位"""
    return n ^ (1 << pos)

num = 0b10110  # 22
print(f"num = {num} (0b{num:05b})")
print(f"get_bit(num, 0) = {get_bit(num, 0)}")
print(f"get_bit(num, 1) = {get_bit(num, 1)}")
print(f"set_bit(num, 0) = {set_bit(num, 0)} (0b{set_bit(num, 0):05b})")
print(f"clear_bit(num, 1) = {clear_bit(num, 1)} (0b{clear_bit(num, 1):05b})")
print(f"toggle_bit(num, 2) = {toggle_bit(num, 2)} (0b{toggle_bit(num, 2):05b})")


# ============ 6. 常用位操作算法 ============
print("\n" + "=" * 50)
print("6. 常用位操作算法")
print("=" * 50)

# 统计1的个数 (popcount)
def count_ones(n):
    count = 0
    while n:
        n &= n - 1  # 清除最低位的1
        count += 1
    return count

print(f"count_ones(0b10110) = {count_ones(0b10110)}")
print(f"内置: (0b10110).bit_count() = {(0b10110).bit_count()}")

# 判断是否为2的幂
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

print(f"\nis_power_of_two(8) = {is_power_of_two(8)}")
print(f"is_power_of_two(10) = {is_power_of_two(10)}")

# 获取最低位的1
def lowest_bit(n):
    return n & (-n)

num = 0b10100
print(f"\nlowest_bit(0b10100) = {lowest_bit(num)} (0b{lowest_bit(num):05b})")

# 向上取整到2的幂
def next_power_of_two(n):
    if n == 0:
        return 1
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return n + 1

print(f"next_power_of_two(5) = {next_power_of_two(5)}")
print(f"next_power_of_two(8) = {next_power_of_two(8)}")


# ============ 7. 位运算应用 ============
print("\n" + "=" * 50)
print("7. 位运算应用")
print("=" * 50)

# 应用1: IP地址转换
def ip_to_int(ip):
    """IP地址转整数"""
    parts = [int(p) for p in ip.split('.')]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

def int_to_ip(num):
    """整数转IP地址"""
    return '.'.join([
        str((num >> 24) & 0xFF),
        str((num >> 16) & 0xFF),
        str((num >> 8) & 0xFF),
        str(num & 0xFF)
    ])

ip = "192.168.1.100"
ip_int = ip_to_int(ip)
print(f"IP: {ip} -> {ip_int}")
print(f"Int: {ip_int} -> {int_to_ip(ip_int)}")

# 应用2: 颜色处理
def rgb_to_hex(r, g, b):
    """RGB转十六进制"""
    return (r << 16) | (g << 8) | b

def hex_to_rgb(color):
    """十六进制转RGB"""
    return (
        (color >> 16) & 0xFF,
        (color >> 8) & 0xFF,
        color & 0xFF
    )

color = rgb_to_hex(255, 128, 64)
print(f"\nRGB(255, 128, 64) -> #{color:06X}")
print(f"#{color:06X} -> RGB{hex_to_rgb(color)}")


# ============ 8. 位域与标志 ============
print("\n" + "=" * 50)
print("8. 位域与标志")
print("=" * 50)

from enum import Flag, auto

class FileMode(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    
    @classmethod
    def from_int(cls, value):
        return cls(value)

# 使用Flag枚举
mode = FileMode.READ | FileMode.WRITE
print(f"mode = {mode}")
print(f"mode.value = {mode.value}")
print(f"READ in mode: {FileMode.READ in mode}")
print(f"EXECUTE in mode: {FileMode.EXECUTE in mode}")


# ============ 9. 有符号数处理 ============
print("\n" + "=" * 50)
print("9. 有符号数处理")
print("=" * 50)

# Python整数无限精度，需要模拟固定位数
def to_signed_8bit(n):
    """转换为8位有符号数"""
    n = n & 0xFF  # 限制为8位
    if n >= 0x80:  # 最高位为1
        n -= 0x100
    return n

print(f"to_signed_8bit(255) = {to_signed_8bit(255)}")
print(f"to_signed_8bit(127) = {to_signed_8bit(127)}")
print(f"to_signed_8bit(128) = {to_signed_8bit(128)}")

# 获取补码
def twos_complement(n, bits=8):
    """获取补码"""
    if n < 0:
        return (1 << bits) + n
    return n

print(f"\ntwos_complement(-1, 8) = {twos_complement(-1, 8):08b}")
print(f"twos_complement(-5, 8) = {twos_complement(-5, 8):08b}")


print("\n" + "=" * 50)
print("所有位运算示例完成!")
print("=" * 50)
