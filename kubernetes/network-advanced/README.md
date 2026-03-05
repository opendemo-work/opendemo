# Domain-5: Kubernetes网络管理

> **案例数量**: 37 个 | **最后更新**: 2026-03 | **状态**: 生产环境就绪

---

## 概述

Kubernetes网络管理域全面覆盖网络架构、CNI插件、Service服务、DNS发现、Ingress入口、网络策略、服务网格等核心技术。为企业构建生产级网络架构提供完整指导。

**核心价值**：
- 🌐 **网络架构**：深入理解K8s网络模型和CNI机制
- 🔗 **服务发现**：Service、CoreDNS、服务网格集成
- 🛡️ **网络安全**：NetworkPolicy、mTLS、零信任模型
- 📊 **性能优化**：网络调优、故障排查、监控告警

---

## 案例目录

### 1. 网络基础架构 (01-05)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 01 | [网络架构概览](./01-network-architecture-overview/) | 网络架构概览与核心组件 | ⭐⭐⭐⭐⭐ |
| 02 | [CNI架构基础](./02-cni-architecture-fundamentals/) | CNI 架构基础与核心原理 | ⭐⭐⭐⭐⭐ |
| 03 | [CNI插件对比](./03-cni-plugins-comparison/) | CNI 插件对比与选型指南 | ⭐⭐⭐⭐ |
| 04 | [Flannel完整指南](./04-flannel-complete-guide/) | Flannel 完整指南 | ⭐⭐⭐⭐ |
| 05 | [Terway高级指南](./05-terway-advanced-guide/) | Terway 高级指南 | ⭐⭐⭐⭐⭐ |

### 2. Service 服务 (06-10)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 06 | [Service概念与类型](./06-service-concepts-types/) | Service 概念与类型深度解析 | ⭐⭐⭐⭐⭐ |
| 07 | [Service实现细节](./07-service-implementation-details/) | Service 实现细节 | ⭐⭐⭐⭐ |
| 08 | [Service拓扑感知](./08-service-topology-aware/) | Service 拓扑感知 | ⭐⭐⭐⭐ |
| 09 | [kube-proxy模式与性能](./09-kube-proxy-modes-performance/) | kube-proxy 模式与性能优化 | ⭐⭐⭐⭐⭐ |
| 10 | [Service高级特性](./10-service-advanced-features/) | Service 高级特性 | ⭐⭐⭐⭐ |

### 3. DNS 服务发现 (11-15)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 11 | [DNS服务发现CoreDNS](./11-dns-service-discovery-coredns/) | DNS 服务发现与 CoreDNS 调优 | ⭐⭐⭐⭐⭐ |
| 12 | [DNS服务发现](./12-dns-service-discovery/) | DNS 服务发现 | ⭐⭐⭐⭐ |
| 13 | [CoreDNS架构原理](./13-coredns-architecture-principles/) | CoreDNS 架构原理 | ⭐⭐⭐⭐ |
| 14 | [CoreDNS配置Corefile](./14-coredns-configuration-corefile/) | CoreDNS 配置 Corefile | ⭐⭐⭐⭐ |
| 15 | [CoreDNS插件参考](./15-coredns-plugins-reference/) | CoreDNS 插件参考 | ⭐⭐⭐⭐ |

### 4. 网络策略与安全 (16-18)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 16 | [NetworkPolicy深度实践](./16-networkpolicy-deep-practice/) | NetworkPolicy 深度实践指南 | ⭐⭐⭐⭐⭐ |
| 17 | [NetworkPolicy高级配置](./17-network-policy-advanced/) | NetworkPolicy 高级配置 | ⭐⭐⭐⭐ |
| 18 | [网络加密与mTLS](./18-network-encryption-mtls/) | 网络加密与 mTLS | ⭐⭐⭐⭐⭐ |

### 5. Ingress 入站流量 (19-26)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 19 | [Ingress基础概念](./19-ingress-fundamentals/) | Ingress 基础概念与核心原理 | ⭐⭐⭐⭐⭐ |
| 20 | [Ingress Controller深入](./20-ingress-controller-deep-dive/) | Ingress Controller 深入解析 | ⭐⭐⭐⭐⭐ |
| 21 | [Nginx Ingress完整指南](./21-nginx-ingress-complete-guide/) | Nginx Ingress 完整指南 | ⭐⭐⭐⭐⭐ |
| 22 | [Ingress TLS证书](./22-ingress-tls-certificate/) | Ingress TLS 证书管理 | ⭐⭐⭐⭐ |
| 23 | [Ingress高级路由](./23-ingress-advanced-routing/) | Ingress 高级路由配置 | ⭐⭐⭐⭐ |
| 24 | [Ingress安全加固](./24-ingress-security-hardening/) | Ingress 安全加固 | ⭐⭐⭐⭐⭐ |
| 25 | [Ingress监控与排错](./25-ingress-monitoring-troubleshooting/) | Ingress 监控与排错 | ⭐⭐⭐⭐ |
| 26 | [Ingress生产最佳实践](./26-ingress-production-best-practices/) | Ingress 生产最佳实践 | ⭐⭐⭐⭐⭐ |

### 6. 网络故障排查 (27-29)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 27 | [CNI故障排查优化](./27-cni-troubleshooting-optimization/) | CNI 故障排查与优化 | ⭐⭐⭐⭐ |
| 28 | [CoreDNS故障排查](./28-coredns-troubleshooting-optimization/) | CoreDNS 故障排查与优化 | ⭐⭐⭐⭐ |
| 29 | [出站流量管理](./29-egress-traffic-management/) | 出站流量管理 | ⭐⭐⭐⭐ |

### 7. 高级主题 (30-37)
| # | 案例 | 关键内容 | 重要程度 |
|:---:|:---|:---|:---|
| 30 | [Service Mesh深度解析](./30-service-mesh-deep-dive/) | Service Mesh 深度解析与生产实践 | ⭐⭐⭐⭐⭐ |
| 31 | [多集群网络联邦](./31-multi-cluster-federation/) | 多集群网络联邦与跨集群通信 | ⭐⭐⭐⭐⭐ |
| 32 | [多集群网络](./32-multi-cluster-networking/) | 多集群网络 | ⭐⭐⭐⭐ |
| 33 | [网络故障排查](./33-network-troubleshooting/) | 网络故障排查 | ⭐⭐⭐⭐⭐ |
| 34 | [网络性能调优](./34-network-performance-tuning/) | 网络性能调优 | ⭐⭐⭐⭐⭐ |
| 35 | [Gateway API概览](./35-gateway-api-overview/) | Gateway API 概览 | ⭐⭐⭐⭐⭐ |
| 36 | [API网关模式](./36-api-gateway-patterns/) | API 网关模式 | ⭐⭐⭐⭐⭐ |
| 37 | [Terway实例CRUD操作](./37-terway-resources-crud-operations/) | Terway 实例 CRUD 操作指南 | ⭐⭐⭐⭐⭐ |

---

## 学习路径建议

### 初级阶段 (01-10)
1. 先学习网络架构概览 (01)
2. 掌握 CNI 基础概念 (02-05)
3. 理解 Service 核心概念 (06-10)

### 中级阶段 (11-20)
1. 深入学习 DNS 服务发现 (11-15)
2. 掌握 NetworkPolicy 基础配置 (16-17)
3. 学习 Ingress 入站流量管理 (19-21)

### 高级阶段 (21-37)
1. 网络策略深度实践 (16)
2. 服务网格生产部署 (30)
3. 多集群网络联邦 (31)
4. 网络性能优化 (34)
5. Terway 实例管理 (37)

---

## 相关领域

- **[架构基础](../architecture-fundamentals)** - Kubernetes核心架构
- **[控制平面](../control-plane)** - kube-proxy配置
- **[安全](../security-advanced)** - 网络安全策略
- **[云原生API网关](../cloud-native-api-gateway)** - API网关深度实践

---

**维护者**: OpenDemo Team | **许可证**: MIT
