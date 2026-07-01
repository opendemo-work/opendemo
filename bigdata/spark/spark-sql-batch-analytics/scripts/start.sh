#!/usr/bin/env bash
# 启动 Spark SQL 批处理分析

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "启动 Spark SQL 批处理分析..."

if command -v docker-compose &>/dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo "✅ Spark SQL 批处理分析 已启动"
