# GPU调度管理

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **GPU类型**: NVIDIA A100/H100/H800

---

## 概述

GPU调度管理是AI基础设施的核心能力，涵盖GPU资源分配、拓扑感知调度、共享机制、监控告警等内容。

---

## GPU调度策略

### 1. 独占调度

每个Pod独占整个GPU设备：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-exclusive-pod
spec:
  containers:
    - name: cuda-container
      image: nvcr.io/nvidia/cuda:12.0.0-base-ubuntu22.04
      command: ["sleep", "infinity"]
      resources:
        limits:
          nvidia.com/gpu: 1
        requests:
          nvidia.com/gpu: 1
```

### 2. GPU时间切片

多个Pod共享单个GPU：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nvidia-plugin-config
  namespace: kube-system
data:
  config.yaml: |
    version: v1
    sharing:
      timeSlicing:
        renameByDefault: false
        failRequestsGreaterThanOne: false
        resources:
          - name: nvidia.com/gpu
            replicas: 4
---
apiVersion: v1
kind: Pod
metadata:
  name: gpu-shared-pod
spec:
  containers:
    - name: cuda-container
      image: nvcr.io/nvidia/cuda:12.0.0-base-ubuntu22.04
      resources:
        limits:
          nvidia.com/gpu: 1
```

### 3. GPU拓扑感知调度

优化多GPU通信性能：

```yaml
apiVersion: scheduling.volcano.sh/v1beta1
kind: Device
metadata:
  name: nvidia-gpu
spec:
  devices:
    - id: GPU-0
      health: true
      topology:
        numa: 0
        pci: "0000:00:04.0"
    - id: GPU-1
      health: true
      topology:
        numa: 0
        pci: "0000:00:05.0"
---
apiVersion: scheduling.volcano.sh/v1beta1
kind: DeviceTopologyConstraint
metadata:
  name: gpu-topology-constraint
spec:
  constraints:
    - name: numa
      required: true
    - name: nvlink
      preferred: true
```

---

## Volcano GPU调度

### GPU优先级队列

```yaml
apiVersion: scheduling.volcano.sh/v1beta1
kind: Queue
metadata:
  name: gpu-high-priority
spec:
  weight: 100
  capability:
    nvidia.com/gpu: 16
    cpu: 64
    memory: 256Gi
  reclaimable: false
---
apiVersion: scheduling.volcano.sh/v1beta1
kind: Queue
metadata:
  name: gpu-low-priority
spec:
  weight: 50
  capability:
    nvidia.com/gpu: 8
    cpu: 32
    memory: 128Gi
  reclaimable: true
```

### GPU Job示例

```yaml
apiVersion: batch.volcano.sh/v1alpha1
kind: Job
metadata:
  name: gpu-training-job
spec:
  schedulerName: volcano
  minAvailable: 2
  priorityClassName: high-priority
  tasks:
    - replicas: 2
      name: worker
      policies:
        - event: TaskCompleted
          action: CompleteJob
      template:
        spec:
          containers:
            - name: pytorch
              image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
              resources:
                limits:
                  nvidia.com/gpu: 4
                  memory: 64Gi
                  cpu: 16
                requests:
                  nvidia.com/gpu: 4
                  memory: 64Gi
                  cpu: 16
```

---

## MIG (Multi-Instance GPU)

### MIG配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nvidia-mig-config
  namespace: kube-system
data:
  config.yaml: |
    version: v1
    mig:
      strategy: mixed
      devices:
        all:
          - mig-gpu: 1g.5gb
          - mig-gpu: 1g.5gb
          - mig-gpu: 1g.5gb
          - mig-gpu: 1g.5gb
          - mig-gpu: 1g.5gb
          - mig-gpu: 1g.5gb
          - mig-gpu: 1g.5gb
```

### MIG Pod示例

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mig-pod
spec:
  containers:
    - name: cuda-container
      image: nvcr.io/nvidia/cuda:12.0.0-base-ubuntu22.04
      resources:
        limits:
          nvidia.com/mig-1g.5gb: 1
```

---

## GPU资源配额

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota
  namespace: ai-team
spec:
  hard:
    requests.nvidia.com/gpu: "16"
    limits.nvidia.com/gpu: "16"
    requests.nvidia.com/mig-1g.5gb: "64"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: gpu-limits
  namespace: ai-team
spec:
  limits:
    - type: Container
      max:
        nvidia.com/gpu: "4"
      min:
        nvidia.com/gpu: "1"
      default:
        nvidia.com/gpu: "1"
      defaultRequest:
        nvidia.com/gpu: "1"
```

---

## GPU调度最佳实践

### 1. 节点标签

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl label nodes gpu-node-1 accelerator=nvidia-a100
kubectl label nodes gpu-node-1 gpu-count=8
kubectl label nodes gpu-node-1 gpu-memory=80Gi
```

### 2. 节点污点

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl taint nodes gpu-node-1 nvidia.com/gpu=true:NoSchedule
```

### 3. Pod容忍

```yaml
spec:
  tolerations:
    - key: nvidia.com/gpu
      operator: Exists
      effect: NoSchedule
  nodeSelector:
    accelerator: nvidia-a100
```

---

## 相关案例

- [AI基础设施概览](../01-ai-infrastructure-overview/) - 架构设计
- [GPU监控DCGM](../04-gpu-monitoring-dcgm/) - GPU监控
- [分布式训练](../05-distributed-training-frameworks/) - 训练框架

---

**维护者**: OpenDemo Team | **许可证**: MIT

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/apply.sh
```

### 检查状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/check.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 Kubernetes 核心概念。

### 2. 适用场景

- 场景 1：开发与测试
- 场景 2：生产环境参考
- 场景 3：故障排查

## 💻 代码示例

### 基本命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
