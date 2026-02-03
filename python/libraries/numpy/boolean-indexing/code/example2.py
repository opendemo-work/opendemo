import numpy as np


def main():
    """
    示例2：高级布尔索引
    演示在二维数组中组合多个布尔条件进行数据筛选
    """
    # 创建一个4x3的二维数组
    arr_2d = np.arange(1, 13).reshape(4, 3)
    print(f"原始二维数组:\n{arr_2d}")

    # 组合条件：元素大于5 且 为奇数
    # 注意：多个条件需用括号包围，并使用 &（与）或 |（或）连接
    mask = (arr_2d > 5) & (arr_2d % 2 == 1)
    result = arr_2d[mask]
    print(f"所有大于5且为奇数的元素: {result}")

    # 筛选每行最大值大于8的行
    row_max = np.max(arr_2d, axis=1)  # 计算每行的最大值
    row_mask = row_max > 8
    selected_rows = arr_2d[row_mask, :]  # 选择满足条件的整行
    print(f"每行最大值大于8的行:\n{selected_rows}")


if __name__ == "__main__":
    main()