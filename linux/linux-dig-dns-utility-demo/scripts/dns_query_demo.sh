#!/usr/bin/env bash
# 风险等级：🟡 中风险
# 说明：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
# 生产安全提示：
#   - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
#   - 注意检查依赖版本、端口占用和目标资源配置。
#   - 生产环境执行前请经过变更评审和备份确认。

# DNS 查询综合演示脚本
# 使用 dig 命令演示基础、高级和批量 DNS 查询

set -euo pipefail

# 默认查询域名（ICANN 保留的示例域名，可安全用于测试）
DOMAIN="${1:-example.com}"
# 默认 DNS 服务器（Cloudflare 公共 DNS）
DNS_SERVER="${2:-1.1.1.1}"

echo "=========================================="
echo "Linux dig DNS 查询演示"
echo "目标域名: $DOMAIN"
echo "DNS 服务器: $DNS_SERVER"
echo "=========================================="

# 检查 dig 命令
if ! command -v dig &>/dev/null; then
    echo "❌ dig 命令未找到。请安装:"
    echo "   Ubuntu/Debian: sudo apt-get install dnsutils"
    echo "   CentOS/RHEL:   sudo yum install bind-utils"
    echo "   macOS:         brew install bind"
    exit 1
fi

echo ""
echo "✅ dig 命令已安装: $(dig -v 2>&1 | head -n 1)"
echo ""

# 1. 基础 A 记录查询
echo "--- 1. 基础 A 记录查询 ---"
dig +short "$DOMAIN" A || true
echo ""

# 2. 查询指定 DNS 服务器
echo "--- 2. 通过 $DNS_SERVER 查询 NS 记录 ---"
dig +short "$DOMAIN" NS @"$DNS_SERVER" || true
echo ""

# 3. 查询 MX 记录
echo "--- 3. MX 记录查询 ---"
dig +short "$DOMAIN" MX || true
echo ""

# 4. 查询 TXT 记录
echo "--- 4. TXT 记录查询 ---"
dig +short "$DOMAIN" TXT || true
echo ""

# 5. 反向 DNS 查询（仅当 A 记录解析出 IP 时）
echo "--- 5. 反向 DNS 查询 ---"
IP=$(dig +short "$DOMAIN" A | head -n 1 || true)
if [[ -n "$IP" ]]; then
    dig +short -x "$IP" || true
else
    echo "(无法获取 $DOMAIN 的 IP，跳过反向查询)"
fi
echo ""

# 6. 简洁输出模式
echo "--- 6. 简洁输出模式 (+short) ---"
dig +short "$DOMAIN" A || true
echo ""

# 7. 显示查询统计
echo "--- 7. 查询统计 (+stats) ---"
dig +stats "$DOMAIN" A | grep -E "Query time|SERVER|WHEN" || true
echo ""

echo "✅ 演示完成"
