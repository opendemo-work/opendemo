# 🏗️ Containerd基础使用入门

> Containerd容器运行时基础入门实战：从安装配置到基本操作的完整指南

## 📋 案例概述

本案例介绍Containerd容器运行时的基础知识和基本操作，作为Docker底层引擎的学习材料。

### 🔧 核心技能点

- **Containerd基础概念**: 理解OCI标准和容器运行时架构
- **环境安装配置**: Containerd安装和基本配置
- **镜像管理操作**: 符合OCI标准的镜像管理
- **容器基本操作**: 容器生命周期管理
- **命名空间管理**: Containerd命名空间概念
- **CRI接口理解**: 容器运行时接口基础

### 🎯 适用人群

- 容器技术进阶学习者
- Kubernetes运维工程师
- 云原生基础设施工程师
- 系统架构师

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查Containerd版本
containerd --version

# 启动Containerd服务
sudo systemctl start containerd

# 验证Containerd运行状态
sudo ctr version
```

### 2. 基础操作练习

```bash
# 拉取基础镜像
sudo ctr images pull docker.io/library/nginx:latest

# 运行第一个容器
sudo ctr run -d docker.io/library/nginx:latest my-nginx

# 查看运行中的容器
sudo ctr containers list

# 查看任务状态
sudo ctr tasks list
```

---

## 📚 详细教程

### 1. Containerd核心概念

#### 1.1 OCI标准和架构

```
OCI Runtime Spec ← Containerd → OCI Image Spec
       ↑                              ↑
   runc/containerd              registry/storage
```

#### 1.2 核心组件

- **Containerd**: 容器运行时管理器
- **ctr**: Containerd命令行工具
- **namespaces**: 容器命名空间隔离
- **snapshots**: 快照和层管理

### 2. 镜像管理

#### 2.1 常用镜像操作

```bash
# 列出本地镜像
sudo ctr images list

# 拉取镜像
sudo ctr images pull docker.io/library/ubuntu:20.04

# 标记镜像
sudo ctr images tag docker.io/library/ubuntu:20.04 my-ubuntu:latest

# 删除镜像
sudo ctr images remove docker.io/library/ubuntu:20.04
```

#### 2.2 镜像导出导入

```bash
# 导出镜像
sudo ctr images export ubuntu.tar docker.io/library/ubuntu:20.04

# 导入镜像
sudo ctr images import ubuntu.tar
```

### 3. 容器管理

#### 3.1 命名空间操作

```bash
# 查看命名空间
sudo ctr namespaces list

# 创建命名空间
sudo ctr namespaces create my-namespace

# 删除命名空间
sudo ctr namespaces remove my-namespace
```

#### 3.2 容器生命周期

```bash
# 创建容器（不启动）
sudo ctr container create docker.io/library/nginx:latest nginx-container

# 启动容器任务
sudo ctr tasks start nginx-container

# 停止任务
sudo ctr tasks kill nginx-container

# 删除容器
sudo ctr container delete nginx-container
```

#### 3.3 容器状态查看

```bash
# 查看容器列表
sudo ctr container list

# 查看任务列表
sudo ctr tasks list

# 查看容器详细信息
sudo ctr container info nginx-container

# 查看任务状态
sudo ctr tasks list
```

### 4. 快照管理

#### 4.1 快照操作

```bash
# 查看快照
sudo ctr snapshot ls

# 查看快照树
sudo ctr snapshot tree

# 删除快照
sudo ctr snapshot remove snapshot-name
```

### 5. 网络配置

#### 5.1 CNI网络配置

```bash
# 查看网络命名空间
sudo ctr namespaces list

# 使用特定网络运行容器
sudo ctr run --net-host docker.io/library/nginx:latest nginx-host
```

---

## 🔧 实践操作

### 1. 部署Web应用

```bash
# 1. 拉取并运行Nginx
sudo ctr images pull docker.io/library/nginx:alpine
sudo ctr run -d --net-host docker.io/library/nginx:alpine web-server

# 2. 验证部署
curl http://localhost

# 3. 查看日志
sudo ctr tasks exec --exec-id test web-server cat /etc/nginx/nginx.conf
```

### 2. 多容器管理

```bash
# 1. 创建多个容器
sudo ctr run -d docker.io/library/redis:alpine redis-server
sudo ctr run -d --env REDIS_HOST=redis-server docker.io/my-app:latest app-server

# 2. 查看所有容器
sudo ctr containers list
```

---

## ⚠️ 常见问题和解决方案

### 1. 权限问题

**问题**: 无法执行ctr命令

**解决**:
```bash
# 使用sudo执行
sudo ctr version

# 或将用户添加到相关组
sudo usermod -aG docker $USER
```

### 2. 镜像拉取失败

**问题**: 无法从registry拉取镜像

**解决**:
```bash
# 检查网络连接
ping registry-1.docker.io

# 配置镜像加速器
sudo vi /etc/containerd/config.toml
```

### 3. 容器启动失败

**问题**: 容器无法正常启动

**解决**:
```bash
# 查看详细错误信息
sudo ctr tasks list
sudo journalctl -u containerd

# 检查镜像完整性
sudo ctr images check
```

---

## 🧪 实践练习

### 练习1：基础镜像操作
掌握Containerd镜像的拉取、查看、删除等操作。

### 练习2：容器生命周期管理
练习容器的创建、启动、停止、删除等操作。

### 练习3：命名空间管理
学习使用命名空间进行资源隔离。

### 练习4：快照管理
理解快照机制和层管理概念。

---

## 📚 扩展阅读

### 官方文档
- [Containerd官方文档](https://containerd.io/docs/)
- [OCI标准规范](https://opencontainers.org/)
- [CRI规范](https://github.com/kubernetes/cri-api)

### 相关技术
- [Docker基础](../../docker/basics/basic-docker-usage/)
- [Runc基础](../../runc/basics/basic-runc-usage/)
- [Kubernetes CRI](../../../kubernetes/)

---

## 📋 清理资源

```bash
# 停止所有任务
sudo ctr tasks list | awk '{print $1}' | xargs -I {} sudo ctr tasks kill {}

# 删除所有容器
sudo ctr containers list | awk '{print $1}' | xargs -I {} sudo ctr containers delete {}

# 删除所有镜像
sudo ctr images list | awk '{print $1}' | xargs -I {} sudo ctr images remove {}

# 清理快照
sudo ctr snapshot ls | awk '{print $1}' | xargs -I {} sudo ctr snapshot remove {}
```

---

> **💡 提示**: Containerd是Kubernetes的默认容器运行时，理解其工作原理对云原生技术学习很重要。