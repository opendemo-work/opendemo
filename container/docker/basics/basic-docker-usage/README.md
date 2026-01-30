# 🐳 Docker基础使用入门

> Docker容器技术基础入门实战：从安装配置到基本操作的完整指南

## 📋 案例概述

本案例介绍Docker容器技术的基础知识和基本操作，帮助初学者快速上手容器化应用开发。

### 🔧 核心技能点

- **Docker基础概念**: 理解容器、镜像、仓库等核心概念
- **环境安装配置**: Docker Engine安装和基本配置
- **镜像管理操作**: 镜像拉取、构建、推送等操作
- **容器基本操作**: 容器创建、启动、停止、删除等
- **数据卷管理**: 容器数据持久化和共享
- **网络配置**: 容器网络连接和端口映射

### 🎯 适用人群

- 容器技术初学者
- DevOps工程师
- 云原生开发者
- 系统管理员

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查Docker版本
docker --version

# 启动Docker服务
sudo systemctl start docker

# 验证Docker运行状态
docker info
```

### 2. 基础操作练习

```bash
# 拉取基础镜像
docker pull nginx:latest

# 运行第一个容器
docker run -d -p 8080:80 --name my-nginx nginx:latest

# 查看运行中的容器
docker ps

# 访问容器应用
curl http://localhost:8080
```

---

## 📚 详细教程

### 1. Docker核心概念

#### 1.1 容器与虚拟机的区别

```
传统虚拟机: Host OS → Hypervisor → Guest OS → Application
Docker容器:   Host OS → Docker Engine → Application
```

#### 1.2 核心组件

- **镜像(Image)**: 只读模板，包含应用程序和运行环境
- **容器(Container)**: 镜像的运行实例
- **仓库(Registry)**: 存储和分发镜像的地方

### 2. 镜像管理

#### 2.1 常用镜像操作

```bash
# 搜索镜像
docker search ubuntu

# 拉取镜像
docker pull ubuntu:20.04

# 查看本地镜像
docker images

# 删除镜像
docker rmi ubuntu:20.04
```

#### 2.2 构建自定义镜像

```dockerfile
# Dockerfile示例
FROM ubuntu:20.04
LABEL maintainer="demo@example.com"
RUN apt-get update && apt-get install -y nginx
COPY index.html /var/www/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```bash
# 构建镜像
docker build -t my-app:1.0 .

# 运行自定义镜像
docker run -d -p 8080:80 my-app:1.0
```

### 3. 容器管理

#### 3.1 容器生命周期

```bash
# 创建容器但不启动
docker create nginx:latest

# 启动容器
docker start my-container

# 停止容器
docker stop my-container

# 重启容器
docker restart my-container

# 删除容器
docker rm my-container
```

#### 3.2 容器状态查看

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括停止的）
docker ps -a

# 查看容器详细信息
docker inspect my-container

# 查看容器日志
docker logs my-container
```

### 4. 数据管理

#### 4.1 数据卷操作

```bash
# 创建数据卷
docker volume create my-volume

# 查看数据卷
docker volume ls

# 使用数据卷运行容器
docker run -d -v my-volume:/data --name data-container nginx:latest

# 删除数据卷
docker volume rm my-volume
```

#### 4.2 绑定挂载

```bash
# 绑定主机目录到容器
docker run -d -v /host/path:/container/path nginx:latest

# 只读挂载
docker run -d -v /host/path:/container/path:ro nginx:latest
```

### 5. 网络配置

#### 5.1 网络模式

```bash
# 桥接网络（默认）
docker run -d -p 8080:80 nginx:latest

# 主机网络
docker run -d --network host nginx:latest

# 无网络
docker run -d --network none nginx:latest
```

#### 5.2 自定义网络

```bash
# 创建自定义网络
docker network create my-network

# 使用自定义网络运行容器
docker run -d --network my-network --name web nginx:latest
docker run -d --network my-network --name db mysql:8.0

# 容器间通信
docker exec web ping db
```

---

## 🔧 实践操作

### 1. 部署Web应用

```bash
# 1. 创建简单HTML文件
echo "<h1>Hello Docker!</h1>" > index.html

# 2. 创建Dockerfile
cat > Dockerfile << EOF
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EOF

# 3. 构建和运行
docker build -t hello-docker .
docker run -d -p 8080:80 hello-docker

# 4. 验证部署
curl http://localhost:8080
```

### 2. 多容器应用

```bash
# 1. 启动数据库
docker run -d --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=myapp \
  mysql:8.0

# 2. 启动应用并连接数据库
docker run -d --name web-app \
  --link mysql-db:mysql \
  -p 8080:8080 \
  my-web-app:latest
```

---

## ⚠️ 常见问题和解决方案

### 1. 权限问题

**问题**: 无法连接到Docker守护进程

**解决**:
```bash
# 将用户添加到docker组
sudo usermod -aG docker $USER
# 重新登录或执行
newgrp docker
```

### 2. 端口冲突

**问题**: 端口已被占用

**解决**:
```bash
# 查找占用端口的进程
sudo netstat -tlnp | grep :8080
# 更换端口或停止占用进程
```

### 3. 磁盘空间不足

**问题**: 系统提示磁盘空间不足

**解决**:
```bash
# 清理未使用的资源
docker system prune -a
# 清理特定资源
docker container prune
docker image prune
docker volume prune
```

---

## 🧪 实践练习

### 练习1：基础镜像操作
掌握镜像的拉取、查看、删除等基本操作。

### 练习2：容器生命周期管理
练习容器的创建、启动、停止、重启等操作。

### 练习3：数据持久化
学习使用数据卷和绑定挂载实现数据持久化。

### 练习4：网络配置
配置不同网络模式和容器间通信。

---

## 📚 扩展阅读

### 官方文档
- [Docker官方文档](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker CLI参考](https://docs.docker.com/engine/reference/commandline/cli/)

### 相关技术
- [Docker Compose](../compose-basics/)
- [Docker Swarm](../swarm-basics/)
- [Kubernetes](../../kubernetes/)

---

## 📋 清理资源

```bash
# 停止所有容器
docker stop $(docker ps -aq)

# 删除所有容器
docker rm $(docker ps -aq)

# 删除所有镜像
docker rmi $(docker images -q)

# 清理系统
docker system prune -a
```

---

> **💡 提示**: Docker是容器技术的基础，建议熟练掌握后再学习更高级的容器编排技术如Kubernetes。