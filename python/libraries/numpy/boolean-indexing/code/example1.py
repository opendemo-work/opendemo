import numpy as np


def main():
    """
    示例1：基础布尔索引
    演示如何使用布尔条件从一维数组中筛选数据
    """
    # 创建一个一维整数数组
    arr = np.arange(1, 11)
    print(f"原始数组: {arr}")

    # 使用布尔索引筛选偶数
    # arr % 2 == 0 生成布尔数组，如 [False True False True ...]
    mask_even = arr % 2 == 0
    even_numbers = arr[mask_even]
    print(f"偶数元素: {even_numbers}")

    # 筛选大于5的元素
    mask_gt_5 = arr > 5
    greater_than_5 = arr[mask_gt_5]
    print(f"大于5的元素: {greater_than_5}")


if __name__ == "__main__":
    main()