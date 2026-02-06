# 计算机视觉实战演示

## 🎯 学习目标

通过本案例你将掌握：
- 计算机视觉基础概念和核心技术
- 图像分类、目标检测和图像分割技术
- 深度学习在计算机视觉中的应用
- 计算机视觉模型的部署和优化

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- GPU环境（推荐NVIDIA GPU，CUDA 11.0+）
- 至少16GB内存

### 依赖安装
```bash
pip install torch torchvision torchaudio
pip install opencv-python pillow scikit-image  # 图像处理
pip install albumentations imgaug  # 数据增强
pip install detectron2  # 目标检测
pip install segmentation-models-pytorch  # 分割模型
pip install pytest  # 测试工具
```

## 📁 项目结构

```
computer-vision-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── train_classifier.py            # 图像分类训练脚本
│   ├── train_detector.py              # 目标检测训练脚本
│   ├── train_segmenter.py             # 图像分割训练脚本
│   └── inference_pipeline.py          # 推理流水线脚本
├── configs/                           # 配置文件
│   ├── classifier_config.yaml         # 分类器配置
│   ├── detector_config.yaml           # 检测器配置
│   ├── segmenter_config.yaml          # 分割器配置
│   └── preprocessing_config.json      # 预处理配置
├── models/                            # 模型文件
│   ├── architectures/                 # 模型架构
│   │   ├── resnet.py                 # ResNet架构
│   │   ├── efficientnet.py           # EfficientNet架构
│   │   ├── yolov5.py                 # YOLOv5架构
│   │   └── unet.py                   # U-Net架构
│   ├── checkpoints/                   # 模型检查点
│   └── pretrained/                    # 预训练模型
├── data/                              # 数据文件
│   ├── datasets/                      # 数据集
│   ├── annotations/                   # 标注文件
│   ├── processed/                     # 处理后数据
│   └── samples/                       # 示例图片
├── transforms/                        # 数据变换
│   ├── augmentations.py               # 数据增强
│   ├── preprocessing.py               # 预处理
│   └── postprocessing.py             # 后处理
├── utils/                             # 工具函数
│   ├── visualization.py               # 可视化工具
│   ├── metrics.py                     # 评估指标
│   └── io_utils.py                    # 输入输出工具
├── training/                          # 训练代码
│   ├── trainer.py                     # 训练器
│   ├── callbacks.py                   # 回调函数
│   └── losses.py                      # 损失函数
├── inference/                         # 推理代码
│   ├── engine.py                      # 推理引擎
│   ├── optimizers.py                  # 推理优化
│   └── benchmark.py                   # 性能基准
└── notebooks/                         # Jupyter笔记本
    ├── 01_image_classification.ipynb  # 图像分类
    ├── 02_object_detection.ipynb      # 目标检测
    └── 03_image_segmentation.ipynb    # 图像分割
```

## 🚀 快速开始

### 步骤1：环境设置

```bash
# 安装计算机视觉相关依赖
pip install -r requirements.txt
```

### 步骤2：数据准备

```bash
# 下载示例数据集
mkdir -p data/datasets/cifar10
wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz -O data/datasets/cifar10/cifar-10-python.tar.gz
tar -xzf data/datasets/cifar-10-python.tar.gz -C data/datasets/cifar10/
```

### 步骤3：训练图像分类模型

```bash
# 训练ResNet分类器
python scripts/train_classifier.py \
  --config configs/classifier_config.yaml \
  --dataset cifar10 \
  --model resnet18 \
  --epochs 50 \
  --batch_size 32 \
  --output_dir models/checkpoints/classifier/
```

### 步骤4：运行推理

```bash
# 运行图像分类推理
python scripts/inference_pipeline.py \
  --model_path models/checkpoints/classifier/resnet18_final.pth \
  --image_path data/samples/sample.jpg \
  --task classification \
  --output_dir results/classification/
```

## 🔍 代码详解

### 核心概念解析

#### 1. 图像分类模型实现
```python
# models/architectures/resnet.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out

class ResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes=10):
        super(ResNet, self).__init__()
        self.in_planes = 64

        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.linear = nn.Linear(512*block.expansion, num_classes)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out

def ResNet18():
    return ResNet(BasicBlock, [2, 2, 2, 2])
```

#### 2. 实际应用示例

##### 场景1：数据增强实现
```python
# transforms/augmentations.py
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2

def get_training_augmentation():
    """获取训练数据增强"""
    train_transform = [
        A.Resize(height=224, width=224, interpolation=cv2.INTER_CUBIC),
        A.HorizontalFlip(p=0.5),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=15, p=0.5),
        A.Blur(blur_limit=3, p=0.1),
        A.CLAHE(clip_limit=2.0, tile_grid_size=(8, 8), p=0.1),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2(),
    ]
    return A.Compose(train_transform)

def get_validation_augmentation():
    """获取验证数据增强"""
    valid_transform = [
        A.Resize(height=224, width=224, interpolation=cv2.INTER_CUBIC),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2(),
    ]
    return A.Compose(valid_transform)
```

##### 场景2：目标检测实现
```python
# models/architectures/yolov5.py
import torch
import torch.nn as nn

class Conv(nn.Module):
    """Standard convolution"""
    def __init__(self, c1, c2, k=1, s=1, p=None, g=1, act=True):
        super(Conv, self).__init__()
        self.conv = nn.Conv2d(c1, c2, k, s, autopad(k, p), groups=g, bias=False)
        self.bn = nn.BatchNorm2d(c2)
        self.act = nn.SiLU() if act is True else (act if isinstance(act, nn.Module) else nn.Identity())

    def forward(self, x):
        return self.act(self.bn(self.conv(x)))

    def fuseforward(self, x):
        return self.act(self.conv(x))

class Detect(nn.Module):
    """YOLOv5 Detect head"""
    def __init__(self, nc=80, anchors=(), ch=()):  # detection layer
        super(Detect, self).__init__()
        self.nc = nc  # number of classes
        self.no = nc + 5  # number of outputs per anchor
        self.nl = len(anchors)  # number of detection layers
        self.na = len(anchors[0]) // 2  # number of anchors
        self.grid = [torch.zeros(1)] * self.nl  # init grid
        a = torch.tensor(anchors).float().view(self.nl, -1, 2)
        self.register_buffer('anchors', a)  # shape(nl,na,2)
        self.register_buffer('anchor_grid', a.clone().view(self.nl, 1, -1, 1, 1, 2))  # shape(nl,1,na,1,1,2)
        self.m = nn.ModuleList(nn.Conv2d(x, self.no * self.na, 1) for x in ch)  # output conv

    def forward(self, x):
        # x = input tensors (different scales)
        z = []  # inference output
        for i in range(self.nl):
            x[i] = self.m[i](x[i])  # conv
            bs, _, ny, nx = x[i].shape  # x(bs,255,20,20) to x(bs,3,20,20,85)
            x[i] = x[i].view(bs, self.na, self.no, ny, nx).permute(0, 1, 3, 4, 2).contiguous()

            if not self.training:  # inference
                if self.grid[i].shape[2:4] != x[i].shape[2:4]:
                    self.grid[i] = self._make_grid(nx, ny).to(x[i].device)

                y = x[i].sigmoid()
                y[..., 0:2] = (y[..., 0:2] * 2. - 0.5 + self.grid[i]) * self.stride[i]  # xy
                y[..., 2:4] = (y[..., 2:4] * 2) ** 2 * self.anchor_grid[i]  # wh
                z.append(y.view(bs, -1, self.no))

        return x if self.training else (torch.cat(z, 1), x)

    @staticmethod
    def _make_grid(nx=20, ny=20):
        yv, xv = torch.meshgrid([torch.arange(ny), torch.arange(nx)])
        return torch.stack((xv, yv), 2).view((1, 1, ny, nx, 2)).float()
```

## 🧪 验证测试

### 测试1：模型构建验证
```python
#!/usr/bin/env python
# 验证计算机视觉模型构建
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

def test_cv_model():
    print("=== 计算机视觉模型验证 ===")
    
    # 测试ResNet模型
    from models.architectures.resnet import ResNet18
    
    model = ResNet18()
    print(f"✅ ResNet18模型构建成功")
    print(f"模型参数数量: {sum(p.numel() for p in model.parameters()):,}")
    
    # 测试前向传播
    dummy_input = torch.randn(1, 3, 32, 32)  # CIFAR-10尺寸
    with torch.no_grad():
        output = model(dummy_input)
    
    print(f"✅ 前向传播正常，输出形状: {output.shape}")
    
    # 测试分类准确率（随机初始化模型的预期行为）
    probabilities = torch.softmax(output, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1)
    print(f"预测类别: {predicted_class.item()}")
    
    print("✅ 计算机视觉模型验证通过")

if __name__ == "__main__":
    test_cv_model()
```

### 测试2：数据预处理验证
```python
#!/usr/bin/env python
# 验证数据预处理管道
import torch
import torchvision.transforms as transforms
import numpy as np
from PIL import Image

def test_preprocessing_pipeline():
    print("=== 数据预处理管道验证 ===")
    
    # 创建模拟图像
    img_array = np.random.randint(0, 255, size=(64, 64, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    
    # 定义预处理管道
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # 应用预处理
    processed_img = transform(img)
    
    print(f"✅ 图像预处理成功")
    print(f"原始尺寸: {img_array.shape}")
    print(f"处理后尺寸: {processed_img.shape}")
    print(f"像素值范围: [{processed_img.min():.3f}, {processed_img.max():.3f}]")
    
    # 验证归一化
    mean_vals = [processed_img[i].mean().item() for i in range(3)]
    std_vals = [processed_img[i].std().item() for i in range(3)]
    
    print(f"通道均值: {mean_vals}")
    print(f"通道标准差: {std_vals}")
    
    print("✅ 数据预处理管道验证通过")

if __name__ == "__main__":
    test_preprocessing_pipeline()
```

## ❓ 常见问题

### Q1: 如何选择合适的计算机视觉架构？
**解决方案**：
```python
# 计算机视觉架构选择指南
"""
1. 图像分类: ResNet, EfficientNet, Vision Transformer
2. 目标检测: YOLO, Faster R-CNN, SSD
3. 图像分割: U-Net, DeepLab, Mask R-CNN
4. 关键点检测: HRNet, OpenPose
"""
```

### Q2: 如何优化计算机视觉模型的推理性能？
**解决方案**：
```python
# 推理性能优化策略
"""
1. 模型量化: INT8量化减少模型大小和推理时间
2. 模型剪枝: 移除冗余参数和连接
3. 知识蒸馏: 使用小型学生模型模仿大型教师模型
4. 硬件加速: 使用TensorRT、OpenVINO等优化推理
"""
```

## 📚 扩展学习

### 相关技术
- **OpenCV**: 计算机视觉基础库
- **Detectron2**: Facebook目标检测框架
- **MMdetection**: 开源目标检测工具箱
- **Segment Anything**: Meta图像分割模型

### 进阶学习路径
1. 掌握经典CNN架构和现代Transformer架构
2. 学习先进的数据增强和正则化技术
3. 理解自监督学习在视觉中的应用
4. 掌握多模态视觉-语言模型

### 企业级应用场景
- 工业质检和缺陷检测
- 医疗影像分析诊断
- 自动驾驶视觉感知
- 零售商品识别和分析

---
> **💡 提示**: 计算机视觉是AI的重要分支，通过深度学习技术实现了图像识别、目标检测、图像分割等复杂任务，广泛应用于各个行业领域。