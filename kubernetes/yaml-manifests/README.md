# Domain-32: YAML清单管理

> **案例数量**: 20+ 个 | **最后更新**: 2026-03 | **适用版本**: Kubernetes 1.25+

---

## 概述

YAML清单管理域涵盖Kubernetes资源清单的编写规范、模板管理、配置组织等核心内容，帮助运维人员编写高质量、可维护的YAML配置。

**核心价值**：
- 📝 **编写规范**：YAML语法、最佳实践
- 📦 **模板管理**：Kustomize、Helm模板
- 🗂️ **配置组织**：目录结构、命名规范
- ✅ **验证工具**：语法检查、策略验证

---

## 案例目录

### YAML基础
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [YAML语法详解](./01-yaml-syntax-details.md) | 基本语法、数据结构 |
| 02 | [K8s资源清单结构](./02-k8s-resource-manifest-structure.md) | apiVersion、kind、metadata、spec |
| 03 | [YAML编写规范](./03-yaml-writing-conventions.md) | 缩进、注释、命名规范 |

### 工作负载清单
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 04 | [Pod清单模板](./04-pod-manifest-templates.md) | 基础Pod、多容器Pod |
| 05 | [Deployment清单模板](./05-deployment-manifest-templates.md) | 部署配置、更新策略 |
| 06 | [StatefulSet清单模板](./06-statefulset-manifest-templates.md) | 有状态应用配置 |
| 07 | [DaemonSet清单模板](./07-daemonset-manifest-templates.md) | 节点守护进程配置 |
| 08 | [Job/CronJob清单模板](./08-job-cronjob-manifest-templates.md) | 批处理任务配置 |

### 网络清单
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 09 | [Service清单模板](./09-service-manifest-templates.md) | 服务类型、端口配置 |
| 10 | [Ingress清单模板](./10-ingress-manifest-templates.md) | 路由规则、TLS配置 |
| 11 | [NetworkPolicy清单模板](./11-networkpolicy-manifest-templates.md) | 网络策略配置 |

### 存储清单
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 12 | [PV清单模板](./12-pv-manifest-templates.md) | 持久卷配置 |
| 13 | [PVC清单模板](./13-pvc-manifest-templates.md) | 持久卷声明配置 |
| 14 | [StorageClass清单模板](./14-storageclass-manifest-templates.md) | 存储类配置 |

### 配置清单
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 15 | [ConfigMap清单模板](./15-configmap-manifest-templates.md) | 配置数据管理 |
| 16 | [Secret清单模板](./16-secret-manifest-templates.md) | 敏感数据管理 |
| 17 | [RBAC清单模板](./17-rbac-manifest-templates.md) | 权限配置 |

### 模板管理
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 18 | [Kustomize实践](./18-kustomize-practices.md) | Overlay、Patch配置 |
| 19 | [Helm Chart模板](./19-helm-chart-templates.md) | Chart结构、模板语法 |
| 20 | [YAML验证工具](./20-yaml-validation-tools.md) | kubeval、kubeconform |

---

## 相关领域

- **[扩展生态](../extensions/)** - Helm/Kustomize
- **[GitOps](../gitops-ci-cd/)** - 配置管理
- **[平台运维](../platform-ops/)** - 运维实践

---

**维护者**: OpenDemo Team | **许可证**: MIT
