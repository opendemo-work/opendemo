# 安全最佳实践指南

## 🛡️ 密钥和敏感信息管理

### 重要声明
本项目中的所有演示代码仅用于学习目的，**绝不应在生产环境中使用硬编码的密码、密钥或令牌**。

## 🔐 正确的密钥管理方式

### 1. 环境变量管理

#### 创建环境变量文件模板
```bash
# .env.template - 环境变量模板文件
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
REDIS_URL=redis://:password@localhost:6379/0
JWT_SECRET=your-jwt-secret-key-here
API_KEY=your-api-key-here
```

#### 实际使用时的环境变量设置
```bash
# Linux/Mac
export DATABASE_URL="postgresql://$(whoami):$(openssl rand -hex 16)@localhost:5432/myapp"
export jwt_secret: "${JWT_SECRET}"
export REDIS_URL="redis://:$(openssl rand -hex 16)@localhost:6379/0"

# Windows PowerShell
$env:DATABASE_URL = "postgresql://$($env:USERNAME):$(openssl rand -hex 16)@localhost:5432/myapp"
$env:jwt_secret: "${JWT_SECRET}"
$env:REDIS_URL = "redis://:$($env:USERNAME)_$(openssl rand -hex 8)@localhost:6379/0"
```

### 2. 密码生成工具

#### 安全密码生成脚本
```bash
#!/bin/bash
# generate_secure_passwords.sh

echo "=== 安全密码生成器 ==="

# 生成数据库密码
DB_PASSWORD=$(openssl rand -base64 24)
echo "数据库密码: $DB_PASSWORD"

# 生成JWT密钥
JWT_SECRET=$(openssl rand -hex 32)
echo "JWT密钥: $JWT_SECRET"

# 生成API密钥
API_KEY=$(openssl rand -hex 40)
echo "API密钥: $API_KEY"

# 生成Redis密码
REDIS_PASSWORD=$(openssl rand -base64 20)
echo "Redis密码: $REDIS_PASSWORD"

# 保存到安全位置
echo "DATABASE_PASSWORD=$DB_PASSWORD" > .env.secure
echo "JWT_SECRET=$JWT_SECRET" >> .env.secure
echo "API_KEY=$API_KEY" >> .env.secure
echo "REDIS_PASSWORD=$REDIS_PASSWORD" >> .env.secure

chmod 600 .env.secure
echo "凭据已保存到 .env.secure (权限已设置为600)"
```

### 3. Kubernetes Secret管理

#### 安全的Secret创建方式
```bash
# 1. 生成随机密钥
API_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)

# 2. 创建Secret
kubectl create secret generic app-secrets \
  --from-literal=api_key: "${API_KEY}" \
  --from-literal=jwt_secret: "${JWT_SECRET}" \
  --from-literal=db-password: "${GENERIC_PASSWORD}"

# 3. 或使用YAML文件（推荐）
cat <<EOF > app-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  api-key: $(echo -n "$API_KEY" | base64)
  jwt-secret: $(echo -n "$JWT_SECRET" | base64)
  db-password: $(echo -n "$(openssl rand -base64 24)" | base64)
EOF

kubectl apply -f app-secrets.yaml
```

### 4. 数据库用户创建脚本

#### 安全的数据库用户创建
```bash
#!/bin/bash
# secure_db_setup.sh

# 生成安全密码
ADMIN_PASSWORD=$(openssl rand -base64 24)
APP_PASSWORD=$(openssl rand -base64 24)
READONLY_PASSWORD=$(openssl rand -base64 24)

# MongoDB安全用户创建
cat <<EOF > create_users.js
use admin
db.createUser({
    user: "admin",
    pwd: "${GENERIC_PASSWORD}",
    roles: [
        { role: "userAdminAnyDatabase", db: "admin" },
        { role: "dbAdminAnyDatabase", db: "admin" },
        { role: "readWriteAnyDatabase", db: "admin" }
    ]
})

use myapp
db.createUser({
    user: "app_user",
    pwd: "${GENERIC_PASSWORD}",
    roles: [
        { role: "readWrite", db: "myapp" }
    ]
})

db.createUser({
    user: "analyst",
    pwd: "${GENERIC_PASSWORD}",
    roles: [
        { role: "read", db: "myapp" }
    ]
})
EOF

# 执行用户创建
mongo < create_users.js

# 保存凭据
echo "=== 数据库凭据 ===" > db_credentials.txt
echo "管理员用户: admin" >> db_credentials.txt
echo "管理员密码: $ADMIN_PASSWORD" >> db_credentials.txt
echo "" >> db_credentials.txt
echo "应用用户: app_user" >> db_credentials.txt
echo "应用密码: $APP_PASSWORD" >> db_credentials.txt
echo "" >> db_credentials.txt
echo "只读用户: analyst" >> db_credentials.txt
echo "只读密码: $READONLY_PASSWORD" >> db_credentials.txt

chmod 600 db_credentials.txt
echo "数据库凭据已保存到 db_credentials.txt"
```

### 5. 配置文件模板

#### 应用配置模板
```yaml
# config.yaml.template
database:
  host: localhost
  port: 5432
  name: myapp
  # 实际部署时通过环境变量注入
  username: ${DB_USERNAME}
  password: ${DB_PASSWORD}

redis:
  host: localhost
  port: 6379
  # Redis密码通过环境变量注入
  password: ${REDIS_PASSWORD}

security:
  # JWT密钥通过环境变量注入
  jwt_secret: ${JWT_SECRET}
  # API密钥通过环境变量注入
  api_key: ${API_KEY}

server:
  port: 8080
  debug: false
```

### 6. Docker环境配置

#### docker-compose安全配置
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - JWT_SECRET=${JWT_SECRET}
    env_file:
      - .env.secure
    depends_on:
      - database
      - redis

  database:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: ${DB_ROOT_PASSWORD}
      POSTGRES_DB: myapp
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    environment:
      REDIS_PASSWORD: ${REDIS_PASSWORD}

volumes:
  db_data:
```

## 🚫 禁止的操作

以下操作在生产环境中**严格禁止**：

❌ 在代码中硬编码密码、密钥或令牌
❌ 将敏感信息提交到版本控制系统
❌ 在日志中记录敏感信息
❌ 使用默认或弱密码
❌ 在公共仓库中暴露配置文件
❌ 明文传输敏感信息

## ✅ 推荐的安全实践

✅ 使用环境变量管理敏感信息
✅ 实施密钥轮换策略
✅ 使用专业的密钥管理服务
✅ 定期审查和更新密码
✅ 实施最小权限原则
✅ 启用审计日志记录
✅ 使用HTTPS/TLS加密传输

## 🔧 安全工具推荐

### 密钥管理工具
- **HashiCorp Vault** - 企业级密钥管理
- **AWS Secrets Manager** - 云原生密钥管理
- **Azure Key Vault** - 微软云密钥服务
- **Kubernetes Secrets** - 容器平台密钥管理

### 密码生成工具
- `openssl rand` - 系统内置安全随机数生成器
- `pwgen` - 专业密码生成工具
- `apg` - 可定制的密码生成器

### 安全扫描工具
- **Trivy** - 容器和文件系统安全扫描
- **Bandit** - Python安全漏洞扫描
- **ESLint plugin security** - JavaScript安全检查
- **gosec** - Go语言安全扫描

## 📚 学习资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST网络安全框架](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls/)
- [密码学最佳实践](https://cryptographic.best.practices/)

---
*本指南旨在帮助开发者建立正确的安全意识和实践习惯*