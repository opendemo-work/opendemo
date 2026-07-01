<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Linux Namespace Isolation

Linux命名空间隔离机制演示，展示容器技术的核心隔离原理。

## 命名空间类型

```
命名空间隔离层次:
┌─────────────────────────────────────────────────────────┐
│                      PID Namespace                       │
│         进程ID隔离，PID 1的独立性                         │
├─────────────────────────────────────────────────────────┤
│                      Mount Namespace                     │
│         文件系统挂载点隔离                                │
├─────────────────────────────────────────────────────────┤
│                      Network Namespace                   │
│         网络接口、路由、防火墙隔离                         │
├─────────────────────────────────────────────────────────┤
│                      UTS Namespace                       │
│         主机名和域名隔离                                  │
├─────────────────────────────────────────────────────────┤
│                      IPC Namespace                       │
│         System V IPC和POSIX消息队列隔离                   │
├─────────────────────────────────────────────────────────┤
│                      User Namespace                      │
│         用户和组ID隔离                                    │
├─────────────────────────────────────────────────────────┤
│                      Cgroup Namespace                    │
│         控制组根目录隔离                                  │
└─────────────────────────────────────────────────────────┘
```

## 创建命名空间

### 使用unshare
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建新的Mount和UTS命名空间
sudo unshare --mount --uts /bin/bash

# 在新命名空间中
hostname container-host
hostname  # 显示 container-host
exit
hostname  # 恢复原来的主机名

# 创建完整的隔离环境
sudo unshare --pid --mount --uts --ipc --net --fork --user --map-root-user /bin/bash
echo $$  # PID 1
```

### 使用clone系统调用
```c
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

static char child_stack[1024*1024];

int child_fn() {
    printf("PID in child: %ld\n", (long)getpid());
    system("hostname container");
    execlp("/bin/bash", "bash", NULL);
    return 0;
}

int main() {
    printf("PID in parent: %ld\n", (long)getpid());
    
    pid_t child_pid = clone(child_fn, child_stack+1024*1024,
        CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNS | SIGCHLD, NULL);
    
    waitpid(child_pid, NULL, 0);
    return 0;
}
```

## 网络命名空间

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建网络命名空间
sudo ip netns add mynamespace

# 列出命名空间
sudo ip netns list

# 在命名空间中执行命令
sudo ip netns exec mynamespace ip link list

# 创建veth对连接命名空间
sudo ip link add veth0 type veth peer name veth1
sudo ip link set veth1 netns mynamespace

# 配置IP地址
sudo ip addr add 192.168.1.1/24 dev veth0
sudo ip netns exec mynamespace ip addr add 192.168.1.2/24 dev veth1
sudo ip link set veth0 up
sudo ip netns exec mynamespace ip link set veth1 up
sudo ip netns exec mynamespace ip link set lo up

# 测试连通性
ping 192.168.1.2
sudo ip netns exec mynamespace ping 192.168.1.1

# 清理
sudo ip netns delete mynamespace
```

## PID命名空间

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建新的PID命名空间
sudo unshare --pid --fork --mount-proc /bin/bash

# 在新PID命名空间中
ps aux  # 只能看到自己命名空间的进程
echo $$  # PID为1

# 查看父命名空间的PID
readlink /proc/self  # 获取真实的PID
```

## User命名空间

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 创建user namespace
unshare --user --map-root-user /bin/bash

# 在新user namespace中
id  # uid=0(root) gid=0(root)

# 查看映射
cat /proc/self/uid_map
# 0 1000 1  (容器内root映射到宿主机UID 1000)

# 外部查看
ps aux | grep bash  # 实际以UID 1000运行
```

## 命名空间管理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查看进程的命名空间
ls -la /proc/self/ns/
ls -la /proc/<pid>/ns/

# 比较两个进程是否在相同命名空间
readlink /proc/<pid1>/ns/pid
readlink /proc/<pid2>/ns/pid

# 进入已有命名空间
sudo nsenter --target <pid> --mount --uts --ipc --net --pid /bin/bash
```

## 完整容器模拟

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
#!/bin/bash
# create_container.sh

CONTAINER_NAME="mycontainer"
ROOTFS="/var/lib/container/rootfs"

# 创建命名空间
unshare --pid --mount --uts --ipc --net --fork --user --map-root-user --mount-proc \
    /bin/bash -c "
        # 设置主机名
        hostname $CONTAINER_NAME
        
        # 挂载rootfs
        mount --bind $ROOTFS $ROOTFS
        cd $ROOTFS
        
        # pivot_root
        mkdir -p old_root
        pivot_root . old_root
        umount -l old_root
        rmdir old_root
        
        # 设置环境
        export PATH=/bin:/sbin:/usr/bin:/usr/sbin
        
        # 启动shell
        exec /bin/bash
    "
```

## 与cgroups结合

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建cgroup
sudo mkdir /sys/fs/cgroup/memory/demo
sudo mkdir /sys/fs/cgroup/cpu/demo

# 设置限制
echo 100000000 | sudo tee /sys/fs/cgroup/memory/demo/memory.limit_in_bytes
echo 50000 | sudo tee /sys/fs/cgroup/cpu/demo/cpu.cfs_quota_us

# 在命名空间中运行并加入cgroup
sudo unshare --pid --mount --uts --ipc --net --fork --mount-proc \
    /bin/bash -c "
        echo \$$ | sudo tee /sys/fs/cgroup/memory/demo/cgroup.procs
        echo \$$ | sudo tee /sys/fs/cgroup/cpu/demo/cgroup.procs
        exec /bin/bash
    "
```

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```
