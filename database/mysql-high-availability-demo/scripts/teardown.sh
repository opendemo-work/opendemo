#!/usr/bin/env bash
# 清理 MySQL 主从容器和数据卷

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "停止并清理 MySQL 主从环境..."
docker-compose down -v

echo "✅ 清理完成"
