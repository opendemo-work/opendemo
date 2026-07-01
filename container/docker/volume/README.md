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

```bash
cd container/docker/volume
./scripts/start.sh
./scripts/check.sh
```

---

## 📖 核心概念

### 1. Bind Mount

将宿主机上的任意路径挂载到容器中：

```bash
docker run -v /host/path:/container/path nginx:alpine
```

### 2. Named Volume

由 Docker 管理的卷，位于 Docker 存储目录：

```bash
docker volume create my-data
docker run -v my-data:/app/data nginx:alpine
```

### 3. tmpfs Mount

数据存储在内存中，容器删除后数据丢失：

```bash
docker run --tmpfs /app/cache:rw,noexec,nosuid,size=100m nginx:alpine
```

---

## 💻 代码示例

### Bind Mount

```bash
docker run -d \
  --name web-bind \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx:alpine
```

### Named Volume

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
