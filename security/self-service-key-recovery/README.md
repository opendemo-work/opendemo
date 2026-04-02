# Self-Service Key Recovery

用户自助密钥恢复门户演示。

## 自助服务架构

```
自助密钥恢复系统:
┌─────────────────────────────────────────────────────────┐
│                    用户浏览器                            │
│              (HTTPS/TLS 1.3)                            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  Web应用服务器                           │
│         (Flask/Django/Node.js)                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  • 身份验证 (MFA)                                │   │
│  │  • 设备验证 (所有权证明)                          │   │
│  │  • 审批工作流                                    │   │
│  │  • 密钥临时展示                                  │   │
│  └─────────────────────────────────────────────────┘   │
├────────────────────────┬────────────────────────────────┤
│                        │                                │
┌────────────────────────▼────────────────────────────────┐
│                  密钥托管后端                            │
│         (HSM/Vault/加密数据库)                           │
└─────────────────────────────────────────────────────────┘
```

## 核心流程

### 用户请求流程
```
1. 用户登录
   └── 用户名/密码 + MFA

2. 设备选择
   └── 显示用户绑定的加密设备

3. 身份验证
   └── 安全问题/邮箱验证/短信验证

4. 管理员审批 (如需要)
   └── 高敏感度设备需要二级审批

5. 密钥展示
   └── 限时展示 (5分钟)
   └── 一次性查看
```

## Python实现示例

```python
from flask import Flask, request, jsonify, session
from functools import wraps
import pyotp
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 模拟数据库
recovery_requests = {}

class SelfServiceRecovery:
    def __init__(self):
        self.key_service = KeyEscrowService()
        self.audit_logger = AuditLogger()
    
    def authenticate_user(self, username, password, mfa_token):
        """用户身份验证"""
        # 验证用户名密码
        if not self.verify_password(username, password):
            return False, "Invalid credentials"
        
        # 验证MFA
        user = self.get_user(username)
        totp = pyotp.TOTP(user['mfa_secret'])
        if not totp.verify(mfa_token):
            return False, "Invalid MFA token"
        
        return True, user
    
    def request_key_recovery(self, user_id, device_id, reason):
        """请求密钥恢复"""
        request_id = generate_request_id()
        
        recovery_requests[request_id] = {
            'user_id': user_id,
            'device_id': device_id,
            'reason': reason,
            'status': 'pending',
            'created_at': time.time(),
            'expires_at': time.time() + 3600  # 1小时过期
        }
        
        # 发送审批通知给管理员
        self.notify_admin(request_id)
        
        return request_id
    
    def approve_recovery(self, request_id, admin_id):
        """管理员批准恢复"""
        request = recovery_requests.get(request_id)
        if not request:
            return False, "Request not found"
        
        # 检索密钥
        key_data = self.key_service.retrieve_key(
            request['device_id'],
            admin_id,
            request['reason']
        )
        
        # 生成临时展示令牌
        display_token = generate_secure_token()
        
        request['status'] = 'approved'
        request['display_token'] = display_token
        request['display_expires'] = time.time() + 300  # 5分钟
        
        return True, display_token

# Flask路由
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    success, result = recovery_service.authenticate_user(
        data['username'],
        data['password'],
        data['mfa_token']
    )
    
    if success:
        session['user_id'] = result['id']
        return jsonify({'success': True, 'user': result})
    else:
        return jsonify({'success': False, 'error': result}), 401

@app.route('/api/request-recovery', methods=['POST'])
def request_recovery():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    request_id = recovery_service.request_key_recovery(
        session['user_id'],
        data['device_id'],
        data['reason']
    )
    
    return jsonify({'request_id': request_id, 'status': 'pending'})

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
```

## 学习要点

1. 自助服务流程设计
2. 多因素身份验证
3. 审批工作流
4. 安全审计日志
5. 密钥限时展示
