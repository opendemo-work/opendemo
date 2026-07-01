#!/usr/bin/env bash
# linux-common-monitoring-commands-demo 演示脚本

set -euo pipefail

echo "=========================================="
echo "vmstat 演示"
echo "=========================================="

# 检查命令是否存在
if ! command -v vmstat &>/dev/null; then
    echo "❌ vmstat 命令未找到，请先安装"
    exit 1
fi

echo "✅ vmstat 已安装"
echo ""

# 运行命令并展示输出（使用 localhost / 示例目标）
echo "--- vmstat 基本用法 ---"
# 请根据实际工具修改以下命令
case "vmstat" in
    dig)
        vmstat +short localhost A || true
        vmstat +short example.com NS || true
        ;;
    nslookup)
        vmstat localhost || true
        vmstat example.com || true
        ;;
    traceroute)
        vmstat -I -m 5 example.com || true
        ;;
    nc)
        echo "测试本地 22 端口连通性..."
        timeout 3 vmstat -zv localhost 22 || echo "端口未开放或超时"
        ;;
    netstat)
        vmstat -tlnp || true
        ;;
    lsof)
        vmstat -i :22 || true
        ;;
    ifconfig|ip)
        vmstat || true
        ;;
    htop|top|iotop|tsar)
        echo "vmstat 为交互式工具，请手动运行: vmstat"
        vmstat -v 2>/dev/null || true
        ;;
    rsync)
        echo "rsync 版本: $(rsync --version | head -n 1)"
        ;;
    *)
        echo "请根据 vmstat 的实际用法修改本脚本"
        ;;
esac

echo ""
echo "✅ 演示完成"
