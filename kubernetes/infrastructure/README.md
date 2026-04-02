# Kubernetes Infrastructure

Kubernetes基础设施管理最佳实践演示。

## 基础设施即代码

```
GitOps流程:
┌──────────┐     ┌──────────┐     ┌──────────┐
│   Git    │────▶│  ArgoCD  │────▶│   K8s    │
│ (Config) │     │ (Sync)   │     │ (Apply)  │
└──────────┘     └──────────┘     └──────────┘
```

## 集群配置管理

### Cluster API
```yaml
apiVersion: cluster.x-k8s.io/v1beta1
kind: Cluster
metadata:
  name: production
spec:
  controlPlaneRef:
    apiVersion: controlplane.cluster.x-k8s.io/v1beta1
    kind: KubeadmControlPlane
    name: production-control-plane
  infrastructureRef:
    apiVersion: infrastructure.cluster.x-k8s.io/v1beta1
    kind: AWSCluster
    name: production
```

### Terraform集成
```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "production"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 2
      max_size     = 10

      instance_types = ["m6i.large"]
      capacity_type  = "ON_DEMAND"
    }
  }
}
```

## 多集群管理

```bash
# 使用kubectl ctx切换上下文
kctx production
kctx staging

# kubefed联邦集群
kubectl config use-context host
kubefedctl join cluster1 --cluster-context cluster1
```

## 学习要点

1. 基础设施即代码实践
2. 集群生命周期管理
3. 多集群联邦方案
4. 云原生网络架构
5. 安全基线配置
