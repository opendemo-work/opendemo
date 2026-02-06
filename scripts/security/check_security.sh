#!/bin/bash

echo "🔐 OpenDemo 项目安全检查"
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

# 执行检查
echo -e "\n🔍 检查敏感文件..."
check_file_exists ".env"
check_file_exists ".secrets"
check_file_exists "config/secrets"
check_file_exists "credentials.json"
check_file_exists "private.key"

echo -e "\n📋 检查 .gitignore 配置..."
# 为 git check-ignore 创建测试文件
touch ".env_test" ".secrets_test" "config/secrets_test" "credentials.json_test" "private.key_test" "node_modules_test" ".DS_Store_test" 2>/dev/null

# 检查每个文件是否被忽略
if git check-ignore ".env_test" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ .gitignore 已排除 .env${NC}"
else
    echo -e "${YELLOW}⚠️  警告: .gitignore 未排除 .env${NC}"
    ((WARNING_COUNT++))
fi

if git check-ignore ".secrets_test" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ .gitignore 已排除 .secrets${NC}"
else
    echo -e "${YELLOW}⚠️  警告: .gitignore 未排除 .secrets${NC}"
    ((WARNING_COUNT++))
fi

if git check-ignore "config/secrets_test" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ .gitignore 已排除 config/secrets${NC}"
else
    echo -e "${YELLOW}⚠️  警告: .gitignore 未排除 config/secrets${NC}"
    ((WARNING_COUNT++))
fi

if git check-ignore "credentials.json_test" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ .gitignore 已排除 credentials.json${NC}"
else
    echo -e "${YELLOW}⚠️  警告: .gitignore 未排除 credentials.json${NC}"
    ((WARNING_COUNT++))
fi

if git check-ignore "private.key_test" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ .gitignore 已排除 private.key${NC}"
else
    echo -e "${YELLOW}⚠️  警告: .gitignore 未排除 private.key${NC}"
    ((WARNING_COUNT++))
fi

if git check-ignore "node_modules_test" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ .gitignore 已排除 node_modules${NC}"
else
    echo -e "${YELLOW}⚠️  警告: .gitignore 未排除 node_modules${NC}"
    ((WARNING_COUNT++))
fi

if git check-ignore ".DS_Store_test" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ .gitignore 已排除 .DS_Store${NC}"
else
    echo -e "${YELLOW}⚠️  警告: .gitignore 未排除 .DS_Store${NC}"
    ((WARNING_COUNT++))
fi

# 清理测试文件
rm -f ".env_test" ".secrets_test" "config/secrets_test" "credentials.json_test" "private.key_test" "node_modules_test" ".DS_Store_test" 2>/dev/null

# 检查最近的 Git 提交
echo -e "\n📚 检查 Git 历史..."
RECENT_COMMITS=$(git log --oneline -10 2>/dev/null | wc -l)
if [ $RECENT_COMMITS -gt 0 ]; then
    echo -e "${GREEN}✅ 发现 $RECENT_COMMITS 个近期提交${NC}"
    # 检查是否有敏感词
    SENSITIVE_COMMITS=$(git log --all --grep -i "password\|secret\|token\|key\|credential" --oneline 2>/dev/null | wc -l)
    if [ $SENSITIVE_COMMITS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  警告: 发现 $SENSITIVE_COMMITS 个可能包含敏感信息的提交${NC}"
        ((WARNING_COUNT++))
    fi
else
    echo -e "${YELLOW}⚠️  警告: 未检测到 Git 提交历史${NC}"
    ((WARNING_COUNT++))
fi

# 检查代码中的潜在敏感信息
echo -e "\n🔍 检查代码中的敏感信息..."
# 检查常见的敏感信息模式
SENSITIVE_IN_CODE=$(grep -r --include="*.py" --include="*.js" --include="*.go" --include="*.java" --include="*.sh" -i "password\s*=\|secret\s*=\|token\s*=\|api_key\s*=\|access_key\s*=" . 2>/dev/null | grep -v ".git" | wc -l)
if [ $SENSITIVE_IN_CODE -gt 0 ]; then
    echo -e "${YELLOW}⚠️  警告: 发现 $SENSITIVE_IN_CODE 处可能的硬编码敏感信息${NC}"
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
    # 警告不阻止提交，但给出提示
    exit 0
else
    echo -e "${RED}❌ 存在安全风险，请立即处理${NC}"
    exit 1
fi