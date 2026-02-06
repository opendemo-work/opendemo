# HAProxy SSL 终止演示

## 🎯 项目概述

HAProxy SSL 终止演示展示了如何使用 HAProxy 作为 SSL/TLS 终止代理，为后端服务提供安全的 HTTPS 访问。

## 📋 核心功能

- SSL/TLS 证书管理
- HTTPS 到 HTTP 的终止转换
- 负载均衡与高可用
- 会话保持与粘性会话
- 性能优化与缓存

## 🚀 部署配置

```bash
# 启动 HAProxy SSL 终止服务
docker-compose up -d

# 检查 SSL 证书状态
openssl x509 -in certs/server.crt -text -noout

# 测试 HTTPS 连接
curl -k https://localhost:443
```

## 🛡️ 安全特性

- 支持 Let's Encrypt 自动证书续期
- TLS 1.2/1.3 协议支持
- 完美前向保密 (PFS)
- HSTS 安全头配置
- OCSP Stapling 支持

## 📊 监控指标

- 连接数和并发处理能力
- SSL 握手性能统计
- 证书过期预警
- 错误率和响应时间
- 流量分析和带宽使用

## 📚 参考资料

- [HAProxy 官方文档](https://www.haproxy.org/)
- [SSL/TLS 最佳实践](https://wiki.mozilla.org/Security/Server_Side_TLS)
- [Let's Encrypt 集成指南](https://letsencrypt.org/docs/)