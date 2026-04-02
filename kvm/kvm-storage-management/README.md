# KVM Storage Management

KVM虚拟存储管理演示。

## 存储类型

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| 本地文件 | 简单管理 | 开发测试 |
| LVM | 动态扩展 | 生产环境 |
| iSCSI | 块设备 | 共享存储 |
| Ceph | 分布式 | 大规模部署 |
| NFS | 网络文件 | 共享数据 |

## 磁盘管理

```bash
# 创建磁盘
qemu-img create -f qcow2 vm-disk.qcow2 50G

# 调整大小
qemu-img resize vm-disk.qcow2 +10G

# 快照管理
qemu-img snapshot -c snapshot1 vm-disk.qcow2
qemu-img snapshot -l vm-disk.qcow2

# 备份
cp vm-disk.qcow2 vm-disk-backup.qcow2
```

## 存储池

```bash
# 创建目录池
virsh pool-define-as mypool dir - - - - /vm/pool
virsh pool-build mypool
virsh pool-start mypool
virsh pool-autostart mypool
```

## 学习要点

1. 存储池类型选择
2. 磁盘格式对比
3. 快照与备份策略
4. 存储性能优化
