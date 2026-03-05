# Domain-12: Kubernetes故障排查

> **案例数量**: 20+ 个 | **最后更新**: 2026-03 | **适用版本**: Kubernetes 1.25+

---

## 概述

Kubernetes故障排查域提供系统化的故障诊断方法论和实战案例，帮助运维人员快速定位和解决K8s集群问题。

**核心价值**：
- 🔍 **系统化方法**：结构化的故障排查流程
- 🛠️ **工具集成**：诊断命令和脚本工具
- 📋 **案例库**：常见故障场景和解决方案

---

## 案例目录

### 故障排查方法论
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [故障排查方法论](./01-troubleshooting-methodology.md) | 系统化排查流程、诊断工具 |
| 02 | [日志分析技巧](./02-log-analysis-techniques.md) | 日志收集、分析、过滤 |
| 03 | [性能问题诊断](./03-performance-issue-diagnosis.md) | 性能瓶颈定位、优化建议 |

### 控制平面故障
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 04 | [API Server故障](./04-apiserver-troubleshooting.md) | 请求超时、认证失败 |
| 05 | [etcd故障](./05-etcd-troubleshooting.md) | 数据损坏、性能问题 |
| 06 | [Scheduler故障](./06-scheduler-troubleshooting.md) | 调度失败、资源不足 |

### 数据平面故障
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 07 | [Kubelet故障](./07-kubelet-troubleshooting.md) | 节点状态、Pod生命周期 |
| 08 | [容器运行时故障](./08-container-runtime-troubleshooting.md) | Docker/containerd问题 |
| 09 | [网络故障](./09-network-troubleshooting.md) | CNI、DNS、Service问题 |

### 工作负载故障
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 10 | [Pod启动失败](./10-pod-startup-failure.md) | 镜像拉取、资源限制 |
| 11 | [Pod运行异常](./11-pod-runtime-issues.md) | OOM、健康检查失败 |
| 12 | [Service不可达](./12-service-unreachable.md) | 网络策略、DNS解析 |

### 存储故障
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 13 | [PV/PVC故障](./13-pv-pvc-troubleshooting.md) | 挂载失败、容量问题 |
| 14 | [CSI驱动故障](./14-csi-driver-troubleshooting.md) | 存储驱动问题 |

### 安全故障
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 15 | [RBAC权限问题](./15-rbac-permission-issues.md) | 权限拒绝、角色配置 |
| 16 | [证书问题](./16-certificate-issues.md) | 证书过期、信任链 |

---

## 故障排查流程

```
1. 问题定义 → 明确故障现象
2. 信息收集 → 日志、事件、指标
3. 问题定位 → 缩小故障范围
4. 根因分析 → 找到根本原因
5. 解决验证 → 应用修复并验证
```

---

## 相关专题

- **[结构化故障排查](../topic-structural-trouble-shooting/)** - 详细故障排查指南
- **[故障树分析](../topic-fta/)** - FTA方法论
- **[可观测性](../observability-advanced/)** - 监控告警体系

---

**维护者**: OpenDemo Team | **许可证**: MIT
