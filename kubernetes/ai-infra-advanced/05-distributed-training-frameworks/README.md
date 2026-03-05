# 分布式训练框架

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **框架**: PyTorch, DeepSpeed, Megatron

---

## 概述

分布式训练是AI基础设施的核心能力，涵盖数据并行、模型并行、混合并行等多种训练模式。

---

## PyTorch分布式训练

### PyTorchJob (Kubeflow)

```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: pytorch-distributed
  namespace: kubeflow
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
              command:
                - python
                - -m
                - torch.distributed.launch
                - --nproc_per_node=4
                - --nnodes=4
                - --node_rank=0
                - --master_addr=pytorch-distributed-master-0
                - --master_port=29500
                - train.py
              resources:
                limits:
                  nvidia.com/gpu: 4
                  memory: 64Gi
                requests:
                  nvidia.com/gpu: 4
                  memory: 64Gi
    Worker:
      replicas: 3
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
              command:
                - python
                - -m
                - torch.distributed.launch
                - --nproc_per_node=4
                - --nnodes=4
                - --node_rank=$(REPLICA_INDEX)
                - --master_addr=pytorch-distributed-master-0
                - --master_port=29500
                - train.py
              resources:
                limits:
                  nvidia.com/gpu: 4
                  memory: 64Gi
                requests:
                  nvidia.com/gpu: 4
                  memory: 64Gi
```

---

## DeepSpeed训练

### DeepSpeed配置

```yaml
apiVersion: batch.volcano.sh/v1alpha1
kind: Job
metadata:
  name: deepspeed-training
spec:
  schedulerName: volcano
  minAvailable: 4
  tasks:
    - replicas: 4
      name: worker
      policies:
        - event: TaskCompleted
          action: CompleteJob
      template:
        spec:
          containers:
            - name: deepspeed
              image: deepspeed/deepspeed:latest
              command:
                - deepspeed
                - --hostfile
                - /etc/deepspeed/hostfile
                - train.py
                - --deepspeed_config
                - ds_config.json
              resources:
                limits:
                  nvidia.com/gpu: 8
                  memory: 128Gi
                requests:
                  nvidia.com/gpu: 8
                  memory: 128Gi
              volumeMounts:
                - name: deepspeed-config
                  mountPath: /etc/deepspeed
          volumes:
            - name: deepspeed-config
              configMap:
                name: deepspeed-config
```

### DeepSpeed配置文件

```json
{
  "train_batch_size": 256,
  "train_micro_batch_size_per_gpu": 4,
  "gradient_accumulation_steps": 8,
  "optimizer": {
    "type": "AdamW",
    "params": {
      "lr": 1e-4,
      "betas": [0.9, 0.999],
      "eps": 1e-8,
      "weight_decay": 0.01
    }
  },
  "scheduler": {
    "type": "WarmupDecayLR",
    "params": {
      "warmup_min_lr": 0,
      "warmup_max_lr": 1e-4,
      "warmup_num_steps": 1000,
      "total_num_steps": 100000
    }
  },
  "fp16": {
    "enabled": true,
    "loss_scale": 0,
    "initial_scale_power": 16,
    "loss_scale_window": 1000,
    "hysteresis": 2,
    "min_loss_scale": 1
  },
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    },
    "offload_param": {
      "device": "cpu",
      "pin_memory": true
    },
    "overlap_comm": true,
    "contiguous_gradients": true,
    "reduce_bucket_size": 5e8,
    "stage3_prefetch_bucket_size": 5e7,
    "stage3_param_persistence_threshold": 1e5
  }
}
```

---

## Megatron-LM训练

### Megatron训练Job

```yaml
apiVersion: batch.volcano.sh/v1alpha1
kind: Job
metadata:
  name: megatron-training
spec:
  schedulerName: volcano
  minAvailable: 8
  tasks:
    - replicas: 8
      name: worker
      template:
        spec:
          containers:
            - name: megatron
              image: nvcr.io/nvidia/megatron-lm:23.05
              command:
                - python
                - pretrain_gpt.py
                - --num-layers=96
                - --hidden-size=12288
                - --num-attention-heads=96
                - --seq-length=2048
                - --max-position-embeddings=2048
                - --micro-batch-size=1
                - --global-batch-size=512
                - --tensor-model-parallel-size=8
                - --pipeline-model-parallel-size=4
                - --distributed-backend=nccl
                - --train-samples=1000000
                - --lr=1.0e-4
                - --min-lr=1.0e-5
                - --lr-decay-style=cosine
                - --lr-warmup-samples=10000
              resources:
                limits:
                  nvidia.com/gpu: 8
                  memory: 256Gi
                requests:
                  nvidia.com/gpu: 8
                  memory: 256Gi
```

---

## 训练监控

### Prometheus指标采集

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: training-metrics-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'pytorch-training'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - kubeflow
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_training_kubeflow_org_job_role]
            action: keep
            regex: master|worker
```

---

## 相关案例

- [GPU调度管理](../03-gpu-scheduling-management/) - GPU资源调度
- [AI数据管道](../06-ai-data-pipeline/) - 数据处理
- [LLM微调训练](../16-llm-finetuning/) - 大模型微调

---

**维护者**: OpenDemo Team | **许可证**: MIT
