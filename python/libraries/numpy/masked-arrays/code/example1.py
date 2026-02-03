import numpy as np
import numpy.ma as ma


def main():
    """
    示例1：基础掩码数组的创建与操作
    """
    # 创建一个普通数组，其中第三个元素是无效的
    data = np.array([1, 2, 3, 4, 5])

    # 定义掩码：True 表示该位置的数据应被屏蔽（无效）
    mask = [False, False, True, False, False]

    # 创建掩码数组
    masked_array = ma.array(data, mask=mask)

    print(f"原始数组: {masked_array}")
    print(f"掩码: {masked_array.mask}")

    # 计算均值时，被屏蔽的值会被自动忽略
    mean_value = masked_array.mean()
    print(f"均值（忽略掩码）: {mean_value}")

    # 使用 filled() 方法填充被屏蔽的值（例如替换为0）
    filled_array = masked_array.filled(0)
    print(f"填充后的数组: {filled_array}")


if __name__ == "__main__":
    main()