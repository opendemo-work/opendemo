#!/usr/bin/env bash
# 停止 数据仓库分层设计

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "停止 数据仓库分层设计..."

if command -v docker-compose &>/dev/null; then
    docker-compose down
else
    docker compose down
fi

echo "✅ 数据仓库分层设计 已停止"
