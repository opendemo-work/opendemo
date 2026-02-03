import numpy as np


def main():
    """
    演示NumPy数组的拼接操作
    包括concatenate和stack的使用
    """
    # 创建两个一维数组
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    
    print(f"原始数组1: {arr1}")
    print(f"原始数组2: {arr2}")
    
    # 水平拼接（沿axis=0，默认）
    concatenated_horizontal = np.concatenate((arr1, arr2))
    print(f"水平拼接结果: {concatenated_horizontal}")
    
    # 垂直拼接（创建二维数组）
    concatenated_vertical = np.concatenate((arr1.reshape(1, -1), arr2.reshape(1, -1)), axis=0)
    print(f"垂直拼接结果: {concatenated_vertical}")
    
    # 使用stack在新轴上堆叠
    stacked = np.stack((arr1, arr2))
    print(f"堆叠结果: {stacked}")
    
    # 创建两个二维数组进行更复杂的拼接
    matrix1 = np.array([[1, 2], [3, 4]])
    matrix2 = np.array([[5, 6], [7, 8]])
    
    print(f"\n矩阵1:\n{matrix1}")
    print(f"矩阵2:\n{matrix2}")
    
    # 沿行方向拼接（垂直拼接）
    vertical_concat = np.concatenate((matrix1, matrix2), axis=0)
    print(f"垂直拼接矩阵:\n{vertical_concat}")
    
    # 沿列方向拼接（水平拼接）
    horizontal_concat = np.concatenate((matrix1, matrix2), axis=1)
    print(f"水平拼接矩阵:\n{horizontal_concat}")


if __name__ == "__main__":
    main()