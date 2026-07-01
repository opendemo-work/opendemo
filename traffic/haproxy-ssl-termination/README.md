# HAProxy SSL 终止演示 - HTTPS 安全入口

> 使用 HAProxy 作为 SSL/TLS 终止点，将客户端 HTTPS 流量解密后转发给后端 HTTP 服务，演示证书生成、HTTPS 前端配置、TLS 版本控制和 HSTS 安全头。

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

- ✅ 理解 SSL/TLS 终止的作用和优势
- ✅ 使用 OpenSSL 生成自签名证书
- ✅ 在 HAProxy 中配置 HTTPS 前端和证书绑定
- ✅ 配置 TLS 版本、加密套件和 HSTS 安全头
- ✅ 验证 HTTPS 连接和证书信息

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    HAProxy SSL 终止架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   客户端 (HTTPS) ──▶ HAProxy :443 ──▶ 后端 HTTP 服务 :8080     │
│                       (SSL/TLS 解密)                            │
│                                                                 │
│              ┌─────────────────────────────┐                   │
│              │ server.crt + server.key     │                   │
│              │ TLS 1.2+ / 强加密套件        │                   │
│              │ HSTS Header                 │                   │
│              └─────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 HAProxy 容器 |
| Docker Compose | >= 1.29 | 编排服务 |
| OpenSSL | >= 1.1.1 | 生成自签名证书 |

### 启动服务

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd traffic/haproxy-ssl-termination
./scripts/start.sh
sleep 5
./scripts/check.sh
```

### 生成证书

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 生成自签名证书（如尚未生成）
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/server.key \
  -out certs/server.crt \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

# 合并为 HAProxy 需要的 PEM 格式
cat certs/server.crt certs/server.key > certs/server.pem
```

### 测试 HTTPS 访问

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 使用 -k 跳过自签名证书验证
curl -k https://localhost/

# 查看证书详情
openssl s_client -connect localhost:443 -servername localhost </dev/null
```

---

## 📖 核心概念

### 1. SSL/TLS 终止

在负载均衡器或网关上完成 HTTPS 解密，后端服务使用普通 HTTP 通信：

- **优势**：简化后端证书管理，统一安全策略，提升后端性能
- **适用场景**：微服务架构、内部网络可信、需要集中安全审计

### 2. 证书格式

HAProxy 要求将证书和私钥合并为 PEM 文件：

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
cat server.crt server.key > server.pem
```

### 3. TLS 版本控制

禁用不安全的 TLS 1.0/1.1，仅允许 TLS 1.2+：

```haproxy
bind *:443 ssl crt /path/server.pem ssl-min-ver TLSv1.2
```

### 4. HSTS

HTTP Strict Transport Security 强制客户端使用 HTTPS：

```haproxy
http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

---

## 💻 代码示例

### HAProxy 配置

```haproxy
# configs/haproxy.cfg
global
    daemon
    maxconn 4096
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    mode http
    timeout connect 5s
    timeout client 30s
    timeout server 30s

frontend https_frontend
    bind *:443 ssl crt /usr/local/etc/haproxy/certs/server.pem ssl-min-ver TLSv1.2
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains"
    http-response set-header X-Frame-Options DENY
    default_backend web_servers

backend web_servers
    server web1 web1:8080 check
```

### Docker Compose 挂载证书

```yaml
services:
  haproxy:
    image: haproxy:lts
    ports:
      - "443:443"
    volumes:
      - ./configs/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
      - ./certs/server.pem:/usr/local/etc/haproxy/certs/server.pem:ro
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `certs/server.crt` | 服务器证书 |
| `certs/server.key` | 服务器私钥 |
| `certs/server.pem` | HAProxy 使用的合并 PEM 文件 |
| `configs/haproxy.cfg` | HAProxy SSL 配置 |

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 检查 HAProxy 配置
docker exec haproxy-ssl-termination haproxy -c -f /usr/local/etc/haproxy/haproxy.cfg

# 测试 HTTPS 访问
curl -k -I https://localhost/

# 检查 TLS 版本和加密套件
openssl s_client -connect localhost:443 -tls1_2 </dev/null

# 检查 HSTS 头
curl -k -I https://localhost/ | grep -i strict-transport-security
```

---

## 📊 运行结果

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
$ curl -k https://localhost/
Hello from backend web1 (via HTTPS)
```

---

## 🐛 常见问题

### Q1：自签名证书被浏览器拦截？

**A**：自签名证书不被浏览器信任，测试环境可添加例外。生产环境应使用 CA 签发的证书。

### Q2：HAProxy 提示证书文件找不到？

**A**：确认 PEM 文件路径正确，且证书和私钥已合并到一个文件中。

### Q3：TLS 1.0/1.1 仍可用？

**A**：在 `bind` 行添加 `ssl-min-ver TLSv1.2` 禁用旧版本。

---

## 📚 扩展学习

- [HAProxy 负载均衡](../haproxy-load-balancing/)
- [HAProxy 流量管理](../haproxy-traffic-management/)
- [NGINX 反向代理](../nginx-reverse-proxy/)
- [HAProxy TLS 官方文档](https://www.haproxy.com/documentation/hapee/latest/tls/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
