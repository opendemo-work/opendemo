# Kubernetes 架构全景图

> **难度**: ⭐⭐ | **时长**: 45分钟 | **适用版本**: Kubernetes 1.25+

## 概述

本案例深入解析 Kubernetes 整体架构设计，包括控制平面与数据平面的协作机制、核心组件关系、数据流向分析等内容。

## 核心知识点

### 1. Kubernetes 架构层次

```
┌─────────────────────────────────────────────────────────────────┐
│                      Kubernetes Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Control Plane                         │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐   │    │
│  │  │API Server│ │  etcd   │ │Scheduler│ │Controller  │   │    │
│  │  │         │ │         │ │         │ │  Manager    │   │    │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └──────┬──────┘   │    │
│  └───────┼───────────┼───────────┼─────────────┼──────────┘    │
│          └───────────┴───────────┴─────────────┘               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     Data Plane                           │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │                   Worker Nodes                     │   │    │
│  │  │  ┌─────────┐ ┌──────────┐ ┌───────────────────┐  │   │    │
│  │  │  │ Kubelet │ │kube-proxy│ │ Container Runtime │  │   │    │
│  │  │  └─────────┘ └──────────┘ └───────────────────┘  │   │    │
│  │  │  ┌─────────────────────────────────────────────┐ │   │    │
│  │  │  │                  Pods                        │ │   │    │
│  │  │  └─────────────────────────────────────────────┘ │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 2. 控制平面组件

| 组件 | 功能 | 默认端口 |
|------|------|----------|
| kube-apiserver | API 入口、认证授权、准入控制 | 6443 |
| etcd | 分布式键值存储、集群状态 | 2379/2380 |
| kube-scheduler | Pod 调度决策 | 10259 |
| kube-controller-manager | 控制循环、资源协调 | 10257 |
| cloud-controller-manager | 云提供商集成 | 10258 |

### 3. 数据平面组件

| 组件 | 功能 | 默认端口 |
|------|------|----------|
| kubelet | 节点代理、Pod 生命周期 | 10250 |
| kube-proxy | 服务发现、负载均衡 | 10256 |
| Container Runtime | 容器执行环境 | - |

## 实践案例

### 查看集群组件状态

```bash
# 查看控制平面组件
kubectl get componentstatuses

# 查看 API Server 详情
kubectl describe pod kube-apiserver-master -n kube-system

# 查看集群信息
kubectl cluster-info

# 查看节点状态
kubectl get nodes -o wide
```

### 检查组件健康状态

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: component-health-check
  namespace: kube-system
spec:
  containers:
  - name: check
    image: bitnami/kubectl:latest
    command:
    - /bin/sh
    - -c
    - |
      echo "=== API Server Health ==="
      kubectl get --raw='/healthz'
      echo "=== etcd Health ==="
      kubectl get --raw='/healthz/etcd'
      echo "=== Scheduler Health ==="
      kubectl get --raw='/healthz/scheduler'
      echo "=== Controller Manager Health ==="
      kubectl get --raw='/healthz/controller-manager'
```

## 数据流向分析

### Pod 创建流程

```
1. kubectl → API Server (认证/授权/准入)
2. API Server → etcd (存储 Pod 定义)
3. Scheduler watch → 发现未调度 Pod
4. Scheduler → API Server (绑定节点)
5. Kubelet watch → 发现分配的 Pod
6. Kubelet → Container Runtime (创建容器)
7. Kubelet → API Server (更新 Pod 状态)
```

## 最佳实践

1. **控制平面高可用**: 多副本部署、负载均衡
2. **etcd 备份**: 定期备份、异地容灾
3. **资源规划**: 控制平面节点独立部署
4. **安全加固**: TLS 加密、RBAC 权限

## 故障排查

```bash
# 查看控制平面日志
kubectl logs -n kube-system kube-apiserver-master
kubectl logs -n kube-system kube-scheduler-master
kubectl logs -n kube-system kube-controller-manager-master

# 查看 etcd 状态
ETCDCTL_API=3 etcdctl endpoint health

# 检查 kubelet 状态
systemctl status kubelet
journalctl -u kubelet -f
```

## 相关案例

- [核心组件深挖](../02-core-components-deep-dive/)
- [集群配置参数](../06-cluster-configuration-parameters/)
- [故障排查指南](../16-troubleshooting-guide/)

---

**维护者**: OpenDemo Team | **最后更新**: 2026-03
