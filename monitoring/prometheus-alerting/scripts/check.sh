#!/usr/bin/env bash
# 检查 Prometheus 告警规则演示 状态

set -euo pipefail

echo "=========================================="
echo "Prometheus 告警规则演示 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo "✅ 检查完成"
