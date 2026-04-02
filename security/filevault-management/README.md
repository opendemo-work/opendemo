# FileVault Management

macOS FileVault全盘加密管理实践。

## FileVault概述

```
FileVault 2架构:
┌─────────────────────────────────────────────────────────┐
│                    macOS Users                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │              FileVault 2                         │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │   │
│  │  │  User   │ │ Recovery│ │  iCloud │          │   │
│  │  │  Key    │ │  Key    │ │  Key    │          │   │
│  │  └─────────┘ └─────────┘ └─────────┘          │   │
│  ├─────────────────────────────────────────────────┤   │
│  │              CoreStorage                        │   │
│  │         (逻辑卷管理 + XTS-AES-128)              │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                   Physical Disk                         │
└─────────────────────────────────────────────────────────┘
```

## 启用FileVault

```bash
# 命令行启用
sudo fdesetup enable

# 查看状态
sudo fdesetup status
# FileVault is On.

# 查看详细信息
sudo fdesetup list
```

## 个人恢复密钥(PRK)

```bash
# 显示恢复密钥
sudo fdesetup showpersonalrecoverykey

# 或
sudo fdesetup showpersonalrecoverykey -device

# 在MDM中查看
# Jamf Pro / Microsoft Intune
```

## 学习要点

1. FileVault 2加密原理
2. 恢复密钥管理
3. MDM集成部署
4. 用户解锁与迁移
