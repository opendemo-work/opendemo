import numpy as np


def main():
    """
    演示NumPy数组的分割操作
    展示如何使用split函数分割数组
    """
    # 创建一个一维数组用于分割
    arr = np.array([1, 2, 3, 4, 5, 6])
    print(f"原始数组: {arr}")
    
    # 将数组平均分割为3部分
    split_arrays = np.split(arr, 3)
    print(f"分割后数组列表: {split_arrays}")
    
    # 创建一个更大的数组
    large_arr = np.arange(1, 13).reshape(4, 3)
    print(f"\n原始大数组:\n{large_arr}")
    
    # 沿轴0（行）分割为两部分
    split_by_rows = np.split(large_arr, 2, axis=0)
    print("按行分割结果:")
    for i, sub_array in enumerate(split_by_rows):
        print(f"  第{i+1}部分:\n{sub_array}\n")
    
    # 沿轴1（列）分割为三部分
    split_by_cols = np.split(large_arr, 3, axis=1)
    print("按列分割结果:")
    for i, sub_array in enumerate(split_by_cols):
        print(f"  第{i+1}部分:\n{sub_array}\n")
    
    # 使用指定索引位置进行分割
    custom_split = np.split(arr, [2, 4])  # 在索引2和4处分割
    print(f"自定义位置分割: {custom_split}")


if __name__ == "__main__":
    main()