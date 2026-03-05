# Topic: 结构化故障排查

> **文档数量**: 60+ 篇 | **最后更新**: 2026-03 | **专业级别**: 企业级生产环境

---

## 概述

本专题提供 Kubernetes 各组件的结构化故障排查指南，按照控制平面、节点组件、网络、存储、工作负载等维度进行系统化组织。

**核心价值**：
- 🔍 **系统化方法**：结构化的故障排查流程
- 📋 **全面覆盖**：涵盖所有核心组件
- 🛠️ **实用工具**：诊断命令和脚本

---

## 文档目录

### 01-控制平面 (Control Plane)
| 文档 | 关键内容 |
|------|----------|
| [API Server故障排查](./01-control-plane/01-apiserver-troubleshooting.md) | 请求超时、认证失败、资源耗尽 |
| [etcd故障排查](./01-control-plane/02-etcd-troubleshooting.md) | 性能问题、数据损坏、集群分裂 |
| [Scheduler故障排查](./01-control-plane/03-scheduler-troubleshooting.md) | 调度失败、资源不足、策略问题 |
| [Controller Manager故障排查](./01-control-plane/04-controller-manager-troubleshooting.md) | 控制循环异常、资源泄漏 |
| [Webhook Admission故障排查](./01-control-plane/05-webhook-admission-troubleshooting.md) | 准入失败、超时问题 |
| [APF故障排查](./01-control-plane/06-apf-troubleshooting.md) | 流量控制、优先级问题 |
| [控制平面安全故障排查](./01-control-plane/07-control-plane-security-troubleshooting.md) | 认证授权、证书问题 |
| [控制平面性能故障排查](./01-control-plane/08-control-plane-performance-troubleshooting.md) | 性能瓶颈、资源优化 |
| [控制平面HA故障排查](./01-control-plane/09-control-plane-ha-troubleshooting.md) | 高可用问题、故障切换 |
| [控制平面升级故障排查](./01-control-plane/10-control-plane-upgrade-troubleshooting.md) | 升级失败、版本兼容 |

### 02-节点组件 (Node Components)
| 文档 | 关键内容 |
|------|----------|
| [Kubelet故障排查](./02-node-components/01-kubelet-troubleshooting.md) | 节点状态、Pod生命周期问题 |
| [Kube-proxy故障排查](./02-node-components/02-kube-proxy-troubleshooting.md) | 服务代理、负载均衡问题 |
| [容器运行时故障排查](./02-node-components/03-container-runtime-troubleshooting.md) | Docker/containerd问题 |
| [节点故障排查](./02-node-components/04-node-troubleshooting.md) | 节点不可用、资源耗尽 |
| [镜像仓库故障排查](./02-node-components/05-image-registry-troubleshooting.md) | 镜像拉取失败、认证问题 |
| [GPU设备插件故障排查](./02-node-components/06-gpu-device-plugin-troubleshooting.md) | GPU调度、驱动问题 |

### 03-网络 (Networking)
| 文档 | 关键内容 |
|------|----------|
| [CNI故障排查](./03-networking/01-cni-troubleshooting.md) | 网络插件、Pod网络问题 |
| [DNS故障排查](./03-networking/02-dns-troubleshooting.md) | 解析失败、性能问题 |
| [Service/Ingress故障排查](./03-networking/03-service-ingress-troubleshooting.md) | 服务访问、路由问题 |
| [NetworkPolicy故障排查](./03-networking/04-networkpolicy-troubleshooting.md) | 策略配置、连通性问题 |
| [服务网格Istio故障排查](./03-networking/05-service-mesh-istio-troubleshooting.md) | 流量管理、代理问题 |
| [Gateway API故障排查](./03-networking/06-gateway-api-troubleshooting.md) | 网关配置、路由问题 |

### 04-存储 (Storage)
| 文档 | 关键内容 |
|------|----------|
| [PV/PVC故障排查](./04-storage/01-pv-pvc-troubleshooting.md) | 存储挂载、容量问题 |
| [CSI故障排查](./04-storage/02-csi-troubleshooting.md) | 存储驱动、卷管理问题 |

### 05-工作负载 (Workloads)
| 文档 | 关键内容 |
|------|----------|
| [Pod故障排查](./05-workloads/01-pod-troubleshooting.md) | 启动失败、运行异常 |
| [Deployment故障排查](./05-workloads/02-deployment-troubleshooting.md) | 滚动更新、副本问题 |
| [StatefulSet故障排查](./05-workloads/03-statefulset-troubleshooting.md) | 有状态应用、存储问题 |
| [DaemonSet故障排查](./05-workloads/04-daemonset-troubleshooting.md) | 节点部署、资源问题 |
| [Job/CronJob故障排查](./05-workloads/05-job-cronjob-troubleshooting.md) | 任务执行、调度问题 |
| [ConfigMap/Secret故障排查](./05-workloads/06-configmap-secret-troubleshooting.md) | 配置注入、挂载问题 |

### 06-安全认证 (Security & Auth)
| 文档 | 关键内容 |
|------|----------|
| [RBAC故障排查](./06-security-auth/01-rbac-troubleshooting.md) | 权限拒绝、角色配置 |
| [证书故障排查](./06-security-auth/02-certificate-troubleshooting.md) | 证书过期、信任链问题 |
| [Pod安全故障排查](./06-security-auth/03-pod-security-troubleshooting.md) | 安全策略、准入控制 |
| [审计日志故障排查](./06-security-auth/04-audit-logging-troubleshooting.md) | 日志配置、审计问题 |

### 07-资源调度 (Resources & Scheduling)
| 文档 | 关键内容 |
|------|----------|
| [资源配额故障排查](./07-resources-scheduling/01-resources-quota-troubleshooting.md) | 配额限制、资源争抢 |
| [自动扩缩容故障排查](./07-resources-scheduling/02-autoscaling-troubleshooting.md) | HPA/VPA问题 |
| [Cluster Autoscaler故障排查](./07-resources-scheduling/03-cluster-autoscaler-troubleshooting.md) | 节点伸缩问题 |
| [PDB故障排查](./07-resources-scheduling/04-pdb-troubleshooting.md) | Pod中断预算问题 |

### 08-集群运维 (Cluster Operations)
| 文档 | 关键内容 |
|------|----------|
| [集群维护故障排查](./08-cluster-operations/01-cluster-maintenance-troubleshooting.md) | 维护操作、升级问题 |
| [日志监控故障排查](./08-cluster-operations/02-logging-monitoring-troubleshooting.md) | 日志收集、监控问题 |
| [Helm故障排查](./08-cluster-operations/03-helm-troubleshooting.md) | Chart部署、版本管理 |
| [HA灾备故障排查](./08-cluster-operations/04-ha-disaster-recovery-troubleshooting.md) | 高可用、备份恢复 |
| [CRD/Operator故障排查](./08-cluster-operations/05-crd-operator-troubleshooting.md) | 自定义资源问题 |
| [Kustomize故障排查](./08-cluster-operations/06-kustomize-troubleshooting.md) | 配置管理问题 |

### 09-云提供商 (Cloud Provider)
| 文档 | 关键内容 |
|------|----------|
| [云提供商集成故障排查](./09-cloud-provider/01-cloud-provider-integration-troubleshooting.md) | 云服务集成、IAM问题 |

### 10-AI/ML工作负载 (AI/ML Workloads)
| 文档 | 关键内容 |
|------|----------|
| [AI/ML工作负载故障排查](./10-ai-ml-workloads/01-ai-ml-workloads-troubleshooting.md) | GPU调度、训练问题 |

### 11-GitOps/DevOps
| 文档 | 关键内容 |
|------|----------|
| [GitOps/DevOps故障排查](./11-gitops-devops/01-gitops-devops-troubleshooting.md) | CI/CD、GitOps问题 |

### 12-监控可观测性 (Monitoring & Observability)
| 文档 | 关键内容 |
|------|----------|
| [监控可观测性故障排查](./12-monitoring-observability/01-monitoring-observability-troubleshooting.md) | 监控系统、告警问题 |

---

## 故障排查方法论

### 1. 信息收集
```bash
# 集群状态
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A -o wide

# 事件查看
kubectl get events -A --sort-by='.lastTimestamp'
```

### 2. 问题定位
```bash
# 组件日志
kubectl logs -n kube-system <component-pod>
journalctl -u kubelet -f

# 资源描述
kubectl describe <resource> <name> -n <namespace>
```

### 3. 根因分析
- 查看事件信息
- 分析日志输出
- 检查资源配置
- 验证网络连通

### 4. 解决验证
- 应用修复方案
- 验证功能恢复
- 监控稳定性

---

## 相关专题

- **[故障树分析 (FTA)](../topic-fta/)** - 故障诊断方法论
- **[运维词典](../topic-dictionary/)** - 运维知识体系
- **[速查表](../topic-cheat-sheet/)** - 命令参考

---

**维护者**: OpenDemo Team | **许可证**: MIT
