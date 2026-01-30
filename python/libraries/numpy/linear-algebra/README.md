# 线性代数Python实战演示

## 简介
本项目通过三个具体的Python脚本，展示如何使用NumPy库进行常见的线性代数运算，包括矩阵的基本操作、求解线性方程组以及矩阵分解。适合初学者理解和掌握线性代数在编程中的实际应用。

## 学习目标
- 掌握使用NumPy进行矩阵和向量的基本运算
- 理解线性方程组的数值求解方法
- 了解特征值分解和奇异值分解的应用场景
- 提升将数学概念转化为代码的能力

## 环境要求
- Python 3.7 或更高版本
- 支持Windows、macOS和Linux系统

## 安装依赖的详细步骤

1. 确保已安装Python（建议使用Python 3.8+）
   ```bash
   python --version
   ```

2. 创建虚拟环境（推荐）
   ```bash
   python -m venv la_env
   ```

3. 激活虚拟环境：
   - Windows:
     ```bash
     la_env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source la_env/bin/activate
     ```

4. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/matrix_operations.py`: 演示矩阵加减乘除、转置、逆等基本操作
- `code/solve_linear_system.py`: 使用NumPy求解线性方程组Ax = b
- `code/matrix_decomposition.py`: 展示特征值分解和奇异值分解
- `requirements.txt`: 项目依赖声明文件

## 逐步实操指南

### 步骤1：运行矩阵基本操作示例
```bash
python code/matrix_operations.py
```
**预期输出**：
- 显示两个矩阵及其加法、乘法结果
- 输出矩阵的转置和逆矩阵

### 步骤2：求解线性方程组
```bash
python code/solve_linear_system.py
```
**预期输出**：
- 输出系数矩阵A、常数向量b和解向量x
- 验证Ax ≈ b的结果

### 步骤3：执行矩阵分解
```bash
python code/matrix_decomposition.py
```
**预期输出**：
- 特征值和特征向量
- 奇异值分解的U, Σ, V^T矩阵

## 代码解析

### matrix_operations.py
```python
np.dot(A, B)
```
使用`np.dot()`进行矩阵乘法，这是线性代数中最核心的操作之一。

```python
np.linalg.inv(A)
```
调用线性代数模块求矩阵的逆，前提是矩阵必须是可逆的。

### solve_linear_system.py
```python
x = np.linalg.solve(A, b)
```
高效求解形如Ax = b的线性方程组，比手动求逆更稳定、更快。

### matrix_decomposition.py
```python
eigenvals, eigenvecs = np.linalg.eig(A)
```
计算方阵的特征值和对应的特征向量，用于主成分分析等场景。

```python
U, S, Vt = np.linalg.svd(A)
```
执行奇异值分解，广泛应用于数据压缩和推荐系统中。

## 预期输出示例
```
=== 矩阵基本运算 ===
矩阵A:\n[[1 2]\n [3 4]]
... ...
```

## 常见问题解答

**Q: 运行时报错 'ModuleNotFoundError: No module named 'numpy''？**
A: 请确保已正确安装依赖：`pip install -r requirements.txt`

**Q: 为什么不用A**(-1)来求逆矩阵？**
A: 应使用`np.linalg.inv(A)`，因为`**`表示元素幂而非矩阵幂。

**Q: 如何判断矩阵是否可逆？**
A: 可先检查行列式是否为零：`np.linalg.det(A) != 0`

## 扩展学习建议
- 学习SciPy中的高级线性代数功能
- 尝试用线性代数实现最小二乘法拟合
- 探索PCA（主成分分析）的实现原理
- 阅读《线性代数应该这样学》配合代码实践