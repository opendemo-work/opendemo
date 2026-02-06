#!/bin/bash

echo "🛡️  CI/CD 安全检查"

# 检查是否在 CI 环境中
if [ "$CI" != "true" ]; then
    echo "⚠️  注意：这不是在 CI 环境中运行"
fi

# 执行完整的安全检查套件
echo "执行安全扫描..."
python3 scripts/security/scan_secrets.py

echo "检查 Git 状态..."
if ! git diff --quiet; then
    echo "❌ 检测到未提交的更改，请先提交更改"
    git status
    exit 1
fi

echo "检查敏感文件..."
./scripts/security/check_security.sh

echo "✅ CI 安全检查通过"