"""
文件: example2.py
功能: 温度转换与分析 - 演示数组的映射与过滤操作
作者: Python导师
日期: 2024
"""

# 定义一组摄氏温度（模拟传感器数据）
celsius_temps = [0, 10, 20, 30, 40]

# 创建空列表用于存储转换后的华氏温度
fahrenheit_temps = []

# 遍历每个摄氏温度，转换为华氏温度并添加到新列表
# 转换公式: F = C * 9/5 + 32
for c in celsius_temps:
    f = c * 9/5 + 32
    fahrenheit_temps.append(f)

# 输出标题和原始数据
print("--- 摄氏温度转华氏温度并分析 ---")
print(f"原始摄氏温度: {celsius_temps}")
print(f"对应华氏温度: {fahrenheit_temps}")

# 计算摄氏温度的平均值
celsius_average = sum(celsius_temps) / len(celsius_temps)

# 创建新列表，存储高于平均值的摄氏温度
above_average = []
for temp in celsius_temps:
    if temp > celsius_average:
        above_average.append(temp)

# 输出分析结果
print(f"高于平均值的温度 (°C): {above_average}")