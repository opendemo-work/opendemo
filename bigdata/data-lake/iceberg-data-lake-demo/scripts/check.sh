#!/usr/bin/env bash
# 检查 Iceberg 数据湖演示 状态

set -euo pipefail

echo "=========================================="
echo "Iceberg 数据湖演示 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo "✅ 检查完成"
