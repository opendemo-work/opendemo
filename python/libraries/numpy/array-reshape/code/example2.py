import numpy as np


def main():
    """
    示例2：高维数组reshape与自动维度推断
    展示更复杂的形状变换和-1的使用
    """
    # 创建一个2x3x2的三维数组
    arr = np.arange(1, 13).reshape(2, 3, 2)
    print(f"原始3D数组形状: {arr.shape}")
    print(f"数组内容:\n{arr}")
    
    # 展平为一维数组（两种写法等价）
    flat = arr.reshape(-1)  # 推荐写法
    # flat = arr.reshape(12) # 显式指定
    print(f"展平为一维数组: {flat}")
    
    # 自动推断行数，指定每行4个元素
    auto_reshape = arr.reshape(-1, 4)
    print("自动推断行数(-1, 4):")
    print(auto_reshape)
    
    # 尝试无效reshape会抛出异常
    try:
        arr.reshape(5, 3)  # 15 ≠ 12，会失败
    except ValueError as e:
        print(f"错误示例: {e}")


if __name__ == "__main__":
    main()