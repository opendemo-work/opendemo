# 矩阵乘法Python实战演示

## 简介
本演示项目通过两个实际场景展示如何在Python中使用NumPy进行矩阵乘法运算。涵盖基础矩阵相乘和图像变换中的矩阵应用，帮助初学者理解线性代数在编程中的实际用途。

## 学习目标
- 理解矩阵乘法的基本概念和规则
- 掌握使用NumPy进行矩阵乘法的两种方法（`dot()` 和 `@` 操作符）
- 了解矩阵乘法在几何变换中的应用
- 学会创建和操作二维数组

## 环境要求
- Python 3.7 或更高版本
- 支持Windows、macOS和Linux系统

## 安装依赖
1. 确保已安装Python（推荐使用Python 3.8+）
2. 打开终端或命令提示符
3. 运行以下命令安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/basic_matrix_multiplication.py`: 基础矩阵乘法示例
- `code/matrix_transformation.py`: 矩阵在坐标变换中的应用示例
- `requirements.txt`: 项目依赖声明文件
- `README.md`: 本说明文档

## 逐步实操指南

### 步骤1: 克隆或创建项目目录
```bash
mkdir matrix-demo
cd matrix-demo
# 将本项目所有文件复制到此目录
```

### 步骤2: 安装依赖
```bash
pip install -r requirements.txt
```
**预期输出**: 
```
Collecting numpy>=1.21.0
  Downloading numpy-1.xx.x-...\nInstalling collected packages: numpy
Successfully installed numpy-1.xx.x
```

### 步骤3: 运行基础矩阵乘法示例
```bash
python code/basic_matrix_multiplication.py
```
**预期输出**:
```
矩阵 A:
[[1 2 3]
 [4 5 6]]
矩阵 B:
[[7 8]
 [9 10]
 [11 12]]
A 与 B 的乘积:
[[ 58  64]
 [139 154]]
验证结果正确！
```

### 步骤4: 运行变换矩阵示例
```bash
python code/matrix_transformation.py
```
**预期输出**:
```
原始坐标点:
[[0 0]
 [1 0]
 [1 1]
 [0 1]]
旋转矩阵:
[[ 0.70710678 -0.70710678]
 [ 0.70710678  0.70710678]]
旋转后的坐标:
[[ 0.          0.        ]
 [ 0.70710678  0.70710678]
 [ 0.          1.41421356]
 [-0.70710678  0.70710678]]
```

## 代码解析

### basic_matrix_multiplication.py 关键代码段
```python
A @ B  # 使用@操作符进行矩阵乘法，等价于np.dot(A, B)
```
这是Python中进行矩阵乘法的标准方式，要求A的列数等于B的行数。

### matrix_transformation.py 关键概念
使用旋转矩阵 [[cosθ, -sinθ], [sinθ, cosθ]] 对二维坐标进行旋转变换，这是计算机图形学中的基础技术。

## 预期输出示例
参见"逐步实操指南"部分的预期输出。

## 常见问题解答

**Q: 运行时提示 'numpy not found' 怎么办？**
A: 请确保已运行 `pip install -r requirements.txt`，并确认使用的Python环境是否正确。

**Q: 为什么矩阵乘法不能使用 * 操作符？**
A: 在NumPy中，* 表示逐元素相乘，而 @ 或 dot() 才表示矩阵乘法（线性代数意义上的乘法）。

**Q: 如何验证矩阵乘法结果是否正确？**
A: 可以手动计算前几个元素，例如第一行第一列元素 = 1×7 + 2×9 + 3×11 = 58。

## 扩展学习建议
- 学习更多NumPy数组操作
- 探索scikit-image库中的图像变换
- 研究机器学习中矩阵运算的应用
- 学习TensorFlow/PyTorch中的张量运算