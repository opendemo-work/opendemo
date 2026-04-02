#!/bin/bash

# OpenDemo 质量检查脚本
# 用于检查案例的文档完整性和质量

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
TOTAL_DIRS=0
HAS_README=0
HAS_METADATA=0
HAS_POM=0
MISSING_README=()
MISSING_METADATA=()

# 技术栈列表
TECH_STACKS=("java" "python" "go" "nodejs" "database" "kubernetes" "traffic" "ai-ml" "linux" "messaging" "container" "monitoring")

echo "=========================================="
echo "OpenDemo 质量检查报告"
echo "时间: $(date)"
echo "=========================================="
echo ""

# 检查每个技术栈
for stack in "${TECH_STACKS[@]}"; do
    if [ -d "$stack" ]; then
        echo "检查技术栈: $stack"
        
        stack_total=0
        stack_readme=0
        stack_metadata=0
        
        for dir in "$stack"/*/; do
            # 跳过cli目录和非目录文件
            if [[ "$(basename "$dir")" == "cli" ]] || [[ ! -d "$dir" ]]; then
                continue
            fi
            
            stack_total=$((stack_total + 1))
            TOTAL_DIRS=$((TOTAL_DIRS + 1))
            
            # 检查README.md
            if [ -f "$dir/README.md" ]; then
                HAS_README=$((HAS_README + 1))
                stack_readme=$((stack_readme + 1))
                
                # 检查README大小
                readme_size=$(stat -f%z "$dir/README.md" 2>/dev/null || stat -c%s "$dir/README.md" 2>/dev/null || echo "0")
                if [ "$readme_size" -lt 500 ]; then
                    echo -e "${YELLOW}警告: $dir README.md 小于500字节 ($readme_size)${NC}"
                fi
            else
                MISSING_README+=("$dir")
            fi
            
            # 检查metadata.json
            if [ -f "$dir/metadata.json" ]; then
                HAS_METADATA=$((HAS_METADATA + 1))
                stack_metadata=$((stack_metadata + 1))
                
                # 验证JSON格式
                if ! jq empty "$dir/metadata.json" 2>/dev/null; then
                    echo -e "${RED}错误: $dir metadata.json JSON格式无效${NC}"
                fi
            else
                MISSING_METADATA+=("$dir")
            fi
            
            # 检查pom.xml或build.gradle（Java/Go项目）
            if [ "$stack" == "java" ]; then
                if [ -f "$dir/pom.xml" ] || [ -f "$dir/build.gradle" ]; then
                    HAS_POM=$((HAS_POM + 1))
                fi
            fi
        done
        
        # 输出技术栈统计
        if [ $stack_total -gt 0 ]; then
            readme_pct=$((stack_readme * 100 / stack_total))
            metadata_pct=$((stack_metadata * 100 / stack_total))
            
            echo "  案例总数: $stack_total"
            echo "  README: $stack_readme/$stack_total (${readme_pct}%)"
            echo "  metadata.json: $stack_metadata/$stack_total (${metadata_pct}%)"
            echo ""
        fi
    fi
done

echo "=========================================="
echo "总体统计"
echo "=========================================="
echo "案例总数: $TOTAL_DIRS"
echo ""

if [ $TOTAL_DIRS -gt 0 ]; then
    readme_total_pct=$((HAS_README * 100 / TOTAL_DIRS))
    metadata_total_pct=$((HAS_METADATA * 100 / TOTAL_DIRS))
    
    echo -e "README覆盖率: ${HAS_README}/${TOTAL_DIRS} (${readme_total_pct}%)"
    if [ $readme_total_pct -ge 90 ]; then
        echo -e "${GREEN}✓ README覆盖率达标${NC}"
    else
        echo -e "${RED}✗ README覆盖率不达标 (目标: 90%)${NC}"
    fi
    
    echo ""
    echo -e "metadata.json覆盖率: ${HAS_METADATA}/${TOTAL_DIRS} (${metadata_total_pct}%)"
    if [ $metadata_total_pct -ge 90 ]; then
        echo -e "${GREEN}✓ metadata.json覆盖率达标${NC}"
    else
        echo -e "${RED}✗ metadata.json覆盖率不达标 (目标: 90%)${NC}"
    fi
fi

echo ""
echo "=========================================="
echo "缺失详情"
echo "=========================================="

if [ ${#MISSING_README[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}缺失 README.md 的案例 (${#MISSING_README[@]}个):${NC}"
    for dir in "${MISSING_README[@]:0:10}"; do
        echo "  - $dir"
    done
    if [ ${#MISSING_README[@]} -gt 10 ]; then
        echo "  ... 还有 $(( ${#MISSING_README[@]} - 10 )) 个"
    fi
fi

if [ ${#MISSING_METADATA[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}缺失 metadata.json 的案例 (${#MISSING_METADATA[@]}个):${NC}"
    for dir in "${MISSING_METADATA[@]:0:10}"; do
        echo "  - $dir"
    done
    if [ ${#MISSING_METADATA[@]} -gt 10 ]; then
        echo "  ... 还有 $(( ${#MISSING_METADATA[@]} - 10 )) 个"
    fi
fi

echo ""
echo "=========================================="
echo "建议行动"
echo "=========================================="

if [ ${#MISSING_README[@]} -gt 0 ]; then
    echo "1. 优先补齐缺失的README.md (${#MISSING_README[@]}个)"
fi

if [ ${#MISSING_METADATA[@]} -gt 0 ]; then
    echo "2. 补齐metadata.json (${#MISSING_METADATA[@]}个)"
fi

if [ $HAS_POM -lt $((TOTAL_DIRS / 2)) ]; then
    echo "3. Java案例需要添加pom.xml或build.gradle"
fi

echo ""
echo "检查完成!"
