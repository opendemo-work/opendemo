#!/usr/bin/env bash
# 启动 RocketMQ 生产者消费者模式

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "启动 RocketMQ 生产者消费者模式..."

if command -v docker-compose &>/dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo "等待服务就绪..."
sleep 10

echo "✅ RocketMQ 生产者消费者模式 已启动"
