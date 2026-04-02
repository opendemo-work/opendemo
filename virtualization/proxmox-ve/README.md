# Proxmox VE

Proxmox VE开源虚拟化平台演示。

## 架构特点

```
Proxmox VE:
┌─────────────────────────────────────────┐
│  Web GUI / API                          │
├─────────────────────────────────────────┤
│  pve-cluster (Corosync)                 │
├─────────────────────────────────────────┤
│  KVM + LXC                              │
├─────────────────────────────────────────┤
│  Ceph / ZFS / LVM                       │
└─────────────────────────────────────────┘
```

## 基本操作

```bash
# 通过CLI管理
qm list
qm start 100
qm shutdown 100

# LXC容器
pct list
pct start 200

# 集群管理
pvecm status
pvecm nodes
```

## 存储配置

```bash
# ZFS存储
zpool create tank raidz1 sda sdb sdc
zfs create tank/vm-storage

# 添加到Proxmox
pvesm add zfspool tank --pool tank/vm-storage
```

## 学习要点

1. Web管理界面
2. KVM与LXC对比
3. 集群高可用
4. Ceph分布式存储
