# ⎈ Kubernetes技术栈完整指南

> Kubernetes从基础到企业级运维的完整学习体系，包含171个核心案例

## 📋 技术栈概述

Kubernetes是一个开源的容器编排平台，用于自动化部署、扩展和管理容器化应用。本技术栈提供从基础概念到生产运维的完整Kubernetes学习路径。

### 🔧 核心技能覆盖

- **基础概念**: Pod、Service、Deployment、StatefulSet等核心资源
- **网络管理**: Service、Ingress、网络策略、DNS服务
- **存储管理**: PV/PVC、StorageClass、CSI插件
- **工作负载**: 各种控制器和调度策略
- **基础架构**: 集群管理、RBAC、监控日志
- **运维实践**: 故障排查、备份恢复、性能优化
- **AI训练**: 大模型训练、分布式训练、模型优化
- **模型服务**: 推理部署、服务网格、负载均衡

### 🎯 适用人群

- Kubernetes初学者
- DevOps工程师
- 云平台架构师
- SRE团队成员
- 容器平台管理员
- AI/ML工程师
- 大模型训练研究人员

---

## 📚 学习路径

### 核心概念系列 (约30个案例)
从Pod到各种控制器，掌握Kubernetes基础资源。

### 网络管理系列 (约25个案例)
学习Service、Ingress、DNS等网络相关组件。

### 存储管理系列 (约20个案例)
掌握PV/PVC、StorageClass等存储相关功能。

### 企业级运维系列 (约90个案例)
涵盖集群管理、监控、安全、故障排查等高级主题。

---

## 🚀 快速开始

```bash
# 查看所有Kubernetes案例
opendemo search kubernetes

# 获取基础概念案例
opendemo get kubernetes pod-basics

# 获取网络管理案例
opendemo get kubernetes service-types-overview

# 获取大模型训练案例
opendemo get kubernetes model-training-basics
```

---

## 📊 案例统计

| 分类 | 案例数量 | 状态 |
|------|----------|------|
| 核心概念 | ~30 | ✅ 基本完成 |
| 网络管理 | ~35 | ✅ 完整增强 |
| 存储管理 | ~20 | ✅ 基本完成 |
| 企业级运维 | ~90 | ✅ 基本完成 |
| 大模型训练 | 5 | ✅ 完整增强 |
| 大模型推理 | 5 | ✅ 新增完成 |
| **总计** | **185** | ✅ |

---

## 📚 详细目录

### 核心概念 (约30个)
<details>
<summary>点击查看完整列表</summary>

- Pod基础入门
- Deployment管理
- StatefulSet有状态应用
- DaemonSet节点级部署
- Job/CronJob批处理
- ConfigMap/Secret配置管理
- Namespace资源隔离

</details>

### 网络管理 (约45个)
<details>
<summary>点击查看完整列表</summary>

- [service-types-overview](./service/service-types-overview/) - Service类型详解
- [**service-production-suite**](./service/service-production-suite/) - **Service生产级完整套件** ⭐
- [ingress-basics](./ingress/ingress-basics/) - Ingress基础入门
- [ingress-advanced](./ingress/ingress-advanced/) - Ingress高级特性
- [ingress-security](./ingress/ingress-security/) - Ingress安全配置
- [ingress-production](./ingress/ingress-production/) - Ingress生产实践
- [ingress-troubleshooting](./ingress/ingress-troubleshooting/) - Ingress故障排查
- [**ingress-production-suite**](./ingress/ingress-production-suite/) - **Ingress生产级完整套件** ⭐
- [**service-ingress-integration-demo**](./service-ingress-integration-demo/) - **Service和Ingress集成演示** ⭐
- [ingress/controllers/nginx-controller](./ingress/controllers/nginx-controller/) - NGINX控制器管理
- [ingress/routing-strategies/path-based-routing](./ingress/routing-strategies/path-based-routing/) - 路径路由策略
- [ingress/security-hardening/tls-ssl-security](./ingress/security-hardening/tls-ssl-security/) - TLS安全加固
- [ingress/monitoring-operations/prometheus-monitoring](./ingress/monitoring-operations/prometheus-monitoring/) - Prometheus监控
- [ingress/advanced-features/custom-annotations](./ingress/advanced-features/custom-annotations/) - 自定义注解
- [network/coredns/coredns-deployment](./network/coredns/coredns-deployment/) - CoreDNS生产部署 ⭐
- [network/coredns/coredns-advanced-features](./network/coredns/coredns-advanced-features/) - CoreDNS高级特性 ⭐
- [network/coredns/monitoring-operations](./network/coredns/monitoring-operations/) - CoreDNS监控运维 ⭐
- [network/coredns/security-hardening](./network/coredns/security-hardening/) - CoreDNS安全加固 ⭐
- [network/coredns-basics](./network/coredns-basics/) - CoreDNS基础入门
- [network/coredns-advanced](./network/coredns-advanced/) - CoreDNS高级特性
- [terway/basics/network-fundamentals](./terway/basics/network-fundamentals/) - Terway网络基础 ⭐
- [terway/advanced-features/advanced-networking](./terway/advanced-features/advanced-networking/) - Terway高级网络 ⭐
- [terway/advanced-features/custom-networking](./terway/advanced-features/custom-networking/) - Terway自定义网络 ⭐
- [terway/deployment/terway-deployment](./terway/deployment/terway-deployment/) - Terway生产部署 ⭐
- [terway/monitoring-operations/prometheus-monitoring](./terway/monitoring-operations/prometheus-monitoring/) - Terway监控运维 ⭐
- [terway/security-hardening/network-security](./terway/security-hardening/network-security/) - Terway安全加固 ⭐
- [network/csi-plugin-basics](./network/csi-plugin-basics/) - CSI存储插件基础

</details>

### 存储管理 (约20个)
<details>
<summary>点击查看完整列表</summary>

- PV/PVC基础
- StorageClass动态供应
- CSI存储插件
- 存储性能优化
- 存储故障排查

</details>

### 企业级运维 (约90个)
<details>
<summary>点击查看完整列表</summary>

- 集群搭建与初始化
- RBAC权限管理
- 监控与日志系统
- 备份与灾备恢复
- 安全加固配置
- 性能优化调优
- 故障排查诊断

</details>

### 大模型训练 (5个)
<details>
<summary>点击查看完整列表</summary>

- [model-training-basics](./model-training/model-training-basics/) - 大模型训练基础入门 (含可运行示例)
- [distributed-training-advanced](./model-training/distributed-training-advanced/) - 分布式训练进阶 (含DDP工具)
- [model-finetuning-optimization](./model-training/model-finetuning-optimization/) - 模型微调与优化 (完整增强版)
- [production-deployment](./model-training/production-deployment/) - 生产环境部署 (含成本优化)
- [monitoring-operations](./model-training/monitoring-operations/) - 监控与运维 (完整体系)

</details>

### 大模型推理 (5个)
<details>
<summary>点击查看完整列表</summary>

- [inference-basics](./model-inference/inference-basics/) - 推理基础入门 (完整教程)
- [inference-advanced](./model-inference/inference-advanced/) - 推理进阶优化 (批量/流式处理)
- [inference-performance](./model-inference/inference-performance/) - 推理性能优化 (延迟/吞吐量)
- [inference-deployment](./model-inference/inference-deployment/) - 推理生产部署 (高可用/自动扩缩容)
- [inference-operations](./model-inference/inference-operations/) - 推理监控运维 (完整监控体系)

</details>

---

## 🛠️ 环境准备

```bash
# 安装kubectl
# 推荐版本: 最新稳定版

# 配置集群访问
kubectl cluster-info

# 验证权限
kubectl auth can-i get pods --all-namespaces

# 安装必要工具
kubectl krew install ctx ns
```

---

## 📖 学习建议

1. **理论结合实践**: 边学边练，每个概念都要动手实验
2. **循序渐进**: 按照基础→网络→存储→运维的顺序学习
3. **重视安全**: Kubernetes安全配置是生产环境的关键
4. **监控先行**: 建立完善的监控告警体系
5. **网络重点**: 深入学习Service和Ingress的生产级配置
6. **集成思维**: 掌握Service与Ingress的协同工作机制
7. **AI训练特别注意**: 大模型训练需要额外关注GPU资源、分布式协调和成本控制
8. **微调实践重点**: 模型微调应注重参数效率、领域适应和生产部署的完整闭环
9. **训练体系完整性**: 确保从环境搭建到生产部署的全链路可执行性
10. **推理服务优化**: AI推理服务需重点关注延迟优化、资源利用率和高可用部署
11. **文档查阅**: 养成查阅官方文档的习惯

---

## 🤝 贡献指南

欢迎提交新的Kubernetes案例或改进现有案例：
- 遵循Kubernetes最佳实践
- 提供可运行的YAML配置
- 确保案例的生产可用性
- 遵循统一的文档格式
- AI/ML相关案例需包含性能基准和资源需求说明
- 模型微调案例需提供完整的行业应用场景和合规指导
- 所有案例必须包含可运行的配置文件和部署脚本
- 建立完整的交叉引用和索引体系便于学习导航
- 推理案例需包含性能基准测试和监控告警配置

---

> **💡 提示**: Kubernetes是云原生时代的标准容器编排平台，掌握它是现代DevOps工程师的必备技能。