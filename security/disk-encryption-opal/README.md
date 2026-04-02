# Disk Encryption with OPAL

OPAL自加密硬盘(SED)管理实践。

## OPAL概述

```
SED架构:
┌─────────────────────────────────────────────────────────┐
│                    操作系统                              │
│              (无感知加密)                                │
├─────────────────────────────────────────────────────────┤
│                   存储驱动                               │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │              SED Controller (硬盘内)              │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │   │
│  │  │  AES    │ │  Range  │ │  Admin  │          │   │
│  │  │Engine   │ │  Tables │ │  Auth   │          │   │
│  │  └─────────┘ └─────────┘ └─────────┘          │   │
│  │  ┌─────────────────────────────────────────┐   │   │
│  │  │           加密数据存储区                  │   │   │
│  │  │      (全盘AES-256自动加密)               │   │   │
│  │  └─────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## OPAL标准

| 版本 | 特性 |
|------|------|
| OPAL 1.0 | 基础加密，单用户 |
| OPAL 2.0 | 多用户，范围锁定 |
| OPAL 2.0+ | 阴影MBR，TLS传输 |

## sedutil工具

```bash
# 安装sedutil
wget https://github.com/Drive-Trust-Alliance/sedutil/releases/...
chmod +x sedutil-cli
sudo mv sedutil-cli /usr/local/bin/

# 检查硬盘支持
sedutil-cli --scan

# 查看详细信息
sedutil-cli --query /dev/sda
```

## 初始化SED

```bash
# 1. 创建管理员密码
sedutil-cli --initialsetup password123 /dev/sda

# 2. 启用锁定
sedutil-cli --enablelockingrange 0 password123 /dev/sda

# 3. 设置MBR阴影
sedutil-cli --setmbrdone off password123 /dev/sda
```

## 学习要点

1. OPAL标准与SED原理
2. 硬件加密vs软件加密
3. PBA预启动认证
4. 企业级密钥托管
