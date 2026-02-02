# 卷积神经网络基础

## 🎯 案例概述

这是一个全面展示卷积神经网络基础概念的示例，涵盖卷积操作、池化操作、CNN架构等计算机视觉核心原理。

## 📚 学习目标

通过本示例你将掌握：
- 卷积操作的数学原理和实现
- 池化操作的作用和不同类型
- CNN网络架构的设计原则
- 计算机视觉中的特征提取机制

## 🔧 核心知识点

### 1. 卷积操作
- 卷积核的设计和作用
- 步长和填充参数
- 特征图的生成过程
- 边缘检测和模式识别

### 2. 池化操作
- 最大池化和平均池化
- 空间降维的作用
- 平移不变性
- 计算效率提升

### 3. CNN架构
- 卷积层堆叠设计
- 特征层次化提取
- 参数共享机制
- 网络深度的影响

## 🚀 运行示例

```bash
# 安装依赖
pip install numpy matplotlib torch torchvision pytest

# 运行主程序
python cnn_basics.py

# 运行测试
python -m pytest test_cnn.py -v
```

## 📖 代码详解

### 主要类结构

```python
class CNNBasics:
    def convolution_operation_demo(self):    # 卷积操作演示
    def pooling_operation_demo(self):        # 池化操作演示
    def simple_cnn_architecture_demo(self):  # CNN架构演示
```

### 关键技术点演示

#### 1. 卷积操作实现
```python
def manual_conv2d(image, kernel, padding=0):
    # 填充处理
    if padding > 0:
        padded_image = np.pad(image, padding, mode='constant')
    
    # 滑动窗口卷积
    for i in range(out_height):
        for j in range(out_width):
            patch = image[i:i+kernel_height, j:j+kernel_width]
            result[i, j] = np.sum(patch * kernel)
```

#### 2. 池化操作实现
```python
def manual_max_pool2d(feature_map, pool_size=2):
    for i in range(out_height):
        for j in range(out_width):
            region = feature_map[i*pool_size:(i+1)*pool_size, 
                               j*pool_size:(j+1)*pool_size]
            result[i, j] = np.max(region)  # 最大池化
```

#### 3. CNN架构设计
```python
class SimpleCNN(nn.Module):
    def __init__(self):
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
```

## 🧪 测试覆盖

测试文件 `test_cnn.py` 包含以下测试：

✅ 手动卷积操作测试  
✅ 带填充卷积测试  
✅ 最大池化操作测试  
✅ 平均池化操作测试  
✅ 池化尺寸一致性测试  
✅ PyTorch CNN层测试  
✅ CNN参数计数测试  
✅ 特征图尺寸测试  

## 🎯 实际应用场景

### 1. 图像分类
```python
# 经典CNN架构
class ImageClassifier(nn.Module):
    def __init__(self, num_classes=10):
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # ... 更多层
        )
        self.classifier = nn.Sequential(
            nn.Linear(512 * 4 * 4, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes)
        )
```

### 2. 目标检测
```python
# Faster R-CNN中的特征提取网络
class FeatureExtractor(nn.Module):
    def __init__(self):
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            # ... Backbone网络
        )
```

### 3. 图像分割
```python
# U-Net编码器-解码器结构
class UNetEncoder(nn.Module):
    def __init__(self):
        self.down_conv1 = self.contract_block(3, 64)
        self.down_conv2 = self.contract_block(64, 128)
        # ... 编码器部分
```

## ⚡ 最佳实践建议

### 1. 网络设计原则
- 使用较小的卷积核(3×3)堆叠而非大卷积核
- 合理设置填充以保持特征图尺寸
- 逐渐增加通道数，减少空间尺寸

### 2. 训练技巧
- 数据增强提高泛化能力
- 批归一化加速训练
- 学习率调度策略

### 3. 性能优化
- 使用GPU加速计算
- 合理的批处理大小
- 内存优化和梯度裁剪

## 🔍 常见问题和解决方案

### 1. 梯度消失问题
```python
# 问题：深层CNN训练困难
# 解决：使用残差连接
class ResidualBlock(nn.Module):
    def forward(self, x):
        residual = x
        out = self.conv_block(x)
        return out + residual  # 跳跃连接
```

### 2. 过拟合问题
```python
# 问题：训练准确率高但测试准确率低
# 解决：正则化技术
model = nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1),
    nn.BatchNorm2d(64),
    nn.ReLU(),
    nn.Dropout2d(0.2),  # 2D Dropout
    # ...
)
```

## 📚 扩展学习资源

### 官方文档
- [PyTorch卷积层](https://pytorch.org/docs/stable/nn.html#convolution-layers)
- [torchvision数据集](https://pytorch.org/vision/stable/datasets.html)

### 推荐书籍
- 《计算机视觉：算法与应用》- Richard Szeliski
- 《深度学习与计算机视觉》- 叶韵
- 《动手学深度学习》- 李沐团队

### 相关课程
- CS231n计算机视觉
- Fast.ai计算机视觉课程

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含完整的CNN基础演示

---
**注意**: CNN是计算机视觉领域的基础，深入理解这些概念对掌握图像处理技术至关重要。