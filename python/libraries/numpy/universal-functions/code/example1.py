"""
文件: example1.py
功能: 演示 NumPy 内置 ufunc 的基本用法，包括算术运算、数学函数和广播机制。
"""

import numpy as np


def main():
    # 创建两个一维数组
    a = np.array([1, 2, 3, 4])
    b = np.array([5, 6, 7, 8])

    # 使用 ufunc 进行加法运算（向量化）
    # np.add 是一个典型的二元 ufunc
    result_add = np.add(a, b)
    print(f"原始数组 a: {a}")
    print(f"原始数组 b: {b}")
    print(f"加法结果: {result_add}")

    # 使用一元 ufunc：计算平方根
    # np.sqrt 对数组中每个元素应用 sqrt 函数
    sqrt_a = np.sqrt(a)
    print(f"平方根结果: {sqrt_a}")

    # 使用三角函数 ufunc
    # 创建角度数组（单位：度）
    angles_deg = np.array([0, 30, 45, 60, 90])
    # 转换为弧度
    angles_rad = np.radians(angles_deg)
    # 计算正弦值，这是一个向量化操作
    sin_values = np.sin(angles_rad)
    print(f"角度数组（度）: {angles_deg}")
    print(f"正弦值: {sin_values}")


if __name__ == "__main__":
    main()