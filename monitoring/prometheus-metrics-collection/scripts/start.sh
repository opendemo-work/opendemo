#!/usr/bin/env bash
# 启动 Prometheus 监控栈

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=========================================="
echo "启动 Prometheus 监控栈"
echo "=========================================="

if command -v docker-compose &>/dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo ""
echo "等待服务就绪..."
sleep 5

echo ""
echo "✅ 监控栈已启动"
echo "Prometheus:   http://localhost:9090"
echo "Grafana:      http://localhost:3000 (admin/admin)"
echo "Alertmanager: http://localhost:9093"
