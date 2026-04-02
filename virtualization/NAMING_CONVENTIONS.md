# Virtualization 命名规范

## 虚拟机命名

### 通用格式
```
<platform>-<env>-<role>-<id>
esxi-prod-web-01       # ESXi生产Web服务器
proxmox-dev-db-01      # Proxmox开发数据库
xen-test-app-01        # Xen测试应用
```

### 模板命名
```
template-<os>-<version>
template-centos-8
template-ubuntu-2204
template-windows-2022
```

### 快照命名
```
snapshot-<vm-name>-<date>-<desc>
snapshot-web01-20240401-before-update
```

## 资源命名

### 资源池
```
compute-pool           # 计算资源池
memory-pool            # 内存资源池
storage-pool-ssd       # SSD存储池
storage-pool-hdd       # HDD存储池
```

### 虚拟磁盘
```
<vm-name>-sys.vmdk     # 系统盘
<vm-name>-data.vmdk    # 数据盘
<vm-name>-log.vmdk     # 日志盘
```

## 网络命名

### 虚拟网络
```
vm-network             # 虚拟机网络
management-network     # 管理网络
storage-network        # 存储网络
public-network         # 公网网络
```

## 文档命名

### 案例目录
```
virtualization-concepts     # 虚拟化概念
vmware-vsphere-basics       # VMware vSphere基础
proxmox-ve                  # Proxmox VE
xen-hypervisor              # Xen虚拟化
ovirt-management            # oVirt管理平台
```
