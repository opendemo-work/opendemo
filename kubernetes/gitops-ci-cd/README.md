# Domain-23: GitOps与CI/CD

> **案例数量**: 20+ 个 | **最后更新**: 2026-03 | **专业级别**: 企业级生产环境

---

## 概述

GitOps与CI/CD域涵盖现代云原生的持续集成和持续部署实践，包括GitOps工作流、CI/CD流水线、自动化测试等内容。

**核心价值**：
- 🔄 **GitOps**：声明式配置管理
- 🚀 **CI/CD**：自动化构建部署流水线
- 🧪 **自动化测试**：测试左移、质量保障
- 📦 **制品管理**：版本控制、追溯审计

---

## 案例目录

### GitOps实践
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [GitOps核心概念](./01-gitops-core-concepts.md) | 原则、工作流、工具对比 |
| 02 | [ArgoCD企业实践](./02-argocd-enterprise-practices.md) | 部署、配置、多集群管理 |
| 03 | [FluxCD实践](./03-fluxcd-practices.md) | 部署、配置、多租户 |
| 04 | [GitOps安全实践](./04-gitops-security-practices.md) | 密钥管理、访问控制 |

### CI流水线
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 05 | [Tekton流水线](./05-tekton-pipeline.md) | 云原生CI/CD框架 |
| 06 | [Jenkins X实践](./06-jenkins-x-practices.md) | 云原生Jenkins |
| 07 | [GitHub Actions集成](./07-github-actions-integration.md) | 工作流配置、K8s集成 |
| 08 | [GitLab CI实践](./08-gitlab-ci-practices.md) | Runner配置、流水线设计 |

### CD流水线
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 09 | [部署策略实践](./09-deployment-strategies-practices.md) | 蓝绿、金丝雀、渐进式 |
| 10 | [Helm Chart管理](./10-helm-chart-management.md) | Chart开发、版本管理 |
| 11 | [Kustomize实践](./11-kustomize-practices.md) | 配置管理、Overlay |
| 12 | [多环境管理](./12-multi-environment-management.md) | 开发、测试、生产环境 |

### 自动化测试
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 13 | [测试左移实践](./13-shift-left-testing.md) | 单元测试、集成测试 |
| 14 | [端到端测试](./14-end-to-end-testing.md) | E2E测试框架、自动化 |
| 15 | [性能测试集成](./15-performance-testing-integration.md) | 压测、基准测试 |

### 制品管理
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 16 | [制品版本管理](./16-artifact-version-management.md) | 版本策略、追溯 |
| 17 | [制品仓库集成](./17-artifact-repository-integration.md) | Nexus、Harbor集成 |
| 18 | [制品安全扫描](./18-artifact-security-scanning.md) | 漏洞扫描、策略验证 |

### 流水线运维
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 19 | [流水线监控](./19-pipeline-monitoring.md) | 指标、告警、可视化 |
| 20 | [流水线安全](./20-pipeline-security.md) | 密钥管理、权限控制 |

---

## 相关领域

- **[扩展生态](../extensions/)** - Kubernetes扩展
- **[平台运维](../platform-ops/)** - 运维自动化
- **[容器镜像管理](../container-image-management/)** - 镜像管理

---

**维护者**: OpenDemo Team | **许可证**: MIT
