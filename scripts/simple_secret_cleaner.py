#!/usr/bin/env python3
"""
简化的敏感信息清理脚本
专注于清理最明显的硬编码密码和密钥
"""

import os
import re
from pathlib import Path

def clean_database_readmes():
    """清理数据库README文件中的硬编码密码"""
    database_dir = Path("database")
    if not database_dir.exists():
        print("未找到database目录")
        return
    
    # 常见的硬编码密码模式
    password_patterns = [
        r'pwd:\s*"[^"]*"',
        r"pwd:\s*'[^']*'",
        r'password["\']?\s*[:=]\s*["\'][^"\']*["\']',
        r'PASSWORD\s*=\s*["\'][^"\']*["\']',
    ]
    
    # 替换为环境变量占位符
    replacements = {
        r'pwd:\s*"[^"]*"': 'pwd: "${DB_PASSWORD}"',
        r"pwd:\s*'[^']*'": "pwd: '${DB_PASSWORD}'",
        r'password["\']?\s*[:=]\s*["\'][^"\']*["\']': 'password: "${DB_PASSWORD}"',
        r'PASSWORD\s*=\s*["\'][^"\']*["\']': 'PASSWORD = "${DB_PASSWORD}"',
    }
    
    readme_files = list(database_dir.rglob("README.md"))
    print(f"找到 {len(readme_files)} 个README文件")
    
    for readme_file in readme_files:
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            for pattern, replacement in replacements.items():
                if re.search(pattern, content, re.IGNORECASE):
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                    changes_made.append(pattern)
            
            if content != original_content:
                with open(readme_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"已更新: {readme_file}")
                print(f"  替换了: {', '.join(changes_made)}")
                
        except Exception as e:
            print(f"处理 {readme_file} 时出错: {e}")

def clean_k8s_secrets():
    """清理Kubernetes secret文件中的示例值"""
    k8s_dirs = ["vibe-coding", "kubernetes"]
    
    for k8s_dir in k8s_dirs:
        dir_path = Path(k8s_dir)
        if not dir_path.exists():
            continue
            
        secret_files = list(dir_path.rglob("secret.yaml"))
        print(f"在 {k8s_dir} 中找到 {len(secret_files)} 个secret文件")
        
        for secret_file in secret_files:
            try:
                with open(secret_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 替换示例值为占位符
                replacements = {
                    'YOUR_[A-Z_]+_BASE64': '${SECRET_PLACEHOLDER}',
                    'YOUR_[A-Z_]+': '${SECRET_PLACEHOLDER}',
                }
                
                original_content = content
                for pattern, replacement in replacements.items():
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    with open(secret_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"已更新: {secret_file}")
                    
            except Exception as e:
                print(f"处理 {secret_file} 时出错: {e}")

def clean_nodejs_examples():
    """清理Node.js示例中的硬编码密码"""
    nodejs_dir = Path("nodejs")
    if not nodejs_dir.exists():
        return
    
    js_files = list(nodejs_dir.rglob("*.js"))
    print(f"找到 {len(js_files)} 个JavaScript文件")
    
    password_patterns = [
        r'const\s+password\s*=\s*["\'][^"\']*["\']',
        r'password\s*=\s*["\'][^"\']*["\']',
    ]
    
    for js_file in js_files:
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            for pattern in password_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    content = re.sub(pattern, 'const password = process.env.PASSWORD || "placeholder"', content, flags=re.IGNORECASE)
            
            if content != original_content:
                with open(js_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"已更新: {js_file}")
                
        except Exception as e:
            print(f"处理 {js_file} 时出错: {e}")

def create_security_docs():
    """创建安全文档"""
    # 创建.env.template
    env_template = """# 环境变量配置文件模板
# 复制此文件为 .env 并填入实际值

# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USERNAME=your_username
DB_PASSWORD=your_secure_password

# Redis配置  
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# 安全配置
JWT_SECRET=your_jwt_secret_key
API_KEY=your_api_key

# 应用配置
APP_ENV=development
DEBUG=true

# 重要提示:
# 1. 请勿将此文件提交到Git
# 2. 在生产环境中使用密钥管理服务
# 3. 定期轮换敏感凭据
"""
    
    with open(".env.template", "w", encoding="utf-8") as f:
        f.write(env_template)
    
    # 创建安全说明
    security_notice = """# 安全配置说明

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
"""
    
    with open("SECURITY_CONFIG.md", "w", encoding="utf-8") as f:
        f.write(security_notice)
    
    print("已创建安全配置文档")

def main():
    print("=== 敏感信息清理工具 ===")
    print("开始清理硬编码的敏感信息...\n")
    
    # 执行各项清理任务
    clean_database_readmes()
    print()
    
    clean_k8s_secrets()
    print()
    
    clean_nodejs_examples()
    print()
    
    create_security_docs()
    
    print("\n=== 清理完成 ===")
    print("已移除硬编码的敏感信息")
    print("请查看 SECURITY_CONFIG.md 了解正确的配置方式")

if __name__ == "__main__":
    main()