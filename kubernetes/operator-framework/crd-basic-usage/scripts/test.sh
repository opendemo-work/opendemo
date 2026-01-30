#!/bin/bash

# CRD测试脚本
# 实现5层验证测试

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 计数器
PASS_COUNT=0
FAIL_COUNT=0

# 日志函数
log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASS_COUNT++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAIL_COUNT++))
}

# L1: 文件完整性检查
test_file_integrity() {
    echo ""
    echo "========== L1: 文件完整性检查 =========="
    
    local files=(
        "metadata.json"
        "README.md"
        "manifests/crd-definition.yaml"
        "manifests/cr-example.yaml"
        "scripts/deploy.sh"
        "scripts/cleanup.sh"
    )
    
    for file in "${files[@]}"; do
        log_test "检查文件: $file"
        if [ -f "$file" ]; then
            log_pass "文件存在"
        else
            log_fail "文件缺失: $file"
        fi
    done
}

# L2: YAML语法验证
test_yaml_syntax() {
    echo ""
    echo "========== L2: YAML语法验证 =========="
    
    log_test "验证CRD定义文件语法"
    if kubectl apply --dry-run=client -f manifests/crd-definition.yaml &> /dev/null; then
        log_pass "CRD语法正确"
    else
        log_fail "CRD语法错误"
    fi
    
    log_test "验证示例资源文件语法"
    # 先部署CRD才能验证CR
    kubectl apply -f manifests/crd-definition.yaml &> /dev/null || true
    sleep 2
    if kubectl apply --dry-run=client -f manifests/cr-example.yaml &> /dev/null; then
        log_pass "示例资源语法正确"
    else
        log_fail "示例资源语法错误"
    fi
}

# L3: API兼容性测试
test_api_compatibility() {
    echo ""
    echo "========== L3: API兼容性测试 =========="
    
    log_test "部署CRD到集群"
    if kubectl apply -f manifests/crd-definition.yaml &> /dev/null; then
        log_pass "CRD部署成功"
    else
        log_fail "CRD部署失败"
        return
    fi
    
    log_test "等待CRD就绪"
    if kubectl wait --for condition=established --timeout=30s crd/appdeployments.demo.opendemo.io &> /dev/null; then
        log_pass "CRD已就绪"
    else
        log_fail "CRD未能就绪"
    fi
    
    log_test "验证API资源注册"
    if kubectl api-resources | grep -q appdeployment; then
        log_pass "API资源已注册"
    else
        log_fail "API资源未注册"
    fi
}

# L4: 功能可用性测试
test_functionality() {
    echo ""
    echo "========== L4: 功能可用性测试 =========="
    
    log_test "创建自定义资源"
    if kubectl apply -f manifests/cr-example.yaml &> /dev/null; then
        log_pass "资源创建成功"
    else
        log_fail "资源创建失败"
        return
    fi
    
    sleep 2
    
    log_test "查询资源列表"
    if kubectl get appdeployments &> /dev/null; then
        log_pass "资源查询成功"
        echo "   资源列表:"
        kubectl get appdeployments | sed 's/^/   /'
    else
        log_fail "资源查询失败"
    fi
    
    log_test "测试资源更新"
    if kubectl patch appdeployment nginx-app -p '{"spec":{"replicas":5}}' --type=merge &> /dev/null; then
        log_pass "资源更新成功"
    else
        log_fail "资源更新失败"
    fi
    
    log_test "测试Schema验证（非法数据）"
    local invalid_yaml="apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: invalid-app
spec:
  replicas: 100
  image: nginx
  port: 80"
    
    if echo "$invalid_yaml" | kubectl apply -f - &> /dev/null; then
        log_fail "Schema验证未生效（应拒绝replicas=100）"
    else
        log_pass "Schema验证正常工作"
    fi
}

# L5: 清理完整性验证
test_cleanup() {
    echo ""
    echo "========== L5: 清理完整性验证 =========="
    
    log_test "删除自定义资源实例"
    if kubectl delete appdeployments --all --timeout=30s &> /dev/null; then
        log_pass "资源实例删除成功"
    else
        log_fail "资源实例删除失败"
    fi
    
    log_test "删除CRD定义"
    if kubectl delete crd appdeployments.demo.opendemo.io --timeout=30s &> /dev/null; then
        log_pass "CRD删除成功"
    else
        log_fail "CRD删除失败"
    fi
    
    sleep 2
    
    log_test "验证资源完全清理"
    if kubectl get crd appdeployments.demo.opendemo.io &> /dev/null; then
        log_fail "CRD残留未清理"
    else
        log_pass "CRD已完全清理"
    fi
}

# 环境检查
check_environment() {
    echo "========== 环境检查 =========="
    
    if ! command -v kubectl &> /dev/null; then
        log_fail "kubectl未安装"
        exit 1
    fi
    log_pass "kubectl已安装"
    
    if ! kubectl cluster-info &> /dev/null; then
        log_fail "无法连接到Kubernetes集群"
        exit 1
    fi
    log_pass "集群连接正常"
}

# 主函数
main() {
    echo "========================================"
    echo " CRD自动化测试脚本"
    echo "========================================"
    
    check_environment
    
    test_file_integrity
    test_yaml_syntax
    test_api_compatibility
    test_functionality
    test_cleanup
    
    echo ""
    echo "========================================"
    echo " 测试结果摘要"
    echo "========================================"
    echo -e "通过测试: ${GREEN}${PASS_COUNT}${NC}"
    echo -e "失败测试: ${RED}${FAIL_COUNT}${NC}"
    echo ""
    
    if [ $FAIL_COUNT -eq 0 ]; then
        echo -e "${GREEN}✓ 所有测试通过${NC}"
        exit 0
    else
        echo -e "${RED}✗ 存在测试失败${NC}"
        exit 1
    fi
}

main "$@"
