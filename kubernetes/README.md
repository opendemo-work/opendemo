# ⎈ Kubernetes技术栈完整指南

> Kubernetes从基础到企业级运维的完整学习体系，包含 **400+ 核心案例**

---

## 🚀 快速入口

- 📋 **[K8s 命令行速查表 (k8s-cli.md)](./cli/k8s-cli.md)** - 生产环境必备的Kubernetes命令大全
- 🔍 **[交叉引用索引](#kubernetes案例交叉引用索引)** - 完整的案例导航和关联关系
- 📊 **案例统计**: 400+ 核心案例，覆盖Kubernetes全技术栈

## 📋 技术栈概述

Kubernetes是一个开源的容器编排平台，用于自动化部署、扩展和管理容器化应用。本技术栈提供从基础概念到生产运维的完整Kubernetes学习路径。

### 🔧 核心技能覆盖

- **架构基础**: 控制平面、数据平面、核心组件、设计原则
- **控制平面**: API Server、etcd、Scheduler、Controller Manager
- **工作负载**: Pod、Deployment、StatefulSet、DaemonSet、Job/CronJob
- **网络管理**: Service、Ingress、CoreDNS、网络策略、服务网格
- **存储管理**: PV/PVC、StorageClass、CSI插件、存储优化
- **安全管理**: RBAC、NetworkPolicy、运行时安全、合规审计
- **可观测性**: 监控、日志、追踪、告警、SLO/SLI
- **平台运维**: 集群管理、GitOps、成本优化、灾备恢复
- **扩展生态**: CRD/Operator、Helm、CI/CD、服务网格
- **AI基础设施**: GPU调度、分布式训练、LLM推理、MLOps
- **云原生API网关**: Gateway API、Higress、APISIX、Kong

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

### 核心概念系列 (约50个案例)
从Pod到各种控制器，掌握Kubernetes基础资源。

### 网络管理系列 (约50个案例)
学习Service、Ingress、DNS等网络相关组件。

### 存储管理系列 (约20个案例)
掌握PV/PVC、StorageClass等存储相关功能。

### 企业级运维系列 (约150个案例)
涵盖集群管理、监控、安全、故障排查等高级主题。

### AI/ML系列 (约40个案例)
涵盖GPU调度、分布式训练、LLM推理等AI主题。

### 云原生API网关系列 (约15个案例)
涵盖Gateway API、主流网关产品、安全可观测性。

---

## 📊 案例统计

| 分类 | 案例数量 | 状态 |
|------|----------|------|
| 架构基础 | 18 | ✅ 完成 |
| 控制平面 | 28 | ✅ 完成 |
| 工作负载管理 | 23 | ✅ 完成 |
| 网络管理 | 37 | ✅ 完成 |
| 存储管理 | 15 | ✅ 完成 |
| 安全管理 | 21 | ✅ 完成 |
| 可观测性 | 27 | ✅ 完成 |
| 平台运维 | 25 | ✅ 完成 |
| 扩展生态 | 16 | ✅ 完成 |
| AI基础设施 | 36 | ✅ 完成 |
| 云原生API网关 | 14 | ✅ 完成 |
| 本地开发 | 15 | ✅ 完成 |
| Kubeflow | 42 | ✅ 完成 |
| **专题系列** | | |
| 速查表 | 4 | ✅ 完成 |
| 部署专题 | 4 | ✅ 完成 |
| 运维词典 | 16 | ✅ 完成 |
| 故障树分析(FTA) | 30+ | ✅ 完成 |
| 故障演化模型(FEBM) | 9 | ✅ 完成 |
| 培训教程 | 60+ | ✅ 完成 |
| 迁移专题 | 11 | ✅ 完成 |
| 演示文稿 | 12 | ✅ 完成 |
| 结构化故障排查 | 60+ | ✅ 完成 |
| 其他案例 | 50+ | ✅ 完成 |
| **总计** | **550+** | ✅ |

---

## 📚 详细目录

### 架构基础 (18个案例)
<details>
<summary>点击查看完整列表</summary>

- [**architecture-fundamentals**](./architecture-fundamentals/) - **Kubernetes架构基础完整指南** ⭐
  - [01-kubernetes-architecture-overview](./architecture-fundamentals/01-kubernetes-architecture-overview/) - K8s架构全景图
  - [02-core-components-deep-dive](./architecture-fundamentals/02-core-components-deep-dive/) - 核心组件深挖
  - [03-api-versions-features](./architecture-fundamentals/03-api-versions-features/) - 功能与API特性
  - [04-source-code-structure](./architecture-fundamentals/04-source-code-structure/) - 源码结构概览
  - [05-kubectl-commands-reference](./architecture-fundamentals/05-kubectl-commands-reference/) - kubectl命令参考
  - [06-cluster-configuration-parameters](./architecture-fundamentals/06-cluster-configuration-parameters/) - 集群配置参数
  - [07-upgrade-paths-strategy](./architecture-fundamentals/07-upgrade-paths-strategy/) - 升级路径表
  - [08-multi-tenancy-architecture](./architecture-fundamentals/08-multi-tenancy-architecture/) - 多租户架构设计
  - [09-edge-computing-kubeedge](./architecture-fundamentals/09-edge-computing-kubeedge/) - 边缘计算集成
  - [10-windows-containers-support](./architecture-fundamentals/10-windows-containers-support/) - Windows容器支持
  - [11-kubernetes-source-code-architecture](./architecture-fundamentals/11-kubernetes-source-code-architecture/) - 源码架构深度分析
  - [12-cluster-deployment-patterns](./architecture-fundamentals/12-cluster-deployment-patterns/) - 集群部署模式
  - [13-performance-tuning-guide](./architecture-fundamentals/13-performance-tuning-guide/) - 性能调优指南
  - [14-security-architecture](./architecture-fundamentals/14-security-architecture/) - 安全架构设计
  - [15-observability-architecture](./architecture-fundamentals/15-observability-architecture/) - 可观测性架构
  - [16-troubleshooting-guide](./architecture-fundamentals/16-troubleshooting-guide/) - 故障排查指南
  - [17-production-operations-best-practices](./architecture-fundamentals/17-production-operations-best-practices/) - 生产运维最佳实践
  - [18-upgrade-migration-strategy](./architecture-fundamentals/18-upgrade-migration-strategy/) - 升级与迁移策略

</details>

### 控制平面 (28个案例)
<details>
<summary>点击查看完整列表</summary>

- [**control-plane**](./control-plane/) - **Kubernetes控制平面完整指南** ⭐
  - [01-plane-architecture-overview](./control-plane/01-plane-architecture-overview/) - 控制平面架构概览
  - [02-plane-components-interaction](./control-plane/02-plane-components-interaction/) - 控制平面组件交互
  - [03-plane-high-availability](./control-plane/03-plane-high-availability/) - 控制平面高可用设计
  - [04-plane-security-hardening](./control-plane/04-plane-security-hardening/) - 控制平面安全加固
  - [05-plane-monitoring-observability](./control-plane/05-plane-monitoring-observability/) - 控制平面监控可观测性
  - [06-plane-troubleshooting](./control-plane/06-plane-troubleshooting/) - 控制平面故障排查
  - [07-plane-upgrade-migration](./control-plane/07-plane-upgrade-migration/) - 控制平面升级迁移
  - [08-plane-performance-benchmarking](./control-plane/08-plane-performance-benchmarking/) - 控制平面性能基准测试
  - [09-plane-scalability-guide](./control-plane/09-plane-scalability-guide/) - 控制平面可扩展性指南
  - [10-plane-backup-disaster-recovery](./control-plane/10-plane-backup-disaster-recovery/) - 控制平面备份与灾难恢复
  - [11-etcd-deep-dive](./control-plane/11-etcd-deep-dive/) - etcd深度解析
  - [12-apiserver-deep-dive](./control-plane/12-apiserver-deep-dive/) - API Server深度解析
  - [13-kube-controller-manager-deep-dive](./control-plane/13-kube-controller-manager-deep-dive/) - kube-controller-manager深度解析
  - [14-cloud-controller-manager-deep-dive](./control-plane/14-cloud-controller-manager-deep-dive/) - cloud-controller-manager深度解析
  - [15-kubelet-deep-dive](./control-plane/15-kubelet-deep-dive/) - kubelet深度解析
  - [16-kube-proxy-deep-dive](./control-plane/16-kube-proxy-deep-dive/) - kube-proxy深度解析
  - [17-apiserver-tuning](./control-plane/17-apiserver-tuning/) - API Server调优
  - [18-api-priority-fairness](./control-plane/18-api-priority-fairness/) - API优先级和公平性
  - [19-etcd-operations](./control-plane/19-etcd-operations/) - etcd运维操作
  - [20-kube-scheduler-deep-dive](./control-plane/20-kube-scheduler-deep-dive/) - kube-scheduler深度解析
  - [21-container-runtime-deep-dive](./control-plane/21-container-runtime-deep-dive/) - 容器运行时深度解析
  - [22-container-storage-deep-dive](./control-plane/22-container-storage-deep-dive/) - 容器存储深度解析
  - [23-container-network-deep-dive](./control-plane/23-container-network-deep-dive/) - 容器网络深度解析
  - [24-production-deployment-best-practices](./control-plane/24-production-deployment-best-practices/) - 生产环境部署最佳实践
  - [25-multi-cloud-hybrid-deployment](./control-plane/25-multi-cloud-hybrid-deployment/) - 多云混合部署架构
  - [26-gitops-automation-operations](./control-plane/26-gitops-automation-operations/) - GitOps自动化运维实践
  - [27-authz-authn-deep-dive](./control-plane/27-authz-authn-deep-dive/) - 认证授权深度解析
  - [28-api-extension-deep-dive](./control-plane/28-api-extension-deep-dive/) - API扩展深度解析

</details>

### 工作负载管理 (23个案例)
<details>
<summary>点击查看完整列表</summary>

- [**workload-advanced**](./workload-advanced/) - **Kubernetes工作负载管理完整指南** ⭐
  - [01-workload-overview-architecture](./workload-advanced/01-workload-overview-architecture/) - 工作负载架构概览
  - [02-deployment-production-patterns](./workload-advanced/02-deployment-production-patterns/) - Deployment生产模式
  - [03-statefulset-advanced-operations](./workload-advanced/03-statefulset-advanced-operations/) - StatefulSet高级运维
  - [04-daemonset-management](./workload-advanced/04-daemonset-management/) - DaemonSet管理策略
  - [05-job-cronjob-advanced](./workload-advanced/05-job-cronjob-advanced/) - Job/CronJob高级用法
  - [06-workload-monitoring-alerting](./workload-advanced/06-workload-monitoring-alerting/) - 工作负载监控告警
  - [07-workload-troubleshooting-handbook](./workload-advanced/07-workload-troubleshooting-handbook/) - 故障排查应急手册
  - [08-multi-cloud-workload-strategy](./workload-advanced/08-multi-cloud-workload-strategy/) - 多云混合部署策略
  - [09-edge-computing-deployment](./workload-advanced/09-edge-computing-deployment/) - 边缘计算部署模式
  - [10-workload-controllers-overview](./workload-advanced/10-workload-controllers-overview/) - 工作负载控制器概览
  - [11-pod-lifecycle-events](./workload-advanced/11-pod-lifecycle-events/) - Pod生命周期事件
  - [12-advanced-pod-patterns](./workload-advanced/12-advanced-pod-patterns/) - 高级Pod模式
  - [13-container-lifecycle-hooks](./workload-advanced/13-container-lifecycle-hooks/) - 容器生命周期钩子
  - [14-sidecar-containers-patterns](./workload-advanced/14-sidecar-containers-patterns/) - Sidecar容器模式
  - [15-container-runtime-interfaces](./workload-advanced/15-container-runtime-interfaces/) - 容器运行时接口
  - [16-runtime-class-configuration](./workload-advanced/16-runtime-class-configuration/) - RuntimeClass配置
  - [17-container-images-registry](./workload-advanced/17-container-images-registry/) - 容器镜像与仓库
  - [18-node-management-operations](./workload-advanced/18-node-management-operations/) - 节点管理操作
  - [19-scheduler-configuration](./workload-advanced/19-scheduler-configuration/) - 调度器配置
  - [20-kubelet-configuration](./workload-advanced/20-kubelet-configuration/) - Kubelet配置
  - [21-hpa-vpa-autoscaling](./workload-advanced/21-hpa-vpa-autoscaling/) - HPA/VPA自动扩缩容
  - [22-cluster-capacity-planning](./workload-advanced/22-cluster-capacity-planning/) - 集群容量规划
  - [23-resource-management](./workload-advanced/23-resource-management/) - 资源管理

</details>

### 网络管理 (37个案例)
<details>
<summary>点击查看完整列表</summary>

- [**network-advanced**](./network-advanced/) - **Kubernetes网络管理完整指南** ⭐
  - 网络基础架构 (01-05): CNI架构、插件对比、Flannel、Terway
  - Service服务 (06-10): 概念类型、实现细节、拓扑感知、kube-proxy
  - DNS服务发现 (11-15): CoreDNS架构、配置、插件
  - 网络策略与安全 (16-18): NetworkPolicy、mTLS
  - Ingress入站流量 (19-26): 控制器、TLS、路由、安全、监控
  - 网络故障排查 (27-29): CNI故障、CoreDNS故障、出站流量
  - 高级主题 (30-37): 服务网格、多集群、Gateway API

</details>

### 存储管理 (15个案例)
<details>
<summary>点击查看完整列表</summary>

- [**storage-advanced**](./storage-advanced/) - **Kubernetes存储管理完整指南** ⭐
  - 基础架构 (01-06): 存储架构、PV/PVC、StorageClass
  - 存储运维 (07-09): 日常运维、性能调优、故障排查
  - 数据保护 (10-15): 备份恢复、安全合规、云原生存储

</details>

### 安全管理 (21个案例)
<details>
<summary>点击查看完整列表</summary>

- [**security-advanced**](./security-advanced/) - **Kubernetes安全管理完整指南** ⭐
  - 基础安全 (01-04): 认证授权、网络安全、运行时安全、审计
  - 安全标准 (05-09): 策略验证、Pod安全标准、RBAC、加固
  - 密钥管理 (10-11): 证书管理、密钥管理工具
  - 合规扫描 (12-17): 合规认证、镜像扫描、策略引擎
  - 高级架构 (18-21): 纵深防御、零信任、事件响应、多集群安全

</details>

### 可观测性 (27个案例)
<details>
<summary>点击查看完整列表</summary>

- [**observability-advanced**](./observability-advanced/) - **Kubernetes可观测性完整指南** ⭐
  - 核心基础 (01-09): 架构、指标、日志、追踪、告警
  - 故障排查 (10-15): Prometheus、自定义指标、健康检查、混沌工程
  - 企业治理 (16-21): 多集群监控、成本优化、SLO/SLI、高可用
  - 高级主题 (22-27): 最佳实践、工具生态、故障排查工具

</details>

### 平台运维 (25个案例)
<details>
<summary>点击查看完整列表</summary>

- [**platform-ops**](./platform-ops/) - **Kubernetes平台运维完整指南** ⭐
  - 运维基础 (01-05): 概述、生命周期、容量规划、性能调优
  - 核心能力 (06-12): 监控告警、GitOps、自动化、成本优化、安全合规
  - 高级管理 (13-18): 多集群、大规模优化、故障诊断、升级迁移
  - 专项技术 (19-25): Lease选举、CRD/Operator、API聚合、虚拟集群

</details>

### 扩展生态 (16个案例)
<details>
<summary>点击查看完整列表</summary>

- [**extensions**](./extensions/) - **Kubernetes扩展生态完整指南** ⭐
  - 扩展开发 (01-04): CRD开发、Operator模式、准入控制、API聚合
  - 包管理 (05-07): Helm管理、高级运维
  - CI/CD (08-10): 流水线、GitOps、镜像构建
  - 服务网格 (11-12): 概览、高级特性
  - 运维管理 (13-16): 运维基础、多集群、监控告警、安全合规

</details>

### AI基础设施 (36个案例)
<details>
<summary>点击查看完整列表</summary>

- [**ai-infra-advanced**](./ai-infra-advanced/) - **AI基础设施完整指南** ⭐
  - AI基础架构 (01-06): 概览、工作负载、GPU调度、监控、分布式训练
  - 模型生命周期 (07-14): 实验管理、AutoML、模型注册、部署、安全
  - LLM大模型 (15-25): 数据管道、微调、推理、量化、RAG、多模态
  - 平台治理 (26-36): 成本优化、安全合规、MLOps、联邦学习

</details>

### 云原生API网关 (14个案例)
<details>
<summary>点击查看完整列表</summary>

- [**cloud-native-api-gateway**](./cloud-native-api-gateway/) - **云原生API网关完整指南** ⭐
  - 基础理论 (01-03): 架构总览、Gateway API、选型指南
  - 产品实践 (04-09): Higress、APISIX、Kong、Envoy Gateway、Traefik
  - 核心能力 (10-12): Wasm插件、安全体系、可观测性
  - 生产运维 (13-14): 性能基准、生产运维

</details>

### 本地开发环境 (15个案例)
<details>
<summary>点击查看本地开发部署方案</summary>

- [**local-development**](./local-development/) - **macOS本地开发环境完整指南** ⭐
  - [minikube部署指南](./local-development/minikube/) - 适合初学者的完整部署教程
  - [kind部署指南](./local-development/kind/) - 开发者的轻量级选择
  - [k3s部署指南](./local-development/k3s/) - 资源受限环境的理想方案
  - [Docker Desktop Kubernetes](./local-development/docker-desktop/) - 一键启用的快速体验
  - [工具对比选择指南](./local-development/tools-comparison/) - 详细的功能对比和选择建议
  - [性能优化与故障排除](./local-development/performance-troubleshooting/) - 完整的调优和问题解决指南

</details>

### Kubeflow (42个案例)
<details>
<summary>点击查看完整列表</summary>

- [**kubeflow**](./kubeflow/) - **Kubeflow机器学习平台完整指南** ⭐
  - Dashboard配置、Notebook服务器、Katib超参调优
  - KServe模型服务、Pipeline流水线、Spark Operator
  - Trainer训练任务、Model Registry模型注册

</details>

---

## � 专题系列

### 速查表 (4篇文档)
<details>
<summary>点击查看完整列表</summary>

- [**topic-cheat-sheet**](./topic-cheat-sheet/) - **运维速查表专题** ⭐
  - Kubernetes 速查表
  - Go 速查表
  - Linux 速查表
  - Docker 速查表

</details>

### 部署专题 (4篇文档)
<details>
<summary>点击查看完整列表</summary>

- [**topic-deployment**](./topic-deployment/) - **集群部署专题** ⭐
  - 本地演示部署
  - 单节点部署
  - 开发环境部署
  - 生产环境部署

</details>

### 运维词典 (16篇文档)
<details>
<summary>点击查看完整列表</summary>

- [**topic-dictionary**](./topic-dictionary/) - **运维知识词典** ⭐
  - 运维最佳实践、故障模式分析、性能调优专家
  - SRE成熟度模型、概念参考、CLI命令参考
  - 工具生态、AI基础设施专家、云原生安全
  - 多云运维、企业运维实践、事件管理手册
  - 容量规划预测、变更管理发布、SLI/SLO/SLA工程

</details>

### 故障树分析 (30+篇文档)
<details>
<summary>点击查看完整列表</summary>

- [**topic-fta**](./topic-fta/) - **故障树分析(FTA)专题** ⭐
  - FTA方法论：起源演进、数学基础、符号系统、核心原则
  - 构建过程：验证质量、维护演进、AI Agent运维革命
  - 组件故障树：API Server、etcd、Scheduler、Pod、Deployment等

</details>

### 故障演化模型 (9篇文档)
<details>
<summary>点击查看完整列表</summary>

- [**topic-febm**](./topic-febm/) - **故障演化模型(FEBM)专题** ⭐
  - FEBM理论基础、技术实现、最佳实践
  - Agent工单处理、构建方法论、未来演进

</details>

### 培训教程 (60+篇文档)
<details>
<summary>点击查看完整列表</summary>

- [**topic-learn**](./topic-learn/) - **培训教程专题** ⭐
  - 内部培训：ACK/ACR生命周期、安全监控、节点工作负载、网络存储
  - 公开培训：基础入门、核心技术、运维实践、企业级实践
  - 实战项目、学习资源、检查点评估

</details>

### 迁移专题 (11篇文档)
<details>
<summary>点击查看完整列表</summary>

- [**topic-migration**](./topic-migration/) - **集群迁移专题** ⭐
  - 迁移评估与规划、ACK目标集群设计
  - 应用工作负载迁移、存储数据迁移
  - 网络迁移与流量切换、有状态服务迁移
  - 可观测性与安全迁移、验证与切换下线
  - 迁移工具链、真实案例研究

</details>

### 演示文稿 (12篇文档)
<details>
<summary>点击查看完整列表</summary>

- [**topic-presentations**](./topic-presentations/) - **演示文稿专题** ⭐
  - 架构基础、调度、工作负载、服务、Ingress演示
  - CoreDNS、存储、安全与RBAC、可观测性演示
  - 故障排查方法论、Terway演示、演示文稿模板

</details>

### 结构化故障排查 (60+篇文档)
<details>
<summary>点击查看完整列表</summary>

- [**topic-structural-trouble-shooting**](./topic-structural-trouble-shooting/) - **结构化故障排查专题** ⭐
  - 控制平面：API Server、etcd、Scheduler、Controller Manager
  - 节点组件：Kubelet、Kube-proxy、容器运行时
  - 网络：CNI、DNS、Service/Ingress、NetworkPolicy
  - 存储：PV/PVC、CSI
  - 工作负载：Pod、Deployment、StatefulSet、DaemonSet
  - 安全认证：RBAC、证书、Pod安全
  - 资源调度：配额、自动扩缩容、PDB
  - 集群运维：维护、日志监控、Helm、HA灾备
  - 云提供商、AI/ML工作负载、GitOps/DevOps、监控可观测性

</details>

---

## ��️ 环境准备

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
2. **循序渐进**: 按照架构→控制平面→工作负载→网络→存储→安全→运维的顺序学习
3. **重视安全**: Kubernetes安全配置是生产环境的关键
4. **监控先行**: 建立完善的监控告警体系
5. **网络重点**: 深入学习Service和Ingress的生产级配置
6. **AI训练特别注意**: 大模型训练需要额外关注GPU资源、分布式协调和成本控制
7. **文档查阅**: 养成查阅官方文档的习惯

---

## 🤝 贡献指南

欢迎提交新的Kubernetes案例或改进现有案例：
- 遵循Kubernetes最佳实践
- 提供可运行的YAML配置
- 确保案例的生产可用性
- 遵循统一的文档格式
- AI/ML相关案例需包含性能基准和资源需求说明

---

> **💡 提示**: Kubernetes是云原生时代的标准容器编排平台，掌握它是现代DevOps工程师的必备技能。

**更新时间**: 2026-03-05  
**版本**: v2.0.0  
**维护状态**: ✅ 活跃维护中
