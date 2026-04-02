# AD/LDAP Integration

FDE与Active Directory/LDAP集成方案演示。

## 集成架构

```
AD集成架构:
┌─────────────────────────────────────────────────────────┐
│              Active Directory Domain                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │  • 计算机账户                                      │   │
│  │  • 组策略 (GPO)                                   │   │
│  │  • 恢复密钥存储 (MS-TPM-Owner-Information)         │   │
│  │  • 访问控制 (ACL)                                 │   │
│  └─────────────────────────────────────────────────┘   │
├────────────────────────┬────────────────────────────────┤
│                        │                                │
┌────────────────────────▼────────────────────────────────┐
│                    客户端设备                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  BitLocker  │  │ 组策略应用   │  │ 域身份验证   │     │
│  │  密钥托管    │  │  (GPO)     │  │  (Kerberos) │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## BitLocker与AD集成

### 配置AD密钥存储
```powershell
# 1. 扩展AD架构 (一次性)
# 复制BitLocker AD扩展文件到域控制器
Copy-Item "C:\Windows\System32\SecureBootAd\*.ldf" "C:\ADExtensions"

# 执行架构扩展
cd "C:\ADExtensions"
ldifde -i -f BitLocker-AD-Schema.ldf -c "CN=Schema,CN=Configuration,DC=X" # SchemaNamingContext

# 2. 配置域控制器存储恢复密钥
# 创建组策略
$GPO = New-GPO -Name "BitLocker Key Storage"

# 配置计算机配置 > 策略 > 管理模板 > Windows组件 > BitLocker驱动器加密
Set-GPRegistryValue `
    -Name $GPO.DisplayName `
    -Key "HKLM\SOFTWARE\Policies\Microsoft\Windows\BitLocker" `
    -ValueName "OSRecoveryKey" `
    -Type DWord `
    -Value 1  # 备份恢复密码到AD

Set-GPRegistryValue `
    -Name $GPO.DisplayName `
    -Key "HKLM\SOFTWARE\Policies\Microsoft\Windows\BitLocker" `
    -ValueName "OSRecoveryPackage" `
    -Type DWord `
    -Value 1  # 备份恢复包到AD

# 链接GPO到OU
New-GPLink -Name $GPO.DisplayName -Target "OU=Workstations,DC=company,DC=com"
```

### 检索AD中的恢复密钥
```powershell
# 从Active Directory检索BitLocker恢复密钥
function Get-BitLockerRecoveryKeyFromAD {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ComputerName
    )
    
    # 导入Active Directory模块
    Import-Module ActiveDirectory
    
    # 获取计算机对象
    $Computer = Get-ADComputer -Identity $ComputerName -Properties msTPM-OwnerInformation, msFVE-RecoveryPassword
    
    # 获取恢复密钥
    $RecoveryKeys = $Computer | Select-Object -ExpandProperty msFVE-RecoveryPassword
    
    if ($RecoveryKeys) {
        Write-Host "Found recovery keys for $ComputerName:" -ForegroundColor Green
        $RecoveryKeys | ForEach-Object { Write-Host $_ }
    } else {
        Write-Warning "No recovery keys found for $ComputerName"
    }
    
    return $RecoveryKeys
}

# 使用
Get-BitLockerRecoveryKeyFromAD -ComputerName "WORKSTATION01"
```

## LDAP集成脚本

```python
#!/usr/bin/env python3
"""
FDE与LDAP/AD集成工具
"""
from ldap3 import Server, Connection, ALL, SUBTREE
import json
from dataclasses import dataclass

@dataclass
class BitLockerKeyInfo:
    computer_name: str
    recovery_key: str
    timestamp: str
    volume_guid: str

class ADKeyManager:
    def __init__(self, server_url: str, username: str, password: str):
        self.server = Server(server_url, get_info=ALL)
        self.conn = Connection(
            self.server,
            user=username,
            password=password,
            auto_bind=True
        )
    
    def store_recovery_key(self, computer_dn: str, recovery_key: str, 
                          volume_guid: str) -> bool:
        """
        存储恢复密钥到AD
        
        LDAP属性:
        - msFVE-RecoveryPassword: 恢复密码
        - msFVE-RecoveryGuid: 卷GUID
        - msFVE-VolumeGuid: 卷GUID
        """
        try:
            # 添加恢复密钥到计算机对象
            self.conn.modify(computer_dn, {
                'msFVE-RecoveryPassword': [(1, [recovery_key])],  # 1 = ADD
                'msFVE-RecoveryGuid': [(1, [volume_guid])]
            })
            
            return self.conn.result['result'] == 0
        except Exception as e:
            print(f"Failed to store key: {e}")
            return False
    
    def retrieve_recovery_key(self, computer_name: str) -> list:
        """从AD检索恢复密钥"""
        search_base = "DC=company,DC=com"
        search_filter = f"(&(objectClass=computer)(cn={computer_name}))"
        
        attributes = [
            'cn',
            'msFVE-RecoveryPassword',
            'msFVE-RecoveryGuid',
            'whenChanged'
        ]
        
        self.conn.search(
            search_base=search_base,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=attributes
        )
        
        results = []
        for entry in self.conn.entries:
            keys = entry.msFVE_RecoveryPassword.values if hasattr(entry, 'msFVE_RecoveryPassword') else []
            for key in keys:
                results.append(BitLockerKeyInfo(
                    computer_name=entry.cn.value,
                    recovery_key=key,
                    timestamp=entry.whenChanged.value if hasattr(entry, 'whenChanged') else '',
                    volume_guid=entry.msFVE_RecoveryGuid.value if hasattr(entry, 'msFVE_RecoveryGuid') else ''
                ))
        
        return results
    
    def find_computer_by_key(self, recovery_key: str) -> str:
        """通过恢复密钥查找计算机"""
        search_base = "DC=company,DC=com"
        search_filter = f"(&(objectClass=computer)(msFVE-RecoveryPassword={recovery_key}))"
        
        self.conn.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=['cn', 'distinguishedName']
        )
        
        if self.conn.entries:
            return self.conn.entries[0].cn.value
        return None
    
    def audit_key_access(self, computer_name: str, admin_username: str):
        """审计密钥访问"""
        # 在实际实现中，应该记录到审计系统
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'computer': computer_name,
            'admin': admin_username,
            'action': 'key_retrieval'
        }
        
        # 这里可以写入到审计日志或SIEM系统
        print(f"AUDIT: {json.dumps(audit_entry)}")

# 使用示例
if __name__ == "__main__":
    manager = ADKeyManager(
        server_url="ldap://dc.company.com",
        username="admin@company.com",
        password="password"
    )
    
    # 检索密钥
    keys = manager.retrieve_recovery_key("WORKSTATION01")
    for key in keys:
        print(f"Key: {key.recovery_key}")
        print(f"Volume: {key.volume_guid}")
```

## 组策略配置

```xml
<!-- BitLocker GPO XML配置 -->
<ComputerConfig>
  <Policies>
    <WindowsComponents>
      <BitLockerDriveEncryption>
        <!-- 启用BitLocker -->
        <OperatingSystemDrives>
          <Enable>
            <Type>Enabled</Type>
            <Settings>
              <ChooseDriveEncryptionMethod>
                <Type>Enabled</Type>
                <Value>AES 256-bit</Value>
              </ChooseDriveEncryptionMethod>
              
              <!-- 配置恢复密钥 -->
              <ConfigureRecoveryPassword>
                <Type>Enabled</Type>
                <Options>48-digit recovery password</Options>
              </ConfigureRecoveryPassword>
              
              <!-- 存储到AD DS -->
              <StoreRecoveryInformationInAD>
                <Type>Enabled</Type>
                <Options>Backup recovery passwords and key packages</Options>
              </StoreRecoveryInformationInAD>
            </Settings>
          </Enable>
        </OperatingSystemDrives>
      </BitLockerDriveEncryption>
    </WindowsComponents>
  </Policies>
</ComputerConfig>
```

## 学习要点

1. AD架构扩展
2. BitLocker密钥存储
3. LDAP查询和修改
4. 组策略配置
5. 审计和合规
