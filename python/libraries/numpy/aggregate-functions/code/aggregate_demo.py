"""NumPy 聚合函数示例"""
import numpy as np

def basic_aggregates():
    """基础聚合函数"""
    print("=" * 50)
    print("基础聚合函数")
    print("=" * 50)
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"数组: {arr}")
    print(f"总和 sum(): {arr.sum()}")
    print(f"平均值 mean(): {arr.mean()}")
    print(f"最小值 min(): {arr.min()}")
    print(f"最大值 max(): {arr.max()}")
    print(f"标准差 std(): {arr.std():.2f}")
    print()

def axis_aggregates():
    """按轴聚合"""
    print("=" * 50)
    print("按轴聚合")
    print("=" * 50)
    arr2d = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"二维数组:\n{arr2d}")
    print(f"按列求和 sum(axis=0): {arr2d.sum(axis=0)}")
    print(f"按行求和 sum(axis=1): {arr2d.sum(axis=1)}")
    print()

if __name__ == "__main__":
    print("\nNumPy 聚合函数演示\n")
    basic_aggregates()
    axis_aggregates()
    print("演示完成！\n")
