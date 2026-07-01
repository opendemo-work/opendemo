#!/usr/bin/env bash
# 检查 数据仓库分层设计 状态

set -euo pipefail

echo "=========================================="
echo "数据仓库分层设计 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo "✅ 检查完成"
