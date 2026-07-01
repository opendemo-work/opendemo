# Karmada Multi-Cluster Management

Karmada多集群管理实践演示。

## 什么是Karmada

Karmada是Kubernetes原生多集群管理系统：

```
Karmada架构:
┌─────────────────────────────────────────────────────────┐
│                  Karmada Control Plane                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │  API    │ │  Scheduler│ │  Controller│ │  Webhook  │       │
│  │ Server  │ │         │ │ Manager │ │         │       │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘       │
├───────┴───────────┴───────────┴───────────┴───────────┤
│                    ETCD Cluster                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │          Karmada API (CRD)                       │   │
│  │  • PropagationPolicy (分发策略)                   │   │
│  │  • OverridePolicy (覆盖策略)                      │   │
│  │  • ResourceBinding (资源绑定)                     │   │
│  │  • Work (工作负载)                                │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  Member Clusters (成员集群)                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│  │ Cluster │    │ Cluster │    │ Cluster │            │
│  │  (Beijing)│    │  (Shanghai)│    │  (Shenzhen)│            │
│  └─────────┘    └─────────┘    └─────────┘            │
└─────────────────────────────────────────────────────────┘
```

## 安装Karmada

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装karmadactl
wget https://github.com/karmada-io/karmada/releases/download/v1.8.0/karmadactl-linux-amd64.tgz
tar -zxvf karmadactl-linux-amd64.tgz
sudo mv karmadactl /usr/local/bin/

# 快速开始 (需要kind或现有集群)
karmadactl init --kubeconfig ~/.kube/config

# 验证安装
kubectl --kubeconfig /etc/karmada/karmada-apiserver.config get clusters
```

## 多集群资源分发

```yaml
# PropagationPolicy 分发策略
apiVersion: policy.karmada.io/v1alpha1
kind: PropagationPolicy
metadata:
  name: nginx-propagation
spec:
  resourceSelectors:
    - apiVersion: apps/v1
      kind: Deployment
      name: nginx
  placement:
    clusterAffinity:
      clusterNames:
        - beijing
        - shanghai
    replicaScheduling:
      replicaDivisionPreference: Weighted
      replicaSchedulingType: Divided
      weightPreference:
        staticWeightList:
          - targetCluster:
              clusterNames:
                - beijing
            weight: 60
          - targetCluster:
              clusterNames:
                - shanghai
            weight: 40
```

## OverridePolicy 覆盖策略

```yaml
apiVersion: policy.karmada.io/v1alpha1
kind: OverridePolicy
metadata:
  name: nginx-override
spec:
  resourceSelectors:
    - apiVersion: apps/v1
      kind: Deployment
      name: nginx
  overrideRules:
    - targetCluster:
        clusterNames:
          - beijing
      overriders:
        plaintext:
          - path: "/spec/template/spec/containers/0/image"
            operator: replace
            value: "nginx:beijing-latest"
    - targetCluster:
        clusterNames:
          - shanghai
      overriders:
        plaintext:
          - path: "/spec/replicas"
            operator: replace
            value: 5
```

## 学习要点

1. 多集群架构设计
2. PropagationPolicy配置
3. OverridePolicy使用
4. 故障转移配置
5. 多集群调度策略

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
