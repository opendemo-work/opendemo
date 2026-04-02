# KVM Backup and Recovery

KVM虚拟机备份与恢复策略演示。

## 备份策略

### 离线备份
```bash
# 关机后备份
virsh shutdown vm-name
sudo cp /var/lib/libvirt/images/vm-name.qcow2 /backup/vm-name-$(date +%Y%m%d).qcow2
virsh start vm-name
```

### 在线备份 (快照)
```bash
# 创建外部快照
virsh snapshot-create-as --domain vm-name --name backup-$(date +%Y%m%d) \
  --disk-only --atomic

# 复制基础镜像
cp /var/lib/libvirt/images/vm-name.qcow2 /backup/

# 合并快照
virsh blockcommit vm-name vda --active --pivot
```

## 增量备份

```bash
# 基于rsync的增量备份
rsync -av --progress /var/lib/libvirt/images/vm-name.qcow2 /backup/

# qemu-img备份
qemu-img convert -O qcow2 -c vm-name.qcow2 /backup/vm-name-$(date +%Y%m%d).qcow2
```

## 恢复操作

```bash
# 从备份恢复
sudo cp /backup/vm-name-20240101.qcow2 /var/lib/libvirt/images/vm-name.qcow2

# 重新定义XML
virsh define /backup/vm-name.xml

# 启动虚拟机
virsh start vm-name
```

## 自动化脚本

```bash
#!/bin/bash
# backup-all-vms.sh

BACKUP_DIR="/backup/kvm"
DATE=$(date +%Y%m%d)

for vm in $(virsh list --all --name); do
    echo "Backing up $vm..."
    virsh dumpxml $vm > $BACKUP_DIR/$vm-$DATE.xml
    qemu-img convert -O qcow2 -c /var/lib/libvirt/images/$vm.qcow2 \
        $BACKUP_DIR/$vm-$DATE.qcow2
done
```
