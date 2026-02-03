# 安全配置说明

## ⚠️ 重要提醒

本项目已移除所有硬编码的敏感信息。请按照以下步骤正确配置：

### 1. 生成安全凭据
```bash
# Linux/Mac
openssl rand -base64 32  # 生成JWT密钥
openssl rand -base64 24  # 生成数据库密码

# Windows PowerShell
$bytes = New-Object byte[] 32
[Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
[Convert]::ToBase64String($bytes)
```

### 2. 配置环境变量
```bash
# 复制模板并编辑
cp .env.template .env
# 编辑 .env 文件填入生成的安全凭据
```

### 3. 在代码中使用环境变量
```javascript
// Node.js示例
const dbPassword = process.env.DB_PASSWORD || 'default_value';

// Python示例  
import os
db_password = os.getenv('DB_PASSWORD', 'default_value')

// Go示例
import "os"
dbPassword := os.Getenv("DB_PASSWORD")
```

## 🛡️ 安全最佳实践

- 永不在代码中硬编码敏感信息
- 使用环境变量或密钥管理服务
- 定期轮换密码和密钥  
- 实施最小权限原则
- 启用审计日志

## 📚 了解更多
查看 SECURITY_BEST_PRACTICES.md 获取详细的安全部署指南
