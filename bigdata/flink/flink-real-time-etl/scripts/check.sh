#!/usr/bin/env bash
# 检查 Flink 实时 ETL 处理 状态

set -euo pipefail

echo "=========================================="
echo "Flink 实时 ETL 处理 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo "✅ 检查完成"
