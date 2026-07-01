#!/usr/bin/env bash
# Docker 数据卷与持久化 演示脚本

set -euo pipefail

echo "=========================================="
echo "Docker 数据卷与持久化"
echo "=========================================="

docker-compose up -d 2>/dev/null || echo '请确保 Docker 已启动'

echo "✅ 演示完成"
