# KVM - 虚拟化技术演示

> 包含11个案例：KVM安装配置、虚拟机管理、网络配置、存储管理、性能调优

## 简介

本目录包含KVM虚拟化技术的实战演示案例，涵盖KVM安装、虚拟机管理、网络配置、存储管理等核心内容。

## 案例列表

### KVM基础
- kvm-installation-config - KVM安装与配置
- libvirt-management - Libvirt管理工具
- qemu-kvm-virtualization - QEMU-KVM虚拟化

### KVM网络与存储
- kvm-networking - KVM网络配置
- kvm-storage-management - KVM存储管理

## 快速开始

```bash
# 检查CPU虚拟化支持
egrep -c '(vmx|svm)' /proc/cpuinfo

# 安装KVM
sudo apt install qemu-kvm libvirt-daemon-system virt-manager

# 启动libvirtd
sudo systemctl start libvirtd
```

## 学习路径

```
KVM基础 → Libvirt管理 → 网络配置 → 存储管理 → 高级特性
```
