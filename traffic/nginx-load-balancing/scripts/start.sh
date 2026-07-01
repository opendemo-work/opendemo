#!/usr/bin/env bash
# 启动 NGINX 负载均衡演示

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "启动 NGINX 负载均衡演示..."

if command -v docker-compose &>/dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo "✅ NGINX 负载均衡演示 已启动"
