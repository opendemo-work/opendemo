# Recovery Key Escrow

恢复密钥托管与恢复方案演示。

## 密钥托管架构

```
密钥托管系统架构:
┌─────────────────────────────────────────────────────────┐
│                    客户端设备                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  BitLocker  │  │  FileVault  │  │    LUKS     │     │
│  │ RecoveryKey │  │     PRK     │  │   Keyfile   │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
└─────────┼────────────────┼────────────────┼─────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │ HTTPS/TLS
┌──────────────────────────▼──────────────────────────────┐
│                 密钥托管服务器                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │           密钥存储 (加密数据库)                    │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │   │
│  │  │DeviceID │ │Encrypted│ │Escrow   │          │   │
│  │  │         │ │Key      │ │Date     │          │   │
│  │  └─────────┘ └─────────┘ └─────────┘          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │          访问控制 (RBAC)                         │   │
│  │  • 管理员审批流程                                │   │
│  │  • 审计日志                                      │   │
│  │  • 多因素认证                                    │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Azure AD密钥托管

### 配置BitLocker密钥托管
```powershell
# 注册表配置：启用Azure AD密钥托管
$RegistryPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\BitLocker\OperatingSystemDrives"

# 启用恢复密钥备份到Azure AD
New-ItemProperty -Path $RegistryPath -Name "OSRecoveryKey" -Value 1 -PropertyType DWord -Force

# 启用恢复密码备份到Azure AD
New-ItemProperty -Path $RegistryPath -Name "OSRecoveryPassword" -Value 1 -PropertyType DWord -Force

# 配置恢复密钥存储
Manage-Bde -Protectors -Add C: -RecoveryPassword

# 验证密钥已托管
$BLV = Get-BitLockerVolume -MountPoint C:
$BLV.KeyProtector | Where-Object {$_.KeyProtectorType -eq 'RecoveryPassword'}
```

### 检索托管密钥
```powershell
# Graph API查询托管密钥
$TenantId = "your-tenant-id"
$ClientId = "your-client-id"
$ClientSecret = "your-client-secret"

# 获取访问令牌
$TokenUrl = "https://login.microsoftonline.com/$TenantId/oauth2/v2.0/token"
$Body = @{
    grant_type = "client_credentials"
    client_id = $ClientId
    client_secret = $ClientSecret
    scope = "https://graph.microsoft.com/.default"
}

$TokenResponse = Invoke-RestMethod -Uri $TokenUrl -Method Post -Body $Body
$AccessToken = $TokenResponse.access_token

# 查询设备BitLocker密钥
$DeviceId = "target-device-id"
$Uri = "https://graph.microsoft.com/v1.0/informationProtection/bitlocker/recoveryKeys?`$filter=deviceId eq '$DeviceId'"

$Headers = @{
    Authorization = "Bearer $AccessToken"
}

$RecoveryKeys = Invoke-RestMethod -Uri $Uri -Headers $Headers -Method Get
$RecoveryKeys.value
```

## 自建密钥托管服务

### Python实现
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import sqlite3
import hashlib
import secrets

class KeyEscrowService:
    def __init__(self, master_key: bytes):
        """
        初始化密钥托管服务
        master_key: 用于加密存储的主密钥
        """
        self.cipher = Fernet(base64.urlsafe_b64encode(master_key))
        self.init_database()
    
    def init_database(self):
        """初始化加密密钥数据库"""
        conn = sqlite3.connect('escrow_keys.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recovery_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT UNIQUE NOT NULL,
                device_name TEXT NOT NULL,
                user_email TEXT NOT NULL,
                encrypted_key BLOB NOT NULL,
                key_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accessed_at TIMESTAMP,
                access_count INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    
    def escrow_key(self, device_id: str, device_name: str, 
                   user_email: str, recovery_key: str, key_type: str) -> bool:
        """
        托管恢复密钥
        """
        try:
            # 加密密钥
            encrypted_key = self.cipher.encrypt(recovery_key.encode())
            
            # 存储到数据库
            conn = sqlite3.connect('escrow_keys.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recovery_keys 
                (device_id, device_name, user_email, encrypted_key, key_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (device_id, device_name, user_email, encrypted_key, key_type))
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Escrow failed: {e}")
            return False
    
    def retrieve_key(self, device_id: str, admin_id: str, 
                     reason: str) -> dict:
        """
        检索恢复密钥 (带审计)
        """
        conn = sqlite3.connect('escrow_keys.db')
        cursor = conn.cursor()
        
        # 获取加密密钥
        cursor.execute('''
            SELECT encrypted_key, key_type, user_email 
            FROM recovery_keys WHERE device_id = ?
        ''', (device_id,))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return None
        
        encrypted_key, key_type, user_email = result
        
        # 解密密钥
        recovery_key = self.cipher.decrypt(encrypted_key).decode()
        
        # 更新访问审计
        cursor.execute('''
            UPDATE recovery_keys 
            SET accessed_at = CURRENT_TIMESTAMP,
                access_count = access_count + 1
            WHERE device_id = ?
        ''', (device_id,))
        
        # 记录审计日志
        cursor.execute('''
            INSERT INTO audit_logs 
            (device_id, admin_id, access_reason, access_time)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (device_id, admin_id, reason))
        
        conn.commit()
        conn.close()
        
        return {
            'device_id': device_id,
            'recovery_key': recovery_key,
            'key_type': key_type,
            'user_email': user_email,
            'accessed_by': admin_id
        }

# 使用示例
if __name__ == "__main__":
    # 生成主密钥 (实际应安全存储)
    master_key = Fernet.generate_key()[:32]
    
    service = KeyEscrowService(master_key)
    
    # 托管密钥
    service.escrow_key(
        device_id="WIN-2024-001",
        device_name="Laptop-IT-01",
        user_email="user@company.com",
        recovery_key="123456-789012-345678-901234-567890-123456-789012-345678",
        key_type="BitLocker"
    )
    
    # 检索密钥
    key_data = service.retrieve_key(
        device_id="WIN-2024-001",
        admin_id="admin@company.com",
        reason="User forgot password, request #12345"
    )
    print(key_data)
```

## 密钥恢复流程

```
标准恢复流程:
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ 用户请求 │────▶│ 身份验证 │────▶│ 管理员  │────▶│ 密钥检索 │
│ 恢复密钥 │     │ (MFA)   │     │ 审批    │     │ 与交付  │
└─────────┘     └─────────┘     └─────────┘     └────┬────┘
                                                     │
                                              ┌──────┴──────┐
                                              │  审计记录    │
                                              │  • 时间戳    │
                                              │  • 操作人    │
                                              │  • 原因      │
                                              └─────────────┘
```

## 学习要点

1. 密钥加密存储方案
2. 访问控制与审计
3. Azure AD集成
4. 自建托管服务
5. 合规性要求
