import numpy as np


def main():
    """
    示例1：基础reshape操作
    将一维数组重塑为二维矩阵
    """
    # 创建一个包含12个元素的一维数组
    arr = np.arange(1, 13)
    print(f"原始一维数组: {arr}")
    
    # 使用reshape将其变为3行4列的矩阵
    # 注意：总元素数必须一致（12 = 3 * 4）
    matrix = arr.reshape(3, 4)
    print("重塑为3x4矩阵:")
    print(matrix)
    
    # 验证原数组未被修改
    print(f"原数组形状保持不变: {arr.shape}")


if __name__ == "__main__":
    main()