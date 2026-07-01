# HTTP 协议分析 - 请求响应与状态码

> 通过 curl、浏览器开发者工具和 Wireshark 深入分析 HTTP/1.1 请求响应格式、常见状态码、Header 和缓存机制。

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

- ✅ 解释 HTTP 请求和响应的基本结构
- ✅ 理解常见状态码的含义
- ✅ 使用 curl 构造和发送 HTTP 请求
- ✅ 分析请求头、响应头和缓存控制

---

## 📐 架构图

```
客户端 ──▶ HTTP Request ──▶ 服务器
                              │
                              ▼
客户端 ◀── HTTP Response ◀── 服务器
```

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd networking/http-protocol-analysis
./scripts/start.sh
./scripts/check.sh
```

---

## 📖 核心概念

### 1. HTTP 请求结构

```
GET /index.html HTTP/1.1
Host: example.com
User-Agent: curl/8.0
Accept: text/html

（请求体，GET 通常为空）
```

### 2. HTTP 响应结构

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234

<html>...</html>
```

### 3. 常见状态码

| 状态码 | 含义 |
|--------|------|
| 200 | OK |
| 301/302 | 重定向 |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |

### 4. 缓存控制

```http
Cache-Control: no-cache
Cache-Control: max-age=3600
ETag: "abc123"
If-None-Match: "abc123"
```

---

## 💻 代码示例

### curl 常用命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# GET 请求
curl -i http://localhost:8080/

# POST 请求
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice"}'

# 查看详细通信过程
curl -v http://localhost:8080/

# 只显示响应头
curl -I http://localhost:8080/
```

### 启动测试服务器

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
python3 -m http.server 8080
```

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 测试不同状态码
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/notfound
```

---

## 📚 扩展学习

- [HTTP 协议深入](../http-protocol-deep-dive/)
- [TCP/IP 基础](../tcp-ip-fundamentals/)
- [MDN HTTP 文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*

---

## 🔍 HTTP/2 与 HTTP/3 简介

### HTTP/2

HTTP/2 引入二进制分帧、多路复用、头部压缩（HPACK）和服务器推送：

```
┌────────────────────────────────────────┐
│            HTTP/2 连接                  │
│  ┌─────┐ ┌─────┐ ┌─────┐              │
│  │流 1 │ │流 3 │ │流 5 │   多路复用    │
│  └─────┘ └─────┘ └─────┘              │
└────────────────────────────────────────┘
```

### HTTP/3

HTTP/3 基于 QUIC 协议，使用 UDP 传输，解决了 TCP 队头阻塞问题。

---

## 🛡️ HTTP 安全头

生产环境建议配置以下安全头：

| Header | 作用 |
|--------|------|
| `Strict-Transport-Security` | 强制 HTTPS |
| `Content-Security-Policy` | 防止 XSS |
| `X-Frame-Options` | 防止点击劫持 |
| `X-Content-Type-Options` | 防止 MIME 嗅探 |
| `Referrer-Policy` | 控制 Referrer 信息 |

---

## 🧪 扩展实验

- [ ] 使用 Wireshark 抓取 HTTP 包并分析三次握手
- [ ] 测试 301 和 302 重定向差异
- [ ] 验证 Cache-Control 的缓存行为
- [ ] 对比 HTTP/1.1 和 HTTP/2 的请求性能

---

## 📝 Cookie 与会话管理

HTTP 是无状态协议，Cookie 用于维持客户端状态：

```http
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict; Max-Age=3600
```

重要属性：

- `HttpOnly`：禁止 JavaScript 访问，防止 XSS 窃取
- `Secure`：仅通过 HTTPS 传输
- `SameSite`：控制跨站请求时是否发送 Cookie
- `Max-Age/Expires`：设置 Cookie 有效期

---

## 🔧 常用工具推荐

| 工具 | 用途 |
|------|------|
| curl | 命令行 HTTP 客户端 |
| Postman | API 测试与调试 |
| httpie | 更友好的命令行 HTTP 工具 |
| Wireshark | 网络抓包分析 |
| Browser DevTools | 浏览器内置调试工具 |
