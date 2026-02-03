"""
文件: example1.py
功能: 学生成绩管理系统 - 演示数组的基本操作
作者: Python导师
日期: 2024
"""

# 定义一个包含学生成绩的列表（模拟数组）
scores = [85, 92, 78, 96, 88]

# 输出原始数据
print("--- 学生成绩管理系统 ---")
print(f"所有成绩: {scores}")

# 计算并输出最高分
max_score = max(scores)
print(f"最高分: {max_score}")

# 计算并输出最低分
min_score = min(scores)
print(f"最低分: {min_score}")

# 计算平均分：总分除以人数
average_score = sum(scores) / len(scores)
print(f"平均分: {average_score:.1f}")  # 保留一位小数