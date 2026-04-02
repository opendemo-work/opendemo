# Compliance and Audit (GDPR/HIPAA/PCI-DSS)

FDE合规性与审计要求演示。

## 合规框架对比

| 标准 | 适用场景 | 加密要求 | 密钥管理 | 审计要求 |
|------|----------|----------|----------|----------|
| **GDPR** | 欧盟个人数据 | 假名化/加密 | 访问控制 | 处理记录 |
| **HIPAA** | 医疗信息 | 加密传输+静态 | 唯一用户ID | 访问日志 |
| **PCI-DSS** | 支付卡数据 | 强加密算法 | 密钥分割 | 全面审计 |
| **SOX** | 财务数据 | 数据保护 | 职责分离 | 变更追踪 |
| **ISO 27001** | 信息安全 | 风险评估 | 密钥生命周期 | 审计追踪 |

## GDPR合规实施

### 技术要求
```yaml
# GDPR技术措施清单
gdpr_encryption_requirements:
  data_at_rest:
    - 全盘加密 (FDE) 强制
    - AES-256 或同等级别
    - 数据库字段级加密 (敏感数据)
    
  data_in_transit:
    - TLS 1.2+
    - 证书固定 (Certificate Pinning)
    
  key_management:
    - 密钥与数据分离存储
    - 定期密钥轮换
    - 安全的密钥销毁
    
  access_control:
    - 最小权限原则
    - 多因素认证 (MFA)
    - 定期访问审查
    
  breach_notification:
    - 72小时内报告
    - 加密状态评估
    - 影响评估记录
```

### 数据保护影响评估 (DPIA)
```markdown
## DPIA模板: 全盘加密部署

### 1. 数据描述
- 数据类型: 员工个人电脑数据
- 数据主体: 公司员工
- 数据量: 约500台设备

### 2. 处理活动
- 加密范围: 系统盘+数据盘
- 加密算法: AES-256-XTS
- 密钥托管: Azure AD + 本地HSM

### 3. 风险评估
| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 设备丢失/被盗 | 中 | 高 | FDE加密 |
| 密钥泄露 | 低 | 高 | HSM保护 |
| 恢复失败 | 低 | 中 | 多重备份 |

### 4. 保护措施
- 技术: TPM + BitLocker/FileVault/LUKS
- 组织: 密钥托管政策、访问审批流程
- 物理: 安全的数据中心

### 5. 残余风险
加密后设备丢失风险降至可接受水平
```

## HIPAA合规 (医疗行业)

### 安全规则要求
```python
# HIPAA审计脚本
import json
from datetime import datetime

class HIPAAComplianceChecker:
    """HIPAA Security Rule 合规检查器"""
    
    def __init__(self):
        self.checks = []
        self.findings = []
    
    def check_encryption_at_rest(self, device_info):
        """检查静态数据加密 (164.312(a)(2)(iv))"""
        check = {
            'control': 'Encryption at Rest',
            'requirement': '164.312(a)(2)(iv)',
            'device': device_info['hostname'],
            'encrypted': device_info.get('encryption_enabled', False),
            'algorithm': device_info.get('encryption_algorithm', 'N/A'),
            'compliant': device_info.get('encryption_enabled', False) and
                        device_info.get('encryption_algorithm') in ['AES-256', 'AES-128']
        }
        self.checks.append(check)
        return check['compliant']
    
    def check_access_controls(self, access_logs):
        """检查访问控制 (164.312(a)(1))"""
        unique_users = set(log['user'] for log in access_logs)
        violations = []
        
        for log in access_logs:
            if log['action'] == 'key_recovery' and not log.get('mfa_verified'):
                violations.append({
                    'time': log['timestamp'],
                    'user': log['user'],
                    'issue': 'Key recovery without MFA'
                })
        
        return {
            'unique_users': len(unique_users),
            'violations': violations,
            'compliant': len(violations) == 0
        }
    
    def check_audit_controls(self, audit_logs):
        """检查审计控制 (164.312(b))"""
        required_events = [
            'encryption_enabled',
            'key_recovery',
            'password_change',
            'device_unlock'
        ]
        
        logged_events = set(log['event_type'] for log in audit_logs)
        missing_events = set(required_events) - logged_events
        
        return {
            'logged_events': list(logged_events),
            'missing_events': list(missing_events),
            'compliant': len(missing_events) == 0
        }
    
    def generate_report(self):
        """生成合规报告"""
        total_checks = len(self.checks)
        passed_checks = sum(1 for c in self.checks if c['compliant'])
        
        return {
            'report_date': datetime.now().isoformat(),
            'summary': {
                'total_checks': total_checks,
                'passed': passed_checks,
                'failed': total_checks - passed_checks,
                'compliance_rate': (passed_checks / total_checks * 100) if total_checks > 0 else 0
            },
            'details': self.checks
        }

# 使用示例
checker = HIPAAComplianceChecker()

# 检查设备加密
checker.check_encryption_at_rest({
    'hostname': 'medical-pc-01',
    'encryption_enabled': True,
    'encryption_algorithm': 'AES-256'
})

# 生成报告
report = checker.generate_report()
print(json.dumps(report, indent=2))
```

## PCI-DSS合规 (支付行业)

### 要求3: 保护存储的持卡人数据
```bash
#!/bin/bash
# PCI-DSS Requirement 3 检查脚本

echo "=== PCI-DSS Requirement 3 验证 ==="

# 3.4 渲染PAN不可读
echo "[3.4] 检查PAN加密..."
if command -v bitlocker_status &> /dev/null; then
    bitlocker_status
fi

# 3.5 保护加密密钥
echo "[3.5] 检查密钥管理..."
echo "- 密钥是否存储在HSM中: $(test -d /dev/tpm* && echo 'Yes' || echo 'No')"
echo "- 密钥访问日志: /var/log/key-access.log"

# 3.6 加密协议和密钥管理
echo "[3.6] 检查加密算法..."
cryptsetup luksDump /dev/sda2 | grep -E "Cipher|Key slots"

# 3.7 限制业务需要的最小数据
echo "[3.7] 数据最小化检查..."
echo "- 已启用全盘加密: 符合数据保护要求"
```

## 审计日志要求

### 必须记录的事件
```yaml
# 加密相关审计事件
audit_events:
  encryption_management:
    - encryption_enabled          # 启用加密
    - encryption_disabled         # 禁用加密 (警报!)
    - encryption_algorithm_changed
    
  key_management:
    - key_generated
    - key_backed_up
    - key_recovered
    - key_rotated
    - key_destroyed
    
  access_control:
    - device_unlocked
    - recovery_key_used
    - unauthorized_access_attempt
    
  compliance:
    - policy_violation
    - compliance_scan_completed
    - remediation_action_taken
```

### 日志保留策略
```python
# 审计日志保留管理
class AuditLogRetention:
    """
    合规审计日志保留策略
    """
    RETENTION_PERIODS = {
        'GDPR': 7 * 365,      # 7年
        'HIPAA': 6 * 365,     # 6年
        'PCI-DSS': 1 * 365,   # 1年 (至少)
        'SOX': 7 * 365,       # 7年
        'ISO27001': 3 * 365   # 3年
    }
    
    @staticmethod
    def get_retention_days(standard):
        return AuditLogRetention.RETENTION_PERIODS.get(standard, 365)
    
    @staticmethod
    def should_archive(log_date, standard):
        """检查是否应该归档"""
        from datetime import datetime, timedelta
        retention_days = AuditLogRetention.get_retention_days(standard)
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        return log_date < cutoff_date
```

## 合规报告自动化

```yaml
# 自动化合规检查配置
compliance_automation:
  schedule: "0 2 * * *"  # 每天凌晨2点
  
  checks:
    - name: encryption_coverage
      description: "验证所有设备已加密"
      threshold: 100%
      
    - name: key_escrow_completeness
      description: "验证所有密钥已托管"
      threshold: 100%
      
    - name: audit_log_integrity
      description: "验证审计日志完整性"
      check_chain_of_custody: true
      
  notifications:
    on_failure:
      - email: compliance@company.com
      - slack: #security-alerts
      - ticket: auto_create
```

## 学习要点

1. 主要合规框架对比
2. GDPR/HIPAA/PCI-DSS具体要求
3. 审计日志管理
4. 自动化合规检查
5. 数据保护影响评估
