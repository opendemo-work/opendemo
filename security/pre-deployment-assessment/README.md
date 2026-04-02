# Pre-Deployment Assessment

FDE部署前系统评估与检查清单。

## 评估维度

```
部署前评估框架:
┌─────────────────────────────────────────────────────────┐
│ 1. 硬件兼容性评估                                        │
│    ├── TPM可用性                                          │
│    ├── 磁盘类型(SSD/HDD)                                  │
│    ├── 处理器AES-NI支持                                   │
│    └── 内存容量                                           │
├─────────────────────────────────────────────────────────┤
│ 2. 软件环境评估                                          │
│    ├── 操作系统版本                                       │
│    ├── 现有加密状态                                       │
│    ├── 关键应用程序                                       │
│    └── 系统更新状态                                       │
├─────────────────────────────────────────────────────────┤
│ 3. 业务影响评估                                          │
│    ├── 停机窗口                                           │
│    ├── 数据备份状态                                       │
│    ├── 用户影响范围                                       │
│    └── 回滚可行性                                         │
├─────────────────────────────────────────────────────────┤
│ 4. 风险评估                                              │
│    ├── 数据丢失风险                                       │
│    ├── 性能影响                                           │
│    └── 兼容性问题                                         │
└─────────────────────────────────────────────────────────┘
```

## 评估脚本

```python
#!/usr/bin/env python3
"""
FDE部署前系统评估工具
"""
import subprocess
import json
import platform
import psutil
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class AssessmentResult:
    category: str
    item: str
    status: str  # PASS, WARN, FAIL
    details: str
    recommendation: Optional[str] = None

class PreDeploymentAssessor:
    def __init__(self):
        self.results: List[AssessmentResult] = []
        self.system_info = {}
        
    def run_all_assessments(self) -> Dict:
        """运行所有评估"""
        self.system_info = self.collect_system_info()
        
        # 硬件评估
        self.assess_hardware()
        
        # 软件评估
        self.assess_software()
        
        # 性能基线
        self.assess_performance_baseline()
        
        # 生成报告
        return self.generate_assessment_report()
    
    def collect_system_info(self) -> Dict:
        """收集系统基本信息"""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'hostname': platform.node(),
            'memory_total': psutil.virtual_memory().total,
            'disk_info': self.get_disk_info()
        }
    
    def get_disk_info(self) -> List[Dict]:
        """获取磁盘信息"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except:
                pass
        return disks
    
    def assess_hardware(self):
        """硬件兼容性评估"""
        # 内存检查
        memory_gb = self.system_info['memory_total'] / (1024**3)
        if memory_gb >= 8:
            self.add_result('Hardware', 'Memory', 'PASS', 
                          f'{memory_gb:.1f}GB RAM available')
        elif memory_gb >= 4:
            self.add_result('Hardware', 'Memory', 'WARN',
                          f'{memory_gb:.1f}GB RAM (recommended: 8GB+)')
        else:
            self.add_result('Hardware', 'Memory', 'FAIL',
                          f'{memory_gb:.1f}GB RAM insufficient',
                          'Upgrade memory before encryption')
        
        # TPM检查 (Windows)
        if self.system_info['platform'] == 'Windows':
            self.check_windows_tpm()
        elif self.system_info['platform'] == 'Linux':
            self.check_linux_tpm()
    
    def check_windows_tpm(self):
        """检查Windows TPM状态"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', 'Get-Tpm | Select-Object TpmPresent,TpmReady | ConvertTo-Json'],
                capture_output=True, text=True
            )
            tpm_info = json.loads(result.stdout)
            
            if tpm_info.get('TpmPresent') and tpm_info.get('TpmReady'):
                self.add_result('Hardware', 'TPM', 'PASS', 'TPM 2.0 available and ready')
            elif tpm_info.get('TpmPresent'):
                self.add_result('Hardware', 'TPM', 'WARN', 'TPM present but not ready',
                              'Check BIOS settings to enable TPM')
            else:
                self.add_result('Hardware', 'TPM', 'FAIL', 'TPM not available',
                              'TPM required for optimal BitLocker experience')
        except:
            self.add_result('Hardware', 'TPM', 'WARN', 'Could not determine TPM status')
    
    def check_linux_tpm(self):
        """检查Linux TPM状态"""
        tpm_paths = ['/dev/tpm0', '/dev/tpmrm0']
        tpm_found = any(os.path.exists(p) for p in tpm_paths)
        
        if tpm_found:
            self.add_result('Hardware', 'TPM', 'PASS', 'TPM device found')
        else:
            self.add_result('Hardware', 'TPM', 'WARN', 'TPM not detected',
                          'Check kernel modules: tpm_tis, tpm_crb')
    
    def assess_software(self):
        """软件环境评估"""
        # 检查现有加密
        if self.system_info['platform'] == 'Windows':
            self.check_windows_encryption()
        elif self.system_info['platform'] == 'Linux':
            self.check_linux_encryption()
    
    def check_windows_encryption(self):
        """检查Windows加密状态"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', 'Get-BitLockerVolume | Select-Object MountPoint,ProtectionStatus | ConvertTo-Json'],
                capture_output=True, text=True
            )
            volumes = json.loads(result.stdout)
            
            encrypted_count = sum(1 for v in volumes if v.get('ProtectionStatus') == 1)
            
            if encrypted_count > 0:
                self.add_result('Software', 'Existing Encryption', 'WARN',
                              f'{encrypted_count} volumes already encrypted',
                              'Review existing encryption configuration')
            else:
                self.add_result('Software', 'Existing Encryption', 'PASS',
                              'No existing encryption detected')
        except:
            self.add_result('Software', 'Existing Encryption', 'WARN',
                          'Could not check encryption status')
    
    def check_linux_encryption(self):
        """检查Linux加密状态"""
        try:
            result = subprocess.run(
                ['lsblk', '-f', '-J'],
                capture_output=True, text=True
            )
            block_info = json.loads(result.stdout)
            
            luks_found = False
            for device in block_info.get('blockdevices', []):
                if 'crypto_LUKS' in str(device):
                    luks_found = True
                    break
            
            if luks_found:
                self.add_result('Software', 'Existing Encryption', 'WARN',
                              'Existing LUKS containers found',
                              'Document existing encryption setup')
            else:
                self.add_result('Software', 'Existing Encryption', 'PASS',
                              'No existing LUKS encryption')
        except:
            pass
    
    def assess_performance_baseline(self):
        """性能基线评估"""
        # 磁盘性能快速测试
        self.add_result('Performance', 'Disk Benchmark', 'INFO',
                       'Run full benchmark before deployment',
                       'Use: fio --name=baseline --filename=test.bin --size=1G')
    
    def add_result(self, category: str, item: str, status: str, 
                   details: str, recommendation: str = None):
        """添加评估结果"""
        self.results.append(AssessmentResult(
            category=category,
            item=item,
            status=status,
            details=details,
            recommendation=recommendation
        ))
    
    def generate_assessment_report(self) -> Dict:
        """生成评估报告"""
        pass_count = sum(1 for r in self.results if r.status == 'PASS')
        warn_count = sum(1 for r in self.results if r.status == 'WARN')
        fail_count = sum(1 for r in self.results if r.status == 'FAIL')
        
        report = {
            'assessment_date': datetime.now().isoformat(),
            'system_info': self.system_info,
            'summary': {
                'total_checks': len(self.results),
                'passed': pass_count,
                'warnings': warn_count,
                'failed': fail_count,
                'ready_for_deployment': fail_count == 0
            },
            'details': [asdict(r) for r in self.results],
            'recommendations': [
                r.recommendation for r in self.results 
                if r.recommendation and r.status in ['WARN', 'FAIL']
            ]
        }
        
        # 保存报告
        with open(f'pre_deployment_assessment_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return report

# 使用示例
if __name__ == "__main__":
    assessor = PreDeploymentAssessor()
    report = assessor.run_all_assessments()
    
    print("\n=== Pre-Deployment Assessment ===")
    print(f"Total Checks: {report['summary']['total_checks']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Warnings: {report['summary']['warnings']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"\nReady for Deployment: {report['summary']['ready_for_deployment']}")
    
    if report['recommendations']:
        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  - {rec}")
```

## 部署检查清单

```markdown
# FDE部署前检查清单

## 硬件要求
- [ ] 内存 >= 4GB (推荐 8GB)
- [ ] 磁盘空间 >= 10GB 可用
- [ ] TPM 2.0 可用 (Windows)
- [ ] 处理器支持 AES-NI
- [ ] 电池健康 (笔记本电脑)

## 软件要求
- [ ] 操作系统版本受支持
- [ ] 所有系统更新已安装
- [ ] 关键应用程序兼容性已验证
- [ ] 现有加密配置已记录

## 业务准备
- [ ] 停机时间窗口已确认
- [ ] 数据备份已完成
- [ ] 用户已收到通知
- [ ] 回滚方案已准备

## 风险评估
- [ ] 数据丢失风险: 低
- [ ] 性能影响: 可接受
- [ ] 兼容性问题: 已识别并解决
```

## 学习要点

1. 部署前评估框架
2. 硬件兼容性检查
3. 软件环境评估
4. 风险识别与缓解
5. 检查清单使用
