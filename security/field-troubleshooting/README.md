# Field Troubleshooting

FDE现场故障诊断与排除指南。

## 常见故障场景

```
故障诊断流程:
┌─────────────────────────────────────────────────────────┐
│ 1. 问题识别                                              │
│    ├── 用户报告问题                                       │
│    ├── 系统自动告警                                       │
│    └── 部署后验证失败                                     │
├─────────────────────────────────────────────────────────┤
│ 2. 信息收集                                              │
│    ├── 查看错误日志                                       │
│    ├── 收集系统信息                                       │
│    └── 复现问题步骤                                       │
├─────────────────────────────────────────────────────────┤
│ 3. 根因分析                                              │
│    ├── 硬件问题 (TPM/磁盘)                                │
│    ├── 软件问题 (驱动/配置)                               │
│    └── 用户操作问题                                       │
├─────────────────────────────────────────────────────────┤
│ 4. 问题解决                                              │
│    ├── 应用修复方案                                       │
│    ├── 验证修复结果                                       │
│    └── 记录解决方案                                       │
└─────────────────────────────────────────────────────────┘
```

## 故障诊断工具

```python
#!/usr/bin/env python3
"""
FDE现场故障诊断工具
"""
import subprocess
import json
import os
import sys
from datetime import datetime
from typing import Dict, List

class FDEFieldTroubleshooter:
    def __init__(self):
        self.findings = []
        self.system_info = {}
        
    def run_diagnostics(self) -> Dict:
        """运行完整诊断"""
        print("=== FDE Field Diagnostics ===\n")
        
        # 系统信息
        self.collect_system_info()
        
        # 加密状态诊断
        self.diagnose_encryption_status()
        
        # TPM诊断
        self.diagnose_tpm()
        
        # 磁盘诊断
        self.diagnose_disk()
        
        # 引导诊断
        self.diagnose_boot()
        
        return self.generate_diagnostic_report()
    
    def collect_system_info(self):
        """收集系统信息"""
        import platform
        self.system_info = {
            'os': platform.system(),
            'version': platform.version(),
            'architecture': platform.machine(),
            'time': datetime.now().isoformat()
        }
    
    def diagnose_encryption_status(self):
        """诊断加密状态"""
        print("[+] Checking encryption status...")
        
        if sys.platform == 'win32':
            self._diagnose_windows_encryption()
        elif sys.platform == 'linux':
            self._diagnose_linux_encryption()
    
    def _diagnose_windows_encryption(self):
        """Windows加密诊断"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', 
                 'Get-BitLockerVolume | Select-Object MountPoint,VolumeStatus,ProtectionStatus,EncryptionPercentage | ConvertTo-Json'],
                capture_output=True, text=True
            )
            
            volumes = json.loads(result.stdout)
            if not isinstance(volumes, list):
                volumes = [volumes]
            
            for vol in volumes:
                mount = vol.get('MountPoint')
                status = vol.get('ProtectionStatus')
                percent = vol.get('EncryptionPercentage', 0)
                
                if status == 0:
                    self.add_finding('WARNING', f'Volume {mount} is not encrypted',
                                   'Run Enable-BitLocker to encrypt')
                elif percent < 100:
                    self.add_finding('INFO', f'Volume {mount} encryption in progress: {percent}%',
                                   'Wait for completion or check performance')
                else:
                    self.add_finding('OK', f'Volume {mount} is fully encrypted')
                    
        except Exception as e:
            self.add_finding('ERROR', f'Failed to check encryption: {e}')
    
    def _diagnose_linux_encryption(self):
        """Linux加密诊断"""
        try:
            # 检查LUKS容器
            result = subprocess.run(['lsblk', '-f', '-J'], capture_output=True, text=True)
            block_info = json.loads(result.stdout)
            
            luks_devices = []
            for device in block_info.get('blockdevices', []):
                if device.get('fstype') == 'crypto_LUKS':
                    luks_devices.append(device)
            
            if luks_devices:
                for dev in luks_devices:
                    self.add_finding('OK', f"LUKS container found: {dev['name']}")
                    
                    # 检查是否已打开
                    mapper_name = f"luks-{dev['name']}"
                    if os.path.exists(f'/dev/mapper/{mapper_name}'):
                        self.add_finding('OK', f'  -> Mapper {mapper_name} is active')
                    else:
                        self.add_finding('WARNING', f'  -> Mapper {mapper_name} not active',
                                       f'Run: cryptsetup luksOpen /dev/{dev["name"]} {mapper_name}')
            else:
                self.add_finding('WARNING', 'No LUKS encryption found')
                
        except Exception as e:
            self.add_finding('ERROR', f'Failed to check LUKS: {e}')
    
    def diagnose_tpm(self):
        """TPM诊断"""
        print("[+] Checking TPM status...")
        
        if sys.platform == 'win32':
            try:
                result = subprocess.run(
                    ['powershell', '-Command', 'Get-Tpm | ConvertTo-Json'],
                    capture_output=True, text=True
                )
                tpm = json.loads(result.stdout)
                
                if tpm.get('TpmPresent'):
                    if tpm.get('TpmReady'):
                        self.add_finding('OK', 'TPM 2.0 is present and ready')
                    else:
                        self.add_finding('WARNING', 'TPM is present but not ready',
                                       'Check BIOS settings')
                else:
                    self.add_finding('ERROR', 'TPM not found',
                                   'Verify hardware supports TPM 2.0')
                    
            except Exception as e:
                self.add_finding('ERROR', f'TPM check failed: {e}')
    
    def diagnose_disk(self):
        """磁盘诊断"""
        print("[+] Checking disk health...")
        
        try:
            import psutil
            disk_info = psutil.disk_usage('/')
            
            if disk_info.percent > 90:
                self.add_finding('WARNING', f'Disk usage critical: {disk_info.percent}%',
                               'Free up space before encryption')
            elif disk_info.percent > 80:
                self.add_finding('WARNING', f'Disk usage high: {disk_info.percent}%',
                               'Consider cleaning up space')
            else:
                self.add_finding('OK', f'Disk usage normal: {disk_info.percent}%')
                
        except:
            pass
    
    def diagnose_boot(self):
        """引导诊断"""
        print("[+] Checking boot configuration...")
        
        if sys.platform == 'linux':
            # 检查initramfs
            if os.path.exists('/etc/crypttab'):
                with open('/etc/crypttab') as f:
                    content = f.read()
                    if content.strip():
                        self.add_finding('OK', 'crypttab configured')
                    else:
                        self.add_finding('WARNING', 'crypttab is empty')
    
    def add_finding(self, severity: str, message: str, recommendation: str = None):
        """添加诊断发现"""
        self.findings.append({
            'severity': severity,
            'message': message,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat()
        })
        
        icon = {'OK': '✓', 'INFO': 'ℹ', 'WARNING': '⚠', 'ERROR': '✗'}.get(severity, '?')
        print(f"  {icon} {message}")
        if recommendation:
            print(f"    → {recommendation}")
    
    def generate_diagnostic_report(self) -> Dict:
        """生成诊断报告"""
        report = {
            'diagnostic_time': datetime.now().isoformat(),
            'system_info': self.system_info,
            'findings': self.findings,
            'summary': {
                'total': len(self.findings),
                'ok': sum(1 for f in self.findings if f['severity'] == 'OK'),
                'warnings': sum(1 for f in self.findings if f['severity'] == 'WARNING'),
                'errors': sum(1 for f in self.findings if f['severity'] == 'ERROR')
            }
        }
        
        # 保存报告
        filename = f'fde_diagnostic_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[+] Diagnostic report saved: {filename}")
        return report

# 使用
if __name__ == "__main__":
    troubleshooter = FDEFieldTroubleshooter()
    report = troubleshooter.run_diagnostics()
    
    print("\n=== Summary ===")
    print(f"Total checks: {report['summary']['total']}")
    print(f"OK: {report['summary']['ok']}")
    print(f"Warnings: {report['summary']['warnings']}")
    print(f"Errors: {report['summary']['errors']}")
```

## 常见问题解决方案

### 问题1: TPM未就绪
```powershell
# 解决方案
# 1. 检查BIOS设置
Get-Tpm | Select-Object TpmPresent,TpmReady

# 2. 清除TPM (谨慎!)
Initialize-Tpm -AllowClear

# 3. 重启后重新配置
Enable-BitLocker -MountPoint C: -RecoveryPasswordProtector
```

### 问题2: 加密进度卡住
```bash
# Linux LUKS检查
# 1. 检查磁盘活动
iostat -x 1

# 2. 检查加密状态
cryptsetup status luks-device

# 3. 如需要，调整优先级
ionice -c 2 -n 0 cryptsetup luksOpen /dev/sda2 data
```

### 问题3: 无法引导
```bash
# 使用Live CD修复
# 1. 从Live USB启动
# 2. 打开LUKS
cryptsetup luksOpen /dev/sda2 chroot

# 3. 挂载并chroot
mount /dev/mapper/chroot /mnt
mount /dev/sda1 /mnt/boot
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys
chroot /mnt

# 4. 重新安装引导
grub-install /dev/sda
update-grub
```

## 学习要点

1. 系统化的故障诊断流程
2. 自动化诊断工具开发
3. 常见问题的快速解决
4. 紧急恢复技术
5. 现场问题处理最佳实践
