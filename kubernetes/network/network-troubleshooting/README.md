# 🔍 Kubernetes网络组件故障排查和维护实战

> 系统化Kubernetes网络组件故障诊断：从DNS解析到存储卷，构建完整的网络运维体系

## 📋 案例概述

本案例提供Kubernetes网络组件故障排查的系统化方法和维护体系建设，帮助运维人员快速定位和解决网络相关问题。

### 🔧 核心技能点

- **系统化排查流程**: 从现象到根因的完整诊断路径
- **网络连通性分析**: DNS解析、Pod通信、服务发现诊断
- **存储组件维护**: CSI驱动、卷管理、性能优化
- **自动化诊断工具**: 脚本化排查、预案执行、智能告警
- **性能瓶颈分析**: 网络延迟、吞吐量、资源使用分析
- **预防性维护**: 健康检查、容量预警、自动修复机制

### 🎯 适用人群

- Kubernetes运维工程师
- SRE团队成员
- 网络系统管理员
- 故障排查专家

---

## 🚀 故障排查体系

### 1. 网络连通性诊断脚本

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
#!/bin/bash
# network-diagnostics.sh

NAMESPACE=${1:-default}
OUTPUT_DIR="./network-diagnostics-$(date +%Y%m%d-%H%M%S)"

mkdir -p $OUTPUT_DIR

echo "=== Kubernetes Network Diagnostics Report ===" > $OUTPUT_DIR/report.txt
echo "Namespace: $NAMESPACE" >> $OUTPUT_DIR/report.txt
echo "Generated: $(date)" >> $OUTPUT_DIR/report.txt
echo "" >> $OUTPUT_DIR/report.txt

# 1. DNS解析检查
echo "1. DNS Resolution Check:" >> $OUTPUT_DIR/report.txt
kubectl run dns-debug --image=busybox --rm -it -- sh -c "
  nslookup kubernetes.default
  nslookup google.com
" >> $OUTPUT_DIR/report.txt 2>&1

# 2. 网络策略检查
echo -e "\n2. Network Policies:" >> $OUTPUT_DIR/report.txt
kubectl get networkpolicies --all-namespaces >> $OUTPUT_DIR/report.txt

# 3. CoreDNS状态检查
echo -e "\n3. CoreDNS Status:" >> $OUTPUT_DIR/report.txt
kubectl get pods -n kube-system -l k8s-app=kube-dns >> $OUTPUT_DIR/report.txt
kubectl describe pods -n kube-system -l k8s-app=kube-dns >> $OUTPUT_DIR/detailed-coredns.txt

# 4. 网络组件日志
echo -e "\n4. Network Component Logs:" >> $OUTPUT_DIR/report.txt
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=50 >> $OUTPUT_DIR/coredns-logs.txt
```

### 2. 存储组件诊断

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# CSI驱动状态检查
kubectl get csidrivers
kubectl get csinodes

# 存储类和卷状态
kubectl get storageclass
kubectl get pv,pvc --all-namespaces

# 存储性能测试
kubectl run storage-perf-test --image=alpine -- sh -c "
  dd if=/dev/zero of=/test bs=1M count=100
  sync
  dd if=/test of=/dev/null bs=1M
"
```

### 3. 性能监控配置

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: network-components
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: network-monitoring
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: network-alerts
  namespace: monitoring
data:
  alerts.yaml: |
    groups:
    - name: network.alerts
      rules:
      - alert: HighDNSErrorRate
        expr: rate(coredns_dns_responses_total{rcode!="NOERROR"}[5m]) > 0.05
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "DNS错误率过高"
          description: "DNS错误率超过5%: {{ $value }}"
```

---

## 📋 完整故障排查方案

包含以下核心内容：
- 系统化网络故障排查方法论
- 自动化诊断工具和脚本
- 存储组件维护和优化
- 性能分析和瓶颈识别
- 预防性维护策略
- 应急响应和恢复流程

---
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
