import numpy as np


def main():
    """
    示例2：二维数组与一维数组的广播
    
    演示如何对矩阵的每一列或每一行统一操作
    """
    # 创建一个3x3的二维数组
    matrix = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]])
    
    # 创建一个列向量（将被广播到每一列）
    col_vector = np.array([10, 20, 30])  # 形状: (3,)
    
    # 重塑为列向量 (3,1)，以便按列广播
    col_vector_reshaped = col_vector.reshape(-1, 1)  # 形状变为 (3,1)
    
    # 对每一列加上对应的列向量值
    result_col = matrix + col_vector_reshaped
    
    # 创建一个行向量（将被广播到每一行）
    row_vector = np.array([100, 200, 300])  # 形状: (3,)
    
    # 对每一行加上对应的行向量值
    # 注意：由于row_vector最后一个维度是3，与matrix的列数一致，可直接广播
    result_row = matrix + row_vector
    
    # 输出结果
    print(f"二维数组:\n {matrix}")
    print(f"列向量: {col_vector}")
    print(f"按列相加结果:\n {result_col}")
    print(f"行向量: {row_vector}")
    print(f"按行相加结果:\n {result_row}")


if __name__ == "__main__":
    main()