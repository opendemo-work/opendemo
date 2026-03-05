# GPU监控与DCGM

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **工具**: DCGM, Prometheus, Grafana

---

## 概述

GPU监控是AI基础设施运维的关键能力，通过NVIDIA DCGM (Data Center GPU Manager) 实现全面的GPU指标采集和监控。

---

## DCGM Exporter部署

### DaemonSet部署

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: dcgm-exporter
  namespace: monitoring
  labels:
    app: dcgm-exporter
spec:
  selector:
    matchLabels:
      app: dcgm-exporter
  template:
    metadata:
      labels:
        app: dcgm-exporter
    spec:
      containers:
        - name: dcgm-exporter
          image: nvcr.io/nvidia/k8s/dcgm-exporter:3.1.7-3.1.4-ubuntu20.04
          args:
            - -f
            - /etc/dcgm-exporter/dcp-metrics-included.csv
          ports:
            - containerPort: 9400
              name: metrics
          resources:
            limits:
              memory: 256Mi
            requests:
              cpu: 100m
              memory: 128Mi
          volumeMounts:
            - name: dcgm-config
              mountPath: /etc/dcgm-exporter
      volumes:
        - name: dcgm-config
          configMap:
            name: dcgm-metrics-config
      nodeSelector:
        accelerator: nvidia-gpu
```

### 自定义指标配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: dcgm-metrics-config
  namespace: monitoring
data:
  dcp-metrics-included.csv: |
    # Format
    # Field, Metric Name, Metric Type, Help Text
    DCGM_FI_DEV_GPU_UTIL, DCGM_FI_DEV_GPU_UTIL, gauge, GPU utilization.
    DCGM_FI_DEV_MEM_COPY_UTIL, DCGM_FI_DEV_MEM_COPY_UTIL, gauge, Memory utilization.
    DCGM_FI_DEV_ENC_UTIL, DCGM_FI_DEV_ENC_UTIL, gauge, Encoder utilization.
    DCGM_FI_DEV_DEC_UTIL, DCGM_FI_DEV_DEC_UTIL, gauge, Decoder utilization.
    DCGM_FI_DEV_GPU_TEMP, DCGM_FI_DEV_GPU_TEMP, gauge, GPU temperature.
    DCGM_FI_DEV_GPU_POWER_USAGE, DCGM_FI_DEV_GPU_POWER_USAGE, gauge, GPU power usage.
    DCGM_FI_DEV_POWER_MGMT_LIMIT, DCGM_FI_DEV_POWER_MGMT_LIMIT, gauge, GPU power management limit.
    DCGM_FI_DEV_FB_FREE, DCGM_FI_DEV_FB_FREE, gauge, Framebuffer memory free.
    DCGM_FI_DEV_FB_USED, DCGM_FI_DEV_FB_USED, gauge, Framebuffer memory used.
    DCGM_FI_DEV_FB_TOTAL, DCGM_FI_DEV_FB_TOTAL, gauge, Framebuffer memory total.
    DCGM_FI_DEV_PCIE_RX_THROUGHPUT, DCGM_FI_DEV_PCIE_RX_THROUGHPUT, gauge, PCIe RX throughput.
    DCGM_FI_DEV_PCIE_TX_THROUGHPUT, DCGM_FI_DEV_PCIE_TX_THROUGHPUT, gauge, PCIe TX throughput.
    DCGM_FI_DEV_NVLINK_BANDWIDTH_TOTAL, DCGM_FI_DEV_NVLINK_BANDWIDTH_TOTAL, gauge, NVLink bandwidth.
    DCGM_FI_DEV_SM_CLOCK, DCGM_FI_DEV_SM_CLOCK, gauge, SM clock frequency.
    DCGM_FI_DEV_MEM_CLOCK, DCGM_FI_DEV_MEM_CLOCK, gauge, Memory clock frequency.
    DCGM_FI_DEV_XID_ERRORS, DCGM_FI_DEV_XID_ERRORS, counter, XID errors.
    DCGM_FI_DEV_ECC_SBE_VOL_TOTAL, DCGM_FI_DEV_ECC_SBE_VOL_TOTAL, counter, Single-bit ECC errors.
    DCGM_FI_DEV_ECC_DBE_VOL_TOTAL, DCGM_FI_DEV_ECC_DBE_VOL_TOTAL, counter, Double-bit ECC errors.
```

---

## Prometheus配置

### ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: dcgm-exporter
  namespace: monitoring
  labels:
    app: dcgm-exporter
spec:
  selector:
    matchLabels:
      app: dcgm-exporter
  endpoints:
    - port: metrics
      interval: 15s
      path: /metrics
---
apiVersion: v1
kind: Service
metadata:
  name: dcgm-exporter
  namespace: monitoring
  labels:
    app: dcgm-exporter
spec:
  selector:
    app: dcgm-exporter
  ports:
    - port: 9400
      name: metrics
      targetPort: 9400
```

---

## Grafana仪表板

### GPU监控仪表板

```json
{
  "dashboard": {
    "title": "GPU Monitoring Dashboard",
    "panels": [
      {
        "title": "GPU Utilization",
        "type": "graph",
        "targets": [
          {
            "expr": "DCGM_FI_DEV_GPU_UTIL",
            "legendFormat": "{{kubernetes_pod_name}} - GPU {{gpu}}"
          }
        ]
      },
      {
        "title": "GPU Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "DCGM_FI_DEV_FB_USED / DCGM_FI_DEV_FB_TOTAL * 100",
            "legendFormat": "{{kubernetes_pod_name}} - GPU {{gpu}}"
          }
        ]
      },
      {
        "title": "GPU Temperature",
        "type": "graph",
        "targets": [
          {
            "expr": "DCGM_FI_DEV_GPU_TEMP",
            "legendFormat": "{{kubernetes_node}} - GPU {{gpu}}"
          }
        ]
      },
      {
        "title": "GPU Power Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "DCGM_FI_DEV_GPU_POWER_USAGE",
            "legendFormat": "{{kubernetes_node}} - GPU {{gpu}}"
          }
        ]
      }
    ]
  }
}
```

---

## 告警规则

### GPU告警规则

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: gpu-alerts
  namespace: monitoring
spec:
  groups:
    - name: gpu-alerts
      rules:
        - alert: GPUHighUtilization
          expr: DCGM_FI_DEV_GPU_UTIL > 95
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "GPU utilization is high"
            description: "GPU {{ labels.gpu }} on node {{ labels.kubernetes_node }} has utilization > 95% for 5 minutes"
        
        - alert: GPUHighTemperature
          expr: DCGM_FI_DEV_GPU_TEMP > 85
          for: 2m
          labels:
            severity: critical
          annotations:
            summary: "GPU temperature is high"
            description: "GPU {{ labels.gpu }} on node {{ labels.kubernetes_node }} temperature > 85°C"
        
        - alert: GPUHighMemoryUsage
          expr: (DCGM_FI_DEV_FB_USED / DCGM_FI_DEV_FB_TOTAL) * 100 > 90
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "GPU memory usage is high"
            description: "GPU {{ labels.gpu }} memory usage > 90%"
        
        - alert: GPUECCError
          expr: increase(DCGM_FI_DEV_ECC_DBE_VOL_TOTAL[5m]) > 0
          labels:
            severity: critical
          annotations:
            summary: "GPU ECC error detected"
            description: "Double-bit ECC error detected on GPU {{ labels.gpu }}"
        
        - alert: GPUXIDError
          expr: increase(DCGM_FI_DEV_XID_ERRORS[5m]) > 0
          labels:
            severity: critical
          annotations:
            summary: "GPU XID error detected"
            description: "XID error detected on GPU {{ labels.gpu }}"
```

---

## GPU健康检查

### 节点问题检测

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-health-check
  namespace: monitoring
spec:
  containers:
    - name: health-check
      image: nvcr.io/nvidia/cuda:12.0.0-base-ubuntu22.04
      command:
        - /bin/bash
        - -c
        - |
          while true; do
            nvidia-smi --query-gpu=utilization.gpu,temperature.gpu,memory.used,memory.total --format=csv
            sleep 60
          done
      resources:
        limits:
          nvidia.com/gpu: 1
```

---

## 相关案例

- [GPU调度管理](../03-gpu-scheduling-management/) - GPU资源调度
- [AI平台可观测性](../13-ai-platform-observability/) - AI监控体系
- [故障排查性能](../14-troubleshooting-performance/) - 性能问题诊断

---

**维护者**: OpenDemo Team | **许可证**: MIT
