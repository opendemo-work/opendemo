# 🚦 流量管理技术栈完整指南

> 从负载均衡到API网关的完整流量管理解决方案，包含Nginx、HAProxy、Higress等核心技术

---

## 🚀 快速入口

- 📋 **[Nginx 命令行速查表](./cli/nginx-cli.md)** - 生产环境必备的Nginx命令大全
- 🔍 **案例导航**: 负载均衡、反向代理、SSL终止、流量管控等核心场景

## 📋 技术栈概述

流量管理是现代应用架构的核心组件，负责请求路由、负载均衡、安全防护和服务治理。本技术栈提供从基础配置到高级特性的完整学习路径。

### 🔧 核心技术覆盖

- **Nginx**: Web服务器、反向代理、负载均衡
- **HAProxy**: 高性能TCP/HTTP负载均衡器
- **Higress**: 云原生API网关和服务网格
- **流量管控**: 限流、熔断、灰度发布
- **安全防护**: SSL/TLS终止、WAF、访问控制

### 🎯 适用人群

- 系统架构师
- DevOps工程师
- SRE团队成员
- 后端开发工程师
- 网络安全工程师

---

## 📚 详细目录

### Nginx 系列
<details>
<summary>点击查看完整列表</summary>

- [nginx-web-server](./nginx-web-server/) - Nginx Web服务器基础配置
- [nginx-reverse-proxy](./nginx-reverse-proxy/) - Nginx 反向代理配置
- [nginx-load-balancing](./nginx-load-balancing/) - Nginx 负载均衡配置
- [**nginx-cli-cheatsheet**](./nginx-cli.md) - **Nginx 命令行速查表** ⭐

</details>

### HAProxy 系列
<details>
<summary>点击查看完整列表</summary>

- [haproxy-traffic-management](./haproxy-traffic-management/) - HAProxy 流量管理
- [haproxy-load-balancing](./haproxy-load-balancing/) - HAProxy 负载均衡
- [haproxy-ssl-termination](./haproxy-ssl-termination/) - HAProxy SSL终止

</details>

### Higress 系列
<details>
<summary>点击查看完整列表</summary>

- [higress-api-gateway](./higress-api-gateway/) - Higress API网关
- [higress-service-mesh](./higress-service-mesh/) - Higress 服务网格

</details>

### 基础入门系列
掌握Web服务器和反向代理的基础配置。

### 负载均衡系列
学习各种负载均衡算法和高可用配置。

### 高级特性系列
深入理解SSL终止、缓存优化、安全加固等高级功能。

### 云原生系列
探索服务网格和API网关的现代化解决方案。

---

## 🚀 快速开始

### 命令行工具使用

```bash
# 查看所有流量管理案例
opendemo search traffic

# 获取Nginx基础案例
opendemo get traffic nginx-web-server

# 获取负载均衡案例
opendemo get traffic nginx-load-balancing

# 获取HAProxy案例
opendemo get traffic haproxy-traffic-management

# 直接查看Nginx CLI速查表
opendemo get traffic nginx-cli-cheatsheet
```

### 生产环境常用命令参考

详细命令清单请查看 **[Nginx CLI 命令行速查表](./nginx-cli.md)**，包含：

- Nginx 配置管理
- 性能监控和调优
- 安全加固配置
- 日志分析和故障排查
- SSL/TLS 管理
- 负载均衡配置

---

## 📊 案例统计

| 分类 | 案例数量 | 状态 |
|------|----------|------|
| Nginx基础 | 3 | ✅ 基本完成 |
| Nginx高级 | 2 | ✅ 进行中 |
| HAProxy | 3 | ✅ 基本完成 |
| Higress | 2 | 🔄 规划中 |
| **总计** | **10** | ✅ |

---

## 🛠️ 环境准备

```bash
# 安装Nginx
sudo apt-get install nginx  # Ubuntu/Debian
sudo yum install nginx      # CentOS/RHEL

# 安装HAProxy
sudo apt-get install haproxy

# 验证安装
nginx -v
haproxy -v
```

---

## 📖 学习建议

1. **理论结合实践**: 边学边练，每个配置都要实际测试
2. **循序渐进**: 按照基础→负载均衡→高级特性的顺序学习
3. **重视安全**: SSL配置和访问控制是生产环境的关键
4. **性能优先**: 掌握性能调优和监控方法
5. **高可用设计**: 学习故障转移和健康检查机制

---

## 🤝 贡献指南

欢迎提交新的流量管理案例或改进现有案例：
- 遵循最佳实践配置
- 提供可运行的配置示例
- 确保案例的生产可用性
- 包含性能基准和安全配置说明
- 所有命令示例需经过实际环境验证

---

> **💡 提示**: 流量管理是构建可靠、高性能应用架构的基础，掌握这些技术对于现代软件工程师至关重要。