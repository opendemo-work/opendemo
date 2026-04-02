# oVirt Management

oVirt虚拟化管理平台演示。

## 架构组件

```
oVirt架构:
┌─────────────────────────────────────────┐
│  Engine (管理节点)                       │
│  - Web界面                               │
│  - REST API                             │
├─────────────────────────────────────────┤
│  Hosts (计算节点)                        │
│  - KVM虚拟化                             │
│  - VDSM代理                              │
├─────────────────────────────────────────┤
│  Storage                                │
│  - NFS/iSCSI/Gluster                     │
└─────────────────────────────────────────┘
```

## 基本操作

```bash
# oVirt Shell
ovirt-shell

# 列出虚拟机
list vms

# 启动虚拟机
action vm my-vm start
```

## 存储域

```bash
# 创建NFS存储域
engine-config -s 
```

## 学习要点

1. Engine与Host关系
2. 数据中心概念
3. 存储域管理
4. 模板与快照
