#!/usr/bin/env bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

# 检查 containerd 与 nerdctl 高级操作 状态

set -euo pipefail

echo "检查 containerd 与 nerdctl 高级操作..."
nerdctl version 2>/dev/null || echo 'nerdctl 未安装'
echo "✅ 检查完成"
