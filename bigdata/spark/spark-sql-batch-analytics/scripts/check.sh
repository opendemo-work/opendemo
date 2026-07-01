#!/usr/bin/env bash
# 检查 Spark SQL 批处理分析 状态

set -euo pipefail

echo "=========================================="
echo "Spark SQL 批处理分析 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo "✅ 检查完成"
