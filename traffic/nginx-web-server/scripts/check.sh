#!/usr/bin/env bash
# 检查 NGINX Web 服务器基础 状态

set -euo pipefail

echo "=========================================="
echo "NGINX Web 服务器基础 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo ""
echo "测试访问:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8080 || echo "服务未就绪"

echo "✅ 检查完成"
