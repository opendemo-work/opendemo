# KVM Installation & Configuration Demo

KVM安装与配置完整演示指南。

## 环境要求

- CPU支持虚拟化 (VT-x/AMD-V)
- Linux操作系统 (Ubuntu/CentOS)
- 4GB+ 内存

## 安装步骤

### 1. 检查CPU虚拟化支持

```bash
# Intel CPU
egrep -c '(vmx)' /proc/cpuinfo

# AMD CPU
egrep -c '(svm)' /proc/cpuinfo

# 查看KVM模块
lsmod | grep kvm
```

### 2. 安装KVM (Ubuntu)

```bash
sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager

# 启动服务
sudo systemctl start libvirtd
sudo systemctl enable libvirtd

# 添加用户到libvirt组
sudo usermod -aG libvirt $USER
```

### 3. 安装KVM (CentOS)

```bash
sudo yum install -y qemu-kvm libvirt libvirt-python libguestfs-tools virt-install

sudo systemctl start libvirtd
sudo systemctl enable libvirtd
```

### 4. 验证安装

```bash
virsh list --all
virt-host-validate
```

## 网络配置

### 创建网桥

```bash
# 编辑网络配置
sudo nano /etc/netplan/01-netcfg.yaml

# 配置内容
network:
  version: 2
  bridges:
    br0:
      interfaces: [enp0s3]
      dhcp4: true
```

## 创建虚拟机

```bash
# 使用virt-install
virt-install \
  --name ubuntu-vm \
  --ram 2048 \
  --disk path=/var/lib/libvirt/images/ubuntu.qcow2,size=20 \
  --vcpus 2 \
  --os-type linux \
  --os-variant ubuntu20.04 \
  --network bridge=br0 \
  --graphics none \
  --console pty,target_type=serial \
  --location 'http://archive.ubuntu.com/ubuntu/dists/focal/main/installer-amd64/'
```

## 常用命令

```bash
# 列出虚拟机
virsh list --all

# 启动虚拟机
virsh start ubuntu-vm

# 停止虚拟机
virsh shutdown ubuntu-vm

# 强制停止
virsh destroy ubuntu-vm

# 删除虚拟机
virsh undefine ubuntu-vm --remove-all-storage
```
