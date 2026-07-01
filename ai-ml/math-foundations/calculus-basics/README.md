<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 微积分基础

## 🎯 案例概述

这是一个全面展示微积分在AI/ML中应用的基础示例，涵盖导数、偏导数、梯度、积分、链式法则等核心数学概念。

## 📚 学习目标

通过本示例你将掌握：
- 导数的几何意义和计算方法
- 偏导数和梯度的概念与应用
- 梯度下降算法的原理和实现
- 数值积分的各种方法
- 链式法则在神经网络中的应用

## 🔧 核心知识点

### 1. 导数概念
- 导数的几何意义（切线斜率）
- 基本求导法则
- 高阶导数
- 导数在优化中的应用

### 2. 偏导数和梯度
- 多元函数的偏导数
- 梯度向量的计算
- 梯度的几何意义
- 方向导数

### 3. 梯度下降
- 梯度下降算法原理
- 学习率的选择
- 收敛性分析
- 优化算法变种

### 4. 积分方法
- 定积分的几何意义
- 数值积分方法（梯形法则、Simpson法则）
- Monte Carlo积分
- 积分在概率中的应用

### 5. 链式法则
- 复合函数求导
- 反向传播算法基础
- 自动微分原理

## 🚀 运行示例

```bash
# 安装依赖
pip install numpy matplotlib scipy pytest

# 运行主程序
python calculus_basics.py

# 运行测试
python -m pytest test_calculus.py -v
```

## 📖 代码详解

### 主要类结构

```python
class CalculusBasics:
    def derivative_concept(self):         # 导数概念演示
    def partial_derivatives(self):        # 偏导数演示
    def gradient_descent_demo(self):      # 梯度下降演示
    def numerical_integration(self):      # 数值积分演示
    def chain_rule_demo(self):            # 链式法则演示
```

### 关键技术点演示

#### 1. 导数计算
```python
# 函数 f(x) = x²
def f(x):
    return x**2

# 导数 f'(x) = 2x
def f_prime(x):
    return 2*x

# 在 x=2 处的导数
derivative_at_2 = f_prime(2)  # 4
```

#### 2. 偏导数和梯度
```python
# 二元函数 f(x,y) = x² + y²
def f(x, y):
    return x**2 + y**2

# 偏导数
def df_dx(x, y):
    return 2*x

def df_dy(x, y):
    return 2*y

# 梯度向量
gradient = np.array([df_dx(1, 2), df_dy(1, 2)])  # [2, 4]
```

#### 3. 梯度下降实现
```python
# 损失函数
def loss_function(x, y):
    return (x - 3)**2 + (y - 2)**2

# 梯度
def gradient(x, y):
    return np.array([2*(x - 3), 2*(y - 2)])

# 梯度下降
point = np.array([0.0, 0.0])
learning_rate = 0.1
for _ in range(100):
    grad = gradient(point[0], point[1])
    point = point - learning_rate * grad
```

#### 4. 数值积分
```python
# 梯形法则
x = np.linspace(0, 3, 1000)
y = x**2
integral = np.trapz(y, x)  # 约等于 9

# Scipy积分
from scipy import integrate
result, error = integrate.quad(lambda x: x**2, 0, 3)
```

#### 5. 链式法则
```python
# 复合函数 h(x) = f(g(x)) = (2x + 1)³
def g(x): return 2*x + 1
def f(u): return u**3

# 链式法则: h'(x) = f'(g(x)) * g'(x)
def dh_dx(x):
    u = g(x)
    return 3*u**2 * 2  # f'(u) * g'(x)
```

## 🧪 测试覆盖

测试文件 `test_calculus.py` 包含以下测试：

✅ 基本导数计算测试  
✅ 偏导数计算测试  
✅ 梯度计算测试  
✅ 梯度下降收敛性测试  
✅ 数值积分测试  
✅ 链式法则测试  
✅ 二阶导数测试  
✅ 多元函数极值测试  

## 🎯 实际应用场景

### 1. 机器学习优化
```python
# 线性回归的梯度下降
def compute_gradients(X, y, weights):
    predictions = X @ weights
    errors = predictions - y
    gradients = 2 * X.T @ errors / len(y)
    return gradients

# 参数更新
weights = weights - learning_rate * gradients
```

### 2. 神经网络反向传播
```python
# 链式法则在反向传播中的应用
# 输出层梯度
dL_doutput = 2 * (output - target)

# 隐藏层梯度（链式法则）
dL_dhidden = dL_doutput * weights_output * activation_derivative(hidden)
```

### 3. 概率密度函数
```python
# 正态分布的概率计算需要积分
from scipy.stats import norm
probability = norm.cdf(b) - norm.cdf(a)  # P(a < X < b)
```

## ⚡ 最佳实践建议

### 1. 数值稳定性
- 选择合适的学习率
- 使用自适应学习率方法
- 注意梯度消失和爆炸问题

### 2. 计算效率
- 向量化计算优于循环
- 利用矩阵运算的优化
- 选择合适的数值积分方法

### 3. 实际应用考虑
- 理解数学概念的物理意义
- 根据问题特点选择合适的优化方法
- 注意数值精度和计算复杂度的平衡

## 🔍 常见问题和解决方案

### 1. 梯度下降不收敛
```python
# 问题：学习率过大导致震荡
# 解决：使用学习率调度或自适应方法
from torch.optim import Adam
optimizer = Adam(model.parameters(), lr=0.001)
```

### 2. 数值积分精度问题
```python
# 问题：简单方法精度不足
# 解决：使用高精度方法或增加采样点
result, error = integrate.quad(func, a, b, epsabs=1e-10, epsrel=1e-10)
```

## 📚 扩展学习资源

### 官方文档
- [NumPy数学函数](https://numpy.org/doc/stable/reference/routines.math.html)
- [SciPy积分模块](https://docs.scipy.org/doc/scipy/reference/integrate.html)

### 推荐书籍
- 《微积分学教程》- Г.М. 菲赫金哥尔茨
- 《数值分析》- Richard L. Burden
- 《深度学习》- Ian Goodfellow

### 相关课程
- MIT单变量微积分
- 斯坦福凸优化课程

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含完整的微积分基础演示

---
**注意**: 微积分是机器学习优化算法的数学基础，深入理解这些概念对掌握深度学习至关重要。
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
