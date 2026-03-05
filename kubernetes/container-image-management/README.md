# Domain-22: 容器镜像管理

> **案例数量**: 15+ 个 | **最后更新**: 2026-03 | **专业级别**: 企业级生产环境

---

## 概述

容器镜像管理域涵盖企业级镜像仓库管理、镜像构建优化、安全扫描、镜像分发等内容。

**核心价值**：
- 📦 **镜像仓库**：Harbor企业级仓库管理
- 🔧 **构建优化**：多阶段构建、镜像瘦身
- 🔒 **安全扫描**：漏洞扫描、签名验证
- 🌐 **镜像分发**：多机房同步、加速分发

---

## 案例目录

### 镜像仓库管理
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [Harbor企业部署](./01-harbor-enterprise-deployment.md) | HA部署、存储配置 |
| 02 | [Harbor权限管理](./02-harbor-permission-management.md) | 项目、用户、角色管理 |
| 03 | [镜像仓库安全](./03-registry-security.md) | HTTPS、认证、访问控制 |

### 镜像构建
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 04 | [Dockerfile最佳实践](./04-dockerfile-best-practices.md) | 构建技巧、优化建议 |
| 05 | [多阶段构建实践](./05-multi-stage-build-practices.md) | 镜像瘦身、构建优化 |
| 06 | [Kaniko无守护构建](./06-kaniko-daemonless-build.md) | CI/CD集成、安全构建 |

### 镜像安全
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 07 | [镜像安全扫描](./07-image-security-scanning.md) | Trivy、Clair扫描集成 |
| 08 | [镜像签名验证](./08-image-signing-verification.md) | Notary、Cosign签名 |
| 09 | [镜像准入控制](./09-image-admission-control.md) | 策略验证、自动拦截 |

### 镜像分发
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 10 | [镜像同步策略](./10-image-synchronization-strategy.md) | 多机房同步、跨云复制 |
| 11 | [镜像缓存加速](./11-image-cache-acceleration.md) | 代理缓存、P2P分发 |
| 12 | [大镜像优化](./12-large-image-optimization.md) | 分层优化、压缩传输 |

### 镜像运维
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 13 | [镜像清理策略](./13-image-cleanup-strategy.md) | 垃圾回收、存储优化 |
| 14 | [镜像仓库监控](./14-registry-monitoring.md) | 指标采集、告警配置 |
| 15 | [镜像灾备方案](./15-registry-disaster-recovery.md) | 备份恢复、高可用 |

---

## 相关领域

- **[Docker技术](../docker-advanced/)** - 容器基础
- **[安全](../security-advanced/)** - 镜像安全
- **[CI/CD](../gitops-ci-cd/)** - 构建流水线

---

**维护者**: OpenDemo Team | **许可证**: MIT
