# 推理基础入门

## 1. 案例概述

本案例介绍Kubernetes环境下大模型推理服务的基础知识和实践操作，帮助初学者快速上手AI模型推理服务部署。

### 1.1 学习目标

- 理解大模型推理服务的基本概念和架构
- 掌握Kubernetes推理环境的搭建方法
- 学会部署基础的推理服务
- 了解模型转换和优化基础
- 掌握基本的推理服务监控方法

### 1.2 适用人群

- Kubernetes初学者
- 对AI推理服务感兴趣的开发者
- MLOps入门者
- 后端服务工程师

## 2. 环境准备

### 2.1 硬件要求

- CPU: 至少4核
- 内存: 至少16GB
- GPU: 至少1块NVIDIA GPU(推荐8GB显存以上)
- 存储: 至少200GB可用空间

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
  name: model-inference-basics
  labels:
    purpose: "model-inference-tutorial"
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: inference-quota
  namespace: model-inference-basics
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 16Gi
    requests.nvidia.com/gpu: "1"
    limits.cpu: "8"
    limits.memory: 32Gi
    limits.nvidia.com/gpu: "1"
```

## 3. 推理环境搭建

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

### 3.2 基础推理镜像准备

```dockerfile
# Dockerfile.inference-base
FROM nvidia/cuda:11.8-runtime-ubuntu20.04

# 安装基础依赖
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置Python环境
ENV PYTHONUNBUFFERED=1
WORKDIR /workspace

# 安装推理相关库
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制推理代码
COPY inference_server.py .
COPY models/ ./models/

# 暴露服务端口
EXPOSE 8080

CMD ["python3", "inference_server.py"]
```

对应的requirements.txt:
```txt
torch>=2.0.0
torchvision>=0.15.0
transformers>=4.30.0
fastapi>=0.95.0
uvicorn>=0.21.0
python-multipart>=0.0.6
numpy>=1.21.0
pillow>=9.0.0
```

## 4. 基础推理服务示例

### 4.1 图像分类推理服务

```python
# inference_server.py
import torch
from torchvision import models, transforms
from PIL import Image
import io
import uvicorn
from fastapi import FastAPI, File, UploadFile
import time

app = FastAPI(title="Image Classification Inference Service")

# 加载预训练模型
model = models.resnet50(pretrained=True)
model.eval()
model.cuda()

# 图像预处理
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                        std=[0.229, 0.224, 0.225]),
])

# ImageNet类别标签
with open('imagenet_classes.txt', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """图像分类预测"""
    start_time = time.time()
    
    # 读取并预处理图像
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    input_tensor = transform(image).unsqueeze(0).cuda()
    
    # 模型推理
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
    
    # 获取top-5预测结果
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    
    results = []
    for i in range(top5_prob.size(0)):
        results.append({
            "class": classes[top5_catid[i]],
            "probability": float(top5_prob[i].item()),
            "rank": i + 1
        })
    
    inference_time = time.time() - start_time
    
    return {
        "predictions": results,
        "inference_time": f"{inference_time:.4f}s",
        "image_size": f"{image.size[0]}x{image.size[1]}"
    }

@app.get("/model/info")
async def model_info():
    """模型信息"""
    return {
        "model_name": "ResNet50",
        "framework": "PyTorch",
        "input_shape": "224x224x3",
        "num_classes": 1000,
        "pretrained": True
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### 4.2 Kubernetes部署配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: image-classification-inference
  namespace: model-inference-basics
spec:
  replicas: 1
  selector:
    matchLabels:
      app: inference-service
  template:
    metadata:
      labels:
        app: inference-service
    spec:
      containers:
      - name: inference-container
        image: your-registry/image-classification-inference:latest
        ports:
        - containerPort: 8080
        env:
        - name: MODEL_PATH
          value: "/models/resnet50.pth"
        resources:
          requests:
            cpu: "2"
            memory: "4Gi"
            nvidia.com/gpu: "1"
          limits:
            cpu: "4"
            memory: "8Gi"
            nvidia.com/gpu: "1"
        volumeMounts:
        - name: model-storage
          mountPath: /models
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 30
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: inference-service
  namespace: model-inference-basics
spec:
  selector:
    app: inference-service
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-pvc
  namespace: model-inference-basics
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
```

## 5. 模型转换与优化

### 5.1 ONNX模型转换

```python
# model_conversion.py
import torch
import torch.onnx
from torchvision import models

def convert_to_onnx():
    """将PyTorch模型转换为ONNX格式"""
    # 加载模型
    model = models.resnet50(pretrained=True)
    model.eval()
    
    # 创建示例输入
    dummy_input = torch.randn(1, 3, 224, 224)
    
    # 导出ONNX模型
    torch.onnx.export(
        model,
        dummy_input,
        "resnet50.onnx",
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    
    print("ONNX模型转换完成: resnet50.onnx")

def optimize_onnx_model():
    """优化ONNX模型"""
    import onnx
    from onnxruntime.transformers import optimizer
    
    # 加载ONNX模型
    model = onnx.load("resnet50.onnx")
    
    # 优化模型
    optimized_model = optimizer.optimize_model(
        model,
        'bert',  # 使用BERT优化器作为示例
        num_heads=16,
        hidden_size=768
    )
    
    # 保存优化后的模型
    optimized_model.save_model_to_file("resnet50_optimized.onnx")
    print("ONNX模型优化完成: resnet50_optimized.onnx")

if __name__ == "__main__":
    convert_to_onnx()
    optimize_onnx_model()
```

### 5.2 TensorRT优化

```python
# tensorrt_optimization.py
import torch
import tensorrt as trt
import numpy as np

def build_tensorrt_engine():
    """构建TensorRT推理引擎"""
    # TRT Logger
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    
    # 创建Builder和Network
    builder = trt.Builder(TRT_LOGGER)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, TRT_LOGGER)
    
    # 解析ONNX模型
    with open("resnet50.onnx", "rb") as model:
        parser.parse(model.read())
    
    # 创建配置
    config = builder.create_builder_config()
    config.max_workspace_size = 1 << 30  # 1GB
    
    # 启用FP16精度
    if builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)
    
    # 构建引擎
    engine = builder.build_engine(network, config)
    
    # 保存引擎
    with open("resnet50.trt", "wb") as f:
        f.write(engine.serialize())
    
    print("TensorRT引擎构建完成: resnet50.trt")
    return engine

def tensorrt_inference(engine, input_data):
    """使用TensorRT引擎进行推理"""
    # 创建执行上下文
    context = engine.create_execution_context()
    
    # 分配输入输出内存
    inputs, outputs, bindings, stream = allocate_buffers(engine)
    
    # 复制输入数据
    np.copyto(inputs[0].host, input_data.ravel())
    
    # 执行推理
    trt_outputs = do_inference(context, bindings=bindings, inputs=inputs, 
                              outputs=outputs, stream=stream)
    
    return trt_outputs

if __name__ == "__main__":
    engine = build_tensorrt_engine()
```

## 6. 推理服务测试

### 6.1 服务调用脚本

```python
# test_inference.py
import requests
import json
from PIL import Image
import io

def test_image_classification():
    """测试图像分类推理服务"""
    # 服务地址
    service_url = "http://localhost:8080"
    
    # 测试图像
    test_image = "test_image.jpg"
    
    # 发送预测请求
    with open(test_image, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{service_url}/predict", files=files)
    
    # 解析响应
    if response.status_code == 200:
        result = response.json()
        print("预测结果:")
        for pred in result["predictions"]:
            print(f"  {pred['rank']}. {pred['class']}: {pred['probability']:.4f}")
        print(f"推理时间: {result['inference_time']}")
    else:
        print(f"请求失败: {response.status_code}")

def test_health_check():
    """测试健康检查"""
    service_url = "http://localhost:8080"
    response = requests.get(f"{service_url}/health")
    
    if response.status_code == 200:
        print("服务健康状态: OK")
        print(response.json())
    else:
        print(f"健康检查失败: {response.status_code}")

if __name__ == "__main__":
    test_health_check()
    test_image_classification()
```

### 6.2 性能基准测试

```python
# benchmark_inference.py
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import statistics

class InferenceBenchmark:
    def __init__(self, service_url, test_image_path):
        self.service_url = service_url
        self.test_image_path = test_image_path
        self.results = []
    
    def single_request(self):
        """发送单个推理请求"""
        start_time = time.time()
        
        with open(self.test_image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{self.service_url}/predict", files=files)
        
        end_time = time.time()
        latency = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            inference_time = float(result["inference_time"].replace("s", ""))
            return {
                "total_latency": latency,
                "inference_time": inference_time,
                "success": True
            }
        else:
            return {
                "total_latency": latency,
                "success": False
            }
    
    def benchmark_sequential(self, num_requests=100):
        """顺序基准测试"""
        print(f"开始顺序基准测试 ({num_requests}次请求)...")
        
        latencies = []
        for i in range(num_requests):
            result = self.single_request()
            if result["success"]:
                latencies.append(result["total_latency"])
            if (i + 1) % 10 == 0:
                print(f"已完成 {i + 1}/{num_requests} 次请求")
        
        self.print_statistics(latencies, "顺序测试")
    
    def benchmark_concurrent(self, num_requests=100, concurrency=10):
        """并发基准测试"""
        print(f"开始并发基准测试 ({num_requests}次请求, 并发数: {concurrency})...")
        
        def worker():
            return self.single_request()
        
        latencies = []
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(worker) for _ in range(num_requests)]
            
            for i, future in enumerate(futures):
                result = future.result()
                if result["success"]:
                    latencies.append(result["total_latency"])
                if (i + 1) % 10 == 0:
                    print(f"已完成 {i + 1}/{num_requests} 次请求")
        
        self.print_statistics(latencies, f"并发测试(并发数:{concurrency})")
    
    def print_statistics(self, latencies, test_type):
        """打印统计信息"""
        if not latencies:
            print(f"{test_type}: 无成功请求")
            return
        
        stats = {
            "平均延迟": statistics.mean(latencies),
            "中位数延迟": statistics.median(latencies),
            "95%分位数": statistics.quantiles(latencies, n=20)[-1],
            "最小延迟": min(latencies),
            "最大延迟": max(latencies),
            "标准差": statistics.stdev(latencies),
            "成功请求数": len(latencies)
        }
        
        print(f"\n{test_type}结果:")
        for key, value in stats.items():
            if "延迟" in key:
                print(f"  {key}: {value:.4f}秒")
            else:
                print(f"  {key}: {value}")

if __name__ == "__main__":
    benchmark = InferenceBenchmark(
        service_url="http://localhost:8080",
        test_image_path="test_image.jpg"
    )
    
    # 顺序测试
    benchmark.benchmark_sequential(num_requests=50)
    
    # 并发测试
    benchmark.benchmark_concurrent(num_requests=50, concurrency=5)
```

## 7. 监控与日志

### 7.1 基础监控配置

```yaml
# prometheus-monitoring.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: inference-monitor
  namespace: model-inference-basics
spec:
  selector:
    matchLabels:
      app: inference-service
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: inference-dashboard
  namespace: model-inference-basics
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Model Inference Service Dashboard",
        "panels": [
          {
            "title": "Request Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total[5m])",
                "legendFormat": "Requests/sec"
              }
            ]
          },
          {
            "title": "Latency Distribution",
            "type": "heatmap",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
                "legendFormat": "95th percentile"
              }
            ]
          },
          {
            "title": "Error Rate",
            "type": "stat",
            "targets": [
              {
                "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
                "legendFormat": "Error Rate"
              }
            ]
          }
        ]
      }
    }
```

这个基础入门案例为后续的进阶推理优化奠定了坚实的基础，包含了完整的环境搭建、服务部署、模型转换和性能测试流程。