#!/usr/bin/env bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

# 检查 Docker 网络模式详解 状态

set -euo pipefail

echo "检查 Docker 网络模式详解..."
docker network ls 2>/dev/null | head -5 || echo 'Docker 未运行或当前用户无权限'
echo "✅ 检查完成"
