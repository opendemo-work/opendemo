import numpy as np


def main():
    """
    演示基础矩阵乘法运算
    矩阵A (2x3) × 矩阵B (3x2) = 结果矩阵 (2x2)
    """
    
    # 创建第一个矩阵 A (2行3列)
    A = np.array([
        [1, 2, 3],
        [4, 5, 6]
    ])
    
    # 创建第二个矩阵 B (3行2列)
    B = np.array([
        [7, 8],
        [9, 10],
        [11, 12]
    ])
    
    # 方法1: 使用 @ 操作符进行矩阵乘法（推荐）
    result1 = A @ B
    
    # 方法2: 使用numpy的dot函数
    result2 = np.dot(A, B)
    
    # 验证两种方法结果相同
    assert np.allclose(result1, result2), "两种计算方法结果不一致！"
    
    # 输出结果
    print("矩阵 A:")
    print(A)
    print("矩阵 B:")
    print(B)
    print("A 与 B 的乘积:")
    print(result1)
    
    # 验证计算结果的正确性（手动验证第一个元素）
    manual_calc = 1*7 + 2*9 + 3*11  # 第一行第一列元素
    assert manual_calc == result1[0, 0], "计算结果错误"
    print("验证结果正确！")


if __name__ == "__main__":
    main()