# Enterprise Encryption Deployment

企业级全盘加密部署方案演示。

## 企业FDE架构

```
企业级加密部署架构:
┌─────────────────────────────────────────────────────────┐
│                  中央管理平台 (MDM/SCCM)                  │
│         ┌─────────────────────────────────────┐         │
│         │   Microsoft Intune / Jamf Pro       │         │
│         │   VMware Workspace ONE              │         │
│         └──────────────────┬──────────────────┘         │
└────────────────────────────┼────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
│  Windows域     │   │   Mac域        │   │  Linux域       │
│  BitLocker    │   │  FileVault     │   │  LUKS          │
│  + SCCM       │   │  + Jamf        │   │  + Puppet      │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   密钥托管服务器 │
                    │   (AD/ESCROW)   │
                    └─────────────────┘
```

## Microsoft Intune + BitLocker

### 配置策略
```powershell
# Intune BitLocker配置策略
$BitLockerPolicy = @{
    '@odata.type' = '#microsoft.graph.bitLockerConfiguration'
    
    # 加密设置
    encryptionMethod = 'aes256'
    
    # 恢复密钥设置
    recoveryKeyRotation = 'enabled'
    recoveryKeyEscrowToAzureAD = $true
    
    # 系统驱动器设置
    systemDrivePolicy = @{
        encryptionMethod = 'aes256'
        recoveryOptions = @{
            recoveryKeyPath = 'AzureAD'
            hideRecoveryOptions = $false
            enableRecoveryPasswordRotation = $true
        }
        minimumDiskSpace = '64GB'
    }
    
    # 固定数据驱动器
    fixedDrivePolicy = @{
        encryptionMethod = 'aes256'
        requireEncryptionForWriteAccess = $true
    }
    
    # 可移动驱动器
    removableDrivePolicy = @{
        requireEncryptionForWriteAccess = $true
        blockCrossOrganizationWriteAccess = $true
    }
}

# 部署策略
New-IntuneDeviceConfigurationPolicy `
    -Name "Corporate BitLocker Policy" `
    -BitLockerConfiguration $BitLockerPolicy
```

### 合规性检查
```powershell
# 检查加密状态
Get-BitLockerVolume | Select-Object `
    MountPoint, `
    EncryptionMethod, `
    ProtectionStatus, `
    KeyProtector

# 导出报告
Get-IntuneManagedDevice | Where-Object { 
    $_.operatingSystem -eq 'Windows' 
} | ForEach-Object {
    Get-IntuneDeviceComplianceState -DeviceId $_.id
}
```

## Jamf Pro + FileVault

### 配置文件
```xml
<!-- FileVault Configuration Profile -->
<dict>
    <key>PayloadType</key>
    <string>com.apple.security.FDERecoveryKeyEscrow</string>
    
    <key>PayloadIdentifier</key>
    <string>com.company.filvault.escrow</string>
    
    <key>PayloadUUID</key>
    <string>550e8400-e29b-41d4-a716-446655440000</string>
    
    <key>PayloadVersion</key>
    <integer>1</integer>
    
    <key>PayloadDisplayName</key>
    <string>FileVault 2 Configuration</string>
    
    <!-- 启用FileVault -->
    <key>EnableFileVault</key>
    <true/>
    
    <!-- 个人恢复密钥 -->
    <key>OutputPath</key>
    <string>/var/db/FileVaultPRK.dat</string>
    
    <!-- 托管到Jamf -->
    <key>EscrowToServer</key>
    <true/>
    
    <!-- 首次登录时启用 -->
    <key>Defer</key>
    <true/>
    <key>DeferForceAtUserLoginMaxBypassAttempts</key>
    <integer>3</integer>
</dict>
```

### 扩展属性收集
```bash
#!/bin/bash
# Jamf Extension Attribute: FileVault Status

FV_STATUS=$(fdesetup status)

if [[ $FV_STATUS == "FileVault is On." ]]; then
    echo "<result>Enabled</result>"
else
    echo "<result>Disabled</result>"
fi
```

## 自动化部署流程

```yaml
# Ansible Playbook: 企业FDE部署
- name: Deploy Full Disk Encryption
  hosts: all
  vars:
    encryption_method: "{{ os_encryption_method }}"
    
  tasks:
    - name: Deploy Windows BitLocker
      when: ansible_os_family == "Windows"
      block:
        - name: Check TPM availability
          win_shell: |
            Get-Tpm | Select-Object TpmPresent,TpmReady
          
        - name: Enable BitLocker
          win_bitlocker:
            mount_path: C:
            encryption_method: aes256
            recovery_key_destination: azure_ad
            
        - name: Escrow recovery key
          win_shell: |
            Manage-Bde -Protectors -Add C: -RecoveryPassword
    
    - name: Deploy Linux LUKS
      when: ansible_os_family == "RedHat" or ansible_os_family == "Debian"
      block:
        - name: Install cryptsetup
          package:
            name: cryptsetup
            state: present
            
        - name: Configure LUKS
          command: |
            cryptsetup luksFormat 
              --type luks2 
              --cipher aes-xts-plain64 
              --key-size 512 
              /dev/sda2
          
        - name: Setup automatic unlock
          template:
            src: crypttab.j2
            dest: /etc/crypttab
```

## 报告与监控

```python
# 企业加密状态报告
import json
from datetime import datetime

class EncryptionReport:
    def __init__(self):
        self.report_date = datetime.now()
        self.devices = []
    
    def add_device(self, device_info):
        self.devices.append({
            'hostname': device_info['hostname'],
            'os': device_info['os'],
            'encryption_status': device_info['status'],
            'last_check': device_info['last_check'],
            'recovery_key_escrowed': device_info['key_escrowed']
        })
    
    def generate_compliance_report(self):
        total = len(self.devices)
        encrypted = sum(1 for d in self.devices if d['encryption_status'] == 'encrypted')
        
        return {
            'report_date': self.report_date.isoformat(),
            'summary': {
                'total_devices': total,
                'encrypted_devices': encrypted,
                'compliance_rate': (encrypted / total) * 100 if total > 0 else 0
            },
            'details': self.devices
        }

# 生成报告
report = EncryptionReport()
# ... 添加设备数据
compliance_data = report.generate_compliance_report()
print(json.dumps(compliance_data, indent=2))
```

## 学习要点

1. MDM/SCCM集成方案
2. 自动化配置策略
3. 合规性检查与报告
4. 大规模部署最佳实践
5. 跨平台统一管理
