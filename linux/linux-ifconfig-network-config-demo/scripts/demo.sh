#!/usr/bin/env bash
# linux-ifconfig-network-config-demo 演示脚本

set -euo pipefail

echo "=========================================="
echo "ifconfig 演示"
echo "=========================================="

# 检查命令是否存在
if ! command -v ifconfig &>/dev/null; then
    echo "❌ ifconfig 命令未找到，请先安装"
    exit 1
fi

echo "✅ ifconfig 已安装"
echo ""

# 运行命令并展示输出（使用 localhost / 示例目标）
echo "--- ifconfig 基本用法 ---"
# 请根据实际工具修改以下命令
case "ifconfig" in
    dig)
        ifconfig +short localhost A || true
        ifconfig +short example.com NS || true
        ;;
    nslookup)
        ifconfig localhost || true
        ifconfig example.com || true
        ;;
    traceroute)
        ifconfig -I -m 5 example.com || true
        ;;
    nc)
        echo "测试本地 22 端口连通性..."
        timeout 3 ifconfig -zv localhost 22 || echo "端口未开放或超时"
        ;;
    netstat)
        ifconfig -tlnp || true
        ;;
    lsof)
        ifconfig -i :22 || true
        ;;
    ifconfig|ip)
        ifconfig || true
        ;;
    htop|top|iotop|tsar)
        echo "ifconfig 为交互式工具，请手动运行: ifconfig"
        ifconfig -v 2>/dev/null || true
        ;;
    rsync)
        echo "rsync 版本: $(rsync --version | head -n 1)"
        ;;
    *)
        echo "请根据 ifconfig 的实际用法修改本脚本"
        ;;
esac

echo ""
echo "✅ 演示完成"
