#!/usr/bin/env bash
# 停止 mongodb 演示环境
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

docker-compose down

echo "✅ mongodb 环境已停止"
