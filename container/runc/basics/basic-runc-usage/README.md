# 🏃 Runc基础使用入门

> Runc容器运行时基础入门实战：从OCI规范到容器执行的完整指南

## 📋 案例概述

本案例介绍Runc容器运行时的基础知识和基本操作，作为OCI容器运行时规范的实现学习材料。

### 🔧 核心技能点

- **Runc基础概念**: 理解OCI运行时规范和runc架构
- **环境安装配置**: Runc安装和基本配置
- **容器配置文件**: bundle和config.json的理解
- **容器生命周期**: 从创建到销毁的完整流程
- **资源限制配置**: CPU、内存等资源控制
- **安全配置**: Linux capabilities和安全选项

### 🎯 适用人群

- 容器技术深度学习者
- 云原生安全工程师
- 系统底层开发人员
- 容器平台架构师

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查Runc版本
runc --version

# 安装依赖
sudo apt-get update
sudo apt-get install -y libseccomp-dev

# 安装Runc
wget https://github.com/opencontainers/runc/releases/download/v1.1.0/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/bin/runc
```

### 2. 基础操作练习

```bash
# 创建容器根文件系统
mkdir -p mycontainer/rootfs
docker export $(docker create busybox) | tar -C mycontainer/rootfs -xf -

# 创建bundle配置
cd mycontainer
runc spec

# 运行容器
sudo runc run mycontainer
```

---

## 📚 详细教程

### 1. Runc核心概念

#### 1.1 OCI运行时规范

```
OCI Runtime Spec ← runc → Container Lifecycle
       ↓
config.json + rootfs
```

#### 1.2 核心组件

- **Bundle**: 包含config.json和rootfs的目录
- **config.json**: 容器配置文件
- **rootfs**: 容器根文件系统
- **State**: 容器运行时状态

### 2. Bundle创建和配置

#### 2.1 创建基础Bundle

```bash
# 创建目录结构
mkdir -p mycontainer/{rootfs,config}

# 准备rootfs
cd mycontainer
docker export $(docker create alpine) | tar -C rootfs -xf -

# 生成默认配置
runc spec
```

#### 2.2 config.json配置详解

```json
{
  "ociVersion": "1.0.2",
  "process": {
    "terminal": true,
    "user": {
      "uid": 0,
      "gid": 0
    },
    "args": [
      "sh"
    ],
    "env": [
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "TERM=xterm"
    ],
    "cwd": "/",
    "capabilities": {
      "bounding": [
        "CAP_AUDIT_WRITE",
        "CAP_KILL",
        "CAP_NET_BIND_SERVICE"
      ]
    }
  },
  "root": {
    "path": "rootfs",
    "readonly": true
  },
  "hostname": "runc",
  "mounts": [
    {
      "destination": "/proc",
      "type": "proc",
      "source": "proc"
    }
  ],
  "linux": {
    "resources": {
      "memory": {
        "limit": 104857600
      },
      "cpu": {
        "shares": 1024
      }
    }
  }
}
```

### 3. 容器生命周期管理

#### 3.1 创建和启动

```bash
# 创建容器（不启动）
sudo runc create mycontainer

# 查看容器状态
sudo runc state mycontainer

# 启动容器
sudo runc start mycontainer

# 进入容器
sudo runc exec mycontainer sh
```

#### 3.2 容器状态管理

```bash
# 查看所有容器
sudo runc list

# 查看特定容器状态
sudo runc state mycontainer

# 暂停容器
sudo runc pause mycontainer

# 恢复容器
sudo runc resume mycontainer

# 停止容器
sudo runc kill mycontainer SIGTERM
```

#### 3.3 容器删除

```bash
# 删除停止的容器
sudo runc delete mycontainer

# 强制删除运行中的容器
sudo runc delete --force mycontainer
```

### 4. 资源限制配置

#### 4.1 内存限制

```json
"linux": {
  "resources": {
    "memory": {
      "limit": 52428800,  // 50MB
      "reservation": 26214400,  // 25MB软限制
      "swap": 104857600  // 100MB交换空间
    }
  }
}
```

#### 4.2 CPU限制

```json
"linux": {
  "resources": {
    "cpu": {
      "shares": 512,  // 相对权重
      "quota": 50000,  // 50ms周期内最多50ms
      "period": 100000,  // 100ms周期
      "cpus": "0-1",  // 绑定到CPU 0和1
      "mems": "0"  // NUMA节点0
    }
  }
}
```

### 5. 安全配置

#### 5.1 Capabilities配置

```json
"process": {
  "capabilities": {
    "bounding": [
      "CAP_CHOWN",
      "CAP_DAC_OVERRIDE",
      "CAP_FSETID",
      "CAP_FOWNER",
      "CAP_MKNOD",
      "CAP_NET_RAW",
      "CAP_SETGID",
      "CAP_SETUID",
      "CAP_SETFCAP",
      "CAP_SETPCAP",
      "CAP_NET_BIND_SERVICE",
      "CAP_SYS_CHROOT",
      "CAP_KILL",
      "CAP_AUDIT_WRITE"
    ]
  }
}
```

#### 5.2 Seccomp配置

```json
"linux": {
  "seccomp": {
    "defaultAction": "SCMP_ACT_ERRNO",
    "architectures": [
      "SCMP_ARCH_X86_64"
    ],
    "syscalls": [
      {
        "names": [
          "accept",
          "accept4",
          "access"
        ],
        "action": "SCMP_ACT_ALLOW"
      }
    ]
  }
}
```

---

## 🔧 实践操作

### 1. 部署简单应用

```bash
# 1. 创建Nginx容器
mkdir -p nginx-container/rootfs
docker export $(docker create nginx:alpine) | tar -C nginx-container/rootfs -xf -
cd nginx-container
runc spec

# 2. 修改配置文件
sed -i 's/"sh"/"nginx", "-g", "daemon off;"/' config.json
sed -i 's/"TERM=xterm"/"TERM=xterm", "NGINX_PORT=8080"/' config.json

# 3. 运行容器
sudo runc run nginx-app
```

### 2. 资源限制测试

```bash
# 1. 创建带资源限制的容器
cat > config.json << EOF
{
  "ociVersion": "1.0.2",
  "process": {
    "terminal": true,
    "user": {"uid": 0, "gid": 0},
    "args": ["stress", "--vm", "1", "--vm-bytes", "100M"],
    "cwd": "/",
    "env": ["PATH=/usr/local/bin:/usr/bin:/bin"]
  },
  "root": {"path": "rootfs"},
  "linux": {
    "resources": {
      "memory": {"limit": 52428800},
      "cpu": {"shares": 256}
    }
  }
}
EOF

# 2. 运行压力测试
sudo runc run stress-test
```

---

## ⚠️ 常见问题和解决方案

### 1. 权限问题

**问题**: 无法创建容器

**解决**:
```bash
# 确保使用root权限
sudo runc run container-name

# 检查cgroup权限
sudo ls /sys/fs/cgroup
```

### 2. 配置文件错误

**问题**: config.json格式错误

**解决**:
```bash
# 验证JSON格式
jq . config.json

# 使用runc validate检查
sudo runc validate
```

### 3. 文件系统问题

**问题**: rootfs挂载失败

**解决**:
```bash
# 检查rootfs完整性
ls -la rootfs/

# 重新创建rootfs
rm -rf rootfs
docker export $(docker create alpine) | tar -C rootfs -xf -
```

---

## 🧪 实践练习

### 练习1：基础容器操作
掌握runc容器的创建、启动、停止等基本操作。

### 练习2：配置文件编写
学习编写和调试config.json配置文件。

### 练习3：资源限制配置
实践CPU和内存资源限制的配置方法。

### 练习4：安全配置实践
配置capabilities和seccomp安全策略。

---

## 📚 扩展阅读

### 官方文档
- [Runc官方文档](https://github.com/opencontainers/runc)
- [OCI运行时规范](https://github.com/opencontainers/runtime-spec)
- [OCI镜像规范](https://github.com/opencontainers/image-spec)

### 相关技术
- [Containerd基础](../../containerd/basics/basic-containerd-usage/)
- [Docker基础](../../docker/basics/basic-docker-usage/)
- [Linux容器技术](../../../linux/)

---

## 📋 清理资源

```bash
# 停止所有容器
sudo runc list | awk 'NR>1 {print $1}' | xargs -I {} sudo runc kill {} SIGKILL

# 删除所有容器
sudo runc list | awk 'NR>1 {print $1}' | xargs -I {} sudo runc delete {}

# 清理临时文件
rm -rf mycontainer nginx-container stress-test
```

---

> **💡 提示**: Runc是最底层的容器运行时，理解其工作原理有助于深入掌握容器技术的本质。