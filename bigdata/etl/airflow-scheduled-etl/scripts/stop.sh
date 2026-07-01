#!/usr/bin/env bash
# 停止 Airflow 定时 ETL 调度

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "停止 Airflow 定时 ETL 调度..."

if command -v docker-compose &>/dev/null; then
    docker-compose down
else
    docker compose down
fi

echo "✅ Airflow 定时 ETL 调度 已停止"
