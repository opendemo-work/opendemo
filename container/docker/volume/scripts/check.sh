#!/usr/bin/env bash
# 检查 Docker 数据卷与持久化 状态

set -euo pipefail

echo "检查 Docker 数据卷与持久化..."
docker volume ls 2>/dev/null | head -5 || echo 'Docker 未运行或当前用户无权限'
echo "✅ 检查完成"
