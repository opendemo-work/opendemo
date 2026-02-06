#!/bin/bash

echo "🔐 OpenDemo 安全检查工具"
echo "========================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERROR_COUNT=0
WARNING_COUNT=0

# 检查函数
check_file_exists() {
    if [ -f "$1" ]; then
        echo -e "${RED}❌ 危险: 发现敏感文件 $1${NC}"
        ((ERROR_COUNT++))
        return 1
    else
        echo -e "${GREEN}✅ 安全: 未发现 $1${NC}"
        return 0
    fi
}

check_pattern_in_gitignore() {
    if grep -q "$1" .gitignore 2>/dev/null; then
        echo -e "${GREEN}✅ .gitignore 已排除 $1${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  警告: .gitignore 未排除 $1${NC}"
        ((WARNING_COUNT++))
        return 1
    fi
}

# 执行检查
echo -e "\n🔍 检查敏感文件..."
check_file_exists ".env"
check_file_exists ".secrets"
check_file_exists "config/secrets"

echo -e "\n📋 检查 .gitignore 配置..."
check_pattern_in_gitignore "\.env"
check_pattern_in_gitignore "\.secrets"
check_pattern_in_gitignore "config/secrets"

# 检查最近的 Git 提交
echo -e "\n📚 检查 Git 历史..."
RECENT_COMMITS=$(git log --oneline -10 2>/dev/null | wc -l)
if [ $RECENT_COMMITS -gt 0 ]; then
    echo -e "${GREEN}✅ 发现 $RECENT_COMMITS 个近期提交${NC}"
    # 检查是否有敏感词
    SENSITIVE_COMMITS=$(git log --all --grep -i "password\|secret\|token\|key" --oneline 2>/dev/null | wc -l)
    if [ $SENSITIVE_COMMITS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  警告: 发现 $SENSITIVE_COMMITS 个可能包含敏感信息的提交${NC}"
        ((WARNING_COUNT++))
    fi
else
    echo -e "${YELLOW}⚠️  警告: 未检测到 Git 提交历史${NC}"
    ((WARNING_COUNT++))
fi

# 最终报告
echo -e "\n📊 安全检查报告:"
echo "================"
echo "严重错误: $ERROR_COUNT 项"
echo "警告事项: $WARNING_COUNT 项"

if [ $ERROR_COUNT -eq 0 ] && [ $WARNING_COUNT -eq 0 ]; then
    echo -e "${GREEN}🎉 所有安全检查通过！${NC}"
    exit 0
elif [ $ERROR_COUNT -eq 0 ]; then
    echo -e "${YELLOW}⚠️  存在警告，请关注建议事项${NC}"
    exit 1
else
    echo -e "${RED}❌ 存在安全风险，请立即处理${NC}"
    exit 2
fi