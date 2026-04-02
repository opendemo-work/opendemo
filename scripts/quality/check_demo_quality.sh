#!/bin/bash

# OpenDemo 案例质量检查脚本
# 用于检查各个案例的质量指标

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 计数器
TOTAL_DEMOS=0
HAS_README=0
HAS_CODE=0
HAS_TESTS=0
HAS_METADATA=0
QUALITY_ISSUES=0

# 技术栈目录
TECH_STACKS=("go" "nodejs" "python" "java" "kubernetes" "database" "linux" "container" "ai-ml" "monitoring" "messaging" "traffic")

echo "🔍 OpenDemo 案例质量检查"
echo "=========================="
echo ""

# 检查单个案例目录
check_demo() {
    local demo_dir=$1
    local demo_name=$(basename "$demo_dir")
    local issues=0
    
    TOTAL_DEMOS=$((TOTAL_DEMOS + 1))
    
    # 检查 README.md
    if [ -f "$demo_dir/README.md" ]; then
        HAS_README=$((HAS_README + 1))
        readme_lines=$(wc -l < "$demo_dir/README.md")
        if [ "$readme_lines" -lt 10 ]; then
            echo -e "${YELLOW}⚠️  $demo_name: README 内容过少 (${readme_lines} 行)${NC}"
            issues=$((issues + 1))
        fi
    else
        echo -e "${RED}❌ $demo_name: 缺少 README.md${NC}"
        issues=$((issues + 1))
    fi
    
    # 检查代码文件
    local code_count=$(find "$demo_dir" -type f \( -name "*.go" -o -name "*.js" -o -name "*.py" -o -name "*.java" -o -name "*.sh" -o -name "*.yaml" -o -name "*.yml" \) 2>/dev/null | wc -l)
    if [ "$code_count" -gt 0 ]; then
        HAS_CODE=$((HAS_CODE + 1))
    else
        echo -e "${YELLOW}⚠️  $demo_name: 未找到代码文件${NC}"
        issues=$((issues + 1))
    fi
    
    # 检查测试文件
    local test_count=$(find "$demo_dir" -type f \( -name "*_test.go" -o -name "*.test.js" -o -name "test_*.py" -o -name "*Test.java" \) 2>/dev/null | wc -l)
    if [ "$test_count" -gt 0 ]; then
        HAS_TESTS=$((HAS_TESTS + 1))
    fi
    
    # 检查 metadata.json
    if [ -f "$demo_dir/metadata.json" ]; then
        HAS_METADATA=$((HAS_METADATA + 1))
    fi
    
    QUALITY_ISSUES=$((QUALITY_ISSUES + issues))
    return $issues
}

# 遍历每个技术栈
for stack in "${TECH_STACKS[@]}"; do
    if [ -d "$stack" ]; then
        echo -e "${BLUE}📁 检查技术栈: $stack${NC}"
        
        # 遍历该栈下的每个案例
        find "$stack" -maxdepth 1 -type d | tail -n +2 | while read demo; do
            check_demo "$demo"
        done
    fi
done

echo ""
echo "📊 质量检查报告"
echo "================"
echo ""
echo "统计信息:"
echo "  案例总数: $TOTAL_DEMOS"
echo "  有 README: $HAS_README ($(( HAS_README * 100 / TOTAL_DEMOS ))%)"
echo "  有代码文件: $HAS_CODE ($(( HAS_CODE * 100 / TOTAL_DEMOS ))%)"
echo "  有测试文件: $HAS_TESTS ($(( HAS_TESTS * 100 / TOTAL_DEMOS ))%)"
echo "  有元数据: $HAS_METADATA ($(( HAS_METADATA * 100 / TOTAL_DEMOS ))%)"
echo ""

# 计算质量评分
QUALITY_SCORE=100
if [ "$HAS_README" -lt "$TOTAL_DEMOS" ]; then
    QUALITY_SCORE=$((QUALITY_SCORE - 20))
fi
if [ "$HAS_TESTS" -lt "$(( TOTAL_DEMOS / 4 ))" ]; then
    QUALITY_SCORE=$((QUALITY_SCORE - 20))
fi
if [ "$QUALITY_ISSUES" -gt 10 ]; then
    QUALITY_SCORE=$((QUALITY_SCORE - 10))
fi

echo "质量评分: $QUALITY_SCORE/100"
echo ""

if [ "$QUALITY_SCORE" -ge 80 ]; then
    echo -e "${GREEN}✅ 案例质量良好${NC}"
elif [ "$QUALITY_SCORE" -ge 60 ]; then
    echo -e "${YELLOW}⚠️  案例质量一般，需要改进${NC}"
else
    echo -e "${RED}❌ 案例质量较差，需要全面改进${NC}"
fi

echo ""
echo "改进建议:"
if [ "$HAS_README" -lt "$TOTAL_DEMOS" ]; then
    echo "  - 为缺少 README 的案例添加文档"
fi
if [ "$HAS_TESTS" -lt "$(( TOTAL_DEMOS / 2 ))" ]; then
    echo "  - 增加测试覆盖，目标: 50% 案例有测试"
fi
if [ "$HAS_METADATA" -lt "$TOTAL_DEMOS" ]; then
    echo "  - 为案例添加 metadata.json 文件"
fi

exit 0
