<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# TensorRT 推理加速

> 本案例详解 TensorRT 推理加速技术，实现 PyTorch 模型到 TensorRT Engine 的转换与优化部署

## 核心原理

### TensorRT 优化机制

```
PyTorch → ONNX → TensorRT Parser → Builder → Engine

TensorRT 核心优化:
1. Layer Fusion (层融合)：多个算子合并为一个
2. Precision Calibration (精度校准)：FP32 → FP16/INT8
3. Kernel Auto-Tuning (内核自动调优)：选择最优 CUDA Kernel
4. Memory Optimization (显存优化)：复用显存，减少分配
```

### 优化效果对比

| 实现 | 延迟 (ms) | 吞吐 (tokens/s) | 显存 (GB) |
|------|----------|-----------------|----------|
| PyTorch (FP16) | 85 | 235 | 18.5 |
| vLLM | 52 | 385 | 16.2 |
| TensorRT (FP16) | 32 | 625 | 14.8 |
| TensorRT (INT8) | 18 | 1100 | 10.2 |

## 实现代码

### PyTorch → ONNX 转换

```python
import torch
import torch.nn as nn

class TransformerModel(nn.Module):
    def __init__(self, d_model, n_heads, vocab_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.layers = nn.ModuleList([
            TransformerLayer(d_model, n_heads) 
            for _ in range(12)
        ])
        self.lm_head = nn.Linear(d_model, vocab_size)
        
    def forward(self, input_ids, attention_mask=None):
        x = self.embedding(input_ids)
        for layer in self.layers:
            x = layer(x, attention_mask)
        logits = self.lm_head(x)
        return logits
    
    def export_to_onnx(self, output_path, input_shape=(1, 512)):
        torch.onnx.export(
            self,
            (torch.zeros(input_shape, dtype=torch.long),),
            output_path,
            input_names=['input_ids'],
            output_names=['logits'],
            dynamic_axes={
                'input_ids': {0: 'batch', 1: 'sequence'},
                'logits': {0: 'batch', 1: 'sequence'}
            },
            opset_version=17,
            do_constant_folding=True
        )
        print(f"ONNX model exported to {output_path}")
```

### TensorRT Engine 构建

```python
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

class TensorRTEngine:
    def __init__(self, engine_path):
        self.logger = trt.Logger(trt.Logger.WARNING)
        self.runtime = trt.Runtime(self.logger)
        
        with open(engine_path, 'rb') as f:
            self.engine = self.runtime.deserialize_cuda_engine(f.read())
            
        self.context = self.engine.create_execution_context()
        
        # 分配显存
        self.inputs = []
        self.outputs = []
        self.bindings = []
        
        for i in range(self.engine.num_io_tensors):
            name = self.engine.get_tensor_name(i)
            shape = self.engine.get_tensor_shape(name)
            dtype = trt.nptype(self.engine.get_tensor_dtype(name))
            
            size = trt.volume(shape)
            host_mem = cuda.pagelocked_empty(size, dtype)
            device_mem = cuda.mem_alloc(host_mem.nbytes)
            
            self.bindings.append(int(device_mem))
            if self.engine.get_tensor_mode(name) == trt.TensorIOMode.INPUT:
                self.inputs.append({'name': name, 'host': host_mem, 'device': device_mem})
            else:
                self.outputs.append({'name': name, 'host': host_mem, 'device': device_mem})
    
    def inference(self, input_ids):
        # 拷贝输入
        input_shape = input_ids.shape
        self.context.set_input_shape('input_ids', input_shape)
        
        np.copyto(self.inputs[0]['host'], input_ids.flatten())
        cuda.memcpy_htod(self.inputs[0]['device'], self.inputs[0]['host'])
        
        # 执行推理
        self.context.execute_v2(bindings=self.bindings)
        
        # 拷贝输出
        cuda.memcpy_dtoh(self.outputs[0]['host'], self.outputs[0]['device'])
        
        return self.outputs[0]['host'].reshape(input_shape[0], -1)
```

### 动态 Shape 配置

```python
def build_tensorrt_engine_dynamic():
    """构建支持动态 Shape 的 TensorRT Engine"""
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    config = builder.create_builder_config()
    
    # 配置动态 Shape
    profile = builder.create_optimization_profile()
    profile.set_shape('input_ids', (1, 64), (1, 512), (1, 2048))
    config.add_optimization_profile(profile)
    
    # 配置精度
    config.set_flag(trt.BuilderFlag.FP16)
    config.set_flag(trt.BuilderFlag.PERFORMANCE_HINT)
    
    # 构建 Engine
    engine_bytes = builder.build_serialized_network(network, config)
    return engine_bytes
```

## 部署命令

```bash
# 安装 TensorRT
pip install tensorrt

# 导出 ONNX
python export_onnx.py --model llama-7b --output llama7b.onnx

# 构建 Engine (FP16)
trtexec --onnx=llama7b.onnx \
    --saveEngine=llama7b_fp16.engine \
    --fp16 \
    --shapes=input_ids:1x512

# 构建 Engine (INT8 校准)
trtexec --onnx=llama7b.onnx \
    --saveEngine=llama7b_int8.engine \
    --int8 \
    --calib=calib_data \
    --shapes=input_ids:1x512

# 性能测试
trtexec --loadEngine=llama7b_fp16.engine \
    --streams=4 \
    --duration=60
```

## 学习要点

1. **转换流程**：PyTorch → ONNX → TensorRT Engine
2. **动态 Shape**：支持不同长度输入，灵活部署
3. **精度选择**：FP16 速度与精度平衡，INT8 极致加速
4. **批处理**：多流并发执行，提高 GPU 利用率

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
