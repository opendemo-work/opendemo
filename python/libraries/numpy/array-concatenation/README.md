# NumPy数组拼接与分割操作演示

## 简介
本演示项目展示了如何使用NumPy库中的`concatenate`、`stack`和`split`函数对数组进行拼接和分割操作。通过具体的代码示例，帮助初学者理解这些常用操作的用法和区别。

## 学习目标
- 掌握NumPy中数组的横向和纵向拼接方法
- 理解`stack`与`concatenate`的区别
- 学会使用`split`函数对数组进行分割
- 能够在实际数据处理中灵活运用这些操作

## 环境要求
- Python 3.7 或更高版本
- 操作系统：Windows、Linux、macOS 均可

## 安装依赖的详细步骤

1. 打开终端（命令提示符或终端应用程序）
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   ```
3. 激活虚拟环境：
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
4. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/example1.py`: 演示数组的拼接操作（concatenate 和 stack）
- `code/example2.py`: 演示数组的分割操作（split）
- `requirements.txt`: 项目依赖声明文件
- `README.md`: 本说明文档

## 逐步实操指南

1. 运行拼接示例：
   ```bash
   python code/example1.py
   ```
   **预期输出**：
   各种拼接操作的结果打印，包括水平拼接、垂直拼接和堆叠。

2. 运行分割示例：
   ```bash
   python code/example2.py
   ```
   **预期输出**：
   分割后的子数组被打印出来，展示如何将一个大数组拆分为多个小数组。

## 代码解析

### example1.py 关键代码段
```python
np.concatenate((arr1, arr2), axis=0)  # 沿轴0（垂直）拼接
np.stack((arr1, arr2))                # 在新轴上堆叠数组
```
- `concatenate`：在现有维度上连接数组
- `stack`：创建一个新的维度来堆叠数组

### example2.py 关键代码段
```python
np.split(arr, 3)  # 将数组平均分为3份
```
- `split`：按指定数量或位置分割数组

## 预期输出示例
```
原始数组1: [1 2 3]
原始数组2: [4 5 6]
水平拼接结果: [1 2 3 4 5 6]
垂直拼接结果: [[1 2 3] [4 5 6]]
堆叠结果: [[[1 2 3] [4 5 6]]]

分割后数组列表: [array([1, 2]), array([3, 4]), array([5, 6])]
```

## 常见问题解答

**Q: concatenate 和 stack 有什么区别？**
A: `concatenate` 在已有维度上连接数组，而 `stack` 会创建一个新的维度来堆叠数组。

**Q: split 分割时数组长度必须能被整除吗？**
A: 使用 `np.split` 时是的；如果不能整除，可以使用 `np.array_split`，它会自动处理不均匀分割。

**Q: 如何在列方向上拼接两个二维数组？**
A: 使用 `axis=1` 参数：`np.concatenate((a, b), axis=1)`。

## 扩展学习建议
- 学习 `hstack`, `vstack`, `dstack` 的便捷用法
- 探索 `tile` 和 `repeat` 函数进行数组复制
- 实践在图像处理或多维数据中应用这些操作