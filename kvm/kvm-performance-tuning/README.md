# KVM Performance Tuning

KVM性能调优最佳实践，展示CPU、内存、磁盘、网络的优化策略。

## 性能调优概览

```
KVM性能优化层次:
┌─────────────────────────────────────────┐
│           应用层优化                      │
│    (NUMA感知、CPU亲和性、大页内存)         │
├─────────────────────────────────────────┤
│           虚拟化层优化                    │
│    (virtio驱动、设备直通、KVM加速)         │
├─────────────────────────────────────────┤
│           宿主机优化                      │
│    (内核参数、I/O调度器、网络调优)         │
├─────────────────────────────────────────┤
│           硬件层优化                      │
│    (CPU VT-x/AMD-V、SR-IOV、NVMe)         │
└─────────────────────────────────────────┘
```

## CPU优化

### CPU模式和特性
```bash
# 查看主机CPU特性
grep -E 'vmx|svm' /proc/cpuinfo | head -5

# 推荐CPU配置
virt-install \
  --cpu host-passthrough,cache.mode=passthrough \
  --vcpus 4,sockets=1,cores=4,threads=1 \
  ...
```

### CPU拓扑优化
```xml
<cpu mode='host-passthrough' check='none'>
  <topology sockets='2' cores='4' threads='2'/>
  <numa>
    <cell id='0' cpus='0-7' memory='16777216'/>
    <cell id='1' cpus='8-15' memory='16777216'/>
  </numa>
</cpu>
```

### CPU亲和性
```bash
# 设置vCPU绑定物理CPU
virsh vcpupin vm-name 0 0
virsh vcpupin vm-name 1 1
virsh vcpupin vm-name 2 2
virsh vcpupin vm-name 3 3

# 批量设置
for i in {0..3}; do
    virsh vcpupin vm-name $i $i
done
```

### 嵌套虚拟化
```xml
<cpu mode='host-passthrough' check='none'>
  <feature policy='require' name='vmx'/>
</cpu>
```

## 内存优化

### 大页内存 (HugePages)
```bash
# 查看当前大页配置
cat /proc/meminfo | grep Huge

# 预留大页内存
echo 1024 | sudo tee /proc/sys/vm/nr_hugepages

# 持久化配置
echo 'vm.nr_hugepages = 1024' | sudo tee /etc/sysctl.d/99-hugepages.conf

# 验证
sysctl vm.nr_hugepages
```

### 透明大页 (THP)
```bash
# 查看THP状态
cat /sys/kernel/mm/transparent_hugepage/enabled

# 启用透明大页
echo always | sudo tee /sys/kernel/mm/transparent_hugepage/enabled

# 虚拟机XML配置
<memoryBacking>
  <hugepages/>
</memoryBacking>
```

### 内存气球 (Ballooning)
```xml
<memballoon model='virtio'>
  <stats period='5'/>
</memballoon>
```

```bash
# 查看内存气球状态
virsh qemu-monitor-command vm-name --hmp info balloon

# 设置当前内存
virsh setmem vm-name 4G --current
```

### KSM (Kernel Same-page Merging)
```bash
# 启用KSM
echo 1 | sudo tee /sys/kernel/mm/ksm/run

# 调整扫描参数
echo 1000 | sudo tee /sys/kernel/mm/ksm/pages_to_scan

# 查看节省内存
cat /sys/kernel/mm/ksm/pages_sharing
cat /sys/kernel/mm/ksm/pages_shared
```

## 磁盘I/O优化

### 磁盘缓存模式
```xml
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2' cache='none' io='native'/>
  <source file='/var/lib/libvirt/images/vm.qcow2'/>
  <target dev='vda' bus='virtio'/>
</disk>
```

| 缓存模式 | 数据安全 | 性能 | 适用场景 |
|---------|---------|------|---------|
| none | 高 | 中 | 数据库生产环境 |
| writethrough | 高 | 低 | 一般应用 |
| writeback | 低 | 高 | 开发测试环境 |
| unsafe | 最低 | 最高 | 临时/缓存数据 |

### I/O调度器
```bash
# 查看当前调度器
cat /sys/block/sda/queue/scheduler

# 设置调度器 (NVMe推荐none)
echo none | sudo tee /sys/block/nvme0n1/queue/scheduler

# SSD推荐mq-deadline
echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler
```

### 磁盘预分配
```bash
# 创建预分配磁盘 (性能更好)
qemu-img create -f qcow2 -o preallocation=metadata vm.qcow2 100G

# 完全预分配 (最佳性能)
qemu-img create -f qcow2 -o preallocation=falloc vm.qcow2 100G

# 转换为raw (最高性能)
qemu-img convert -f qcow2 -O raw vm.qcow2 vm.raw
```

### Virtio-blk vs Virtio-scsi
```xml
<!-- Virtio-blk -->
<disk type='file' device='disk'>
  <target dev='vda' bus='virtio'/>
</disk>

<!-- Virtio-scsi (支持更多设备) -->
<controller type='scsi' index='0' model='virtio-scsi'/>
<disk type='file' device='disk'>
  <target dev='sda' bus='scsi'/>
</disk>
```

### iothreads
```xml
<iothreads>4</iothreads>
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2' iothread='1'/>
  <target dev='vda' bus='virtio'/>
</disk>
```

## 网络优化

### 网络模式对比
```
NAT模式:                   桥接模式:
┌──────────────┐          ┌──────────────┐
│   VM (NAT)   │          │   VM (桥接)   │
│   10.0.2.15  │          │   192.168.1.50│
└──────┬───────┘          └──────┬───────┘
       │                         │
┌──────┴───────┐          ┌──────┴───────┐
│    NAT       │          │    br0       │
│  192.168.1.10│          │  192.168.1.10│
└──────────────┘          └──────────────┘
   (端口映射)                (同网段IP)
```

### SR-IOV网络直通
```xml
<interface type='hostdev' managed='yes'>
  <source>
    <address type='pci' domain='0x0000' bus='0x04' slot='0x10' function='0x0'/>
  </source>
  <mac address='52:54:00:6d:90:02'/>
</interface>
```

### 多队列网卡
```xml
<interface type='network'>
  <mac address='52:54:00:6d:90:01'/>
  <source network='default'/>
  <model type='virtio'/>
  <driver name='vhost' queues='4'/>
</interface>
```

### vhost-net加速
```bash
# 加载vhost-net模块
sudo modprobe vhost-net

# XML配置
<interface type='network'>
  <model type='virtio'/>
  <driver name='vhost'/>
</interface>
```

## 宿主机优化

### 内核参数
```bash
# /etc/sysctl.d/99-kvm.conf
# 内存优化
vm.swappiness = 10
vm.dirty_ratio = 40
vm.dirty_background_ratio = 10

# 网络优化
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

# 启用KVM嵌套虚拟化
options kvm-intel nested=1
options kvm-amd nested=1
```

### CPU隔离
```bash
# 隔离特定CPU用于虚拟机
# /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="isolcpus=2-7 nohz_full=2-7 rcu_nocbs=2-7"

# 更新grub
sudo update-grub
```

## 性能监控

### 使用perf
```bash
# 采样CPU性能
sudo perf kvm stat live

# 记录事件
sudo perf record -e kvm:* -a -- sleep 10
sudo perf report
```

### 使用qemu-monitor
```bash
# 查看统计信息
virsh qemu-monitor-command vm-name --hmp info cpus
virsh qemu-monitor-command vm-name --hmp info registers
virsh qemu-monitor-command vm-name --hmp info tlb
```

### 使用virt-top
```bash
# 实时查看虚拟机资源使用
virt-top

# 导出CSV
virt-top --csv /tmp/virt-stats.csv --time 60
```

## 基准测试

### CPU测试
```bash
# 安装sysbench
sudo apt install sysbench

# CPU基准测试
sysbench cpu --cpu-max-prime=20000 run
```

### 磁盘测试
```bash
# FIO测试
fio --name=randread --ioengine=libaio --iodepth=32 \
    --rw=randread --bs=4k --direct=1 --size=4G \
    --numjobs=4 --runtime=60 --group_reporting
```

### 网络测试
```bash
# iperf3测试
# 服务端
iperf3 -s

# 客户端
iperf3 -c <server_ip> -t 30 -P 4
```

## 学习要点

1. CPU亲和性和NUMA拓扑优化
2. 大页内存和内存去重
3. 磁盘缓存策略和I/O调度
4. SR-IOV和多队列网卡
5. 性能监控和基准测试
