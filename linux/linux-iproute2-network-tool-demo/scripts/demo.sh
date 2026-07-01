#!/usr/bin/env bash
# linux-iproute2-network-tool-demo 演示脚本

set -euo pipefail

echo "=========================================="
echo "ip 演示"
echo "=========================================="

# 检查命令是否存在
if ! command -v ip &>/dev/null; then
    echo "❌ ip 命令未找到，请先安装"
    exit 1
fi

echo "✅ ip 已安装"
echo ""

# 运行命令并展示输出（使用 localhost / 示例目标）
echo "--- ip 基本用法 ---"
# 请根据实际工具修改以下命令
case "ip" in
    dig)
        ip +short localhost A || true
        ip +short example.com NS || true
        ;;
    nslookup)
        ip localhost || true
        ip example.com || true
        ;;
    traceroute)
        ip -I -m 5 example.com || true
        ;;
    nc)
        echo "测试本地 22 端口连通性..."
        timeout 3 ip -zv localhost 22 || echo "端口未开放或超时"
        ;;
    netstat)
        ip -tlnp || true
        ;;
    lsof)
        ip -i :22 || true
        ;;
    ifconfig|ip)
        ip || true
        ;;
    htop|top|iotop|tsar)
        echo "ip 为交互式工具，请手动运行: ip"
        ip -v 2>/dev/null || true
        ;;
    rsync)
        echo "rsync 版本: $(rsync --version | head -n 1)"
        ;;
    *)
        echo "请根据 ip 的实际用法修改本脚本"
        ;;
esac

echo ""
echo "✅ 演示完成"
