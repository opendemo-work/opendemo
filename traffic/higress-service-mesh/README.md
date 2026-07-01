# Higress 服务网格演示 - 微服务流量治理

> 使用 Higress 作为服务网格数据面，演示微服务间的流量管理、服务发现、熔断限流和可观测性。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解服务网格与 API 网关的区别
- ✅ 使用 Higress 实现服务间流量治理
- ✅ 配置服务发现、负载均衡和熔断
- ✅ 了解 Sidecar 和 Sidecar-less 两种模式

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Higress 服务网格架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    Service A ──┐                                                │
│                ├──▶ Higress Sidecar/Proxy ──▶ Service B        │
│    Service C ──┘                                                │
│                                                                 │
│              ┌─────────────────────────────┐                   │
│              │ 服务发现 / mTLS / 流量治理   │                   │
│              │ 熔断 / 重试 / 超时 / 可观测性 │                   │
│              └─────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd traffic/higress-service-mesh
./scripts/start.sh
sleep 20
./scripts/check.sh
```

---

## 📖 核心概念

### 1. 服务网格（Service Mesh）

服务网格是处理服务间通信的基础设施层，将流量管理、安全、可观测性从应用代码中剥离出来。

### 2. Sidecar 模式

每个服务实例旁边部署一个代理（如 Envoy），所有进出流量都经过代理。

### 3. Sidecar-less 模式

Higress 支持无 Sidecar 模式，通过节点级或命名空间级代理减少资源开销。

### 4. 流量治理

- **负载均衡**：round-robin、least-request、consistent-hash
- **熔断**：基于错误率或慢请求的熔断策略
- **重试/超时**：自动重试失败请求，设置超时时间
- **灰度发布**：基于 Header、权重的流量切分

---

## 💻 代码示例

### 服务注册

```yaml
# configs/service-registry.yaml
apiVersion: networking.higress.io/v1
kind: McpBridge
metadata:
  name: default
spec:
  registries:
    - type: static
      name: demo-services
      services:
        - name: order-service
          domain: order-service
          port: 8080
        - name: payment-service
          domain: payment-service
          port: 8080
```

### 流量策略

```yaml
# configs/traffic-policy.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: order-service-policy
spec:
  host: order-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `configs/service-registry.yaml` | 服务注册配置 |
| `configs/traffic-policy.yaml` | 流量治理策略 |
| `docker-compose.yml` | 服务编排 |

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 调用服务 A，观察流量是否经过 Higress 治理
curl -s http://localhost:8080/order-service/orders

# 查看服务列表
curl -s http://localhost:8080/api/v1/services
```

---

## 📚 扩展学习

- [Higress API 网关](../higress-api-gateway/)
- [Kubernetes 服务网格](../kubernetes/service-mesh/)
- [Higress 官方文档](https://higress.io/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
