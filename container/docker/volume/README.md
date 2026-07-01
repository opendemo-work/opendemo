# Docker 数据卷 - 容器数据持久化

> 学习 Docker 数据持久化机制，演示 Bind Mount、Named Volume、tmpfs 挂载的使用场景和差异。

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

- ✅ 区分 Bind Mount、Named Volume 和 tmpfs 挂载
- ✅ 使用 `-v` 和 `--mount` 两种方式挂载
- ✅ 实现容器数据持久化
- ✅ 在多容器间共享数据

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker 数据持久化                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Host FS                                                        │
│   ┌─────────────────┐    ┌─────────────────┐                   │
│   │ /host/data      │    │ docker volume   │                   │
│   │ (Bind Mount)    │    │ my-volume       │                   │
│   └────────┬────────┘    └────────┬────────┘                   │
│            │                      │                            │
│            ▼                      ▼                            │
│      ┌──────────┐          ┌──────────┐                       │
│      │ Container│          │ Container│                       │
│      │ /app/data│          │ /app/data│                       │
│      └──────────┘          └──────────┘                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd container/docker/volume
./scripts/start.sh
./scripts/check.sh
```

---

## 📖 核心概念

### 1. Bind Mount

将宿主机上的任意路径挂载到容器中：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker run -v /host/path:/container/path nginx:alpine
```

### 2. Named Volume

由 Docker 管理的卷，位于 Docker 存储目录：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker volume create my-data
docker run -v my-data:/app/data nginx:alpine
```

### 3. tmpfs Mount

数据存储在内存中，容器删除后数据丢失：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker run --tmpfs /app/cache:rw,noexec,nosuid,size=100m nginx:alpine
```

---

## 💻 代码示例

### Bind Mount

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker run -d \
  --name web-bind \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx:alpine
```

### Named Volume

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker volume create web-data

docker run -d \
  --name web-volume \
  -v web-data:/usr/share/nginx/html \
  nginx:alpine

# 查看卷信息
docker volume inspect web-data
```

### Docker Compose

```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - web-data:/usr/share/nginx/html
      - ./html:/usr/share/nginx/html/custom:ro

volumes:
  web-data:
```

---

## 🧪 验证测试

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 查看卷列表
docker volume ls

# 在容器内写入数据
docker exec web-volume sh -c "echo 'hello' > /usr/share/nginx/html/test.txt"

# 停止删除容器后数据仍在
docker rm -f web-volume
docker volume inspect web-data
```

---

## 📚 扩展学习

- [Docker 基础入门](../basics/)
- [Docker 高级网络](../networking/)
- [Docker 存储官方文档](https://docs.docker.com/storage/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
