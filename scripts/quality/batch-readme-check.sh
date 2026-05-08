#!/bin/bash
# 批量检查 README 格式
# 检查所有 demo 的 README.md 是否符合质量标准

set -e

echo "========== OpenDemo README 批量检查 =========="
echo ""

# 检查目录
TECH_STACKS=("go" "java" "nodejs" "python" "kubernetes" "database" "security" "networking" "ai-ml")

TOTAL_DEMOS=0
PASSED=0
FAILED=0

for tech in "${TECH_STACKS[@]}"; do
    if [ ! -d "$tech" ]; then
        echo "⚠️  跳过不存在的目录: $tech"
        continue
    fi

    echo "📂 检查 $tech 技术栈..."

    # 遍历所有 demo 目录
    while IFS= read -r -d '' demo_dir; do
        demo_name=$(basename "$demo_dir")
        readme_file="$demo_dir/README.md"

        TOTAL_DEMOS=$((TOTAL_DEMOS + 1))

        if [ ! -f "$readme_file" ]; then
            echo "  ❌ $demo_name - 缺少 README.md"
            FAILED=$((FAILED + 1))
            continue
        fi

        # 检查 README 字数（标准：≥3000 字符）
        char_count=$(wc -c < "$readme_file")

        if [ "$char_count" -lt 3000 ]; then
            echo "  ⚠️  $demo_name - README 过短 ($char_count 字符)"
            FAILED=$((FAILED + 1))
        else
            echo "  ✅ $demo_name - OK ($char_count 字符)"
            PASSED=$((PASSED + 1))
        fi

    done < <(find "$tech" -mindepth 1 -maxdepth 1 -type d -not -name ".*" -not -name "NAMING_CONVENTIONS.md" -not -name "README.md" -print0)

    echo ""
done

echo "========== 检查结果汇总 =========="
echo "总计: $TOTAL_DEMOS 个 demo"
echo "通过: $PASSED 个"
echo "失败: $FAILED 个"

if [ "$FAILED" -gt 0 ]; then
    echo ""
    echo "失败率为: $(echo "scale=2; $FAILED * 100 / $TOTAL_DEMOS" | bc)%"
    exit 1
fi

exit 0