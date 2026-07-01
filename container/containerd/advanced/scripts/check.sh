#!/usr/bin/env bash
# 检查 containerd 与 nerdctl 高级操作 状态

set -euo pipefail

echo "检查 containerd 与 nerdctl 高级操作..."
nerdctl version 2>/dev/null || echo 'nerdctl 未安装'
echo "✅ 检查完成"
