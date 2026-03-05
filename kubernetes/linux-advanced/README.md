# Domain-14: Linux系统管理

> **案例数量**: 20+ 个 | **最后更新**: 2026-03 | **适用版本**: CentOS 7+/Ubuntu 20.04+

---

## 概述

Linux系统管理域涵盖系统管理、网络配置、存储管理、性能调优、安全加固等核心内容，为Kubernetes节点运维提供坚实基础。

**核心价值**：
- 🐧 **系统管理**：用户、权限、进程管理
- 🌐 **网络配置**：网络接口、防火墙、DNS
- 💾 **存储管理**：磁盘分区、文件系统、LVM
- ⚡ **性能调优**：内核参数、资源优化

---

## 案例目录

### 系统管理
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [用户与权限管理](./01-user-permission-management.md) | 用户创建、权限配置 |
| 02 | [进程管理](./02-process-management.md) | 进程监控、资源限制 |
| 03 | [服务管理](./03-service-management.md) | systemd服务配置 |

### 网络配置
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 04 | [网络接口配置](./04-network-interface-configuration.md) | IP配置、网卡绑定 |
| 05 | [防火墙配置](./05-firewall-configuration.md) | iptables、firewalld |
| 06 | [DNS配置](./06-dns-configuration.md) | 解析配置、缓存优化 |

### 存储管理
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 07 | [磁盘分区管理](./07-disk-partition-management.md) | 分区创建、格式化 |
| 08 | [LVM逻辑卷管理](./08-lvm-management.md) | 卷组、逻辑卷配置 |
| 09 | [文件系统管理](./09-filesystem-management.md) | ext4、xfs配置优化 |

### 性能调优
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 10 | [内核参数调优](./10-kernel-parameter-tuning.md) | sysctl配置优化 |
| 11 | [内存管理优化](./11-memory-management-optimization.md) | 内存监控、优化 |
| 12 | [CPU调度优化](./12-cpu-scheduling-optimization.md) | CPU亲和性、调度策略 |

### 安全加固
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 13 | [SSH安全配置](./13-ssh-security-configuration.md) | 密钥认证、安全加固 |
| 14 | [SELinux配置](./14-selinux-configuration.md) | 策略配置、故障排查 |
| 15 | [审计日志配置](./15-audit-log-configuration.md) | auditd配置、日志分析 |

### 故障排查
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 16 | [系统故障诊断](./16-system-fault-diagnosis.md) | 故障定位、分析工具 |
| 17 | [性能问题排查](./17-performance-troubleshooting.md) | 性能瓶颈定位 |
| 18 | [网络故障排查](./18-network-troubleshooting.md) | 网络连通性诊断 |

---

## 相关领域

- **[控制平面](../control-plane/)** - Kubelet配置
- **[网络基础](../network-fundamentals/)** - 网络基础知识
- **[存储基础](../storage-fundamentals/)** - 存储基础知识

---

**维护者**: OpenDemo Team | **许可证**: MIT
