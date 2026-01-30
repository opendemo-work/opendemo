#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 数值运算完整示例
演示 math、decimal、fractions 模块和数值操作
"""

import math
from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_DOWN
from fractions import Fraction
import random
import statistics


# ============ 1. 基本数值类型 ============
print("=" * 50)
print("1. 基本数值类型")
print("=" * 50)

# 整数 (无限精度)
big_int = 10 ** 100
print(f"大整数: 10^100 = {str(big_int)[:30]}...")
print(f"整数位数: {len(str(big_int))}")

# 浮点数 (IEEE 754 双精度)
pi = 3.14159265358979323846
print(f"\n浮点数 pi: {pi}")
print(f"浮点数精度问题: 0.1 + 0.2 = {0.1 + 0.2}")

# 复数
z = 3 + 4j
print(f"\n复数: {z}")
print(f"实部: {z.real}, 虚部: {z.imag}")
print(f"共轭: {z.conjugate()}")
print(f"模: {abs(z)}")


# ============ 2. 数值进制转换 ============
print("\n" + "=" * 50)
print("2. 数值进制转换")
print("=" * 50)

num = 255

print(f"十进制: {num}")
print(f"二进制: {bin(num)}")
print(f"八进制: {oct(num)}")
print(f"十六进制: {hex(num)}")

# 字面量表示
binary = 0b11111111
octal = 0o377
hexadecimal = 0xFF
print(f"\n0b11111111 = {binary}")
print(f"0o377 = {octal}")
print(f"0xFF = {hexadecimal}")

# 进制转换
print(f"\nint('ff', 16) = {int('ff', 16)}")
print(f"int('11111111', 2) = {int('11111111', 2)}")


# ============ 3. math 模块 ============
print("\n" + "=" * 50)
print("3. math 模块")
print("=" * 50)

# 常量
print(f"pi = {math.pi}")
print(f"e = {math.e}")
print(f"tau = {math.tau}")
print(f"inf = {math.inf}")
print(f"nan = {math.nan}")

# 基本函数
print(f"\n基本函数:")
print(f"  sqrt(16) = {math.sqrt(16)}")
print(f"  pow(2, 10) = {math.pow(2, 10)}")
print(f"  exp(1) = {math.exp(1)}")
print(f"  log(e) = {math.log(math.e)}")
print(f"  log10(100) = {math.log10(100)}")
print(f"  log2(8) = {math.log2(8)}")

# 取整函数
print(f"\n取整函数:")
print(f"  floor(3.7) = {math.floor(3.7)}")
print(f"  ceil(3.2) = {math.ceil(3.2)}")
print(f"  trunc(-3.7) = {math.trunc(-3.7)}")
print(f"  round(3.5) = {round(3.5)}")  # 银行家舍入

# 三角函数
print(f"\n三角函数:")
print(f"  sin(pi/2) = {math.sin(math.pi/2)}")
print(f"  cos(0) = {math.cos(0)}")
print(f"  tan(pi/4) = {math.tan(math.pi/4)}")
print(f"  degrees(pi) = {math.degrees(math.pi)}")
print(f"  radians(180) = {math.radians(180)}")

# 其他函数
print(f"\n其他函数:")
print(f"  factorial(5) = {math.factorial(5)}")
print(f"  gcd(48, 18) = {math.gcd(48, 18)}")
print(f"  lcm(4, 6) = {math.lcm(4, 6)}")
print(f"  copysign(1.0, -3) = {math.copysign(1.0, -3)}")
print(f"  isclose(0.1+0.2, 0.3) = {math.isclose(0.1+0.2, 0.3)}")


# ============ 4. Decimal 高精度计算 ============
print("\n" + "=" * 50)
print("4. Decimal 高精度计算")
print("=" * 50)

# 精度问题对比
print("浮点数问题:")
print(f"  float: 0.1 + 0.2 = {0.1 + 0.2}")
print(f"  Decimal: {Decimal('0.1') + Decimal('0.2')}")

# 设置精度
getcontext().prec = 50
print(f"\n高精度计算 1/7:")
print(f"  {Decimal(1) / Decimal(7)}")

# 舍入模式
getcontext().prec = 4
d = Decimal('1.2345')
print(f"\n舍入模式 (原值: {d}):")
print(f"  ROUND_HALF_UP: {d.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)}")
print(f"  ROUND_DOWN: {d.quantize(Decimal('0.001'), rounding=ROUND_DOWN)}")

# 金融计算
getcontext().prec = 28
price = Decimal('19.99')
tax_rate = Decimal('0.0725')
tax = (price * tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
total = price + tax
print(f"\n金融计算:")
print(f"  价格: ${price}")
print(f"  税率: {tax_rate}")
print(f"  税额: ${tax}")
print(f"  总计: ${total}")


# ============ 5. Fraction 分数运算 ============
print("\n" + "=" * 50)
print("5. Fraction 分数运算")
print("=" * 50)

# 创建分数
f1 = Fraction(1, 3)
f2 = Fraction(2, 5)
f3 = Fraction('3/7')
f4 = Fraction(0.5)

print(f"f1 = {f1}")
print(f"f2 = {f2}")
print(f"f3 = {f3}")
print(f"f4 = {f4}")

# 分数运算
print(f"\n分数运算:")
print(f"  {f1} + {f2} = {f1 + f2}")
print(f"  {f1} * {f2} = {f1 * f2}")
print(f"  {f1} / {f2} = {f1 / f2}")

# 分数属性
print(f"\n分数属性:")
print(f"  分子: {f1.numerator}")
print(f"  分母: {f1.denominator}")
print(f"  小数值: {float(f1)}")

# 限制分母
pi_fraction = Fraction(math.pi).limit_denominator(1000)
print(f"\npi 近似分数: {pi_fraction}")


# ============ 6. random 随机数 ============
print("\n" + "=" * 50)
print("6. random 随机数")
print("=" * 50)

# 设置种子 (可重现)
random.seed(42)

print(f"random(): {random.random():.4f}")
print(f"randint(1, 10): {random.randint(1, 10)}")
print(f"randrange(0, 100, 5): {random.randrange(0, 100, 5)}")
print(f"uniform(1.0, 10.0): {random.uniform(1.0, 10.0):.4f}")

# 序列操作
items = ['A', 'B', 'C', 'D', 'E']
print(f"\nchoice({items}): {random.choice(items)}")
print(f"choices({items}, k=3): {random.choices(items, k=3)}")
print(f"sample({items}, k=3): {random.sample(items, k=3)}")

shuffled = items.copy()
random.shuffle(shuffled)
print(f"shuffle后: {shuffled}")

# 分布
print(f"\n分布:")
print(f"  正态分布 gauss(0, 1): {random.gauss(0, 1):.4f}")
print(f"  指数分布 expovariate(1.5): {random.expovariate(1.5):.4f}")


# ============ 7. statistics 统计 ============
print("\n" + "=" * 50)
print("7. statistics 统计")
print("=" * 50)

data = [2, 4, 4, 4, 5, 5, 7, 9]
print(f"数据: {data}")

print(f"\n集中趋势:")
print(f"  平均值 mean: {statistics.mean(data)}")
print(f"  中位数 median: {statistics.median(data)}")
print(f"  众数 mode: {statistics.mode(data)}")

print(f"\n离散程度:")
print(f"  样本方差 variance: {statistics.variance(data)}")
print(f"  样本标准差 stdev: {statistics.stdev(data):.4f}")
print(f"  总体方差 pvariance: {statistics.pvariance(data)}")
print(f"  总体标准差 pstdev: {statistics.pstdev(data):.4f}")

# 分位数
print(f"\n分位数:")
print(f"  四分位数: {statistics.quantiles(data, n=4)}")


# ============ 8. 位运算 ============
print("\n" + "=" * 50)
print("8. 位运算速览")
print("=" * 50)

a, b = 0b1100, 0b1010
print(f"a = {a} (0b{a:04b})")
print(f"b = {b} (0b{b:04b})")
print(f"a & b = {a & b} (0b{a & b:04b}) - AND")
print(f"a | b = {a | b} (0b{a | b:04b}) - OR")
print(f"a ^ b = {a ^ b} (0b{a ^ b:04b}) - XOR")
print(f"~a = {~a} - NOT")
print(f"a << 2 = {a << 2} (0b{a << 2:06b}) - 左移")
print(f"a >> 2 = {a >> 2} (0b{a >> 2:02b}) - 右移")


print("\n" + "=" * 50)
print("所有数值运算示例完成!")
print("=" * 50)
