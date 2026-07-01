#!/usr/bin/env bash
# 启动本地 Kafka 环境

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=========================================="
echo "启动本地 Kafka 环境"
echo "=========================================="

if ! command -v docker-compose &>/dev/null && ! docker compose version &>/dev/null; then
    echo "❌ 需要安装 Docker Compose"
    exit 1
fi

if command -v docker-compose &>/dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo ""
echo "等待 Kafka 就绪..."
sleep 5

echo ""
echo "✅ Kafka 环境已启动"
echo "Broker: localhost:9092"
echo "停止环境: ./scripts/stop_kafka.sh"
