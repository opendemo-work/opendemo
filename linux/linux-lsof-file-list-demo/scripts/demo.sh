#!/usr/bin/env bash
# linux-lsof-file-list-demo 演示脚本

set -euo pipefail

echo "=========================================="
echo "lsof 演示"
echo "=========================================="

# 检查命令是否存在
if ! command -v lsof &>/dev/null; then
    echo "❌ lsof 命令未找到，请先安装"
    exit 1
fi

echo "✅ lsof 已安装"
echo ""

# 运行命令并展示输出（使用 localhost / 示例目标）
echo "--- lsof 基本用法 ---"
# 请根据实际工具修改以下命令
case "lsof" in
    dig)
        lsof +short localhost A || true
        lsof +short example.com NS || true
        ;;
    nslookup)
        lsof localhost || true
        lsof example.com || true
        ;;
    traceroute)
        lsof -I -m 5 example.com || true
        ;;
    nc)
        echo "测试本地 22 端口连通性..."
        timeout 3 lsof -zv localhost 22 || echo "端口未开放或超时"
        ;;
    netstat)
        lsof -tlnp || true
        ;;
    lsof)
        lsof -i :22 || true
        ;;
    ifconfig|ip)
        lsof || true
        ;;
    htop|top|iotop|tsar)
        echo "lsof 为交互式工具，请手动运行: lsof"
        lsof -v 2>/dev/null || true
        ;;
    rsync)
        echo "rsync 版本: $(rsync --version | head -n 1)"
        ;;
    *)
        echo "请根据 lsof 的实际用法修改本脚本"
        ;;
esac

echo ""
echo "✅ 演示完成"
