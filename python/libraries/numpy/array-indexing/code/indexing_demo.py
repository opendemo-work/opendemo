"""NumPy 数组索引与切片示例"""
import numpy as np

def indexing_demo():
    """演示数组索引"""
    print("=" * 50)
    print("数组索引")
    print("=" * 50)
    arr = np.array([10, 20, 30, 40, 50])
    print(f"数组: {arr}")
    print(f"arr[0] = {arr[0]}")  # 第一个元素
    print(f"arr[-1] = {arr[-1]}")  # 最后一个元素
    print(f"arr[1:4] = {arr[1:4]}")  # 切片
    print()

def multi_dim_indexing():
    """多维数组索引"""
    print("=" * 50)
    print("多维数组索引")
    print("=" * 50)
    arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"二维数组:\n{arr2d}")
    print(f"arr2d[0, 0] = {arr2d[0, 0]}")  # 第一行第一列
    print(f"arr2d[1, :] = {arr2d[1, :]}")  # 第二行所有列
    print(f"arr2d[:, 1] = {arr2d[:, 1]}")  # 所有行的第二列
    print()

def boolean_indexing():
    """布尔索引"""
    print("=" * 50)
    print("布尔索引")
    print("=" * 50)
    arr = np.array([1, 2, 3, 4, 5, 6])
    mask = arr > 3
    print(f"数组: {arr}")
    print(f"大于3的元素: {arr[mask]}")
    print()

if __name__ == "__main__":
    print("\nNumPy 数组索引与切片演示\n")
    indexing_demo()
    multi_dim_indexing()
    boolean_indexing()
    print("演示完成！\n")
