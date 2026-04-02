# KVM Templates

KVM虚拟机模板创建与管理演示。

## 创建模板

### 准备黄金镜像
```bash
# 安装基础VM
virt-install --name template-centos8 \
  --memory 2048 --vcpus 2 \
  --disk size=20 --os-variant centos8 \
  --location /var/lib/libvirt/iso/CentOS-8.iso

# 清理特定配置
sudo virt-sysprep -d template-centos8

# 标记为模板
virsh undefine template-centos8 --keep-nvram
```

## 从模板克隆

```bash
# 克隆虚拟机
virt-clone --original-xml /etc/libvirt/qemu/template-centos8.xml \
  --name webserver01 --file /var/lib/libvirt/images/webserver01.qcow2

# 使用qemu-img创建链接克隆
qemu-img create -f qcow2 -b template-centos8.qcow2 webserver01.qcow2

# 重新定义
virt-install --import --name webserver01 --memory 2048 \
  --disk path=/var/lib/libvirt/images/webserver01.qcow2
```

## cloud-init集成

```yaml
# user-data
#cloud-config
hostname: {{ vm_name }}
fqdn: {{ vm_name }}.example.com
users:
  - name: admin
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-rsa AAAAB3...

package_update: true
packages:
  - nginx
  - mysql-server

runcmd:
  - systemctl enable nginx
  - systemctl start nginx
```

## 批量部署

```bash
#!/bin/bash
# deploy-vms.sh

for i in {1..5}; do
  virt-clone --original template-centos8 \
    --name webserver0$i \
    --file /var/lib/libvirt/images/webserver0$i.qcow2
  
  # 生成cloud-init ISO
  cloud-localds webserver0$i-seed.iso webserver0$i-user-data.yaml
  
  virsh attach-disk webserver0$i webserver0$i-seed.iso sdb --type cdrom
  virsh start webserver0$i
done
```
