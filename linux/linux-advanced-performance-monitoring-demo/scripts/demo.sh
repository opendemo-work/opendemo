#!/usr/bin/env bash
# linux-advanced-performance-monitoring-demo 演示脚本

set -euo pipefail

echo "=========================================="
echo "perf 演示"
echo "=========================================="

# 检查命令是否存在
if ! command -v perf &>/dev/null; then
    echo "❌ perf 命令未找到，请先安装"
    exit 1
fi

echo "✅ perf 已安装"
echo ""

# 运行命令并展示输出（使用 localhost / 示例目标）
echo "--- perf 基本用法 ---"
# 请根据实际工具修改以下命令
case "perf" in
    dig)
        perf +short localhost A || true
        perf +short example.com NS || true
        ;;
    nslookup)
        perf localhost || true
        perf example.com || true
        ;;
    traceroute)
        perf -I -m 5 example.com || true
        ;;
    nc)
        echo "测试本地 22 端口连通性..."
        timeout 3 perf -zv localhost 22 || echo "端口未开放或超时"
        ;;
    netstat)
        perf -tlnp || true
        ;;
    lsof)
        perf -i :22 || true
        ;;
    ifconfig|ip)
        perf || true
        ;;
    htop|top|iotop|tsar)
        echo "perf 为交互式工具，请手动运行: perf"
        perf -v 2>/dev/null || true
        ;;
    rsync)
        echo "rsync 版本: $(rsync --version | head -n 1)"
        ;;
    *)
        echo "请根据 perf 的实际用法修改本脚本"
        ;;
esac

echo ""
echo "✅ 演示完成"
