# Higress API 网关演示 - 云原生网关入门

> 使用 Docker 部署 Higress 云原生 API 网关，演示路由配置、限流、认证和插件扩展能力。

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

- ✅ 理解 Higress 作为云原生 API 网关的定位
- ✅ 使用 Docker 部署 Higress
- ✅ 配置路由规则将请求转发到后端服务
- ✅ 了解 Higress 的 Wasm 插件机制

---

## 📐 架构图

```
客户端 ──▶ Higress Gateway ──┬─▶ /api/v1/users ──▶ user-service
                             ├─▶ /api/v1/orders ──▶ order-service
                             └─▶ /api/v1/pay ────▶ pay-service
```

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd traffic/higress-api-gateway
./scripts/start.sh
sleep 20
./scripts/check.sh
```

访问 Higress 控制台：

```
http://localhost:8080
```

---

## 📖 核心概念

### 1. Higress

Higress 是基于 Envoy + Istio + WASM 构建的云原生 API 网关，提供：

- 南北向流量管理
- 安全防护（认证、鉴权、WAF）
- 协议转换（HTTP <> Dubbo）
- 可观测性

### 2. 路由（Route）

将请求按域名、路径、Header 等条件路由到不同后端。

### 3. Wasm 插件

Higress 支持使用 WebAssembly 编写插件，实现自定义逻辑：

- 认证鉴权
- 限流熔断
- 请求/响应改写
- 日志记录

---

## 💻 代码示例

### 路由配置（Kubernetes CRD）

```yaml
# configs/route.yaml
apiVersion: networking.higress.io/v1
kind: McpBridge
metadata:
  name: default
spec:
  registries:
    - type: static
      name: static-service
      domain: "localhost"
      port: 8080
      services:
        - name: user-service
          domain: user-service
          port: 8080
---
apiVersion: networking.higress.io/v1
kind: Ingress
metadata:
  name: api-route
  annotations:
    higress.io/destination: user-service
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /api/v1/users
            pathType: Prefix
            backend:
              service:
                name: user-service
                port:
                  number: 8080
```

### 限流插件配置

```yaml
apiVersion: extensions.higress.io/v1alpha1
kind: WasmPlugin
metadata:
  name: rate-limit
spec:
  defaultConfig:
    limit_by_conSUMER: false
    limit_keys:
      - key: "_default_"
        query_per_minute: 60
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `configs/route.yaml` | Higress 路由规则 |
| `configs/plugin.yaml` | Wasm 插件配置 |
| `docker-compose.yml` | Higress 服务编排 |

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 测试路由
curl -H "Host: api.example.com" http://localhost/api/v1/users

# 检查网关状态
curl -s http://localhost:8080/api/v1/status
```

---

## 📚 扩展学习

- [Higress 服务网格](../higress-service-mesh/)
- [NGINX 反向代理](../nginx-reverse-proxy/)
- [Higress 官方文档](https://higress.io/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 🔐 Higress 认证鉴权插件

Higress 通过 Wasm 插件实现灵活的认证鉴权，常见插件包括：

### JWT 认证

```yaml
apiVersion: extensions.higress.io/v1alpha1
kind: WasmPlugin
metadata:
  name: jwt-auth
spec:
  defaultConfig:
    consumers:
      - name: consumer1
        key: abc-123
    allow:
      - consumer1
```

### 黑白名单

```yaml
apiVersion: extensions.higress.io/v1alpha1
kind: WasmPlugin
metadata:
  name: ip-restriction
spec:
  defaultConfig:
    ip_blacklist:
      - "192.168.1.100"
```

插件机制使 Higress 能够快速扩展安全能力。
