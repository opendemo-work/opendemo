# Domain-1: Kubernetes架构基础

> **案例数量**: 18 个 | **最后更新**: 2026-03 | **适用版本**: Kubernetes 1.25+

---

## 概述

Kubernetes架构基础域深入解析K8s核心架构设计原理，涵盖控制平面、数据平面、核心组件工作机制等内容。帮助读者建立扎实的K8s理论基础。

**核心价值**：
- 🏗️ **架构理解**：深入理解K8s核心架构设计思想
- 🔧 **组件剖析**：掌握各核心组件工作原理和交互机制  
- 📊 **数据流向**：清晰的数据流转和控制流分析
- 🎯 **设计原则**：学习K8s架构设计的最佳实践

---

## 案例目录

### 架构基础 (01-04)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 01 | [K8s架构全景图](./01-kubernetes-architecture-overview/) | 整体架构、控制平面vs数据平面、核心组件关系 | ⭐⭐⭐⭐⭐ |
| 02 | [核心组件深挖](./02-core-components-deep-dive/) | API Server, etcd, Scheduler, Controller Manager | ⭐⭐⭐⭐⭐ |
| 03 | [功能与API特性](./03-api-versions-features/) | API版本演进、弃用策略、Feature Gates | ⭐⭐⭐⭐ |
| 04 | [源码结构概览](./04-source-code-structure/) | 仓库目录结构、核心包分布、开发工具 | ⭐⭐⭐ |

### 运维与工具 (05-08)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 05 | [kubectl命令参考](./05-kubectl-commands-reference/) | 生产级常用命令、插件机制、输出格式 | ⭐⭐⭐⭐ |
| 06 | [集群配置参数](./06-cluster-configuration-parameters/) | 核心组件参数详解、最佳实践配置 | ⭐⭐⭐⭐ |
| 07 | [升级路径表](./07-upgrade-paths-strategy/) | 版本兼容性矩阵、kubeadm升级实战 | ⭐⭐⭐⭐ |
| 08 | [多租户架构设计](./08-multi-tenancy-architecture/) | 软隔离vs硬隔离、Namespace、vCluster | ⭐⭐⭐⭐⭐ |

### 扩展与异构 (09-12)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 09 | [边缘计算集成](./09-edge-computing-kubeedge/) | KubeEdge, OpenYurt 架构与集成 | ⭐⭐⭐ |
| 10 | [Windows容器支持](./10-windows-containers-support/) | Windows节点加入、网络隔离、限制说明 | ⭐⭐⭐ |
| 11 | [源码架构深度分析](./11-kubernetes-source-code-architecture/) | 核心流程分析、设计模式应用 | ⭐⭐⭐⭐ |
| 12 | [集群部署模式](./12-cluster-deployment-patterns/) | 高可用架构、多数据中心部署、DR设计 | ⭐⭐⭐⭐⭐ |

### 高级运维与安全 (13-18)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 13 | [性能调优指南](./13-performance-tuning-guide/) | 内核参数、APF调优、etcd性能优化 | ⭐⭐⭐⭐⭐ |
| 14 | [安全架构设计](./14-security-architecture/) | RBAC, OIDC, KMS v2, 零信任模型 | ⭐⭐⭐⭐⭐ |
| 15 | [可观测性架构](./15-observability-architecture/) | Metrics, Logs, Traces, Profiling 集成 | ⭐⭐⭐⭐⭐ |
| 16 | [故障排查指南](./16-troubleshooting-guide/) | 架构级故障诊断逻辑、核心指标分析 | ⭐⭐⭐⭐⭐ |
| 17 | [生产运维最佳实践](./17-production-operations-best-practices/) | 备份恢复、健康巡检、容量规划 | ⭐⭐⭐⭐⭐ |
| 18 | [升级与迁移策略](./18-upgrade-migration-strategy/) | 蓝绿升级、跨云迁移、回滚自动化 | ⭐⭐⭐⭐⭐ |

---

## 学习路径建议

### 🎯 新手入门路径
**01 → 02 → 03 → 04 → 08**  
建立K8s架构基础认知，理解核心组件工作原理

### 🔧 进阶深入路径  
**05 → 06 → 07 → 09 → 10**  
深入学习存储、调度、控制器等核心机制

### 🏢 专家精通路径
**11 → 12 → 13 → 14 → 15 → 17**  
掌握安全、可观测性、扩展等高级架构主题，深入生产运维最佳实践

---

## 相关领域

- **[控制平面](../control-plane)** - 控制平面详细配置
- **[工作负载](../workload)** - Pod、Deployment等资源管理
- **[网络](../network)** - 网络插件和策略配置
- **[存储](../pv-pvc)** - 存储插件和持久化配置

---

**维护者**: OpenDemo Team | **许可证**: MIT
