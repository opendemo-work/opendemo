# SPIFFE/SPIRE Identity

零信任服务身份认证实践。

## 核心概念

SPIFFE/SPIRE为微服务提供统一身份认证：

```
身份认证架构:
┌─────────────────────────────────────────────────────────┐
│                    SPIRE Server                         │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │  CA Plugin   │  │  Node Attest │                     │
│  │  (Signing)   │  │  (Verify)    │                     │
│  └──────────────┘  └──────────────┘                     │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │  Datastore   │  │  SVID Issuer │                     │
│  │  (SQL/K8s)   │  │  (Identity)  │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────┬───────────────────────────────┘
                          │ gRPC
┌─────────────────────────┴───────────────────────────────┐
│                   SPIRE Agents                          │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │  Workload Att│  │  SVID Cache  │                     │
│  │  (Selector)  │  │  (Rotation)  │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────┬───────────────────────────────┘
                          │ Unix Socket / Envoy SDS
┌─────────────────────────┴───────────────────────────────┐
│                   Workloads                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Service A│  │ Service B│  │ Service C│              │
│  │ mTLS     │  │ mTLS     │  │ mTLS     │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

## 安装SPIRE

```bash
# 安装SPIRE Server和Agent
kubectl apply -f https://github.com/spiffe/spire/releases/download/v1.8.0/spire-quickstart.yaml

# 验证
kubectl get pods -n spire
```

## 工作负载注册

```yaml
# 注册工作负载
apiVersion: spire.spiffe.io/v1alpha1
kind: ClusterSPIFFEID
metadata:
  name: backend-workload
spec:
  spiffeIDTemplate: "spiffe://example.org/ns/{{ .PodMeta.Namespace }}/sa/{{ .PodSpec.ServiceAccountName }}"
  podSelector:
    matchLabels:
      app: backend
  workloadSelectorTemplates:
    - "k8s:ns:{{ .PodMeta.Namespace }}"
    - "k8s:sa:{{ .PodSpec.ServiceAccountName }}"
```

## 服务间mTLS

```yaml
# 使用SPIFFE身份进行mTLS
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: mtls-spiffe
spec:
  host: backend.default.svc.cluster.local
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
      clientCertificate: /etc/certs/cert-chain.pem
      privateKey: /etc/certs/key.pem
      caCertificates: /etc/certs/root-cert.pem
```

## 学习要点

1. SPIFFE ID标准
2. SVID证书管理
3. 工作负载证明
4. 自动轮换
5. 跨集群身份

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

```bash
./scripts/apply.sh
```

### 检查状态

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

```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
