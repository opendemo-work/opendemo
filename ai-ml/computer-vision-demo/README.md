# 计算机视觉入门 - 图像分类与目标检测

> 使用 PyTorch 和 torchvision 实现图像分类与目标检测，理解卷积神经网络（CNN）在视觉任务中的应用。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解 CNN 在计算机视觉中的作用
- ✅ 使用 torchvision 加载预训练模型
- ✅ 实现图像分类推理
- ✅ 了解目标检测的基本流程

---

## 📐 架构图

```
输入图像 ──▶ 预处理 ──▶ CNN 骨干网络 ──▶ 分类头/检测头 ──▶ 预测结果
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 |
|------|----------|
| Python | >= 3.9 |
| PyTorch | >= 2.0 |
| torchvision | >= 0.15 |

### 安装与运行

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd ai-ml/computer-vision-demo
pip install -r requirements.txt
python code/image_classification.py
```

---

## 📖 核心概念

### 1. 卷积神经网络（CNN）

CNN 通过卷积层提取图像的局部特征，池化层降低维度，全连接层进行分类。

### 2. 图像分类

将输入图像分配到预定义类别，使用 Softmax 输出概率分布。

### 3. 目标检测

不仅识别类别，还要定位目标位置，常用模型包括 YOLO、Faster R-CNN、SSD。

### 4. 迁移学习

使用在 ImageNet 上预训练的模型，针对特定任务进行微调。

---

## 💻 代码示例

### 图像分类

```python
import torch
from torchvision import models, transforms
from PIL import Image

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

img = Image.open("data/cat.jpg")
input_tensor = transform(img).unsqueeze(0)

with torch.no_grad():
    output = model(input_tensor)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top5 = torch.topk(probabilities, 5)
    print(top5)
```

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
python code/image_classification.py
python code/object_detection.py
```

---

## 📚 扩展学习

- [神经网络基础](../deep-learning/neural-network-basics/)
- [PyTorch 官方教程](https://pytorch.org/tutorials/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 核心流程

计算机视觉实战演示 从启动到完成主要包含以下环节：

1. **环境准备**：配置运行所需的依赖、网络和存储资源。
2. **主流程执行**：运行案例的核心逻辑并产出结果。
3. **结果验证**：通过日志、命令输出或测试用例确认正确性。
4. **资源回收**：停止服务并清理临时数据，保证可重复执行。

### 设计要点

| 方面 | 做法 | 说明 |
|------|------|------|
| 部署方式 | 本地容器化 | 减少环境差异，便于复现 |
| 配置管理 | 配置文件 + 环境变量 | 兼顾可读性与灵活性 |
| 可观测性 | 日志 + 健康检查 | 方便定位问题 |
| 扩展方式 | 模块化组织 | 后续可按需增加功能 |

### 需要关注的指标

在生产环境中落地类似方案时，建议留意：

- 关键路径的响应延迟
- CPU、内存、磁盘和网络资源使用
- 并发量与吞吐量变化
- 错误率和异常告警

---

## 🛡️ 安全与最佳实践

### 安全建议

- 生产环境不要使用默认密码、密钥或令牌。
- 定期将依赖升级到稳定的最新版本。
- 敏感配置优先使用密钥管理工具或环境变量注入。
- 通过防火墙、安全组或网络策略限制访问范围。

### 操作建议

- 修改配置前备份现有环境。
- 将配置文件和脚本纳入版本控制。
- 为核心路径补充自动化测试。
- 保留运行日志以便审计和排障。

---

## 🧪 进阶实验

基础流程跑通后，可以尝试：

1. 调整关键参数，观察对结果的影响。
2. 模拟异常场景，验证容错能力。
3. 增加负载，分析系统瓶颈。
4. 与其他组件组合，形成完整链路。

---

## 📚 扩展资源

- 相关技术的官方文档
- [OpenDemo 项目主页](https://github.com/opendemo)
- GitHub Discussions 与技术社区

---

## 🤝 贡献与反馈

如发现内容有误或希望补充，欢迎提交 Issue 或 Pull Request。

---

*本 README 由 OpenDemo 自动生成并持续维护，欢迎根据实际案例补充细节。*


---

## 🖼️ 数据增强

在训练计算机视觉模型时，数据增强可以提升泛化能力：

```python
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor()
])
```

常用增强操作包括随机裁剪、翻转、旋转、缩放和颜色抖动。

---

## 📊 模型评估

分类任务常用评估指标：

| 指标 | 说明 |
|------|------|
| Accuracy | 准确率 |
| Precision | 精确率 |
| Recall | 召回率 |
| F1 Score | 精确率和召回率的调和平均 |
| mAP | 目标检测平均精度 |
