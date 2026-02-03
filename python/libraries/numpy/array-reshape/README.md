# 数组形状操作reshape演示

## 简介
本示例展示了如何使用NumPy库中的`reshape`方法对数组进行形状变换。`reshape`是数据处理和科学计算中常用的操作，用于改变数组的维度而不改变其数据。

## 学习目标
- 理解`reshape`的基本概念
- 掌握一维到多维数组的转换方法
- 学会使用`-1`自动推断维度
- 了解`reshape`在实际场景中的应用

## 环境要求
- Python 3.7 或更高版本
- 支持Windows、Linux和macOS系统

## 安装依赖的详细步骤

1. 打开终端（命令提示符或PowerShell）
2. 运行以下命令安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/example1.py`: 基础reshape操作：将一维数组转为二维
- `code/example2.py`: 高维数组reshape及自动维度推断
- `code/example3.py`: 实际应用场景：图像数据预处理模拟
- `requirements.txt`: 项目依赖声明文件

## 逐步实操指南

### 步骤1：安装依赖
```bash
pip install -r requirements.txt
```
**预期输出**：
```
Collecting numpy>=1.21.0
  Downloading numpy-...\nInstalling collected packages: numpy
Successfully installed numpy-...
```

### 步骤2：运行第一个示例
```bash
python code/example1.py
```
**预期输出**：
```
原始一维数组: [ 1  2  3  4  5  6  7  8  9 10 11 12]
重塑为3x4矩阵:\n[[ 1  2  3  4]\n [ 5  6  7  8]\n [ 9 10 11 12]]
```

### 步骤3：运行第二个示例
```bash
python code/example2.py
```
**预期输出**：
```
原始3D数组形状: (2, 3, 2)
展平为一维数组: [ 1  2  3  4  5  6  7  8  9 10 11 12]
自动推断行数(-1, 4):\n[[ 1  2  3  4]\n [ 5  6  7  8]\n [ 9 10 11 12]]
```

### 步骤4：运行第三个示例
```bash
python code/example3.py
```
**预期输出**：
```
原始图像数据形状 (高度, 宽度, 通道): (28, 28, 3)
转换为批量输入形状 (批量大小, 特征数): (1, 2352)
模型输入准备完成。
```

## 代码解析

### example1.py 关键点
```python
arr.reshape(3, 4)
```
将长度为12的一维数组变为3行4列的二维数组。总元素数必须匹配。

### example2.py 关键点
```python
arr.reshape(-1)
```
`-1`表示该维度由系统自动计算，常用于展平操作。

### example3.py 关键点
```python
image_data.reshape(1, -1)
```
将三维图像数据展平并添加批量维度，符合深度学习模型输入要求。

## 预期输出示例
参见“逐步实操指南”部分的输出示例。

## 常见问题解答

**Q: reshape时出现'cannot reshape array'错误怎么办？**
A: 检查原数组元素总数是否等于新形状的乘积。例如12个元素不能变成3x5=15个位置。

**Q: 什么是`-1`的作用？**
A: `-1`让NumPy自动推断该维度的大小，只能在一个轴上使用。

**Q: reshape会修改原数组吗？**
A: 不会，它返回新数组，原数组保持不变（除非使用inplace操作）。

## 扩展学习建议
- 学习`flatten()`与`ravel()`的区别
- 探索`transpose()`和`swapaxes()`进行维度重排
- 学习在深度学习框架（如TensorFlow/PyTorch）中使用reshape
- 阅读NumPy官方文档中关于数组操作的部分