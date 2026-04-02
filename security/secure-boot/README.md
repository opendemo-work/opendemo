# Secure Boot

UEFI安全启动实践演示。

## 安全启动链

```
信任链 (Chain of Trust):
┌─────────────────────────────────────────────────────────┐
│  Root of Trust                                          │
│  ┌─────────────┐                                        │
│  │  Platform   │  ← 硬件根密钥 ( burned in firmware )   │
│  │    Key      │                                        │
│  └──────┬──────┘                                        │
├─────────┼───────────────────────────────────────────────┤
│  UEFI   │                                               │
│  ┌──────┴──────┐                                        │
│  │  db (whitelist)  ← 允许签名的证书                    │
│  │  dbx (blacklist) ← 撤销的证书                        │
│  │  KEK            ← 更新db的密钥                        │
│  └──────┬──────┘                                        │
├─────────┼───────────────────────────────────────────────┤
│  Boot   │                                               │
│  ┌──────┴──────┐                                        │
│  │  Bootloader │  ← shim/GRUB2 (signed)                 │
│  └──────┬──────┘                                        │
├─────────┼───────────────────────────────────────────────┤
│  OS     │                                               │
│  ┌──────┴──────┐                                        │
│  │   Kernel    │  ← Linux Kernel (signed)               │
│  │   Modules   │  ← Kernel modules (signed)             │
│  └─────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

## 检查安全启动状态

```bash
# 检查安全启动状态
mokutil --sb-state
# SecureBoot enabled

# 查看 enrolled keys
mokutil --list-enrolled

# 查看 MokList (Machine Owner Key)
mokutil --list-new

# 查看详细的UEFI变量
efivar -l | grep -i secure
```

## 签名内核模块

```bash
# 生成MOK密钥对
openssl req -new -x509 -newkey rsa:2048 \
  -keyout MOK.priv -outform DER -out MOK.der \
  -nodes -days 36500 -subj "/CN=My Secure Boot Key/"

# 导入公钥到MOK
sudo mokutil --import MOK.der
# 设置密码，重启后 enroll

# 签名内核模块
sudo /usr/src/linux-headers-$(uname -r)/scripts/sign-file \
  sha256 \
  ./MOK.priv \
  ./MOK.der \
  /path/to/module.ko

# 验证签名
modinfo /path/to/module.ko | grep sig
```

## 自定义密钥管理

```bash
# 查看当前密钥
sudo efi-readvar -v db	sudo efi-readvar -v KEK
sudo efi-readvar -v PK

# 备份当前密钥
sudo efi-readvar -v db -o db.backup
sudo efi-readvar -v KEK -o KEK.backup
sudo efi-readvar -v PK -o PK.backup

# 使用sbupdate工具 (Arch Linux)
# /etc/sbupdate.conf
ESP_DIR="/boot"
KEY_DIR="/root/secureboot"

# 签名内核
sbupdate
```

## 学习要点

1. UEFI安全启动原理
2. 密钥层级关系 (PK/KEK/db)
3. 内核模块签名流程
4. 自定义密钥管理
5. 双系统安全启动配置
