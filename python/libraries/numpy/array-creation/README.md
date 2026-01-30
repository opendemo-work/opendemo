# NumPy 数组创建

这个 demo 演示了使用 NumPy 创建数组的多种方法。

## 功能说明

1. **从列表创建数组**：使用 `np.array()` 从 Python 列表创建一维和二维数组
2. **使用 zeros 和 ones**：创建全零或全一数组
3. **等差数列**：使用 `arange()` 和 `linspace()` 创建等差数列
4. **单位矩阵和对角矩阵**：使用 `eye()` 和 `diag()` 创建特殊矩阵
5. **empty 和 full**：创建未初始化数组和填充特定值的数组

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行示例
python code/array_creation_demo.py
```

## 示例输出

```
==================================================
NumPy 数组创建方法演示
==================================================

==================================================
1. 从列表创建数组
==================================================
一维数组: [1 2 3 4 5]
形状: (5,), 维度: 1, 类型: int32

二维数组:
[[1 2 3]
 [4 5 6]]
形状: (2, 3), 维度: 2
```

## 核心概念

### np.array()
从 Python 列表或元组创建数组，是最基础的创建方法。

### np.zeros() / np.ones()
创建指定形状的全零或全一数组，常用于初始化。

### np.arange() vs np.linspace()
- `arange(start, stop, step)`：类似 Python range，不包含 stop
- `linspace(start, stop, num)`：生成指定数量的等间距数值，包含 stop

### np.eye() / np.diag()
创建单位矩阵和对角矩阵，在线性代数中常用。

## 相关功能

- [array-indexing](../array-indexing/): 数组索引与切片
- [array-attributes](../array-attributes/): 数组属性

## 参考文档

- [NumPy Array Creation](https://numpy.org/doc/stable/user/basics.creation.html)
