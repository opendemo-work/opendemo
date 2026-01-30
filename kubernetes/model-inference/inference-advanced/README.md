# 推理进阶优化

## 1. 案例概述

本案例深入讲解Kubernetes环境下大模型推理服务的进阶优化技术，涵盖批量推理、流式处理、多模型服务等高级主题。

### 1.1 学习目标

- 掌握批量推理的优化策略和技术实现
- 理解流式推理处理的核心原理和应用场景
- 学会多模型并发服务的架构设计和部署
- 掌握推理服务的高级调度和资源管理
- 理解不同推理模式的适用场景和性能特点

### 1.2 适用人群

- 有一定推理服务基础的开发者
- 需要处理高并发推理请求的工程师
- 对推理服务性能优化有深入需求的技术人员
- MLOps工程师和AI平台架构师

## 2. 批量推理优化

### 2.1 动态批处理技术

```python
# dynamic_batching.py
import asyncio
import time
from typing import List, Dict, Any
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class DynamicBatchProcessor:
    def __init__(self, model_name: str, max_batch_size: int = 32, timeout_ms: int = 100):
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_batch_size = max_batch_size
        self.timeout_ms = timeout_ms
        self.request_queue = asyncio.Queue()
        self.batch_lock = asyncio.Lock()
        self.running = True
        
    async def add_request(self, prompt: str, max_length: int = 100) -> Dict[str, Any]:
        """添加推理请求到批处理队列"""
        request_id = str(time.time())
        future = asyncio.Future()
        
        await self.request_queue.put({
            'id': request_id,
            'prompt': prompt,
            'max_length': max_length,
            'future': future,
            'timestamp': time.time()
        })
        
        return await future
    
    async def batch_processor_loop(self):
        """批量处理循环"""
        while self.running:
            batch_requests = []
            
            # 收集批次请求
            try:
                # 等待第一个请求
                first_request = await asyncio.wait_for(
                    self.request_queue.get(), 
                    timeout=self.timeout_ms/1000.0
                )
                batch_requests.append(first_request)
                
                # 尝试收集更多请求形成批次
                while len(batch_requests) < self.max_batch_size:
                    try:
                        request = self.request_queue.get_nowait()
                        batch_requests.append(request)
                    except asyncio.QueueEmpty:
                        break
                        
            except asyncio.TimeoutError:
                # 超时但队列为空，继续等待
                continue
            
            if batch_requests:
                await self.process_batch(batch_requests)
    
    async def process_batch(self, requests: List[Dict]):
        """处理批量请求"""
        try:
            # 准备批量输入
            prompts = [req['prompt'] for req in requests]
            max_lengths = [req['max_length'] for req in requests]
            
            # Tokenize批量输入
            inputs = self.tokenizer(
                prompts, 
                return_tensors="pt", 
                padding=True, 
                truncation=True
            )
            
            # 模型推理
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max(max_lengths),
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # 处理输出结果
            for i, request in enumerate(requests):
                try:
                    # 解码对应请求的输出
                    output_tokens = outputs[i][inputs['input_ids'].shape[1]:]
                    result_text = self.tokenizer.decode(output_tokens, skip_special_tokens=True)
                    
                    request['future'].set_result({
                        'result': result_text,
                        'request_id': request['id'],
                        'processing_time': time.time() - request['timestamp']
                    })
                except Exception as e:
                    request['future'].set_exception(e)
                    
        except Exception as e:
            # 批量处理失败，逐个返回错误
            for request in requests:
                request['future'].set_exception(e)

# 使用示例
async def main():
    processor = DynamicBatchProcessor("gpt2", max_batch_size=8, timeout_ms=50)
    
    # 启动批处理循环
    batch_task = asyncio.create_task(processor.batch_processor_loop())
    
    # 发送多个并发请求
    tasks = []
    for i in range(20):
        task = asyncio.create_task(
            processor.add_request(f"Translate to French: Hello world {i}")
        )
        tasks.append(task)
    
    # 等待所有结果
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 处理结果
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Request {i} failed: {result}")
        else:
            print(f"Request {i}: {result['result']}")
    
    # 停止处理器
    processor.running = False
    await batch_task

if __name__ == "__main__":
    asyncio.run(main())
```

### 2.2 Kubernetes批量推理部署

```yaml
# batch-inference-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-inference-service
  namespace: model-inference-advanced
spec:
  replicas: 3
  selector:
    matchLabels:
      app: batch-inference
  template:
    metadata:
      labels:
        app: batch-inference
    spec:
      containers:
      - name: batch-inference-container
        image: your-registry/batch-inference-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: MAX_BATCH_SIZE
          value: "16"
        - name: BATCH_TIMEOUT_MS
          value: "100"
        - name: MODEL_NAME
          value: "gpt2"
        resources:
          requests:
            cpu: "4"
            memory: "16Gi"
            nvidia.com/gpu: "1"
          limits:
            cpu: "8"
            memory: "32Gi"
            nvidia.com/gpu: "1"
        volumeMounts:
        - name: model-cache
          mountPath: /models
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 120
          periodSeconds: 30
      volumes:
      - name: model-cache
        persistentVolumeClaim:
          claimName: model-cache-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: batch-inference-service
  namespace: model-inference-advanced
spec:
  selector:
    app: batch-inference
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: batch-inference-hpa
  namespace: model-inference-advanced
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: batch-inference-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: queue_length
      target:
        type: AverageValue
        averageValue: "50"
```

## 3. 流式推理处理

### 3.1 流式推理服务器

```python
# streaming_inference.py
import asyncio
import json
from typing import AsyncGenerator
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI(title="Streaming Inference Service")

class StreamingInferenceService:
    def __init__(self, model_name: str):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    async def stream_generate(self, prompt: str, max_length: int = 200) -> AsyncGenerator[str, None]:
        """流式生成文本"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        
        # 创建流式处理器
        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True
        )
        
        # 生成参数
        generation_kwargs = dict(
            inputs,
            streamer=streamer,
            max_new_tokens=max_length,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # 在后台线程中运行生成
        from threading import Thread
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        
        # 流式返回结果
        for new_text in streamer:
            yield new_text
            # 添加小延迟以模拟真实流式体验
            await asyncio.sleep(0.01)

# 初始化服务
service = StreamingInferenceService("gpt2")

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket流式推理端点"""
    await websocket.accept()
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            request = json.loads(data)
            
            prompt = request.get("prompt", "")
            max_length = request.get("max_length", 100)
            
            # 流式生成并发送结果
            async for token in service.stream_generate(prompt, max_length):
                response = {
                    "token": token,
                    "finished": False
                }
                await websocket.send_text(json.dumps(response))
            
            # 发送结束标记
            await websocket.send_text(json.dumps({
                "token": "",
                "finished": True
            }))
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error in streaming: {e}")
        await websocket.close()

@app.post("/stream/http")
async def http_stream(request: dict):
    """HTTP流式推理端点"""
    prompt = request.get("prompt", "")
    max_length = request.get("max_length", 100)
    
    async def generate_stream():
        async for token in service.stream_generate(prompt, max_length):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield f"data: {json.dumps({'token': '', 'finished': True})}\n\n"
    
    return StreamingResponse(generate_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### 3.2 流式推理客户端

```python
# streaming_client.py
import asyncio
import aiohttp
import json
import websockets

class StreamingClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    async def websocket_stream(self, prompt: str, max_length: int = 100):
        """WebSocket流式推理"""
        uri = f"ws://{self.base_url.replace('http://', '')}/ws/stream"
        
        async with websockets.connect(uri) as websocket:
            # 发送请求
            request = {
                "prompt": prompt,
                "max_length": max_length
            }
            await websocket.send(json.dumps(request))
            
            # 接收流式响应
            full_response = ""
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                
                if data.get("finished"):
                    break
                    
                token = data.get("token", "")
                full_response += token
                print(token, end="", flush=True)
            
            print()  # 换行
            return full_response
    
    async def http_stream(self, prompt: str, max_length: int = 100):
        """HTTP流式推理"""
        url = f"{self.base_url}/stream/http"
        data = {
            "prompt": prompt,
            "max_length": max_length
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                full_response = ""
                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])  # 移除 'data: ' 前缀
                            token = data.get("token", "")
                            
                            if data.get("finished"):
                                break
                                
                            full_response += token
                            print(token, end="", flush=True)
                        except json.JSONDecodeError:
                            continue
                
                print()  # 换行
                return full_response

# 使用示例
async def main():
    client = StreamingClient("http://localhost:8080")
    
    prompt = "Write a story about artificial intelligence: "
    
    print("=== WebSocket Stream ===")
    result1 = await client.websocket_stream(prompt, max_length=200)
    
    print("\n=== HTTP Stream ===")
    result2 = await client.http_stream(prompt, max_length=200)
    
    print(f"\nWebSocket result length: {len(result1)}")
    print(f"HTTP result length: {len(result2)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 4. 多模型服务架构

### 4.1 多模型管理器

```python
# multi_model_manager.py
import asyncio
import torch
from typing import Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
import time

class ModelInstance:
    def __init__(self, model_name: str, device: str = "cuda"):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.tokenizer = None
        self.load_time = None
        self.last_used = time.time()
        self.request_count = 0
        
    async def load(self):
        """加载模型"""
        print(f"Loading model: {self.model_name}")
        start_time = time.time()
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        self.load_time = time.time() - start_time
        print(f"Model {self.model_name} loaded in {self.load_time:.2f}s")
        
    def unload(self):
        """卸载模型"""
        if self.model:
            del self.model
            self.model = None
        if self.tokenizer:
            del self.tokenizer
            self.tokenizer = None
        torch.cuda.empty_cache()

class MultiModelManager:
    def __init__(self, max_models: int = 3, ttl_seconds: int = 3600):
        self.max_models = max_models
        self.ttl_seconds = ttl_seconds
        self.models: Dict[str, ModelInstance] = {}
        self.lock = asyncio.Lock()
        
    async def get_model(self, model_name: str) -> ModelInstance:
        """获取模型实例"""
        async with self.lock:
            # 如果模型已加载，直接返回
            if model_name in self.models:
                model_instance = self.models[model_name]
                model_instance.last_used = time.time()
                model_instance.request_count += 1
                return model_instance
            
            # 如果达到最大模型数，移除最久未使用的模型
            if len(self.models) >= self.max_models:
                self._evict_least_recently_used()
            
            # 创建并加载新模型
            model_instance = ModelInstance(model_name)
            await model_instance.load()
            self.models[model_name] = model_instance
            model_instance.request_count += 1
            
            return model_instance
    
    def _evict_least_recently_used(self):
        """移除最久未使用的模型"""
        if not self.models:
            return
            
        oldest_model = min(
            self.models.items(),
            key=lambda x: x[1].last_used
        )
        
        print(f"Evicting model: {oldest_model[0]}")
        oldest_model[1].unload()
        del self.models[oldest_model[0]]
    
    async def cleanup_expired_models(self):
        """清理过期模型"""
        current_time = time.time()
        expired_models = []
        
        async with self.lock:
            for model_name, model_instance in self.models.items():
                if current_time - model_instance.last_used > self.ttl_seconds:
                    expired_models.append(model_name)
            
            for model_name in expired_models:
                print(f"Cleaning up expired model: {model_name}")
                self.models[model_name].unload()
                del self.models[model_name]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取管理器统计信息"""
        return {
            "loaded_models": len(self.models),
            "max_models": self.max_models,
            "model_details": {
                name: {
                    "load_time": instance.load_time,
                    "last_used": instance.last_used,
                    "request_count": instance.request_count
                }
                for name, instance in self.models.items()
            }
        }

# 使用示例
async def main():
    manager = MultiModelManager(max_models=2, ttl_seconds=300)
    
    # 测试多模型推理
    models_to_test = ["gpt2", "distilgpt2"]
    
    for model_name in models_to_test:
        print(f"\n--- Testing {model_name} ---")
        model_instance = await manager.get_model(model_name)
        
        # 执行推理
        inputs = model_instance.tokenizer(
            "Hello, how are you?",
            return_tensors="pt"
        ).to("cuda")
        
        with torch.no_grad():
            outputs = model_instance.model.generate(
                **inputs,
                max_new_tokens=50,
                pad_token_id=model_instance.tokenizer.eos_token_id
            )
        
        result = model_instance.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
        print(f"Result: {result}")
    
    # 显示统计信息
    stats = manager.get_stats()
    print(f"\nManager Stats: {stats}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 4.2 多模型服务部署

```yaml
# multi-model-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multi-model-inference
  namespace: model-inference-advanced
spec:
  replicas: 2
  selector:
    matchLabels:
      app: multi-model-inference
  template:
    metadata:
      labels:
        app: multi-model-inference
    spec:
      containers:
      - name: multi-model-container
        image: your-registry/multi-model-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: MAX_CONCURRENT_MODELS
          value: "3"
        - name: MODEL_TTL_SECONDS
          value: "1800"
        - name: PRELOAD_MODELS
          value: "gpt2,distilgpt2"
        resources:
          requests:
            cpu: "8"
            memory: "32Gi"
            nvidia.com/gpu: "2"
          limits:
            cpu: "16"
            memory: "64Gi"
            nvidia.com/gpu: "2"
        volumeMounts:
        - name: model-cache
          mountPath: /models
        - name: shm-volume
          mountPath: /dev/shm
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 120
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 180
          periodSeconds: 30
      volumes:
      - name: model-cache
        persistentVolumeClaim:
          claimName: model-cache-pvc
      - name: shm-volume
        emptyDir:
          medium: Memory
          sizeLimit: 4Gi
---
apiVersion: v1
kind: Service
metadata:
  name: multi-model-service
  namespace: model-inference-advanced
spec:
  selector:
    app: multi-model-inference
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

## 5. 高级调度策略

### 5.1 智能负载均衡

```python
# intelligent_load_balancer.py
import asyncio
import time
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ServerStats:
    endpoint: str
    current_load: float
    response_time: float
    error_rate: float
    last_update: float

class IntelligentLoadBalancer:
    def __init__(self, servers: List[str]):
        self.servers = servers
        self.server_stats: Dict[str, ServerStats] = {}
        self.update_interval = 5.0  # 秒
        self.running = True
        
        # 初始化服务器统计
        for server in servers:
            self.server_stats[server] = ServerStats(
                endpoint=server,
                current_load=0.0,
                response_time=0.0,
                error_rate=0.0,
                last_update=time.time()
            )
    
    def get_best_server(self, request_type: str = "normal") -> str:
        """根据请求类型选择最佳服务器"""
        if request_type == "urgent":
            return self._get_lowest_latency_server()
        elif request_type == "batch":
            return self._get_lowest_load_server()
        else:
            return self._get_weighted_best_server()
    
    def _get_lowest_latency_server(self) -> str:
        """选择延迟最低的服务器"""
        valid_servers = self._get_valid_servers()
        if not valid_servers:
            return random.choice(self.servers)
        
        return min(valid_servers, key=lambda s: self.server_stats[s].response_time)
    
    def _get_lowest_load_server(self) -> str:
        """选择负载最低的服务器"""
        valid_servers = self._get_valid_servers()
        if not valid_servers:
            return random.choice(self.servers)
        
        return min(valid_servers, key=lambda s: self.server_stats[s].current_load)
    
    def _get_weighted_best_server(self) -> str:
        """基于加权算法选择服务器"""
        valid_servers = self._get_valid_servers()
        if not valid_servers:
            return random.choice(self.servers)
        
        # 计算每个服务器的综合得分
        scores = {}
        for server in valid_servers:
            stats = self.server_stats[server]
            # 综合得分 = 负载权重 + 延迟权重 + 错误率惩罚
            score = (
                stats.current_load * 0.5 +
                stats.response_time * 0.3 +
                stats.error_rate * 10.0
            )
            scores[server] = score
        
        # 选择得分最低的服务器
        return min(scores.items(), key=lambda x: x[1])[0]
    
    def _get_valid_servers(self) -> List[str]:
        """获取有效的服务器列表（剔除长时间未更新的）"""
        current_time = time.time()
        valid_servers = []
        
        for server, stats in self.server_stats.items():
            if current_time - stats.last_update < 30:  # 30秒内更新过的才算有效
                valid_servers.append(server)
        
        return valid_servers
    
    async def update_server_stats(self, server: str, response_time: float, success: bool):
        """更新服务器统计数据"""
        if server not in self.server_stats:
            return
            
        stats = self.server_stats[server]
        stats.last_update = time.time()
        
        # 更新响应时间（指数移动平均）
        if stats.response_time == 0:
            stats.response_time = response_time
        else:
            stats.response_time = stats.response_time * 0.9 + response_time * 0.1
        
        # 更新错误率
        if success:
            if stats.error_rate > 0:
                stats.error_rate = max(0, stats.error_rate - 0.01)
        else:
            stats.error_rate = min(1.0, stats.error_rate + 0.1)
    
    async def monitor_loop(self):
        """监控循环"""
        while self.running:
            await self._update_load_metrics()
            await asyncio.sleep(self.update_interval)
    
    async def _update_load_metrics(self):
        """更新负载指标"""
        # 这里可以集成实际的监控系统
        # 模拟负载更新
        for server in self.servers:
            if server in self.server_stats:
                # 模拟负载波动
                current_load = random.uniform(0.1, 0.9)
                self.server_stats[server].current_load = current_load

# 使用示例
async def main():
    servers = [
        "http://inference-server-1:8080",
        "http://inference-server-2:8080",
        "http://inference-server-3:8080"
    ]
    
    balancer = IntelligentLoadBalancer(servers)
    monitor_task = asyncio.create_task(balancer.monitor_loop())
    
    # 模拟请求分发
    for i in range(20):
        request_type = random.choice(["normal", "urgent", "batch"])
        best_server = balancer.get_best_server(request_type)
        print(f"Request {i+1} ({request_type}): routed to {best_server}")
        
        # 模拟请求处理
        response_time = random.uniform(0.1, 2.0)
        success = random.random() > 0.1  # 90%成功率
        
        await balancer.update_server_stats(best_server, response_time, success)
        await asyncio.sleep(0.5)
    
    balancer.running = False
    await monitor_task

if __name__ == "__main__":
    asyncio.run(main())
```

## 6. 性能基准测试

### 6.1 批量推理性能测试

```python
# batch_performance_test.py
import asyncio
import time
import statistics
from typing import List, Dict
import aiohttp

class BatchPerformanceTester:
    def __init__(self, service_url: str):
        self.service_url = service_url
        self.results = []
    
    async def test_batch_performance(self, batch_sizes: List[int], num_requests: int = 10):
        """测试不同批次大小的性能"""
        async with aiohttp.ClientSession() as session:
            for batch_size in batch_sizes:
                print(f"\nTesting batch size: {batch_size}")
                
                batch_results = []
                for i in range(num_requests):
                    # 准备批次请求
                    prompts = [f"Test prompt {j}" for j in range(batch_size)]
                    
                    start_time = time.time()
                    try:
                        async with session.post(
                            f"{self.service_url}/batch_predict",
                            json={"prompts": prompts}
                        ) as response:
                            if response.status == 200:
                                await response.json()
                                end_time = time.time()
                                batch_results.append(end_time - start_time)
                            else:
                                print(f"Request failed with status: {response.status}")
                    except Exception as e:
                        print(f"Request error: {e}")
                
                if batch_results:
                    avg_time = statistics.mean(batch_results)
                    throughput = batch_size / avg_time if avg_time > 0 else 0
                    
                    print(f"  Average time: {avg_time:.4f}s")
                    print(f"  Throughput: {throughput:.2f} tokens/sec")
                    print(f"  Per-token time: {avg_time/batch_size:.4f}s")
                    
                    self.results.append({
                        "batch_size": batch_size,
                        "avg_time": avg_time,
                        "throughput": throughput,
                        "per_token_time": avg_time/batch_size
                    })

# 使用示例
async def main():
    tester = BatchPerformanceTester("http://localhost:8080")
    await tester.test_batch_performance([1, 4, 8, 16, 32], num_requests=5)
    
    # 输出结果摘要
    print("\n=== Performance Summary ===")
    for result in tester.results:
        print(f"Batch size {result['batch_size']:2d}: "
              f"{result['throughput']:6.1f} tokens/sec "
              f"({result['per_token_time']*1000:5.1f}ms/token)")

if __name__ == "__main__":
    asyncio.run(main())
```

这个进阶优化模块为推理服务提供了批量处理、流式传输和多模型管理等高级功能，大大提升了推理服务的灵活性和性能表现。