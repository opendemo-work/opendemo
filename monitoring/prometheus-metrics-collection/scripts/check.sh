#!/usr/bin/env bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

# 检查 Prometheus 监控栈状态

set -euo pipefail

echo "=========================================="
echo "Prometheus 监控栈状态检查"
echo "=========================================="

echo ""
echo "--- 容器状态 ---"
docker ps --filter name=prometheus --filter name=grafana --filter name=alertmanager --filter name=node-exporter --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "--- Prometheus Targets ---"
curl -s http://localhost:9090/api/v1/targets | python3 -c "import sys,json; d=json.load(sys.stdin); print('Active targets:', len(d['data']['activeTargets'])); [print(f\"  {t['labels'].get('job','?')}: {t['health']}\") for t in d['data']['activeTargets']]" 2>/dev/null || echo "无法连接 Prometheus"

echo ""
echo "--- Alertmanager Status ---"
curl -s http://localhost:9093/api/v2/status | python3 -c "import sys,json; d=json.load(sys.stdin); print('Cluster status:', d.get('cluster','N/A'))" 2>/dev/null || echo "无法连接 Alertmanager"

echo ""
echo "✅ 检查完成"
