#!/usr/bin/env bash
# 风险等级：🟡 中风险
# 说明：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
# 生产安全提示：
#   - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
#   - 注意检查依赖版本、端口占用和目标资源配置。
#   - 生产环境执行前请经过变更评审和备份确认。

# 检查 Higress 服务网格集成 状态

set -euo pipefail

echo "=========================================="
echo "Higress 服务网格集成 状态检查"
echo "=========================================="

docker ps --format "table {.Names}\t{.Status}\t{.Ports}"

echo ""
echo "测试访问:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8080 || echo "服务未就绪"

echo "✅ 检查完成"
