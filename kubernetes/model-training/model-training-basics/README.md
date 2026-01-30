# 大模型训练基础入门

## 1. 案例概述

本案例介绍Kubernetes环境下大模型训练的基础知识和实践操作，帮助初学者快速上手大模型训练。

### 1.1 学习目标

- 理解大模型训练的基本概念和流程
- 掌握Kubernetes训练环境的搭建方法
- 学会编写基础的训练脚本
- 了解训练数据的准备和管理
- 掌握基本的训练监控方法

### 1.2 适用人群

- Kubernetes初学者
- 机器学习入门者
- 对大模型训练感兴趣的开发者

## 2. 环境准备

### 2.1 硬件要求

- CPU: 至少8核
- 内存: 至少32GB
- GPU: 至少1块NVIDIA GPU(推荐16GB显存以上)
- 存储: 至少500GB可用空间

### 2.2 软件环境

```bash
# Kubernetes集群(v1.23+)
kubectl version --short

# NVIDIA GPU驱动
nvidia-smi

# Docker环境
docker --version

# Python环境
python --version  # 推荐3.8+
```

### 2.3 命名空间创建

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: model-training-basics
  labels:
    purpose: "model-training-tutorial"
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: training-quota
  namespace: model-training-basics
spec:
  hard:
    requests.cpu: "8"
    requests.memory: 32Gi
    requests.nvidia.com/gpu: "1"
    limits.cpu: "16"
    limits.memory: 64Gi
    limits.nvidia.com/gpu: "1"
```

## 3. 基础训练环境搭建

### 3.1 GPU驱动和运行时配置

```yaml
# NVIDIA Device Plugin部署
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nvidia-device-plugin-daemonset
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: nvidia-device-plugin-ds
  template:
    metadata:
      labels:
        name: nvidia-device-plugin-ds
    spec:
      tolerations:
      - key: nvidia.com/gpu
        operator: Exists
        effect: NoSchedule
      containers:
      - image: nvcr.io/nvidia/k8s-device-plugin:v0.14.0
        name: nvidia-device-plugin-ctr
        env:
        - name: FAIL_ON_INIT_ERROR
          value: "false"
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop: ["ALL"]
        volumeMounts:
        - name: device-plugin
          mountPath: /var/lib/kubelet/device-plugins
      volumes:
      - name: device-plugin
        hostPath:
          path: /var/lib/kubelet/device-plugins
```

### 3.2 基础训练镜像准备

```dockerfile
# Dockerfile.training-base
FROM nvidia/cuda:11.8-devel-ubuntu20.04

# 安装基础依赖
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置Python环境
ENV PYTHONUNBUFFERED=1
WORKDIR /workspace

# 安装机器学习库
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制训练代码
COPY train.py .
COPY data/ ./data/

CMD ["python3", "train.py"]
```

对应的requirements.txt:
```txt
torch>=2.0.0
torchvision>=0.15.0
transformers>=4.30.0
datasets>=2.12.0
accelerate>=0.20.0
wandb>=0.15.0
numpy>=1.21.0
```

## 4. 简单模型训练示例

### 4.1 图像分类训练

```python
# train.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import wandb
import os

def create_model():
    """创建简单的CNN模型"""
    model = nn.Sequential(
        nn.Conv2d(3, 32, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(64, 128, 3, padding=1),
        nn.ReLU(),
        nn.AdaptiveAvgPool2d((1, 1)),
        nn.Flatten(),
        nn.Linear(128, 10)
    )
    return model

def train_epoch(model, dataloader, criterion, optimizer, device):
    """训练一个epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch_idx, (data, target) in enumerate(dataloader):
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        total += target.size(0)
        
        if batch_idx % 100 == 0:
            print(f'Batch {batch_idx}, Loss: {loss.item():.6f}')
            
    accuracy = 100. * correct / total
    avg_loss = total_loss / len(dataloader)
    
    return avg_loss, accuracy

def main():
    # 初始化wandb
    wandb.init(project="basic-model-training", config={
        "learning_rate": 0.001,
        "batch_size": 64,
        "epochs": 10
    })
    
    # 设备配置
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 数据预处理
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    # 加载CIFAR-10数据集
    train_dataset = datasets.CIFAR10(
        root='./data', 
        train=True, 
        download=True, 
        transform=transform
    )
    
    train_loader = DataLoader(
        train_dataset, 
        batch_size=64, 
        shuffle=True,
        num_workers=2
    )
    
    # 创建模型
    model = create_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 训练循环
    for epoch in range(10):
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device
        )
        
        print(f'Epoch {epoch+1}: Loss={train_loss:.4f}, Accuracy={train_acc:.2f}%')
        
        # 记录到wandb
        wandb.log({
            "epoch": epoch + 1,
            "train_loss": train_loss,
            "train_accuracy": train_acc
        })
    
    # 保存模型
    torch.save(model.state_dict(), "model.pth")
    wandb.save("model.pth")
    
    wandb.finish()

if __name__ == "__main__":
    main()
```

### 4.2 Kubernetes训练作业配置

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: cifar10-training-basic
  namespace: model-training-basics
spec:
  template:
    spec:
      containers:
      - name: training-container
        image: your-registry/model-training:basic
        command: ["python3", "train.py"]
        resources:
          limits:
            nvidia.com/gpu: 1
            cpu: 4
            memory: 16Gi
          requests:
            nvidia.com/gpu: 1
            cpu: 2
            memory: 8Gi
        volumeMounts:
        - name: training-data
          mountPath: /workspace/data
        - name: model-output
          mountPath: /workspace/output
        env:
        - name: WANDB_API_KEY
          valueFrom:
            secretKeyRef:
              name: wandb-secret
              key: api-key
      volumes:
      - name: training-data
        persistentVolumeClaim:
          claimName: training-data-pvc
      - name: model-output
        persistentVolumeClaim:
          claimName: model-output-pvc
      restartPolicy: OnFailure
```

## 5. 数据管理

### 5.1 数据持久化配置

```yaml
# 训练数据PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: training-data-pvc
  namespace: model-training-basics
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: fast-ssd

---
# 模型输出PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-output-pvc
  namespace: model-training-basics
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
  storageClassName: fast-ssd
```

### 5.2 数据预处理脚本

```python
# preprocess_data.py
import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
import argparse

def prepare_cifar10_data(data_dir="./data", val_split=0.2):
    """准备CIFAR-10数据集"""
    
    # 创建数据目录
    os.makedirs(data_dir, exist_ok=True)
    
    # 数据预处理
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), 
                           (0.2023, 0.1994, 0.2010)),
    ])
    
    transform_val = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), 
                           (0.2023, 0.1994, 0.2010)),
    ])
    
    # 下载数据集
    full_dataset = datasets.CIFAR10(
        root=data_dir, 
        train=True, 
        download=True, 
        transform=None
    )
    
    # 划分训练集和验证集
    train_size = int((1 - val_split) * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
    
    # 应用不同的变换
    class TransformDataset(torch.utils.data.Dataset):
        def __init__(self, subset, transform=None):
            self.subset = subset
            self.transform = transform
            
        def __getitem__(self, index):
            x, y = self.subset[index]
            if self.transform:
                x = self.transform(x)
            return x, y
            
        def __len__(self):
            return len(self.subset)
    
    train_dataset = TransformDataset(train_dataset, transform_train)
    val_dataset = TransformDataset(val_dataset, transform_val)
    
    print(f"训练集大小: {len(train_dataset)}")
    print(f"验证集大小: {len(val_dataset)}")
    
    return train_dataset, val_dataset

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="./data", help="数据目录")
    parser.add_argument("--val-split", type=float, default=0.2, help="验证集比例")
    args = parser.parse_args()
    
    train_dataset, val_dataset = prepare_cifar10_data(
        args.data_dir, args.val_split
    )
    
    # 保存数据集信息
    dataset_info = {
        "train_size": len(train_dataset),
        "val_size": len(val_dataset),
        "num_classes": 10,
        "classes": ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                   'dog', 'frog', 'horse', 'ship', 'truck']
    }
    
    torch.save(dataset_info, os.path.join(args.data_dir, "dataset_info.pt"))
    print("数据准备完成!")

if __name__ == "__main__":
    main()
```

## 6. 训练监控

### 6.1 Weights & Biases集成

```yaml
# wandb secret配置
apiVersion: v1
kind: Secret
metadata:
  name: wandb-secret
  namespace: model-training-basics
type: Opaque
data:
  api-key: <base64-encoded-wandb-api-key>
```

### 6.2 训练指标监控

```python
# monitor_training.py
import wandb
import torch
import time
from datetime import datetime

class TrainingMonitor:
    def __init__(self, project_name="model-training"):
        self.project_name = project_name
        self.run = None
        
    def start_run(self, config=None):
        """开始监控会话"""
        self.run = wandb.init(
            project=self.project_name,
            config=config or {},
            name=f"training-run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        )
        
    def log_metrics(self, metrics, step=None):
        """记录训练指标"""
        if self.run:
            wandb.log(metrics, step=step)
            
    def log_model(self, model, model_name="model"):
        """记录模型"""
        if self.run:
            torch.save(model.state_dict(), f"{model_name}.pth")
            wandb.save(f"{model_name}.pth")
            
    def finish_run(self):
        """结束监控会话"""
        if self.run:
            wandb.finish()

# 在训练脚本中使用
monitor = TrainingMonitor("cifar10-basic-training")

config = {
    "learning_rate": 0.001,
    "batch_size": 64,
    "epochs": 10,
    "model_type": "simple-cnn"
}

monitor.start_run(config)
```

### 6.3 GPU资源监控

```yaml
# GPU监控DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: gpu-monitor
  namespace: model-training-basics
spec:
  selector:
    matchLabels:
      name: gpu-monitor
  template:
    metadata:
      labels:
        name: gpu-monitor
    spec:
      containers:
      - name: gpu-monitor
        image: nvidia/dcgm-exporter:3.1.6-3.1.0
        ports:
        - containerPort: 9400
        resources:
          limits:
            nvidia.com/gpu: 1
        volumeMounts:
        - name: pod-gpu-resources
          readOnly: true
          mountPath: /var/lib/kubelet/pod-resources
      volumes:
      - name: pod-gpu-resources
        hostPath:
          path: /var/lib/kubelet/pod-resources
```

## 7. 案例部署与验证

### 7.1 部署步骤

```bash
# 1. 创建命名空间和资源配额
kubectl apply -f namespace.yaml

# 2. 部署NVIDIA设备插件
kubectl apply -f nvidia-device-plugin.yaml

# 3. 创建存储卷
kubectl apply -f storage.yaml

# 4. 构建和推送训练镜像
docker build -t your-registry/model-training:basic -f Dockerfile.training-base .
docker push your-registry/model-training:basic

# 5. 创建W&B密钥
kubectl create secret generic wandb-secret \
    --from-literal=api-key=your-wandb-api-key \
    -n model-training-basics

# 6. 启动训练作业
kubectl apply -f training-job.yaml
```

### 7.2 验证训练状态

```bash
# 查看训练作业状态
kubectl get jobs -n model-training-basics

# 查看Pod状态
kubectl get pods -n model-training-basics

# 查看训练日志
kubectl logs -f -n model-training-basics -l job-name=cifar10-training-basic

# 查看GPU使用情况
kubectl exec -it <pod-name> -n model-training-basics -- nvidia-smi

# 查看存储使用情况
kubectl exec -it <pod-name> -n model-training-basics -- df -h
```

### 7.3 结果验证

```bash
# 检查模型文件是否生成
kubectl exec -it <pod-name> -n model-training-basics -- ls -la /workspace/output/

# 验证模型加载
kubectl exec -it <pod-name> -n model-training-basics -- python3 -c "
import torch
model = torch.load('/workspace/output/model.pth')
print('模型加载成功!')
print(f'模型大小: {len(str(model))} 字节')
"
```

## 8. 常见问题与解决方案

### 8.1 GPU资源不足

**问题**: `0/5 nodes are available: 5 Insufficient nvidia.com/gpu`

**解决方案**:
```bash
# 检查GPU节点状态
kubectl get nodes -l nvidia.com/gpu.present=true

# 检查GPU插件状态
kubectl get daemonsets -n kube-system nvidia-device-plugin-daemonset

# 查看节点GPU容量
kubectl describe nodes | grep -i nvidia
```

### 8.2 存储空间不足

**问题**: `DiskPressure` 或训练过程中出现磁盘满错误

**解决方案**:
```bash
# 检查存储使用情况
kubectl exec -it <pod-name> -- df -h

# 清理临时文件
kubectl exec -it <pod-name> -- rm -rf /tmp/*

# 增加存储容量
kubectl patch pvc training-data-pvc -p '{"spec":{"resources":{"requests":{"storage":"200Gi"}}}}'
```

### 8.3 网络连接问题

**问题**: 数据下载失败或wandb连接超时

**解决方案**:
```yaml
# 为Pod配置DNS和代理
apiVersion: v1
kind: Pod
spec:
  dnsConfig:
    nameservers:
      - 8.8.8.8
      - 8.8.4.4
  containers:
  - name: training
    env:
    - name: HTTP_PROXY
      value: "http://proxy.company.com:8080"
    - name: HTTPS_PROXY
      value: "http://proxy.company.com:8080"
```

## 9. 最佳实践

### 9.1 代码组织建议

```
model-training-basics/
├── Dockerfile
├── requirements.txt
├── train.py                 # 主训练脚本
├── preprocess_data.py       # 数据预处理
├── monitor_training.py      # 监控工具
├── configs/
│   ├── base_config.yaml     # 基础配置
│   └── training_config.yaml # 训练配置
├── scripts/
│   ├── build.sh             # 构建脚本
│   └── deploy.sh            # 部署脚本
└── manifests/
    ├── namespace.yaml       # 命名空间配置
    ├── storage.yaml         # 存储配置
    └── training-job.yaml    # 训练作业配置
```

### 9.2 训练配置管理

```yaml
# training_config.yaml
training:
  epochs: 10
  batch_size: 64
  learning_rate: 0.001
  validation_split: 0.2
  
model:
  type: "simple_cnn"
  input_channels: 3
  num_classes: 10
  
data:
  dataset: "cifar10"
  data_dir: "./data"
  num_workers: 2
  
logging:
  wandb_project: "model-training-basics"
  log_interval: 100
  save_checkpoint: true
```

### 9.3 版本控制建议

1. **Git标签管理**:
   ```bash
   git tag v1.0.0-initial-training
   git tag v1.1.0-improved-hyperparams
   ```

2. **模型版本追踪**:
   ```python
   import hashlib
   
   def get_model_hash(model_state_dict):
       """生成模型哈希值用于版本控制"""
       model_str = str(sorted(model_state_dict.items()))
       return hashlib.md5(model_str.encode()).hexdigest()[:8]
   ```

## 10. 总结

本案例介绍了Kubernetes大模型训练的基础入门知识，涵盖了：

✅ 环境搭建和配置  
✅ 基础训练脚本编写  
✅ 数据管理和预处理  
✅ 训练监控和日志记录  
✅ 常见问题诊断和解决  

通过本案例的学习，您应该能够：
- 独立搭建基础的Kubernetes训练环境
- 编写简单但完整的训练脚本
- 管理训练数据和模型输出
- 监控训练过程并分析结果
- 解决常见的训练问题

下一步建议学习分布式训练进阶案例，了解如何在多GPU环境下进行更大规模的模型训练。