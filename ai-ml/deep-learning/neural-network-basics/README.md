# 神经网络基础

## 🎯 案例概述

这是一个全面展示神经网络基础概念的示例，涵盖感知机、多层感知机、激活函数、反向传播等深度学习核心原理。

## 📚 学习目标

通过本示例你将掌握：
- 感知机的工作原理和局限性
- 多层感知机的结构和训练方法
- 常用激活函数的特点和应用
- 反向传播算法的手动实现
- 深度学习基础概念的理解

## 🔧 核心知识点

### 1. 感知机原理
- 单层神经网络结构
- 权重更新规则
- 线性可分问题
- 逻辑门实现

### 2. 多层感知机
- 隐藏层的作用
- 非线性映射能力
- 前向传播过程
- 网络深度的影响

### 3. 激活函数
- Sigmoid函数特性
- ReLU及其变种
- Tanh函数
- Softmax函数

### 4. 反向传播
- 链式法则应用
- 梯度计算过程
- 权重更新机制
- 损失函数优化

## 🚀 运行示例

```bash
# 安装依赖
pip install numpy matplotlib torch pytest

# 运行主程序
python neural_network_basics.py

# 运行测试
python -m pytest test_neural_network.py -v
```

## 📖 代码详解

### 主要类结构

```python
class NeuralNetworkBasics:
    def perceptron_demo(self):           # 感知机演示
    def mlp_classification_demo(self):   # 多层感知机演示
    def activation_functions_demo(self): # 激活函数演示
    def backpropagation_demo(self):      # 反向传播演示
```

### 关键技术点演示

#### 1. 感知机实现
```python
# 感知机前向传播
z = np.dot(weights, input) + bias
output = step_activation(z)  # 阶跃函数

# 权重更新规则
weights += learning_rate * error * input
bias += learning_rate * error
```

#### 2. MLP网络结构
```python
class SimpleMLP(nn.Module):
    def __init__(self):
        self.hidden = nn.Linear(2, 8)    # 输入层到隐藏层
        self.output = nn.Linear(8, 1)    # 隐藏层到输出层
        self.activation = nn.ReLU()      # 激活函数
    
    def forward(self, x):
        x = self.activation(self.hidden(x))
        x = torch.sigmoid(self.output(x))
        return x
```

#### 3. 反向传播手动实现
```python
# 输出层梯度
dL_da2 = -(target - output)
da2_dz2 = output * (1 - output)  # sigmoid导数
dL_dz2 = dL_da2 * da2_dz2

# 权重梯度
dL_dW2 = np.outer(hidden_output, dL_dz2)
dL_dW1 = np.outer(input, dL_dz1)

# 更新权重
W2 -= learning_rate * dL_dW2
W1 -= learning_rate * dL_dW1
```

#### 4. 激活函数对比
```python
# Sigmoid: σ(x) = 1/(1+e^(-x))
def sigmoid(x): return 1 / (1 + np.exp(-x))

# ReLU: f(x) = max(0,x)
def relu(x): return np.maximum(0, x)

# Tanh: tanh(x) = (e^x - e^(-x))/(e^x + e^(-x))
def tanh(x): return np.tanh(x)
```

## 🧪 测试覆盖

测试文件 `test_neural_network.py` 包含以下测试：

✅ 阶跃激活函数测试  
✅ Sigmoid函数测试  
✅ ReLU函数测试  
✅ Tanh函数测试  
✅ 感知机AND门测试  
✅ Softmax归一化测试  
✅ 矩阵运算形状测试  
✅ PyTorch MLP结构测试  
✅ 梯度计算测试  
✅ XOR问题线性不可分测试  

## 🎯 实际应用场景

### 1. 图像分类
```python
# CNN中的全连接层就是MLP
class ImageClassifier(nn.Module):
    def __init__(self):
        self.conv_layers = nn.Sequential(...)
        self.fc_layers = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 10)  # 10个类别
        )
```

### 2. 自然语言处理
```python
# Transformer中的前馈网络
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        self.linear1 = nn.Linear(d_model, d_ff)
        self.activation = nn.ReLU()
        self.linear2 = nn.Linear(d_ff, d_model)
```

### 3. 强化学习
```python
# 策略网络
class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Softmax(dim=-1)
        )
```

## ⚡ 最佳实践建议

### 1. 网络设计
- 根据问题复杂度选择合适的网络深度
- 隐藏层大小通常为输入输出的几何平均
- 使用批归一化提高训练稳定性

### 2. 激活函数选择
- 隐藏层优先使用ReLU或其变种
- 输出层根据任务选择：sigmoid(二分类)、softmax(多分类)
- 避免梯度消失：使用残差连接或归一化

### 3. 训练技巧
- 合理设置学习率和优化器
- 使用早停防止过拟合
- 监控训练和验证损失曲线

## 🔍 常见问题和解决方案

### 1. 梯度消失问题
```python
# 问题：深层网络梯度接近零
# 解决：使用残差连接
class ResidualBlock(nn.Module):
    def forward(self, x):
        residual = x
        out = self.layers(x)
        return out + residual  # 残差连接
```

### 2. 过拟合问题
```python
# 问题：训练效果好但测试效果差
# 解决：添加正则化
model = nn.Sequential(
    nn.Linear(100, 50),
    nn.Dropout(0.5),  # Dropout正则化
    nn.Linear(50, 10)
)
```

## 📚 扩展学习资源

### 官方文档
- [PyTorch神经网络](https://pytorch.org/docs/stable/nn.html)
- [深度学习优化器](https://pytorch.org/docs/stable/optim.html)

### 推荐书籍
- 《深度学习》- Ian Goodfellow
- 《动手学深度学习》- 李沐
- 《神经网络与深度学习》- 邱锡鹏

### 相关课程
- CS231n卷积神经网络
- DeepLearning.AI深度学习专项课程

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含完整的神经网络基础演示

---
**注意**: 神经网络是深度学习的基础，深入理解这些概念对掌握现代AI技术至关重要。