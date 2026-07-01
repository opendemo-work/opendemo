#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "检查 MySQL 高可用架构状态..."
./scripts/check_replication.sh
