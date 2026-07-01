#!/usr/bin/env bash
# 检查 RocketMQ 生产者消费者模式 状态

set -euo pipefail

echo "=========================================="
echo "RocketMQ 生产者消费者模式 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo "✅ 检查完成"
