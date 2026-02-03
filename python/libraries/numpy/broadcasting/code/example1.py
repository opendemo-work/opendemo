import numpy as np


def main():
    """
    示例1：标量与向量的广播运算
    
    演示标量如何被自动广播到向量的每一个元素上
    """
    # 创建一个一维向量
    vector = np.array([1, 2, 3, 4])
    
    # 定义一个标量
    scalar = 10
    
    # 广播加法：标量被应用到每个元素
    result_add = vector + scalar
    
    # 广播乘法
    result_mul = vector * scalar
    
    # 输出结果
    print(f"原始向量: {vector}")
    print(f"标量: {scalar}")
    print(f"广播加法结果: {result_add}")
    print(f"广播乘法结果: {result_mul}")


if __name__ == "__main__":
    main()