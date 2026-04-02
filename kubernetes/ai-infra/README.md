# AI Infrastructure on Kubernetes

Kubernetes AI基础设施部署演示。

## AI基础设施栈

```
AI Infra Stack:
┌─────────────────────────────────────────────────────────┐
│                  AI/ML Applications                     │
│         (Training / Inference / Serving)                │
├─────────────────────────────────────────────────────────┤
│  Training Operators │ Serving Platform │ Experiment     │
│  (TF/PyTorch/MPI)   │ (KServe/Triton)  │ Tracking       │
├─────────────────────────────────────────────────────────┤
│                  GPU Scheduler                          │
│              (Volcano/Yunikorn)                         │
├─────────────────────────────────────────────────────────┤
│                  GPU Device Plugin                      │
│              (NVIDIA/AMD/Intel)                         │
├─────────────────────────────────────────────────────────┤
│                  Kubernetes Cluster                     │
└─────────────────────────────────────────────────────────┘
```

## GPU Operator

```bash
# 安装NVIDIA GPU Operator
helm install gpu-operator nvidia/gpu-operator \
  --namespace gpu-operator \
  --create-namespace

# 验证
kubectl get pods -n gpu-operator
kubectl get nodes -o json | jq '.items[].status.capacity'
```

## 训练任务

```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: pytorch-training
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      template:
        spec:
          containers:
          - name: pytorch
            image: pytorch/pytorch:latest
            resources:
              limits:
                nvidia.com/gpu: 2
            command:
            - python
            - train.py
    Worker:
      replicas: 3
      template:
        spec:
          containers:
          - name: pytorch
            image: pytorch/pytorch:latest
            resources:
              limits:
                nvidia.com/gpu: 2
```

## 学习要点

1. GPU资源管理
2. 分布式训练配置
3. 推理服务部署
4. 调度优化策略
