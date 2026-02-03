#!/bin/bash

# 安全凭据生成脚本
# 生成用于开发和测试的安全密码、密钥等

echo "=== 安全凭据生成器 ==="
echo ""

# 检查是否安装了必要的工具
if ! command -v openssl &> /dev/null; then
    echo "错误: 需要安装 openssl"
    exit 1
fi

# 创建安全凭据
echo "正在生成安全凭据..."

# 生成各种类型的密钥和密码
DB_ADMIN_PASSWORD=$(openssl rand -base64 24)
DB_APP_PASSWORD=$(openssl rand -base64 24)
DB_READONLY_PASSWORD=$(openssl rand -base64 24)

REDIS_PASSWORD=$(openssl rand -base64 20)
JWT_SECRET=$(openssl rand -hex 32)
API_KEY=$(openssl rand -hex 40)

# 显示生成的凭据
echo "=== 生成的凭据 ==="
echo "数据库管理员密码: $DB_ADMIN_PASSWORD"
echo "数据库应用密码: $DB_APP_PASSWORD" 
echo "数据库只读密码: $DB_READONLY_PASSWORD"
echo "Redis密码: $REDIS_PASSWORD"
echo "JWT密钥: $JWT_SECRET"
echo "API密钥: $API_KEY"
echo ""

# 询问是否保存到文件
read -p "是否将凭据保存到 .env 文件? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 创建 .env 文件
    cat > .env << EOF
# 自动生成的安全凭据
# 请勿提交到版本控制系统

# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_ADMIN_USER=admin
DB_ADMIN_PASSWORD=$DB_ADMIN_PASSWORD
DB_APP_USER=app_user
DB_APP_PASSWORD=$DB_APP_PASSWORD
DB_READONLY_USER=analyst
DB_READONLY_PASSWORD=$DB_READONLY_PASSWORD

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=$REDIS_PASSWORD

# 安全配置
JWT_SECRET=$JWT_SECRET
API_KEY=$API_KEY

# 应用配置
APP_ENV=development
DEBUG=true
EOF

    # 设置文件权限
    chmod 600 .env
    echo "凭据已保存到 .env 文件 (权限已设置为 600)"
    echo "请确保将 .env 添加到 .gitignore 文件中"
fi

# 询问是否创建Kubernetes Secret
echo ""
read -p "是否创建Kubernetes Secret YAML文件? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 创建Kubernetes Secret文件
    cat > k8s-secrets.yaml << EOF
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: default
type: Opaque
data:
  # 数据库凭据
  db-admin-password: $(echo -n "$DB_ADMIN_PASSWORD" | base64)
  db-app-password: $(echo -n "$DB_APP_PASSWORD" | base64)
  db-readonly-password: $(echo -n "$DB_READONLY_PASSWORD" | base64)
  
  # Redis凭据
  redis-password: $(echo -n "$REDIS_PASSWORD" | base64)
  
  # 安全凭据
  jwt-secret: $(echo -n "$JWT_SECRET" | base64)
  api-key: $(echo -n "$API_KEY" | base64)
EOF

    echo "Kubernetes Secret文件已创建: k8s-secrets.yaml"
    echo "使用命令部署: kubectl apply -f k8s-secrets.yaml"
fi

echo ""
echo "=== 完成 ==="
echo "凭据生成完毕，请妥善保管这些敏感信息"
echo "建议定期轮换这些凭据以确保安全"