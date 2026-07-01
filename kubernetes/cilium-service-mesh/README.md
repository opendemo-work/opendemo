# Cilium Service Mesh

Cilium eBPF服务网格实践。

## 什么是Cilium

Cilium是基于eBPF的网络、安全和可观测性解决方案：

```
Cilium架构:
┌─────────────────────────────────────────────────────────┐
│                    Control Plane                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                 │
│  │  Cilium │  │  Hubble │  │   CLI   │                 │
│  │ Operator│  │  (Obs)  │  │         │                 │
│  └────┬────┘  └─────────┘  └─────────┘                 │
├───────┴─────────────────────────────────────────────────┤
│                    Kubernetes Cluster                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Cilium Agent (DaemonSet)                        │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐       │   │
│  │  │  eBPF   │  │  Envoy  │  │  Hubble │       │   │
│  │  │Programs │  │ (Sidecar)│  │  Probe  │       │   │
│  │  └─────────┘  └─────────┘  └─────────┘       │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                    Linux Kernel                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                 │
│  │ eBPF VM │  │ XDP     │  │ tc      │                 │
│  │         │  │ (L2)    │  │ (L3/L7) │                 │
│  └─────────┘  └─────────┘  └─────────┘                 │
└─────────────────────────────────────────────────────────┘
```

## 安装Cilium

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# Helm安装
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set hubble.enabled=true \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true

# 验证
cilium status
```

## 网络策略

```yaml
# L3/L4网络策略
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP

# L7应用层策略
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: http-restrictions
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
          rules:
            http:
              - method: GET
                path: "/api/.*"
```

## 服务网格

```yaml
# 启用mTLS
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: enable-mtls
spec:
  mutualAuthMode: required
```

## 学习要点

1. eBPF基础
2. Cilium网络策略
3. 可观测性 (Hubble)
4. 服务网格功能
5. 性能优化

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
