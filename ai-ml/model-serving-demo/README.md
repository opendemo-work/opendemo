# AI模型部署与推理服务实战演示

## 🎯 学习目标

通过本案例你将掌握：
- AI模型部署的最佳实践和架构模式
- 模型版本管理和A/B测试策略
- 批量推理和实时推理优化技术
- 模型服务的监控和弹性伸缩

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- Docker环境
- Kubernetes集群（可选，用于生产部署）

### 依赖安装
```bash
pip install torch transformers scikit-learn
pip install fastapi uvicorn gunicorn  # Web框架
pip install celery redis  # 异步任务处理
pip install prometheus-client  # 监控
pip install pytest  # 测试工具
```

## 📁 项目结构

```
model-serving-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── api/                               # API服务
│   ├── main.py                        # 主服务入口
│   ├── inference.py                   # 推理端点
│   ├── model_management.py            # 模型管理
│   └── health_check.py                # 健康检查
├── configs/                           # 配置文件
│   ├── serving_config.yaml            # 服务配置
│   ├── model_registry.json            # 模型注册表
│   └── deployment_config.yaml         # 部署配置
├── models/                            # 模型文件
│   ├── registry/                      # 模型注册表
│   ├── versions/                      # 版本管理
│   └── artifacts/                     # 模型制品
├── serving/                           # 推理服务
│   ├── sync_inference.py              # 同步推理
│   ├── async_inference.py             # 异步推理
│   ├── batch_inference.py             # 批量推理
│   └── streaming_inference.py         # 流式推理
├── deployment/                        # 部署配置
│   ├── docker/                        # Docker配置
│   │   ├── Dockerfile                 # 服务镜像
│   │   └── docker-compose.yml         # Compose配置
│   ├── kubernetes/                    # Kubernetes配置
│   │   ├── deployment.yaml            # 部署定义
│   │   ├── service.yaml               # 服务定义
│   │   └── hpa.yaml                   # 自动伸缩
│   └── helm/                          # Helm Chart
├── monitoring/                        # 监控配置
│   ├── metrics.py                     # 指标收集
│   ├── prometheus.yml                 # Prometheus配置
│   └── grafana_dashboards/            # Grafana仪表板
├── tests/                             # 测试文件
│   ├── integration_tests.py           # 集成测试
│   ├── performance_tests.py           # 性能测试
│   └── load_tests.py                  # 负载测试
└── notebooks/                         # Jupyter笔记本
    ├── 01_model_serving_patterns.ipynb  # 服务模式
    ├── 02_batch_vs_realtime.ipynb       # 批量vs实时
    └── 03_scalability_testing.ipynb     # 可扩展性测试
```

## 🚀 快速开始

### 步骤1：环境设置

```bash
# 安装模型服务相关依赖
pip install -r requirements.txt

# 启动Redis（用于异步任务）
docker run -d --name redis -p 6379:6379 redis:alpine
```

### 步骤2：启动模型服务

```bash
# 启动API服务
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# 或使用Gunicorn进行生产部署
gunicorn api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 步骤3：部署到Kubernetes

```bash
# 构建Docker镜像
docker build -t model-serving-service:latest .

# 部署到Kubernetes
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service.yaml
kubectl apply -f deployment/kubernetes/hpa.yaml
```

## 🔍 代码详解

### 核心概念解析

#### 1. 模型服务API实现
```python
# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import torch
import pickle
import time
from prometheus_client import Counter, Histogram

# 定义指标
inference_requests_total = Counter('inference_requests_total', 'Total inference requests', ['model_name'])
inference_duration = Histogram('inference_duration_seconds', 'Time spent on inference')

app = FastAPI(title="Model Serving API", version="1.0.0")

class PredictionRequest(BaseModel):
    inputs: List[float]
    model_version: Optional[str] = "latest"

class PredictionResponse(BaseModel):
    prediction: float
    model_version: str
    processing_time: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """模型推理端点"""
    start_time = time.time()
    
    try:
        # 获取模型（简化实现）
        model = load_model(request.model_version)
        
        # 执行推理
        inputs_tensor = torch.tensor(request.inputs).unsqueeze(0)
        with torch.no_grad():
            prediction = model(inputs_tensor).item()
        
        processing_time = time.time() - start_time
        
        # 记录指标
        inference_requests_total.labels(model_name=request.model_version).inc()
        inference_duration.observe(processing_time)
        
        return PredictionResponse(
            prediction=prediction,
            model_version=request.model_version,
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def load_model(version: str):
    """加载指定版本的模型"""
    # 这里应该是从模型注册表加载模型的逻辑
    model_path = f"models/versions/{version}/model.pkl"
    with open(model_path, 'rb') as f:
        return pickle.load(f)
```

#### 2. 实际应用示例

##### 场景1：批量推理服务
```python
# serving/batch_inference.py
from celery import Celery
from typing import List
import numpy as np

# 配置Celery
celery_app = Celery('model_serving', broker='redis://localhost:6379')

@celery_app.task
def batch_predict(model_version: str, inputs: List[List[float]]) -> List[float]:
    """批量推理任务"""
    # 加载模型
    model = load_model(model_version)
    
    # 转换为tensor
    inputs_tensor = torch.tensor(inputs, dtype=torch.float32)
    
    # 批量推理
    with torch.no_grad():
        predictions = model(inputs_tensor)
    
    return predictions.numpy().tolist()

class BatchInferenceService:
    def __init__(self):
        self.batch_size = 32
        self.batch_buffer = []
        self.processing_queue = []
    
    def add_to_batch(self, inputs: List[float], callback_url: str = None):
        """添加到批处理队列"""
        self.batch_buffer.append({
            'inputs': inputs,
            'callback_url': callback_url,
            'timestamp': time.time()
        })
        
        # 如果达到批处理大小，提交批处理
        if len(self.batch_buffer) >= self.batch_size:
            self.submit_batch()
    
    def submit_batch(self):
        """提交批处理任务"""
        if not self.batch_buffer:
            return
        
        batch_inputs = [item['inputs'] for item in self.batch_buffer]
        
        # 异步执行批处理
        task = batch_predict.delay('latest', batch_inputs)
        
        # 记录批处理信息
        batch_info = {
            'task_id': task.id,
            'size': len(batch_inputs),
            'submitted_at': time.time(),
            'callbacks': [item['callback_url'] for item in self.batch_buffer]
        }
        
        self.processing_queue.append(batch_info)
        self.batch_buffer.clear()
```

##### 场景2：模型版本管理和A/B测试
```python
# api/model_management.py
from enum import Enum
from typing import Dict, Any
import threading

class ModelStatus(Enum):
    LOADING = "loading"
    LOADED = "loaded"
    SERVING = "serving"
    FAILED = "failed"

class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.RLock()
    
    def register_model(self, name: str, version: str, path: str, metadata: Dict = None):
        """注册模型"""
        with self.lock:
            if name not in self.models:
                self.models[name] = {}
            
            self.models[name][version] = {
                'path': path,
                'status': ModelStatus.LOADING,
                'metadata': metadata or {},
                'created_at': time.time(),
                'model_instance': None
            }
    
    def load_model(self, name: str, version: str = 'latest'):
        """加载模型到内存"""
        with self.lock:
            if name not in self.models:
                raise ValueError(f"Model {name} not found")
            
            if version == 'latest':
                # 获取最新版本
                versions = list(self.models[name].keys())
                version = sorted(versions, reverse=True)[0]
            
            if version not in self.models[name]:
                raise ValueError(f"Version {version} of model {name} not found")
            
            model_info = self.models[name][version]
            
            if model_info['status'] == ModelStatus.LOADED:
                return model_info['model_instance']
            
            # 加载模型
            try:
                with open(model_info['path'], 'rb') as f:
                    model_instance = pickle.load(f)
                
                model_info['model_instance'] = model_instance
                model_info['status'] = ModelStatus.LOADED
                
                return model_instance
            except Exception as e:
                model_info['status'] = ModelStatus.FAILED
                raise e

class ABTestRouter:
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.traffic_split = {'model_v1': 0.5, 'model_v2': 0.5}  # 50/50分流
    
    def route_request(self, request_data: Any) -> str:
        """根据A/B测试配置路由请求"""
        import random
        
        rand_val = random.random()
        cumulative_prob = 0.0
        
        for model_name, prob in self.traffic_split.items():
            cumulative_prob += prob
            if rand_val <= cumulative_prob:
                return model_name
        
        # 默认返回第一个模型
        return list(self.traffic_split.keys())[0]
```

## 🧪 验证测试

### 测试1：模型服务功能验证
```python
#!/usr/bin/env python
# 验证模型服务功能
import asyncio
import aiohttp
import time
import numpy as np

async def test_model_serving():
    print("=== 模型服务功能验证 ===")
    
    # 模拟模型输入
    test_inputs = np.random.rand(10).tolist()
    
    # 发送推理请求
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/predict"
        payload = {
            "inputs": test_inputs,
            "model_version": "latest"
        }
        
        try:
            start_time = time.time()
            async with session.post(url, json=payload) as response:
                result = await response.json()
                elapsed_time = time.time() - start_time
            
            print(f"✅ 推理请求成功")
            print(f"输入: {test_inputs[:3]}... (共{len(test_inputs)}个特征)")
            print(f"预测结果: {result['prediction']}")
            print(f"模型版本: {result['model_version']}")
            print(f"处理时间: {elapsed_time:.4f}s")
            
        except Exception as e:
            print(f"❌ 推理请求失败: {e}")
            print("请确保模型服务正在运行 (uvicorn api.main:app --host 0.0.0.0 --port 8000)")

if __name__ == "__main__":
    asyncio.run(test_model_serving())
```

### 测试2：批量推理性能验证
```python
#!/usr/bin/env python
# 验证批量推理性能
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import asyncio

def simulate_single_inference(inputs):
    """模拟单次推理"""
    # 模拟推理延迟
    time.sleep(0.01)
    return sum(inputs) / len(inputs)  # 简单的计算

def test_batch_vs_single_performance():
    print("=== 批量vs单次推理性能验证 ===")
    
    # 生成测试数据
    num_requests = 100
    test_inputs = [np.random.rand(10).tolist() for _ in range(num_requests)]
    
    # 测试单次推理性能
    start_time = time.time()
    single_results = []
    for inputs in test_inputs:
        result = simulate_single_inference(inputs)
        single_results.append(result)
    single_time = time.time() - start_time
    
    # 测试批量推理性能（模拟）
    start_time = time.time()
    # 模拟批量处理 - 一次处理所有输入
    batch_result = [sum(inputs) / len(inputs) for inputs in test_inputs]
    batch_time = time.time() - start_time
    
    print(f"✅ 性能对比结果:")
    print(f"单次推理总时间: {single_time:.4f}s")
    print(f"批量推理总时间: {batch_time:.4f}s")
    print(f"性能提升倍数: {single_time/batch_time:.2f}x")
    print(f"处理请求数量: {num_requests}")
    
    # 验证结果一致性
    results_match = all(abs(a - b) < 1e-10 for a, b in zip(single_results, batch_result))
    print(f"结果一致性: {'✅' if results_match else '❌'}")

if __name__ == "__main__":
    test_batch_vs_single_performance()
```

## ❓ 常见问题

### Q1: 如何处理模型服务的高并发请求？
**解决方案**：
```python
# 高并发处理策略
"""
1. 异步处理: 使用FastAPI和async/await
2. 连接池: 配置数据库和外部服务连接池
3. 缓存: 使用Redis缓存频繁请求的结果
4. 负载均衡: 使用多实例和负载均衡器
"""
```

### Q2: 如何实现模型的零停机更新？
**解决方案**：
```python
# 零停机更新策略
"""
1. 蓝绿部署: 维护两套环境交替更新
2. 滚动更新: 逐步替换旧实例
3. A/B测试: 逐步转移流量
4. 健康检查: 确保新版本正常工作
"""
```

## 📚 扩展学习

### 相关技术
- **TorchServe**: PyTorch模型服务
- **TF-Serving**: TensorFlow模型服务
- **Seldon**: Kubernetes原生模型服务
- **KServe**: Kubeflow模型服务

### 进阶学习路径
1. 掌握不同模型服务框架的特点
2. 学习容器化部署最佳实践
3. 理解服务网格在模型部署中的应用
4. 掌握自动扩缩容和弹性伸缩

### 企业级应用场景
- 高可用模型服务架构
- 多模型版本管理
- A/B测试和实验平台
- 模型性能监控和告警

---
> **💡 提示**: AI模型部署是连接模型开发和实际应用的关键环节，需要综合考虑性能、可扩展性、可靠性和维护性等多个方面，是现代AI系统不可或缺的组成部分。