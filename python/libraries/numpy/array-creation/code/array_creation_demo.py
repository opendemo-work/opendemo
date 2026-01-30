"""
NumPy 数组创建示例

演示使用 numpy 创建数组的多种方法。
"""

import numpy as np


def create_from_list():
    """从 Python 列表创建数组"""
    print("=" * 50)
    print("1. 从列表创建数组")
    print("=" * 50)
    
    # 一维数组
    arr1d = np.array([1, 2, 3, 4, 5])
    print(f"一维数组: {arr1d}")
    print(f"形状: {arr1d.shape}, 维度: {arr1d.ndim}, 类型: {arr1d.dtype}")
    
    # 二维数组
    arr2d = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"\n二维数组:\n{arr2d}")
    print(f"形状: {arr2d.shape}, 维度: {arr2d.ndim}")
    print()


def create_with_zeros_ones():
    """使用 zeros 和 ones 创建数组"""
    print("=" * 50)
    print("2. 使用 zeros 和 ones 创建数组")
    print("=" * 50)
    
    # 全零数组
    zeros_arr = np.zeros((3, 4))
    print(f"全零数组 (3x4):\n{zeros_arr}")
    
    # 全一数组
    ones_arr = np.ones((2, 3))
    print(f"\n全一数组 (2x3):\n{ones_arr}")
    
    # 指定数据类型
    zeros_int = np.zeros(5, dtype=int)
    print(f"\n整型全零数组: {zeros_int}")
    print()


def create_with_arange_linspace():
    """使用 arange 和 linspace 创建等差数列"""
    print("=" * 50)
    print("3. 使用 arange 和 linspace 创建等差数列")
    print("=" * 50)
    
    # arange: 类似 Python 的 range
    arr_arange = np.arange(0, 10, 2)  # 起始值, 结束值(不包含), 步长
    print(f"arange(0, 10, 2): {arr_arange}")
    
    # linspace: 在指定范围内生成等间距的数值
    arr_linspace = np.linspace(0, 1, 5)  # 起始值, 结束值(包含), 数量
    print(f"linspace(0, 1, 5): {arr_linspace}")
    
    # 浮点数范围
    arr_float = np.arange(0, 1, 0.2)
    print(f"arange(0, 1, 0.2): {arr_float}")
    print()


def create_with_eye_identity():
    """创建单位矩阵和对角矩阵"""
    print("=" * 50)
    print("4. 创建单位矩阵和对角矩阵")
    print("=" * 50)
    
    # 单位矩阵
    identity = np.eye(3)
    print(f"3x3 单位矩阵:\n{identity}")
    
    # 对角矩阵
    diagonal = np.diag([1, 2, 3, 4])
    print(f"\n对角矩阵:\n{diagonal}")
    print()


def create_with_empty_full():
    """使用 empty 和 full 创建数组"""
    print("=" * 50)
    print("5. 使用 empty 和 full 创建数组")
    print("=" * 50)
    
    # empty: 创建未初始化的数组（内容随机）
    empty_arr = np.empty((2, 3))
    print(f"未初始化数组 (2x3):\n{empty_arr}")
    
    # full: 创建填充指定值的数组
    full_arr = np.full((3, 3), 7)
    print(f"\n填充值为 7 的数组 (3x3):\n{full_arr}")
    print()


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("NumPy 数组创建方法演示")
    print("=" * 50 + "\n")
    
    create_from_list()
    create_with_zeros_ones()
    create_with_arange_linspace()
    create_with_eye_identity()
    create_with_empty_full()
    
    print("=" * 50)
    print("演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
