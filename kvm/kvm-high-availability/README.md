<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# KVM High Availability

KVM高可用架构演示，展示虚拟机热迁移、故障转移和集群管理。

## HA架构设计

```
KVM集群架构:
┌─────────────────────────────────────────────────────────┐
│                     共享存储                              │
│              (NFS/iSCSI/Ceph)                            │
└─────────────────────────────────────────────────────────┘
     │                           │
     │                           │
┌────┴────────┐          ┌──────┴────────┐
│  Node 1     │          │   Node 2      │
│  ┌───────┐  │          │  ┌───────┐    │
│  │ VM 1  │  │◄────────►│  │ VM 2  │    │
│  └───────┘  │  迁移    │  └───────┘    │
│  ┌───────┐  │          │  ┌───────┐    │
│  │ VM 3  │  │          │  │ VM 4  │    │
│  └───────┘  │          │  └───────┘    │
└─────────────┘          └───────────────┘
     │                           │
     └───────────┬───────────────┘
                 │
          ┌──────┴──────┐
          │   Fencing   │
          │   (STONITH) │
          └─────────────┘
```

## 安装Pacemaker集群

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 所有节点安装
sudo apt install pacemaker pcs corosync fence-agents

# 设置密码
sudo passwd hacluster

# 认证节点
sudo pcs cluster auth node1 node2 -u hacluster -p password

# 创建集群
sudo pcs cluster setup --name mycluster node1 node2

# 启动集群
sudo pcs cluster start --all
sudo pcs cluster enable --all

# 查看状态
sudo pcs status
```

## 配置STONITH

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 查看可用fencing代理
sudo pcs stonith list

# 配置IPMI fencing
sudo pcs stonith create ipmi-node1 fence_ipmilan \
  pcmk_host_list=node1 ipaddr=192.168.1.10 \
  login=admin passwd=secret lanplus=1 \
  op monitor interval=60s

# 验证配置
sudo pcs stonith show
```

## 虚拟机资源管理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 将VM添加为资源
sudo pcs resource create vm1 VirtualDomain \
  config=/etc/libvirt/qemu/vm1.xml \
  hypervisor=qemu:///system \
  migration_transport=ssh \
  op start timeout=120s interval=0 \
  op stop timeout=120s interval=0 \
  op monitor timeout=30s interval=10s \
  meta allow-migrate=true

# 设置资源位置偏好
sudo pcs constraint location vm1 prefers node1=100

# 创建资源组
sudo pcs resource group add web-group vm1 vm2
```

## 热迁移

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 在线迁移
virsh migrate --live vm1 qemu+ssh://node2/system

# 使用virsh
virsh migrate --live --verbose vm1 qemu+ssh://node2/system --undefinesource --persistent

# 查看迁移进度
virsh domjobinfo vm1
```

## 存储配置

### NFS共享存储
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 服务端
sudo apt install nfs-kernel-server
echo "/exports/vms 192.168.1.0/24(rw,sync,no_root_squash,no_subtree_check)" | sudo tee -a /etc/exports
sudo exportfs -a

# 客户端
sudo mount -t nfs 192.168.1.100:/exports/vms /var/lib/libvirt/images
```

### iSCSI配置
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 发现target
sudo iscsiadm --mode discovery --type sendtargets --portal 192.168.1.100

# 登录
sudo iscsiadm --mode node --targetname iqn.2024-01.com.example:storage --portal 192.168.1.100 --login

# 查看磁盘
lsblk
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
