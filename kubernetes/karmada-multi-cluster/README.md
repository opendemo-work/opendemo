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
