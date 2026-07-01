# Linux iptables 防火墙实战

> 学习使用 iptables 配置 Linux 防火墙规则，演示过滤、NAT、端口转发和自定义链，保护服务器网络安全。

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

- ✅ 理解 iptables 四表五链的概念
- ✅ 配置入站/出站过滤规则
- ✅ 实现端口转发和 NAT
- ✅ 保存和恢复 iptables 规则

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    iptables 数据包处理流程                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   入站包 ──▶ PREROUTING ──┬──▶ FORWARD ──▶ POSTROUTING ──▶ 出 │
│                           │                                    │
│                           ▼                                    │
│                       INPUT ──▶ 本地进程                        │
│                                                                 │
│   本地进程 ──▶ OUTPUT ──▶ POSTROUTING ──▶ 出                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```bash
cd networking/network-security-iptables
./scripts/start.sh
./scripts/check.sh
```

---

## 📖 核心概念

### 1. 四表

| 表名 | 作用 |
|------|------|
| filter | 过滤数据包（默认） |
| nat | 地址转换 |
| mangle | 修改数据包头部 |
| raw | 连接追踪处理 |

### 2. 五链

| 链名 | 作用 |
|------|------|
| PREROUTING | 路由前处理 |
| INPUT | 进入本机 |
| FORWARD | 转发 |
| OUTPUT | 本机发出 |
| POSTROUTING | 路由后处理 |

### 3. 规则匹配

```bash
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

- `-A INPUT`：追加到 INPUT 链
- `-p tcp`：协议 TCP
- `--dport 22`：目标端口 22
- `-j ACCEPT`：接受匹配包

---

## 💻 代码示例

### 基本规则配置

```bash
# 清空默认规则
iptables -F
iptables -X

# 默认策略：丢弃入站和转发，允许出站
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 允许回环
iptables -A INPUT -i lo -j ACCEPT

# 允许已建立连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 允许 SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 允许 HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### 端口转发

```bash
# 将本机 8080 转发到内网 192.168.1.10:80
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.10:80
iptables -t nat -A POSTROUTING -j MASQUERADE
```

### 保存规则

```bash
# Debian/Ubuntu
iptables-save > /etc/iptables/rules.v4

# CentOS/RHEL
service iptables save
```

---

## 🧪 验证测试

```bash
# 查看规则
iptables -L -n -v

# 查看 NAT 表
iptables -t nat -L -n -v

# 测试端口连通性
nc -zv localhost 22
nc -zv localhost 80
```

---

## 📚 扩展学习

- [网络安全基础](../network-security-basics/)
- [网络故障排查](../network-troubleshooting/)
- [iptables 手册](https://linux.die.net/man/8/iptables)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 工作原理

Network Security with iptables 的核心机制可以概括为以下几个步骤：

1. **初始化阶段**：准备运行环境，加载必要的配置和依赖。
2. **执行阶段**：按照预定的流程执行主要逻辑，处理输入并生成输出。
3. **验证阶段**：检查结果是否符合预期，记录关键指标和日志。
4. **清理阶段**：释放资源，确保环境可以重复运行。

### 关键设计决策

| 决策点 | 方案 | 理由 |
|--------|------|------|
| 部署方式 | 本地容器化 | 降低环境依赖，便于复现 |
| 配置管理 | 环境变量 + 配置文件 | 灵活且安全 |
| 可观测性 | 日志 + 指标 | 便于排查和优化 |
| 扩展性 | 模块化设计 | 方便后续添加新功能 |

### 性能考量

在实际生产环境中使用本案例时，建议关注以下性能指标：

- **响应时间**：确保核心操作在可接受范围内完成。
- **资源占用**：监控 CPU、内存、磁盘和网络使用情况。
- **吞吐量**：根据业务需求评估并发处理能力。
- **错误率**：建立告警机制，及时发现异常。

---

## 🛡️ 安全与最佳实践

### 安全建议

- 不要在生产环境中使用默认密码或密钥。
- 定期更新依赖组件到最新稳定版本。
- 对敏感配置使用密钥管理工具（如 Kubernetes Secrets、Vault）。
- 限制网络暴露面，使用防火墙或安全组控制访问。

### 最佳实践

- 在修改配置前备份现有环境。
- 使用版本控制管理所有配置文件和脚本。
- 编写自动化测试覆盖核心路径。
- 记录运行日志，便于审计和故障排查。

---

## 🧪 进阶实验

完成基础演示后，可以尝试以下进阶实验：

1. **参数调优**：修改关键配置参数，观察对结果的影响。
2. **故障注入**：故意制造错误，验证系统的容错能力。
3. **压力测试**：增加负载，评估系统瓶颈。
4. **集成测试**：将本案例与其他组件组合，构建完整链路。

---

## 📚 扩展资源

### 官方文档

- [相关技术官方文档](https://example.com)
- [OpenDemo 项目主页](https://github.com/opendemo)

### 推荐书籍

- 《相关技术权威指南》
- 《云原生架构实践》

### 社区与论坛

- Stack Overflow 相关标签
- GitHub Discussions
- 技术博客与公众号

---

## 🤝 贡献与反馈

如果你发现本案例有任何问题，或希望补充更多内容，欢迎提交 Issue 或 Pull Request。

---

*本 README 为 OpenDemo 五星案例标准模板，请根据实际案例内容持续完善。*
