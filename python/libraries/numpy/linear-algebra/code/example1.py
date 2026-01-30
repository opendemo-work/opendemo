import numpy as np


def main():
    """
    演示矩阵的基本线性代数运算
    包括：创建矩阵、加法、乘法、转置、求逆
    """
    # 创建两个2x2矩阵
    A = np.array([[1, 2],
                  [3, 4]])
    
    B = np.array([[5, 6],
                  [7, 8]])
    
    print("=== 矩阵基本运算 ===")
    print(f"矩阵A:\n{A}\n")
    print(f"矩阵B:\n{B}\n")
    
    # 矩阵加法
    C = A + B
    print(f"A + B =\n{C}\n")
    
    # 矩阵乘法（点积）
    D = np.dot(A, B)
    print(f"A × B =\n{D}\n")
    
    # 矩阵转置
    A_transpose = A.T
    print(f"A的转置:\n{A_transpose}\n")
    
    # 矩阵求逆（需确保矩阵可逆）
    try:
        A_inv = np.linalg.inv(A)
        print(f"A的逆矩阵:\n{A_inv}\n")
        
        # 验证逆矩阵：A × A⁻¹ 应等于单位矩阵
        I = np.dot(A, A_inv)
        print(f"验证 A × A⁻¹ (应接近单位矩阵):\n{I}\n")
    except np.linalg.LinAlgError:
        print("矩阵A不可逆！\n")


if __name__ == "__main__":
    main()