#!/bin/bash

# OpenDemo 代码质量门禁脚本
# 在提交前运行，检查代码质量

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 计数器
ERRORS=0
WARNINGS=0

echo "🔍 OpenDemo 代码质量门禁"
echo "========================="
echo ""

# 检查命令是否存在
command_exists() {
    command -v "$1" &> /dev/null
}

# Python 代码质量检查
check_python() {
    echo -e "${BLUE}📦 检查 Python 代码...${NC}"
    
    if ! command_exists python3; then
        echo -e "${YELLOW}⚠️  Python3 未安装，跳过 Python 检查${NC}"
        return
    fi
    
    # 检查 Black
    if command_exists black; then
        echo "  运行 Black 格式检查..."
        if ! black --check opendemo-cli/ python/ 2>/dev/null; then
            echo -e "${YELLOW}  ⚠️  Python 代码格式不符合 Black 规范${NC}"
            echo "     运行 'black opendemo-cli/ python/' 修复"
            WARNINGS=$((WARNINGS + 1))
        else
            echo -e "${GREEN}  ✅ Black 检查通过${NC}"
        fi
    else
        echo -e "${YELLOW}  ⚠️  Black 未安装${NC}"
    fi
    
    # 检查 Flake8
    if command_exists flake8; then
        echo "  运行 Flake8 代码检查..."
        FLAKE8_ERRORS=$(flake8 opendemo-cli/ python/ --count 2>/dev/null || true)
        if [ "$FLAKE8_ERRORS" -gt 0 ]; then
            echo -e "${YELLOW}  ⚠️  发现 $FLAKE8_ERRORS 个 Flake8 警告${NC}"
            WARNINGS=$((WARNINGS + 1))
        else
            echo -e "${GREEN}  ✅ Flake8 检查通过${NC}"
        fi
    fi
    
    echo ""
}

# Go 代码质量检查
check_go() {
    echo -e "${BLUE}🐹 检查 Go 代码...${NC}"
    
    if ! command_exists go; then
        echo -e "${YELLOW}⚠️  Go 未安装，跳过 Go 检查${NC}"
        return
    fi
    
    # 检查 gofmt
    echo "  运行 gofmt 格式检查..."
    UNFORMATTED=$(gofmt -l go/ 2>/dev/null | wc -l)
    if [ "$UNFORMATTED" -gt 0 ]; then
        echo -e "${YELLOW}  ⚠️  发现 $UNFORMATTED 个文件格式不正确${NC}"
        echo "     运行 'gofmt -w go/' 修复"
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${GREEN}  ✅ gofmt 检查通过${NC}"
    fi
    
    # 检查 golangci-lint
    if command_exists golangci-lint; then
        echo "  运行 golangci-lint..."
        if ! golangci-lint run ./go/... 2>/dev/null; then
            echo -e "${YELLOW}  ⚠️  golangci-lint 发现问题${NC}"
            WARNINGS=$((WARNINGS + 1))
        else
            echo -e "${GREEN}  ✅ golangci-lint 检查通过${NC}"
        fi
    else
        echo -e "${YELLOW}  ⚠️  golangci-lint 未安装${NC}"
    fi
    
    echo ""
}

# Node.js 代码质量检查
check_nodejs() {
    echo -e "${BLUE}🟢 检查 Node.js 代码...${NC}"
    
    if ! command_exists node; then
        echo -e "${YELLOW}⚠️  Node.js 未安装，跳过 Node.js 检查${NC}"
        return
    fi
    
    # 检查 ESLint
    if command_exists eslint; then
        echo "  运行 ESLint..."
        if ! eslint nodejs/ 2>/dev/null; then
            echo -e "${YELLOW}  ⚠️  ESLint 发现问题${NC}"
            WARNINGS=$((WARNINGS + 1))
        else
            echo -e "${GREEN}  ✅ ESLint 检查通过${NC}"
        fi
    else
        echo -e "${YELLOW}  ⚠️  ESLint 未安装${NC}"
    fi
    
    echo ""
}

# Java 代码质量检查
check_java() {
    echo -e "${BLUE}☕ 检查 Java 代码...${NC}"
    
    if ! command_exists java; then
        echo -e "${YELLOW}⚠️  Java 未安装，跳过 Java 检查${NC}"
        return
    fi
    
    echo -e "${YELLOW}  ℹ️  Java 代码检查请在项目目录运行 'mvn check' 或 'gradle check'${NC}"
    
    echo ""
}

# 测试检查
check_tests() {
    echo -e "${BLUE}🧪 检查测试...${NC}"
    
    # 统计各语言测试文件数量
    GO_TESTS=$(find go -name "*_test.go" 2>/dev/null | wc -l)
    PYTHON_TESTS=$(find python -name "test_*.py" -o -name "*_test.py" 2>/dev/null | wc -l)
    NODEJS_TESTS=$(find nodejs -name "*.test.js" 2>/dev/null | wc -l)
    JAVA_TESTS=$(find java -name "*Test.java" 2>/dev/null | wc -l)
    
    echo "  测试文件统计:"
    echo "    Go: $GO_TESTS 个"
    echo "    Python: $PYTHON_TESTS 个"
    echo "    Node.js: $NODEJS_TESTS 个"
    echo "    Java: $JAVA_TESTS 个"
    
    # 检查测试覆盖率（如果有）
    if [ -f "coverage/lcov.info" ] || [ -f ".coverage" ]; then
        echo -e "${GREEN}  ✅ 发现覆盖率报告${NC}"
    fi
    
    echo ""
}

# 安全检查
check_security() {
    echo -e "${BLUE}🔒 安全检查...${NC}"
    
    # 检查敏感信息
    if grep -r --include="*.py" --include="*.js" --include="*.go" --include="*.java" \
       -i "password\s*=\s*['\"][^'\"]\{8,\}['\"]" . 2>/dev/null | grep -v ".git"; then
        echo -e "${RED}  ❌ 发现可能的硬编码密码!${NC}"
        ERRORS=$((ERRORS + 1))
    else
        echo -e "${GREEN}  ✅ 未发现硬编码密码${NC}"
    fi
    
    # 检查 API Key
    if grep -r --include="*.py" --include="*.js" --include="*.go" --include="*.java" \
       -E "(api_key|apikey|api-key)\s*=\s*['\"][a-zA-Z0-9]{16,}['\"]" . 2>/dev/null | grep -v ".git"; then
        echo -e "${RED}  ❌ 发现可能的硬编码 API Key!${NC}"
        ERRORS=$((ERRORS + 1))
    else
        echo -e "${GREEN}  ✅ 未发现硬编码 API Key${NC}"
    fi
    
    echo ""
}

# 主函数
main() {
    check_python
    check_go
    check_nodejs
    check_java
    check_tests
    check_security
    
    # 总结
    echo "📊 质量门禁报告"
    echo "==============="
    echo ""
    
    if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✅ 所有检查通过！${NC}"
        exit 0
    elif [ $ERRORS -eq 0 ]; then
        echo -e "${YELLOW}⚠️  发现 $WARNINGS 个警告，建议修复${NC}"
        echo "   使用 --no-verify 跳过此检查"
        exit 0
    else
        echo -e "${RED}❌ 发现 $ERRORS 个错误，$WARNINGS 个警告${NC}"
        echo "   请修复错误后再提交"
        exit 1
    fi
}

main "$@"
