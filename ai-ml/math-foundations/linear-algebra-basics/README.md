<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 线性代数基础

## 🎯 案例概述

这是一个全面展示线性代数在AI/ML中应用的基础示例，涵盖向量运算、矩阵操作、特征值分解、奇异值分解等核心数学概念。

## 📚 学习目标

通过本示例你将掌握：
- 向量的基本运算和几何意义
- 矩阵的运算规则和重要性质
- 特征值分解的原理和应用
- 奇异值分解的概念和用途
- 线性代数在机器学习中的实际应用

## 🔧 核心知识点

### 1. 向量运算
- 向量加法和减法
- 标量乘法
- 点积（内积）和叉积
- 向量模长和单位向量
- 向量夹角和正交性

### 2. 矩阵运算
- 矩阵加法和乘法
- 矩阵转置
- 行列式计算
- 矩阵求逆
- 矩阵的秩

### 3. 特征值分解
- 特征值和特征向量的计算
- 对称矩阵的特征分解
- 特征值分解的几何意义
- 在PCA中的应用

### 4. 奇异值分解
- SVD分解的原理
- 奇异值的物理意义
- 矩阵近似和降维
- 在推荐系统中的应用

## 🚀 运行示例

```bash
# 安装依赖
pip install numpy matplotlib pytest

# 运行主程序
python linear_algebra_basics.py

# 运行测试
python -m pytest test_linear_algebra.py -v
```

## 📖 代码详解

### 主要类结构

```python
class LinearAlgebraBasics:
    def vector_operations(self):      # 向量运算演示
    def matrix_operations(self):      # 矩阵运算演示  
    def eigen_decomposition(self):    # 特征值分解演示
    def singular_value_decomposition(self):  # 奇异值分解演示
    def visualize_vectors(self):      # 向量可视化
    def visualize_eigenvectors(self): # 特征向量可视化
```

### 关键技术点演示

#### 1. 向量运算
```python
# 向量创建和基本运算
v1 = np.array([3, 4])
v2 = np.array([1, 2])

# 向量加法
v_sum = v1 + v2  # [4, 6]

# 点积计算
dot_product = np.dot(v1, v2)  # 3*1 + 4*2 = 11

# 向量模长
norm = np.linalg.norm(v1)  # 5.0
```

#### 2. 矩阵运算
```python
# 矩阵创建和运算
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 矩阵乘法
C = np.dot(A, B)  # [[19, 22], [43, 50]]

# 矩阵行列式
det = np.linalg.det(A)  # -2.0

# 矩阵逆
A_inv = np.linalg.inv(A)  # [[-2, 1], [1.5, -0.5]]
```

#### 3. 特征值分解
```python
# 对称矩阵特征分解
A = np.array([[4, 2], [2, 3]])
eigenvalues, eigenvectors = np.linalg.eig(A)

# 验证 A * v = λ * v
for i in range(len(eigenvalues)):
    Av = np.dot(A, eigenvectors[:, i])
    lambda_v = eigenvalues[i] * eigenvectors[:, i]
    # 误差应该接近0
```

#### 4. 奇异值分解
```python
# SVD分解
A = np.array([[1, 2, 3], [4, 5, 6]])
U, singular_values, Vt = np.linalg.svd(A)

# 矩阵重构
Sigma = np.zeros((2, 3))
np.fill_diagonal(Sigma, singular_values)
A_reconstructed = np.dot(U, np.dot(Sigma, Vt))
# 重构误差应该很小
```

## 🧪 测试覆盖

测试文件 `test_linear_algebra.py` 包含以下测试：

✅ 向量加法测试  
✅ 向量点积测试  
✅ 向量模长测试  
✅ 矩阵乘法测试  
✅ 矩阵行列式测试  
✅ 矩阵逆测试  
✅ 特征值分解测试  
✅ 奇异值分解测试  
✅ 矩阵秩测试  
✅ 正交向量测试  

## 🎯 实际应用场景

### 1. 机器学习中的应用
```python
# PCA降维
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_transformed = pca.fit_transform(X)

# 特征值对应主成分的重要性
explained_variance_ratio = pca.explained_variance_ratio_
```

### 2. 推荐系统中的应用
```python
# 协同过滤中的矩阵分解
U, sigma, Vt = np.linalg.svd(rating_matrix)
# 使用前k个奇异值进行矩阵近似
k = 50
rating_approx = U[:, :k] @ np.diag(sigma[:k]) @ Vt[:k, :]
```

### 3. 计算机视觉中的应用
```python
# 图像压缩
U, s, Vt = np.linalg.svd(image_matrix)
# 保留主要奇异值进行压缩
compressed_image = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
```

## ⚡ 最佳实践建议

### 1. 数值稳定性
- 注意矩阵条件数，避免病态矩阵
- 使用适当的数值精度
- 对于大型矩阵考虑稀疏表示

### 2. 计算效率
- 利用矩阵的特殊结构（对称、稀疏等）
- 选择合适的分解方法
- 避免不必要的矩阵求逆

### 3. 实际应用考虑
- 理解数学概念的几何意义
- 注意数值误差的累积
- 根据具体问题选择合适的线性代数工具

## 🔍 常见问题和解决方案

### 1. 矩阵不可逆
```python
# 问题：奇异矩阵无法求逆
A = np.array([[1, 2], [2, 4]])  # 秩亏矩阵
try:
    A_inv = np.linalg.inv(A)
except np.linalg.LinAlgError:
    # 解决：使用伪逆或正则化
    A_pinv = np.linalg.pinv(A)
```

### 2. 数值精度问题
```python
# 问题：浮点数计算误差
A = np.array([[1, 1], [1, 1+1e-16]])
eigenvals = np.linalg.eigvals(A)
# 可能得到微小的复数部分

# 解决：使用适当的容差
eigenvals = np.real_if_close(eigenvals, tol=1e-10)
```

## 📚 扩展学习资源

### 官方文档
- [NumPy线性代数文档](https://numpy.org/doc/stable/reference/routines.linalg.html)
- [SciPy线性代数模块](https://docs.scipy.org/doc/scipy/reference/linalg.html)

### 推荐书籍
- 《线性代数及其应用》- Gilbert Strang
- 《矩阵分析》- Roger A. Horn
- 《机器学习中的数学》- 雷明

### 相关课程
- MIT线性代数公开课
- Stanford机器学习课程中的数学基础

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含完整的线性代数基础演示

---
**注意**: 线性代数是AI/ML的数学基础，深入理解这些概念对掌握机器学习算法至关重要。
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 AI/ML 核心概念。

### 2. 适用场景

- 场景 1：学术研究
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
python code/main.py
```
