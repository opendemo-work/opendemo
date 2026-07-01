#!/bin/bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

# 跨技术栈索引生成脚本
# 生成 CROSS-TECH-INDEX.md 跨技术栈索引文件

set -e

OUTPUT_FILE="docs/CROSS-TECH-INDEX.md"
TECH_STACKS=("go" "java" "nodejs" "python" "kubernetes" "database" "security" "networking" "ai-ml" "linux" "sre")

echo "========== OpenDemo 跨技术栈索引生成 =========="
echo ""

# 开始生成 Markdown
{
    echo "# 跨技术栈索引"
    echo ""
    echo "> 最后更新: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "---"
    echo ""

    for tech in "${TECH_STACKS[@]}"; do
        if [ ! -d "$tech" ]; then
            continue
        fi

        echo "## $tech"
        echo ""

        # 读取技术栈 README 描述
        if [ -f "$tech/README.md" ]; then
            # 获取第一个 H1 标题
            title=$(grep -m1 "^# " "$tech/README.md" | sed 's/^# //')
            if [ -n "$title" ]; then
                echo "**$title**"
                echo ""
            fi
        fi

        echo "| Demo | 描述 | 难度 |"
        echo "|------|------|------|"

        # 遍历所有 demo
        while IFS= read -r -d '' demo_dir; do
            demo_name=$(basename "$demo_dir")

            # 默认值
            description=""
            difficulty="-"

            # 尝试从 metadata.json 读取
            metadata_file="$demo_dir/metadata.json"
            if [ -f "$metadata_file" ]; then
                description=$(python3 -c "import json; d=json.load(open('$metadata_file')); print(d.get('description', ''))" 2>/dev/null || echo "")
                difficulty=$(python3 -c "import json; d=json.load(open('$metadata_file')); print(d.get('difficulty', '-'))" 2>/dev/null || echo "-")
            fi

            # 截断过长的描述
            if [ ${#description} -gt 60 ]; then
                description="${description:0:57}..."
            fi

            echo "| [$demo_name](../$tech/$demo_name) | $description | $difficulty |"

        done < <(find "$tech" -mindepth 1 -maxdepth 1 -type d -not -name ".*" -not -name "NAMING_CONVENTIONS.md" -not -name "README.md" -not -name "metadata.json" -print0 | sort)

        echo ""
    done

    echo "---"
    echo ""
    echo "*本索引由脚本自动生成*"

} > "$OUTPUT_FILE"

echo "✅ 索引已生成: $OUTPUT_FILE"
echo ""
echo "共计 $(find "${TECH_STACKS[@]}" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ') 个 demo"
