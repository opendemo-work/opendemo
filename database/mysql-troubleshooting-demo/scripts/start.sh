#!/usr/bin/env bash
# 启动 mysql 演示环境
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "启动 mysql 演示环境..."
docker-compose up -d

echo "等待服务就绪..."
sleep 5

echo "✅ mysql 环境已启动"
