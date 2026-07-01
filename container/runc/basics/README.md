# runc 基础入门 - OCI 容器运行时

> 学习使用 runc 直接运行容器，理解 OCI（Open Container Initiative）规范和 Linux Namespace、Cgroups 等底层容器技术。

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

- ✅ 理解 OCI Runtime Spec 和 runc 的关系
- ✅ 使用 runc 创建、启动、停止容器
- ✅ 理解容器根文件系统（rootfs）的构建
- ✅ 理解 Namespace、Cgroups 在容器隔离中的作用

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    runc 运行时架构                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   runc spec ──▶ config.json                                     │
│        │                                                        │
│        ▼                                                        │
│   runc create ──▶ runc start ──▶ 容器进程                        │
│        │                              │                         │
│        │              ┌───────────────┘                         │
│        │              │                                          │
│        │              ▼                                          │
│        │       Linux Namespace + Cgroups                        │
│        │       PID / Network / Mount / UTS / IPC / User         │
│        │                                                         │
│        ▼                                                         │
│   runc delete                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| runc | >= 1.1 | OCI 容器运行时 |
| rootfs | - | 容器根文件系统 |

### 启动容器

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd container/runc/basics
./scripts/start.sh
./scripts/check.sh
```

---

## 📖 核心概念

### 1. OCI Runtime Spec

OCI 定义了容器运行时的标准接口，runc 是该标准的参考实现。容器配置保存在 `config.json` 中。

### 2. rootfs

rootfs 是容器的根文件系统，通常从一个基础镜像解压得到。runc 不管理镜像，只负责运行已经准备好的 rootfs。

### 3. Linux Namespace

Namespace 提供进程隔离：

- PID：进程 ID 隔离
- Network：网络接口隔离
- Mount：文件系统挂载点隔离
- UTS：主机名隔离
- IPC：进程间通信隔离
- User：用户 ID 隔离

### 4. Cgroups

Cgroups 限制容器资源使用：

- CPU
- Memory
- Block I/O
- Pids

---

## 💻 代码示例

### 创建 OCI 配置

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建 rootfs 目录
mkdir -p mycontainer/rootfs

# 生成默认 config.json
cd mycontainer
runc spec
```

### config.json 关键部分

```json
{
  "ociVersion": "1.0.2",
  "process": {
    "terminal": false,
    "user": { "uid": 0, "gid": 0 },
    "args": ["sh"],
    "env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"]
  },
  "linux": {
    "namespaces": [
      { "type": "pid" },
      { "type": "network" },
      { "type": "ipc" },
      { "type": "uts" },
      { "type": "mount" },
      { "type": "user" }
    ]
  }
}
```

### 运行容器

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 创建容器
runc create mycontainer

# 启动容器
runc start mycontainer

# 查看容器列表
runc list

# 进入容器
runc exec -t mycontainer sh

# 停止并删除
runc kill mycontainer SIGTERM
runc delete mycontainer
```

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 检查 runc 版本
runc --version

# 列出容器
runc list

# 查看容器配置
runc state mycontainer
```

---

## 📚 扩展学习

- [Docker 基础入门](../docker/basics/)
- [containerd 基础入门](../containerd/basics/)
- [runc GitHub](https://github.com/opencontainers/runc)
- [OCI Runtime Spec](https://github.com/opencontainers/runtime-spec)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
