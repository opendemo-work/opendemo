# Domain-16: 存储基础

> **案例数量**: 12+ 个 | **最后更新**: 2026-03 | **适用场景**: 存储工程师、运维工程师

---

## 概述

存储基础域涵盖存储架构、磁盘技术、文件系统、存储网络等核心存储知识，为Kubernetes存储管理提供理论基础。

**核心价值**：
- 💾 **存储架构**：DAS、NAS、SAN存储架构
- 📀 **磁盘技术**：HDD、SSD、NVMe技术
- 📁 **文件系统**：ext4、xfs、分布式文件系统
- 🔗 **存储网络**：iSCSI、FC、NVMe-oF

---

## 案例目录

### 存储架构
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [存储架构概览](./01-storage-architecture-overview.md) | DAS/NAS/SAN对比 |
| 02 | [存储性能指标](./02-storage-performance-metrics.md) | IOPS、吞吐量、延迟 |

### 磁盘技术
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 03 | [磁盘技术原理](./03-disk-technology-principles.md) | HDD/SSD/NVMe对比 |
| 04 | [RAID技术详解](./04-raid-technology-details.md) | RAID级别、配置实践 |

### 文件系统
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 05 | [ext4文件系统](./05-ext4-filesystem.md) | 特性、配置、优化 |
| 06 | [XFS文件系统](./06-xfs-filesystem.md) | 特性、配置、优化 |
| 07 | [分布式文件系统](./07-distributed-filesystem.md) | Ceph、GlusterFS |

### 存储网络
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 08 | [iSCSI配置实践](./08-iscsi-configuration.md) | Target/Initiator配置 |
| 09 | [光纤通道FC](./09-fibre-channel.md) | FC网络架构 |
| 10 | [NVMe-oF技术](./10-nvme-of-technology.md) | 高性能存储网络 |

### 数据保护
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 11 | [数据备份策略](./11-data-backup-strategy.md) | 备份方案、恢复流程 |
| 12 | [存储容灾方案](./12-storage-disaster-recovery.md) | 同步/异步复制 |

---

## 相关领域

- **[存储管理](../storage-advanced/)** - Kubernetes存储
- **[Linux系统](../linux-advanced/)** - Linux存储配置
- **[灾难恢复](../disaster-recovery-business-continuity/)** - 数据保护

---

**维护者**: OpenDemo Team | **许可证**: MIT
