#!/usr/bin/env bash
# 检查 RocketMQ 延迟消息演示 状态

set -euo pipefail

echo "=========================================="
echo "RocketMQ 延迟消息演示 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo "✅ 检查完成"
