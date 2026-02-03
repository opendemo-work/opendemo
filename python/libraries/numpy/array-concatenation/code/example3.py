import numpy as np

# 示例3：不可广播的情况演示
# 创建两个不兼容广播规则的数组
a = np.array([[1, 2, 3],        # shape: (2,3)
              [4, 5, 6]])

b = np.array([10, 20])          # shape: (2,)

print("\n示例3：不可广播情况")
try:
    # 尝试相加 —— 会出错，因为末尾维度3 != 2，且都不是1
    result = a + b
except ValueError as e:
    print(f"错误：{e}")
    print("提示：数组形状 (2,3) 和 (2,) 不满足广播规则。\n      广播要求从右开始的每个维度要么相等，要么其中一个为1。")