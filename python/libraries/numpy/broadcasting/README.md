# NumPy Broadcasting 实战演示

## 简介
本示例演示了NumPy中**广播（Broadcasting）**的核心概念。广播是NumPy实现高效数组运算的关键机制，它允许不同形状的数组进行算术运算，而无需显式复制数据。

我们将通过两个具体场景展示广播的实际应用：
1. 向量与标量的运算
2. 二维数组与一维数组的列/行操作

---

## 学习目标
- 理解什么是广播以及为什么需要它
- 掌握广播的两条基本规则
- 能够预测广播操作的结果形状
- 学会在实际数据处理中使用广播提升效率

---

## 环境要求
- Python 3.8 或更高版本
- 操作系统：Windows / Linux / macOS（跨平台兼容）

---

## 安装依赖
打开终端或命令提示符，执行以下命令：

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

---

## 文件说明
- `code/example1.py`: 标量与向量的广播运算示例
- `code/example2.py`: 二维数组与一维数组的广播应用

---

## 逐步实操指南

### 第一步：运行第一个示例
```bash
python code/example1.py
```

**预期输出**：
```
原始向量: [1 2 3 4]
标量: 10
广播加法结果: [11 12 13 14]
广播乘法结果: [10 20 30 40]
```

### 第二步：运行第二个示例
```bash
python code/example2.py
```

**预期输出**：
```
二维数组:\n [[1 2 3]\n  [4 5 6]\n  [7 8 9]]
列向量: [10 20 30]
按列相加结果:\n [[11 12 13]\n  [24 25 26]\n  [37 38 39]]
行向量: [100 200 300]
按行相加结果:\n [[101 202 303]\n  [104 205 306]\n  [107 208 309]]
```

---

## 代码解析

### example1.py 关键点
```python
result = vector + scalar
```
尽管 `vector` 是 (4,) 形状，`scalar` 是标量，NumPy 自动将标量“广播”到每个元素上，等价于 `[scalar, scalar, scalar, scalar]`。

### example2.py 关键点
```python
result_col = matrix + col_vector.reshape(-1, 1)
```
将一维列向量 reshape 为 (3,1)，使其能与 (3,3) 矩阵按列广播。这是处理列统计量（如标准化）的常见模式。

```python
result_row = matrix + row_vector
```
一维行向量 (3,) 可直接与 (3,3) 矩阵按行广播，因为其最后一个维度匹配。

---

## 预期输出示例
见“逐步实操指南”部分的输出样例。

---

## 常见问题解答

**Q: 什么情况下会触发 ValueError: operands could not be broadcast together?**
A: 当两个数组的对应维度既不相等，也没有一个是1时。例如 (3,4) 和 (2,4) 无法广播。

**Q: 广播会占用额外内存吗？**
A: 不会！广播是虚拟扩展，不会复制数据，因此非常高效。

**Q: 如何查看广播后的形状？**
A: 使用 `np.broadcast_arrays(arr1, arr2)` 查看实际广播后的数组形状。

---

## 扩展学习建议
- 尝试修改 `example2.py` 中的数组形状，观察哪些组合可以广播
- 使用广播实现数据的Z-score标准化：`(x - mean) / std`
- 阅读官方文档：https://numpy.org/doc/stable/user/basics.broadcasting.html