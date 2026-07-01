#!/usr/bin/env bash
# linux-iotop-disk-monitor-demo 演示脚本

set -euo pipefail

echo "=========================================="
echo "iotop 演示"
echo "=========================================="

# 检查命令是否存在
if ! command -v iotop &>/dev/null; then
    echo "❌ iotop 命令未找到，请先安装"
    exit 1
fi

echo "✅ iotop 已安装"
echo ""

# 运行命令并展示输出（使用 localhost / 示例目标）
echo "--- iotop 基本用法 ---"
# 请根据实际工具修改以下命令
case "iotop" in
    dig)
        iotop +short localhost A || true
        iotop +short example.com NS || true
        ;;
    nslookup)
        iotop localhost || true
        iotop example.com || true
        ;;
    traceroute)
        iotop -I -m 5 example.com || true
        ;;
    nc)
        echo "测试本地 22 端口连通性..."
        timeout 3 iotop -zv localhost 22 || echo "端口未开放或超时"
        ;;
    netstat)
        iotop -tlnp || true
        ;;
    lsof)
        iotop -i :22 || true
        ;;
    ifconfig|ip)
        iotop || true
        ;;
    htop|top|iotop|tsar)
        echo "iotop 为交互式工具，请手动运行: iotop"
        iotop -v 2>/dev/null || true
        ;;
    rsync)
        echo "rsync 版本: $(rsync --version | head -n 1)"
        ;;
    *)
        echo "请根据 iotop 的实际用法修改本脚本"
        ;;
esac

echo ""
echo "✅ 演示完成"
