# KVM Security

KVM虚拟化安全最佳实践演示。

## 安全架构

```
纵深防御:
┌─────────────────────────────────────────────────────────┐
│  应用层: SELinux/AppArmor沙箱                            │
├─────────────────────────────────────────────────────────┤
│  Hypervisor: sVirt、seccomp                              │
├─────────────────────────────────────────────────────────┤
│  宿主机: 最小化安装、及时补丁                            │
├─────────────────────────────────────────────────────────┤
│  网络: 虚拟网络隔离、防火墙                              │
├─────────────────────────────────────────────────────────┤
│  存储: 加密、访问控制                                    │
└─────────────────────────────────────────────────────────┘
```

## sVirt (SELinux for Virt)

```bash
# 查看sVirt标签
ls -lZ /var/lib/libvirt/images/

# VM进程标签
ps -eZ | grep qemu

# 自定义SELinux策略
semanage fcontext -a -t virt_image_t "/vm(/.*)?"
restorecon -R /vm
```

## 网络安全

```bash
# 启用防火墙
sudo systemctl enable --now firewalld

# 限制VM网络访问
firewall-cmd --zone=internal --add-interface=virbr1

# ebtables过滤
sudo ebtables -A FORWARD -s ! 52:54:00:00:00:00/24 -j DROP
```

## 存储安全

```bash
# 镜像加密
qemu-img convert -O luks --object secret,id=sec0,data=password -o key-secret=sec0 plain.qcow2 encrypted.qcow2

# 安全删除
shred -vfz -n 3 /var/lib/libvirt/images/old-vm.qcow2
```
