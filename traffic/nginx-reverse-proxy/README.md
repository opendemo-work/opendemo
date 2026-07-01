# NGINX 反向代理演示

> 使用 NGINX 作为反向代理，将客户端请求转发到后端应用服务，演示路径路由、请求头传递和静态资源缓存。

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

- ✅ 理解正向代理与反向代理的区别
- ✅ 使用 NGINX 配置反向代理
- ✅ 配置路径路由和请求头转发
- ✅ 启用静态资源缓存提升性能

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    NGINX 反向代理架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   客户端 ──▶ NGINX Reverse Proxy ──▶ 后端应用                   │
│              :80                       :8080                    │
│              │                            │                     │
│              │    /api/* ───────────────▶  API 服务             │
│              │    /static/* ────────────▶  静态资源             │
│              │    / ───────────────────▶  前端应用              │
│              ▼                                                  │
│        缓存 / SSL / 日志 / 限流                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```bash
cd traffic/nginx-reverse-proxy
./scripts/start.sh
sleep 5
./scripts/check.sh
```

测试代理：

```bash
curl -s http://localhost/api/health
curl -s http://localhost/static/index.html
curl -s http://localhost/
```

---

## 📖 核心概念

### 1. 反向代理

反向代理位于客户端和后端服务器之间，客户端只与代理交互，不直接访问后端。常用于：

- 隐藏后端服务真实地址
- 统一入口和 SSL 终止
- 负载均衡和高可用
- 缓存和压缩

### 2. proxy_pass

```nginx
location /api/ {
    proxy_pass http://api-service:8080/;
}
```

注意末尾斜杠的差异：
- `proxy_pass http://api:8080/;`：去掉 location 匹配前缀
- `proxy_pass http://api:8080;`：保留完整路径

### 3. 请求头转发

```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

---

## 💻 代码示例

```nginx
# configs/nginx.conf
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://api-service:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /var/www/static/;
        expires 1h;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 🧪 验证测试

```bash
# 测试根路径转发
curl -s -I http://localhost/

# 测试 API 路径转发
curl -s http://localhost/api/users

# 检查响应头中的后端信息
curl -s -I http://localhost/static/test.css
```

---

## 📚 扩展学习

- [NGINX 负载均衡](../nginx-load-balancing/)
- [HAProxy 反向代理](../haproxy-traffic-management/)
- [NGINX 反向代理官方文档](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
