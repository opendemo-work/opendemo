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
