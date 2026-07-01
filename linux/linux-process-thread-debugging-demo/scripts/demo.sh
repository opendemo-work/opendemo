#!/usr/bin/env bash
# linux-process-thread-debugging-demo 演示脚本

set -euo pipefail

echo "=========================================="
echo "pstree 演示"
echo "=========================================="

# 检查命令是否存在
if ! command -v pstree &>/dev/null; then
    echo "❌ pstree 命令未找到，请先安装"
    exit 1
fi

echo "✅ pstree 已安装"
echo ""

# 运行命令并展示输出（使用 localhost / 示例目标）
echo "--- pstree 基本用法 ---"
# 请根据实际工具修改以下命令
case "pstree" in
    dig)
        pstree +short localhost A || true
        pstree +short example.com NS || true
        ;;
    nslookup)
        pstree localhost || true
        pstree example.com || true
        ;;
    traceroute)
        pstree -I -m 5 example.com || true
        ;;
    nc)
        echo "测试本地 22 端口连通性..."
        timeout 3 pstree -zv localhost 22 || echo "端口未开放或超时"
        ;;
    netstat)
        pstree -tlnp || true
        ;;
    lsof)
        pstree -i :22 || true
        ;;
    ifconfig|ip)
        pstree || true
        ;;
    htop|top|iotop|tsar)
        echo "pstree 为交互式工具，请手动运行: pstree"
        pstree -v 2>/dev/null || true
        ;;
    rsync)
        echo "rsync 版本: $(rsync --version | head -n 1)"
        ;;
    *)
        echo "请根据 pstree 的实际用法修改本脚本"
        ;;
esac

echo ""
echo "✅ 演示完成"
