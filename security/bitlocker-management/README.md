# BitLocker Management

Windows BitLocker加密管理实践。

## BitLocker架构

```
BitLocker组件:
┌─────────────────────────────────────────────────────────┐
│              BitLocker Drive Encryption                 │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │  TPM    │ │ USB Key │ │ Password│ │  AD DS  │      │
│  │ Module  │ │         │ │         │ │ Backup  │      │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘      │
├───────┴───────────┴───────────┴───────────┴───────────┤
│                   FVE Filter Driver                     │
├─────────────────────────────────────────────────────────┤
│                   Encrypted Volume                      │
└─────────────────────────────────────────────────────────┘
```

## 启用BitLocker

```powershell
# 检查TPM状态
Get-Tpm

# 启用BitLocker (TPM+PIN)
Enable-BitLocker -MountPoint C: -EncryptionMethod Aes256 -Pin $(ConvertTo-SecureString "123456" -AsPlainText -Force) -RecoveryPasswordProtector

# 启用BitLocker (仅密码)
Enable-BitLocker -MountPoint D: -EncryptionMethod Aes256 -PasswordProtector

# 检查加密进度
Get-BitLockerVolume -MountPoint C: | Select-Object EncryptionPercentage
```

## 恢复密钥管理

```powershell
# 查看恢复密钥
(Get-BitLockerVolume -MountPoint C:).KeyProtector

# 备份到AD
Backup-BitLockerKeyProtector -MountPoint C: -KeyProtectorId "{xxx}"

# 保存到文件
(Get-BitLockerVolume -MountPoint C:).KeyProtector | 
  Where-Object {$_.KeyProtectorType -eq 'RecoveryPassword'} |
  Select-Object -ExpandProperty RecoveryPassword |
  Out-File C:\RecoveryKey.txt
```

## 学习要点

1. TPM与PIN组合认证
2. 恢复密钥备份策略
3. 企业级BitLocker管理
4. 网络解锁(NBUnlocker)
