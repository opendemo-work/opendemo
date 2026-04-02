# FDE Disaster Recovery

全盘加密环境灾难恢复方案演示。

## 灾难场景分析

```
灾难恢复场景:
┌─────────────────────────────────────────────────────────┐
│ 场景1: 密钥丢失                                          │
│ ├── 用户忘记密码                                          │
│ ├── 恢复密钥丢失                                          │
│ └── 密钥托管系统故障                                       │
├─────────────────────────────────────────────────────────┤
│ 场景2: 硬件故障                                          │
│ ├── TPM芯片损坏                                           │
│ ├── 主板故障导致TPM不可用                                  │
│ └── 硬盘控制器故障                                         │
├─────────────────────────────────────────────────────────┤
│ 场景3: 系统损坏                                          │
│ ├── 引导加载器损坏                                        │
│ ├── 内核更新失败                                          │
│ └── 文件系统损坏                                          │
├─────────────────────────────────────────────────────────┤
│ 场景4: 数据中心灾难                                      │
│ ├── 站点完全丢失                                          │
│ ├── 备份介质损坏                                          │
│ └── 密钥托管服务器不可用                                   │
└─────────────────────────────────────────────────────────┘
```

## 灾难恢复预案

### 1. 密钥备份策略

```bash
#!/bin/bash
# 自动化密钥备份脚本

BACKUP_DIR="/secure/backup/luks"
DATE=$(date +%Y%m%d)

# 创建加密备份容器
setup_backup_container() {
    local backup_device="/dev/sdb1"
    
    # 创建LUKS容器用于备份存储
    cryptsetup luksFormat --type luks2 $backup_device
    cryptsetup luksOpen $backup_device backup_storage
    
    # 创建文件系统
    mkfs.ext4 /dev/mapper/backup_storage
    mkdir -p $BACKUP_DIR
    mount /dev/mapper/backup_storage $BACKUP_DIR
}

# 备份LUKS头
backup_luks_headers() {
    local device=$1
    local hostname=$(hostname)
    
    cryptsetup luksHeaderBackup $device \
        --header-backup-file "$BACKUP_DIR/${hostname}_$(basename $device)_header_${DATE}.img"
    
    # 计算校验和
    sha256sum "$BACKUP_DIR/${hostname}_$(basename $device)_header_${DATE}.img" \
        > "$BACKUP_DIR/${hostname}_$(basename $device)_header_${DATE}.sha256"
}

# 备份恢复密钥
backup_recovery_keys() {
    local key_file=$1
    local hostname=$(hostname)
    
    # 使用GPG加密备份
    gpg --symmetric --cipher-algo AES256 \
        --output "$BACKUP_DIR/${hostname}_recovery_key_${DATE}.gpg" \
        $key_file
}

# 主备份流程
main() {
    # 备份所有加密设备
    for device in /dev/sda2 /dev/sdb2; do
        if cryptsetup isLuks $device 2>/dev/null; then
            backup_luks_headers $device
        fi
    done
    
    # 同步到远程位置
    rsync -avz --delete $BACKUP_DIR/ remote-server:/backups/luks/
}

main
```

### 2. 紧急恢复流程

```bash
#!/bin/bash
# 紧急恢复脚本

RECOVERY_LOG="/var/log/fde_recovery.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $RECOVERY_LOG
}

# 场景1: LUKS头损坏恢复
recover_luks_header() {
    local device=$1
    local backup_file=$2
    
    log "Starting LUKS header recovery for $device"
    
    # 验证备份文件
    if [ ! -f "$backup_file" ]; then
        log "ERROR: Backup file not found: $backup_file"
        return 1
    fi
    
    # 验证校验和
    if ! sha256sum -c "${backup_file}.sha256"; then
        log "ERROR: Backup file checksum failed"
        return 1
    fi
    
    # 恢复头部
    cryptsetup luksHeaderRestore $device --header-backup-file $backup_file
    
    if [ $? -eq 0 ]; then
        log "SUCCESS: LUKS header restored for $device"
        return 0
    else
        log "ERROR: Failed to restore LUKS header"
        return 1
    fi
}

# 场景2: 使用备份密钥解锁
unlock_with_backup_key() {
    local device=$1
    local backup_key_file=$2
    
    log "Attempting to unlock $device with backup key"
    
    # 解密备份密钥
    local decrypted_key=$(gpg --decrypt $backup_key_file 2>/dev/null)
    
    if [ -z "$decrypted_key" ]; then
        log "ERROR: Failed to decrypt backup key"
        return 1
    fi
    
    # 尝试解锁
    echo "$decrypted_key" | cryptsetup luksOpen $device recovered_data -
    
    if [ $? -eq 0 ]; then
        log "SUCCESS: Device unlocked with backup key"
        return 0
    else
        log "ERROR: Failed to unlock with backup key"
        return 1
    fi
}

# 场景3: 数据恢复 (无头部)
recover_data_without_header() {
    local device=$1
    local original_cipher="aes-xts-plain64"
    local original_offset=4096  # 假设标准偏移
    
    log "ATTEMPTING EMERGENCY DATA RECOVERY"
    log "This requires knowing the original encryption parameters"
    
    # 尝试使用已知参数打开
    cryptsetup open --type plain \
        --cipher $original_cipher \
        --offset $original_offset \
        --key-file /recovery/master-key \
        $device emergency_recovery
    
    return $?
}
```

## 灾难恢复测试

```python
#!/usr/bin/env python3
"""
FDE灾难恢复测试框架
"""
import subprocess
import json
import tempfile
import os
from datetime import datetime

class FDERecoveryTest:
    def __init__(self):
        self.test_results = []
        self.test_container = None
    
    def setup_test_environment(self):
        """创建测试环境"""
        # 创建测试文件
        self.test_container = tempfile.NamedTemporaryFile(delete=False, suffix='.img')
        
        # 创建100MB测试容器
        subprocess.run(['dd', 'if=/dev/zero', f'of={self.test_container.name}', 
                      'bs=1M', 'count=100'], check=True)
        
        # 设置LUKS
        subprocess.run(['cryptsetup', 'luksFormat', '--type', 'luks2',
                      '-q', self.test_container.name], 
                      input='testpassword123', text=True, check=True)
        
        return self.test_container.name
    
    def test_header_backup_restore(self):
        """测试头部备份恢复"""
        print("Testing: Header Backup and Restore")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.header') as backup:
            # 备份头部
            subprocess.run(['cryptsetup', 'luksHeaderBackup',
                          self.test_container.name,
                          '--header-backup-file', backup.name], check=True)
            
            # 模拟损坏 (创建新LUKS)
            subprocess.run(['cryptsetup', 'luksFormat', '--type', 'luks2',
                          '-q', self.test_container.name],
                          input='newpassword456', text=True, check=True)
            
            # 恢复头部
            result = subprocess.run(['cryptsetup', 'luksHeaderRestore',
                                   self.test_container.name,
                                   '--header-backup-file', backup.name],
                                   input='YES', text=True, capture_output=True)
            
            success = result.returncode == 0
            
            # 验证可以解锁
            if success:
                unlock = subprocess.run(['cryptsetup', 'luksOpen', '-q',
                                       self.test_container.name, 'test_recovery',
                                       '-'], input='testpassword123',
                                       text=True, capture_output=True)
                success = unlock.returncode == 0
                
                if success:
                    subprocess.run(['cryptsetup', 'luksClose', 'test_recovery'])
            
            self.test_results.append({
                'test': 'header_backup_restore',
                'success': success,
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"  Result: {'PASS' if success else 'FAIL'}")
            return success
    
    def test_key_slot_management(self):
        """测试密钥槽管理"""
        print("Testing: Key Slot Management")
        
        # 添加备用密钥
        result1 = subprocess.run(['cryptsetup', 'luksAddKey', '-q',
                                self.test_container.name],
                                input='testpassword123\nbackuppassword456',
                                text=True, capture_output=True)
        
        # 删除主密钥
        result2 = subprocess.run(['cryptsetup', 'luksKillSlot', '-q',
                                self.test_container.name, '0'],
                                input='backuppassword456',
                                text=True, capture_output=True)
        
        # 验证备用密钥仍可解锁
        result3 = subprocess.run(['cryptsetup', 'luksOpen', '-q',
                                self.test_container.name, 'test_slot',
                                '-'], input='backuppassword456',
                                text=True, capture_output=True)
        
        success = result1.returncode == 0 and result2.returncode == 0 and result3.returncode == 0
        
        if success:
            subprocess.run(['cryptsetup', 'luksClose', 'test_slot'])
        
        self.test_results.append({
            'test': 'key_slot_management',
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"  Result: {'PASS' if success else 'FAIL'}")
        return success
    
    def generate_report(self):
        """生成测试报告"""
        passed = sum(1 for r in self.test_results if r['success'])
        total = len(self.test_results)
        
        report = {
            'test_date': datetime.now().isoformat(),
            'summary': {
                'total_tests': total,
                'passed': passed,
                'failed': total - passed,
                'success_rate': (passed / total * 100) if total > 0 else 0
            },
            'details': self.test_results
        }
        
        with open('fde_recovery_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n=== Test Summary ===")
        print(f"Total: {total}, Passed: {passed}, Failed: {total - passed}")
        print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
        
        return report
    
    def cleanup(self):
        """清理测试环境"""
        if self.test_container and os.path.exists(self.test_container.name):
            os.unlink(self.test_container.name)

# 运行测试
if __name__ == "__main__":
    test = FDERecoveryTest()
    try:
        test.setup_test_environment()
        test.test_header_backup_restore()
        test.test_key_slot_management()
        test.generate_report()
    finally:
        test.cleanup()
```

## 业务连续性计划

```
RTO/RPO目标:
┌─────────────────────────────────────────────────────────┐
│ 场景              │ RTO     │ RPO     │ 恢复策略        │
├─────────────────────────────────────────────────────────┤
│ 单设备密钥丢失    │ 1小时   │ 0       │ 恢复密钥托管    │
│ TPM故障          │ 4小时   │ 0       │ 备用解锁方式    │
│ LUKS头损坏       │ 2小时   │ 0       │ 头部备份恢复    │
│ 数据中心灾难     │ 24小时  │ 1小时   │ 异地备份恢复    │
└─────────────────────────────────────────────────────────┘
```

## 学习要点

1. 灾难场景分类与应对
2. 密钥备份策略
3. 紧急恢复流程
4. 灾难恢复测试
5. 业务连续性规划
