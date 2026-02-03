"""
文件: example1.py
功能: 演示集合的基本操作——去重与集合运算
作者: Python导师
日期: 2024
"""

# 定义原始数据（含重复元素）
data_list = [1, 2, 2, 3, 4, 4, 5]
print(f"原始列表: {data_list}")

# 使用集合进行去重
unique_set = set(data_list)
print(f"去重后集合: {unique_set}")

# 创建两个集合用于演示集合运算
set_a = {1, 2, 3, 4, 5}
set_b = {3, 4, 5, 6, 7}

# 交集：同时存在于A和B中的元素
intersection = set_a & set_b  # 等价于 set_a.intersection(set_b)
print(f"A与B的交集: {intersection}")

# 并集：存在于A或B中的所有元素
union = set_a | set_b  # 等价于 set_a.union(set_b)
print(f"A与B的并集: {union}")

# 差集：存在于A但不存在于B中的元素
difference = set_a - set_b  # 等价于 set_a.difference(set_b)
print(f"A与B的差集 (A-B): {difference}")

# 对称差集：存在于A或B中，但不同时存在于两者中的元素
symmetric_diff = set_a ^ set_b  # 等价于 set_a.symmetric_difference(set_b)
print(f"A与B的对称差集: {symmetric_diff}")