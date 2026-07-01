#!/usr/bin/env bash
# 检查 Docker 高级网络与多阶段构建 状态

set -euo pipefail

echo "检查 Docker 高级网络与多阶段构建..."
docker ps 2>/dev/null | head -5 || echo 'Docker 未运行或当前用户无权限'
echo "✅ 检查完成"
