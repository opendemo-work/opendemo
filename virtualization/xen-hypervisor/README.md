# Xen Hypervisor

Xen开源虚拟化平台演示。

## 架构模式

```
Xen架构:
┌─────────────────────────────────────────┐
│  Domain 0 (Dom0)                        │
│  - 特权域                                │
│  - 设备驱动                              │
│  - 管理工具                              │
├─────────────────────────────────────────┤
│  Xen Hypervisor                         │
├─────────────────────────────────────────┤
│  Domain U (DomU)                        │
│  - 普通虚拟机                            │
│  - PV/HVM模式                            │
└─────────────────────────────────────────┘
```

## 安装管理

```bash
# Xen工具
xl list
xl create /etc/xen/vm.cfg
xl destroy vm-name

# 配置文件
cat /etc/xen/vm.cfg
name = "ubuntu"
memory = 2048
vcpus = 2
disk = ['file:/vm/disk.img,xvda,w']
```

## PV vs HVM

| 特性 | PV | HVM |
|------|-----|-----|
| 性能 | 高 | 中 |
| 兼容性 | 需修改内核 | 无需修改 |
| 硬件支持 | 不需要 | 需要VT-x |

## 学习要点

1. Dom0/DomU概念
2. PV与HVM对比
3. xl工具使用
4. 性能优化
