# Libvirt Management

Libvirt虚拟化管理工具演示。

## 架构概览

```
Libvirt架构:
┌─────────────────────────────────────────┐
│  Applications                           │
│  (virt-manager, virsh, OpenStack)       │
├─────────────────────────────────────────┤
│  Libvirt Daemon                         │
│  - API接口                              │
│  - 资源管理                             │
├─────────────────────────────────────────┤
│  Drivers                                │
│  QEMU/KVM │ Xen │ VMware │ Hyper-V     │
├─────────────────────────────────────────┤
│  Hypervisors                            │
└─────────────────────────────────────────┘
```

## 常用命令

```bash
# 虚拟机管理
virsh list --all
virsh start vm-name
virsh shutdown vm-name
virsh destroy vm-name

# 资源池管理
virsh pool-list
virsh pool-define-as mypool dir - - - - /vm/pool
virsh pool-build mypool

# 网络管理
virsh net-list
virsh net-edit default
```

## XML配置

```xml
<domain type='kvm'>
  <name>ubuntu-vm</name>
  <memory unit='KiB'>2097152</memory>
  <vcpu>2</vcpu>
  <os>
    <type arch='x86_64'>hvm</type>
  </os>
</domain>
```

## 学习要点

1. Libvirt API使用
2. XML配置详解
3. 生命周期管理
4. 网络与存储配置
