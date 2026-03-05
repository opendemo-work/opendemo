# Domain-15: 网络基础

> **案例数量**: 15+ 个 | **最后更新**: 2026-03 | **适用场景**: 网络工程师、运维工程师

---

## 概述

网络基础域涵盖TCP/IP协议栈、网络设备、路由交换、负载均衡等核心网络知识，为Kubernetes网络管理提供理论基础。

**核心价值**：
- 🌐 **协议基础**：TCP/IP协议栈深度解析
- 🔧 **网络设备**：交换机、路由器配置
- ⚖️ **负载均衡**：L4/L7负载均衡原理
- 🔒 **网络安全**：防火墙、VPN、加密

---

## 案例目录

### TCP/IP协议
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 01 | [TCP/IP协议栈](./01-tcp-ip-protocol-stack.md) | OSI模型、TCP/IP分层 |
| 02 | [TCP连接管理](./02-tcp-connection-management.md) | 三次握手、四次挥手 |
| 03 | [UDP协议详解](./03-udp-protocol-details.md) | 无连接传输、应用场景 |

### 网络设备
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 04 | [交换机原理与配置](./04-switch-principles-configuration.md) | VLAN、STP、链路聚合 |
| 05 | [路由器原理与配置](./05-router-principles-configuration.md) | 路由协议、NAT配置 |
| 06 | [网络设备监控](./06-network-device-monitoring.md) | SNMP、流量分析 |

### 负载均衡
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 07 | [L4负载均衡](./07-l4-load-balancing.md) | NAT、DR模式 |
| 08 | [L7负载均衡](./08-l7-load-balancing.md) | HTTP路由、会话保持 |
| 09 | [HAProxy配置实践](./09-haproxy-configuration.md) | 配置模板、性能优化 |

### DNS与DHCP
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 10 | [DNS原理与配置](./10-dns-principles-configuration.md) | 解析流程、BIND配置 |
| 11 | [DHCP服务配置](./11-dhcp-service-configuration.md) | 地址分配、租约管理 |

### 网络安全
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 12 | [防火墙原理](./12-firewall-principles.md) | 包过滤、状态检测 |
| 13 | [VPN技术原理](./13-vpn-technology-principles.md) | IPSec、OpenVPN |
| 14 | [网络加密技术](./14-network-encryption-technology.md) | TLS、IPSec加密 |

### 网络故障排查
| # | 案例 | 关键内容 |
|:---:|:---|:---|
| 15 | [网络诊断工具](./15-network-diagnostic-tools.md) | tcpdump、wireshark |
| 16 | [网络故障案例](./16-network-fault-cases.md) | 典型故障分析 |

---

## 相关领域

- **[网络管理](../network-advanced/)** - Kubernetes网络
- **[Linux系统](../linux-advanced/)** - Linux网络配置
- **[安全](../security-advanced/)** - 网络安全实践

---

**维护者**: OpenDemo Team | **许可证**: MIT
