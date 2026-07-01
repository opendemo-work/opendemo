# Docker 基础入门 - 容器化第一程

> 从零开始学习 Docker 核心命令与概念，包括镜像拉取、容器运行、端口映射、卷挂载、日志查看和容器生命周期管理。

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

- ✅ 解释镜像、容器、仓库的核心概念
- ✅ 使用 `docker pull`、`run`、`ps`、`exec`、`stop`、`rm` 等基础命令
- ✅ 配置端口映射 `-p` 和卷挂载 `-v`
- ✅ 查看容器日志和进入容器内部
- ✅ 编写简单的 Dockerfile 并构建镜像

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker 基础架构                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Docker Client ──▶ Docker Daemon ──▶ Container Runtime         │
│        │                 │                    │                 │
│        │                 ▼                    ▼                 │
│        │          ┌──────────────┐      ┌──────────┐           │
│        │          │   Images     │      │Containers│           │
│        │          │ (nginx:alpine│      │ (running)│           │
│        │          └──────────────┘      └──────────┘           │
│        │                                                        │
│        ▼                                                        │
│   Docker Hub / Registry                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行容器 |

### 拉取并运行第一个容器

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 拉取 Nginx 镜像
docker pull nginx:alpine

# 运行容器
./scripts/start.sh

# 检查状态
./scripts/check.sh
```

### 访问应用

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
curl -s http://localhost:8080
```

浏览器访问 http://localhost:8080 查看 Nginx 默认页面。

---

## 📖 核心概念

### 1. 镜像（Image）

镜像是只读模板，包含运行应用所需的文件系统、代码、运行时、库和配置。镜像是分层构建的，每层对应 Dockerfile 的一条指令。

### 2. 容器（Container）

容器是镜像的运行实例，具有独立的进程空间、网络接口和文件系统。容器是轻量级的，共享宿主机内核。

### 3. 仓库（Registry）

仓库用于存储和分发镜像，Docker Hub 是默认的公共仓库。企业通常使用私有仓库如 Harbor、AWS ECR、阿里云 ACR。

### 4. 端口映射

将容器的端口映射到宿主机，使外部可以访问容器服务：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker run -p 宿主机端口:容器端口 nginx:alpine
```

### 5. 卷挂载

将宿主机的目录或文件挂载到容器中，实现数据持久化：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker run -v /host/data:/container/data nginx:alpine
```

---

## 💻 代码示例

### Dockerfile

```dockerfile
# Dockerfile
FROM nginx:alpine

LABEL maintainer="OpenDemo Team"

COPY html/index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 构建并运行

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 构建镜像
docker build -t opendemo-nginx:1.0 .

# 运行容器
docker run -d \
  --name opendemo-nginx \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  opendemo-nginx:1.0

# 查看容器日志
docker logs -f opendemo-nginx

# 进入容器内部
docker exec -it opendemo-nginx sh

# 停止并删除容器
docker stop opendemo-nginx && docker rm opendemo-nginx
```

### 常用命令速查

| 命令 | 作用 |
|------|------|
| `docker pull <image>` | 拉取镜像 |
| `docker images` | 查看本地镜像 |
| `docker run <image>` | 运行容器 |
| `docker ps` | 查看运行中的容器 |
| `docker ps -a` | 查看所有容器 |
| `docker exec -it <id> sh` | 进入容器 |
| `docker logs <id>` | 查看日志 |
| `docker stop <id>` | 停止容器 |
| `docker rm <id>` | 删除容器 |
| `docker rmi <image>` | 删除镜像 |
| `docker build -t <tag> .` | 构建镜像 |

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `Dockerfile` | 定义镜像构建步骤 |
| `html/index.html` | 自定义网站首页 |
| `scripts/start.sh` | 启动容器脚本 |
| `scripts/stop.sh` | 停止容器脚本 |

---

## 🧪 验证测试

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 1. 检查镜像是否构建成功
docker images | grep opendemo-nginx

# 2. 检查容器是否运行
docker ps | grep opendemo-nginx

# 3. 访问服务
curl -s http://localhost:8080

# 4. 查看容器资源使用
docker stats opendemo-nginx --no-stream
```

---

## 📊 运行结果

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
$ curl -s http://localhost:8080
<!DOCTYPE html>
<html>
<head><title>OpenDemo Docker</title></head>
<body>
  <h1>Hello from Docker Container!</h1>
</body>
</html>
```

---

## 🐛 常见问题

### Q1：端口被占用？

**A**：换一个宿主机端口，如 `-p 8081:80`，或停止占用 8080 的进程。

### Q2：容器启动后立即退出？

**A**：查看日志 `docker logs <container>`，可能是前台进程结束或配置错误。

### Q3：修改文件后容器内没有更新？

**A**：确认卷挂载路径正确，并且文件修改在挂载目录内。

### Q4：权限不足？

**A**：将当前用户加入 docker 组，或在 Linux 上使用 `sudo`。

---

## 📚 扩展学习

- [Docker 高级网络](../docker/networking/)
- [Docker 数据卷](../docker/volume/)
- [containerd 基础](../containerd/basics/)
- [Docker 官方文档](https://docs.docker.com/)
- [Dockerfile 最佳实践](https://docs.docker.com/develop/dev-best-practices/)

### 进阶实验

- [ ] 构建一个多阶段 Dockerfile
- [ ] 使用 Docker Compose 运行多容器应用
- [ ] 将镜像推送到 Docker Hub
- [ ] 使用 `.dockerignore` 减少镜像体积

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
