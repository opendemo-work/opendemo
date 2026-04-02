# FDE with LUKS

Linux全盘加密(Full Disk Encryption)与LUKS实践演示。

## 什么是FDE

全盘加密(FDE)保护静态数据，防止物理介质丢失/被盗导致的数据泄露：

```
FDE架构:
┌─────────────────────────────────────────────────────────┐
│                    应用程序                              │
│                   (无感知)                               │
├─────────────────────────────────────────────────────────┤
│                   文件系统                               │
│              (ext4/xfs/btrfs)                            │
├─────────────────────────────────────────────────────────┤
│                   dm-crypt                               │
│              (设备映射加密层)                             │
├─────────────────────────────────────────────────────────┤
│                   LUKS Header                            │
│              (密钥槽/配置信息)                            │
├─────────────────────────────────────────────────────────┤
│                   物理磁盘                               │
│              (SSD/HDD/NVMe)                              │
└─────────────────────────────────────────────────────────┘
```

## LUKS版本对比

| 特性 | LUKS1 | LUKS2 |
|------|-------|-------|
| 发布年份 | 2004 | 2018 |
| 密钥槽数量 | 8 | 32 |
| 加密算法 | 固定 | 可扩展 |
| 损坏恢复 | 有限 | 更好的冗余 |
| 在线调整 | 不支持 | 支持 |

## 创建加密卷

### 格式化新设备
```bash
# 安装cryptsetup
sudo apt install cryptsetup

# 查看设备
lsblk
sudo fdisk -l /dev/sdb

# 创建LUKS容器
sudo cryptsetup luksFormat \
  --type luks2 \
  --cipher aes-xts-plain64 \
  --key-size 512 \
  --hash sha512 \
  --iter-time 5000 \
  /dev/sdb

# 确认并输入密码
WARNING: This will overwrite data!
Are you sure? (Type uppercase yes): YES
Enter passphrase: ********
Verify passphrase: ********
```

### 打开加密卷
```bash
# 打开设备
sudo cryptsetup luksOpen /dev/sdb secure_data

# 查看映射
ls /dev/mapper/
# secure_data -> /dev/dm-0

# 创建文件系统
sudo mkfs.ext4 /dev/mapper/secure_data

# 挂载使用
sudo mkdir -p /mnt/secure
sudo mount /dev/mapper/secure_data /mnt/secure
```

## 密钥管理

### 多个密钥槽
```bash
# 查看密钥槽状态
sudo cryptsetup luksDump /dev/sdb

# Slot 0: ENABLED (管理员密码)
# Slot 1: DISABLED
# Slot 2: DISABLED

# 添加备份密码到Slot 1
sudo cryptsetup luksAddKey /dev/sdb
Enter any existing passphrase: ********
Enter new passphrase for key slot: ********

# 添加密钥文件
sudo dd if=/dev/urandom of=/root/luks-keyfile bs=4096 count=1
sudo chmod 600 /root/luks-keyfile
sudo cryptsetup luksAddKey /dev/sdb /root/luks-keyfile
```

### 密钥轮换
```bash
# 更改指定槽位的密码
sudo cryptsetup luksChangeKey /dev/sdb -S 0
Enter passphrase to be changed: ********
Enter new passphrase: ********
```

## 系统全盘加密

### 安装时启用FDE
```bash
# Ubuntu安装器选项
# 选择 "Encrypt the new Ubuntu installation for security"
# 选择 "Use LVM with the new Ubuntu installation"

# 或手动分区方案
/boot     - 未加密 (500MB)
/         - LUKS加密 (剩余空间)
swap      - 加密交换分区
```

### 手动配置启动
```bash
# /etc/crypttab
data UUID=xxxxx-xxxxx-xxxxx none luks,discard,timeout=30

# /etc/fstab
/dev/mapper/data /data ext4 defaults 0 2

# 更新initramfs
sudo update-initramfs -u
```

## 性能优化

### 加密对性能的影响
```
性能对比 (NVMe SSD):
┌────────────────┬──────────────┬──────────────┐
│    操作        │   无加密     │   LUKS加密    │
├────────────────┼──────────────┼──────────────┤
│ 顺序读         │ 3500 MB/s    │ 3200 MB/s    │
│ 顺序写         │ 3000 MB/s    │ 2800 MB/s    │
│ 随机读 IOPS    │ 600K         │ 550K         │
│ 随机写 IOPS    │ 550K         │ 500K         │
│ CPU占用        │ 0%           │ 5-10%        │
└────────────────┴──────────────┴──────────────┘
```

### 启用硬件加速
```bash
# 检查CPU AES-NI支持
grep -o aes /proc/cpuinfo | head -1
# 输出 'aes' 表示支持

# 现代CPU自动使用AES-NI指令集
# cryptsetup会自动检测并使用

# 验证加密算法
cryptsetup benchmark
```

## 备份与恢复

### 备份LUKS头
```bash
# 备份头部 (必须!)
sudo cryptsetup luksHeaderBackup /dev/sdb \
  --header-backup-file /backup/luks-header-backup.img

# 存储到安全位置 (加密U盘/离线存储)

# 恢复头部 (紧急情况)
sudo cryptsetup luksHeaderRestore /dev/sdb \
  --header-backup-file /backup/luks-header-backup.img
```

### 数据恢复
```bash
# 如果头部损坏但数据区完好
# 需要知道确切的偏移量和参数
sudo cryptsetup open --type plain \
  --cipher aes-xts-plain64 \
  --offset 4096 \
  /dev/sdb recovered_data
```

## 学习要点

1. LUKS1 vs LUKS2的选择
2. 密钥槽管理与备份策略
3. 系统启动时自动解锁
4. 性能影响与硬件加速
5. 灾难恢复计划
