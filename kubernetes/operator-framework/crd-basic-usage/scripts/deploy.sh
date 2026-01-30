#!/bin/bash

# CRD部署脚本
# 用途：将CRD定义部署到Kubernetes集群

set -e

# 颜色定义
RED='\033[0:31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# 检查kubectl是否可用
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl命令未找到，请先安装kubectl"
        exit 1
    fi
    log_info "kubectl已安装: $(kubectl version --client --short 2>/dev/null || kubectl version --client 2>&1 | head -n1)"
}

# 检查集群连接
check_cluster() {
    if ! kubectl cluster-info &> /dev/null; then
        log_error "无法连接到Kubernetes集群，请检查kubeconfig配置"
        exit 1
    fi
    log_info "成功连接到集群: $(kubectl config current-context)"
}

# 部署CRD
deploy_crd() {
    local crd_file="manifests/crd-definition.yaml"
    
    if [ ! -f "$crd_file" ]; then
        log_error "CRD定义文件不存在: $crd_file"
        exit 1
    fi
    
    log_info "正在部署CRD定义..."
    if kubectl apply -f "$crd_file"; then
        log_info "CRD部署成功"
    else
        log_error "CRD部署失败"
        exit 1
    fi
}

# 验证CRD
verify_crd() {
    log_info "正在验证CRD注册状态..."
    
    # 等待CRD就绪
    if kubectl wait --for condition=established --timeout=60s crd/appdeployments.demo.opendemo.io 2>/dev/null; then
        log_info "CRD已成功注册并就绪"
    else
        log_warn "CRD验证超时，但可能已经注册成功"
    fi
    
    # 显示CRD信息
    echo ""
    log_info "CRD详细信息:"
    kubectl get crd appdeployments.demo.opendemo.io -o wide
    
    # 检查API资源
    echo ""
    log_info "验证API资源可用性:"
    kubectl api-resources | grep appdeployment || log_warn "未找到appdeployment资源"
}

# 主函数
main() {
    echo "========================================"
    echo " CRD部署脚本"
    echo "========================================"
    echo ""
    
    check_kubectl
    check_cluster
    
    echo ""
    deploy_crd
    
    echo ""
    verify_crd
    
    echo ""
    echo "========================================"
    log_info "CRD部署完成！"
    echo "========================================"
    echo ""
    log_info "下一步操作:"
    echo "  1. 创建自定义资源: kubectl apply -f manifests/cr-example.yaml"
    echo "  2. 查看资源列表: kubectl get appdeployments"
    echo "  3. 查看资源详情: kubectl describe appdeployment <name>"
}

main "$@"
