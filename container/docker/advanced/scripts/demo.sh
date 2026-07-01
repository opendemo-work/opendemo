#!/usr/bin/env bash
# Docker 高级网络与多阶段构建 演示脚本

set -euo pipefail

echo "=========================================="
echo "Docker 高级网络与多阶段构建"
echo "=========================================="

docker-compose up -d 2>/dev/null || echo '请确保 Docker 已启动'

echo "✅ 演示完成"
