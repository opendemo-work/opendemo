# Notebook GPU Allocation

## Overview

This demo demonstrates how to configure and allocate GPU resources for Kubeflow Notebook servers to accelerate deep learning and machine learning workloads. GPUs provide significant speedup for training neural networks, processing large datasets, and running inference tasks.

GPU allocation in Kubeflow enables data scientists to leverage hardware acceleration directly from their Jupyter notebooks, making it easier to experiment with computationally intensive models.

## Prerequisites

Before starting this demo, ensure you have:

- A Kubernetes cluster with GPU nodes (NVIDIA GPUs)
- NVIDIA GPU Operator or NVIDIA device plugin installed
- Kubeflow Notebooks component installed (v1.7+)
- kubectl configured with cluster access
- Basic understanding of GPU computing and CUDA
- Knowledge of Kubernetes resource management

## Architecture

### GPU Resource Flow

```
┌────────────────────────────────────────────────────────┐
│              Kubernetes Cluster                         │
│                                                         │
│  GPU Nodes (with NVIDIA GPUs)                          │
│  ┌──────────────────────────────────────────────┐     │
│  │  Node: gpu-node-1                            │     │
│  │  ┌────────────────────────────────────────┐  │     │
│  │  │  GPU 0: Tesla V100 (available)         │  │     │
│  │  │  GPU 1: Tesla V100 (allocated)         │  │     │
│  │  └────────────────────────────────────────┘  │     │
│  └──────────────────────────────────────────────┘     │
│                      │                                 │
│                      ▼                                 │
│  ┌──────────────────────────────────────────────┐     │
│  │  NVIDIA Device Plugin                        │     │
│  │  - Discovers GPU resources                   │     │
│  │  - Reports to Kubernetes API                 │     │
│  │  - Manages GPU allocation                    │     │
│  └──────────────────────────────────────────────┘     │
│                      │                                 │
│                      ▼                                 │
│  ┌──────────────────────────────────────────────┐     │
│  │  Notebook Pod with GPU                       │     │
│  │  ┌────────────────────────────────────────┐  │     │
│  │  │  Container: jupyter-notebook           │  │     │
│  │  │  - CUDA runtime available              │  │     │
│  │  │  - cuDNN libraries mounted             │  │     │
│  │  │  - GPU device accessible               │  │     │
│  │  │  - nvidia-smi command available        │  │     │
│  │  └────────────────────────────────────────┘  │     │
│  └──────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────┘
```

### GPU Resource Request

```
Notebook CRD
    │
    ├── spec.template.spec.containers[0].resources
    │       │
    │       ├── requests:
    │       │     nvidia.com/gpu: "1"
    │       │
    │       └── limits:
    │             nvidia.com/gpu: "1"
    │
    └── Kubernetes Scheduler
            │
            ├── Find node with available GPU
            ├── Bind pod to GPU node
            └── NVIDIA device plugin allocates GPU
```

## Step-by-Step Guide

### Step 1: Verify GPU Availability

Check that GPU nodes and device plugin are ready:

```bash
# List nodes with GPU labels
kubectl get nodes -l accelerator=nvidia-gpu

# Check NVIDIA device plugin pods
kubectl get pods -n kube-system -l name=nvidia-device-plugin-ds

# Verify GPU capacity on nodes
kubectl describe nodes | grep -A 5 "nvidia.com/gpu"
```

### Step 2: Create GPU-Enabled Notebook

Apply the notebook manifest with GPU request:

```bash
kubectl apply -f manifests/notebook-gpu.yaml

# Check notebook status
kubectl get notebooks -n kubeflow-user-example-com

# Wait for notebook to be ready
kubectl wait --for=condition=Ready \
  notebook/gpu-notebook \
  -n kubeflow-user-example-com \
  --timeout=600s
```

### Step 3: Access the Notebook

Get access to your GPU-enabled notebook:

```bash
# Port-forward to notebook service
kubectl port-forward -n kubeflow-user-example-com \
  svc/gpu-notebook 8080:80

# Access at http://localhost:8080
# Or use Kubeflow Dashboard UI
```

### Step 4: Verify GPU Access in Notebook

Once in Jupyter, create a new notebook and verify GPU:

```python
# Cell 1: Check nvidia-smi
import subprocess
result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
print(result.stdout)

# Cell 2: Check with PyTorch
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"Number of GPUs: {torch.cuda.device_count()}")
if torch.cuda.is_available():
    print(f"GPU name: {torch.cuda.get_device_name(0)}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# Cell 3: Check with TensorFlow
import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")
print(f"GPU devices: {tf.config.list_physical_devices('GPU')}")
```

### Step 5: Run GPU-Accelerated Training

Test GPU performance with a simple training example:

```python
# PyTorch example
import torch
import torch.nn as nn
import time

# Define simple model
model = nn.Sequential(
    nn.Linear(1000, 512),
    nn.ReLU(),
    nn.Linear(512, 10)
).cuda()

# Generate random data
x = torch.randn(1024, 1000).cuda()
y = torch.randint(0, 10, (1024,)).cuda()

# Training loop
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()

start = time.time()
for epoch in range(100):
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    
print(f"Training time: {time.time() - start:.2f}s")
print(f"GPU utilized: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
```

### Step 6: Monitor GPU Usage

Monitor GPU utilization during training:

```bash
# Watch GPU usage in real-time
kubectl exec -it -n kubeflow-user-example-com \
  $(kubectl get pod -n kubeflow-user-example-com -l notebook-name=gpu-notebook -o jsonpath='{.items[0].metadata.name}') \
  -- watch -n 1 nvidia-smi

# Or check from notebook
import subprocess
subprocess.run(['nvidia-smi', 'dmon', '-s', 'u'])
```

### Step 7: Configure Multiple GPUs (Optional)

For multi-GPU training, update the notebook resource request:

```yaml
# Edit manifests/notebook-multi-gpu.yaml
resources:
  limits:
    nvidia.com/gpu: "2"  # Request 2 GPUs
```

## Configuration Files

### Single GPU Notebook
See `manifests/notebook-gpu.yaml` for single GPU configuration.

### Multi-GPU Notebook
See `manifests/notebook-multi-gpu.yaml` for multi-GPU setup.

### GPU with Specific Memory
See `manifests/notebook-gpu-memory-limit.yaml` for memory-constrained configuration.

## Validation

### Verify GPU Allocation

```bash
# Check pod has GPU assigned
kubectl describe pod -n kubeflow-user-example-com \
  -l notebook-name=gpu-notebook | grep nvidia.com/gpu

# Expected output:
# nvidia.com/gpu: 1
# nvidia.com/gpu: 1
```

### Test GPU Performance

```python
# Benchmark GPU vs CPU
import torch
import time

size = 10000

# CPU benchmark
x_cpu = torch.randn(size, size)
y_cpu = torch.randn(size, size)
start = time.time()
z_cpu = torch.mm(x_cpu, y_cpu)
cpu_time = time.time() - start

# GPU benchmark
x_gpu = torch.randn(size, size).cuda()
y_gpu = torch.randn(size, size).cuda()
torch.cuda.synchronize()
start = time.time()
z_gpu = torch.mm(x_gpu, y_gpu)
torch.cuda.synchronize()
gpu_time = time.time() - start

print(f"CPU time: {cpu_time:.4f}s")
print(f"GPU time: {gpu_time:.4f}s")
print(f"Speedup: {cpu_time/gpu_time:.2f}x")
```

### Check GPU Memory Usage

```bash
# From host
kubectl exec -n kubeflow-user-example-com \
  $(kubectl get pod -n kubeflow-user-example-com -l notebook-name=gpu-notebook -o jsonpath='{.items[0].metadata.name}') \
  -- nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

## Expected Results

After completing this demo, you should observe:

1. **GPU Allocation**: Notebook pod successfully allocated to GPU node
2. **CUDA Available**: PyTorch and TensorFlow detect GPU
3. **Performance Boost**: Significant speedup compared to CPU
4. **GPU Monitoring**: nvidia-smi shows GPU utilization
5. **Memory Management**: GPU memory properly allocated and released

### Success Indicators

- [ ] Notebook pod scheduled on GPU node
- [ ] nvidia-smi command works in notebook
- [ ] PyTorch/TensorFlow detect GPU
- [ ] Training runs on GPU successfully
- [ ] GPU memory usage is visible
- [ ] Performance improvement over CPU

## Troubleshooting

### Pod Stuck in Pending

**Problem**: Notebook pod cannot be scheduled

**Solution**:
```bash
# Check pod events
kubectl describe pod -n kubeflow-user-example-com -l notebook-name=gpu-notebook

# Common issues:
# 1. No GPU nodes available
kubectl get nodes -l accelerator=nvidia-gpu

# 2. All GPUs allocated
kubectl describe nodes | grep -A 10 "Allocated resources"

# 3. Device plugin not running
kubectl get pods -n kube-system -l name=nvidia-device-plugin-ds
```

### CUDA Not Available

**Problem**: torch.cuda.is_available() returns False

**Solution**:
```python
# Check CUDA installation
import subprocess
print(subprocess.run(['nvcc', '--version'], capture_output=True, text=True).stdout)

# Verify PyTorch CUDA version matches driver
import torch
print(f"PyTorch built with CUDA: {torch.version.cuda}")
print(f"Driver CUDA version: ", end='')
subprocess.run(['nvidia-smi'])

# Reinstall PyTorch with correct CUDA version if needed
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Out of Memory Errors

**Problem**: CUDA out of memory during training

**Solution**:
```python
# Clear GPU cache
import torch
torch.cuda.empty_cache()

# Reduce batch size
batch_size = 32  # Try smaller value

# Use gradient accumulation
for i, (inputs, labels) in enumerate(dataloader):
    outputs = model(inputs)
    loss = criterion(outputs, labels) / accumulation_steps
    loss.backward()
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()

# Monitor memory
print(torch.cuda.memory_summary())
```

### Multiple Notebooks Competing for GPU

**Problem**: GPU contention between notebooks

**Solution**:
```bash
# Set resource quotas per namespace
kubectl apply -f - <<EOF
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota
  namespace: kubeflow-user-example-com
spec:
  hard:
    requests.nvidia.com/gpu: "2"
    limits.nvidia.com/gpu: "2"
EOF

# Or use GPU sharing (MIG/MPS)
# Requires NVIDIA Multi-Instance GPU or MPS setup
```

## Advanced Usage

### GPU with Specific Model

Request specific GPU models using node selectors:

```yaml
spec:
  template:
    spec:
      nodeSelector:
        gpu-model: "Tesla-V100"
      containers:
      - name: notebook
        resources:
          limits:
            nvidia.com/gpu: "1"
```

### Mixed Precision Training

Leverage Tensor Cores for faster training:

```python
# PyTorch mixed precision
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for data, target in dataloader:
    optimizer.zero_grad()
    
    with autocast():
        output = model(data)
        loss = criterion(output, target)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### GPU Sharing with Time-Slicing

Configure GPU time-slicing for multiple notebooks:

```yaml
# NVIDIA device plugin ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: nvidia-device-plugin-config
data:
  config.yaml: |
    sharing:
      timeSlicing:
        replicas: 4  # Allow 4 pods per GPU
```

## Best Practices

1. **Right-size GPU Requests**: Don't request more GPUs than needed
2. **Release Resources**: Stop notebooks when not in use
3. **Monitor Utilization**: Use nvidia-smi to track GPU usage
4. **Optimize Batch Sizes**: Find optimal batch size for your GPU
5. **Use Mixed Precision**: Enable FP16 training when possible
6. **Clean Up Memory**: Clear CUDA cache between experiments
7. **Profile Code**: Use profiling tools to identify bottlenecks
8. **Version Pin**: Specify exact CUDA versions in requirements

## Security Considerations

- Limit GPU access with RBAC policies
- Set resource quotas to prevent monopolization
- Monitor GPU usage for abuse
- Use separate namespaces for different teams
- Implement pod security policies
- Audit GPU resource requests

## Cleanup

To remove the GPU notebook:

```bash
# Delete notebook
kubectl delete notebook gpu-notebook -n kubeflow-user-example-com

# Verify GPU is released
kubectl describe nodes | grep nvidia.com/gpu
```

## Additional Resources

- [Kubernetes GPU Scheduling](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)
- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/overview.html)
- [Kubeflow Notebook GPU Configuration](https://www.kubeflow.org/docs/components/notebooks/setup/)
- [PyTorch CUDA Best Practices](https://pytorch.org/docs/stable/notes/cuda.html)
- [TensorFlow GPU Guide](https://www.tensorflow.org/guide/gpu)

## Related Demos

- [notebook-server-creation](../notebook-server-creation/): Basic notebook setup
- [notebook-custom-image](../notebook-custom-image/): Custom images with GPU support
- [notebook-persistent-storage](../notebook-persistent-storage/): Data persistence

## Summary

This demo covered:
- Configuring GPU resources for Kubeflow Notebooks
- Verifying GPU availability and allocation
- Running GPU-accelerated ML training
- Monitoring GPU utilization
- Troubleshooting common GPU issues
- Best practices for GPU usage in notebooks

GPU allocation in Kubeflow enables data scientists to leverage powerful hardware acceleration directly from Jupyter notebooks, significantly speeding up deep learning experimentation and training.
