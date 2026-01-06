#!/bin/bash

# CRD清理脚本
# 用途：完全清理CRD和相关资源

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查kubectl
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl命令未找到"
        exit 1
    fi
}

# 删除自定义资源实例
delete_resources() {
    log_info "正在删除所有AppDeployment资源实例..."
    
    if kubectl get appdeployments &> /dev/null; then
        local count=$(kubectl get appdeployments --no-headers 2>/dev/null | wc -l)
        if [ "$count" -gt 0 ]; then
            log_info "找到 $count 个资源实例"
            kubectl delete appdeployments --all --timeout=60s
            log_info "资源实例删除完成"
        else
            log_info "未找到资源实例"
        fi
    else
        log_info "CRD未注册或无资源实例"
    fi
}

# 删除CRD定义
delete_crd() {
    log_info "正在删除CRD定义..."
    
    if kubectl get crd appdeployments.demo.opendemo.io &> /dev/null; then
        kubectl delete crd appdeployments.demo.opendemo.io --timeout=60s
        log_info "CRD删除完成"
    else
        log_info "CRD不存在，跳过删除"
    fi
}

# 验证清理结果
verify_cleanup() {
    log_info "正在验证清理结果..."
    
    sleep 2
    
    # 检查CRD
    if kubectl get crd appdeployments.demo.opendemo.io &> /dev/null; then
        log_warn "CRD仍然存在"
        return 1
    fi
    
    # 检查API资源
    if kubectl api-resources 2>/dev/null | grep -q appdeployment; then
        log_warn "API资源仍然注册"
        return 1
    fi
    
    log_info "清理验证通过，所有资源已删除"
    return 0
}

# 主函数
main() {
    echo "========================================"
    echo " CRD清理脚本"
    echo "========================================"
    echo ""
    
    check_kubectl
    
    # 确认操作
    log_warn "此操作将删除所有AppDeployment资源和CRD定义"
    read -p "是否继续？[y/N] " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "操作已取消"
        exit 0
    fi
    
    echo ""
    delete_resources
    
    echo ""
    delete_crd
    
    echo ""
    if verify_cleanup; then
        echo ""
        echo "========================================"
        log_info "清理成功完成！"
        echo "========================================"
    else
        echo ""
        echo "========================================"
        log_error "清理未完全成功，请手动检查"
        echo "========================================"
        exit 1
    fi
}

main "$@"
#!/bin/bash

# CRD清理脚本
# 用途：完全清理CRD和相关资源

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查kubectl
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl命令未找到"
        exit 1
    fi
}

# 删除自定义资源实例
delete_resources() {
    log_info "正在删除所有AppDeployment资源实例..."
    
    if kubectl get appdeployments &> /dev/null; then
        local count=$(kubectl get appdeployments --no-headers 2>/dev/null | wc -l)
        if [ "$count" -gt 0 ]; then
            log_info "找到 $count 个资源实例"
            kubectl delete appdeployments --all --timeout=60s
            log_info "资源实例删除完成"
        else
            log_info "未找到资源实例"
        fi
    else
        log_info "CRD未注册或无资源实例"
    fi
}

# 删除CRD定义
delete_crd() {
    log_info "正在删除CRD定义..."
    
    if kubectl get crd appdeployments.demo.opendemo.io &> /dev/null; then
        kubectl delete crd appdeployments.demo.opendemo.io --timeout=60s
        log_info "CRD删除完成"
    else
        log_info "CRD不存在，跳过删除"
    fi
}

# 验证清理结果
verify_cleanup() {
    log_info "正在验证清理结果..."
    
    sleep 2
    
    # 检查CRD
    if kubectl get crd appdeployments.demo.opendemo.io &> /dev/null; then
        log_warn "CRD仍然存在"
        return 1
    fi
    
    # 检查API资源
    if kubectl api-resources 2>/dev/null | grep -q appdeployment; then
        log_warn "API资源仍然注册"
        return 1
    fi
    
    log_info "清理验证通过，所有资源已删除"
    return 0
}

# 主函数
main() {
    echo "========================================"
    echo " CRD清理脚本"
    echo "========================================"
    echo ""
    
    check_kubectl
    
    # 确认操作
    log_warn "此操作将删除所有AppDeployment资源和CRD定义"
    read -p "是否继续？[y/N] " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "操作已取消"
        exit 0
    fi
    
    echo ""
    delete_resources
    
    echo ""
    delete_crd
    
    echo ""
    if verify_cleanup; then
        echo ""
        echo "========================================"
        log_info "清理成功完成！"
        echo "========================================"
    else
        echo ""
        echo "========================================"
        log_error "清理未完全成功，请手动检查"
        echo "========================================"
        exit 1
    fi
}

main "$@"
