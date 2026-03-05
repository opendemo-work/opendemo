# Topic: 速查表 (Cheat Sheet)

> **文档数量**: 4 篇 | **最后更新**: 2026-03 | **适用版本**: Kubernetes 1.25+

---

## 概述

本专题提供 Kubernetes、Go、Linux 等技术的快速参考速查表，帮助运维人员和开发者快速查找常用命令和配置。

**核心价值**：
- 📋 **快速参考**：常用命令和配置一目了然
- 🔍 **便于检索**：分类清晰，便于快速查找
- 💡 **实用导向**：聚焦生产环境常用操作

---

## 文档目录

| # | 文档 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 01 | [Kubernetes 速查表](./k8s-cheatsheet.md) | kubectl 呸用命令、资源管理、故障排查 | ⭐⭐⭐⭐⭐ |
| 02 | [Go 速查表](./go-cheatsheet.md) | Go 语言常用语法、并发模式、工具链 | ⭐⭐⭐⭐ |
| 03 | [Linux 速查表](./linux-cheatsheet.md) | 系统管理、网络配置、性能调优 | ⭐⭐⭐⭐⭐ |
| 04 | [Docker 速查表](./docker-cheatsheet.md) | 容器管理、镜像操作、网络配置 | ⭐⭐⭐⭐ |

---

## Kubernetes 常用命令速查

### 集群管理

```bash
# 集群信息
kubectl cluster-info
kubectl get nodes -o wide
kubectl get componentstatuses

# 资源查看
kubectl get all -A
kubectl get pods -A -o wide
kubectl get svc -A
```

### 工作负载管理

```bash
# Pod 管理
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> -f
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Deployment 管理
kubectl scale deployment <name> --replicas=3 -n <namespace>
kubectl rollout status deployment/<name> -n <namespace>
kubectl rollout undo deployment/<name> -n <namespace>
```

### 网络管理

```bash
# Service 管理
kubectl get svc -n <namespace>
kubectl describe svc <name> -n <namespace>
kubectl expose deployment <name> --port=80 --target-port=8080

# Ingress 管理
kubectl get ingress -A
kubectl describe ingress <name> -n <namespace>
```

### 存储管理

```bash
# PV/PVC 管理
kubectl get pv
kubectl get pvc -A
kubectl describe pvc <name> -n <namespace>
```

### 故障排查

```bash
# 事件查看
kubectl get events -A --sort-by='.lastTimestamp'
kubectl describe <resource> <name> -n <namespace>

# 日志查看
kubectl logs <pod-name> -n <namespace> --previous
kubectl logs <pod-name> -n <namespace> -c <container>
```

---

## 相关专题

- **[运维词典](../topic-dictionary/)** - 详细的概念解释和最佳实践
- **[结构化故障排查](../topic-structural-trouble-shooting/)** - 系统性故障诊断方法

---

**维护者**: OpenDemo Team | **许可证**: MIT
