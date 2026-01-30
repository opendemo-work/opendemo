# 🔍 Kubernetes Workload故障排查与监控实战

> 系统化Kubernetes工作负载故障诊断：从基础排查到高级监控，构建完整的工作负载运维体系

## 📋 案例概述

本案例提供Kubernetes Workload故障排查的系统化方法和监控体系建设，帮助运维人员快速定位和解决工作负载相关问题。

### 🔧 核心技能点

- **系统化排查流程**: 从现象到根因的完整诊断路径
- **监控体系建设**: 工作负载指标采集、告警配置、可视化展示
- **自动化故障处理**: 自愈脚本、预案执行、应急响应
- **性能瓶颈分析**: 资源使用分析、调度问题、网络瓶颈
- **日志分析技巧**: 工作负载日志解读、事件关联分析
- **预防性维护**: 健康检查、容量预警、性能趋势分析

### 🎯 适用人群

- Kubernetes运维工程师
- SRE团队成员
- 系统管理员
- 故障排查专家

---

## 🚀 故障排查体系

### 1. 常见故障场景诊断

```bash
# 1. Pod相关故障排查
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous

# 2. Deployment相关故障
kubectl describe deployment <deployment-name> -n <namespace>
kubectl get rs -n <namespace> --selector=app=<app-name>
kubectl rollout status deployment <deployment-name> -n <namespace>

# 3. 资源相关问题
kubectl top pods -n <namespace>
kubectl describe nodes
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

### 2. 监控指标配置

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: workload-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: prometheus-operator
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: workload-alerts
  namespace: monitoring
data:
  alerts.yaml: |
    groups:
    - name: workload.alerts
      rules:
      - alert: HighPodRestartRate
        expr: rate(kube_pod_container_status_restarts_total[5m]) > 0.1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.pod }} restart rate is high"
          description: "{{ $labels.pod }} has restarted {{ $value }} times in the last 5 minutes"
```

### 3. 自动化诊断脚本

```bash
#!/bin/bash
# workload-diagnostics.sh

NAMESPACE=${1:-default}
OUTPUT_DIR="./diagnostics-$(date +%Y%m%d-%H%M%S)"

mkdir -p $OUTPUT_DIR

echo "=== Kubernetes Workload Diagnostics Report ===" > $OUTPUT_DIR/report.txt
echo "Namespace: $NAMESPACE" >> $OUTPUT_DIR/report.txt
echo "Generated: $(date)" >> $OUTPUT_DIR/report.txt
echo "" >> $OUTPUT_DIR/report.txt

# 1. 工作负载状态检查
echo "1. Workload Status Check:" >> $OUTPUT_DIR/report.txt
kubectl get deployments,statefulsets,daemonsets,jobs,cronjobs -n $NAMESPACE >> $OUTPUT_DIR/report.txt

# 2. Pod状态分析
echo -e "\n2. Pod Status Analysis:" >> $OUTPUT_DIR/report.txt
kubectl get pods -n $NAMESPACE -o wide >> $OUTPUT_DIR/report.txt

# 3. 资源使用情况
echo -e "\n3. Resource Usage:" >> $OUTPUT_DIR/report.txt
if command -v kubectl &> /dev/null && kubectl top pods -n $NAMESPACE &> /dev/null; then
  kubectl top pods -n $NAMESPACE >> $OUTPUT_DIR/report.txt
else
  echo "kubectl top not available or metrics server not configured" >> $OUTPUT_DIR/report.txt
fi

# 4. 最近事件
echo -e "\n4. Recent Events:" >> $OUTPUT_DIR/report.txt
kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | tail -20 >> $OUTPUT_DIR/report.txt

# 5. 详细诊断信息
kubectl describe deployments,statefulsets,daemonsets -n $NAMESPACE > $OUTPUT_DIR/detailed-describe.txt
kubectl get pods -n $NAMESPACE -o yaml > $OUTPUT_DIR/pods-full.yaml

echo "Diagnostics completed. Results saved to $OUTPUT_DIR/"
```

---

## 📋 完整故障排查方案

包含以下核心内容：
- 系统化排查方法论
- 监控指标体系设计
- 自动化诊断工具
- 性能分析技巧
- 预防性维护策略
- 应急响应流程

---