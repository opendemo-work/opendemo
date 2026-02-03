"""
文件: example2.py
功能: 演示如何将普通 Python 函数转换为自定义 ufunc。
"""

import numpy as np


def custom_power(x, y):
    """
    自定义函数：如果 y 为 0，返回 1；否则返回 x^y
    """
    if y == 0:
        return 1
    else:
        return x ** y


def main():
    # 将普通函数转换为 ufunc
    # 参数说明：
    # - 函数对象
    # - 输入参数个数：2
    # - 输出参数个数：1
    ufunc_custom_power = np.frompyfunc(custom_power, 2, 1)

    # 创建输入数组
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 0, 2, 1, 0])

    # 使用自定义 ufunc 进行运算
    result = ufunc_custom_power(x, y)

    print(f"数组 x: {x}")
    print(f"数组 y: {y}")
    print(f"自定义幂运算结果: {result}")


if __name__ == "__main__":
    main()