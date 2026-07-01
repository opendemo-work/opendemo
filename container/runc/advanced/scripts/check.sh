#!/usr/bin/env bash
# 检查 runc 自定义容器运行时配置 状态

set -euo pipefail

echo "检查 runc 自定义容器运行时配置..."
runc --version 2>/dev/null || echo 'runc 未安装'
echo "✅ 检查完成"
