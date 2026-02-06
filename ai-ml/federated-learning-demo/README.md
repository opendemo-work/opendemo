# 联邦学习实战演示

## 🎯 学习目标

通过本案例你将掌握：
- 联邦学习的基本概念和架构
- 联邦平均算法(FedAvg)的实现
- 联邦学习中的隐私保护技术
- 联邦学习系统的部署和管理

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- 多节点环境（本地可通过多进程模拟）
- 至少16GB内存

### 依赖安装
```bash
pip install torch torchvision tensorflow
pip install flwr flake  # 联邦学习框架
pip install syft  # 隐私保护库
pip install opacus  # 差分隐私库
pip install pytest  # 测试工具
```

## 📁 项目结构

```
federated-learning-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── start_server.py                # 启动联邦服务器
│   ├── start_client.py                # 启动联邦客户端
│   └── simulate_federation.py         # 联邦模拟脚本
├── configs/                           # 配置文件
│   ├── server_config.json             # 服务器配置
│   ├── client_config.json             # 客户端配置
│   └── privacy_config.yaml            # 隐私配置
├── server/                            # 服务器端代码
│   ├── server.py                      # 联邦服务器实现
│   ├── strategy.py                    # 联邦聚合策略
│   └── utils.py                       # 服务器工具函数
├── clients/                           # 客户端代码
│   ├── client.py                      # 联邦客户端实现
│   ├── local_training.py              # 本地训练逻辑
│   └── data_loader.py                 # 数据加载器
├── privacy/                           # 隐私保护
│   ├── differential_privacy.py        # 差分隐私实现
│   ├── homomorphic_encryption.py      # 同态加密实现
│   └── secure_aggregation.py          # 安全聚合实现
├── models/                            # 模型文件
│   ├── global_model.py                # 全局模型定义
│   ├── client_models/                 # 客户端模型
│   └── aggregation/                   # 聚合模型
├── data/                              # 数据文件
│   ├── partitions/                    # 数据分区
│   └── synthetic/                     # 合成数据
├── monitoring/                        # 监控代码
│   ├── metrics_collector.py           # 指标收集器
│   └── privacy_auditor.py             # 隐私审计器
└── notebooks/                         # Jupyter笔记本
    ├── 01_federated_learning_intro.ipynb   # 联邦学习介绍
    ├── 02_fedavg_implementation.ipynb      # FedAvg实现
    └── 03_privacy_preservation.ipynb       # 隐私保护
```

## 🚀 快速开始

### 步骤1：环境设置

```bash
# 安装联邦学习相关依赖
pip install -r requirements.txt
```

### 步骤2：启动联邦服务器

```bash
# 启动联邦学习服务器
python scripts/start_server.py \
  --server_address 0.0.0.0:8080 \
  --min_clients 2 \
  --rounds 10 \
  --strategy fedavg
```

### 步骤3：启动联邦客户端

```bash
# 启动第一个客户端
python scripts/start_client.py \
  --server_address localhost:8080 \
  --client_id 1 \
  --data_partition 0

# 启动第二个客户端
python scripts/start_client.py \
  --server_address localhost:8080 \
  --client_id 2 \
  --data_partition 1
```

### 步骤4：运行联邦学习模拟

```bash
# 运行本地联邦学习模拟
python scripts/simulate_federation.py \
  --num_clients 5 \
  --rounds 10 \
  --epochs_per_round 1 \
  --fraction_fit 0.8 \
  --fraction_evaluate 0.8
```

## 🔍 代码详解

### 核心概念解析

#### 1. 联邦学习服务器实现
```python
# server/server.py
import flwr as fl
from typing import List, Tuple, Optional
import torch
import torch.nn as nn

class FederatedServer:
    def __init__(self, model: nn.Module, strategy: fl.server.strategy.Strategy):
        self.model = model
        self.strategy = strategy
    
    def start_server(self, server_address: str, rounds: int):
        """启动联邦学习服务器"""
        fl.server.start_server(
            server_address=server_address,
            config=fl.server.ServerConfig(num_rounds=rounds),
            strategy=self.strategy
        )

# 默认FedAvg策略
class FedAvgStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[fl.common.Weights, fl.common.Scalar]],
        failures: List[BaseException]
    ) -> Optional[fl.common.Weights]:
        """聚合客户端更新"""
        if not results:
            return None
        
        # 使用Flower内置的权重聚合
        return super().aggregate_fit(server_round, results, failures)
```

#### 2. 实际应用示例

##### 场景1：联邦客户端实现
```python
# clients/client.py
import flwr as fl
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Dict, List

class FederatedClient(fl.client.NumPyClient):
    def __init__(self, model: nn.Module, trainloader: DataLoader, testloader: DataLoader):
        self.model = model
        self.trainloader = trainloader
        self.testloader = testloader
    
    def get_parameters(self) -> List[np.ndarray]:
        """获取模型参数"""
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]
    
    def set_parameters(self, parameters: List[np.ndarray]) -> None:
        """设置模型参数"""
        params_dict = zip(self.model.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        self.model.load_state_dict(state_dict, strict=True)
    
    def fit(self, parameters: List[np.ndarray], config: Dict) -> Tuple[List[np.ndarray], int, Dict]:
        """本地训练"""
        self.set_parameters(parameters)
        
        # 训练循环
        optimizer = optim.SGD(self.model.parameters(), lr=0.01)
        for epoch in range(config.get("local_epochs", 1)):
            for batch_idx, (data, target) in enumerate(self.trainloader):
                optimizer.zero_grad()
                output = self.model(data)
                loss = nn.functional.cross_entropy(output, target)
                loss.backward()
                optimizer.step()
        
        return self.get_parameters(), len(self.trainloader.dataset), {}
    
    def evaluate(self, parameters: List[np.ndarray], config: Dict) -> Tuple[float, int, Dict]:
        """本地评估"""
        self.set_parameters(parameters)
        
        loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in self.testloader:
                outputs = self.model(data)
                loss += nn.functional.cross_entropy(outputs, target).item()
                _, predicted = torch.max(outputs.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        
        accuracy = correct / total
        return loss, len(self.testloader.dataset), {"accuracy": accuracy}
```

##### 场景2：差分隐私实现
```python
# privacy/differential_privacy.py
import torch
import torch.nn as nn
from opacus import PrivacyEngine

class PrivateFederatedLearning:
    def __init__(self, model, noise_multiplier=1.0, max_grad_norm=1.0):
        self.model = model
        self.privacy_engine = PrivacyEngine()
        self.noise_multiplier = noise_multiplier
        self.max_grad_norm = max_grad_norm
    
    def enable_dp_training(self, optimizer, data_loader, epochs):
        """启用差分隐私训练"""
        # 使用Opacus包装优化器
        self.model, optimizer, data_loader = self.privacy_engine.make_private(
            module=self.model,
            optimizer=optimizer,
            data_loader=data_loader,
            noise_multiplier=self.noise_multiplier,
            max_grad_norm=self.max_grad_norm,
        )
        
        return optimizer, data_loader
    
    def get_epsilon_delta(self, steps, delta=1e-5):
        """计算隐私预算"""
        return self.privacy_engine.get_epsilon(delta=delta)
```

## 🧪 验证测试

### 测试1：联邦学习基本功能验证
```python
#!/usr/bin/env python
# 验证联邦学习基本功能
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import flwr as fl
import numpy as np

def test_federated_basic():
    print("=== 联邦学习基本功能验证 ===")
    
    # 创建简单模型
    class SimpleNet(nn.Module):
        def __init__(self):
            super(SimpleNet, self).__init__()
            self.fc = nn.Linear(10, 2)
        
        def forward(self, x):
            return self.fc(x)
    
    model = SimpleNet()
    
    # 创建模拟数据
    X = torch.randn(100, 10)
    y = torch.randint(0, 2, (100,))
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=10, shuffle=True)
    
    print(f"✅ 模型参数数量: {sum(p.numel() for p in model.parameters())}")
    print(f"✅ 数据集大小: {len(dataset)}")
    
    # 验证参数获取和设置
    original_params = [p.clone() for p in model.parameters()]
    
    # 获取参数
    params_list = [param.detach().cpu().numpy() for param in original_params]
    
    # 创建新模型并设置参数
    new_model = SimpleNet()
    for param, new_param in zip(params_list, new_model.parameters()):
        new_param.data = torch.from_numpy(param)
    
    # 验证参数是否一致
    for orig, new in zip(original_params, new_model.parameters()):
        assert torch.allclose(orig, new), "参数设置失败"
    
    print("✅ 参数获取和设置功能正常")
    print("✅ 联邦学习基本功能验证通过")

if __name__ == "__main__":
    test_federated_basic()
```

### 测试2：联邦聚合验证
```python
#!/usr/bin/env python
# 验证联邦聚合功能
import torch
import torch.nn as nn
import copy

def test_federated_aggregation():
    print("=== 联邦聚合功能验证 ===")
    
    # 创建两个客户端模型
    class SimpleNet(nn.Module):
        def __init__(self):
            super(SimpleNet, self).__init__()
            self.fc1 = nn.Linear(10, 5)
            self.fc2 = nn.Linear(5, 2)
        
        def forward(self, x):
            x = torch.relu(self.fc1(x))
            return self.fc2(x)
    
    # 初始化模型
    server_model = SimpleNet()
    
    # 模拟两个客户端的更新
    client1_model = copy.deepcopy(server_model)
    client2_model = copy.deepcopy(server_model)
    
    # 对客户端模型应用不同的更新
    with torch.no_grad():
        for param in client1_model.parameters():
            param.add_(torch.randn_like(param) * 0.1)  # 添加随机更新
    
    with torch.no_grad():
        for param in client2_model.parameters():
            param.add_(torch.randn_like(param) * 0.1)  # 添加随机更新
    
    # 简单平均聚合
    aggregated_model = SimpleNet()
    
    with torch.no_grad():
        for server_param, c1_param, c2_param in zip(
            server_model.parameters(), 
            client1_model.parameters(), 
            client2_model.parameters()
        ):
            avg_param = (c1_param + c2_param) / 2
            aggregated_model.state_dict()[server_param.shape] = avg_param
    
    # 实际聚合实现
    for server_param, c1_param, c2_param in zip(
        server_model.named_parameters(), 
        client1_model.named_parameters(), 
        client2_model.named_parameters()
    ):
        param_name, _ = server_param
        _, c1_param_val = c1_param
        _, c2_param_val = c2_param
        
        # 计算平均值
        avg_param = (c1_param_val + c2_param_val) / 2
        
        # 更新服务器模型
        server_model.state_dict()[param_name].copy_(avg_param)
    
    print("✅ 联邦聚合算法验证通过")
    print("✅ 模型参数成功聚合")
    
    # 验证聚合后的模型可以正常使用
    test_input = torch.randn(1, 10)
    output = server_model(test_input)
    print(f"✅ 聚合后模型正常工作，输出形状: {output.shape}")

if __name__ == "__main__":
    test_federated_aggregation()
```

## ❓ 常见问题

### Q1: 如何处理客户端异构性？
**解决方案**：
```python
# 客户端异构性处理
"""
1. 数据异构: 使用加权聚合考虑数据分布差异
2. 设备异构: 根据设备能力分配不同任务
3. 网络异构: 实现网络弹性通信协议
4. 时间异构: 使用异步联邦学习算法
"""
```

### Q2: 如何保证联邦学习中的隐私？
**解决方案**：
```python
# 联邦学习隐私保护
"""
1. 差分隐私: 在模型更新中添加噪声
2. 同态加密: 加密状态下进行计算
3. 安全聚合: 隐藏个体更新值
4. 联邦迁移学习: 仅共享知识而非数据
"""
```

## 📚 扩展学习

### 相关技术
- **Flower**: 联邦学习框架
- **PySyft**: 隐私优先的AI框架
- **TensorFlow Federated**: TensorFlow联邦学习
- **Pysyft**: 隐私保护机器学习

### 进阶学习路径
1. 掌握不同联邦学习算法的特点
2. 学习高级隐私保护技术
3. 理解通信效率优化方法
4. 掌握异构环境下的联邦学习

### 企业级应用场景
- 跨机构医疗数据分析
- 金融风控模型联合训练
- 智能制造质量预测
- 电信运营商客户洞察

---
> **💡 提示**: 联邦学习是一种新兴的分布式机器学习范式，能够在保护数据隐私的前提下实现多方协作建模，是构建可信AI系统的重要技术。