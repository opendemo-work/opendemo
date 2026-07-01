#!/usr/bin/env bash
# 停止 Iceberg 数据湖演示

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "停止 Iceberg 数据湖演示..."

if command -v docker-compose &>/dev/null; then
    docker-compose down
else
    docker compose down
fi

echo "✅ Iceberg 数据湖演示 已停止"
