# LXC Containers

LXC (Linux Containers) 系统容器演示。

## LXC vs Docker

```
对比:
LXC:                        Docker:
┌──────────────┐            ┌──────────────┐
│ 系统容器      │            │ 应用容器      │
│ 完整OS       │            │ 单进程       │
│ 多进程       │            │ 轻量级       │
│ 更接近VM    │            │ 更适合微服务  │
└──────────────┘            └──────────────┘
```

## 安装LXC

```bash
# Ubuntu
sudo apt install lxc lxc-templates

# CentOS
sudo yum install epel-release
sudo yum install lxc lxc-templates

# 检查配置
sudo lxc-checkconfig
```

## 创建容器

```bash
# 创建容器
sudo lxc-create -n mycontainer -t ubuntu -- -r focal

# 列出容器
sudo lxc-ls --fancy

# 启动容器
sudo lxc-start -n mycontainer -d

# 进入容器
sudo lxc-attach -n mycontainer

# 停止容器
sudo lxc-stop -n mycontainer

# 销毁容器
sudo lxc-destroy -n mycontainer
```

## 容器配置

```bash
# 编辑配置
sudo nano /var/lib/lxc/mycontainer/config

# 设置资源限制
lxc.cgroup.memory.limit_in_bytes = 512M
lxc.cgroup.cpu.shares = 256

# 网络配置
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
```

## LXD管理

```bash
# 初始化LXD
sudo lxd init

# 创建容器
lxc launch ubuntu:22.04 mycontainer

# 列出容器
lxc list

# 执行命令
lxc exec mycontainer -- bash

# 文件传输
lxc file push local.txt mycontainer/tmp/
lxc file pull mycontainer/etc/hosts .

# 快照
lxc snapshot mycontainer snap1
lxc restore mycontainer snap1

# 删除容器
lxc delete mycontainer
```
