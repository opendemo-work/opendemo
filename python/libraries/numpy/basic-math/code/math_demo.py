"""NumPy 基础数学运算示例"""
import numpy as np

def arithmetic_operations():
    """基础算术运算"""
    print("=" * 50)
    print("基础算术运算")
    print("=" * 50)
    a = np.array([1, 2, 3, 4])
    b = np.array([5, 6, 7, 8])
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")
    print(f"a ** 2 = {a ** 2}")
    print()

def scalar_operations():
    """标量运算"""
    print("=" * 50)
    print("标量运算")
    print("=" * 50)
    arr = np.array([1, 2, 3, 4, 5])
    print(f"数组: {arr}")
    print(f"arr + 10 = {arr + 10}")
    print(f"arr * 2 = {arr * 2}")
    print()

if __name__ == "__main__":
    print("\nNumPy 基础数学运算演示\n")
    arithmetic_operations()
    scalar_operations()
    print("演示完成！\n")
