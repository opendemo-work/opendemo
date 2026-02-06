#!/bin/bash

echo "🔑 生成安全密钥..."

# 创建输出目录
KEYS_DIR="config/secrets/$(date +%Y%m)"
mkdir -p "$KEYS_DIR"

# 生成各种类型的密钥
echo "生成 JWT 密钥..."
JWT_SECRET=$(openssl rand -hex 32)
echo "JWT_SECRET=$JWT_SECRET" > "$KEYS_DIR/jwt.secret"

echo "生成应用密钥..."
APP_SECRET=$(openssl rand -hex 64)
echo "APP_SECRET=$APP_SECRET" > "$KEYS_DIR/app.secret"

echo "生成加密密钥..."
ENCRYPTION_KEY=$(openssl rand -hex 32)
echo "ENCRYPTION_KEY=$ENCRYPTION_KEY" > "$KEYS_DIR/encryption.secret"

echo "生成数据库密码..."
DB_PASSWORD=$(openssl rand -base64 32)
echo "DB_PASSWORD=$DB_PASSWORD" > "$KEYS_DIR/database.secret"

# 创建汇总文件
cat > "$KEYS_DIR/keys_summary.txt" << SUMMARY
密钥生成报告 - $(date)
========================

生成的密钥文件：
- jwt.secret: JWT 签名密钥
- app.secret: 应用程序密钥  
- encryption.secret: 加密密钥
- database.secret: 数据库密码

请妥善保管这些密钥文件！
SUMMARY

echo "✅ 密钥生成完成！"
echo "密钥文件保存在: $KEYS_DIR"
echo "请立即将这些密钥添加到您的 .env 文件中"