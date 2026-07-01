# HAProxy 流量管理演示 - 限流、黑白名单与重写

> 使用 HAProxy 实现高级流量管理功能，包括速率限制、连接限制、IP 黑白名单、请求重定向和 URL 重写。

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

- ✅ 使用 HAProxy 实现请求速率限制
- ✅ 配置 IP 黑白名单
- ✅ 实现 HTTP 重定向和 URL 重写
- ✅ 使用 ACL 进行条件路由

---

## 📐 架构图

```
客户端 ──▶ HAProxy ──┬─▶ 正常流量 ──▶ 后端服务
                     ├─▶ 限流 ─────▶ 429 Too Many Requests
                     ├─▶ 黑名单 ───▶ 403 Forbidden
                     └─▶ 重写 ─────▶ 新路径
```

---

## 🚀 快速开始

```bash
cd traffic/haproxy-traffic-management
./scripts/start.sh
sleep 5
./scripts/check.sh
```

---

## 📖 核心概念

### 1. ACL（访问控制列表）

HAProxy 使用 ACL 进行条件判断：

```haproxy
acl is_api path_beg /api
acl is_internal src 10.0.0.0/8
```

### 2. 限流

限制单个 IP 的请求速率：

```haproxy
stick-table type ip size 100k expire 30s store http_req_rate(10s)
acl rate_limit src_http_req_rate gt 10
http-request deny if rate_limit
```

### 3. 黑白名单

```haproxy
acl blacklist src 192.168.1.100 192.168.1.101
http-request deny if blacklist
```

---

## 💻 代码示例

```haproxy
# configs/haproxy.cfg
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5s
    timeout client 30s
    timeout server 30s

frontend web_frontend
    bind *:80

    # 限流：每 IP 每 10 秒最多 10 个请求
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    acl rate_limit src_http_req_rate gt 10
    http-request deny deny_status 429 if rate_limit

    # IP 黑名单
    acl blacklist src 192.168.1.100
    http-request deny if blacklist

    # URL 重写：/old/path 重写到 /new/path
    http-request set-path /new/path if { path /old/path }

    # HTTP 重定向到 HTTPS
    redirect scheme https code 301 if !{ ssl_fc }

    default_backend web_servers

backend web_servers
    balance roundrobin
    server web1 web1:8080 check
```

---

## 🧪 验证测试

```bash
# 测试正常访问
curl -s http://localhost/

# 测试限流（快速请求）
for i in {1..15}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost/; done

# 测试 URL 重写
curl -s -I http://localhost/old/path
```

---

## 📚 扩展学习

- [HAProxy 负载均衡](../haproxy-load-balancing/)
- [HAProxy SSL 终止](../haproxy-ssl-termination/)
- [HAProxy 配置手册](https://www.haproxy.org/download/2.8/doc/configuration.txt)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📈 HAProxy 限流策略实践

### 基于请求速率限流

```haproxy
stick-table type ip size 1m expire 10s store http_req_rate(10s)
acl rate_limit src_http_req_rate gt 100
http-request deny deny_status 429 if rate_limit
```

### 基于并发连接数限流

```haproxy
stick-table type ip size 1m expire 30s store conn_cur
acl too_many src_conn_cur gt 50
http-request deny if too_many
```

### 基于 URI 限流

```haproxy
stick-table type binary len 8 size 1m expire 10s store http_req_rate(10s)
http-request track-sc0 base32+src
acl api_rate_limit sc0_http_req_rate gt 50
http-request deny if api_rate_limit
```

生产环境建议将限流与监控告警结合，及时调整阈值。

---

## 🚀 进阶实验

完成基础学习后，建议尝试以下实验：

- 配置基于用户身份的动态限流
- 结合 HAProxy 统计页面监控限流效果
- 使用 Lua 脚本实现自定义 ACL 逻辑
- 将限流日志输出到 Syslog 进行集中分析
