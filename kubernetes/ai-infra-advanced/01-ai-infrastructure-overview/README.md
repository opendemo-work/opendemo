# AI基础设施架构概览

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **参考**: [NVIDIA AI Enterprise](https://www.nvidia.com/en-us/data-center/products/ai-enterprise/) | [Kubeflow](https://www.kubeflow.org/)

---

## AI Infra 全景架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI平台控制平面                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Kubernetes Control Plane (API Server/Scheduler/etcd)   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  AI调度层: Volcano / Kueue / YuniKorn                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│                     计算资源层                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  GPU集群     │  │  NPU集群     │  │  RDMA网络    │         │
│  │  A100/H100   │  │  昇腾910B    │  │  InfiniBand  │         │
│  │  (节点池)    │  │  (节点池)    │  │  RoCE        │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│                     AI工作负载编排层                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ 训练框架   │  │ 推理引擎   │  │ 数据处理   │               │
│  │ PyTorch    │  │ vLLM       │  │ Ray        │               │
│  │ DeepSpeed  │  │ TensorRT   │  │ Spark      │               │
│  │ Megatron   │  │ Triton     │  │ Flink      │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│                     存储与数据层                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ 对象存储   │  │ 向量数据库 │  │ 特征存储   │               │
│  │ S3/OSS     │  │ Milvus     │  │ Feast      │               │
│  │ (模型/数据)│  │ Weaviate   │  │ Tecton     │               │
│  └────────────┘  └────────────┘  └────────────┘               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ 分布式存储 │  │ 缓存层     │  │ 数据湖     │               │
│  │ JuiceFS    │  │ Alluxio    │  │ Iceberg    │               │
│  │ CephFS     │  │ Fluid      │  │ Hudi       │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│                     可观测性与治理层                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ 实验跟踪   │  │ 模型管理   │  │ 数据血缘   │               │
│  │ MLflow     │  │ ModelMesh  │  │ DataHub    │               │
│  │ W&B        │  │ Seldon     │  │ Amundsen   │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

---

## AI专用调度器对比

### 调度器选型矩阵

| 调度器 | Gang调度 | 队列管理 | 优先级抢占 | GPU拓扑感知 | 成熟度 | 生产推荐 |
|-------|---------|---------|-----------|------------|--------|---------|
| **Volcano** | ✅ | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ | 强烈推荐 |
| **Kueue** | ✅ | ✅ | ✅ | ⚠️ 部分 | ⭐⭐⭐⭐ | 推荐 |
| **YuniKorn** | ✅ | ✅ | ✅ | ❌ | ⭐⭐⭐ | 特定场景 |
| **原生K8s Scheduler** | ❌ | ❌ | ✅ | ❌ | ⭐⭐⭐⭐⭐ | 不推荐AI |

---

## Volcano 安装配置

### Helm 安装

```bash
helm repo add volcano-sh https://volcano-sh.github.io/helm-chart
helm install volcano volcano-sh/volcano -n volcano-system --create-namespace
```

### Gang 调度示例

```yaml
apiVersion: batch.volcano.sh/v1alpha1
kind: Job
metadata:
  name: pytorch-training
spec:
  schedulerName: volcano
  minAvailable: 3
  policies:
    - event: TaskCompleted
      action: CompleteJob
  tasks:
    - replicas: 1
      name: master
      policies:
        - event: TaskCompleted
          action: CompleteJob
      template:
        spec:
          containers:
            - name: pytorch
              image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
              command:
                - python
                - -m
                - torch.distributed.launch
                - --nproc_per_node=1
                - --nnodes=3
                - --node_rank=0
                - --master_addr=pytorch-training-master-0
                - --master_port=29500
                - train.py
              resources:
                limits:
                  nvidia.com/gpu: 1
                  memory: 32Gi
                requests:
                  nvidia.com/gpu: 1
                  memory: 32Gi
    - replicas: 2
      name: worker
      template:
        spec:
          containers:
            - name: pytorch
              image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
              command:
                - python
                - -m
                - torch.distributed.launch
                - --nproc_per_node=1
                - --nnodes=3
                - --node_rank=$(TASK_INDEX)
                - --master_addr=pytorch-training-master-0
                - --master_port=29500
                - train.py
              resources:
                limits:
                  nvidia.com/gpu: 1
                  memory: 32Gi
                requests:
                  nvidia.com/gpu: 1
                  memory: 32Gi
```

---

## GPU 资源管理

### NVIDIA Device Plugin

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nvidia-device-plugin-daemonset
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: nvidia-device-plugin-ds
  updateStrategy:
    type: RollingUpdate
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
        - name: nvidia-device-plugin-ctr
          image: nvcr.io/nvidia/k8s-device-plugin:v0.14.0
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

### GPU 时间切片配置

```yaml
version: v1
sharing:
  timeSlicing:
    renameByDefault: false
    failRequestsGreaterThanOne: false
    resources:
      - name: nvidia.com/gpu
        replicas: 4
```

---

## 相关案例

- [GPU调度管理](../03-gpu-scheduling-management/) - GPU资源调度详解
- [分布式训练框架](../05-distributed-training-frameworks/) - 训练框架集成
- [LLM推理服务](../17-llm-inference-serving/) - 大模型推理部署

---

**维护者**: OpenDemo Team | **许可证**: MIT
