# containerd 基础入门 - 脱离 Docker 运行容器

> 学习使用 containerd 和 nerdctl 直接管理容器镜像与容器生命周期，理解 containerd 在容器生态系统中的位置。

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

- ✅ 理解 containerd 与 Docker 的关系
- ✅ 使用 nerdctl 拉取镜像、运行容器
- ✅ 使用 ctr 查看 containerd 内部对象
- ✅ 理解 CRI 和 containerd 在 Kubernetes 中的作用

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    containerd 生态架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Docker / Kubernetes / nerdctl                                  │
│              │                                                   │
│              ▼                                                   │
│        containerd (CRI / containerd API)                         │
│              │                                                   │
│              ▼                                                   │
│        containerd-shim                                           │
│              │                                                   │
│              ▼                                                   │
│        runc ──▶ Linux Namespace + Cgroups                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| containerd | >= 1.6 | 容器运行时 |
| nerdctl | >= 1.0 | 兼容 Docker CLI 的 containerd 客户端 |

### 启动 containerd

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd container/containerd/basics
./scripts/start.sh
./scripts/check.sh
```

---

## 📖 核心概念

### 1. containerd

containerd 是行业标准的容器运行时，专注于：

- 镜像管理（pull/push）
- 容器执行和生命周期
- 存储管理
- 网络管理

Docker 在内部也使用 containerd 来运行容器。

### 2. nerdctl

nerdctl 是 Docker CLI 的兼容实现，使用 containerd 作为后端：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
nerdctl run -d -p 8080:80 nginx:alpine
```

### 3. ctr

ctr 是 containerd 自带的低级客户端，用于调试和管理：

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
ctr images ls
ctr containers ls
ctr tasks ls
```

---

## 💻 代码示例

### 使用 nerdctl 运行容器

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 拉取镜像
nerdctl pull nginx:alpine

# 运行容器
nerdctl run -d --name nginx-ctr -p 8080:80 nginx:alpine

# 查看容器
nerdctl ps

# 进入容器
nerdctl exec -it nginx-ctr sh

# 停止并删除
nerdctl stop nginx-ctr
nerdctl rm nginx-ctr
```

### 使用 ctr 查看内部对象

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 列出镜像
ctr -n default images ls

# 列出容器
ctr -n default containers ls

# 列出运行中的任务
ctr -n default tasks ls
```

---

## 🧪 验证测试

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 测试服务访问
curl -s http://localhost:8080

# 查看 containerd 版本
nerdctl version

# 查看镜像层
ctr -n default images ls | grep nginx
```

---

## 📚 扩展学习

- [Docker 基础入门](../docker/basics/)
- [runc 基础入门](../runc/basics/)
- [containerd 官方文档](https://containerd.io/docs/)
- [nerdctl GitHub](https://github.com/containerd/nerdctl)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
