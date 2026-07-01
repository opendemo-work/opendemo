#!/usr/bin/env bash
# 检查 Airflow 定时 ETL 调度 状态

set -euo pipefail

echo "=========================================="
echo "Airflow 定时 ETL 调度 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo "✅ 检查完成"
