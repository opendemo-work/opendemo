# Domain-17: 云提供商集成

> **案例数量**: 15+ 个 | **最后更新**: 2026-03 | **云厂商**: 阿里云、AWS、Azure、GCP

---

## 概述

云提供商集成域涵盖主流云厂商的Kubernetes服务集成，包括托管K8s服务、云存储、云网络、云安全等内容。

**核心价值**：
- ☁️ **多云架构**：跨云部署、混合云集成
- 🔧 **托管服务**：ACK、EKS、AKS、GKE
- 🔐 **云安全**：IAM集成、安全组配置
- 💰 **成本优化**：资源规划、成本控制

---

## 案例目录

### 阿里云ACK
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [ACK集群管理](./01-ack-cluster-management.md) | 集群创建、节点池管理 |
| 02 | [ACK网络配置](./02-ack-network-configuration.md) | Terway、Service配置 |
| 03 | [ACK存储集成](./03-ack-storage-integration.md) | 云盘、NAS、OSS集成 |

### AWS EKS
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 04 | [EKS集群管理](./04-eks-cluster-management.md) | 集群创建、节点组管理 |
| 05 | [EKS网络配置](./05-eks-network-configuration.md) | VPC、安全组配置 |
| 06 | [EKS存储集成](./06-eks-storage-integration.md) | EBS、EFS集成 |

### Azure AKS
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 07 | [AKS集群管理](./07-aks-cluster-management.md) | 集群创建、节点池管理 |
| 08 | [AKS网络配置](./08-aks-network-configuration.md) | VNet、NSG配置 |

### GCP GKE
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 09 | [GKE集群管理](./09-gke-cluster-management.md) | 集群创建、节点池管理 |
| 10 | [GKE网络配置](./10-gke-network-configuration.md) | VPC、防火墙配置 |

### 多云管理
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 11 | [多云架构设计](./11-multi-cloud-architecture-design.md) | 跨云部署策略 |
| 12 | [混合云集成](./12-hybrid-cloud-integration.md) | 本地数据中心集成 |
| 13 | [云间网络互联](./13-cloud-network-interconnection.md) | VPN、专线配置 |

### 成本优化
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 14 | [云资源成本优化](./14-cloud-resource-cost-optimization.md) | 实例选型、Spot实例 |
| 15 | [FinOps实践](./15-finops-practices.md) | 成本分析、预算管理 |

---

## 相关领域

- **[平台运维](../platform-ops/)** - 集群管理
- **[网络管理](../network-advanced/)** - 网络配置
- **[存储管理](../storage-advanced/)** - 存储集成

---

**维护者**: OpenDemo Team | **许可证**: MIT
