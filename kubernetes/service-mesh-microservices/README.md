# Domain-26: 服务网格与微服务

> **案例数量**: 18+ 个 | **最后更新**: 2026-03 | **专业级别**: 企业级生产环境

---

## 概述

服务网格与微服务域涵盖服务网格架构、Istio/Linkerd实践、微服务设计模式、流量管理等内容。

**核心价值**：
- 🌐 **服务网格**：Istio、Linkerd深度实践
- 📦 **微服务架构**：设计模式、最佳实践
- 🔄 **流量管理**：智能路由、故障注入
- 🔒 **安全通信**：mTLS、访问控制

---

## 案例目录

### 服务网格基础
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [服务网格架构概览](./01-service-mesh-architecture-overview.md) | 架构原理、组件分析 |
| 02 | [服务网格选型指南](./02-service-mesh-selection-guide.md) | Istio vs Linkerd对比 |
| 03 | [服务网格部署模式](./03-service-mesh-deployment-patterns.md) | 单集群、多集群、联邦 |

### Istio实践
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 04 | [Istio安装配置](./04-istio-installation-configuration.md) | 安装方式、配置优化 |
| 05 | [Istio流量管理](./05-istio-traffic-management.md) | VirtualService、DestinationRule |
| 06 | [Istio安全配置](./06-istio-security-configuration.md) | mTLS、授权策略 |
| 07 | [Istio可观测性](./07-istio-observability.md) | Kiali、Jaeger集成 |

### Linkerd实践
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 08 | [Linkerd安装配置](./08-linkerd-installation-configuration.md) | 安装方式、配置优化 |
| 09 | [Linkerd流量管理](./09-linkerd-traffic-management.md) | 服务配置、流量分割 |
| 10 | [Linkerd安全配置](./10-linkerd-security-configuration.md) | mTLS、RBAC |

### 微服务设计
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 11 | [微服务设计模式](./11-microservice-design-patterns.md) | 服务拆分、通信模式 |
| 12 | [API网关设计](./12-api-gateway-design.md) | 网关选型、路由设计 |
| 13 | [服务发现机制](./13-service-discovery-mechanism.md) | 注册中心、健康检查 |

### 流量管理
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 14 | [灰度发布实践](./14-canary-deployment-practices.md) | 流量分割、渐进发布 |
| 15 | [故障注入测试](./15-fault-injection-testing.md) | 混沌工程、弹性测试 |
| 16 | [流量镜像实践](./16-traffic-mirroring-practices.md) | 流量复制、测试验证 |

### 服务网格运维
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 17 | [服务网格监控](./17-service-mesh-monitoring.md) | 指标采集、仪表板 |
| 18 | [服务网格故障排查](./18-service-mesh-troubleshooting.md) | 常见问题、解决方案 |

---

## 相关领域

- **[网络管理](../network-advanced/)** - Kubernetes网络
- **[安全](../security-advanced/)** - 安全通信
- **[可观测性](../observability-advanced/)** - 分布式追踪

---

**维护者**: OpenDemo Team | **许可证**: MIT
