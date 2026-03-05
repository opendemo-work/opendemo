# AI成本分析与FinOps

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **工具**: Kubecost, Grafana

---

## 概述

AI基础设施成本管理是企业AI落地的关键挑战，GPU资源的高昂成本需要精细化的成本分析和优化策略。

---

## Kubecost部署

### Helm安装

```bash
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost --create-namespace \
  --set prometheus.serviceAccount.create=true \
  --set prometheus.server.persistentVolume.enabled=true \
  --set prometheus.server.persistentVolume.size=32Gi
```

### Kubecost配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubecost-config
  namespace: kubecost
data:
  custom-pricing.json: |
    {
      "provider": "custom",
      "description": "Custom GPU pricing configuration",
      "CPU": "0.031",
      "RAM": "0.00000387",
      "GPU_NVIDIA_A100": "2.50",
      "GPU_NVIDIA_H100": "3.50",
      "GPU_NVIDIA_V100": "1.50",
      "storage": "0.00005"
    }
```

---

## GPU成本分析

### GPU资源成本Dashboard

```yaml
apiVersion: integreatly.org/v1alpha1
kind: GrafanaDashboard
metadata:
  name: gpu-cost-dashboard
  namespace: monitoring
spec:
  json: |
    {
      "dashboard": {
        "title": "GPU Cost Analysis",
        "panels": [
          {
            "title": "GPU Cost by Namespace",
            "type": "piechart",
            "targets": [
              {
                "expr": "sum by (namespace) (kubecost_gpu_hourly_cost)"
              }
            ]
          },
          {
            "title": "GPU Utilization vs Cost",
            "type": "graph",
            "targets": [
              {
                "expr": "DCGM_FI_DEV_GPU_UTIL"
              },
              {
                "expr": "kubecost_gpu_hourly_cost"
              }
            ]
          },
          {
            "title": "GPU Idle Cost",
            "type": "stat",
            "targets": [
              {
                "expr": "sum(kubecost_gpu_hourly_cost * (1 - DCGM_FI_DEV_GPU_UTIL / 100))"
              }
            ]
          }
        ]
      }
    }
```

---

## 成本优化策略

### 1. GPU资源配额

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota-ai-team
  namespace: ai-team
spec:
  hard:
    requests.nvidia.com/gpu: "16"
    limits.nvidia.com/gpu: "16"
    requests.memory: "256Gi"
    limits.memory: "512Gi"
```

### 2. GPU调度优化

```yaml
apiVersion: scheduling.volcano.sh/v1beta1
kind: Queue
metadata:
  name: gpu-spot-queue
spec:
  weight: 50
  capability:
    nvidia.com/gpu: 32
  reclaimable: true
---
apiVersion: scheduling.volcano.sh/v1beta1
kind: Queue
metadata:
  name: gpu-ondemand-queue
spec:
  weight: 100
  capability:
    nvidia.com/gpu: 16
  reclaimable: false
```

### 3. Spot实例使用

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-spot-pod
spec:
  nodeSelector:
    instance-type: spot
  tolerations:
    - key: "cloud.google.com/gke-preemptible"
      operator: "Equal"
      value: "true"
      effect: "NoSchedule"
  containers:
    - name: training
      image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
      resources:
        limits:
          nvidia.com/gpu: 4
```

---

## 成本告警

### PrometheusRule

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: gpu-cost-alerts
  namespace: monitoring
spec:
  groups:
    - name: gpu-cost-alerts
      rules:
        - alert: HighGPUCost
          expr: sum(kubecost_gpu_hourly_cost) > 100
          for: 1h
          labels:
            severity: warning
          annotations:
            summary: "GPU cost is high"
            description: "Hourly GPU cost exceeds $100"
        
        - alert: LowGPUUtilization
          expr: avg(DCGM_FI_DEV_GPU_UTIL) < 30
          for: 4h
          labels:
            severity: warning
          annotations:
            summary: "GPU utilization is low"
            description: "Average GPU utilization below 30% for 4 hours"
        
        - alert: GPUIdleResources
          expr: count(DCGM_FI_DEV_GPU_UTIL < 10) > 2
          for: 2h
          labels:
            severity: info
          annotations:
            summary: "GPU idle resources detected"
            description: "{{ $value }} GPUs have utilization below 10%"
```

---

## 成本报告

### 定期成本报告

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cost-report
  namespace: kubecost
spec:
  schedule: "0 9 * * 1"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: report
              image: curlimages/curl:latest
              command:
                - curl
                - -X
                - GET
                - "http://kubecost-cost-analyzer.kubecost:9090/model/allocation?window=7d&aggregate=namespace"
                - -o
                - /reports/weekly-cost.json
          restartPolicy: OnFailure
```

---

## 成本优化最佳实践

| 策略 | 节省比例 | 实施难度 |
|------|---------|---------|
| Spot实例 | 60-80% | 中 |
| GPU时间切片 | 30-50% | 低 |
| 模型量化 | 40-60% | 中 |
| 自动扩缩容 | 20-40% | 低 |
| 任务调度优化 | 15-30% | 高 |

---

## 相关案例

- [GPU调度管理](../03-gpu-scheduling-management/) - GPU资源调度
- [成本优化概览](../26-cost-optimization-overview/) - 成本优化策略
- [绿色计算](../28-green-computing-sustainability/) - 可持续发展

---

**维护者**: OpenDemo Team | **许可证**: MIT
