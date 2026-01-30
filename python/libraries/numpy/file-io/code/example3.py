"""
文件名: example3.py
功能: 使用NumPy保存和加载数值数组
使用场景: 科学计算、机器学习数据存储等
"""

import numpy as np

# 创建一个简单的二维数值数组
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# 使用savetxt保存数组到文本文件
np.savetxt('array_data.txt', arr, fmt='%d')

print("数值数组已保存至 array_data.txt")

# 使用loadtxt重新加载数组
loaded = np.loadtxt('array_data.txt')

print("加载的数组：")
print(loaded)

# 验证原始数组与加载数组是否一致
assert np.array_equal(arr, loaded), "加载的数据与原始数据不一致！"
print("数据一致性验证通过。")