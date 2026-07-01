# 🐳 Container 容器技术栈

> 容器化技术从入门到精通，涵盖 Docker、containerd、runc 等主流容器运行时，以及镜像构建、网络、存储和故障排查。

---

## 📚 技术栈概览

容器技术是现代云原生应用的基础。本技术栈提供从 Docker 基础到 OCI 运行时的完整学习路径，包含 14 个实战案例，覆盖以下主题：

- Docker 基础与镜像构建
- Docker 网络与数据卷
- Docker 高级特性与故障排查
- containerd 基础与高级用法
- nerdctl 与 ctr 实践
- runc 与 OCI 规范
- 容器安全与资源限制

---

## 🎯 学习目标

完成本技术栈学习后，你将能够：

- ✅ 使用 Docker 构建、运行和管理容器
- ✅ 配置容器网络和持久化存储
- ✅ 使用 containerd 和 nerdctl 管理容器
- ✅ 理解 runc 和 OCI 运行时规范
- ✅ 排查常见容器问题

---

## 📂 案例目录

| 案例 | 主题 |
|------|------|
| [Docker 基础入门](./docker/basics/) | 镜像/容器/卷 |
| [Docker 高级网络](./docker/networking/) | 网络模式 |
| [Docker 数据卷](./docker/volume/) | 持久化存储 |
| [containerd 基础](./containerd/basics/) | nerdctl 使用 |
| [runc 基础](./runc/basics/) | OCI 运行时 |

... 共 14 个案例，详见各子目录。

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd container/docker/basics
./scripts/start.sh
./scripts/check.sh
```

---

## 🔗 相关技术栈

- [Kubernetes](./../kubernetes/) - 容器编排
- [Traffic](./../traffic/) - 容器入口流量
- [SRE](./../sre/) - 容器化运维

---

*最后更新：2026-07-01*  
*维护者：OpenDemo Team*
