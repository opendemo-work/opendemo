# Domain-13: Docker容器技术

> **案例数量**: 15+ 个 | **最后更新**: 2026-03 | **适用版本**: Docker 24.0+

---

## 概述

Docker容器技术域涵盖容器基础、镜像管理、网络配置、存储管理、安全实践等核心内容，为Kubernetes容器编排提供坚实基础。

**核心价值**：
- 🐳 **容器基础**：Docker核心概念和操作
- 📦 **镜像管理**：镜像构建、优化、分发
- 🔧 **生产实践**：安全加固、性能优化

---

## 案例目录

### 容器基础
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [Docker架构概览](./01-docker-architecture-overview.md) | 架构组件、工作原理 |
| 02 | [容器生命周期管理](./02-container-lifecycle-management.md) | 创建、启动、停止、删除 |
| 03 | [Dockerfile最佳实践](./03-dockerfile-best-practices.md) | 镜像构建、优化技巧 |

### 镜像管理
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 04 | [镜像仓库管理](./04-image-registry-management.md) | Harbor、Docker Hub |
| 05 | [镜像安全扫描](./05-image-security-scanning.md) | Trivy、Clair扫描 |
| 06 | [多阶段构建](./06-multi-stage-builds.md) | 镜像瘦身、优化 |

### 网络配置
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 07 | [Docker网络模式](./07-docker-network-modes.md) | Bridge、Host、Overlay |
| 08 | [容器网络配置](./08-container-networking.md) | 网络驱动、DNS配置 |

### 存储管理
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 09 | [Docker存储驱动](./09-docker-storage-drivers.md) | Overlay2、DeviceMapper |
| 10 | [数据卷管理](./10-volume-management.md) | Bind Mount、Volume |

### 安全实践
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 11 | [容器安全加固](./11-container-security-hardening.md) | 安全配置、最佳实践 |
| 12 | [Docker Bench Security](./12-docker-bench-security.md) | 安全基准检查 |

### 生产运维
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 13 | [Docker监控](./13-docker-monitoring.md) | 指标采集、告警配置 |
| 14 | [Docker日志管理](./14-docker-logging.md) | 日志驱动、收集分析 |
| 15 | [Docker性能调优](./15-docker-performance-tuning.md) | 资源限制、优化建议 |

---

## 相关领域

- **[容器镜像管理](../container-image-management/)** - 企业级镜像管理
- **[安全](../security-advanced/)** - 容器安全实践
- **[Kubernetes](../architecture-fundamentals/)** - 容器编排平台

---

**维护者**: OpenDemo Team | **许可证**: MIT
