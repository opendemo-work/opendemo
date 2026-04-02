# FDE Field Deployment Automation

FDE现场部署自动化工具与流程演示。

## 现场部署挑战

```
现场部署场景:
┌─────────────────────────────────────────────────────────┐
│ 场景1: 100台设备需要在周末完成部署                        │
│ ├── 时间紧，人工操作来不及                                │
│ ├── 配置一致性要求高                                      │
│ └── 需要实时状态报告                                      │
├─────────────────────────────────────────────────────────┤
│ 场景2: 分布式办公地点 (5个城市)                          │
│ ├── 远程技术支持能力有限                                  │
│ ├── 各地IT水平参差不齐                                    │
│ └── 需要标准化流程                                        │
├─────────────────────────────────────────────────────────┤
│ 场景3: 生产环境，不能停机                                 │
│ ├── 业务连续性要求                                        │
│ ├── 需要零停机部署                                        │
│ └── 回滚方案必须就绪                                      │
└─────────────────────────────────────────────────────────┘
```

## Ansible自动化部署

### 完整Playbook
```yaml
# fde-deployment.yml
---
- name: FDE Deployment to Corporate Devices
  hosts: windows_workstations
  gather_facts: yes
  vars:
    encryption_method: "BitLocker"
    recovery_key_destination: "AzureAD"
    tpm_required: true
    
  tasks:
    # 1. 预检查
    - name: Check if device supports TPM
      win_shell: |
        Get-Tpm | Select-Object TpmPresent,TpmReady
      register: tpm_status
      
    - name: Fail if TPM not available
      fail:
        msg: "TPM not available on {{ inventory_hostname }}"
      when: 
        - tpm_required
        - "'TpmPresent : False' in tpm_status.stdout"
    
    # 2. 检查当前加密状态
    - name: Get current BitLocker status
      win_shell: |
        $vol = Get-BitLockerVolume -MountPoint C:
        $vol.ProtectionStatus
      register: bl_status
      changed_when: false
      
    # 3. 启用BitLocker (如果未加密)
    - name: Enable BitLocker encryption
      win_shell: |
        Enable-BitLocker `
          -MountPoint C: `
          -EncryptionMethod Aes256 `
          -RecoveryPasswordProtector `
          -SkipHardwareTest
      when: bl_status.stdout | trim == "Off"
      register: enable_result
      
    # 4. 备份恢复密钥到Azure AD
    - name: Backup recovery key to Azure AD
      win_shell: |
        $BLV = Get-BitLockerVolume -MountPoint C:
        BackupToAAD-BitLockerKeyProtector `
          -MountPoint C: `
          -KeyProtectorId ($BLV.KeyProtector | Where-Object {$_.KeyProtectorType -eq 'RecoveryPassword'}).KeyProtectorId
      when: enable_result.changed
      
    # 5. 验证加密状态
    - name: Verify encryption completed
      win_shell: |
        $vol = Get-BitLockerVolume -MountPoint C:
        if ($vol.ProtectionStatus -eq 'On') {
          "ENCRYPTED"
        } else {
          "NOT_ENCRYPTED"
        }
      register: verify_status
      
    # 6. 生成报告
    - name: Generate deployment report
      win_template:
        src: report.j2
        dest: "C:\\DeploymentReports\\{{ inventory_hostname }}_report.txt"
      vars:
        status: "{{ verify_status.stdout | trim }}"
        tpm_info: "{{ tpm_status.stdout }}"
        
  handlers:
    - name: Notify deployment completion
      debug:
        msg: "FDE deployment completed on {{ inventory_hostname }}"
```

### Linux LUKS自动化
```yaml
# luks-deployment.yml
---
- name: LUKS Deployment to Linux Servers
  hosts: linux_servers
  become: yes
  vars:
    luks_devices:
      - /dev/sda2
      - /dev/sdb1
    cipher: "aes-xts-plain64"
    key_size: 512
    
  tasks:
    # 1. 安装必要软件
    - name: Install cryptsetup
      package:
        name: cryptsetup
        state: present
        
    # 2. 检查设备是否已加密
    - name: Check if device is already LUKS
      command: "cryptsetup isLuks {{ item }}"
      with_items: "{{ luks_devices }}"
      register: luks_check
      ignore_errors: yes
      changed_when: false
      
    # 3. 创建LUKS容器
    - name: Create LUKS container
      shell: |
        echo "{{ luks_passphrase }}" | cryptsetup luksFormat \
          --type luks2 \
          --cipher {{ cipher }} \
          --key-size {{ key_size }} \
          --batch-mode {{ item.item }}
      with_items: "{{ luks_check.results }}"
      when: item.rc != 0
      
    # 4. 打开加密设备
    - name: Open LUKS device
      shell: |
        echo "{{ luks_passphrase }}" | cryptsetup luksOpen \
          {{ item.item }} secure_{{ item.item | basename }}
      with_items: "{{ luks_check.results }}"
      when: item.rc != 0
      
    # 5. 创建文件系统
    - name: Create filesystem
      filesystem:
        fstype: ext4
        dev: "/dev/mapper/secure_{{ item | basename }}"
      with_items: "{{ luks_devices }}"
      
    # 6. 配置/etc/crypttab
    - name: Configure crypttab
      template:
        src: crypttab.j2
        dest: /etc/crypttab
        
    # 7. 配置/etc/fstab
    - name: Configure fstab
      mount:
        path: "/mnt/secure_{{ item | basename }}"
        src: "/dev/mapper/secure_{{ item | basename }}"
        fstype: ext4
        state: mounted
      with_items: "{{ luks_devices }}"
```

## 批量部署脚本

```python
#!/usr/bin/env python3
"""
FDE批量部署控制器
"""
import json
import subprocess
import concurrent.futures
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict
import threading

@dataclass
class DeploymentResult:
    hostname: str
    status: str
    message: str
    timestamp: datetime
    details: Dict

class FDEBatchDeployment:
    def __init__(self, inventory_file: str, max_workers: int = 10):
        self.inventory = self.load_inventory(inventory_file)
        self.max_workers = max_workers
        self.results = []
        self.lock = threading.Lock()
        
    def load_inventory(self, file: str) -> List[Dict]:
        """加载设备清单"""
        with open(file) as f:
            return json.load(f)
    
    def deploy_to_host(self, host: Dict) -> DeploymentResult:
        """部署到单个主机"""
        hostname = host['hostname']
        platform = host['platform']
        
        try:
            if platform == 'windows':
                result = self.deploy_windows(host)
            elif platform == 'linux':
                result = self.deploy_linux(host)
            elif platform == 'macos':
                result = self.deploy_macos(host)
            else:
                return DeploymentResult(
                    hostname=hostname,
                    status='FAILED',
                    message=f'Unsupported platform: {platform}',
                    timestamp=datetime.now(),
                    details={}
                )
            
            return result
            
        except Exception as e:
            return DeploymentResult(
                hostname=hostname,
                status='ERROR',
                message=str(e),
                timestamp=datetime.now(),
                details={'error_type': type(e).__name__}
            )
    
    def deploy_windows(self, host: Dict) -> DeploymentResult:
        """Windows部署"""
        # 执行Ansible playbook
        cmd = [
            'ansible-playbook',
            '-i', host['ip'] + ',',
            'fde-deployment.yml',
            '-e', f"target_host={host['hostname']}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        success = result.returncode == 0
        return DeploymentResult(
            hostname=host['hostname'],
            status='SUCCESS' if success else 'FAILED',
            message='BitLocker enabled successfully' if success else result.stderr,
            timestamp=datetime.now(),
            details={'ansible_output': result.stdout}
        )
    
    def deploy_linux(self, host: Dict) -> DeploymentResult:
        """Linux部署"""
        cmd = [
            'ansible-playbook',
            '-i', host['ip'] + ',',
            'luks-deployment.yml',
            '-e', f"target_host={host['hostname']}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        success = result.returncode == 0
        return DeploymentResult(
            hostname=host['hostname'],
            status='SUCCESS' if success else 'FAILED',
            message='LUKS encryption enabled' if success else result.stderr,
            timestamp=datetime.now(),
            details={'ansible_output': result.stdout}
        )
    
    def run_batch_deployment(self) -> List[DeploymentResult]:
        """执行批量部署"""
        print(f"Starting batch deployment to {len(self.inventory)} hosts...")
        print(f"Max parallel workers: {self.max_workers}")
        
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            futures = {
                executor.submit(self.deploy_to_host, host): host 
                for host in self.inventory
            }
            
            for future in concurrent.futures.as_completed(futures):
                host = futures[future]
                try:
                    result = future.result()
                    with self.lock:
                        self.results.append(result)
                    
                    # 实时状态更新
                    print(f"[{result.status}] {result.hostname}: {result.message}")
                    
                except Exception as e:
                    print(f"[ERROR] {host['hostname']}: {e}")
        
        return self.results
    
    def generate_report(self) -> Dict:
        """生成部署报告"""
        total = len(self.results)
        success = sum(1 for r in self.results if r.status == 'SUCCESS')
        failed = total - success
        
        report = {
            'deployment_date': datetime.now().isoformat(),
            'summary': {
                'total_hosts': total,
                'successful': success,
                'failed': failed,
                'success_rate': (success / total * 100) if total > 0 else 0
            },
            'details': [
                {
                    'hostname': r.hostname,
                    'status': r.status,
                    'message': r.message,
                    'timestamp': r.timestamp.isoformat()
                }
                for r in self.results
            ]
        }
        
        # 保存报告
        with open(f'deployment_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return report

# 使用示例
if __name__ == "__main__":
    deployer = FDEBatchDeployment('inventory.json', max_workers=5)
    results = deployer.run_batch_deployment()
    report = deployer.generate_report()
    
    print("\n=== Deployment Summary ===")
    print(f"Total: {report['summary']['total_hosts']}")
    print(f"Success: {report['summary']['successful']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"Rate: {report['summary']['success_rate']:.1f}%")
```

## 实时状态监控

```python
# 部署状态WebSocket服务器
import asyncio
import websockets
import json
from datetime import datetime

connected_clients = set()

def broadcast_status_update(hostname: str, status: str, progress: int):
    """广播状态更新到所有客户端"""
    message = json.dumps({
        'type': 'status_update',
        'hostname': hostname,
        'status': status,
        'progress': progress,
        'timestamp': datetime.now().isoformat()
    })
    
    websockets.broadcast(connected_clients, message)

async def status_server(websocket, path):
    """WebSocket状态服务器"""
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # 处理客户端请求
            data = json.loads(message)
            if data['action'] == 'get_status':
                # 返回当前部署状态
                pass
    finally:
        connected_clients.remove(websocket)

# 启动服务器
# asyncio.run(websockets.serve(status_server, '0.0.0.0', 8765))
```

## 部署清单验证

```yaml
# pre-deployment-checklist.yml
---
- name: Pre-Deployment System Check
  hosts: all
  gather_facts: yes
  
  tasks:
    - name: Check disk space
      assert:
        that:
          - ansible_facts['mounts'] | selectattr('mount', 'equalto', '/') | map(attribute='size_available') | first > 10737418240
        fail_msg: "Insufficient disk space (need 10GB+)"
        success_msg: "Disk space check passed"
        
    - name: Check memory
      assert:
        that:
          - ansible_facts['memtotal_mb'] > 4096
        fail_msg: "Insufficient memory (need 4GB+)"
        
    - name: Check BIOS settings (Windows)
      win_shell: |
        $bios = Get-WmiObject -Class Win32_BIOS
        $tpm = Get-Tpm
        @{
          BIOSVersion = $bios.SMBIOSBIOSVersion
          TPMReady = $tpm.TpmReady
        } | ConvertTo-Json
      when: ansible_os_family == "Windows"
      register: bios_info
      
    - name: Warn if Secure Boot disabled
      debug:
        msg: "WARNING: Secure Boot is disabled"
      when: 
        - ansible_os_family == "Windows"
        - "'SecureBoot : Disabled' in bios_info.stdout"
```

## 学习要点

1. Ansible自动化部署
2. 批量部署并行处理
3. 实时状态监控
4. 部署前系统检查
5. 部署报告生成
