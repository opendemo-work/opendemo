# Domain-98: 云原生 API 网关技术体系

> **适用范围**: 云原生 API 网关、Ingress 控制器、Gateway API | **维护状态**: 持续更新中 | **专家级别**: ⭐⭐⭐⭐⭐ | **更新时间**: 2026-03

---

## 领域概览

本领域专注于云原生 API 网关技术栈的深度实践，涵盖 Higress、Apache APISIX、Kong、Envoy Gateway、Traefik 等主流开源 API 网关产品。领域范围聚焦于南北向（Ingress）流量治理，包括 Kubernetes Gateway API 标准、Wasm 插件生态、API 安全体系、可观测性集成以及生产环境最佳实践。

**核心价值**：
- 🌐 **流量管理**：路由、负载均衡、流量控制
- 🔐 **安全防护**：认证授权、WAF、限流熔断
- 📊 **可观测性**：监控、日志、链路追踪
- 🚀 **高性能**：高并发、低延迟、弹性扩展

---

## 案例目录

### 🎯 基础理论与标准 (01-03)
| # | 案例 | 关键内容 | 技术深度 |
|:---:|:---|:---|:---|
| 01 | [云原生API网关架构总览](./01-api-gateway-architecture-overview/) | API 网关 vs Ingress 控制器 vs 服务网格网关；请求生命周期；控制平面/数据平面分离 | ⭐⭐⭐⭐ |
| 02 | [Kubernetes Gateway API标准深度解析](./02-kubernetes-gateway-api-deep-dive/) | GatewayClass/Gateway/HTTPRoute/ReferenceGrant CRD 体系；角色模型；v1.0/v1.1 GA | ⭐⭐⭐⭐⭐ |
| 03 | [API网关选型指南与对比矩阵](./03-api-gateway-selection-guide/) | 12+ 维度功能矩阵；场景决策框架；TCO 分析；迁移成本评估 | ⭐⭐⭐ |

### 🌐 主流产品深度实践 (04-09)
| # | 案例 | 关键内容 | 技术深度 |
|:---:|:---|:---|:---|
| 04 | [Higress云原生API网关企业级实践](./04-higress-enterprise-gateway/) | Istiod 控制平面 + Envoy 数据平面架构；AI 网关能力；Gateway API 一致性 | ⭐⭐⭐⭐⭐ |
| 05 | [Apache APISIX企业级API网关实践](./05-apisix-enterprise-gateway/) | etcd 控制平面 + OpenResty 数据平面；100+ 插件；Wasm 支持 | ⭐⭐⭐⭐⭐ |
| 06 | [Kong API网关企业级实践](./06-kong-enterprise-gateway/) | PostgreSQL/DB-less/Konnect 模式；KIC 架构；Gateway API 一致性 | ⭐⭐⭐⭐⭐ |
| 07 | [Envoy Gateway企业级实践](./07-envoy-gateway-enterprise/) | Envoy 官方项目；Gateway API 原生 API 接口；Wasm 集成 | ⭐⭐⭐⭐⭐ |
| 08 | [Traefik API网关企业级实践](./08-traefik-enterprise-gateway/) | Traefik v3 架构；Provider（K8s CRD/Ingress/Gateway API）；TLS 自动化 | ⭐⭐⭐⭐ |
| 09 | [传统Ingress控制器向云原生API网关迁移](./09-nginx-ingress-migration-guide/) | 功能差距分析；迁移模式；零停机迁移清单 | ⭐⭐⭐⭐ |

### 🔧 核心能力专题 (10-12)
| # | 案例 | 关键内容 | 技术深度 |
|:---:|:---|:---|:---|
| 10 | [Wasm插件生态与开发实践](./10-wasm-plugin-ecosystem/) | proxy-wasm ABI 规范；Go/Rust Wasm 插件开发；性能开销分析 | ⭐⭐⭐⭐⭐ |
| 11 | [API网关安全体系：认证、鉴权与WAF](./11-api-gateway-security-practices/) | JWT/OIDC/mTLS/API Key 认证；OPA 集成；WAF（ModSecurity）；限流策略 | ⭐⭐⭐⭐⭐ |
| 12 | [API网关可观测性：指标、日志与链路追踪](./12-api-gateway-observability/) | 黄金信号；Prometheus 指标；OpenTelemetry 集成；Grafana 仪表盘 | ⭐⭐⭐⭐ |

### ⚡ 生产运维与高级主题 (13-14)
| # | 案例 | 关键内容 | 技术深度 |
|:---:|:---|:---|:---|
| 13 | [API网关性能基准测试与调优](./13-api-gateway-performance-benchmarks/) | 基准测试方法论；Higress/APISIX/Kong 对比；调优参数；eBPF 加速 | ⭐⭐⭐⭐⭐ |
| 14 | [API网关生产运维最佳实践](./14-api-gateway-production-operations/) | HA 部署模式；滚动升级；GitOps 配置管理；灾备预案；容量规划 | ⭐⭐⭐⭐⭐ |

---

## 学习路径建议

### 🔰 入门阶段
1. **01-架构总览** → 理解 API 网关核心概念与分类
2. **02-Gateway API** → 掌握 Kubernetes 标准网关接口
3. **03-选型指南** → 根据场景选择合适产品

### ⭐ 进阶阶段
1. **04~08-产品深度实践** → 根据团队技术栈选择对应产品深入学习
2. **10-Wasm 插件** → 掌握现代网关插件开发模式
3. **09-迁移指南** → 从传统 Ingress 迁移到云原生 API 网关

### 🔒 专家阶段
1. **11-安全体系** → 构建企业级 API 安全边界
2. **12-可观测性** → 建立网关层全链路可观测体系
3. **13-性能调优** → 基准测试与生产环境性能优化
4. **14-生产运维** → 大规模网关集群运维最佳实践

---

## 核心技术栈

```bash
# 主流 API 网关产品
Higress (CNCF Sandbox)              # 阿里云开源，AI 网关能力
Apache APISIX (Apache TLP)          # 高性能，100+ 插件
Kong (Kong Inc.)                    # 企业级 API 平台
Envoy Gateway (CNCF/Envoy)         # Gateway API 原生实现
Traefik (Traefik Labs)             # 轻量级，自动化 TLS

# 标准与规范
Kubernetes Gateway API v1.1         # 统一网关标准接口
proxy-wasm ABI                      # Wasm 插件标准接口

# 插件运行时
Wasm (TinyGo/Rust/AssemblyScript)  # 跨语言安全沙箱
Lua (OpenResty/LuaJIT)             # APISIX/Kong 原生
Go/Java Plugin Runner              # 多语言插件运行时

# 安全组件
OPA (Open Policy Agent)            # 策略引擎
ModSecurity                        # WAF 引擎
cert-manager                       # 证书自动化

# 可观测性
OpenTelemetry                      # 统一遥测框架
Prometheus + Grafana               # 指标监控
```

---

## 相关领域链接

- **[网络](../network-advanced)** - Kubernetes 网络架构、Ingress 基础、Gateway API 概览
- **[安全](../security-advanced)** - 安全架构基础
- **[可观测性](../observability-advanced)** - 监控告警体系基础

---

**维护者**: OpenDemo Team | **许可证**: MIT
