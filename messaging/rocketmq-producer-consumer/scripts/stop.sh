#!/usr/bin/env bash
# 停止 RocketMQ 生产者消费者模式

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "停止 RocketMQ 生产者消费者模式..."

if command -v docker-compose &>/dev/null; then
    docker-compose down
else
    docker compose down
fi

echo "✅ RocketMQ 生产者消费者模式 已停止"
