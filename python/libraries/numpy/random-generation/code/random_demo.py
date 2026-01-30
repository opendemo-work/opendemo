"""NumPy 随机数生成示例"""
import numpy as np

def random_uniform():
    """均匀分布随机数"""
    print("=" * 50)
    print("均匀分布随机数")
    print("=" * 50)
    # 0到1之间的随机数
    rand_arr = np.random.rand(5)
    print(f"rand(5): {rand_arr}")
    
    # 指定范围的随机整数
    rand_int = np.random.randint(1, 100, size=10)
    print(f"randint(1, 100, size=10): {rand_int}")
    print()

def random_normal():
    """正态分布随机数"""
    print("=" * 50)
    print("正态分布随机数")
    print("=" * 50)
    # 标准正态分布
    normal_arr = np.random.randn(5)
    print(f"randn(5): {normal_arr}")
    
    # 指定均值和标准差的正态分布
    normal_custom = np.random.normal(loc=10, scale=2, size=5)
    print(f"normal(loc=10, scale=2, size=5): {normal_custom}")
    print()

def random_choice():
    """随机选择"""
    print("=" * 50)
    print("随机选择")
    print("=" * 50)
    arr = np.array([1, 2, 3, 4, 5])
    choice = np.random.choice(arr, size=3)
    print(f"从 {arr} 中随机选择3个: {choice}")
    print()

if __name__ == "__main__":
    print("\nNumPy 随机数生成演示\n")
    np.random.seed(42)  # 设置随机种子以获得可重复的结果
    random_uniform()
    random_normal()
    random_choice()
    print("演示完成！\n")
