# NGINX 负载均衡演示 - 反向代理与高可用

> 使用 Docker Compose 部署一个 NGINX 负载均衡器和三个后端 Web 服务，演示轮询、权重、健康检查等负载均衡算法。

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

- ✅ 理解负载均衡的作用和常见算法
- ✅ 使用 NGINX 配置 upstream 后端集群
- ✅ 配置轮询、加权轮询、ip_hash 等调度策略
- ✅ 使用健康检查确保后端服务高可用

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    NGINX 负载均衡架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                         客户端请求                               │
│                              │                                  │
│                              ▼                                  │
│                    ┌──────────────────┐                        │
│                    │   NGINX LB       │                        │
│                    │  (负载均衡器)     │                        │
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
| Docker | >= 20.10 | 运行 NGINX 和 Web 服务 |
| Docker Compose | >= 1.29 | 编排服务 |

### 启动服务

```bash
cd traffic/nginx-load-balancing
./scripts/start.sh
sleep 5
./scripts/check.sh
```

### 测试负载均衡

```bash
# 连续访问 6 次，观察请求分布
for i in {1..6}; do
  curl -s http://localhost:80/
done
```

---

## 📖 核心概念

### 1. 负载均衡算法

| 算法 | 说明 | 适用场景 |
|------|------|----------|
| round_robin | 轮询，默认算法 | 后端性能一致 |
| weight | 加权轮询 | 后端性能不一致 |
| least_conn | 最少连接 | 长连接场景 |
| ip_hash | 基于客户端 IP 哈希 | 需要会话保持 |

### 2. upstream 配置

```nginx
upstream backend {
    server web1:8080 weight=3;
    server web2:8080 weight=2;
    server web3:8080 backup;
}
```

### 3. 健康检查

NGINX 开源版通过 `max_fails` 和 `fail_timeout` 实现被动健康检查：

```nginx
upstream backend {
    server web1:8080 max_fails=3 fail_timeout=30s;
    server web2:8080 max_fails=3 fail_timeout=30s;
}
```

---

## 💻 代码示例

### NGINX 配置文件

```nginx
# configs/nginx.conf
upstream backend {
    least_conn;
    server web1:8080;
    server web2:8080;
    server web3:8080;
}

server {
    listen 80;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Docker Compose 服务

```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./configs/nginx.conf:/etc/nginx/conf.d/default.conf:ro

  web1:
    image: hashicorp/http-echo
    command: ["-text", "Response from web1"]
  web2:
    image: hashicorp/http-echo
    command: ["-text", "Response from web2"]
  web3:
    image: hashicorp/http-echo
    command: ["-text", "Response from web3"]
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `configs/nginx.conf` | NGINX 负载均衡配置 |
| `docker-compose.yml` | 服务拓扑定义 |

---

## 🧪 验证测试

```bash
# 检查 NGINX 配置是否正确
docker exec nginx-load-balancer nginx -t

# 重新加载配置
docker exec nginx-load-balancer nginx -s reload

# 测试负载分发
watch -n 1 curl -s http://localhost/
```

---

## 📊 运行结果

连续访问多次，预期输出在 web1/web2/web3 之间分发：

```
Response from web1
Response from web2
Response from web3
Response from web1
...
```

---

## 🐛 常见问题

### Q1：请求总是落到同一个后端？

**A**：可能是浏览器缓存或长连接导致。使用 curl 并添加 `-H "Connection: close"`。

### Q2：后端宕机后请求仍失败？

**A**：确认 `max_fails` 和 `fail_timeout` 配置，健康检查需要一定时间生效。

---

## 📚 扩展学习

- [NGINX 反向代理](../nginx-reverse-proxy/)
- [HAProxy 负载均衡](../haproxy-load-balancing/)
- [NGINX 官方文档](https://nginx.org/en/docs/http/load_balancing.html)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
