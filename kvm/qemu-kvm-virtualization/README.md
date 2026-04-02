# QEMU/KVM Virtualization

QEMU/KVM虚拟化基础演示。

## 架构原理

```
QEMU+KVM架构:
┌─────────────────────────────────────────┐
│  Guest OS                               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │  App    │ │  App    │ │  App    │   │
│  └────┬────┘ └────┬────┘ └────┬────┘   │
│       └───────────┴───────────┘        │
│              Guest Kernel               │
├─────────────────────────────────────────┤
│  /dev/kvm                               │
├─────────────────────────────────────────┤
│  KVM (Kernel Module)                    │
│  - CPU virtualization                   │
│  - Memory management                    │
├─────────────────────────────────────────┤
│  QEMU                                   │
│  - Device emulation                     │
│  - I/O handling                         │
├─────────────────────────────────────────┤
│  Host Kernel                            │
└─────────────────────────────────────────┘
```

## 基本操作

```bash
# 创建虚拟机
qemu-system-x86_64 \
  -m 2048 \
  -smp 2 \
  -enable-kvm \
  -hda ubuntu.qcow2 \
  -cdrom ubuntu.iso \
  -boot d

# 使用virt-manager图形界面
sudo apt install virt-manager
virt-manager
```

## 性能优化

```bash
# CPU设置
-cpu host,-kvm -smp cores=4,threads=2

# 磁盘缓存
drive file=disk.qcow2,cache=none,aio=native
```

## 学习要点

1. KVM内核模块
2. QEMU设备模拟
3. VirtIO驱动
4. 性能调优技巧
