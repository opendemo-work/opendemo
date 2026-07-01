#!/usr/bin/env bash
# 检查 containerd 基础使用 状态

set -euo pipefail

echo "检查 containerd 基础使用..."
ctr version 2>/dev/null || echo 'containerd/ctr 未安装'
echo "✅ 检查完成"
