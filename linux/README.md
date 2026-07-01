# 🐧 Linux 技术栈

> Linux 系统管理与运维实践，涵盖常用命令、性能监控、网络工具、文件系统和 Shell 脚本等方向。

---

## 📚 技术栈概览

Linux 是服务器和云基础设施的主流操作系统。本技术栈提供从基础命令到高级监控的完整学习路径，包含 18 个实战案例，覆盖以下主题：

- Linux 常用命令与工具
- 系统性能监控（CPU/内存/磁盘/网络）
- 网络诊断与配置
- 文件系统与进程管理
- Shell 脚本与自动化
- 日志分析与故障排查

---

## 🎯 学习目标

完成本技术栈学习后，你将能够：

- ✅ 熟练使用 Linux 常用命令
- ✅ 监控系统资源并定位瓶颈
- ✅ 使用网络工具诊断连接问题
- ✅ 编写 Shell 脚本实现自动化
- ✅ 排查常见 Linux 系统故障

---

## 📂 案例目录

| 案例 | 主题 |
|------|------|
| [dig DNS 工具](./linux-dig-dns-utility-demo/) | DNS 查询 |
| [htop 系统监控](./linux-htop-system-monitor-demo/) | 进程监控 |
| [iostat 磁盘监控](./linux-iostat-disk-monitoring-demo/) | IO 分析 |
| [netstat 网络监控](./linux-netstat-network-monitoring-demo/) | 连接统计 |
| [lsof 文件列表](./linux-lsof-file-list-demo/) | 打开文件 |

... 共 18 个案例，详见各子目录。

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd linux/linux-dig-dns-utility-demo
./scripts/start.sh
./scripts/check.sh
```

---

## 🔗 相关技术栈

- [Networking](./../networking/) - 网络协议与工具
- [SRE](./../sre/) - 系统可靠性工程
- [Security](./../security/) - Linux 安全加固

---

*最后更新：2026-07-01*  
*维护者：OpenDemo Team*
