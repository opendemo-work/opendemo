#!/bin/bash
# 批量验证 metadata.json 格式
# 检查所有 demo 的 metadata.json 是否符合规范

set -e

echo "========== OpenDemo Metadata 批量验证 =========="
echo ""

TECH_STACKS=("go" "java" "nodejs" "python" "kubernetes" "database" "security" "networking" "ai-ml")

TOTAL_DEMOS=0
PASSED=0
FAILED=0

REQUIRED_FIELDS=("name" "language" "keywords" "description" "difficulty")

for tech in "${TECH_STACKS[@]}"; do
    if [ ! -d "$tech" ]; then
        echo "⚠️  跳过不存在的目录: $tech"
        continue
    fi

    echo "📂 检查 $tech 技术栈..."

    # 遍历所有 demo 目录
    while IFS= read -r -d '' demo_dir; do
        demo_name=$(basename "$demo_dir")
        metadata_file="$demo_dir/metadata.json"

        TOTAL_DEMOS=$((TOTAL_DEMOS + 1))

        if [ ! -f "$metadata_file" ]; then
            echo "  ❌ $demo_name - 缺少 metadata.json"
            FAILED=$((FAILED + 1))
            continue
        fi

        # 检查 JSON 格式
        if ! python3 -c "import json; json.load(open('$metadata_file'))" 2>/dev/null; then
            echo "  ❌ $demo_name - JSON 格式错误"
            FAILED=$((FAILED + 1))
            continue
        fi

        # 检查必需字段
        missing_fields=""
        for field in "${REQUIRED_FIELDS[@]}"; do
            if ! python3 -c "import json; d=json.load(open('$metadata_file')); exit(0 if '$field' in d else 1)" 2>/dev/null; then
                missing_fields="$missing_fields $field"
            fi
        done

        if [ -n "$missing_fields" ]; then
            echo "  ⚠️  $demo_name - 缺少字段:$missing_fields"
            FAILED=$((FAILED + 1))
        else
            echo "  ✅ $demo_name - OK"
            PASSED=$((PASSED + 1))
        fi

    done < <(find "$tech" -mindepth 1 -maxdepth 1 -type d -not -name ".*" -not -name "NAMING_CONVENTIONS.md" -not -name "README.md" -print0)

    echo ""
done

echo "========== 验证结果汇总 =========="
echo "总计: $TOTAL_DEMOS 个 demo"
echo "通过: $PASSED 个"
echo "失败: $FAILED 个"

if [ "$FAILED" -gt 0 ]; then
    exit 1
fi

exit 0