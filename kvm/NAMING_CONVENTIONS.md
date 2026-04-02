# KVM 命名规范

## 虚拟机命名

### 虚拟机名称格式
```
<环境>-<角色>-<序号>
prod-web-01        # 生产环境Web服务器01
dev-db-01          # 开发环境数据库01
test-app-03        # 测试环境应用服务器03
```

### 虚拟机文件命名
```
vm-<name>.xml          # 虚拟机配置文件
<name>-disk1.qcow2     # 磁盘镜像文件
<name>-snapshot1.qcow2 # 快照文件
```

## 网络命名

### 虚拟网络
```
default              # 默认NAT网络
br0, br1             # 网桥
vmnet-<id>           # VMware风格网络
```

## 存储命名

### 存储池
```
default              # 默认存储池
images               # 镜像存储池
vms                  # 虚拟机存储池
backups              # 备份存储池
```

## 资源命名

### CPU/内存
```
vcpu-<id>            # 虚拟CPU
memory-<id>          # 内存区域
```
