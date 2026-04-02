# QEMU/KVM Internals

QEMU/KVM虚拟化原理深度解析。

## 架构对比

```
纯QEMU:                     QEMU+KVM:
┌─────────┐                ┌─────────┐
│  Guest  │                │  Guest  │
├─────────┤                ├─────────┤
│  QEMU   │                │  QEMU   │
│  (二进制│                │  (设备) │
│   翻译) │                ├─────────┤
├─────────┤                │  KVM    │
│  Host   │                │ (内核)  │
└─────────┘                ├─────────┤
                           │  Host   │
                           │  Kernel │
                           └─────────┘

性能: 慢                      性能: 接近原生
```

## CPU虚拟化

### 硬件加速
```
VT-x技术:
┌────────────────────────────────────┐
│           Guest OS                 │
│  ┌─────────┐    ┌─────────┐       │
│  │ Ring 3  │    │ Ring 0  │──VMX──┼──▶ VM Exit
│  │ (User)  │    │ (Kernel)│       │    (切换到Host)
│  └─────────┘    └─────────┘       │
└────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────┐
│           Host OS (KVM)            │
│  ┌─────────────────────────────┐   │
│  │     VMX Root Operation      │   │
│  │     (处理VM Exit)           │   │
│  └─────────────────────────────┘   │
└────────────────────────────────────┘
```

## 内存虚拟化

```bash
# EPT (Extended Page Tables)
# 硬件辅助的二级地址转换

cat /proc/cpuinfo | grep ept

# 查看KVM内存使用
virsh nodememstats

# 大页内存支持
echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
```

## 设备虚拟化

### VirtIO
```
VirtIO架构:
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Guest  │    │  VirtIO │    │  Host   │
│ Driver  │◄──►│  Queue  │◄──►│ Backend │
└─────────┘    └─────────┘    └─────────┘
   (前端)         (队列)         (后端)
```

### 设备直通
```bash
# SR-IOV网卡直通
# 1. 在BIOS启用VT-d
# 2. 绑定VFIO驱动

# 查看IOMMU组
find /sys/kernel/iommu_groups/ -type l

# 绑定到vfio-pci
echo "8086 10c9" | sudo tee /sys/bus/pci/drivers/vfio-pci/new_id

# 配置直通
virsh attach-device vm-name device.xml
```

## 性能调优

```bash
# CPU pinning
taskset -pc 0-3 <qemu-pid>

# 查看exit原因
perf kvm stat live

# 分析性能瓶颈
cat /sys/kernel/debug/kvm/
```
