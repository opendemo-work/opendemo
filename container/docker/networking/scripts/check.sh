#!/usr/bin/env bash
# 检查 Docker 网络模式详解 状态

set -euo pipefail

echo "检查 Docker 网络模式详解..."
docker network ls 2>/dev/null | head -5 || echo 'Docker 未运行或当前用户无权限'
echo "✅ 检查完成"
