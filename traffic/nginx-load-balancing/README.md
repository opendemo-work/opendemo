# NGINX 负载均衡演示

## 🎯 项目概述

NGINX 负载均衡演示展示了如何使用 NGINX 作为高性能的 HTTP 和 TCP 负载均衡器，实现流量分发和高可用架构。

## 📋 核心特性

- HTTP/HTTPS 负载均衡
- TCP/UDP 流量代理
- 健康检查和故障转移
- 会话保持和粘性负载
- 动态上游服务器管理
- 缓存和压缩优化

## 🚀 快速部署

```bash
# 启动 NGINX 负载均衡集群
docker-compose up -d

# 查看负载均衡状态
curl http://localhost:8080/nginx_status

# 测试负载分发效果
for i in {1..10}; do curl -s http://localhost:80/ | grep "Server IP"; done
```

## 📊 负载均衡算法

- **轮询 (Round Robin)**: 默认算法，依次分发请求
- **加权轮询 (Weighted Round Robin)**: 根据权重分配请求
- **最少连接 (Least Connections)**: 分发给连接数最少的服务器
- **IP 哈希 (IP Hash)**: 根据客户端 IP 进行会话保持
- **URL 哈希 (URL Hash)**: 根据请求 URL 进行分发

## 🔧 高级配置

- 主动和被动健康检查
- 动态上游服务器发现
- SSL 终止和证书管理
- 访问控制和速率限制
- 日志记录和监控集成
- A/B 测试和金丝雀发布

## 📈 性能优化

- 连接池和复用优化
- 缓冲区大小调优
- 工作进程配置
- 内存使用优化
- 网络性能调优
- 压缩和缓存策略

## 📚 学习资源

- [NGINX 官方文档](https://nginx.org/en/docs/)
- [负载均衡最佳实践](https://www.nginx.com/resources/admin-guide/load-balancer/)
- [性能调优指南](https://www.nginx.com/blog/tuning-nginx/)