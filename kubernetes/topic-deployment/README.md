# Topic: 部署专题

> **文档数量**: 5 篇 | **最后更新**: 2026-03 | **适用版本**: Kubernetes 1.25+

---

## 概述

本专题涵盖 Kubernetes 集群从本地开发到生产环境的完整部署方案，包括不同场景的部署策略和最佳实践。

**核心价值**：
- 🚀 **场景覆盖**：本地开发、单节点、开发环境、生产环境
- 📋 **最佳实践**：经过验证的部署配置和流程
- 🔧 **工具集成**：kubeadm、k3s、kind、minikube 等

---

## 文档目录

| # | 文档 | 关键内容 | 适用场景 |
|:---:|:---|:---|:---|
| 01 | [本地演示部署](./01-local-demo-deployment.md) | minikube、kind、Docker Desktop | 学习测试 |
| 02 | [单节点部署](./02-single-node-deployment.md) | k3s、k3d、MicroK8s | 开发测试 |
| 03 | [开发环境部署](./03-development-environment-deployment.md) | 多节点集群、基础组件 | 开发环境 |
| 04 | [生产环境部署](./04-production-environment-deployment.md) | 高可用集群、安全加固、监控 | 生产环境 |

---

## 部署方案对比

| 方案 | 节点数 | 复杂度 | 适用场景 | 推荐工具 |
|------|--------|--------|----------|----------|
| 本地演示 | 1 | 低 | 学习、测试 | minikube, kind |
| 单节点 | 1 | 低 | 开发、CI/CD | k3s, k3d |
| 开发环境 | 3+ | 中 | 团队开发 | kubeadm, k3s |
| 生产环境 | 5+ | 高 | 生产运行 | kubeadm, 云托管 |

---

## 部署前检查清单

### 硬件要求

```yaml
# 最小配置
control-plane:
  cpu: 2
  memory: 4Gi
  storage: 50Gi

worker:
  cpu: 2
  memory: 8Gi
  storage: 100Gi

# 生产配置
control-plane:
  cpu: 4
  memory: 16Gi
  storage: 100Gi

worker:
  cpu: 8
  memory: 32Gi
  storage: 500Gi
```

### 网络要求

- 节点间网络互通
- 开放必要端口（6443, 2379-2380, 10250-10252 等）
- 配置 DNS 解析

### 系统要求

- 操作系统：Ubuntu 20.04+, CentOS 7+, RHEL 8+
- 内核版本：4.19+
- 关闭 Swap
- 配置 sysctl 参数

---

## 相关专题

- **[架构基础](../architecture-fundamentals/)** - 集群架构设计
- **[平台运维](../platform-ops/)** - 集群生命周期管理
- **[本地开发](../local-development/)** - 本地开发环境搭建

---

**维护者**: OpenDemo Team | **许可证**: MIT
