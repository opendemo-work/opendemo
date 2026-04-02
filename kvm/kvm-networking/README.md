# KVM Networking

KVM虚拟网络配置演示。

## 网络模式

```
网络模式对比:

NAT模式:                    Bridge模式:
┌─────────┐                 ┌─────────┐
│   VM    │ 10.0.2.x        │   VM    │ 192.168.1.x
└────┬────┘                 └────┬────┘
     │ virbr0                    │ br0
┌────┴────┐                 ┌────┴────┐
│  NAT    │                 │ Bridge  │
│10.0.2.2 │                 │192.168.1│
└────┬────┘                 └────┬────┘
     │                           │
┌────┴────┐                 ┌────┴────┐
│  Host   │                 │  Host   │
│192.168.1│                 │192.168.1│
└─────────┘                 └─────────┘
```

## 配置桥接网络

```bash
# 创建桥接
sudo ip link add name br0 type bridge
sudo ip link set br0 up
sudo ip link set eth0 master br0

# 配置VM使用桥接
virsh attach-interface vm-name bridge br0 --persistent
```

## SR-IOV

```bash
# 启用SR-IOV
echo 4 | sudo tee /sys/bus/pci/devices/0000:03:00.0/sriov_numvfs

# 查看VF
ip link show eth0
```

## 学习要点

1. NAT vs Bridge对比
2. Open vSwitch配置
3. SR-IOV直通
4. 网络性能优化
