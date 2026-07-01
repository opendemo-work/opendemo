#!/usr/bin/env bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

# 批量 DNS 查询脚本
# 从 domains.txt 读取域名列表，批量查询 A/MX/NS/TXT 记录

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOMAINS_FILE="${1:-$SCRIPT_DIR/../config/domains.txt}"

echo "=========================================="
echo "批量 DNS 查询"
echo "域名列表: $DOMAINS_FILE"
echo "=========================================="

if ! command -v dig &>/dev/null; then
    echo "❌ dig 命令未找到"
    exit 1
fi

if [[ ! -f "$DOMAINS_FILE" ]]; then
    echo "⚠️  域名列表文件不存在: $DOMAINS_FILE"
    echo "使用默认测试域名: example.com github.com"
    DOMAINS=("example.com" "github.com")
else
    mapfile -t DOMAINS < <(grep -v '^#' "$DOMAINS_FILE" | grep -v '^$')
fi

for domain in "${DOMAINS[@]}"; do
    echo ""
    echo "=== $domain ==="
    for type in A MX NS TXT; do
        result=$(dig +short "$domain" "$type" 2>/dev/null || true)
        if [[ -n "$result" ]]; then
            echo "[$type]"
            echo "$result" | sed 's/^/  /'
        fi
    done
done

echo ""
echo "✅ 批量查询完成"
