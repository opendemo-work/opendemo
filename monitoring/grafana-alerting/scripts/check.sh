#!/usr/bin/env bash
# 检查 Grafana 告警通知演示 状态

set -euo pipefail

echo "=========================================="
echo "Grafana 告警通知演示 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo "✅ 检查完成"
