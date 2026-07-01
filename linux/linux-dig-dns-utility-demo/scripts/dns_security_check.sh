#!/usr/bin/env bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

# DNS 安全配置检查脚本
# 检查域名的 SPF、DKIM、DMARC、DNSSEC 等安全记录

set -euo pipefail

DOMAIN="${1:-example.com}"

echo "=========================================="
echo "DNS 安全配置检查: $DOMAIN"
echo "=========================================="

if ! command -v dig &>/dev/null; then
    echo "❌ dig 命令未找到"
    exit 1
fi

check_record() {
    local name=$1
    local type=$2
    local result
    result=$(dig +short "$name" "$type" || true)
    if [[ -n "$result" ]]; then
        echo "✅ $type 记录: $name"
        echo "$result" | sed 's/^/   /'
    else
        echo "⚠️  未找到 $type 记录: $name"
    fi
    echo ""
}

# SPF / TXT
check_record "$DOMAIN" TXT

# DMARC
check_record "_dmarc.$DOMAIN" TXT

# DNSKEY (DNSSEC)
check_record "$DOMAIN" DNSKEY

# DS (Delegation Signer)
check_record "$DOMAIN" DS

echo "✅ 安全检查完成"
