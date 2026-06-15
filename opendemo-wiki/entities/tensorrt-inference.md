---
title: TensorRT Inference
summary: PyTorch to TensorRT Engine conversion with layer fusion, precision calibration, and kernel auto-tuning for 3-5x throughput gains.
updated: 2026-06-05
tags:
  - llm
  - optimization
  - inference
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/optimization/tensorrt-inference/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# TensorRT Inference

TensorRT accelerates LLM inference through PyTorch → ONNX → TensorRT Engine conversion with multiple optimization techniques.

## Core Optimization Mechanisms

```
PyTorch → ONNX → TensorRT Parser → Builder → Engine

TensorRT Core Optimizations:
1. Layer Fusion: Multiple ops merged into one
2. Precision Calibration: FP32 → FP16/INT8
3. Kernel Auto-Tuning: Select optimal CUDA kernel
4. Memory Optimization: Reuse memory, reduce allocation
```

## Performance Comparison

| Implementation | Latency (ms) | Throughput (tokens/s) | Memory (GB) |
|----------------|-------------|----------------------|-------------|
| PyTorch (FP16) | 85 | 235 | 18.5 |
| vLLM | 52 | 385 | 16.2 |
| TensorRT (FP16) | 32 | 625 | 14.8 |
| TensorRT (INT8) | 18 | 1100 | 10.2 |

## PyTorch → ONNX Export

```python
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
        return self.lm_head(x)
    
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
```

## TensorRT Engine Builder

```python
class TensorRTEngine:
    def __init__(self, engine_path):
        self.logger = trt.Logger(trt.Logger.WARNING)
        self.runtime = trt.Runtime(self.logger)
        with open(engine_path, 'rb') as f:
            self.engine = self.runtime.deserialize_cuda_engine(f.read())
        self.context = self.engine.create_execution_context()
        
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
        input_shape = input_ids.shape
        self.context.set_input_shape('input_ids', input_shape)
        np.copyto(self.inputs[0]['host'], input_ids.flatten())
        cuda.memcpy_htod(self.inputs[0]['device'], self.inputs[0]['host'])
        self.context.execute_v2(bindings=self.bindings)
        cuda.memcpy_dtoh(self.outputs[0]['host'], self.outputs[0]['device'])
        return self.outputs[0]['host'].reshape(input_shape[0], -1)
```

## Dynamic Shape Configuration

```python
def build_tensorrt_engine_dynamic():
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    config = builder.create_builder_config()
    
    profile = builder.create_optimization_profile()
    profile.set_shape('input_ids', (1, 64), (1, 512), (1, 2048))
    config.add_optimization_profile(profile)
    config.set_flag(trt.BuilderFlag.FP16)
    config.set_flag(trt.BuilderFlag.PERFORMANCE_HINT)
    
    engine_bytes = builder.build_serialized_network(network, config)
    return engine_bytes
```

## Deployment Commands

```bash
pip install tensorrt
python export_onnx.py --model llama-7b --output llama7b.onnx

# Build Engine (FP16)
trtexec --onnx=llama7b.onnx \
    --saveEngine=llama7b_fp16.engine \
    --fp16 \
    --shapes=input_ids:1x512

# Build Engine (INT8 calibration)
trtexec --onnx=llama7b.onnx \
    --saveEngine=llama7b_int8.engine \
    --int8 \
    --calib=calib_data \
    --shapes=input_ids:1x512

# Performance test
trtexec --loadEngine=llama7b_fp16.engine \
    --streams=4 \
    --duration=60
```

## Key Takeaways

1. **Conversion flow**: PyTorch → ONNX → TensorRT Engine
2. **Dynamic shape**: Supports variable length inputs, flexible deployment
3. **Precision selection**: FP16 balances speed/accuracy, INT8 for maximum speed
4. **Batching**: Multi-stream concurrent execution improves GPU utilization

## Related

- [[entities/paged-attention]] - Memory optimization
- [[entities/kv-cache-optimization]] - Cache strategies
- [[entities/awq-quantization]] - Weight quantization
- [[entities/tech-stacks]] - LLM inference stack
