# VMware vSphere Basics

VMware vSphere虚拟化平台演示。

## vSphere组件

```
vSphere架构:
┌─────────────────────────────────────────┐
│  vCenter Server                         │
│  - 集中管理                              │
│  - vMotion                              │
│  - DRS/HA                               │
├─────────────────────────────────────────┤
│  ESXi Hosts                             │
│  - Hypervisor                           │
│  - 虚拟机运行                            │
├─────────────────────────────────────────┤
│  Datastores                             │
│  - VMFS                                 │
│  - NFS/iSCSI                            │
└─────────────────────────────────────────┘
```

## ESXi安装配置

```bash
# 通过vSphere Client连接
# 或使用PowerCLI
Install-Module VMware.PowerCLI
Connect-VIServer vcenter.local -Credential (Get-Credential)

# 创建虚拟机
New-VM -Name "MyVM" -VMHost "esxi01.local" `
       -Datastore "datastore1" -DiskGB 50 `
       -MemoryGB 4 -NumCpu 2
```

## 学习要点

1. vCenter管理
2. vMotion迁移
3. DRS资源调度
4. HA高可用
