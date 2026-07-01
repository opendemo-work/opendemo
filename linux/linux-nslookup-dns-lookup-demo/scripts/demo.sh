#!/usr/bin/env bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

# linux-nslookup-dns-lookup-demo 演示脚本

set -euo pipefail

echo "=========================================="
echo "nslookup 演示"
echo "=========================================="

# 检查命令是否存在
if ! command -v nslookup &>/dev/null; then
    echo "❌ nslookup 命令未找到，请先安装"
    exit 1
fi

echo "✅ nslookup 已安装"
echo ""

# 运行命令并展示输出（使用 localhost / 示例目标）
echo "--- nslookup 基本用法 ---"
# 请根据实际工具修改以下命令
case "nslookup" in
    dig)
        nslookup +short localhost A || true
        nslookup +short example.com NS || true
        ;;
    nslookup)
        nslookup localhost || true
        nslookup example.com || true
        ;;
    traceroute)
        nslookup -I -m 5 example.com || true
        ;;
    nc)
        echo "测试本地 22 端口连通性..."
        timeout 3 nslookup -zv localhost 22 || echo "端口未开放或超时"
        ;;
    netstat)
        nslookup -tlnp || true
        ;;
    lsof)
        nslookup -i :22 || true
        ;;
    ifconfig|ip)
        nslookup || true
        ;;
    htop|top|iotop|tsar)
        echo "nslookup 为交互式工具，请手动运行: nslookup"
        nslookup -v 2>/dev/null || true
        ;;
    rsync)
        echo "rsync 版本: $(rsync --version | head -n 1)"
        ;;
    *)
        echo "请根据 nslookup 的实际用法修改本脚本"
        ;;
esac

echo ""
echo "✅ 演示完成"
