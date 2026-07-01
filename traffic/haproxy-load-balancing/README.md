# HAProxy 负载均衡演示 - 四层/七层流量分发

> 使用 HAProxy 作为高性能负载均衡器，演示 HTTP 七层负载均衡、TCP 四层负载均衡、健康检查、会话保持和权重配置。

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

- ✅ 理解 HAProxy 在四层和七层负载均衡中的应用
- ✅ 配置 frontend、backend 和 listen 段
- ✅ 配置 TCP 和 HTTP 健康检查
- ✅ 使用 cookie 实现会话保持
- ✅ 使用统计页面监控后端状态

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    HAProxy 负载均衡架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                         客户端请求                               │
│                              │                                  │
│                              ▼                                  │
│                    ┌──────────────────┐                        │
│                    │   HAProxy        │                        │
│                    │  :80 / :8404     │                        │
│                    └────────┬─────────┘                        │
│                             │                                   │
│            ┌────────────────┼────────────────┐                 │
│            ▼                ▼                ▼                 │
│      ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│      │ Web Svr 1│    │ Web Svr 2│    │ Web Svr 3│             │
│      │ :8081    │    │ :8082    │    │ :8083    │             │
│      └──────────┘    └──────────┘    └──────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 HAProxy 和后端服务 |
| Docker Compose | >= 1.29 | 编排服务 |

### 启动服务

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd traffic/haproxy-load-balancing
./scripts/start.sh
sleep 5
./scripts/check.sh
```

### 测试负载均衡

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
for i in {1..6}; do
  curl -s http://localhost/
done
```

---

## 📖 核心概念

### 1. 四层 vs 七层负载均衡

| 层级 | 工作层级 | 特点 |
|------|----------|------|
| 四层（L4） | 传输层 TCP/UDP | 性能高，不解析应用协议 |
| 七层（L7） | 应用层 HTTP | 可基于 URL、Header、Cookie 路由 |

### 2. balance 算法

| 算法 | 说明 |
|------|------|
| roundrobin | 轮询，默认算法 |
| leastconn | 最少连接 |
| source | 基于源 IP 哈希 |
| uri | 基于 URI 哈希 |

### 3. 健康检查

HAProxy 支持 TCP 和 HTTP 健康检查：

```haproxy
server web1 web1:8080 check inter 5s fall 3 rise 2
```

---

## 💻 代码示例

### HAProxy 配置文件

```haproxy
# configs/haproxy.cfg
global
    daemon
    maxconn 4096
    stats socket /run/haproxy/admin.sock mode 660 level admin

defaults
    mode http
    timeout connect 5s
    timeout client 30s
    timeout server 30s
    option httpchk GET /health
    http-check expect status 200

frontend web_frontend
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web1 web1:8080 check cookie web1 weight 3
    server web2 web2:8080 check cookie web2 weight 2
    server web3 web3:8080 check cookie web3 weight 1

listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats auth admin:admin
    stats refresh 10s
```

### TCP 四层负载均衡示例

```haproxy
frontend tcp_frontend
    bind *:3306
    default_backend mysql_servers

backend mysql_servers
    mode tcp
    balance leastconn
    option tcp-check
    server mysql1 mysql1:3306 check
    server mysql2 mysql2:3306 check
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `configs/haproxy.cfg` | HAProxy 主配置 |
| `docker-compose.yml` | 服务编排 |

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 检查 HAProxy 配置
docker exec haproxy-load-balancer haproxy -c -f /usr/local/etc/haproxy/haproxy.cfg

# 查看统计页面
curl -s -u admin:admin http://localhost:8404/stats

# 测试会话保持
curl -s -c cookies.txt -b cookies.txt http://localhost/
```

---

## 📊 运行结果

连续访问将看到请求按权重分配到不同后端：

```
Response from web1
Response from web2
Response from web1
Response from web3
...
```

---

## 🐛 常见问题

### Q1：HAProxy 启动失败？

**A**：检查配置文件语法：`docker exec haproxy-load-balancer haproxy -c -f /usr/local/etc/haproxy/haproxy.cfg`

### Q2：后端一直显示 DOWN？

**A**：检查健康检查路径是否正确，以及后端服务是否返回 200。

---

## 📚 扩展学习

- [HAProxy SSL 终止](../haproxy-ssl-termination/)
- [HAProxy 流量管理](../haproxy-traffic-management/)
- [NGINX 负载均衡](../nginx-load-balancing/)
- [HAProxy 官方文档](http://www.haproxy.org/#docs)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
